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
      <form class="d-flex search-form" @submit.prevent="searchEmbalajes">
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="tipo de embalaje"
          aria-label="Buscar"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px;"
        />
      </form>
    </div>
    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="AdicionarTipoEmbalaje">
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h6 style="margin-top: -31px; font-size: 19px;
    margin-right: 630px;">Listado de tipos de embalajes:</h6>
    <br />
    <div class="table-container">
    <table class="table">
      <thead>
        <tr>
          <th scope="col">No</th>
          <th scope="col">Forma de presentación</th>
          <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in embalajes" :key="item.id">
          <th scope="row" style="background-color: white;">{{ (index + 1) }}</th>
          <td>{{ item.nombre_tipo_embalaje }}</td>
          <td v-if="hasGroup('Admin')">
            <button class="btn btn-warning btn-small">
                  <router-link :to="{name: 'EditarTipoEmbalaje', params: {id:item.id}}">
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
import Swal from 'sweetalert2';
import axios from 'axios';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'TipoEmbalajeView',
  components: {
    NavbarComponent,
  },
  data() {
    return {
      embalajes: [],
      searchQuery: '',
      debounceTimeout: null,
      busqueda_existente: true,
      userPermissions: [],
      userGroups: [],
    };
  },
  mounted() {
    this.get_embalajes();
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
    // Obtiene la lista de embalajes
    async get_embalajes() {
      this.$store.commit('setIsLoading', true);
      try {
        const response = await axios.get('/api/embalajes/');
        this.embalajes = response.data;
      } catch (error) {
        console.error('Error al obtener embalajes:', error);
      }
      this.$store.commit('setIsLoading', false);
    },
    // Busca embalajes según el término de búsqueda
    async searchEmbalajes() {
      this.$store.commit('setIsLoading', true);
      try {
        const response = await axios.get(`/api/embalajes/?nombre_tipo_embalaje=${this.searchQuery}`);
        this.embalajes = response.data;
        this.busqueda_existente = this.embalajes.length > 0;
      } catch (error) {
        console.error('Error al buscar embalajes:', error);
        this.busqueda_existente = false;
      }
      this.$store.commit('setIsLoading', false);
    },
    // Confirma la eliminación de un embalaje
    confirmDelete(id) {
      Swal.fire({
        title: '¿Estás seguro?',
        text: '¡No podrás revertir esta acción!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
        reverseButtons: true,
      }).then((result) => {
        if (result.isConfirmed) {
          this.deleteEmbalaje(id);
        }
      });
    },
    // Maneja la entrada de búsqueda con debounce
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchEmbalajes();
      }, 300);
    },
    // Elimina un embalaje
    async deleteEmbalaje(id) {
      try {
        await axios.delete(`/api/embalajes/${id}/`);
        this.embalajes = this.embalajes.filter(embalaje => embalaje.id !== id);
        Swal.fire('Eliminado!', 'El tipo de embalaje ha sido eliminado exitosamente.', 'success');
      } catch (error) {
        console.error('Error al eliminar el tipo de embalaje:', error);
        Swal.fire('Error', 'Hubo un error al eliminar el tipo de embalaje.', 'error');
      }
    },
  },
};
</script>