<template>
  <div>
    <img style="width: 250px" src="@/assets/Imagenes/mitrans.png" />
    <NavbarComponent />
    
    <div class="search-container">
      <form
        class="d-flex"
        @submit.prevent="searchCargos"
        style="padding: 10px; margin-left: 58em"
      >
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="nombre"
          aria-label="Buscar"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px"
        />
        <button style="" class="btn btn-outline-success btn-sm" type="submit">
          Buscar
        </button>
      </form>
    </div>
    <div class="create-button-container">
      <!-- Mostrar el botón "Adicionar Cargo" solo si el usuario pertenece al grupo "Admin" -->
      <router-link v-if="hasGroup('Admin')" class="create-button" to="/AdicionarCargo">
        Adicionar Cargo <i class="bi bi-plus-circle"></i>
      </router-link>
    </div>
    <br />
    <br />
    <table class="table">
      <thead>
        <tr>
          <th scope="col">No</th>
          <th scope="col">Cargo</th>
          <!-- Mostrar la columna "Acciones" solo si el usuario pertenece al grupo "Admin" -->
          <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in cargos" :key="item.id">
          <th scope="row" style="background-color:white">{{ index + 1 }}</th>
          <td>{{ item.nombre_cargo }}</td>
          <!-- Mostrar los botones de acciones solo si el usuario pertenece al grupo "Admin" -->
          <td v-if="hasGroup('Admin')">
            <button @click.prevent="confirmDelete(item.id)" class="btn btn-danger">
              <i style="color: white" class="bi bi-trash"></i>
            </button>
            <button style="margin-left: 10px" class="btn btn-warning">
              <router-link :to="{ name: 'EditarCargo', params: { id: item.id } }">
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
import Swal from "sweetalert2";
import axios from "axios";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "CargosView",

  components: {
    NavbarComponent,
  },

  data() {
    return {
      cargos: [],
      searchQuery: "", // Añadido aquí
      debounceTimeout: null, // Añadido aquí
      busqueda_existente: true, // Variable para controlar la visibilidad del mensaje de búsqueda
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [],      // Almacenará los grupos del usuario
    };
  },

  async created() {
    // Obtener los permisos y grupos del usuario al cargar el componente
    await this.fetchUserPermissionsAndGroups();
  },

  mounted() {
    this.get_cargos();
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

    get_cargos() {
      this.$store.commit("setIsLoading", true);
      axios
        .get("/api/cargos/")
        .then((response) => {
          this.cargos = response.data;
          this.busqueda_existente = true; // Reinicia la variable al cargar todos los cargos
        })
        .catch((error) => {
          console.log(error);
        });
      this.$store.commit("setIsLoading", false);
    },

    async searchCargos() {
      this.$store.commit("setIsLoading", true);

      axios
        .get(`/api/cargos/?n_cargo=${this.searchQuery}`)
        .then((response) => {
          this.cargos = response.data;
          // Actualiza busqueda_existente basado en el resultado
          this.busqueda_existente = this.cargos.length > 0;
        })
        .catch((error) => {
          console.log(error);
          this.busqueda_existente = false; // Asegura que busqueda_existente sea false en caso de error
        });

      this.$store.commit("setIsLoading", false);
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
          this.deleteCargo(id);
        }
      });
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchCargos();
      }, 300); // Ajusta el tiempo de espera según sea necesario
    },

    // Eliminar cargo
    async deleteCargo(id) {
      try {
        await axios.delete(`/api/cargos/${id}/`);
        // Actualizar la lista de cargos eliminando el que se ha borrado
        this.cargos = this.cargos.filter((cargo) => cargo.id !== id);
        Swal.fire(
          "Eliminado!",
          "El cargo ha sido eliminado exitosamente.",
          "success"
        );
      } catch (error) {
        console.error("Error al eliminar el cargo:", error);
        Swal.fire("Error", "Hubo un error al eliminar el cargo.", "error");
      }
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