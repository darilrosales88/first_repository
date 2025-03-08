<template>
  <img style="width: 250px" src="@/assets/Imagenes/mitrans.png" />
  <Navbar-Component />
  <br />
  <div class="search-container">
    <form class="d-flex search-form" @submit.prevent="searchAtraque">
      <input
        class="form-control form-control-sm me-2"
        type="search"
        placeholder="nombre"
        aria-label="Buscar"
        v-model="searchQuery"
        @input="handleSearchInput"
        style="width: 200px;"
      />
      <button class="btn btn-outline-success btn-sm" type="submit">Buscar</button>
    </form>
  </div>
  <div class="create-button-container">
    <router-link class="create-button" to="AdicionarAtraque">
      Crear atraque <i class="bi bi-plus-circle"></i>
    </router-link>
  </div>
  <br />
  <br />
  <table class="table">
    <thead>
      <tr>
        <th scope="col">No</th>
        <th scope="col">Id</th>
        <th scope="col">Nombre</th>
        <th scope="col">Terminal</th>
        <th scope="col">Puerto</th>
        <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, index) in atraques" :key="item.id">
        <th scope="row" style="background-color: white;">{{ index + 1 }}</th>
        <th scope="row" style="background-color: white;">{{ item.id }}</th>
        <td>{{ item.nombre_atraque }}</td>
        <td>{{ item.puerto_name }}</td>
        <td>{{ item.terminal_name }}</td>
        <td v-if="hasGroup('Admin')">
          <button @click.prevent="confirmDelete(item.id)" class="btn btn-danger">
            <i style="color:white" class="bi bi-trash"></i>
          </button>
          <button style="margin-left:10px" class="btn btn-warning">
            <router-link :to="{name: 'EditarAtraque', params: {id:item.id}}">
              <i style="color:white" class="bi bi-pencil-square"></i>
            </router-link>
          </button>
        </td>
      </tr>
    </tbody>
  </table>
  <!-- Mensaje cuando no hay resultados -->
  <h1 v-if="!busqueda_existente">No existe ningún registro asociado a ese parámetro de búsqueda.</h1>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'AtraquesView',
  components: {
    NavbarComponent,
  },
  data() {
    return {
      atraques: [],
      nombre_atraque: '',
      puerto: '',
      terminal: '',
      searchQuery: '', // Añadido aquí
      debounceTimeout: null, // Añadido aquí
      busqueda_existente: true, // Variable para controlar la visibilidad del <h1> de la busqueda
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [], // Almacenará los grupos del usuario
    };
  },
  mounted() {
    this.getAtraques();
  },
  async created() {
    // Obtener los permisos y grupos del usuario al cargar el componente
    await this.fetchUserPermissionsAndGroups();
  },
  methods: {
    // Verifica si el usuario tiene un permiso específico
    hasPermission(permission) {
      return this.userPermissions.some((p) => p.name === permission);
    },
    hasGroup(group) {
      return this.userGroups.some((g) => g.name === group);
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
    getAtraques() {
      axios
        .get('/api/atraques/')
        .then((response) => {
          console.log(response.data);
          this.atraques = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    // Usar SweetAlert2 para confirmar la eliminación
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
          this.delete_atraque(id);
        }
      });
    },
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.search_atraque();
      }, 300); // Ajusta el tiempo de espera según sea necesario
    },
    // Eliminar atraque
    async delete_atraque(id) {
      try {
        await axios.delete(`/api/atraques/${id}/`);
        // Actualizar la lista de atraques eliminando el que se ha borrado
        this.atraques = this.atraques.filter((atraque) => atraque.id !== id);
        Swal.fire('Eliminado!', 'El atraque ha sido eliminado exitosamente.', 'success');
      } catch (error) {
        console.error('Error al eliminar el atraque:', error);
        Swal.fire('Error', 'Hubo un error al eliminar el atraque.', 'error');
      }
    },
    async search_atraque() {
      this.$store.commit('setIsLoading', true);
      axios
        .get(`/api/atraques/?nombre_atraque=${this.searchQuery}`)
        .then((response) => {
          this.atraques = response.data;
          // Actualiza busqueda_existente basado en el resultado
          this.busqueda_existente = this.atraques.length > 0;
        })
        .catch((error) => {
          console.log(error);
          this.busqueda_existente = false; // Asegura que busqueda_existente sea false en caso de error
        });
      this.$store.commit('setIsLoading', false);
    },
  },
};
</script>

<style scoped>
/*para el placeholder del buscador */
.search-container input::placeholder {
  font-size: 12px; /* Tamaño de la fuente más pequeño */
  color: #999;     /* Color del texto del placeholder */
}

body {
  overflow: scroll;
}

.search-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
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
</style>
