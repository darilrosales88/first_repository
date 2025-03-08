<template>
  <div>
    <img style="width: 250px" src="@/assets/Imagenes/mitrans.png" />
    <NavbarComponent />
    <br />
    <div class="search-container">
      <form class="d-flex search-form" @submit.prevent="searchPaises">
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="Search"
          aria-label="Search"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px;"
        />
        <button class="btn btn-outline-success btn-sm" type="submit">
          Buscar
        </button>
      </form>
    </div>
    <div class="create-button-container">
      <!-- Mostrar el botón "Adicionar Pais" solo si el usuario pertenece al grupo "Admin" -->
      <router-link v-if="hasGroup('Admin')" class="create-button" to="/AdicionarPais">
        Adicionar Pais <i class="bi bi-plus-circle"></i>
      </router-link>
    </div>
    <br />
    <table class="table">
      <thead>
        <tr>
          <th scope="col">id</th>
          <th scope="col">Nacionalidad</th>
          <th scope="col">Pais</th>
          <!-- Mostrar la columna "Acciones" solo si el usuario pertenece al grupo "Admin" -->
          <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in paises" :key="item.id">
          <th scope="row" style="background-color:white">{{ index + 1 }}</th>
          <td>{{ item.nacionalidad }}</td>
          <td>{{ item.nombre_pais }}</td>
          <!-- Mostrar los botones de acciones solo si el usuario pertenece al grupo "Admin" -->
          <td v-if="hasGroup('Admin')">
            <button @click="confirmDelete(item.id)" class="btn btn-danger">
              <i style="color: white" class="bi bi-trash"></i>
            </button>
            <button style="margin-left: 10px" class="btn btn-warning">
              <router-link :to="{ name: 'EditarPais', params: { id: item.id } }">
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

<script>
import NavbarComponent from "@/components/NavbarComponent.vue";
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "PaisesView",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      paises: [],
      searchQuery: '', // Añadido aquí
      debounceTimeout: null, // Añadido aquí
      busqueda_existente: true, // Variable para controlar la visibilidad del <h1> de la busqueda
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [],      // Almacenará los grupos del usuario
    };
  },

  async created() {
    // Obtener los permisos y grupos del usuario al cargar el componente
    await this.fetchUserPermissionsAndGroups();
  },

  mounted() {
    this.getpaises();
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
        const userId = localStorage.getItem("userid");
        if (userId) {
          const response = await axios.get(`/apiAdmin/user/${userId}/permissions-and-groups/`);
          this.userPermissions = response.data.permissions;
          this.userGroups = response.data.groups;
        }
      } catch (error) {
        console.error("Error al obtener permisos y grupos:", error);
      }
    },

    async getpaises() {
      try {
        const response = await axios.get("/api/paises/");
        this.paises = response.data;

      } catch (error) {
        console.error("Error al obtener los paises:", error);

      }
    },

    async searchPaises() {
      this.$store.commit("setIsLoading", true);
      try {
        const response = await axios.get(`/api/paises/?nombre_p=${this.searchQuery}`);
        this.paises = response.data;        
        // Actualiza busqueda_existente basado en el resultado
        this.busqueda_existente = this.paises.length > 0;
      } catch (error) {
        console.error("Error al buscar el pais:", error);
        this.busqueda_existente = false;
      }
      this.$store.commit("setIsLoading", false);
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchPaises();
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
          this.deletePaises(id);
        }
      });
    },

    async deletePaises(id) {
      try {
        await axios.delete(`/api/paises/${id}/`);
        // Actualizar la lista de países eliminando el que se ha borrado
        this.paises = this.paises.filter((pais) => pais.id !== id);
        Swal.fire("Eliminado!", "El país ha sido eliminado exitosamente.", "success");
      } catch (error) {
        console.error("Error al eliminar el país:", error);
        Swal.fire("Error", "Hubo un error al eliminar el país.", "error");
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
</style>