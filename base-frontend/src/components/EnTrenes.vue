<template>
  <div style="padding: 20px">
    <button @click="toggleContentVisibility" class="btn btn-primary">
      <h2>En Trenes</h2>
    </button>

    <div v-if="showContent">
      <div class="d-flex" style="padding: 1%">
        <div class="create-button-container">
          <router-link
            v-if="hasPermission"
            class="create-button"
            to="AdicionarVagon"
          >
            <i class="bi bi-plus-circle large-icon"></i>
          </router-link>
        </div>

        <div class="search-container" style="padding-left: 10%">
          <form class="d-flex search-form" @submit.prevent="search_producto">
            <input
              class="form-control form-control-sm me-2"
              type="search"
              placeholder="Origen, Destino, Producto"
              aria-label="Search"
              v-model="searchQuery"
              @input="handleSearchInput"
              style="width: 200px"
            />
          </form>
        </div>
      </div>
      <div class="table-container" style="padding-left: 15%">
        <table class="table">
          <thead>
            <tr>
              <th scope="col" v-if="showNoId">No</th>
              <th scope="col">No</th>
              <th scope="col">Código_locomotora</th>
              <th scope="col">Tipo</th>
              <th scope="col">Estado</th>
              <th scope="col">Producto</th>
              <th scope="col">Cantidad de vagones</th>
              <th scope="col">Origen</th>
              <th scope="col">Destino</th>
              <th scope="col" v-if="showNoId">Descripción</th>
              <th scope="col" v-if="hasPermission">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(tren, index) in en_trenes" :key="tren.id">
              <th scope="row" style="background-color: white">
                {{ index + 1 }}
              </th>
              <td>{{ tren.numero_identificacion_locomotora }}</td>
              <td>{{ tren.tipo_equipo }}</td>
              <!-- nacionalidad_name esta declarado en el serializador -->
              <td>{{ tren.estado }}</td>
              <td>{{ tren.producto.producto_name }}</td>
              <td>{{ tren.cantidad_vagones }}</td>
              <td>{{ tren.origen }}</td>
              <td>{{ tren.destino }}</td>

              <td>
                <button
                  @click="toggleNoIdVisibility"
                  class="btn btn-info btn-small btn-eye"
                  v-html="
                    showNoId
                      ? '<i class=\'bi bi-eye-slash-fill\'></i>'
                      : '<i class=\'bi bi-eye-fill\'></i>'
                  "
                ></button>
                <span v-if="hasPermission">
                  <button
                    class="btn btn-warning bt n-small"
                    style="margin-left: 3%"
                  >
                    <router-link>
                      <i style="color: white" class="bi bi-pencil-square"></i>
                    </router-link>
                  </button>
                  <button
                    style="margin-left: 5px"
                    @click.prevent="confirmDelete(tren.id)"
                    class="btn btn-danger btn-small"
                  >
                    <i style="color: white" class="bi bi-trash"></i>
                  </button>
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Estilos para la barra de navegación */
</style>
<script>
import axios from "axios";
import Swal from "sweetalert2";
export default {
  name: "EnTrenes",

  data() {
    return {
      en_trenes: [],
      user_role: "",
      searchQuery: "",
      debounceTimeout: null, // Añadido aquí
      busqueda_existente: true,
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [], // Almacenará los grupos del usuario
      showContent: false,
    };
  },

  async mounted() {
    // Cuando el componente se monta, llamamos a las funciones necesarias// Obtener el rol del usuario
    await this.getTrenes();
    await this.hasGroup(); // Obtener la lista de trenes
    await this.fetchUserPermissionsAndGroups();
    console.log(this.user_role);
  },

  methods: {
    // Verifica si el usuario tiene un permiso específico

    hasPermission() {
      if (this.user_role === "role") {
        return true;
      } else {
        return this.user_role === "admin";
      }
    },
    toggleContentVisibility() {
      this.showContent = !this.showContent; // Alternar la visibilidad de las columnas No e Id
    },
    hasGroup(group) {
      return this.userGroups.some((g) => g.name === group);
    },
    // Obtiene los permisos y grupos del usuario desde el backend
    async fetchUserPermissionsAndGroups() {
      try {
        const userId = localStorage.getItem("userid");
        if (userId) {
          const response = await axios.get(`/apiAdmin/users/${userId}/`);
          this.userPermissions = response.data.permissions;
          this.userGroups = response.data.groups;
          this.user_role = response.data.role;
        }
      } catch (error) {
        console.error("Error al obtener permisos y grupos:", error);
      }
    },

    async getTrenes() {
      try {
        const response = await axios.get("/ufc/en-trenes/");
        this.en_trenes = response.data; // Asignar la lista de trenes
        console.log("Trenes obtenidos:", this.en_trenes);
      } catch (error) {
        console.error("Error al obtener los trenes:", error);
      }
    },

    async searchTrenes() {
      this.$store.commit("setIsLoading", true);
      try {
        const response = await axios.get(
          `/ufc/en-trenes/?origen_destino=${this.searchQuery}`
        );
        this.en_trenes = response.data;
        // Actualiza busqueda_existente basado en el resultado
        this.busqueda_existente = this.paises.length > 0;
      } catch (error) {
        console.error("Error al buscar trenes", error);
        this.busqueda_existente = false;
      }
      this.$store.commit("setIsLoading", false);
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchTrenes();
      }, 300);
    },
    async delete_tren(id) {
      try {
        await axios.delete(`/ufc/en-trenes/${id}/`);
        // Actualizar la lista de productos eliminando el que se ha borrado
        this.en_trenes = this.en_trenes.filter((tren) => tren.id !== id);

        Swal.fire(
          "Eliminado!",
          "El producto ha sido eliminado exitosamente.",
          "success"
        );
      } catch (error) {
        console.error("Error al eliminar el producto:", error);
        Swal.fire("Error", "Hubo un error al eliminar el producto.", "error");
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
          this.delete_tren(id);
        }
      });
    },
  },
};
</script>

<style>
.create-button {
  text-decoration: none;
  color: green;
  margin-left: 940px;
}
</style>
