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
      <form class="d-flex search-form" @submit.prevent="searchEquipo">
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="Buscar por tipo, número o territorio"
          aria-label="Buscar"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px;"
        />
      </form>
    </div>

    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="AdicionarEquipo">
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h6 style="margin-top: -31px; font-size: 19px;
    margin-right: 630px;">Listado de equipos ferroviarios:</h6>
    <br />

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th scope="col" v-if="showNoId">No</th>
            <th scope="col">Tipo de equipo</th>
            <th scope="col">No. de identificación</th>
            <th scope="col">Territorio</th>
            <th scope="col" v-if="showNoId">Tipo de carga</th>
            <th scope="col">Tipo de combustible</th>
            <th scope="col" v-if="showNoId">Peso</th>
            <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in equiposFiltrados" :key="item.id">
            <th scope="row" v-if="showNoId">{{ index + 1 }}</th>
            <td>{{ item.tipo_equipo_name }}</td>
            <td>{{ item.numero_identificacion }}</td>
            <td>{{ item.territorio_name }}</td>
            <td v-if="showNoId">{{ item.tipo_carga }}</td>
            <td>{{ item.tipo_combustible }}</td>
            <td v-if="showNoId">{{ item.peso_maximo }}</td>
            <td v-if="hasGroup('Admin')">
              <button @click="toggleNoIdVisibility" class="btn btn-info btn-small btn-eye" 
              v-html="showNoId ? '<i class=\'bi bi-eye-slash-fill\'></i>' : '<i class=\'bi bi-eye-fill\'></i>'">
              </button>
              <span v-if="hasGroup('Admin')">
                <button class="btn btn-warning btn-small">
                  <router-link :to="{name: 'EditarEquipo', params: {id:item.id}}">
                    <i style="color:white" class="bi bi-pencil-square"></i>
                  </router-link>
                </button>
                <button style="margin-left:10px" @click.prevent="confirmDelete(item.id)" class="btn btn-danger btn-small">
                  <i style="color:white" class="bi bi-trash"></i>
                </button>
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Mensaje cuando no hay resultados -->
    <h1 v-if="equiposFiltrados.length === 0 && searchQuery">
      No existe ningún registro asociado a ese parámetro de búsqueda.
    </h1>
  </div>
</template>

<script>
import Swal from 'sweetalert2';
import axios from 'axios';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'EquipoFerroView',
  components: {
    NavbarComponent,
  },
  data() {
    return {
      equipos: [], // Lista completa de equipos
      equiposFiltrados: [], // Lista filtrada de equipos
      searchQuery: '', // Término de búsqueda
      debounceTimeout: null, // Timeout para el debounce
      userPermissions: [], // Permisos del usuario
      userGroups: [], // Grupos del usuario
      showNoId: false,
    };
  },
  async created() {
    await this.fetchUserPermissionsAndGroups();
    await this.getEquipos();
  },
  methods: {
    toggleNoIdVisibility() {
      this.showNoId = !this.showNoId; // Alternar la visibilidad de las columnas No e Id
    },
    // Verifica si el usuario tiene un permiso específico
    hasPermission(permission) {
      return this.userPermissions.some(p => p.name === permission);
    },
    // Verifica si el usuario pertenece a un grupo específico
    hasGroup(group) {
      return this.userGroups.some(g => g.name === group);
    },
    // Obtiene los permisos y grupos del usuario
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
    // Obtiene todos los equipos
    async getEquipos() {
      try {
        const response = await axios.get('/api/equipos_ferroviarios/');
        this.equipos = response.data;
        this.equiposFiltrados = this.equipos; // Inicialmente, muestra todos los equipos
      } catch (error) {
        console.error('Error al obtener los equipos:', error);
        Swal.fire('Error', 'No se pudieron cargar los equipos.', 'error');
      }
    },
    // Filtra los equipos según el término de búsqueda
    searchEquipo() {
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        this.equiposFiltrados = this.equipos.filter(
          (equipo) =>
            equipo.tipo_equipo_name.toLowerCase().includes(query) ||
            equipo.numero_identificacion.toLowerCase().includes(query) ||
            equipo.territorio_name.toLowerCase().includes(query)
        );
      } else {
        this.equiposFiltrados = this.equipos; // Si no hay búsqueda, muestra todos
      }
    },
    // Debounce para evitar múltiples llamadas durante la escritura
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchEquipo();
      }, 300);
    },
    // Confirma la eliminación de un equipo
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
          this.deleteEquipo(id);
        }
      });
    },
    // Elimina un equipo
    async deleteEquipo(id) {
      try {
        await axios.delete(`/api/equipos_ferroviarios/${id}/`);
        this.equipos = this.equipos.filter(equipo => equipo.id !== id);
        this.equiposFiltrados = this.equiposFiltrados.filter(equipo => equipo.id !== id);
        Swal.fire('Eliminado!', 'El equipo ha sido eliminado exitosamente.', 'success');
      } catch (error) {
        console.error('Error al eliminar el equipo:', error);
        Swal.fire('Error', 'Hubo un error al eliminar el equipo.', 'error');
      }
    },
  },
};
</script>

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
