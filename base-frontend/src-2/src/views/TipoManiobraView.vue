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
      <form class="d-flex search-form" @submit.prevent="searchDestinos">
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="nombre o tipo de maniobra"
          aria-label="Buscar"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px;"
        />
      </form>
    </div>
    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="AdicionarAtraque">
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h6 style="margin-top: -31px; font-size: 19px;
    margin-right: 630px;">Listado de tipos de maniobras:</h6>
    <br />
    <div class="table-container">
<table class="table">
  <thead>
    <tr>
      <th scope="col">No</th>
      <th scope="col">Nombre de la maniobra</th>
      <th scope="col">Tipo</th>
      <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="(item, index) in tipo_maniobras" :key="item.id">
      <th scope="row" style="background-color: white;">{{ item.id }}</th>
      <td>{{ item.nombre_maniobra }}</td>
      <td>{{ item.tipo_maniobra_description }}</td>
      <td v-if="hasGroup('Admin')">
        <button class="btn btn-warning btn-small">
                  <router-link :to="{name: 'EditarManiobra', params: {id:item.id}}">
                    <i style="color:white" class="bi bi-pencil-square"></i>
                  </router-link>
                </button>
                <button style="margin-left:10px" @click.prevent="confirmDelete(item.id)" class="btn btn-danger btn-small">
                  <i style="color:white" class="bi bi-trash"></i>
                </button>
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
import axios from 'axios';
import Swal from 'sweetalert2'
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'TipoManiobraView',
  components:{
    NavbarComponent
  },
  data(){
    return{
      tipo_maniobras: [],
      nombre_maniobra: '',
      tipo_maniobra: '',
      searchQuery: "", // Para la búsqueda
      busqueda_existente: true,
      debounceTimeout: null, // Para el debounce en la búsqueda
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [],      // Almacenará los grupos del usuario
        }
    },

    mounted() {
        this.getTipoManiobra()
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

    getTipoManiobra(){
      axios.get('api/tipo_maniobras/')
      .then(response =>{
        this.tipo_maniobras = response.data
      })
      .catch(error =>{
        console.log(error)
      })
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
                    this.deleteTManiobra(id)
                }
            })
        },

        async searchtipoEstructura() {
      this.$store.commit("setIsLoading", true);

      axios
        .get(`/api/tipo_maniobras/?nombre_y_tipo_maniobra=${this.searchQuery}`)
        .then((response) => {
          console.log('respuesta del server: ',response.data)
          this.tipo_maniobras = response.data;
          this.busqueda_existente = this.tipo_maniobras.length > 0;
        })
        .catch((error) => {
          console.log(error);
          this.busqueda_existente = false;
        });

      this.$store.commit("setIsLoading", false);
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchtipoEstructura();
      }, 300); // Ajusta el tiempo de espera según sea necesario
    },

        // Eliminar tipo_maniobra
        async deleteTManiobra(id) {
            try {
                await axios.delete(`/api/tipo_maniobras/${id}/`)
                // Actualizar la lista de tipos de maniobra eliminando el que se ha borrado
                this.tipo_maniobras = this.tipo_maniobras.filter(tmaniobra => tmaniobra.id !== id)
                Swal.fire('Eliminado!', 'El tipo de maniobra ha sido eliminado exitosamente.', 'success')
            } catch (error) {
                console.error("Error al eliminar el tipo de maniobra:", error)
                Swal.fire('Error', 'Hubo un error al eliminar el tipo de maniobra.', 'error')
            }
        }   
  }
}
</script>
