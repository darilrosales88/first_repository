<template>
  <div class="container py-3">
    <!-- Encabezado con acciones -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <!-- Botón de agregar - más destacado -->

      <button class="btn btn-link p-0">
        <router-link to="AdicionarVagon"
          ><i class="bi bi-plus-circle fs-3"></i
        ></router-link>
      </button>

      <!-- Buscador mejorado -->
      <form @submit.prevent="search_producto" class="search-container">
        <div class="input-group">
          <span class="input-group-text bg-white border-end-0">
            <i class="bi bi-search"></i>
          </span>
          <input
            type="search"
            class="form-control border-start-0"
            placeholder="Buscar..."
            v-model="searchQuery"
            @input="handleSearchInput"
          />
        </div>
      </form>
    </div>

    <!-- Tabla responsive con mejoras -->
    <div class="table-responsive rounded-3 shadow-sm">
      <table class="table table-hover mb-0">
        <thead class="table-light">
          <tr>
            <th scope="col" style="width: 50px">#</th>
            <th scope="col">Código Locomotora</th>
            <th scope="col">Tipo</th>
            <th scope="col">Estado</th>
            <th scope="col">Producto</th>
            <th scope="col" class="text-end">Cant. Vagones</th>
            <th scope="col">Origen</th>
            <th scope="col">Destino</th>
            <th scope="col" v-if="showNoId">Descripción</th>
            <th scope="col" v-if="hasPermission" style="width: 120px">
              Acciones
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="10" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
            </td>
          </tr>

          <tr
            v-for="(tren, index) in en_trenes"
            :key="tren.id"
            class="align-middle"
          >
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ tren.numero_identificacion_locomotora || "-" }}</td>
            <td>{{ tren.tipo_equipo || "-" }}</td>
            <td>
              <span>
                {{ tren.estado || "-" }}
              </span>
            </td>
            <td>{{ tren.producto_name || "-" }}</td>
            <td class="text-end">{{ tren.cantidad_vagones || "0" }}</td>
            <td>{{ tren.origen || "-" }}</td>
            <td>{{ tren.destino || "-" }}</td>
            <td v-if="showNoId">{{ tren.descripcion || "-" }}</td>
            <td v-if="hasPermission">
              <div class="d-flex">
                <button
                  @click="openVagonDetailsModal(tren)"
                  class="btn btn-sm btn-info me-1"
                  :title="showNoId ? 'Ocultar detalles' : 'Ver detalles'"
                >
                  <i
                    :class="
                      showNoId
                        ? 'bi bi-eye-slash-fill text-white'
                        : 'bi bi-eye-fill text-white'
                    "
                  ></i>
                </button>
                <router-link
                  :to="{ name: 'EditarEnTren', params: { id: tren.id } }"
                  class="btn btn-sm btn-warning me-1"
                  title="Editar"
                >
                  <i class="bi bi-pencil-square text-white"></i>
                </router-link>
                <button
                  @click.prevent="confirmDelete(tren.id)"
                  class="btn btn-sm btn-danger"
                  title="Eliminar"
                >
                  <i class="bi bi-trash text-white"></i>
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="!busqueda_existente && en_trenes.length === 0">
            <td colspan="10" class="text-center text-muted py-4">
              <i class="bi bi-exclamation-circle fs-4"></i>
              <p class="mt-2 mb-0">
                No se encontraron resultados para "{{ searchQuery }}"
              </p>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Paginación mejorada -->
    <div class="d-flex justify-content-between align-items-center mt-3">
      <div class="text-muted small">
        Mostrando {{ en_trenes.length }} de {{ totalItems }} registros
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

    <!-- Modal para detalles -->
    <div
      v-if="showDetailsModal"
      class="modal-backdrop"
      @click.self="closeDetailsModal"
    >
      <div class="modal-content">
        <div class="modal-header bg-primary text-white">
          <h5 class="modal-title">Info del vagon</h5>
          <button
            type="button"
            class="btn-close btn-close-white"
            @click="closeDetailsModal"
          >
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-md-6 mb-3">
              <div class="detail-item">
                <span class="detail-label">No Id Locomotora:</span>
                <span class="detail-value">{{
                  currentTren.numero_identificacion_locomotora || "N/A"
                }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Tipo de equipo:</span>
                <span class="detail-value">{{
                  currentTren.tipo_equipo || "N/A"
                }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Estado:</span>
                <span class="detail-value">{{
                  currentTren.estado || "N/A"
                }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Producto Id:</span>
                <span class="detail-value">{{
                  currentTren.producto || "N/A"
                }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Producto nombre:</span>
                <span class="detail-value">{{
                  currentTren.producto_name || "N/A"
                }}</span>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <div class="detail-item">
                <span class="detail-label">Tipo de origen:</span>
                <span class="detail-value">{{
                  currentTren.tipo_origen || "N/A"
                }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Origen:</span>
                <span class="detail-value">{{
                  currentTren.origen || "N/A"
                }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Tipo de destino:</span>
                <span class="detail-value">{{
                  currentTren.tipo_destino || "N/A"
                }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Destino:</span>
                <span class="detail-value">{{
                  currentTren.destino || "N/A"
                }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Equipo de carga:</span>
                <span class="detail-value">{{
                  currentTren.equipo_carga_name || "N/A"
                }}</span>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <div class="detail-item">
                <span class="detail-label">Cantidad de vagones:</span>
                <span class="detail-value">{{
                  currentTren.cantidad_vagones || "0"
                }}</span>
              </div>
            </div>
            <div class="col-md-6">
              <div class="detail-item">
                <span class="detail-label">Descripción:</span>
                <span class="detail-value">{{
                  currentTren.descripcion || "Ninguna"
                }}</span>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-12">
              <div class="detail-item">
                <span class="detail-label">Observaciones:</span>
                <span class="detail-value">{{
                  currentTren.observaciones || "Ninguna"
                }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            @click="closeDetailsModal"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import ModalEnTrenes from "@/components/ModalViewEnTrenes.vue";

export default {
  name: "EnTrenes",
  components: {
    ModalEnTrenes,
  },

  data() {
    return {
      en_trenes: [],
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 0,
      searchQuery: "",
      debounceTimeout: null,
      busqueda_existente: true,
      userPermissions: [],
      userGroups: [],
      showContent: false,
      mostrarModal: false,
      loading: false,
      user_role: "",
      showNoId: false,
      showDetailsModal: false, // <-- Añade esta línea
      currentTren: {}, // <-- Añade esta línea si no está
    };
  },

  async mounted() {
    await this.getTrenes();
    await this.fetchUserPermissionsAndGroups();
  },

  methods: {
    hasPermission() {
      if (this.user_role === "role") {
        return true;
      } else {
        return this.user_role === "admin";
      }
    },

    toggleContentVisibility() {
      this.showNoId = !this.showNoId;
    },

    hasGroup(group) {
      return this.userGroups.some((g) => g.name === group);
    },

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
      this.loading = true;
      try {
        const response = await axios.get("/ufc/en-trenes/", {
          params: {
            page: this.currentPage,
            page_size: this.itemsPerPage,
          },
        });
        this.en_trenes = response.data.results;
        this.totalItems = response.data.count;
      } catch (error) {
        console.error("Error al obtener los trenes:", error);
      } finally {
        this.loading = false;
      }
    },

    async searchTrenes() {
      this.loading = true;
      try {
        const response = await axios.get("/ufc/en-trenes/", {
          params: {
            origen_destino: this.searchQuery,
            page: this.currentPage,
            page_size: this.itemsPerPage,
          },
        });
        this.en_trenes = response.data.results;
        this.totalItems = response.data.count;
        this.busqueda_existente = this.en_trenes.length > 0;
      } catch (error) {
        console.error("Error al buscar trenes", error);
        this.busqueda_existente = false;
      } finally {
        this.loading = false;
      }
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

    nextPage() {
      if (this.currentPage * this.itemsPerPage < this.totalItems) {
        this.currentPage++;
        this.getTrenes();
      }
    },

    goToPage(page) {
      this.currentPage = page;
      this.getTrenes();
    },

    async delete_tren(id) {
      try {
        await axios.delete(`/ufc/en-trenes/${id}/`);
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

    openVagonDetailsModal(tren) {
      this.currentTren = { ...tren };
      this.showDetailsModal = true; // <-- Asegúrate que esta línea está así

      // Opcional: Cargar datos completos del servidor
    },

    closeDetailsModal() {
      this.showDetailsModal = false;
      this.currentTren = {};
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

<style scoped>
/* Estilos generales */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* Botón de agregar */
.btn-primary {
  padding: 8px 16px;
  border-radius: 20px;
}

/* Buscador */
.search-container {
  width: 100%;
  max-width: 400px;
}

.search-container .input-group-text {
  border-radius: 20px 0 0 20px;
  border-right: none;
}

.search-container input {
  border-radius: 0 20px 20px 0;
  border-left: none;
  padding: 8px 15px;
}

/* Tabla */
.table-responsive {
  border-radius: 8px;
  overflow: hidden;
}

.table {
  margin-bottom: 0;
}

.table th {
  font-weight: 600;
  background-color: #f8f9fa;
  padding: 12px 15px;
}

.table td {
  padding: 12px 15px;
  vertical-align: middle;
}

.table-hover tbody tr:hover {
  background-color: rgba(0, 123, 255, 0.05);
}

/* Botones de acción */
.btn-sm {
  padding: 5px 10px;
  border-radius: 4px;
}

.btn-info {
  background-color: #0dcaf0;
  border-color: #0dcaf0;
}

.btn-warning {
  background-color: #ffc107;
  border-color: #ffc107;
}

.btn-danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.btn-info:hover,
.btn-warning:hover,
.btn-danger:hover {
  opacity: 0.9;
}

/* Paginación */
.pagination {
  margin: 0;
}

.page-link {
  padding: 6px 12px;
  border-radius: 4px;
  margin: 0 2px;
}

/* Mensaje de no resultados */
.text-muted {
  color: #6c757d !important;
}

/* Modal personalizado */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  animation: modalFadeIn 0.3s ease-out;
}

.modal-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #dee2e6;
}

.modal-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #dee2e6;
}

/* Detalles en el modal */
.detail-item {
  margin-bottom: 1rem;
}

.detail-label {
  font-weight: 600;
  color: #495057;
  display: inline-block;
  min-width: 140px;
}

.detail-value {
  color: #212529;
}

/* Animación del modal */
@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .d-flex.justify-content-between {
    flex-direction: column;
    gap: 15px;
  }

  .search-container {
    max-width: 100%;
  }

  .btn-primary {
    width: 100%;
    text-align: center;
  }

  .table-responsive {
    overflow-x: auto;
  }

  .table th,
  .table td {
    padding: 8px 10px;
    font-size: 0.9rem;
  }

  .btn-sm {
    padding: 4px 8px;
    font-size: 0.8rem;
  }
}
</style>
