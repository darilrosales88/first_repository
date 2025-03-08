<template>
  <div>
    <img style="width: 250px;" src="@/assets/Imagenes/mitrans.png" />
    <Navbar-Component />
    <br />
    <div class="search-container">
      <form class="d-flex search-form" @submit.prevent="searchTerminales">
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="nombre de terminal o puerto"
          aria-label="Buscar"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px;"
        />
        <button class="btn btn-outline-success btn-sm" type="submit">Buscar</button>
      </form>
      <br>
    </div>
    <!-- Mostrar el botón "Crear nueva terminal" solo si el usuario pertenece al grupo "Admin" -->
    <router-link
      v-if="hasGroup('Admin')"
      style="text-decoration:none;margin-right:1150px;color:black"
      to="/CrearTerminal"
    >
      Crear nueva terminal <i class="bi bi-plus-circle"></i>
    </router-link>
    <br />
    <br />
    <table class="table">
      <thead>
        <tr>
          <th scope="col">No</th>
          <th scope="col">Nombre</th>
          <th scope="col">Puerto</th>
          <th scope="col">Capacidad Importación</th>
          <th scope="col">Capacidad Exportación</th>
          <!-- Mostrar la columna "Acción" solo si el usuario pertenece al grupo "Admin" -->
          <th scope="col" v-if="hasGroup('Admin')">Acción</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in terminalesFiltrados" :key="item.id">
          <th scope="row" style="background-color: white;">{{ index + 1 }}</th>
          <td>{{ item.nombre_terminal }}</td>
          <td>{{ item.puerto_name }}</td>
          <td>{{ item.capacidad_almacen_importacion }}</td>
          <td>{{ item.capacidad_almacen_exportacion }}</td>
          <!-- Mostrar los botones de acciones solo si el usuario pertenece al grupo "Admin" -->
          <td v-if="hasGroup('Admin')">
            <button @click="deleteItem(item.id)" class="btn btn-danger">
              <i style="color:white" class="bi bi-trash"></i>
            </button>
            <button style="margin-left:10px" class="btn btn-warning">
              <router-link :to="{name: 'EditarTerminal', params: {id: item.id}}">
                <i style="color:white" class="bi bi-pencil-square"></i>
              </router-link>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <h1 v-if="terminalesFiltrados.length === 0 && searchQuery">
      No existe ningún registro asociado a ese parámetro de búsqueda.
    </h1>
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
    };
  },

  async created() {
    // Obtener los permisos y grupos del usuario al cargar el componente
    await this.fetchUserPermissionsAndGroups();
    this.getTerminales();
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