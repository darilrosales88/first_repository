<template>
    <div>
      <img style="width: 250px;" src="@/assets/Imagenes/mitrans.png">
      <user_autenticado />
      <Navbar-Component />
  
      <div class="search-container">
      <form class="d-flex search-form" @submit.prevent="searchProvincias">
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="nombre de provincia"
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
        <router-link style="text-decoration:none; color:black; margin-right: 1330px;" to="/AdicionarProvincia" v-if="hasGroup('Admin')">Crear provincia <i class="bi bi-plus-circle"></i></router-link>
        <br>
      </div>
      <br>
  
      <table class="table">
        <thead>
          <tr>
            <th scope="col">No</th>
            <th scope="col">Código</th>
            <th scope="col">Nombre de la provincia</th>
            <th scope="col">País</th>
            <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in provincias" :key="item.id">
            <th scope="row" style="background-color: white">{{ (index + 1) }}</th>
            <td>{{ item.codigo }}</td>
            <td>{{ item.nombre_provincia }}</td>
            <td>{{ item.nombre_pais }}</td>
            <td v-if="hasGroup('Admin')">
              <button @click.prevent="confirmDelete(item.id)" class="btn btn-danger">
                <i style="color:white" class="bi bi-trash"></i>
              </button>
              <button style="margin-left:10px" class="btn btn-warning">
                <router-link :to="{name: 'EditarProvincia', params: {id:item.id}}">
                  <i style="color:white" class="bi bi-pencil-square"></i>
                </router-link>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
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
import Swal from 'sweetalert2';
import axios from 'axios';
import NavbarComponent from '@/components/NavbarComponent.vue';
import user_autenticado from '@/components/user_autenticado.vue';

export default {
  name: 'ProvinciaView',
  components: {
    user_autenticado,
    NavbarComponent
  },
  data() {
    return {
      provincias: [],
      searchQuery: '',
      busqueda_existente: true,
      debounceTimeout: null,
      userPermissions: [],
      userGroups: [],
      user_autenticado: '',
    };
  },
  mounted() {
    this.getProvincias();
  },
  async created() {
    await this.fetchUserPermissionsAndGroups();
  },
  methods: {
    // Verifica si el usuario tiene un permiso específico
    hasPermission(permission) {
      return this.userPermissions.some(p => p.name === permission);
    },
    // Verifica si el usuario pertenece a un grupo específico
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
    async getProvincias() {
      this.$store.commit('setIsLoading', true);
      axios.get('/api/provincias/')
        .then(response => {
          this.provincias = response.data;
        })
        .catch(error => {
          console.log(error);
        });
      this.$store.commit('setIsLoading', false);
    },
    async searchProvincias() {
      this.$store.commit('setIsLoading', true);
      axios.get(`/api/provincias/?nombre_prov=${this.searchQuery}`)
        .then(response => {
          this.provincias = response.data;
          this.busqueda_existente = this.provincias.length > 0;
        })
        .catch(error => {
          console.log(error);
          this.busqueda_existente = false;
        });
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
          this.deleteProvincia(id);
        }
      });
    },
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchProvincias();
      }, 300);
    },
    async deleteProvincia(id) {
      try {
        await axios.delete(`/api/provincias/${id}/`);
        this.provincias = this.provincias.filter(provincia => provincia.id !== id);
        Swal.fire('Eliminado!', 'La provincia ha sido eliminada exitosamente.', 'success');
      } catch (error) {
        console.error("Error al eliminar la provincia:", error);
        Swal.fire('Error', 'Hubo un error al eliminar la provincia.', 'error');
      }
    },
  },
};
</script>