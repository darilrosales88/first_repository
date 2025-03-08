<template>
  <div>
    <img style="width: 250px" src="@/assets/Imagenes/mitrans.png" />
    <NavbarComponent />
    
    <div class="search-container">
      <form
        class="d-flex"
        @submit.prevent="searchContenedor"
        style="padding: 10px; margin-left: 65em"
      >
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="no.ID -tipo contenedor -longitud"
          aria-label="Buscar"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px"
        />
        <button class="btn btn-outline-success btn-sm" type="submit">Buscar</button>
      </form>
    </div>
    <div style="margin-top: -40px">
      <router-link
        style="
          text-decoration: none;
          margin-right: 1150px;
          color: black;
          padding-bottom: 2em;
        "
        to="/CrearContenedor"
        >Crear contenedor <i class="bi bi-plus-circle"></i
      ></router-link>
    </div>
    <br />
    <table class="table">
      <thead>
        <tr>
          <th scope="col" style="background-color:white">#</th>
          <th scope="col">ID Contenedor</th>
          <th scope="col">Tipo</th>
          <th scope="col">Longitud</th>
          <th scope="col">ISO</th>
          <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in contenedores" :key="item.id">
          <th scope="row" style="background-color:white">{{ index + 1 }}</th>
          <td>{{ item.id_contenedor }}</td>
          <td>{{ item.tipo_contenedor_description }}</td>
          <td>{{ item.longitud }}</td>
          <td>{{ item.codigo_iso }}</td>
          <td v-if="hasGroup('Admin')">
            <button @click.prevent="confirmDelete(item.id_contenedor)" class="btn btn-danger">
              <i style="color: white" class="bi bi-trash"></i>
            </button>
            <button style="margin-left: 10px" class="btn btn-warning">
              <router-link :to="{ name: 'EditarContenedor', params: { id: item.id_contenedor } }">
                <i style="color: white" class="bi bi-pencil-square"></i>
              </router-link>
            </button>
          </td>
        </tr>
      </tbody>
    </table>    
  </div>
  <!-- Mensaje cuando no hay resultados -->
  <h1 v-if="!busqueda_existente">No existe ningún registro asociado a ese parámetro de búsqueda.</h1>
</template>

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
</style>


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
</style>


<style scoped>


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
