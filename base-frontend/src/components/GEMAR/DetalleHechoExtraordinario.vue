<template>
  <div>
    <div class="card border" style="margin-left: 15.8em; width: 79%">
      <Navbar-Component />
      <div class="card-header bg-light border-bottom d-flex justify-content-between align-items-center">
        <h6 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-clipboard-data me-2"></i>Detalle del Parte - Hecho Extraordinario
        </h6>
        <button class="btn btn-sm btn-outline-secondary" @click="volver">
          <i class="bi bi-arrow-left me-1"></i> Volver
        </button>
      </div>

      <div class="card-body p-3">
        <!-- Loading state -->
        <div v-if="loading" class="text-center">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Cargando...</span>
          </div>
          <p class="mt-2 text-muted">Cargando información del parte...</p>
        </div>

        <!-- Error state -->
        <div v-else-if="error" class="text-center text-danger">
          <i class="bi bi-exclamation-triangle fs-4"></i>
          <p class="mt-2">{{ error }}</p>
          <button @click="cargarDetalle" class="btn btn-sm btn-outline-primary mt-2">
            <i class="bi bi-arrow-clockwise me-1"></i> Reintentar
          </button>
        </div>

        <!-- Success state -->
        <div v-else-if="parte">
          <!-- Información básica del parte -->
          <div class="row mb-4">
            <div class="col-md-4">
              <div class="card bg-light">
                <div class="card-body py-2">
                  <small class="text-muted">Tipo</small>
                  <p class="mb-0 fw-semibold">Hecho Extraordinario</p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card bg-light">
                <div class="card-body py-2">
                  <small class="text-muted">Fecha</small>
                  <p class="mb-0">{{ formatDateTime(parte.fecha_actual || parte.fecha_creacion) }}</p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card bg-light">
                <div class="card-body py-2">
                  <small class="text-muted">Estado</small>
                  <p class="mb-0">
                    <span :class="'status-' + getStatusClass(parte.estado_parte || parte.estado || parte.estado_registro)">
                      {{ parte.estado_parte || parte.estado || parte.estado_registro || 'N/A' }}
                    </span>
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Información del usuario -->
          <div class="row mb-4">
            <div class="col-md-6">
              <div class="card">
                <div class="card-body py-2">
                  <small class="text-muted">Creado por</small>
                  <p class="mb-0">{{ parte.creado_por_name || parte.creado_por?.username || 'N/A' }}</p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card">
                <div class="card-body py-2">
                  <small class="text-muted">Aprobado por</small>
                  <p class="mb-0">{{ parte.aprobado_por_name || parte.aprobado_por?.username || '-' }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Información de la fecha de operación -->
          <div class="row mb-4">
            <div class="col-md-6">
              <div class="card">
                <div class="card-body py-2">
                  <small class="text-muted">Fecha de operación</small>
                  <p class="mb-0">{{ formatDate(parte.fecha_operacion) }}</p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card">
                <div class="card-body py-2">
                  <small class="text-muted">Fecha de creación</small>
                  <p class="mb-0">{{ formatDateTime(parte.fecha_creacion) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Tabla de información específica de Hechos Extraordinarios -->
          <div class="table-section">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h6 class="text-dark fw-semibold mb-0">
                Detalles del Hecho Extraordinario
              </h6>
            </div>

            <div class="table-responsive">
              <table class="table table-sm table-bordered table-hover">
                <thead class="table-light">
                  <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Fecha Operación</th>
                    <th scope="col">Fecha Creación</th>
                    <th scope="col">Estado</th>
                    <th scope="col">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>{{ parte.id || 'N/A' }}</td>
                    <td>{{ formatDate(parte.fecha_operacion) }}</td>
                    <td>{{ formatDateTime(parte.fecha_creacion) }}</td>
                    <td>
                      <span :class="'status-' + getStatusClass(parte.estado_parte || parte.estado || parte.estado_registro)">
                        {{ parte.estado_parte || parte.estado || parte.estado_registro || 'N/A' }}
                      </span>
                    </td>
                    <td>
                      <div class="d-flex gap-1">
                        <button
                          @click="editarParte"
                          class="btn btn-sm btn-outline-primary"
                          :disabled="!puedeEditar"
                        >
                          <i class="bi bi-pencil"></i>
                        </button>
                        <button
                          @click="eliminarParte"
                          class="btn btn-sm btn-outline-danger"
                          :disabled="!puedeEliminar"
                        >
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Información de paginación (solo muestra 1 registro) -->
            <div class="io-pagination d-flex justify-content-between align-items-center mt-3">
              <div class="text-muted small">
                Mostrando 1 registro
              </div>
              <nav aria-label="Page navigation">
                <ul class="pagination pagination-sm mb-0">
                  <li class="page-item disabled">
                    <button class="page-link">
                      <i class="bi bi-chevron-left"></i>
                    </button>
                  </li>
                  <li class="page-item disabled">
                    <span class="page-link"> Página 1 de 1 </span>
                  </li>
                  <li class="page-item">
                    <button class="page-link">
                      <i class="bi bi-chevron-right"></i>
                    </button>
                  </li>
                </ul>
              </nav>
            </div>
          </div>

          <!-- Botones de acción adicionales -->
          <div class="d-flex justify-content-center gap-2 mt-4" v-if="mostrarBotonesAccion">
            <!-- Aprobar - Para RevisorGEMAR -->
            <button v-if="puedeAprobar" 
                    @click="aprobarParte" 
                    class="btn btn-sm btn-outline-success"
                    :disabled="loadingAccion">
              <i class="bi bi-check-circle me-1"></i> 
              {{ loadingAccion ? 'Procesando...' : 'Aprobar' }}
            </button>

            <!-- Rechazar - Para RevisorGEMAR -->
            <button v-if="puedeRechazar" 
                    @click="rechazarParte" 
                    class="btn btn-sm btn-outline-warning"
                    :disabled="loadingAccion">
              <i class="bi bi-x-circle me-1"></i> 
              {{ loadingAccion ? 'Procesando...' : 'Rechazar' }}
            </button>

            <!-- Marcar como Listo - Para AdminGEMAR -->
            <button v-if="puedeMarcarListo" 
                    @click="marcarListo" 
                    class="btn btn-sm btn-outline-info"
                    :disabled="loadingAccion">
              <i class="bi bi-check-all me-1"></i> 
              {{ loadingAccion ? 'Procesando...' : 'Listo' }}
            </button>
          </div>

          <!-- Mensaje si no hay botones disponibles -->
          <div v-else class="text-center text-muted mt-4">
            <i class="bi bi-info-circle"></i>
            <p class="mb-0">No hay acciones disponibles para este estado</p>
          </div>
        </div>

        <!-- No data state -->
        <div v-else class="text-center text-muted">
          <i class="bi bi-database-exclamation fs-4"></i>
          <p class="mt-2">No se encontró información del parte</p>
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
  name: "DetalleHechoExtraordinario",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      parte: null,
      loading: false,
      loadingAccion: false,
      error: '',
      userGroups: [],
      userPermissions: []
    };
  },
  async created() {
    await this.fetchUserPermissionsAndGroups();
    await this.cargarDetalle();
  },
  computed: {
    estadoActual() {
      return this.parte?.estado_parte || this.parte?.estado || this.parte?.estado_registro || '';
    },
    
    puedeEditar() {
      return ['creado', 'pendiente'].includes(this.estadoActual.toLowerCase()) && 
             this.hasGroup('AdminGEMAR') &&
             !this.loadingAccion;
    },
    
    puedeEliminar() {
      return ['creado', 'pendiente'].includes(this.estadoActual.toLowerCase()) && 
             this.hasGroup('AdminGEMAR') &&
             !this.loadingAccion;
    },
    
    puedeAprobar() {
      return ['creado', 'pendiente', 'listo'].includes(this.estadoActual.toLowerCase()) && 
             this.hasGroup('RevisorGEMAR') &&
             !this.loadingAccion;
    },
    
    puedeRechazar() {
      return ['creado', 'pendiente', 'listo', 'aprobado'].includes(this.estadoActual.toLowerCase()) && 
             this.hasGroup('RevisorGEMAR') &&
             !this.loadingAccion;
    },
    
    puedeMarcarListo() {
      return ['creado', 'pendiente'].includes(this.estadoActual.toLowerCase()) && 
             this.hasGroup('AdminGEMAR') &&
             !this.loadingAccion;
    },
    
    mostrarBotonesAccion() {
      return this.parte && !this.loading && 
             (this.puedeAprobar || this.puedeRechazar || this.puedeMarcarListo);
    }
  },
  methods: {
    async cargarDetalle() {
      this.loading = true;
      this.error = '';
      try {
        const response = await axios.get(`/gemar/gemar-partes-hechos-extraordinarios/${this.$route.params.id}/`);
        this.parte = response.data;
      } catch (error) {
        console.error('Error al cargar detalle de hecho extraordinario:', error);
        this.error = 'No se pudo cargar el detalle del parte de hecho extraordinario';
        this.showErrorToast(this.error);
      } finally {
        this.loading = false;
      }
    },

    async fetchUserPermissionsAndGroups() {
      try {
        const userId = localStorage.getItem("userid");
        if (userId) {
          const response = await axios.get(
            `/apiAdmin/user/${userId}/permissions-and-groups/`
          );
          
          this.userPermissions = response.data?.permissions || [];
          this.userGroups = response.data?.groups || [];
        }
      } catch (error) {
        console.error("Error al obtener permisos:", error);
        this.userPermissions = [];
        this.userGroups = [];
      }
    },

    hasGroup(groupName) {
      return this.userGroups.some(group => group.name === groupName);
    },

    getStatusClass(status) {
      if (!status) return 'default';
      
      const statusLower = status.toLowerCase();
      if (statusLower.includes('aprobado')) return 'success';
      if (statusLower.includes('pendiente') || statusLower.includes('creado')) return 'warning';
      if (statusLower.includes('rechazado') || statusLower.includes('cancelado')) return 'danger';
      if (statusLower.includes('listo')) return 'info';
      return 'default';
    },

    formatDateTime(dateTime) {
      if (!dateTime) return '-';
      try {
        const date = new Date(dateTime);
        if (isNaN(date.getTime())) return '-';
        
        return date.toLocaleDateString('es-ES', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        });
      } catch (error) {
        return '-';
      }
    },

    formatDate(dateString) {
      if (!dateString) return '-';
      try {
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return '-';
        
        return date.toLocaleDateString('es-ES', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        });
      } catch (error) {
        return '-';
      }
    },

    volver() {
      this.$router.go(-1);
    },

    async editarParte() {
      this.$router.push({
        name: 'Editar-Hechos-Extraordinarios',
        params: { id: this.parte.id }
      });
    },

    async eliminarParte() {
      try {
        const confirmacion = await Swal.fire({
          title: "¿Estás seguro?",
          text: "Esta acción no se puede deshacer",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#d33",
          cancelButtonColor: "#3085d6",
          confirmButtonText: "Sí, eliminar",
          cancelButtonText: "Cancelar",
        });

        if (confirmacion.isConfirmed) {
          this.loadingAccion = true;
          await axios.delete(`/gemar/gemar-partes-hechos-extraordinarios/${this.parte.id}/`);
          this.showSuccessToast("Parte eliminado correctamente");
          this.$router.go(-1);
        }
      } catch (error) {
        console.error("Error al eliminar parte de hecho extraordinario:", error);
        this.showErrorToast("Error al eliminar el parte de hecho extraordinario");
      } finally {
        this.loadingAccion = false;
      }
    },

    async aprobarParte() {
      try {
        const result = await Swal.fire({
          title: "¿Estás seguro?",
          text: "¿Está seguro que desea aprobar este parte de hecho extraordinario?",
          icon: "question",
          showCancelButton: true,
          confirmButtonColor: "#002a68",
          cancelButtonColor: "#d33",
          confirmButtonText: "Sí, aprobar",
          cancelButtonText: "Cancelar",
        });

        if (result.isConfirmed) {
          this.loadingAccion = true;
          await axios.patch(
            `/gemar/gemar-partes-hechos-extraordinarios/${this.parte.id}/`,
            { estado_parte: 'Aprobado' }
          );
          this.showSuccessToast("Parte aprobado correctamente");
          await this.cargarDetalle();
        }
      } catch (error) {
        console.error("Error al aprobar parte de hecho extraordinario:", error);
        this.showErrorToast("Error al aprobar el parte de hecho extraordinario");
      } finally {
        this.loadingAccion = false;
      }
    },

    async rechazarParte() {
      try {
        const result = await Swal.fire({
          title: "¿Estás seguro?",
          text: "¿Está seguro que desea rechazar este parte de hecho extraordinario?",
          icon: "question",
          showCancelButton: true,
          confirmButtonColor: "#002a68",
          cancelButtonColor: "#d33",
          confirmButtonText: "Sí, rechazar",
          cancelButtonText: "Cancelar",
        });

        if (result.isConfirmed) {
          this.loadingAccion = true;
          await axios.patch(
            `/gemar/gemar-partes-hechos-extraordinarios/${this.parte.id}/`,
            { estado_parte: 'Rechazado' }
          );
          this.showSuccessToast("Parte rechazado correctamente");
          await this.cargarDetalle();
        }
      } catch (error) {
        console.error("Error al rechazar parte de hecho extraordinario:", error);
        this.showErrorToast("Error al rechazar el parte de hecho extraordinario");
      } finally {
        this.loadingAccion = false;
      }
    },

    async marcarListo() {
      try {
        const result = await Swal.fire({
          title: "¿Estás seguro?",
          text: "¿Está seguro que desea marcar este parte de hecho extraordinario como 'Listo'?",
          icon: "question",
          showCancelButton: true,
          confirmButtonColor: "#002a68",
          cancelButtonColor: "#d33",
          confirmButtonText: "Sí, marcar como listo",
          cancelButtonText: "Cancelar",
        });

        if (result.isConfirmed) {
          this.loadingAccion = true;
          await axios.post(`/gemar/gemar-partes-hechos-extraordinarios/${this.parte.id}/listo/`);
          this.showSuccessToast("Parte marcado como listo correctamente");
          await this.cargarDetalle();
        }
      } catch (error) {
        console.error("Error al marcar parte como listo:", error);
        this.showErrorToast("Error al marcar el parte como listo");
      } finally {
        this.loadingAccion = false;
      }
    },

    showErrorToast(message) {
      const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 4000,
        timerProgressBar: true,
        background: "#ff4444",
        color: "#fff",
        iconColor: "#fff",
        didOpen: (toast) => {
          toast.addEventListener("mouseenter", Swal.stopTimer);
          toast.addEventListener("mouseleave", Swal.resumeTimer);
        },
      });

      Toast.fire({
        icon: "error",
        title: message,
      });
    },

    showSuccessToast(message) {
      const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 4000,
        timerProgressBar: true,
        background: "#00C851",
        color: "#fff",
        iconColor: "#fff",
        didOpen: (toast) => {
          toast.addEventListener("mouseenter", Swal.stopTimer);
          toast.addEventListener("mouseleave", Swal.resumeTimer);
        },
      });

      Toast.fire({
        icon: "success",
        title: message,
      });
    }
  }
};
</script>

<style scoped>
/* Los estilos son los mismos que en el componente DetallePBIP */
.card {
  border-radius: 0.25rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 2px solid #e0e0e0 !important;
  padding: 0.75rem 1.25rem;
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

/* Estilos para estados */
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

/* Estilos para botones */
.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  color: white;
}

.btn-outline-success {
  color: #28a745;
  border-color: #28a745;
}

.btn-outline-success:hover {
  background-color: #28a745;
  color: white;
}

.btn-outline-primary {
  color: #0d6efd;
  border-color: #0d6efd;
}

.btn-outline-primary:hover {
  background-color: #0d6efd;
  color: white;
}

.btn-outline-secondary {
  color: #6c757d;
  border-color: #6c757d;
}

.btn-outline-secondary:hover {
  background-color: #6c757d;
  color: white;
}

.btn-outline-warning {
  color: #ffc107;
  border-color: #ffc107;
}

.btn-outline-warning:hover {
  background-color: #ffc107;
  color: #000;
}

.btn-outline-info {
  color: #17a2b8;
  border-color: #17a2b8;
}

.btn-outline-info:hover {
  background-color: #17a2b8;
  color: white;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsividad */
@media (max-width: 768px) {
  .d-flex.justify-content-center.gap-2 {
    flex-wrap: wrap;
    gap: 0.5rem !important;
  }
  
  .btn {
    min-width: auto;
    flex: 1;
  }
}
</style>