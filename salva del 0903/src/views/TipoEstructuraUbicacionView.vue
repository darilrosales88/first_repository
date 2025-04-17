<template>
  <div>
    <img style="width: 250px;" src="@/assets/Imagenes/mitrans.png" />
    <Navbar-Component />
    <div class="search-container">
      <form
        class="d-flex"
        @submit.prevent="searchTipoEstructura"
        style="padding: 10px; margin-left: 65em"
      >
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="Tipo de estructura"
          aria-label="Search"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px"
        />
        <button class="btn btn-outline-success btn-sm" type="submit">Buscar</button>
      </form>
    </div>
    <!-- Mostrar el botón "Crear nueva ubicación" solo si el usuario pertenece al grupo "Admin" -->
    <router-link
      v-if="hasGroup('Admin')"
      style="text-decoration:none; margin-right:1150px; color:black"
      to="/CrearTipoUbicacion"
    >
      Crear nueva ubicación <i class="bi bi-plus-circle"></i>
    </router-link>
    <br />
    <table class="table">
      <thead>
        <tr>
          <th scope="col">No</th>
          <th scope="col">Tipo de estructura de ubicación</th>
          <!-- Mostrar la columna "Acciones" solo si el usuario pertenece al grupo "Admin" -->
          <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in tipos_estructura_ubicacion" :key="item.id">
          <th scope="row" style="background-color: white;">{{ index + 1 }}</th>
          <td>{{ item.nombre_tipo_estructura_ubicacion }}</td>
          <!-- Mostrar los botones de acciones solo si el usuario pertenece al grupo "Admin" -->
          <td v-if="hasGroup('Admin')">
            <button class="btn btn-danger" @click="confirmDelete(item.id)">
              <i style="color:white" class="bi bi-trash"></i>
            </button>
            <button style="margin-left:10px" class="btn btn-warning">
              <router-link :to="{ name: 'EditarTipoUbicacion', params: { id: item.id } }">
                <i style="color:white" class="bi bi-pencil-square"></i>
              </router-link>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <h1 v-if="!busqueda_existente">No existe ningún registro asociado a ese parámetro de búsqueda</h1>
  </div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'TipoEstructuraUbicacionView',
  components: {
    NavbarComponent,
  },
  data() {
    return {
      tipos_estructura_ubicacion: [], // Almacena los tipos de estructura de ubicación
      searchQuery: "", // Para la búsqueda
      busqueda_existente: true,
      debounceTimeout: null, // Para el debounce en la búsqueda
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [],      // Almacenará los grupos del usuario
    };
  },

  async created() {
    // Obtener los permisos y grupos del usuario al cargar el componente
    await this.fetchUserPermissionsAndGroups();
    this.getTiposEstructuraUbicacion();
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

    // Obtener los tipos de estructura de ubicación
    async getTiposEstructuraUbicacion() {
      try {
        const response = await axios.get('/api/tipos_estructuras_ubicacion/');
        this.tipos_estructura_ubicacion = response.data;
      } catch (error) {
        console.error('Error al obtener los tipos de estructura de ubicación:', error);
        Swal.fire('Error', 'No se pudieron cargar los tipos de estructura de ubicación.', 'error');
      }
    },

    async searchTipoEstructura() {
      try {
        const response = await axios.get(`/api/tipos_estructuras_ubicacion/?nombre_tipo_estructura_ubicacion=${this.searchQuery}`);
        this.tipos_estructura_ubicacion = response.data;
        this.busqueda_existente = this.tipos_estructura_ubicacion.length > 0;
      } catch (error) {
        console.error('Error al buscar tipos de estructura de ubicación:', error);
        this.busqueda_existente = false;
      }
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchTipoEstructura();
      }, 300); // Ajusta el tiempo de espera según sea necesario
    },

    // Confirmar eliminación de un tipo de estructura de ubicación
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
          this.deleteTipoEstructuraUbicacion(id);
        }
      });
    },

    // Eliminar un tipo de estructura de ubicación
    async deleteTipoEstructuraUbicacion(id) {
      try {
        await axios.delete(`/api/tipos_estructuras_ubicacion/${id}/`);
        Swal.fire('Eliminado!', 'El tipo de estructura de ubicación ha sido eliminado exitosamente.', 'success');
        this.getTiposEstructuraUbicacion(); // Recargar la lista después de eliminar
      } catch (error) {
        console.error('Error al eliminar el tipo de estructura de ubicación:', error);
        Swal.fire('Error', 'Hubo un error al eliminar el tipo de estructura de ubicación.', 'error');
      }
    },
  },
};
</script>

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