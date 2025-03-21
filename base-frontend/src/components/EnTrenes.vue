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
              placeholder="Origen, Destino, Producto, Locomotora"
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
              <td>{{ tren.producto_name }}</td>
              <td>{{ tren.cantidad_vagones }}</td>
              <td>{{ tren.origen }}</td>
              <td>{{ tren.destino }}</td>

              <td>
                <!--   <button
                  @click="openCargoDetailsModal(item)"
                  class="btn btn-info btn-small btn-eye"
                  v-html="
                    showNoId
                      ? '<i class=\'bi bi-eye-slash-fill\'></i>'
                      : '<i class=\'bi bi-eye-fill\'></i>'
                  "
                ></button>

                <button class="btn btn-warning btn-small">
                  <router-link
                    :to="{ name: 'EditarEnTren', params: { id: item.id } }"
                  >
                    <i style="color: black" class="bi bi-pencil-square"></i>
                  </router-link>
                </button>
                <button class="btn btn-danger btn-small">
                  <i class="bi bi-trash"></i>
                </button> -->
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
                    class="btn btn-danger btn-small btn-eye"
                    style="margin-left: 3%"
                  >
                    <router-link
                      :to="{ name: 'EditarEnTren', params: { id: tren.id } }"
                    >
                      <i style="color: black" class="bi bi-pencil-square"></i>
                    </router-link>
                  </button>
                  <button
                    style="margin-left: 5px"
                    @click.prevent="confirmDelete(tren.id)"
                    class="btn btn-danger btn-small"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="pagination-container" style="padding-left: 15%">
      <button
        @click="previousPage"
        :disabled="currentPage === 1"
        class="btn btn-primary"
      >
        Anterior
      </button>
      <span style="margin: 0 10px">
        Página {{ currentPage }} de {{ Math.ceil(totalItems / itemsPerPage) }}
      </span>
      <button
        @click="nextPage"
        :disabled="currentPage * itemsPerPage >= totalItems"
        class="btn btn-primary"
      >
        Siguiente
      </button>
    </div>
  </div>
</template>

<style scoped>
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.pagination-container button {
  margin: 0 5px;
}
.btn-small {
  font-size: 22px; /* Aumenta el tamaño del ícono */
  color: black;
  margin-right: 5px;
  outline: none; /* Elimina el borde de foco */
  border: none;
  background: none; /* Elimina el fondo */
  padding: 0; /* Elimina el padding para que solo se vea el ícono */
}
.btn-eye {
  font-size: 22px; /* Aumenta el tamaño del ícono */
  margin-right: 5px;
  outline: none; /* Elimina el borde de foco */
  border: none;
  background: none; /* Elimina el fondo */
  padding: 0; /* Elimina el padding para que solo se vea el ícono */
}
.btn:hover {
  scale: 1.1; /* Asegura que no haya fondo al hacer hover */
}

.btn:focus {
  outline: none; /* Elimina el borde de foco al hacer clic */
  box-shadow: none; /* Elimina cualquier sombra de foco en algunos navegadores */
}
</style>
<script>
import axios from "axios";
import Swal from "sweetalert2";
export default {
  name: "EnTrenes",

  data() {
    return {
      en_trenes: [], // Lista de trenes
      currentPage: 1, // Página actual
      itemsPerPage: 10, // Elementos por página
      totalItems: 0, // Total de elementos
      searchQuery: "", // Búsqueda
      debounceTimeout: null,
      busqueda_existente: true,
      userPermissions: [],
      userGroups: [],
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
        const response = await axios.get("/ufc/en-trenes/", {
          params: {
            page: this.currentPage, // Página actual
            page_size: this.itemsPerPage, // Elementos por página
          },
        });
        this.en_trenes = response.data.results; // Datos de la página actual
        this.totalItems = response.data.count; // Total de elementos
        console.log("Trenes obtenidos:", this.en_trenes);
      } catch (error) {
        console.error("Error al obtener los trenes:", error);
      }
    },

    async searchTrenes() {
      this.$store.commit("setIsLoading", true);
      try {
        const response = await axios.get("/ufc/en-trenes/", {
          params: {
            search: this.searchQuery, // Término de búsqueda
            page: this.currentPage, // Página actual
            page_size: this.itemsPerPage, // Elementos por página
          },
        });
        this.en_trenes = response.data.results; // Datos de la página actual
        this.totalItems = response.data.count; // Total de elementos
        this.busqueda_existente = this.en_trenes.length > 0;
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
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.getTrenes();
      }
    },

    // Cambiar a la página siguiente
    nextPage() {
      if (this.currentPage * this.itemsPerPage < this.totalItems) {
        this.currentPage++;
        this.getTrenes();
      }
    },

    // Cambiar a una página específica
    goToPage(page) {
      this.currentPage = page;
      this.getTrenes();
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
