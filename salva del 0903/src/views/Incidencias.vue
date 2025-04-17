<template>
  <div>
    <img style="width: 250px;" src="@/assets/Imagenes/mitrans.png" />
    <Navbar-Component />
    <br />

    <div class="search-container">
      <form class="d-flex search-form" @submit.prevent="search_incidencia">
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="Código o nombre"
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
      <br />
      <router-link
        style="text-decoration:none; color:black; margin-right: 1330px;"
        to="/CrearIncidencia"
        v-if="hasGroup('Admin')"
      >
        Crear incidencia <i class="bi bi-plus-circle"></i>
      </router-link>
      <br />
    </div>

    <br />

    <div class="table-responsive">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">No</th>
            <th scope="col">Código</th>
            <th scope="col">Incidencia</th>
            <th scope="col">Imputable</th>
            <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in incidencias" :key="item.id">
            <th scope="row" style="background-color: white;">{{ index + 1 }}</th>
            <td>{{ item.codigo_incidencia }}</td>
            <td>{{ item.nombre_incidencia }}</td>
            <td>{{ item.tipo_imputable_name }}</td>
            <td v-if="hasGroup('Admin')">
              <button @click.prevent="confirmDelete(item.id)" class="btn btn-danger">
                <i style="color:white" class="bi bi-trash"></i>
              </button>
              <button style="margin-left:10px" class="btn btn-warning">
                <router-link :to="{name: 'EditarIncidencia', params: {id:item.id}}">
                  <i style="color:white" class="bi bi-pencil-square"></i>
                </router-link>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <h1 v-if="!busqueda_existente">No existe ningún registro asociado a ese parámetro de búsqueda</h1>
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
  name: 'IncidenciasView',
  components: {
    NavbarComponent,
  },
  data() {
    return {
      incidencias: [],
      searchQuery: '', // Para la búsqueda
      debounceTimeout: null, // Para el debounce en la búsqueda
      busqueda_existente: true, // Controla la visibilidad del mensaje de búsqueda
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [],      // Almacenará los grupos del usuario
    };
  },

  async created() {
    // Obtener los permisos y grupos del usuario al cargar el componente
    await this.fetchUserPermissionsAndGroups();
    this.getIncidencias();
  },

  methods: {
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

    async getIncidencias() {
      this.$store.commit('setIsLoading', true);
      try {
        const response = await axios.get('/api/incidencias/');
        this.incidencias = response.data;
      } catch (error) {
        console.error('Error al obtener las incidencias:', error);
      }
      this.$store.commit('setIsLoading', false);
    },

    async search_incidencia() {
      this.$store.commit('setIsLoading', true);
      try {
        const response = await axios.get(`/api/incidencias/?nombre_codigo=${this.searchQuery}`);
        this.incidencias = response.data;
        this.busqueda_existente = this.incidencias.length > 0;
      } catch (error) {
        console.error('Error al buscar incidencias:', error);
        this.busqueda_existente = false;
      }
      this.$store.commit('setIsLoading', false);
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.search_incidencia();
      }, 300); // Ajusta el tiempo de espera según sea necesario
    },

    // Confirmar eliminación de una incidencia
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
          this.deleteIncidencia(id);
        }
      });
    },

    // Eliminar una incidencia
    async deleteIncidencia(id) {
      try {
        await axios.delete(`/api/incidencias/${id}/`);
        // Actualizar la lista de incidencias eliminando la que se ha borrado
        this.incidencias = this.incidencias.filter(incidencia => incidencia.id !== id);
        Swal.fire('Eliminado!', 'La incidencia ha sido eliminada exitosamente.', 'success');
      } catch (error) {
        console.error('Error al eliminar la incidencia:', error);
        Swal.fire('Error', 'Hubo un error al eliminar la incidencia.', 'error');
      }
    },
  },
};
</script>