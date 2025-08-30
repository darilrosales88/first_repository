<template>
  <div style="margin-left: 16.5em; width: 79%">
    <div
      style="
        background-color: #002a68;
        color: white;
        text-align: right;
        padding: 10px;
      "
    >
      <h6>Partes combinados</h6>
    </div>

    <Navbar-Component /><br />

    <div class="container py-3">
      <div class="card border">
        <div class="card-header bg-light border-bottom">
          <h6 class="mb-0 text-dark fw-semibold">
            <i class="bi bi-clipboard-data me-2"></i>Registro de partes combinados
          </h6>
        </div>

        <div class="card-body p-3">
          <div class="row mb-3 g-2">
            <div class="col-md-4">
              <div class="form-group">
                <label class="form-label small fw-semibold text-secondary">
                  <i class="bi bi-calendar me-2 text-primary"></i>Fecha inicio
                </label>
                <input
                  type="date"
                  class="form-control form-control-sm border-secondary"
                  v-model="filters.fecha_inicio"
                />
              </div>
            </div>
            <div class="col-md-4">
              <div class="form-group">
                <label class="form-label small fw-semibold text-secondary">
                  <i class="bi bi-calendar me-2 text-primary"></i>Fecha fin
                </label>
                <input
                  type="date"
                  class="form-control form-control-sm border-secondary"
                  v-model="filters.fecha_fin"
                />
              </div>
            </div>
            <div class="col-md-4">
              <div class="form-group">
                <label class="form-label small fw-semibold text-secondary">
                  <i class="bi bi-filter-circle me-2 text-primary"></i>Estado
                </label>
                <select
                  class="form-control form-control-sm border-secondary"
                  v-model="filters.estado"
                >
                  <option value="">Todos</option>
                  <option value="creado">Creado</option>
                  <option value="aprobado">Aprobado</option>
                  <option value="rechazado">Rechazado</option>
                  <option value="listo">Listo</option>
                </select>
              </div>
            </div>
          </div>

          <div class="d-flex justify-content-end gap-2 mt-4">
            <button
              type="button"
              class="btn btn-primary btn-sm"
              @click="fetchPartesCombinados"
              :disabled="loading"
            >
              <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              <i v-else class="bi bi-search me-2"></i>
              {{ loading ? 'Buscando...' : 'Buscar' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="card border mt-4">
      <div class="card-header bg-light border-bottom">
        <h6 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-table me-2"></i>Resultados
        </h6>
      </div>
      <div class="card-body p-3">
        <div class="table-responsive">
          <table class="table table-sm table-bordered table-hover">
            <thead class="table-light">
              <tr>
                <th scope="col">Tipo</th>
                <th scope="col">Fecha</th>
                <th scope="col">Estado</th>
                <th scope="col">Creado por</th>
                <th scope="col">Aprobado por</th>
                <th scope="col">Entidad</th>
                <th scope="col">Organismo</th>
                <th scope="col">Provincia</th>
                <th scope="col">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loadingData">
                <td colspan="9" class="text-center">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Cargando...</span>
                  </div>
                </td>
              </tr>
              <tr v-else-if="partesCombinados.length === 0">
                <td colspan="9" class="text-center text-muted py-4">
                  <i class="bi bi-database-exclamation fs-4"></i>
                  <p class="mt-2">No hay registros para mostrar</p>
                </td>
              </tr>
              <tr v-for="parte in partesCombinados" :key="parte.id">
                <td>{{ getTipoParte(parte.tipo_parte || 'N/A') }}</td>
                <td>{{ formatDateTime(parte.fecha_actual) }}</td>
                <td>
                  <span :class="'status-' + getStatusClass(parte.estado_parte || '')">
                    {{ parte.estado_parte || '-' }}
                  </span>
                </td>
                <td>{{ parte.creado_por_name || 'N/A' }}</td>
                <td>{{ parte.aprobado_por_name || '-' }}</td>
                <td>{{ parte.entidad_name || 'N/A' }}</td>
                <td>{{ parte.organismo_name || 'N/A' }}</td>
                <td>{{ parte.provincia_name || 'N/A' }}</td>
                <td>
                  <div class="d-flex">
                    <button 
                      @click="verDetalle(parte)"
                      class="btn btn-sm btn-outline-primary me-2"
                      title="Ver detalles">
                      <i class="bi bi-eye-fill"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="io-pagination d-flex justify-content-between align-items-center mt-3">
          <div class="text-muted small">
            Mostrando {{ (currentPage - 1) * itemsPerPage + 1 }}-{{ Math.min(currentPage * itemsPerPage, partesCombinados.length) }} de {{ totalRegistros }} registros
          </div>
          <nav aria-label="Page navigation">
            <ul class="pagination pagination-sm mb-0">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <button class="page-link" @click="prevPage">
                  <i class="bi bi-chevron-left"></i>
                </button>
              </li>
              <li class="page-item disabled">
                <span class="page-link">
                  Página {{ currentPage }} de {{ totalPages }}
                </span>
              </li>
              <li class="page-item" :class="{ disabled: currentPage >= totalPages }">
                <button class="page-link" @click="nextPage">
                  <i class="bi bi-chevron-right"></i>
                </button>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "RegistrosPartesCombinadosView",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      partesCombinados: [],
      loading: false,
      loadingData: false,
      error: null,
      filters: {
        fecha_inicio: "",
        fecha_fin: "",
        estado: "",
      },
      currentPage: 1,
      itemsPerPage: 10,
      totalRegistros: 0,
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalRegistros / this.itemsPerPage);
    },
  },
  created() {
    this.fetchPartesCombinados();
  },
  methods: {
    async fetchPartesCombinados() {
      this.loading = true;
      this.loadingData = true;
      this.error = null;

      try {
        const params = {
          page: this.currentPage,
          ...this.filters,
        };

        Object.keys(params).forEach(key => {
          if (params[key] === "") {
            delete params[key];
          }
        });

        const response = await axios.get("/gemar/gemar-partes-combinados/", { params });

        this.partesCombinados = response.data.results || [];
        this.totalRegistros = response.data.count || 0;
      } catch (error) {
        console.error("Error al obtener partes combinados:", error);
        this.error = error.response?.data || "Error al cargar los datos";
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "No se pudieron cargar los partes combinados",
          confirmButtonColor: "#002a68",
        });
      } finally {
        this.loading = false;
        this.loadingData = false;
      }
    },
    
    getTipoParte(tipo) {
      const tipos = {
        'HECHO_EXTRAORDINARIO': 'Hecho Extraordinario',
        'PROGRAMACION_MANIOBRAS': 'Programación Maniobras',
        'PBIP': 'PBIP',
        'EXISTENCIA_MERCANCIA': 'Existencia Mercancía'
      };
      return tipos[tipo] || tipo;
    },
    
    getStatusClass(status) {
      if (!status) return 'default';
      
      const statusStr = typeof status === 'string' ? status : String(status);
      const statusLower = statusStr.toLowerCase();

      if (statusLower.includes('aprobado')) return 'success';
      if (statusLower.includes('pendiente') || statusLower.includes('creado'))
        return 'warning';
      if (statusLower.includes('rechazado') || statusLower.includes('cancelado')) 
        return 'danger';
      if (statusLower.includes('listo')) return 'info';

      return 'default';
    },
    
  formatDateTime(dateTime) {
  if (!dateTime) return '-';
  
  // Asumir que la fecha viene en UTC del backend
  const date = new Date(dateTime + 'Z'); // Agregar 'Z' para indicar UTC
  return date.toLocaleDateString('es-ES', { 
    timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone 
    });
  },
    
     verDetalle(parte) {
    // Redirigir a la vista de detalle específica según el tipo de parte
    if (parte.tipo_parte === 'HECHO_EXTRAORDINARIO') {
        this.$router.push(`/gemar/hechos-extraordinarios/${parte.id}/detalle`);
    } else if (parte.tipo_parte === 'PROGRAMACION_MANIOBRAS') {
        this.$router.push(`/gemar/programacion-maniobras/${parte.id}/detalle`);
    } else if (parte.tipo_parte === 'PBIP') {
        this.$router.push(`/gemar/partes-pbip/${parte.id}/detalle`);
    } else if (parte.tipo_parte === 'EXISTENCIA_MERCANCIA') {
        this.$router.push(`/gemar/existencias-mercancia/${parte.id}/detalle`);
    } else {
        console.error('Tipo de parte no reconocido:', parte.tipo_parte);
    }
},
    
    goToPage(page) {
      if (page !== this.currentPage) {
        this.currentPage = page;
        this.fetchPartesCombinados();
      }
    },
    
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.fetchPartesCombinados();
      }
    },
    
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.fetchPartesCombinados();
      }
    },
  },
};
</script>

<style scoped>
/* Estilos copiados exactamente del segundo código */
.card-header {
  background-color: #f8f9fa;
  border-bottom: 2px solid #e0e0e0 !important;
  padding: 0.75rem 1.25rem;
}

.search-container {
  position: relative;
  width: 100%;
  max-width: 300px;
}

.search-container input {
  padding-left: 2.5rem !important;
  border-radius: 20px !important;
}

.search-container .bi-search {
  color: #6c757d;
  z-index: 10;
}

.input-group {
  width: 100%;
}

.table-responsive {
  overflow-x: auto;
}

.table {
  font-size: 0.875rem;
}

.table thead th {
  background-color: #f8f9fa;
  border-color: #dee2e6;
  color: #495057;
  font-weight: 500;
}

.table tbody tr:hover {
  background-color: #f8f9fa;
}

/* Estilos para los estados */
.status-success {
  background-color: rgba(40, 167, 69, 0.1);
  color: #28a745;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-warning {
  background-color: rgba(255, 193, 7, 0.1);
  color: #ffc107;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-danger {
  background-color: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-info {
  background-color: rgba(23, 162, 184, 0.1);
  color: #17a2b8;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-default {
  background-color: rgba(108, 117, 125, 0.1);
  color: #6c757d;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.menu-options {
  background-color: white;
  border: 1px solid #dee2e6;
  border-radius: 0.25rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  min-width: 200px;
}

.menu-options a {
  display: block;
  padding: 0.5rem 1rem;
  color: #212529;
  text-decoration: none;
}

.menu-options a:hover {
  background-color: #f8f9fa;
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 0.25rem 1rem;
  clear: both;
  font-weight: 400;
  color: #212529;
  text-align: inherit;
  text-decoration: none;
  white-space: nowrap;
  background-color: transparent;
  border: 0;
}

.dropdown-item:hover {
  color: #16181b;
  background-color: #f8f9fa;
}

.selected-part-container {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #dee2e6;
  border-radius: 0.25rem;
  background-color: #f8f9fa;
}

/* Estilos para la paginación */
.io-pagination {
  padding: 0.75rem 1.25rem;
  background-color: #f8f9fa;
  border-top: 1px solid #dee2e6;
  border-radius: 0 0 0.25rem 0.25rem;
}

.page-link {
  min-width: 32px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-item.active .page-link {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.page-link {
  color: #0d6efd;
  text-decoration: none;
}

.page-item.disabled .page-link {
  color: #6c757d;
  pointer-events: none;
  height: 30px;
}

.page-item:not(.disabled):not(.active) .page-link:hover {
  background-color: #e9ecef;
  color: #0a58ca;
}

.page-item .page-link i {
  font-size: 0.9rem;
}

/* Estilos para el mensaje de no resultados */
.text-muted {
  color: #6c757d !important;
}

.bi-database-exclamation {
  color: #adb5bd;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

/* Modal de confirmación */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.modal {
  background: white;
  border-radius: 0.5rem;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.modal-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h5 {
  margin: 0;
  font-size: 1.25rem;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6c757d;
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #dee2e6;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

/* Estilos adicionales para mantener consistencia */
.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
  border-radius: 0.2rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.btn:hover {
  transform: translateY(-1px);
  opacity: 0.9;
}

.btn i {
  font-size: 1rem;
}

.form-control {
  font-size: 0.875rem;
}

.form-label {
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.bi {
  vertical-align: middle;
}
</style>