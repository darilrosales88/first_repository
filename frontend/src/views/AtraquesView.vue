<template>
  <div >
    <div style=" background-color: #003366; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    <br />
    <br />
    <div class="search-container">
      <form class="d-flex search-form" @submit.prevent="searchAtraque">
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="Nombre"
          aria-label="Search"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px;"
        />
      </form>
    </div>
    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="AdicionarAtraque">
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h6 style="margin-top: -31px; font-size: 19px;
    margin-right: 630px;">Listado de atraques:</h6>
    <br />
    <div class="table-container" >
      <table class="table">
        <thead>
          <tr >
            <th scope="col" v-if="showNoId">No</th>
            <th scope="col" v-if="showNoId">Id</th>
            <th  scope="col">Nombre</th>
            <th scope="col">Terminal</th>
            <th scope="col">Puerto</th>
            <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in atraques" :key="item.id">
            <td v-if="showNoId">{{ index + 1 }}</td>
            <td v-if="showNoId">{{ item.id }}</td>
            <td>{{ item.nombre_atraque }}</td>
            <td>{{ item.puerto_name }}</td>
            <td>{{ item.terminal_name }}</td>
            <td >
              <button @click="toggleNoIdVisibility" class="btn btn-info btn-small btn-eye" 
              v-html="showNoId ? '<i class=\'bi bi-eye-slash-fill\'></i>' : '<i class=\'bi bi-eye-fill\'></i>'">
              </button>
              <span v-if="hasGroup('Admin')">
                <button class="btn btn-warning btn-small">
                  <router-link :to="{name: 'EditarAtraque', params: {id:item.id}}">
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
      <h1 v-if="!busqueda_existente">No existe ningún registro asociado a ese parámetro de búsqueda.</h1>
    </div>
  </div>
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
      showNoId: false,
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
    toggleNoIdVisibility() {
      this.showNoId = !this.showNoId; // Alternar la visibilidad de las columnas No e Id
    },
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
