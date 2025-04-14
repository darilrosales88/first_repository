<template>
  <div class="container">
    <!-- Fila para el icono y el buscador -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <!-- Icono de agregar -->
      <button class="btn btn-link p-0">
        <router-link to="/AdicionarSituados"
          ><i class="bi bi-plus-circle fs-3"></i
        ></router-link>

        <!-- Icono grande -->
      </button>

      <!-- Buscador -->
      <form @submit.prevent="search_por_situar" class="search-container">
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

    <!-- Tabla -->
    <div class="table-responsive rounded-3 shadow-sm">
      <table class="table table-hover mb-0">
        <thead class="table-light">
          <tr>
            <th scope="col">#</th>
            <th scope="col">Tipo de origen</th>
            <th scope="col">Origen</th>
            <th scope="col">Tipo de equipo</th>
            <th scope="col">Estado</th>
            <th scope="col">Operacion</th>
            <th scope="col">Producto</th>
            <th scope="col">Situados</th>
            <th scope="col">Pendientes por situar</th>
            <th scope="col">Acciones</th>
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

          <tr v-for="(item, index) in registrosPorSituar" :key="item.id">
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ item.tipo_origen }}</td>
            <td>{{ item.origen }}</td>
            <td>{{ item.tipo_equipo }}</td>
            <td>{{ item.estado }}</td>
            <td>{{ item.operacion }}</td>
            <td>{{ item.producto_name }}</td>
            <td>{{ item.situados }}</td>
            <td>{{ item.pendiente_proximo_dia }}</td>
            <td style="display: flex">
              <button
                class="btn btn-sm btn-info me-1"
                @click="showDetails(item)"
                title="Ver detalles"
              >
                <i class="bi bi-eye-fill text-white"></i>
              </button>
              <router-link
                :to="{ name: 'EditarSituados', params: { id: item.id } }"
                class="btn btn-sm btn-warning me-1"
                title="Editar"
              >
                <i class="bi bi-pencil-square text-white"></i>
              </router-link>
              <button
                class="btn btn-sm btn-danger"
                @click="confirmDelete(item.id)"
                :disabled="loading"
                title="Eliminar"
              >
                <i class="bi bi-trash text-white"></i>
              </button>
            </td>
          </tr>
          <tr v-if="!busqueda_existente && registrosPorSituar.length === 0">
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

    <!-- Paginación -->
    <div class="d-flex justify-content-between align-items-center mt-3">
      <div class="text-muted small">
        Mostrando {{ registrosPorSituar.length }} de {{ totalItems }} registros
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

    <!-- Modal para visualizar detalles -->
    <div v-if="showModal" class="modal-backdrop" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header bg-primary text-white">
          <h5 class="modal-title">Info</h5>
          <button
            type="button"
            class="btn-close btn-close-white"
            @click="closeModal"
          ></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-md-6 mb-3">
              <div class="detail-item">
                <span class="detail-label">Tipo de origen:</span>
                <span class="detail-value">{{
                  selectedItem.tipo_origen || "N/A"
                }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Origen:</span>
                <span class="detail-value">{{
                  selectedItem.origen || "N/A"
                }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Tipo de equipo:</span>
                <span class="detail-value">{{
                  selectedItem.tipo_equipo || "N/A"
                }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Estado:</span>
                <span class="detail-value">{{
                  selectedItem.estado || "N/A"
                }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Operación:</span>
                <span class="detail-value">{{
                  selectedItem.operacion || "N/A"
                }}</span>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <div class="detail-item">
                <span class="detail-label">Producto:</span>
                <span class="detail-value">{{
                  selectedItem.producto_name || "N/A"
                }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Situados:</span>
                <span class="detail-value">{{
                  selectedItem.situados || "0"
                }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Pendientes por situar:</span>
                <span class="detail-value">{{
                  selectedItem.pendiente_proximo_dia || "0"
                }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Observaciones:</span>
                <span class="detail-value">{{
                  selectedItem.observaciones || "Ninguna"
                }}</span>
              </div>
              <div class="detail-item" v-if="selectedItem.created_at">
                <span class="detail-label">Fecha de creación:</span>
                <span class="detail-value">{{
                  formatDate(selectedItem.created_at)
                }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeModal">
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";

export default {
  data() {
    return {
      allRecords: [],
      debounceTimeout: null,
      searchQuery: "",
      registrosPorSituar: [],
      loading: false,
      busqueda_existente: true,
      showModal: false,
      selectedItem: {},
      totalItems: 0,
      currentPage: 1,
      itemsPerPage: 10,
    };
  },

  mounted() {
    this.getPorSituar();
  },

  methods: {
    async getPorSituar() {
      this.loading = true;
      try {
        const response = await axios.get("http://127.0.0.1:8000/ufc/situados/");
        this.totalItems = response.data.count;
        if (
          response.data &&
          Array.isArray(response.data.results || response.data)
        ) {
          const data = response.data.results || response.data;
          this.allRecords = data.map((item) => ({
            id: item.id,
            tipo_origen: item.tipo_origen || "",
            origen: item.origen || "",
            tipo_equipo: item.tipo_equipo || "",
            estado: item.estado || "",
            operacion: item.operacion || "",
            producto_name: item.producto_name || "",
            situados: item.situados || 0,
            pendiente_proximo_dia: item.pendiente_proximo_dia || 0,
            observaciones: item.observaciones || "",
            created_at: item.created_at || null,
          }));

          this.registrosPorSituar = [...this.allRecords];
          this.busqueda_existente = true;
        }
      } catch (error) {
        this.handleApiError(error, "cargar registros");
        this.registrosPorSituar = [];
      } finally {
        this.loading = false;
      }
    },

    async showDetails(item) {
      try {
        this.loading = true;
        // Mostrar datos básicos inmediatamente
        this.selectedItem = { ...item };
        this.showModal = true;

        // Obtener datos completos del servidor
        const response = await axios.get(
          `http://127.0.0.1:8000/ufc/situados/${item.id}/`
        );
        this.selectedItem = response.data;
      } catch (error) {
        console.error("Error al cargar detalles:", error);
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "No se pudieron cargar los detalles completos del registro.",
        });
      } finally {
        this.loading = false;
      }
    },

    closeModal() {
      this.showModal = false;
      this.selectedItem = {};
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        if (!this.searchQuery.trim()) {
          this.registrosPorSituar = [...this.allRecords];
          this.busqueda_existente = true;
          return;
        }

        const query = this.searchQuery.toLowerCase();
        this.registrosPorSituar = this.allRecords.filter((item) => {
          const fieldsToSearch = [
            item.tipo_origen,
            item.origen,
            item.tipo_equipo,
            item.estado,
            item.operacion,
            item.producto_name,
            item.situados?.toString(),
            item.pendiente_proximo_dia?.toString(),
            item.observaciones,
          ];

          return fieldsToSearch.some(
            (field) => field && field.toString().toLowerCase().includes(query)
          );
        });

        this.busqueda_existente = this.registrosPorSituar.length > 0;
      }, 300);
    },

    // Agregar nuevo registro

    // Confirmar eliminación
    async confirmDelete(id) {
      const result = await Swal.fire({
        title: "¿Estás seguro?",
        text: "¡No podrás revertir esta acción!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
      });

      if (result.isConfirmed) {
        try {
          this.loading = true;
          await axios.delete(`http://127.0.0.1:8000/ufc/situados/${id}/`);
          Swal.fire("Eliminado", "El registro ha sido eliminado", "success");
          await this.getPorSituar();
        } catch (error) {
          this.handleApiError(error, "eliminar registro");
        } finally {
          this.loading = false;
        }
      }
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

    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.getPorSituar();
      }
    },

    nextPage() {
      if (this.currentPage * this.itemsPerPage < this.totalItems) {
        this.currentPage++;
        this.getPorSituar();
      }
    },

    formatDate(dateString) {
      if (!dateString) return "N/A";
      const options = {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      };
      return new Date(dateString).toLocaleDateString("es-ES", options);
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
  max-width: 350px;
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

/* Modal */
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
  min-width: 180px;
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

/* Paginación */
.pagination {
  margin: 0;
}

.page-link {
  padding: 6px 12px;
  border-radius: 4px;
  margin: 0 2px;
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

  .detail-label {
    min-width: 150px;
    display: block;
    margin-bottom: 0.25rem;
  }
}
</style>
