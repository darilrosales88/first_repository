<template>
  <div>
    <div style=" background-color: #003366; color: white; text-align: right;">
      <h6>Bienvenido: Admin autenticado</h6>
    </div>  
    <br />
    <Navbar-Component />
    <br />
    <br />

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
      </form>
    </div>

    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="CrearProducto">
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h6 style="margin-top: -31px; font-size: 19px;
    margin-right: 630px;">Listado de productos:</h6>
    <br />
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th scope="col" v-if="showNoId">No</th>
            <th scope="col">Código del producto</th>
            <th scope="col">Nombre</th>
            <th scope="col">Tipo</th>
            <th scope="col" v-if="showNoId">Descripción</th>
            <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in productos" :key="item.id">
            <th v-if="showNoId" scope="row" style="background-color: white;">{{ (index + 1) }}</th>
            <td>{{ item.codigo_producto }}</td>
            <td>{{ item.nombre_producto }}</td><!-- nacionalidad_name esta declarado en el serializador -->
            <td>{{ getTipoProductoText(item.tipo_producto) }}</td>
            <td v-if="showNoId">{{ item.descripcion }}</td>
            <td v-if="hasGroup('Admin')">
              <button @click="toggleNoIdVisibility" class="btn btn-info btn-small btn-eye" 
              v-html="showNoId ? '<i class=\'bi bi-eye-slash-fill\'></i>' : '<i class=\'bi bi-eye-fill\'></i>'">
              </button>
              <span v-if="hasGroup('Admin')">
                <button class="btn btn-warning btn-small">
                  <router-link :to="{name: 'EditarProducto', params: {id:item.id}}">
                    <i style="color:white" class="bi bi-pencil-square"></i>
                  </router-link>
                </button>
                <button style="margin-left:10px" @click.prevent="confirmDelete(item.id)" class="btn btn-danger btn-small">
                  <i style="color:white" class="bi bi-trash"></i>
                </button>
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    <h1 v-if="!busqueda_existente">No existe ningún registro asociado a ese parámetro de búsqueda</h1>
  </div>
  </div>
</template>

<style scoped>

.search-container input::placeholder {
  font-size: 12px; 
  color: #999;   
}

body {
  overflow: scroll;
}

.search-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 5px;
}

.table-container {
  overflow-x: auto;
  max-width: 100%;
}
.large-icon {
  font-size: 1.7rem; /* Tamaño del ícono */
}
table {
  width: 84%;
  border-collapse: collapse;
  margin-left: 190px;
  margin-bottom: 20px;
  font-size: 0.875rem;
  min-width: 300px;
}

th, td {
  padding: 0.5rem;
  white-space: nowrap;
}

th {
  background-color: #f2f2f2;
}

.btn {
  cursor: pointer;
  font-weight: bold;
}

.btn-small {
  padding: 0.25rem 0.45rem;
  font-size: 0.875rem;
}
.btn-eye {
  background-color: rgb(0, 71, 163);
  margin-right: 10px;
  color: white;
  border: none;
}

.create-button-container {
  margin-top: -40px;
  text-align: left;
}

.create-button {
  text-decoration: none;
  color: green;
  margin-left: 940px;
}

@media (max-width: 768px) {
  .create-button-container {
    text-align: left;
    margin-right: 0;
  }
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
          showNoId: false,
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
  toggleNoIdVisibility() {
      this.showNoId = !this.showNoId; // Alternar la visibilidad de las columnas No e Id
    },
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