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
      <form class="d-flex search-form" @submit.prevent="searchAtraque">
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="Contenedor"
          aria-label="Search"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px;"
        />
      </form>
    </div>
    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="/CrearContenedor">
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h6 style="margin-top: -31px; font-size: 19px;
    margin-right: 570px;">Listado de contenedores:</h6>
    <br />
    <div class="table-container">
    <table class="table">
      <thead>
        <tr>
          <th scope="col" v-if="showNoId">#</th>
          <th scope="col">ID Contenedor</th>
          <th scope="col">Tipo</th>
          <th scope="col">Longitud</th>
          <th scope="col" v-if="showNoId">ISO</th>
          <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in contenedores" :key="item.id">
          <th  v-if="showNoId" scope="row">{{ index + 1 }}</th>
          <td>{{ item.id_contenedor }}</td>
          <td>{{ item.tipo_contenedor_description }}</td>
          <td>{{ item.longitud }}</td>
          <td  v-if="showNoId">{{ item.codigo_iso }}</td>
          <td >
            <button @click="toggleNoIdVisibility" class="btn btn-info btn-small btn-eye" 
              v-html="showNoId ? '<i class=\'bi bi-eye-slash-fill\'></i>' : '<i class=\'bi bi-eye-fill\'></i>'">
              </button>
              <span v-if="hasGroup('Admin')">
                <button class="btn btn-warning btn-small">
              <router-link :to="{ name: 'EditarContenedor', params: { id: item.id_contenedor } }">
                <i style="color: white" class="bi bi-pencil-square"></i>
              </router-link>
            </button>
            <button style="margin-left:10px" @click.prevent="confirmDelete(item.id_contenedor)" class="btn btn-danger btn-small">
              <i style="color: white" class="bi bi-trash"></i>
            </button>
          </span>
          </td>
        </tr>
      </tbody>
    </table>    
  <!-- Mensaje cuando no hay resultados -->
  <h1 v-if="!busqueda_existente">No existe ningún registro asociado a ese parámetro de búsqueda.</h1>
</div>
</div>
</template>

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

<script>
import axios from "axios";
import Swal from "sweetalert2";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "ContenedorView",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      contenedores: [],
      searchQuery: "",
      debounceTimeout: null,
      busqueda_existente: true, // Variable para controlar la visibilidad del mensaje de búsqueda
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [],      // Almacenará los grupos del usuario
      showNoId: false,
    };
  },
  mounted() {
    this.getContenedores();
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
    async getContenedores() {
      try {
        const response = await axios.get("/api/contenedores/");
        this.contenedores = response.data;
        this.busqueda_existente = true; // Reinicia la variable al cargar todos los contenedores
      } catch (error) {
        console.error("Error al obtener los contenedores:", error);
      }
    },
    async searchContenedor() {
      this.$store.commit("setIsLoading", true);
      try {
        const response = await axios.get(
          `/api/contenedores/?id_tipo_longitud=${this.searchQuery}`
        );
        this.contenedores = response.data;
        // Actualiza busqueda_existente basado en el resultado
        this.busqueda_existente = this.contenedores.length > 0;
      } catch (error) {
        console.error("Error al buscar contenedores:", error);
        this.busqueda_existente = false; // Asegura que busqueda_existente sea false en caso de error
      }
      this.$store.commit("setIsLoading", false);
    },
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchContenedor();
      }, 300);
    },
    confirmDelete(id) {
      Swal.fire({
        title: "¿Estás seguro?",
        text: "¡No podrás revertir esta acción!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
        reverseButtons: true,
      }).then((result) => {
        if (result.isConfirmed) {
          this.deleteContenedor(id);
        }
      });
    },
    async deleteContenedor(id) {
      try {
        await axios.delete(`/api/contenedores/${id}/`);
        // Actualizar la lista de contenedores eliminando el que se ha borrado
        this.contenedores = this.contenedores.filter(contenedor => contenedor.id_contenedor !== id);
        Swal.fire('Eliminado!', 'El contenedor ha sido eliminado exitosamente.', 'success');
      } catch (error) {
        console.error("Error al eliminar el contenedor:", error);
        Swal.fire('Error', 'Hubo un error al eliminar el contenedor.', 'error');
      }
    }
  },
};
</script>
