<template>
  <img style="width: 250px" src="@/assets/Imagenes/mitrans.png" />
  <NavbarComponent />
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
        <button class="btn btn-outline-success btn-sm" type="submit">Buscar</button>
      </form>
      <br>
    </div>

  <div class="create-button-container">
    <router-link class="create-button" to="AdicionarTerritorio" v-if="hasGroup('Admin')">
      Crear Territorio <i class="bi bi-plus-circle"></i>
    </router-link>
  </div>
  <br />
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
          <button @click.prevent="confirmDelete(item.id)" class="btn btn-danger">
            
            <i style="color:white" class="bi bi-trash"></i>
          </button>
              <button style="margin-left:10px" class="btn btn-warning">
                <router-link :to="{name: 'EditarTerritorio', params: {id:item.id}}">
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
