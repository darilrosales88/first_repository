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
      <form class="d-flex search-form" @submit.prevent="searchTerminales">
        <div class="input-container">
          <i class="bi bi-search"></i> 
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="nombre de terminal o puerto"
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
      <router-link v-if="hasGroup('Admin')" class="create-button" to="CrearTerminal">
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h6 style="margin-top: -33px; font-size: 18px;
    margin-right: 595px;color: #002A68;">Listado de terminales</h6>
    <br />
    <div class="table-container">
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Nombre</th>
          <th scope="col">Puerto</th>
          <th scope="col">Capacidad de Importación</th>
          <th scope="col">Capacidad de Exportación</th>
          <!-- Mostrar la columna "Acción" solo si el usuario pertenece al grupo "Admin" -->
          <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item) in terminalesFiltrados" :key="item.id">
          <td>{{ item.nombre_terminal }}</td>
          <td>{{ item.puerto_name }}</td>
          <td>{{ item.capacidad_almacen_importacion }}</td>
          <td>{{ item.capacidad_almacen_exportacion }}</td>
          <!-- Mostrar los botones de acciones solo si el usuario pertenece al grupo "Admin" -->
          <td >
              <button @click="openTerminalDetailsModal(item)" class="btn btn-info btn-small btn-eye" 
              v-html="showNoId ? '<i class=\'bi bi-eye-slash-fill\'></i>' : '<i class=\'bi bi-eye-fill\'></i>'">
              </button>
              <span v-if="hasGroup('Admin')">
                <button class="btn btn-warning btn-small">
                  <router-link :to="{name: 'EditarTerminal', params: {id:item.id}}">
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
    <h1 v-if="terminalesFiltrados.length === 0 && searchQuery">
      No existe ningún registro asociado a ese parámetro de búsqueda.
    </h1>
  </div>
</div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'TerminalView',
  components: {
    NavbarComponent,
  },

  data() {
    return {
      terminales: [],
      terminalesFiltrados: [], // Lista filtrada de terminales
      searchQuery: '', // Añadido aquí
      debounceTimeout: null, // Añadido aquí
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [],      // Almacenará los grupos del usuario
      showNoId: false,
    };
  },

  async created() {
    // Obtener los permisos y grupos del usuario al cargar el componente
    await this.fetchUserPermissionsAndGroups();
    this.getTerminales();
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

    async getTerminales() {
      try {
        const response = await axios.get('api/terminales/');
        this.terminales = response.data;
        this.terminalesFiltrados = this.terminales; // Inicialmente, muestra todas las terminales
      } catch (error) {
        console.error('Error al obtener las terminales:', error);
      }
    },

    searchTerminales() {
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase(); // Convirtiendo a minúsculas el parámetro de búsqueda
        this.terminalesFiltrados = this.terminales.filter(
          (terminal) =>
            terminal.nombre_terminal.toLowerCase().includes(query) ||
            terminal.puerto_name.toLowerCase().includes(query)
        );
      } else {
        this.terminalesFiltrados = this.terminales; // Si no hay búsqueda, muestra todas
      }
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchTerminales();
      }, 300);
    },

    deleteItem(id) {
      Swal.fire({
        title: '¿Desea eliminar esta terminal?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
      }).then((result) => {
        if (result.isConfirmed) {
          axios.delete(`api/terminales/${id}/`)
            .then(() => {
              this.getTerminales(); // Actualizar la lista de terminales después de eliminar
              Swal.fire(
                'Eliminado',
                'La terminal ha sido eliminada exitosamente.',
                'success'
              );
            })
            .catch(error => {
              console.error('Error al eliminar la terminal:', error);
              Swal.fire(
                'Error',
                'Hubo un error al eliminar la terminal.',
                'error'
              );
            });
        }
      });
    },
    openTerminalDetailsModal(Terminal) {
    // Mapear IDs de grupos a nombres
    const gruposAsignados = Terminal.groups && Terminal.groups.length > 0
        ? Terminal.groups
            .map(groupId => {
                const grupo = this.gruposDisponibles.find(g => g.id === groupId);
                return grupo ? grupo.name : 'Desconocido';
            })
            .join(', ')
        : 'Ninguno';

    // Mapear IDs de permisos a nombres
    const permisosAsignados = Terminal.Terminal_permissions && Terminal.Terminal_permissions.length > 0
        ? Terminal.Terminal_permissions
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
                <p><strong>Nombre:</strong> ${Terminal.nombre_terminal}</p>
                <p><strong>Puerto:</strong> ${Terminal.puerto_name}</p>
                <p><strong>Capacidad de Importación:</strong> ${Terminal.capacidad_almacen_importacion}</p>
                <p><strong>Capacidad de Exportación:</strong> ${Terminal.capacidad_almacen_exportacion}</p>
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
