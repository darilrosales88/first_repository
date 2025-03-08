<template>
  <div>
    <img style="width: 250px;" src="@/assets/Imagenes/mitrans.png">
    <Navbar-Component />

    <form class="d-flex" @submit.prevent="search_estructura" style="padding: 10px; margin-left: 75em;">
      <input class="form-control form-control-sm me-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery" @input="handleSearchInput" style="width: 200px;">
      <button class="btn btn-outline-success btn-sm" type="submit">Buscar</button>
    </form>

    <div style="margin-top: -4em;">
      <br>
      <router-link style="text-decoration:none;  color:black;margin-right: 1330px;" to="/AdicionarEstructura" v-if="hasGroup('Admin')">Crear estructura de ubicación&nbsp;<i class="bi bi-plus-circle"></i></router-link>
      <br>
    </div>

    <br>

    <div class="table-responsive">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">No</th>
            <th scope="col">Nombre</th>
            <th scope="col">Terminal</th>
            <th scope="col">Tipo de estructura</th>
            <th scope="col">Estructura padre</th>           
            <th scope="col">Capacidad</th>

            <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in estructuras" :key="item.id">
            <th scope="row" style="background-color: white;">{{ (index + 1) }}</th>
            <td>{{ item.nombre_estructura_ubicacion }}</td>
            <td>{{ item.terminal_name }}</td>
            <td>{{ item.tipo_estructura_name }}</td><!-- nacionalidad_name esta declarado en el serializador -->
            <td>{{ item.estructura_padre_name }}</td>            
            <td>{{ item.capacidad }}</td>
            <td v-if="hasGroup('Admin')">
              <button @click.prevent="confirmDelete(item.id)" class="btn btn-danger">
                <i style="color:white" class="bi bi-trash"></i>
              </button>
              <button style="margin-left:10px" class="btn btn-warning">
                <router-link :to="{name: 'EditarEstructura', params: {id:item.id}}">
                  <i style="color:white" class="bi bi-pencil-square"></i>
                </router-link>
              </button>
            </td>
          </tr>
        </tbody>
      </table>            
    </div>
    <h1 v-if="!busqueda_existente">No existe ningún registro asociado a ese parámetro de búsqueda.</h1>
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
</style>


<style scoped>


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
</style>

<script>
import Swal from 'sweetalert2'
import axios from 'axios';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'EmbarcacionView',

  components:{
      NavbarComponent
  },

  data(){
      return{
          estructuras: [],
          searchQuery: '', // Añadido aquí
          debounceTimeout: null, // Añadido aquí
          busqueda_existente: true, // Variable para controlar la visibilidad del <h1> de la busqueda
          userPermissions: [], // Almacenará los permisos del usuario
          userGroups: [],      // Almacenará los grupos del usuario
      }
  },

  mounted() {
      this.get_estructuras()
  },
  async created() {
        // Obtener los permisos y grupos del usuario al cargar el componente
        await this.fetchUserPermissionsAndGroups();
      },
 methods:{
  // Verifica si el usuario tiene un permiso específico
  hasPermission(permission) {
      if (!this.userPermissions) return false; // Verificación adicional
      return this.userPermissions.some(p => p.name === permission);
    },
    hasGroup(group) {
      if (!this.userGroups) return false; // Verificación adicional
      return this.userGroups.some(g => g.name === group);
    },
    // Obtiene los permisos y grupos del usuario desde el backend
    async fetchUserPermissionsAndGroups() {
      try {
        const userId = localStorage.getItem('userid');
        if (userId) {
          const response = await axios.get(`/apiAdmin/user/${userId}/permissions-and-groups/`);
          this.userPermissions = response.data.permissions || []; // Inicializa como array vacío si es undefined
          this.userGroups = response.data.groups || []; // Inicializa como array vacío si es undefined
        }
      } catch (error) {
        console.error('Error al obtener permisos y grupos:', error);
      }
    },
    async get_estructuras() {
    this.$store.commit('setIsLoading', true);

    try {
        const response = await axios.get('/api/estructuras_ubicacion/');
        console.log('Datos recibidos:', response.data);  // Verifica los datos recibidos
        this.estructuras = response.data;
    } catch (error) {
        console.error('Error al obtener las estructuras:', error);
    } finally {
        this.$store.commit('setIsLoading', false);
    }
},
      //metodo para buscar registros en base al parametro de búsqueda
      async search_estructura() {
          this.$store.commit('setIsLoading', true);

          axios
          //aqui nombre_embarcacion es el nombre que declaramos en el parametro al que se iguala la variable search
          //en la vista asociada al serializador del modelo en cuestion
              .get(`/api/estructuras_ubicacion/?nombre_estructura=${this.searchQuery}`)
              .then(response => {
                  this.estructuras = response.data;
                  // Actualiza showH1 basado en el resultado
                  this.busqueda_existente = this.estructuras.length > 0;
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
                  this.delete_embarcacion(id)
              }
          })
      },

      handleSearchInput() {
          clearTimeout(this.debounceTimeout);
          this.debounceTimeout = setTimeout(() => {
              this.search_estructura();
          }, 300); // Ajusta el tiempo de espera según sea necesario
      },

      // Eliminar embarcacion
      async delete_embarcacion(id) {
          try {
              await axios.delete(`/api/tipos_estructuras_ubicacion/${id}/`)
              // Actualizar la lista de estructuras eliminando el que se ha borrado
              this.estructuras = this.estructuras.filter(estructura => estructura.id !== id)

              Swal.fire('Eliminado!', 'La estructura ha sido eliminada exitosamente.', 'success')
            } catch (error) {
            
              console.error("Error al eliminar la estructura:", error)
              Swal.fire('Error', 'Hubo un error al eliminar la estructura.', 'error')
          }
      },     

  },


}
</script>