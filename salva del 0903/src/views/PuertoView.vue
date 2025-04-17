<template>
  <div>
    <img style="width: 250px;" src="@/assets/Imagenes/mitrans.png" />
    <Navbar-Component />
    <br />
    <div class="search-container">
      <form class="d-flex search-form" @submit.prevent="searchPuertos">
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="Buscar por nombre o país"
          aria-label="Buscar"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px;"
        />
        <button class="btn btn-outline-success btn-sm" type="submit">Buscar</button>
      </form>
      <br>
    </div>
    <!-- Mostrar el botón "Crear nuevo puerto" solo si el usuario pertenece al grupo "Admin" -->
    <router-link
      v-if="hasGroup('Admin')"
      style="text-decoration:none;margin-right:1150px;color:black"
      to="/CrearPuerto"
    >
      Crear nuevo puerto <i class="bi bi-plus-circle"></i>
    </router-link>
    <br />
    <br />
    <table class="table">
      <thead>
        <tr>
          <th scope="col">No</th>
          <th scope="col">Nombre</th>
          <th scope="col">País</th>
          <th scope="col">Provincia</th>
          <th scope="col">Servicio portuario</th>
          <th scope="col">Latitud</th>
          <th scope="col">Longitud</th>
          <!-- Mostrar la columna "Acción" solo si el usuario pertenece al grupo "Admin" -->
          <th scope="col" v-if="hasGroup('Admin')">Acción</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in puertosFiltrados" :key="item.id">
          <th scope="row" style="background-color: white;">{{ index + 1 }}</th>
          <td>{{ item.nombre_puerto }}</td>
          <td>{{ item.nombre_pais }}</td>
          <td>{{ item.nombre_provincia }}</td>
          <td>{{ item.servicio_portuario_name }}</td>
          <td>{{ item.latitud }}</td>
          <td>{{ item.longitud }}</td>
          <!-- Mostrar los botones de acciones solo si el usuario pertenece al grupo "Admin" -->
          <td v-if="hasGroup('Admin')">
            <button @click="deleteItem(item.id)" class="btn btn-danger">
              <i style="color:white" class="bi bi-trash"></i>
            </button>
            <button style="margin-left:10px" class="btn btn-warning">
              <router-link :to="{name: 'EditarPuerto', params: {id: item.id}}">
                <i style="color:white" class="bi bi-pencil-square"></i>
              </router-link>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <h1 v-if="puertosFiltrados.length === 0 && searchQuery">
      No existe ningún registro asociado a ese parámetro de búsqueda.
    </h1>
  </div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'PuertoView',
  components: {
    NavbarComponent,
  },

  data() {
    return {
      puertos: [],
      puertosFiltrados: [], // Lista filtrada de puertos
      searchQuery: '', // Añadido aquí
      debounceTimeout: null, // Añadido aquí
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [],      // Almacenará los grupos del usuario
    };
  },

  async created() {
    // Obtener los permisos y grupos del usuario al cargar el componente
    await this.fetchUserPermissionsAndGroups();
    this.getPuertos();
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

    async getPuertos() {
      try {
        const response = await axios.get('api/puertos/');
        this.puertos = response.data;
        this.puertosFiltrados = this.puertos; // Inicialmente, muestra todos los puertos
      } catch (error) {
        console.error('Error al obtener los puertos:', error);
      }
    },

    searchPuertos() {
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase(); // Convirtiendo a minúsculas el parámetro de búsqueda
        this.puertosFiltrados = this.puertos.filter(
          (puerto) =>
            puerto.nombre_pais.toLowerCase().includes(query) ||
            puerto.nombre_puerto.toLowerCase().includes(query)
        );
      } else {
        this.puertosFiltrados = this.puertos; // Si no hay búsqueda, muestra todos
      }
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchPuertos();
      }, 300);
    },

    deleteItem(id) {
      Swal.fire({
        title: '¿Desea eliminar este puerto?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
      }).then((result) => {
        if (result.isConfirmed) {
          axios.delete(`api/puertos/${id}/`)
            .then(() => {
              this.getPuertos(); // Actualizar la lista de puertos después de eliminar
              Swal.fire(
                'Eliminado',
                'El puerto ha sido eliminado exitosamente.',
                'success'
              );
            })
            .catch(error => {
              console.error('Error al eliminar el puerto:', error);
              Swal.fire(
                'Error',
                'Hubo un error al eliminar el puerto.',
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