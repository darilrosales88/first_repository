<template>
    <img style="width: 250px ;" src="@/assets/Imagenes/mitrans.png">
  <Navbar-Component />
  
        <form class="d-flex" @submit.prevent="search_grupo" style="padding: 10px; margin-left: 75em;">
            <input class="form-control form-control-sm me-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery" @input="handleSearchInput" style="width: 200px;">
            
            
            <button  class="btn btn-outline-success btn-sm"  type="submit">Search</button>
        </form>
      
      <div style="margin-top: -4em;" >
        <br>
        <router-link style="text-decoration:none;  color:black;margin-right: 1330px;" to="/create-group">Crear grupo <i class="bi bi-plus-circle"></i></router-link>
  <br>  
      </div>
  
  <br>
  
  <table class="table">
  <thead>
    <tr>
      <th scope="col">No</th>
      <th scope="col">Nombre</th>
      <th scope="col">Acciones</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="(item, index) in grupos" :key="item.id">
      <th scope="row" style="background-color: white;">{{ (index + 1) }}</th>
      <td>{{ item.name }}</td>
      <td>
        
        <button @click.prevent="confirmDelete(item.id)" class="btn btn-danger">         
        <i style="color:white" class="bi bi-trash"></i>
        </button> 
        <button style="margin-left:10px" class="btn btn-warning">
        <router-link :to="{name: 'EditGroup', params: {id:item.id}}">
        <i style="color:white" class="bi bi-pencil-square"></i>
        </router-link>
        </button>
          
      </td>
    </tr>
  </tbody>
  </table>
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
    name: 'GroupsView',
  
    components:{
        NavbarComponent
    },
  
    data(){
        return{
            grupos: [],
            searchQuery: '', // Añadido aquí
            debounceTimeout: null // Añadido aquí
        }
    },
  
    mounted() {
        this.get_grupos()
    },
  
   methods:{
    async get_grupos(){
            this.$store.commit('setIsLoading', true)
  
            axios
                .get('/apiAdmin/groups/')
                .then(response => {
                    console.log(response.data)
                    this.grupos = response.data
                })
                .catch(error => {
                    console.log("Error al obtener los grupos:",error)
                })
  
            this.$store.commit('setIsLoading', false)
        },
        async search_grupo() {
            this.$store.commit('setIsLoading', true);
  
            axios
                .get(`/apiAdmin/groups/?nombre_grupo=${this.searchQuery}`)
                .then(response => {
                    this.grupos = response.data;
                })
                .catch(error => {
                    console.log(error);
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
                    this.delete_group(id)
                }
            })
        },
  
        handleSearchInput() {
            clearTimeout(this.debounceTimeout);
            this.debounceTimeout = setTimeout(() => {
                this.search_grupo();
            }, 300); // Ajusta el tiempo de espera según sea necesario
        },
  
        // Eliminar grupo
        async delete_group(id) {
                try {
                    await axios.delete(`/apiAdmin/groups/${id}/`)
                    // Actualizar la lista de grupos eliminando el que se ha borrado
                    this.grupos = this.grupos.filter(grupo => grupo.id !== id)
                    Swal.fire('Eliminado!', 'El grupo ha sido eliminado exitosamente.', 'success')
                } catch (error) {
                    console.error("Error al eliminar el grupo:", error)
                    Swal.fire('Error', 'Hubo un error al eliminar el grupo.', 'error')
                }
            }  
     
    },  
    
  }
  </script>