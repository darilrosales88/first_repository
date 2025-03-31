<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido: </h6>
    </div>  
    <br />
    <Navbar-Component />
    <br />
    <br />
    <div class="search-container">
      <form class="d-flex" @submit.prevent="searchTipoEstructura">
        <div class="input-container">
          <i class="bi bi-search"></i>
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="Tipo de estructura"
          aria-label="Search"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px; padding-left: 5px;margin-top: -70px;" 
        />
      </div>
      </form>
    </div>
    <!-- Mostrar el botón "Crear nueva ubicación" solo si el usuario pertenece al grupo "Admin" -->
    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="CrearTipoUbicacion">
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h3 style="margin-top: -33px; font-size: 18px;
    margin-right: 390px;color: #002A68;">Listado de tipos de estructuras de ubicaciones</h3>
    <br />
    <div class="table-container">
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Tipo de estructura de ubicación</th>
          <!-- Mostrar la columna "Acciones" solo si el usuario pertenece al grupo "Admin" -->
          <th scope="col" >Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item) in tipos_estructura_ubicacion" :key="item.id">
          <td>{{ item.nombre_tipo_estructura_ubicacion }}</td>
          <!-- Mostrar los botones de acciones solo si el usuario pertenece al grupo "Admin" -->
          <td>
              <button @click="openTipoEstructuraUbicacionDetailsModal(item)" class="btn btn-info btn-small btn-eye" 
              v-html="showNoId ? '<i class=\'bi bi-eye-slash-fill\'></i>' : '<i class=\'bi bi-eye-fill\'></i>'">
              </button>
              <span v-if="hasGroup('Admin')">
            <button class="btn btn-warning btn-small">
                  <router-link :to="{name: 'EditarTipoUbicacion', params: {id:item.id}}">
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
    <h1 v-if="!busqueda_existente">No existe ningún registro asociado a ese parámetro de búsqueda</h1>
  </div>
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
      showNoId: false,
    };
  },

  async created() {
    // Obtener los permisos y grupos del usuario al cargar el componente
    await this.fetchUserPermissionsAndGroups();
    this.getTiposEstructuraUbicacion();
  },

  methods: {
    toggleNoIdVisibility() {
      this.showNoId = !this.showNoId; // Alternar la visibilidad de las columnas No e Id
    },
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
    openTipoEstructuraUbicacionDetailsModal(TipoEstructuraUbicacion) {
    // Mapear IDs de grupos a nombres
    const gruposAsignados = TipoEstructuraUbicacion.groups && TipoEstructuraUbicacion.groups.length > 0
        ? TipoEstructuraUbicacion.groups
            .map(groupId => {
                const grupo = this.gruposDisponibles.find(g => g.id === groupId);
                return grupo ? grupo.name : 'Desconocido';
            })
            .join(', ')
        : 'Ninguno';

    // Mapear IDs de permisos a nombres
    const permisosAsignados = TipoEstructuraUbicacion.TipoEstructuraUbicacion_permissions && 
    TipoEstructuraUbicacion.TipoEstructuraUbicacion_permissions.length > 0
        ? TipoEstructuraUbicacion.TipoEstructuraUbicacion_permissions
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
                <p><strong>Tipo de estructura de ubicación:</strong> ${TipoEstructuraUbicacion.nombre_tipo_estructura_ubicacion}</p>
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
