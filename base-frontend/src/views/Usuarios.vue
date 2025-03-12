<template>
  <div>
    <img style="width: 250px" src="@/assets/Imagenes/mitrans.png" />
    <Navbar-Component />

    <form
      class="d-flex"
      @submit.prevent="search_user"
      style="padding: 10px; margin-left: 75em"
    >
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

    <div style="margin-top: -4em">
      <br />
      <router-link
        style="text-decoration: none; color: black; margin-right: 1330px"
        to="/AdicionarUsuario"
      >
        Crear usuario <i class="bi bi-plus-circle"></i>
      </router-link>
      <br />
    </div>

    <br />

    <table class="table">
      <thead>
        <tr>
          <th scope="col">No</th>
          <th scope="col">Nombre</th>
          <th scope="col">Apellidos</th>
          <th scope="col">Usuario</th>
          <th scope="col">Email</th>
          <th scope="col">Entidad</th>
          <th scope="col">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in usuarios" :key="item.id">
          <th scope="row" style="background-color: white">{{ index + 1 }}</th>
          <td>{{ item.first_name }}</td>
          <td>{{ item.last_name }}</td>
          <td>{{ item.username }}</td>
          <td>{{ item.email }}</td>
          <td>{{ item.entidad_name }}</td>
          <td>
            <button
              @click.prevent="confirmDelete(item.id)"
              class="btn btn-danger"
            >
              <i style="color: white" class="bi bi-trash"></i>
            </button>
            <button style="margin-left: 10px" class="btn btn-warning">
              <router-link
                :to="{ name: 'EditarUsuario', params: { id: item.id } }"
              >
                <i style="color: white" class="bi bi-pencil-square"></i>
              </router-link>
            </button>
            <button
              style="margin-left: 10px"
              class="btn btn-info"
              @click="openUserDetailsModal(item)"
            >
              <i style="color: white" class="bi bi-eye"></i>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

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

/*estilos para el modal */
.custom-swal-popup {
  border-radius: 10px;
  font-family: Arial, sans-serif;
}

.custom-swal-title {
  font-size: 24px;
  color: #333;
}

.custom-swal-html {
  font-size: 16px;
  color: #555;
}
</style>

<script>
import Swal from "sweetalert2";
import axios from "axios";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "Usuarios",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      usuarios: [],
      gruposDisponibles: [], // Lista de grupos disponibles
      permisosDisponibles: [], // Lista de permisos disponibles
      searchQuery: "",
      debounceTimeout: null,
    };
  },
  mounted() {
    this.get_usuarios();
    this.fetchGroups();
    this.fetchPermisosDisponibles();
  },
  methods: {
    async get_usuarios() {
      this.$store.commit("setIsLoading", true);
      try {
        const response = await axios.get("/apiAdmin/users/");
        this.usuarios = response.data;
      } catch (error) {
        console.error(error);
      } finally {
        this.$store.commit("setIsLoading", false);
      }
    },
    async fetchGroups() {
      try {
        const response = await axios.get("/apiAdmin/groups/");
        this.gruposDisponibles = response.data;
      } catch (error) {
        console.error("Error al obtener los grupos:", error);
      }
    },
    async fetchPermisosDisponibles() {
      try {
        const response = await axios.get("/apiAdmin/permisos/");
        this.permisosDisponibles = response.data;
      } catch (error) {
        console.error("Error al obtener los permisos:", error);
      }
    },

    async search_user() {
      this.$store.commit("setIsLoading", true);
      try {
        const response = await axios.get(
          `/apiAdmin/users/?username=${this.searchQuery}`
        );
        this.usuarios = response.data;
      } catch (error) {
        console.error(error);
      } finally {
        this.$store.commit("setIsLoading", false);
      }
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
          this.delete_unidad(id);
        }
      });
    },
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.search_user();
      }, 300);
    },
    async delete_unidad(id) {
      try {
        await axios.delete(`/apiAdmin/users/${id}/`);
        this.usuarios = this.usuarios.filter((usuario) => usuario.id !== id);
        Swal.fire(
          "Eliminado!",
          "El usuario se ha eliminado exitosamente.",
          "success"
        );
      } catch (error) {
        console.error("Error al eliminar el usuario:", error);
        Swal.fire("Error", "Hubo un error al eliminar el usuario.", "error");
      }
    },
    openUserDetailsModal(user) {
      // Mapear IDs de grupos a nombres
      const gruposAsignados =
        user.groups && user.groups.length > 0
          ? user.groups
              .map((groupId) => {
                const grupo = this.gruposDisponibles.find(
                  (g) => g.id === groupId
                );
                return grupo ? grupo.name : "Desconocido";
              })
              .join(", ")
          : "Ninguno";

      // Mapear IDs de permisos a nombres
      const permisosAsignados =
        user.user_permissions && user.user_permissions.length > 0
          ? user.user_permissions
              .map((permisoId) => {
                const permiso = this.permisosDisponibles.find(
                  (p) => p.id === permisoId
                );
                return permiso ? permiso.name : "Desconocido";
              })
              .join(", ")
          : "Ninguno";

      Swal.fire({
        title: "Detalles del Usuario",
        html: `
            <div style="text-align: left;">
                <p><strong>Nombre:</strong> ${user.first_name}</p>
                <p><strong>Apellidos:</strong> ${user.last_name}</p>
                <p><strong>Usuario:</strong> ${user.username}</p>
                <p><strong>Email:</strong> ${user.email}</p>
                <p><strong>Entidad:</strong> ${user.entidad_name}</p>
                <p><strong>Cargo:</strong> ${user.cargo_name}</p>
                <p><strong>Grupos Asignados:</strong> ${gruposAsignados}</p>
                <p><strong>Rol asignado</strong> ${user.role}</p>
                <p><strong>Permisos Asignados:</strong> ${permisosAsignados}</p>
            </div>
        `,
        width: "600px",
        customClass: {
          popup: "custom-swal-popup",
          title: "custom-swal-title",
          htmlContainer: "custom-swal-html",
        },
      });
    },
  },
};
</script>
