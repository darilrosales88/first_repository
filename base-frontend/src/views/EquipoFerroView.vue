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
      <form class="d-flex search-form" @submit.prevent="searchEquipo">
        <div class="input-container">
          <i class="bi bi-search"></i> 
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="Buscar por tipo, número o territorio"
          aria-label="Buscar"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px; padding-left: 5px;margin-top: -70px;" 
        />
      </div>
      </form>
    </div>

    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="AdicionarEquipo">
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h3 style="margin-top: -33px; font-size: 18px;
    margin-right: 530px;color: #002A68;">Listado de equipos ferroviarios</h3>
    <br />

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Tipo de equipo</th>
            <th scope="col">No. de identificación</th>
            <th scope="col">Territorio</th>
            <th scope="col">Tipo de carga</th>
            <th scope="col">Tipo de combustible</th>
            <th scope="col">Peso</th>
            <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item) in equiposFiltrados" :key="item.id">
            <td>{{ item.tipo_equipo_name }}</td>
            <td>{{ item.numero_identificacion }}</td>
            <td>{{ item.territorio_name }}</td>
            <td>{{ item.tipo_carga }}</td>
            <td>{{ item.tipo_combustible }}</td>
            <td>{{ item.peso_maximo }}</td>
            <td >
              <button @click="openEquipoFerroDetailsModal(item)" class="btn btn-info btn-small btn-eye" 
              v-html="showNoId ? '<i class=\'bi bi-eye-slash-fill\'></i>' : '<i class=\'bi bi-eye-fill\'></i>'">
              </button>
              <span v-if="hasGroup('Admin')">
                <button class="btn btn-warning btn-small">
                  <router-link :to="{name: 'EditarEquipo', params: {id:item.id}}">
                    <i style="color:black" class="bi bi-pencil-square"></i>
                  </router-link>
                </button>
                <button  @click.prevent="confirmDelete(item.id)" class="btn btn-danger btn-small">
                  <i  class="bi bi-trash"></i>
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
    openEquipoFerroDetailsModal(EquipoFerro) {
    // Mapear IDs de grupos a nombres
    const gruposAsignados = EquipoFerro.groups && EquipoFerro.groups.length > 0
        ? EquipoFerro.groups
            .map(groupId => {
                const grupo = this.gruposDisponibles.find(g => g.id === groupId);
                return grupo ? grupo.name : 'Desconocido';
            })
            .join(', ')
        : 'Ninguno';

    // Mapear IDs de permisos a nombres
    const permisosAsignados = EquipoFerro.EquipoFerro_permissions && EquipoFerro.EquipoFerro_permissions.length > 0
        ? EquipoFerro.EquipoFerro_permissions
            .map(permisoId => {
                const permiso = this.permisosDisponibles.find(p => p.id === permisoId);
                return permiso ? permiso.name : 'Desconocido';
            })
            .join(', ')
        : 'Ninguno';

    Swal.fire({
        title: 'Detalles del Atraque',
        html: `
            <div style="text-align: left;">
                <p><strong>Tipo de equipo:</strong> ${EquipoFerro.tipo_equipo_name}</p>
                <p><strong>No. de identificación:</strong> ${EquipoFerro.numero_identificacion}</p>
                <p><strong>Territorio:</strong> ${EquipoFerro.territorio_name}</p>
                <p><strong>Tipo de carga:</strong> ${EquipoFerro.tipo_carga}</p>
                <p><strong>Tipo de combustible:</strong> ${EquipoFerro.tipo_combustible}</p>
                <p><strong>Peso:</strong> ${EquipoFerro.peso_maximo}</p>
                
            </div>
        `,
        width: '600px',
        customClass: {
            popup: 'custom-swal-popup',
            title: 'custom-swal-title',
            htmlContainer: 'custom-swal-html',
        },
    });
},
  },
};
</script>

<style scoped>

.search-container input::placeholder {
  font-size: 14px; 
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
.input-container {
  position: relative;
  display: inline-block;
}

.input-container .bi {
  position: absolute;
  left: 180px;
  color: #999;
  margin-top: -55px;
  transform: translateY(-50%);
  pointer-events: none; /* Para que el ícono no interfiera con el clic en el input */
}
.large-icon {
  font-size: 1.7rem; /* Tamaño del ícono */
}
table {
  width: 84%;
  border-collapse: collapse;
  margin-left: 190px;
  margin-bottom: 10px;
  font-size: 0.875rem;
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
}

.btn-small {
  font-size: 22px; /* Aumenta el tamaño del ícono */
  color: black;
  margin-right: 5px;
  outline: none; /* Elimina el borde de foco */
  border: none;
  background: none; /* Elimina el fondo */
  padding: 0; /* Elimina el padding para que solo se vea el ícono */
}
.btn-eye {
  font-size: 22px; /* Aumenta el tamaño del ícono */
  margin-right: 5px;
  outline: none; /* Elimina el borde de foco */
  border: none;
  background: none; /* Elimina el fondo */
  padding: 0; /* Elimina el padding para que solo se vea el ícono */
}
.btn:hover {
  background: none; /* Asegura que no haya fondo al hacer hover */
}

.btn:focus {
  outline: none; /* Elimina el borde de foco al hacer clic */
  box-shadow: none; /* Elimina cualquier sombra de foco en algunos navegadores */
}

.create-button-container {
  margin-top: -80px;
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
