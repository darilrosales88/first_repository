<template>
  <div>
    <div style="background-color: #002a68; color: white; text-align: right">
      <h6>Bienvenido:</h6>
    </div>
    <br />
    <Navbar-Component />
    <br />
    <br />
    <div class="search-container">
      <form class="d-flex" @submit.prevent="search_unidad_medida">
        <div class="input-container">
          <i class="bi bi-search"></i>
          <input
            class="form-control form-control-sm me-2"
            type="search"
            placeholder="magnitud,unidad de medida o símbolo"
            aria-label="Search"
            v-model="searchQuery"
            @input="handleSearchInput"
            style="width: 200px; padding-left: 5px; margin-top: -70px"
          />
        </div>
      </form>
    </div>
    <div class="create-button-container">
      <router-link
        v-if="hasGroup('Admin')"
        class="create-button"
        to="AdicionarUM"
      >
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h3
      style="
        margin-top: -33px;
        font-size: 18px;
        margin-right: 500px;
        color: #002a68;
      "
    >
      Listado de unidades de medidas
    </h3>
    <br />
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Magnitud</th>
            <th scope="col">Unidad de medida</th>
            <th scope="col">Símbolo</th>
            <!-- Mostrar la columna "Acciones" solo si el usuario pertenece al grupo "Admin" -->
            <th scope="col">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in unidades" :key="item.id">
            <td>{{ item.magnitud }}</td>
            <td>{{ item.unidad_medida }}</td>
            <td>{{ item.simbolo }}</td>
            <!-- Mostrar los botones de acciones solo si el usuario pertenece al grupo "Admin" -->
            <td>
              <button
                @click="openUMDetailsModal(item)"
                class="btn btn-info btn-small btn-eye"
                v-html="
                  showNoId
                    ? '<i class=\'bi bi-eye-slash-fill\'></i>'
                    : '<i class=\'bi bi-eye-fill\'></i>'
                "
              ></button>
              <span v-if="hasGroup('Admin')">
                <button class="btn btn-warning btn-small">
                  <router-link
                    :to="{ name: 'EditarUM', params: { id: item.id } }"
                  >
                    <i style="color: black" class="bi bi-pencil-square"></i>
                  </router-link>
                </button>
                <button
                  @click.prevent="confirmDelete(item.id)"
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
    <!-- Paginación -->
    <nav aria-label="Page navigation example">
      <ul class="pagination">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <a
            class="page-link"
            href="#"
            @click.prevent="changePage(currentPage - 1)"
            >Anterior</a
          >
        </li>
        <li
          class="page-item"
          v-for="page in pages"
          :key="page"
          :class="{ active: page === currentPage }"
        >
          <a class="page-link" href="#" @click.prevent="changePage(page)">{{
            page
          }}</a>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <a
            class="page-link"
            href="#"
            @click.prevent="changePage(currentPage + 1)"
            >Siguiente</a
          >
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "UMView",

  components: {
    NavbarComponent,
  },

  data() {
    return {
      unidades: [],
      searchQuery: "", // Para la búsqueda
      debounceTimeout: null, // Para el debounce en la búsqueda
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [], // Almacenará los grupos del usuario
      currentPage: 1, // Página actual
      totalPages: 1, // Total de páginas
      pages: [], // Lista de páginas visibles
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
      return this.userPermissions.some((p) => p.name === permission);
    },
    hasGroup(group) {
      return this.userGroups.some((g) => g.name === group);
    },
    // Obtiene los permisos y grupos del usuario desde el backend
    async fetchUserPermissionsAndGroups() {
      try {
        const userId = localStorage.getItem("userid");
        if (userId) {
          const response = await axios.get(
            `/apiAdmin/user/${userId}/permissions-and-groups/`
          );
          this.userPermissions = response.data.permissions;
          this.userGroups = response.data.groups;
        }
      } catch (error) {
        console.error("Error al obtener permisos y grupos:", error);
      }
    },

    async get_unidades() {
      this.$store.commit("setIsLoading", true);
      try {
        const response = await axios.get("/api/unidades_medida/", {
          params: {
            page: this.currentPage,
            search: this.searchQuery,
          },
        });
        this.unidades = response.data.results; // Obtener los registros de la página actual
        this.totalPages = Math.ceil(response.data.count / 15); // Calcular el número total de páginas
        this.updatePages(); // Actualizar la lista de páginas visibles
        this.busqueda_existente = true; // Reinicia la variable al cargar todas las unidades de medida
      } catch (error) {
        console.error("Error al obtener las unidades de medida:", error);
        Swal.fire(
          "Error",
          "No se pudieron cargar las unidades de medida.",
          "error"
        );
      }
      this.$store.commit("setIsLoading", false);
    },

    async search_unidad_medida() {
      this.$store.commit("setIsLoading", true);
      this.currentPage = 1; // Reiniciar a la primera página al realizar una búsqueda
      try {
        const response = await axios.get("/api/unidades_medida/", {
          params: {
            page: this.currentPage,
            search: this.searchQuery,
          },
        });
        this.unidades = response.data.results;
        this.totalPages = Math.ceil(response.data.count / 15);
        this.updatePages();
        this.busqueda_existente = this.unidades.length > 0;
      } catch (error) {
        console.error("Error al buscar unidades de medida:", error);
        this.busqueda_existente = false; // Asegura que busqueda_existente sea false en caso de error
      }
      this.$store.commit("setIsLoading", false);
    },
    updatePages() {
      const startPage = Math.max(1, this.currentPage - 2); // Mostrar 2 páginas antes de la actual
      const endPage = Math.min(this.totalPages, this.currentPage + 2); // Mostrar 2 páginas después de la actual
      this.pages = [];
      for (let i = startPage; i <= endPage; i++) {
        this.pages.push(i);
      }
    },

    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        this.get_unidades();
      }
    },
    // Usar SweetAlert2 para confirmar la eliminación
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
        this.search_unidad_medida();
      }, 300); // Ajusta el tiempo de espera según sea necesario
    },

    // Eliminar unidad de medida
    async delete_unidad(id) {
      try {
        await axios.delete(`/api/unidades_medida/${id}/`);
        // Actualizar la lista de unidades de medida eliminando el que se ha borrado
        this.unidades = this.unidades.filter((unidad) => unidad.id !== id);
        Swal.fire(
          "Eliminado!",
          "La unidad de medida ha sido eliminada exitosamente.",
          "success"
        );
      } catch (error) {
        console.error("Error al eliminar la unidad de medida:", error);
        Swal.fire(
          "Error",
          "Hubo un error al eliminar la unidad de medida.",
          "error"
        );
      }
    },
    openUMDetailsModal(UM) {
      // Mapear IDs de grupos a nombres
      const gruposAsignados =
        UM.groups && UM.groups.length > 0
          ? UM.groups
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
        UM.UM_permissions && UM.UM_permissions.length > 0
          ? UM.UM_permissions.map((permisoId) => {
              const permiso = this.permisosDisponibles.find(
                (p) => p.id === permisoId
              );
              return permiso ? permiso.name : "Desconocido";
            }).join(", ")
          : "Ninguno";

      Swal.fire({
        title: "Detalles de la UM",
        html: `
            <div style="text-align: left;">
                <p><strong>Magnitud:</strong> ${UM.magnitud}</p>
                <p><strong>Unidad de medida:</strong> ${UM.unidad_medida}</p>
                <p><strong>Símbolo:</strong> ${UM.simbolo}</p>
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
<style scoped>
.search-container input::placeholder {
  font-size: 14px;
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
.input-container {
  position: relative;
  display: inline-block;
}

.input-container .bi {
  position: absolute;
  left: 180px;
  color: #999;
  margin-top: -55px;
  transform: translateY(-50%);
  pointer-events: none; /* Para que el ícono no interfiera con el clic en el input */
}
nav .pagination {
  display: flex;
  justify-content: center;
  align-items: center;
}
.large-icon {
  font-size: 1.7rem; /* Tamaño del ícono */
}
table {
  width: 84%;
  border-collapse: collapse;
  margin-left: 190px;
  margin-bottom: 10px;
  font-size: 0.875rem;
}

th,
td {
  padding: 0.15rem; /* Reducir el padding */
  white-space: nowrap;
}

th {
  background-color: #f2f2f2;
}

.btn {
  cursor: pointer;
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
  background: none; /* Asegura que no haya fondo al hacer hover */
}

.btn:focus {
  outline: none; /* Elimina el borde de foco al hacer clic */
  box-shadow: none; /* Elimina cualquier sombra de foco en algunos navegadores */
}

.create-button-container {
  margin-top: -80px;
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
