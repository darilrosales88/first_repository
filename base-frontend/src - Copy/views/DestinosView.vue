<template>
  <img style="width: 250px" src="@/assets/Imagenes/mitrans.png" />
  <Navbar-Component />
  <br />
  <div class="search-container">
    <form class="d-flex search-form" @submit.prevent="searchDestinos">
      <input
        class="form-control form-control-sm me-2"
        type="search"
        placeholder="Search"
        aria-label="Search"
        v-model="searchQuery"
        @input="handleSearchInput"
        style="width: 200px"
      />
      <button class="btn btn-outline-success btn-sm" type="submit">
        Search
      </button>
    </form>
  </div>
  <div class="create-button-container">
    <router-link
      class="create-button"
      to="/AdicionarDestino"
      v-if="hasGroup('Admin')"
    >
      Adicionar destino <i class="bi bi-plus-circle"></i>
    </router-link>
  </div>
  <br />
  <table class="table">
    <thead>
      <tr>
        <th scope="col">id</th>
        <th scope="col">Cliente</th>
        <th scope="col">Destino</th>
        <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, index) in destinos" :key="item.id">
        <th scope="row" style="background-color: white">{{ index + 1 }}</th>
        <td>{{ item.cliente_name }}</td>
        <td>{{ item.destino }}</td>
        <td v-if="hasGroup('Admin')">
          <button @click="confirmDelete(item.id)" class="btn btn-danger">
            <i style="color: white" class="bi bi-trash"></i>
          </button>
          <button style="margin-left: 10px" class="btn btn-warning">
            <router-link
              :to="{ name: 'EditarDestino', params: { id: item.id } }"
            >
              <i style="color: white" class="bi bi-pencil-square"></i>
            </router-link>
          </button>
        </td>
      </tr>
    </tbody>
  </table>
  <br />
  <br />
</template>

<style scoped>
.search-container {
  padding: 10px;
}

.search-form {
  display: flex;
  justify-content: flex-end;
  margin-left: auto;
  margin-right: 0;
  margin-bottom: 2em;
}

@media (max-width: 768px) {
  .search-form {
    margin-left: auto;
    margin-right: 10px;
  }
}
</style>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "DestinoView",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      destinos: [],
      cliente: "",
      destino: "",
      searchQuery: "",
      debounceTimeout: null,
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [], // Almacenará los grupos del usuario
    };
  },

  mounted() {
    this.getDestinos();
  },
  async created() {
    // Obtener los permisos y grupos del usuario al cargar el componente
    await this.fetchUserPermissionsAndGroups();
  },
  methods: {
    hasPermission(permission) {
      return this.userPermissions.includes(permission);
    },
    hasGroup(group) {
      return this.userGroups.includes(group);
    },
    async fetchUserPermissionsAndGroups() {
      try {
        const userId = localStorage.getItem("userid");
        if (userId) {
          const response = await axios.get(
            `/api/user/${userId}/permissions-and-groups/`
          );
          this.userPermissions = response.data.permissions;
          this.userGroups = response.data.groups;
        }
      } catch (error) {
        console.error("Error al obtener permisos y grupos:", error);
      }
    },
    getDestinos() {
      axios
        .get("http://127.0.0.1:8000/api/destinos/")
        .then((response) => {
          console.log(response);
          this.destinos = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    async searchDestino() {
      this.$store.commit("setIsLoading", true);

      axios
        .get(`/api/destinos/?destino=${this.searchQuery}`)
        .then((response) => {
          this.destinos = response.data;
        })
        .catch((error) => {
          console.log(error);
        });

      this.$store.commit("setIsLoading", false);
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchDestino();
      }, 300); // Ajusta el tiempo de espera según sea necesario
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
          this.deleteDestino(id);
        }
      });
    },

    async deleteDestino(id) {
      try {
        await axios.delete(`/api/destinos/${id}/`);
        // Actualizar la lista de destinos eliminando el que se ha borrado
        this.destinos = this.destinos.filter((item) => item.id !== id);
        Swal.fire(
          "Eliminado!",
          "El destino ha sido eliminado exitosamente.",
          "success"
        );
      } catch (error) {
        console.error("Error al eliminar el destino:", error);
        Swal.fire("Error", "Hubo un error al eliminar el destino.", "error");
      }
    },
  },
};
</script>

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
nav .pagination {
  display: flex;
  justify-content: center;
  align-items: center;
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
