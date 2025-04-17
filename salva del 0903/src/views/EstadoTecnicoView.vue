<template>
    <img style="width: 250px ;" src="@/assets/Imagenes/mitrans.png">
  <Navbar-Component />
  
        <form class="d-flex" @submit.prevent="search_estado_tecnico" style="padding: 10px; margin-left: 75em;">
            <input class="form-control form-control-sm me-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery" @input="handleSearchInput" style="width: 200px;">
            
            
            <button  class="btn btn-outline-success btn-sm"  type="submit">Buscar</button>
        </form>
      
      <div style="margin-top: -4em;" >
        <br>
        <router-link style="text-decoration:none;  color:black;margin-right: 1330px;" to="/AdicionarEstadoTecnico" v-if="hasGroup('Admin')">Crear estado técnico <i class="bi bi-plus-circle"></i></router-link>
  <br>  
      </div>
  
  <br>
  
  <table class="table">
  <thead>
    <tr>
      <th scope="col">No</th>
      <th scope="col">Código</th>
      <th scope="col">Nombre</th>
      <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="(item, index) in estados_tecnicos" :key="item.id">
      <th scope="row" style="background-color: white;">{{ (index + 1) }}</th>      
      <td>{{ item.codigo_estado_tecnico }}</td>
      <td>{{ item.nombre_estado_tecnico }}</td>

      <td v-if="hasGroup('Admin')">
            <button @click.prevent="confirmDelete(item.codigo_estado_tecnico)" class="btn btn-danger">
              <i style="color: white" class="bi bi-trash"></i>
            </button>
            <button style="margin-left: 10px" class="btn btn-warning">
              <router-link :to="{ name: 'EditarEstadoTecnico', params: { id: item.codigo_estado_tecnico } }">
                <i style="color: white" class="bi bi-pencil-square"></i>
              </router-link>
            </button>
          </td>
    </tr>
  </tbody>
  </table>
  <h1 v-if="!busqueda_existente">No existe ningún registro asociado a ese parámetro de búsqueda</h1>
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
    name: 'EstadoTecnicoView',
  
    components:{
        NavbarComponent
    },
  
    data(){
        return{
            estados_tecnicos: [],
            searchQuery: '', // Añadido aquí
            debounceTimeout: null, // Añadido aquí
            busqueda_existente: true, // Variable para controlar la visibilidad del <h1> de la busqueda
            userPermissions: [], // Almacenará los permisos del usuario
            userGroups: [],      // Almacenará los grupos del usuario
        }
    },
  
    mounted() {
        this.get_estados_tecnicos()
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
    async get_estados_tecnicos(){
            this.$store.commit('setIsLoading', true)
  
            axios
                .get('/api/estados/')
                .then(response => {
                    this.estados_tecnicos = response.data
                })
                .catch(error => {
                    console.log(error)
                })
  
            this.$store.commit('setIsLoading', false)
        },
        //metodo para buscar registros en base al parametro de búsqueda
        async search_estado_tecnico() {
            this.$store.commit('setIsLoading', true);
  
            axios
            //aqui codigo_estado es el nombre que declaramos en el parametro al que se iguala la variable search
            //en la vista asociada al serializador del modelo en cuestion
                .get(`/api/estados/?codigo_estado=${this.searchQuery}`)
                .then(response => {
                    this.estados_tecnicos = response.data;
                    // Actualiza showH1 basado en el resultado
                    this.busqueda_existente = this.estados_tecnicos.length > 0;
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
              title: "¿Estás seguro?",
              text: "¡No podrás revertir esta acción!",
              icon: "warning",
              showCancelButton: true,
              confirmButtonText: "Sí, eliminar",
              cancelButtonText: "Cancelar",
              reverseButtons: true,
            }).then((result) => {
              if (result.isConfirmed) {
                this.delete_estado_tecnico(id);
              }
            });
          },
  
        handleSearchInput() {
            clearTimeout(this.debounceTimeout);
            this.debounceTimeout = setTimeout(() => {
                this.search_estado_tecnico();
            }, 300); // Ajusta el tiempo de espera según sea necesario
        },
  
        // Eliminar estado_tecnico 
        async delete_estado_tecnico(id) {
                    try {
                  await axios.delete(`/api/estados/${id}/`);  // Asegúrate de que la URL sea correcta
                  // Actualizar la lista de productos eliminando el que se ha borrado
                  this.estados_tecnicos = this.estados_tecnicos.filter(estado => estado.codigo_estado_tecnico !== id);

                  Swal.fire('Eliminado!', 'El estado ha sido eliminado exitosamente.', 'success');
              } catch (error) {
                  console.error("Error al eliminar el estado:", error);
                  Swal.fire('Error', 'Hubo un error al eliminar el estado.', 'error');
              }
            } 
    },
  
  
  }
</script>