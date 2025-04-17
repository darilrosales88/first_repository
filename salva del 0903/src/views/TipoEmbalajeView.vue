<template>
  <div>
    <img style="width: 250px;" src="@/assets/Imagenes/mitrans.png">
    <NavbarComponent />

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
        <button class="btn btn-outline-success btn-sm" type="submit">Buscar</button>
      </form>
      <br>
    </div>

    <div style="margin-top: -4em;">
      <br>
      <router-link style="text-decoration:none; color:black; margin-right: 1330px;" to="/AdicionarTipoEmbalaje" v-if="hasGroup('Admin')">
        Crear embalaje <i class="bi bi-plus-circle"></i>
      </router-link>
      <br>
    </div>

    <br>

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
            <button @click.prevent="confirmDelete(item.id)" class="btn btn-danger">
              <i style="color:white" class="bi bi-trash"></i>
            </button>
            <button style="margin-left:10px" class="btn btn-warning">
              <router-link :to="{name: 'EditarTipoEmbalaje', params: {id:item.id}}">
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