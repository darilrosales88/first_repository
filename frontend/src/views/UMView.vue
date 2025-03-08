<template>
  <div>
    <img style="width: 250px;" src="@/assets/Imagenes/mitrans.png" />
    <Navbar-Component />
    <div class="search-container">
      <form
        class="d-flex"
        @submit.prevent="search_unidad_medida"
        style="padding: 10px; margin-left: 65em"
      >
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="magnitud,unidad de medida o símbolo"
          aria-label="Search"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px"
        />
        <button class="btn btn-outline-success btn-sm" type="submit">Buscar</button>
      </form>
    </div>
    <div style="margin-top: -4em;">
      <br />
      <!-- Mostrar el botón "Crear unidad de medida" solo si el usuario pertenece al grupo "Admin" -->
      <router-link
        v-if="hasGroup('Admin')"
        style="text-decoration:none; color:black; margin-right: 1330px;"
        to="/AdicionarUM"
      >
        Crear unidad de medida <i class="bi bi-plus-circle"></i>
      </router-link>
      <br />
    </div>
    <br />
    <table class="table">
      <thead>
        <tr>
          <th scope="col">No</th>
          <th scope="col">Magnitud</th>
          <th scope="col">Unidad de medida</th>
          <th scope="col">Símbolo</th>
          <!-- Mostrar la columna "Acciones" solo si el usuario pertenece al grupo "Admin" -->
          <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in unidades" :key="item.id">
          <th scope="row" style="background-color: white;">{{ index + 1 }}</th>
          <td>{{ item.magnitud }}</td>
          <td>{{ item.unidad_medida }}</td>
          <td>{{ item.simbolo }}</td>
          <!-- Mostrar los botones de acciones solo si el usuario pertenece al grupo "Admin" -->
          <td v-if="hasGroup('Admin')">
            <button @click.prevent="confirmDelete(item.id)" class="btn btn-danger">
              <i style="color:white" class="bi bi-trash"></i>
            </button>
            <button style="margin-left:10px" class="btn btn-warning">
              <router-link :to="{name: 'EditarUM', params: {id:item.id}}">
                <i style="color:white" class="bi bi-pencil-square"></i>
              </router-link>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import Swal from 'sweetalert2';
import axios from 'axios';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'UMView',

  components: {
    NavbarComponent,
  },

  data() {
    return {
      unidades: [],
      searchQuery: '', // Para la búsqueda
      debounceTimeout: null, // Para el debounce en la búsqueda
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [],      // Almacenará los grupos del usuario
    };
  },

  async created() {
    // Obtener los permisos y grupos del usuario al cargar el componente
    await this.fetchUserPermissionsAndGroups();
  },

  mounted() {
    this.get_unidades();
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

    async get_unidades() {
      this.$store.commit('setIsLoading', true);
      axios
        .get('/api/unidades_medida/')
        .then(response => {
          this.unidades = response.data;
        })
        .catch(error => {
          console.log(error);
        });
      this.$store.commit('setIsLoading', false);
    },

    async search_unidad_medida() {
      this.$store.commit('setIsLoading', true);
      axios
        .get(`/api/unidades_medida/?magnitud_um_simbolo=${this.searchQuery}`)
        .then(response => {
          this.unidades = response.data;
        })
        .catch(error => {
          console.log(error);
        });
      this.$store.commit('setIsLoading', false);
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
          this.delete_unidad(id);
        }
      });
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.search_unidad_medida();
      }, 300); // Ajusta el tiempo de espera según sea necesario
    },

    // Eliminar unidad de medida
    async delete_unidad(id) {
      try {
        await axios.delete(`/api/unidades_medida/${id}/`);
        // Actualizar la lista de unidades de medida eliminando el que se ha borrado
        this.unidades = this.unidades.filter(unidad => unidad.id !== id);
        Swal.fire('Eliminado!', 'La unidad de medida ha sido eliminada exitosamente.', 'success');
      } catch (error) {
        console.error('Error al eliminar la unidad de medida:', error);
        Swal.fire('Error', 'Hubo un error al eliminar la unidad de medida.', 'error');
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