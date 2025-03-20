<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    <br />
    <br />

    <div class="search-container">
      <form class="d-flex search-form" @submit.prevent="searchDestinos">
        <div class="input-container">
          <i class="bi bi-search"></i>
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="Buscar por cliente o destino"
          aria-label="Buscar"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px; padding-left: 5px;margin-top: -70px;" 
        />
      </div>
      </form>
      <br>
    </div>

    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="/AdicionarDestino">
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h6 style="margin-top: -33px; font-size: 18px;
    margin-right: 630px;color: #002A68;">Listado de destinos</h6>
    <br />
    <div class="table-container">
    <table class="table">
      <thead>
        <tr>
          <th>Cliente</th>
          <th>Destino</th>
          <th v-if="hasGroup('Admin')">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item) in destinosFiltrados" :key="item.id">
          <td>{{ item.cliente_name }}</td>
          <td>{{ item.destino }}</td>
          <td>
            <button @click="openatraqueDetailsModal(item)" class="btn btn-info btn-small btn-eye" 
              v-html="showNoId ? '<i class=\'bi bi-eye-slash-fill\'></i>' : '<i class=\'bi bi-eye-fill\'></i>'">
              </button>
              <span v-if="hasGroup('Admin')">
            <button class="btn btn-warning btn-small">
              <router-link :to="{name: 'EditarDestino', params: {id: item.id}}">
                <i style="color:black" class="bi bi-pencil-square"></i>
              </router-link>
            </button>
            <button @click.prevent="confirmDelete(item.id)" class="btn btn-danger btn-small">
              <i  class="bi bi-trash"></i>
            </button>
          </span>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Mensaje cuando no hay resultados -->
    <h1 v-if="destinosFiltrados.length === 0 && searchQuery">
      No existe ningún registro asociado a ese parámetro de búsqueda.
    </h1>
  </div>
  </div>
</template>

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

<script>
import axios from 'axios';
import NavbarComponent from "@/components/NavbarComponent.vue";
import Swal from 'sweetalert2';

export default {
  name: 'DestinoView',
  components: {
    NavbarComponent,
  },
  data() {
    return {
      destinos: [], // Lista completa de destinos
      destinosFiltrados: [], // Lista filtrada de destinos
      searchQuery: '', // Término de búsqueda
      debounceTimeout: null, // Timeout para el debounce
      userPermissions: [], // Permisos del usuario
      userGroups: [], // Grupos del usuario
    };
  },
  async created() {
    await this.fetchUserPermissionsAndGroups();
    await this.getDestinos();
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
    // Obtiene todos los destinos
    async getDestinos() {
      try {
        const response = await axios.get("/api/destinos/");
        this.destinos = response.data;
        this.destinosFiltrados = this.destinos; // Inicialmente, muestra todos los destinos
      } catch (error) {
        console.error("Error al obtener los destinos:", error);
        Swal.fire('Error', 'No se pudieron cargar los destinos.', 'error');
      }
    },
    // Filtra los destinos según el término de búsqueda
    searchDestinos() {
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();//convirtiendo a minusculas el parametro de busqueda
        this.destinosFiltrados = this.destinos.filter(
          (destino) =>
            destino.cliente_name.toLowerCase().includes(query) ||
            destino.destino.toLowerCase().includes(query)
        );
      } else {
        this.destinosFiltrados = this.destinos; // Si no hay búsqueda, muestra todos
      }
    },
    // Debounce para evitar múltiples llamadas durante la escritura
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchDestinos();
      }, 300);
    },
    // Confirma la eliminación de un destino
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
          this.deleteDestino(id);
        }
      });
    },
    // Elimina un destino
    async deleteDestino(id) {
      try {
        await axios.delete(`/api/destinos/${id}/`);
        this.destinos = this.destinos.filter(destino => destino.id !== id);
        this.destinosFiltrados = this.destinosFiltrados.filter(destino => destino.id !== id);
        Swal.fire('Eliminado!', 'El destino ha sido eliminado exitosamente.', 'success');
      } catch (error) {
        console.error('Error al eliminar el destino:', error);
        Swal.fire('Error', 'Hubo un error al eliminar el destino.', 'error');
      }
    },
    openDestinoDetailsModal(Destino) {
    // Mapear IDs de grupos a nombres
    const gruposAsignados = Destino.groups && Destino.groups.length > 0
        ? Destino.groups
            .map(groupId => {
                const grupo = this.gruposDisponibles.find(g => g.id === groupId);
                return grupo ? grupo.name : 'Desconocido';
            })
            .join(', ')
        : 'Ninguno';

    // Mapear IDs de permisos a nombres
    const permisosAsignados = Destino.Destino_permissions && Destino.Destino_permissions.length > 0
        ? Destino.Destino_permissions
            .map(permisoId => {
                const permiso = this.permisosDisponibles.find(p => p.id === permisoId);
                return permiso ? permiso.name : 'Desconocido';
            })
            .join(', ')
        : 'Ninguno';

    Swal.fire({
        title: 'Detalles del Destino',
        html: `
            <div style="text-align: left;">
                <p><strong>Cliente:</strong> ${Destino.cliente_name}</p>
                <p><strong>Destino:</strong> ${Destino.destino}</p>
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
  }
};
</script>