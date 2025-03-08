<template>
  <div>
    <img style="width: 250px;" src="@/assets/Imagenes/mitrans.png">
    <Navbar-Component />

    <div class="search-container">
      <form class="d-flex search-form" @submit.prevent="search_producto">
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="código,nombre,tipo de producto"
          aria-label="Search"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px;"
        />
        <button class="btn btn-outline-success btn-sm" type="submit">
          Buscar
        </button>
      </form>
    </div>

    <div style="margin-top: -4em;">
      <br>
      <router-link style="text-decoration:none;  color:black;margin-right: 1330px;" to="/CrearProducto" v-if="hasGroup('Admin')">Crear producto &nbsp;<i class="bi bi-plus-circle"></i></router-link>
      <br>
    </div>

    <br>

    <div class="table-responsive">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">No</th>
            <th scope="col">Código del producto</th>
            <th scope="col">Nombre</th>
            <th scope="col">Tipo</th>
            <th scope="col">Descripción</th>
            <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in productos" :key="item.id">
            <th scope="row" style="background-color: white;">{{ (index + 1) }}</th>
            <td>{{ item.codigo_producto }}</td>
            <td>{{ item.nombre_producto }}</td><!-- nacionalidad_name esta declarado en el serializador -->
            <td>{{ getTipoProductoText(item.tipo_producto) }}</td>
            <td>{{ item.descripcion }}</td>
            <td v-if="hasGroup('Admin')">
              <button @click.prevent="confirmDelete(item.id)" class="btn btn-danger">
                <i style="color:white" class="bi bi-trash"></i>
              </button>
              <button style="margin-left:10px" class="btn btn-warning">
                <router-link :to="{name: 'EditarProducto', params: {id:item.id}}">
                  <i style="color:white" class="bi bi-pencil-square"></i>
                </router-link>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <h1 v-if="!busqueda_existente">No existe ningún registro asociado a ese parámetro de búsqueda</h1>
  </div>
</template>

<style scoped>
.search-container {
  padding: 10px;
}

.search-form {
  display: flex;
  justify-content: flex-end;
  margin-left: auto;
}

@media (max-width: 768px) {
  .search-form {
    margin-left: auto;
    margin-right: 10px;
  }
}

th {
  background-color: #f2f2f2;
}

.btn {
  cursor: pointer;
  font-weight: bold;
}

.create-button-container {
  margin-top: -40px;
  text-align: left;
}

.create-button {
  text-decoration: none;
  color: black;
  padding-bottom: 2em;
}

@media (max-width: 768px) {
  .create-button-container {
    text-align: left;
    margin-right: 0;
  }
}

/*para el placeholder del buscador */
.search-container input::placeholder {
  font-size: 12px; /* Tamaño de la fuente más pequeño */
  color: #999;     /* Color del texto del placeholder */
}
</style>

<script>
import Swal from 'sweetalert2'
import axios from 'axios';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'ProductoView',

  components:{
      NavbarComponent
  },

  data(){
      return{
          productos: [],
          searchQuery: '', // Añadido aquí
          debounceTimeout: null, // Añadido aquí
          busqueda_existente: true, // Variable para controlar la visibilidad del <h1> de la busqueda
          userPermissions: [], // Almacenará los permisos del usuario
          userGroups: [],      // Almacenará los grupos del usuario
      }
  },

  mounted() {
      this.get_productos()
  },
  async created() {
        // Obtener los permisos y grupos del usuario al cargar el componente
        await this.fetchUserPermissionsAndGroups();
      },
 methods:{
  // Verifica si el usuario tiene un permiso específico
  hasPermission(permission) {
      return this.userPermissions.some(p => p.name === permission);
      },
    hasGroup(group) {
          return this.userGroups.some(g => g.name === group);
      },
    // Obtiene los permisos y grupos del usuario desde el backend
    async fetchUserPermissionsAndGroups() {
      try {
        const userId = localStorage.getItem('userid');
        if (userId) {
          const response = await axios.get(`/apiAdmin/user/${userId}/permissions-and-groups/`);
          this.userPermissions = response.data.permissions;
          this.userGroups = response.data.groups;          
        }
      } catch (error) {
        console.error('Error al obtener permisos y grupos:', error);
      }
    },
  async get_productos(){
          this.$store.commit('setIsLoading', true)

          axios
              .get('/api/productos/')
              .then(response => {
                  this.productos = response.data
              })
              .catch(error => {
                  console.log(error)
              })

          this.$store.commit('setIsLoading', false)
      },
      //metodo para buscar registros en base al parametro de búsqueda
      async search_producto() {
          this.$store.commit('setIsLoading', true);

          axios
          //aqui nombre_descripcion_codigo_producto es el nombre que declaramos en el parametro al que se iguala la variable search
          //en la vista asociada al serializador del modelo en cuestion
              .get(`/api/productos/?nombre_tipo_codigo_producto=${this.searchQuery}`)
              .then(response => {
                  this.productos = response.data;
                  // Actualiza showH1 basado en el resultado
                  this.busqueda_existente = this.productos.length > 0;
              })
              .catch(error => {
                  console.log(error);
                  this.busqueda_inexistente = false; // Asegura que busqueda_inexistente sea false en caso de error
              });

          this.$store.commit('setIsLoading', false);
      },
              
      // Usar SweetAlert2 para confirmar la eliminación
      confirmDelete(id) {
          Swal.fire({
              title: '¿Estás seguro?',
              text: '¡No podrás revertir esta acción!',
              icon: 'warning',
              showCancelButton: true,
              confirmButtonText: 'Sí, eliminar',
              cancelButtonText: 'Cancelar',
              reverseButtons: true
          }).then((result) => {
              if (result.isConfirmed) {
                  this.delete_produto(id)
              }
          })
      },

      handleSearchInput() {
          clearTimeout(this.debounceTimeout);
          this.debounceTimeout = setTimeout(() => {
              this.search_producto();
          }, 300); // Ajusta el tiempo de espera según sea necesario
      },

      // Eliminar producto
      async delete_produto(id) {
          try {
              await axios.delete(`/api/productos/${id}/`)
              // Actualizar la lista de productos eliminando el que se ha borrado
              this.productos = this.productos.filter(producto => producto.id !== id)

              Swal.fire('Eliminado!', 'El producto ha sido eliminado exitosamente.', 'success')
            } catch (error) {
            
              console.error("Error al eliminar el producto:", error)
              Swal.fire('Error', 'Hubo un error al eliminar el producto.', 'error')
          }
      },

      //funcion para que sea mostrado el texto asociado al valor del select
      getTipoProductoText(value) {
            const tipos_productos = {
              'alimento': 'Alimento',
              'combustible': 'Combustible',
              'otros': 'Otros',
     
            };
            return tipos_productos[value] || 'Desconocido';
        },       

  },


}
</script>