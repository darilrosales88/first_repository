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
      <form class="d-flex search-form" @submit.prevent="searchEntidad">
        <div class="input-container">
          <i class="bi bi-search"></i>
          <input
            class="form-control form-control-sm me-2"
            type="search"
            placeholder="Buscar por nombre, abreviatura o OSDE/OACE"
            aria-label="Buscar"
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
        to="/AdicionarEntidades"
      >
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h3
      style="
        margin-top: -33px;
        font-size: 18px;
        margin-right: 630px;
        color: #002a68;
      "
    >
      Listado de entidades
    </h3>
    <br />
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Nombre</th>
            <th scope="col">Abreviatura</th>
            <th scope="col">OSDE/OACE u Organismo</th>
            <th scope="col">Tipo de entidad</th>
            <th scope="col">Provincia</th>
            <th scope="col">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in entidades" :key="item.id">
            <td>{{ item.nombre }}</td>
            <td>{{ item.abreviatura }}</td>
            <td>{{ item.o_o_o_name }}</td>
            <td>{{ item.tipo_entidad_name }}</td>
            <td>{{ item.provincia_name }}</td>
            <td>
              <button
                @click="openEntidadesDetailsModal(item)"
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
                    :to="{ name: 'EditarEntidades', params: { id: item.id } }"
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

      <!-- Mensaje cuando no hay resultados -->
      <h1 v-if="!busqueda_existente">
        No existe ningún registro asociado a ese parámetro de búsqueda.
      </h1>

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
          <li
            class="page-item"
            :class="{ disabled: currentPage === totalPages }"
          >
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
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "EntidadesView",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      entidades: [], // Lista paginada de entidades
      searchQuery: "", // Término de búsqueda
      debounceTimeout: null, // Timeout para el debounce
      userPermissions: [], // Permisos del usuario
      userGroups: [], // Grupos del usuario
      showNoId: false,
      currentPage: 1, // Página actual
      totalPages: 1, // Total de páginas
      pages: [], // Lista de páginas visibles
      busqueda_existente: true, // Controla si hay resultados de búsqueda
    };
  },
  async created() {
    await this.fetchUserPermissionsAndGroups();
    await this.getEntidades();
  },
  methods: {
    toggleNoIdVisibility() {
      this.showNoId = !this.showNoId;
    },
    // Verifica si el usuario tiene un permiso específico
    hasPermission(permission) {
      return this.userPermissions.some((p) => p.name === permission);
    },
    // Verifica si el usuario pertenece a un grupo específico
    hasGroup(group) {
      return this.userGroups.some((g) => g.name === group);
    },
    // Obtiene los permisos y grupos del usuario
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
    // Obtiene las entidades con paginación
    async getEntidades() {
      try {
        this.$store.commit("setIsLoading", true);
        const response = await axios.get("/api/entidades/", {
          params: {
            page: this.currentPage,
            search: this.searchQuery,
          },
        });
        this.entidades = response.data.results;
        this.totalPages = Math.ceil(response.data.count / 15);
        this.updatePages();
        this.busqueda_existente = this.entidades.length > 0;
      } catch (error) {
        console.error("Error al obtener las entidades:", error);
        Swal.fire("Error", "No se pudieron cargar las entidades.", "error");
      } finally {
        this.$store.commit("setIsLoading", false);
      }
    },
    // Busca entidades con paginación
    async searchEntidad() {
      try {
        this.$store.commit("setIsLoading", true);
        this.currentPage = 1; // Reiniciar a la primera página al buscar
        const response = await axios.get("/api/entidades/", {
          params: {
            page: this.currentPage,
            search: this.searchQuery,
          },
        });
        this.entidades = response.data.results;
        this.totalPages = Math.ceil(response.data.count / 15);
        this.updatePages();
        this.busqueda_existente = this.entidades.length > 0;
      } catch (error) {
        console.error("Error al buscar entidades:", error);
        this.busqueda_existente = false;
      } finally {
        this.$store.commit("setIsLoading", false);
      }
    },
    // Debounce para evitar múltiples llamadas durante la escritura
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchEntidad();
      }, 300);
    },
    // Confirma la eliminación de una entidad
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
          this.deleteEntidad(id);
        }
      });
    },
    // Elimina una entidad
    async deleteEntidad(id) {
      try {
        await axios.delete(`/api/entidades/${id}/`);
        // Si era el último elemento de la página, retroceder una página
        if (this.entidades.length === 1 && this.currentPage > 1) {
          this.currentPage -= 1;
        }
        await this.getEntidades();
        Swal.fire(
          "Eliminado!",
          "La entidad ha sido eliminada exitosamente.",
          "success"
        );
      } catch (error) {
        console.error("Error al eliminar la entidad:", error);
        Swal.fire("Error", "Hubo un error al eliminar la entidad.", "error");
      }
    },
    // Cambia de página
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        this.getEntidades();
      }
    },
    // Actualiza la lista de páginas visibles
    updatePages() {
      const startPage = Math.max(1, this.currentPage - 2);
      const endPage = Math.min(this.totalPages, this.currentPage + 2);
      this.pages = [];
      for (let i = startPage; i <= endPage; i++) {
        this.pages.push(i);
      }
    },
    openEntidadesDetailsModal(Entidades) {
      Swal.fire({
        title: "Detalles de la Entidad",
        html: `
          <div style="text-align: left;">
            <p><strong>Nombre:</strong> ${Entidades.nombre}</p>
            <p><strong>Abrebiatura:</strong> ${Entidades.abreviatura}</p>
            <p><strong>OSDE/OACE u Organismo:</strong> ${Entidades.o_o_o_name}</p>
            <p><strong>Tipo de Entidad:</strong> ${Entidades.tipo_entidad_name}</p>
            <p><strong>Provincia:</strong> ${Entidades.provincia_name}</p>
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
nav .pagination {
  display: flex;
  justify-content: center;
  align-items: center;
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
