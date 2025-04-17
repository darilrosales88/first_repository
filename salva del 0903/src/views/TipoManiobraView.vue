<template>
  <img style="width: 250px ;" src="@/assets/Imagenes/mitrans.png">

  <Navbar-Component />
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
        <button class="btn btn-outline-success btn-sm" type="submit">Buscar</button>
      </form>
      <br>
    </div>
  <br>
<router-link style="text-decoration:none;margin-right:1150px;color:black" to="/AdicionarManiobra" v-if="hasGroup('Admin')">Crear tipo de maniobra <i class="bi bi-plus-circle"></i></router-link>
<br>
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
        <button @click.prevent="confirmDelete(item.id)" class="btn btn-danger">         
            <i style="color:white" class="bi bi-trash"></i>
          </button> 
          <button style="margin-left:10px" class="btn btn-warning">
          <router-link :to="{name: 'EditarManiobra', params: {id:item.id}}">
            <i style="color:white" class="bi bi-pencil-square"></i>
          </router-link>
          </button>
      </td>
    </tr>
  </tbody>
</table>
<h1 v-if="!busqueda_existente">No existe ningún registro asociado a ese parámetro de búsqueda</h1>
</template>

<style scoped>

/*para el placeholder del buscador */
.search-container input::placeholder {
  font-size: 12px; /* Tamaño de la fuente más pequeño */
  color: #999;     /* Color del texto del placeholder */
}

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
