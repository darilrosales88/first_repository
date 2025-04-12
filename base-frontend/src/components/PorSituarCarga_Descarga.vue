<template>
  <div class="container">
    <!-- Fila para el icono y el buscador -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <!-- Icono de agregar -->
      <button class="btn btn-link p-0">
        <router-link to="/AdicionarPorSituar"><i class="bi bi-plus-circle fs-3"></i></router-link>
      </button>

      <!-- Buscador mejorado -->
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
            <th scope="col">Tipo Origen</th>
            <th scope="col">Origen</th>
            <th scope="col">Tipo de equipo</th>
            <th scope="col">Estado</th>
            <th scope="col">Operacion</th>
            <th scope="col">Producto</th>
            <th scope="col">Por Situar</th>
            <th scope="col">Acciones</th>        
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="9" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
            </td>
          </tr>

          <tr v-for="(item, index) in filteredRecords" :key="item.id">
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ item.tipo_origen }}</td>
            <td>{{ item.origen }}</td>
            <td>{{ item.tipo_equipo }}</td>
            <td>{{ item.estado }}</td>
            <td>{{ item.operacion }}</td>
            <td>{{ item.producto_name }}</td>
            <td>{{ item.por_situar }}</td>

            <td>
              <button
                @click="viewDetails(item)"
                class="btn btn-sm btn-info me-2"
                title="Ver detalles"
              >
                <i class="bi bi-eye-fill text-white"></i>
              </button>
              <router-link
                :to="{ name: 'EditarPorSituar', params: { id: item.id || 'default-id' } }"
                class="btn btn-sm btn-warning me-2"
                title="Editar"
              >
                <i class="bi bi-pencil-square text-white"></i>
              </router-link>
              <button
                @click="confirmDelete(item.id)"
                class="btn btn-sm btn-danger"
                title="Eliminar"
                :disabled="loading"
              >
                <i class="bi bi-trash text-white"></i>
              </button>
            </td>
          </tr>

          <tr v-if="!loading && filteredRecords.length === 0">
            <td colspan="9" class="text-center text-muted py-4">
              <i class="bi bi-exclamation-circle fs-4"></i>
              <p class="mt-2 mb-0">
                {{ searchQuery ? `No se encontraron resultados para "${searchQuery}"` : 'No hay registros disponibles' }}
              </p>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal para detalles -->
    <div v-if="showDetailsModal" class="modal-backdrop" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header bg-primary text-white">
          <h5 class="modal-title">Info</h5>
          <button type="button" class="btn-close btn-close-white" @click="closeModal"></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col-md-6 mb-3">
              <div class="detail-item">
                <span class="detail-label">Tipo Origen:</span>
                <span class="detail-value">{{ currentRecord.tipo_origen || 'N/A' }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Origen:</span>
                <span class="detail-value">{{ currentRecord.origen || 'N/A' }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Tipo de Equipo:</span>
                <span class="detail-value">{{ currentRecord.tipo_equipo || 'N/A' }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Estado:</span>
                <span class="detail-value">{{ currentRecord.estado || 'N/A' }}</span>
              </div>
            </div>
            <div class="col-md-6 mb-3">
              <div class="detail-item">
                <span class="detail-label">Operación:</span>
                <span class="detail-value">{{ currentRecord.operacion || 'N/A' }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Producto:</span>
                <span class="detail-value">{{ currentRecord.producto_name || 'N/A' }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Por Situar:</span>
                <span class="detail-value">{{ currentRecord.por_situar || '0' }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Observaciones:</span>
                <span class="detail-value">{{ currentRecord.observaciones || 'Ninguna' }}</span>
              </div>
              <div class="detail-item" v-if="currentRecord.created_at">
                <span class="detail-label">Fecha Creación:</span>
                <span class="detail-value">{{ formatDate(currentRecord.created_at) }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeModal">Cerrar</button>
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
      searchQuery: "",
      registrosPorSituar: [],
      loading: false,
      showDetailsModal: false,
      errorLoading: false,
      currentRecord: {},
      debounceTimeout: null,
    };
  },

  computed: {
    filteredRecords() {
      if (!this.searchQuery) return this.registrosPorSituar;
      
      const query = this.searchQuery.toLowerCase();
      return this.registrosPorSituar.filter(item => {
        // Buscar en todos los campos relevantes
        const fieldsToSearch = [
          item.tipo_origen,
          item.origen,
          item.tipo_equipo,
          item.estado,
          item.operacion,
          item.producto_name,
          item.por_situar?.toString(),
          item.observaciones
        ];
        
        return fieldsToSearch.some(field => 
          field && field.toString().toLowerCase().includes(query)
        );
      });
    }
  },

  mounted() {
    this.getPorSituar();
  },

  methods: {
    async getPorSituar() {
      this.loading = true;
      this.errorLoading = false;
      try {
        const response = await axios.get("http://127.0.0.1:8000/ufc/por-situar/");
        this.allRecords = Array.isArray(response.data) ? response.data : response.data.results || [];
        this.registrosPorSituar = [...this.allRecords];
      } catch (error) {
        console.error("Error al cargar datos:", error);
        this.errorLoading = true;
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'No se pudieron cargar los datos. Por favor, intente nuevamente.',
        });
      } finally {
        this.loading = false;
      }
    },

    async viewDetails(item) {
      this.loading = true;
      try {
        // Usamos los datos que ya tenemos para mostrar inmediatamente
        this.currentRecord = { ...item };
        this.showDetailsModal = true;
        
        // Opcional: Si quieres cargar datos adicionales del servidor
        const response = await axios.get(`http://127.0.0.1:8000/ufc/por-situar/${item.id}/`);
        this.currentRecord = response.data;
      } catch (error) {
        console.error("Error al cargar detalles:", error);
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'No se pudieron cargar los detalles completos del registro.',
        });
      } finally {
        this.loading = false;
      }
    },

    closeModal() {
      this.showDetailsModal = false;
      this.currentRecord = {};
    },

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
          await axios.delete(`http://127.0.0.1:8000/ufc/por-situar/${id}/`);
          Swal.fire("Eliminado", "El registro ha sido eliminado", "success");
          await this.getPorSituar();
        } catch (error) {
          let errorMsg = 'Error al eliminar el registro';
          if (error.response?.status === 404) {
            errorMsg = 'El registro no existe o ya fue eliminado';
          }
          Swal.fire("Error", errorMsg, "error");
        } finally {
          this.loading = false;
        }
      }
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.search_por_situar();
      }, 300);
    },

    search_por_situar() {
      // No es necesario hacer nada aquí ya que filteredRecords es computado
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      };
      return new Date(dateString).toLocaleDateString('es-ES', options);
    }
  }
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
  
  .modal-content {
    width: 95%;
  }
  
  .detail-label {
    min-width: 120px;
    display: block;
    margin-bottom: 0.25rem;
  }
}
</style>