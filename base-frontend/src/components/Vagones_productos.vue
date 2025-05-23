<template>
  <div class="container py-3">
    <!-- Encabezado con acciones -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <!-- Botón de agregar - más destacado -->
      <button class="btn btn-link p-0" @click="showModal = true">
        <router-link
          v-if="hasGroup('AdminUFC')"
          to="AdicionarVagonProducto"
          title="Agregar nuevo vagón con productos"
        >
          <i class="bi bi-plus-circle fs-3"></i>
        </router-link>
        <!-- Icono grande -->
      </button>

      <form @submit.prevent="search_producto" class="search-container">
        <div class="input-group">
          <input
            type="search"
            class="form-control"
            placeholder="Origen, Tipo Equipo, Producto"
            v-model="searchQuery"
            @input="handleSearchInput"
          />
          <span
            class="position-absolute top-50 start-0 translate-middle-y ps-2"
          >
            <i class="bi bi-search"></i>
          </span>
        </div>
      </form>
    </div>
    <h6>Vagones y productos</h6>
    <!-- Tabla responsive con mejoras -->
    <div class="table table-responsive">
      <table class="table table-hover mb-0">
        <thead>
          <tr>
            <th scope="col" style="width: 50px">No</th>
            <th scope="col">Origen</th>
            <th scope="col">Combustible</th>
            <th scope="col">Vagones situados</th>
            <th scope="col">Vagones cargados</th>
            <th scope="col">Productos</th>
            <th scope="col">Acciones</th>
          </tr>
          <tr v-if="!busqueda_existente">
            <td colspan="8" class="text-center text-muted py-4">
              <i class="bi bi-exclamation-circle fs-4"></i>
              <p class="mt-2">
                No se encontraron resultados para "{{ searchQuery }}"
              </p>
            </td>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="(vagon, index) in vagones_productos"
            :key="vagon.id"
            class="align-middle"
          >
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ vagon.origen }}</td>
            <td>{{ vagon.tipo_combustible_name || "-" }}</td>
            <td>{{ vagon.vagones_situados }}</td>
            <td>{{ vagon.vagones_cargados }}</td>
            <td>{{ vagon.productos_list }}</td>
            <td v-if="hasGroup('AdminUFC')">
              <div class="d-flex">
                <button
                  @click="viewDetails(vagon)"
                  class="btn btn-sm btn-outline-info me-2"
                  title="Ver detalles"
                >
                  <i class="bi bi-eye-fill"></i>
                </button>
                <button
                  @click="editVagon(vagon)"
                  class="btn btn-sm btn-outline-warning me-2"
                  title="Editar"
                >
                  <i class="bi bi-pencil-square"></i>
                </button>
                <button
                  @click="confirmDelete(vagon.id)"
                  class="btn btn-sm btn-outline-danger"
                  title="Eliminar"
                >
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Paginación mejorada -->
    <div class="d-flex justify-content-between align-items-center">
      <div class="text-muted small">
        Mostrando {{ vagones_productos.length }} de {{ totalItems }} registros
      </div>
      <nav aria-label="Page navigation">
        <ul class="pagination pagination-sm mb-0">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link" @click="previousPage">
              <i class="bi bi-chevron-left"></i>
            </button>
          </li>
          <li class="page-item disabled">
            <span class="page-link">
              Página {{ currentPage }} de
              {{ Math.ceil(totalItems / itemsPerPage) }}
            </span>
          </li>
          <li
            class="page-item"
            :class="{ disabled: currentPage * itemsPerPage >= totalItems }"
          >
            <button class="page-link" @click="nextPage">
              <i class="bi bi-chevron-right"></i>
            </button>
          </li>
        </ul>
      </nav>
    </div>
    <!-- Termina la paginacion -->

    <!-- Modal de detalles -->
    <div v-if="mostrarModalDetalles" class="modal-backdrop">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Detalles del Vagón y Productos</h5>
          <button @click="cerrarModalDetalles" class="btn-close">
            <i class="bi bi-x"></i>
          </button>
        </div>
        <div class="modal-body" v-if="vagonSeleccionado">
          <!-- Información básica -->
          <div class="row mb-3">
            <div class="col-md-6">
              <p>
                <strong>Tipo de origen:</strong>
                {{ vagonSeleccionado.tipo_origen_name || "N/A" }}
              </p>
              <p>
                <strong>Origen:</strong> {{ vagonSeleccionado.origen || "N/A" }}
              </p>
              <p>
                <strong>Tipo de combustible:</strong>
                {{ vagonSeleccionado.tipo_combustible_name || "N/A" }}
              </p>
              <p>
                <strong>Tipo de equipo ferroviario:</strong>
                {{ vagonSeleccionado.tipo_equipo_ferroviario_name || "N/A" }}
              </p>
            </div>
            <div class="col-md-6">
              <p>
                <strong>Tipo de producto:</strong>
                {{ vagonSeleccionado.tipo_producto || "N/A" }}
              </p>
              <p>
                <strong>Plan mensual:</strong>
                {{ vagonSeleccionado.plan_mensual || "N/A" }}
              </p>
              <p>
                <strong>Plan anual:</strong>
                {{ vagonSeleccionado.plan_anual || "N/A" }}
              </p>
            </div>
          </div>

          <!-- Estadísticas -->
          <div class="row mb-3">
            <div class="col-md-6">
              <p>
                <strong>Vagones situados:</strong>
                {{ vagonSeleccionado.vagones_situados || "0" }}
              </p>
              <p>
                <strong>Vagones cargados:</strong>
                {{ vagonSeleccionado.vagones_cargados || "0" }}
              </p>
            </div>
            <div class="col-md-6">
              <p>
                <strong>Plan acumulado día anterior:</strong>
                {{ vagonSeleccionado.plan_acumulado_dia_anterior || "0" }}
              </p>
              <p>
                <strong>Real acumulado día anterior:</strong>
                {{ vagonSeleccionado.real_acumulado_dia_anterior || "0" }}
              </p>
              <p>
                <strong>Plan del día :</strong>
                {{ vagonSeleccionado.plan_dia || "0" }}
              </p>
            </div>
          </div>

          <!-- Productos asociados -->
          <div class="mb-3">
            <h6 class="border-bottom pb-2">Productos asociados</h6>
            <div
              v-if="
                vagonSeleccionado.productos_list &&
                vagonSeleccionado.productos_list.length > 0
              "
            >
              <p>{{ vagonSeleccionado.productos_list }}</p>
            </div>
            <div v-else>
              <p class="text-muted">No hay productos asociados</p>
            </div>
          </div>

          <!-- Observaciones -->
          <div class="mb-3">
            <h6 class="border-bottom pb-2">Observaciones</h6>
            <p v-if="vagonSeleccionado.observaciones">
              {{ vagonSeleccionado.observaciones }}
            </p>
            <p v-else class="text-muted">No hay observaciones registradas</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "VagonesProductos",

  data() {
    return {
      vagones_productos: [], // Lista de vagones con productos
      allRecords: [], // Copia completa de todos los registros para filtrado local
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 0,
      searchQuery: "",
      debounceTimeout: null,
      busqueda_existente: true,
      userPermissions: [],
      userGroups: [],
      showContent: false,
      mostrarModalDetalles: false,
      vagonSeleccionado: null,
      loading: false,
    };
  },

  async mounted() {
    await this.getVagonesProductos();
    await this.fetchUserPermissionsAndGroups();
  },

  methods: {
    toggleContentVisibility() {
      this.showContent = !this.showContent;
    },

    hasGroup(group) {
      return this.userGroups.some((g) => g.name === group);
    },

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

    async getVagonesProductos() {
      this.loading = true;
      const today = new Date();
      const fechaFormateada = `${today.getFullYear()}-${String(
        today.getMonth() + 1
      ).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;

      try {
        const infoID = await axios.get(
          `/ufc/verificar-informe-existente/?fecha_operacion=${fechaFormateada}`
        );
        if (infoID.data.existe) {
          const response = await axios.get("/ufc/vagones-productos/", {
            params: {
              page: this.currentPage,
              page_size: this.itemsPerPage,
              informe: infoID.data.id,
            },
          });

          this.vagones_productos = response.data.results;
          this.allRecords = [...response.data.results]; // Guardar copia completa para filtrado
          this.totalItems = response.data.count;
          this.busqueda_existente = true;
        }
      } catch (error) {
        console.error("Error al obtener los vagones con productos:", error);
        this.busqueda_existente = false;
      } finally {
        this.loading = false;
      }
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        if (!this.searchQuery.trim()) {
          this.vagones_productos = [...this.allRecords];
          this.busqueda_existente = true;
          return;
        }

        const query = this.searchQuery.toLowerCase();
        this.vagones_productos = this.allRecords.filter((item) => {
          const tipoEquipo =
            item.tipo_equipo_ferroviario_name?.toLowerCase() || "";
          const tipoOrigen = item.origen?.toLowerCase() || "";
          const productos = item.productos_list?.toLowerCase() || "";

          return (
            tipoEquipo.includes(query) ||
            tipoOrigen.includes(query) ||
            productos.includes(query)
          );
        });

        this.busqueda_existente = this.vagones_productos.length > 0;
      }, 300);
    },

    // Métodos de paginación
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.getVagonesProductos();
      }
    },

    nextPage() {
      if (this.currentPage * this.itemsPerPage < this.totalItems) {
        this.currentPage++;
        this.getVagonesProductos();
      }
    },

    goToPage(page) {
      this.currentPage = page;
      this.getVagonesProductos();
    },

    async deleteVagon(id) {
      try {
        await axios.delete(`/ufc/vagones-productos/${id}/`);
        this.vagones_productos = this.vagones_productos.filter(
          (objeto) => objeto.id !== id
        );
        Swal.fire(
          "Eliminado!",
          "El registro ha sido eliminado exitosamente.",
          "success"
        );
      } catch (error) {
        console.error("Error al eliminar el registro:", error);
        Swal.fire("Error", "Hubo un error al eliminar el registro.", "error");
      }
    },

    viewDetails(vagon) {
      this.vagonSeleccionado = vagon;
      this.mostrarModalDetalles = true;
    },

    cerrarModalDetalles() {
      this.mostrarModalDetalles = false;
      this.vagonSeleccionado = null;
    },

    editVagon(vagon) {
      // Aquí puedes implementar la navegación a la página de edición
      this.$router.push({
        name: "EditarVagonesyProductos",
        params: { id: vagon.id },
      });
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
          this.deleteVagon(id);
        }
      });
    },

    handleApiError(error, action) {
      let errorMsg = `Error al ${action}`;
      if (error.response) {
        errorMsg += ` (${error.response.status})`;
        if (error.response.data) {
          errorMsg += `: ${JSON.stringify(error.response.data)}`;
        }
      } else {
        errorMsg += `: ${error.message}`;
      }
      console.error(errorMsg, error);
      Swal.fire("Error", errorMsg, "error");
    },
  },
};
</script>

<style scoped>
/* Estilos para el contenedor del buscador */
.search-container {
  position: relative;
  width: 100%;
  max-width: 300px; /* Ancho máximo del buscador */
}

/* Estilos para el input del buscador */
.search-container input {
  padding-right: 40px; /* Espacio para el icono de lupa */
  border-radius: 20px; /* Bordes redondeados */
}

/* Estilos para el icono de lupa */
.search-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #888; /* Color del icono */
  pointer-events: none; /* Evita que el icono interfiera con el input */
}

/* Estilos para la tabla responsive */
.table-responsive {
  overflow-x: auto; /* Permite desplazamiento horizontal en pantallas pequeñas */
}

/* Estilos para el modal */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Fondo semitransparente */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* Asegura que el modal esté por encima de todo */
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  width: 90%;
  max-width: 500px; /* Ancho máximo del modal */
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.modal-title {
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.modal-body {
  margin-bottom: 20px;
}

/* Estilos para el icono de agregar */
.btn-link {
  color: #007bff; /* Color azul para el icono */
  text-decoration: none; /* Sin subrayado */
}

.btn-link:hover {
  color: #0056b3; /* Color azul más oscuro al pasar el mouse */
}

.search-container {
  position: relative;
  width: 100%;
  max-width: 300px;
}

.search-container input {
  padding-left: 2.5rem !important; /* Espacio para el icono */
  border-radius: 20px !important;
}

.search-container .bi-search {
  color: #6c757d; /* Color gris para el icono */
  z-index: 10;
}

/* Para asegurar que el input group conserve los estilos */
.input-group {
  width: 100%;
}

/* Estilos para los botones de acción */
.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
  line-height: 1.5;
  border-radius: 0.2rem;
}

.btn-outline-info {
  color: #17a2b8;
  border-color: #17a2b8;
}

.btn-outline-warning {
  color: #ffc107;
  border-color: #ffc107;
}

.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
}

.btn-outline-info:hover,
.btn-outline-warning:hover,
.btn-outline-danger:hover {
  color: #fff;
}
</style>
