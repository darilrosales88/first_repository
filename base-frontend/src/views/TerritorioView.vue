<template>
  <div>
    <div style=" background-color: #003366; color: white; text-align: right;">
      <h6>Bienvenido: </h6>
    </div>  
    <br />
    <Navbar-Component />
    <br />
    <br />
  <div class="search-container">
      <form class="d-flex search-form" @submit.prevent="search_territorio">
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="nombre del territorio"
          aria-label="Buscar"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px;"
        />
      </form>
      <br>
    </div>

    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="AdicionarTerritorio">
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h6 style="margin-top: -31px; font-size: 19px;
    margin-right: 600px;">Listado de territorios:</h6>
    <br />
    <div class="table-container">
  <table class="table" :fields="territorios">
    <thead>
      <tr>
        <th scope="col">id</th>
        <th scope="col">Nombre</th>
        <th scope="col">Abreviatura</th>
        <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, index) in territorios" :key="item.id">
        <th scope="row" style="background-color: white;">{{ (index + 1) }}</th>
        <td>{{ item.nombre_territorio }}</td>
        <td>{{ item.abreviatura }}</td>
        <td v-if="hasGroup('Admin')">
          <button class="btn btn-warning btn-small">
                  <router-link :to="{name: 'EditarTerritorio', params: {id:item.id}}">
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
  padding: 0.15rem; /* Reducir el padding */
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
import NavbarComponent from "@/components/NavbarComponent.vue";
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "HomeView",
  components: {
    NavbarComponent,
  },

  data() {
    return {
      territorios: [],
      searchQuery: '',
      debounceTimeout: null,
      busqueda_existente: true,
      userPermissions: [],
      userGroups: [],
    };
  },

  mounted() {
    this.get_territorios();
  },

  async created() {
    await this.fetchUserPermissionsAndGroups();
  },

  methods: {
    hasPermission(permission) {
      return this.userPermissions.some(p => p.name === permission);
      },
    hasGroup(group) {
          return this.userGroups.some(g => g.name === group);
      },

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

    async get_territorios() {
      this.$store.commit('setIsLoading', true);

      try {
        const response = await axios.get('/api/territorios/');
        this.territorios = response.data;
      } catch (error) {
        console.error("Error al obtener territorios:", error);
      }

      this.$store.commit('setIsLoading', false);
    },

    async search_territorio() {
      this.$store.commit('setIsLoading', true);

      try {
        const response = await axios.get(`/api/territorios/?nomb_territorio=${this.searchQuery}`);
        this.territorios = response.data;
        this.busqueda_existente = this.territorios.length > 0;
      } catch (error) {
        console.error("Error al buscar territorios:", error);
        this.busqueda_existente = false;
      }

      this.$store.commit('setIsLoading', false);
    },

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
          this.deleteTerritorio(id);
        }
      });
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.search_territorio();
      }, 300);
    },

    async deleteTerritorio(id) {
      this.$store.commit("setIsLoading", true);
      
      try {
        await axios.delete(`/api/territorios/${id}/`);
        this.territorios = this.territorios.filter(territ => territ.id !== id);

        Swal.fire('Eliminado!', 'El territorio ha sido eliminado exitosamente.', 'success');
      } catch (error) {
        console.error("Error al eliminar el territorio:", error);
        Swal.fire('Error', 'Hubo un error al eliminar el territorio.', 'error');
      }

      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>
