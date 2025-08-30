<template>
  <div>
    <div class="card border" style="margin-left: 15.8em; width: 79%">
      <!-- Header azul con título -->
      <div
        style="
          background-color: #002a68;
          color: white;
          text-align: right;
          padding: 10px;
        "
      >
        <h6>Parte de programación de maniobras</h6>
      </div>

      <Navbar-Component />
      
      <div class="card-header bg-light border-bottom d-flex justify-content-between align-items-center">
        <h6 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-clipboard-data me-2"></i>Detalle del Parte - Programación de Maniobras
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
                  <p class="mb-0 fw-semibold">Programación de Maniobras</p>
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

          <!-- Tabla de información específica de Programación de Maniobras -->
          <div class="table-section">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h6 class="text-dark fw-semibold mb-0">
                Detalles de la Programación de Maniobras
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

          <!-- Componente de programación de maniobras (tablas de datos) -->
          <div v-if="parte.estado_parte !== 'creado'" class="row mb-4">
            <div class="col-md-12">
              <programacion_maniobra 
                :estado-parte="parte.estado_parte || ''"
                @estado-cambiado="handleEstadoCambiado"
                :key="componentKey"
              />
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
import programacion_maniobra from "@/components/GEMAR/programacion_maniobra.vue";

export default {
  name: "DetalleProgramacionManiobras",
  components: {
    NavbarComponent,
    programacion_maniobra,
  },
  data() {
    return {
      parte: null,
      loading: false,
      loadingAccion: false,
      error: '',
      userGroups: [],
      userPermissions: [],
      componentKey: 0
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
        const response = await axios.get(`/gemar/gemar-partes-programacion-maniobras/${this.$route.params.id}/`);
        this.parte = response.data;
      } catch (error) {
        console.error('Error al cargar detalle de programación de maniobras:', error);
        this.error = 'No se pudo cargar el detalle del parte de programación de maniobras';
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
        name: 'Editar-Programacion-Maniobras',
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
          await axios.delete(`/gemar/gemar-partes-programacion-maniobras/${this.parte.id}/`);
          this.showSuccessToast("Parte eliminado correctamente");
          this.$router.go(-1);
        }
      } catch (error) {
        console.error("Error al eliminar parte de programación de maniobras:", error);
        this.showErrorToast("Error al eliminar el parte de programación de maniobras");
      } finally {
        this.loadingAccion = false;
      }
    },

    async aprobarParte() {
      try {
        const result = await Swal.fire({
          title: "¿Estás seguro?",
          text: "¿Está seguro que desea aprobar este parte de programación de maniobras?",
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
            `/gemar/gemar-partes-programacion-maniobras/${this.parte.id}/`,
            { estado_parte: 'Aprobado' }
          );
          this.showSuccessToast("Parte aprobado correctamente");
          await this.cargarDetalle();
          this.componentKey += 1; // Forzar recarga del componente hijo
        }
      } catch (error) {
        console.error("Error al aprobar parte de programación de maniobras:", error);
        this.showErrorToast("Error al aprobar el parte de programación de maniobras");
      } finally {
        this.loadingAccion = false;
      }
    },

    async rechazarParte() {
      try {
        const result = await Swal.fire({
          title: "¿Estás seguro?",
          text: "¿Está seguro que desea rechazar este parte de programación de maniobras?",
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
            `/gemar/gemar-partes-programacion-maniobras/${this.parte.id}/`,
            { estado_parte: 'Rechazado' }
          );
          this.showSuccessToast("Parte rechazado correctamente");
          await this.cargarDetalle();
          this.componentKey += 1; // Forzar recarga del componente hijo
        }
      } catch (error) {
        console.error("Error al rechazar parte de programación de maniobras:", error);
        this.showErrorToast("Error al rechazar el parte de programación de maniobras");
      } finally {
        this.loadingAccion = false;
      }
    },

    async marcarListo() {
      try {
        const result = await Swal.fire({
          title: "¿Estás seguro?",
          text: "¿Está seguro que desea marcar este parte de programación de maniobras como 'Listo'?",
          icon: "question",
          showCancelButton: true,
          confirmButtonColor: "#002a68",
          cancelButtonColor: "#d33",
          confirmButtonText: "Sí, marcar como listo",
          cancelButtonText: "Cancelar",
        });

        if (result.isConfirmed) {
          this.loadingAccion = true;
          await axios.post(`/gemar/gemar-partes-programacion-maniobras/${this.parte.id}/listo/`);
          this.showSuccessToast("Parte marcado como listo correctamente");
          await this.cargarDetalle();
          this.componentKey += 1; // Forzar recarga del componente hijo
        }
      } catch (error) {
        console.error("Error al marcar parte como listo:", error);
        this.showErrorToast("Error al marcar el parte como listo");
      } finally {
        this.loadingAccion = false;
      }
    },

    handleEstadoCambiado(nuevoEstado) {
      if (this.parte) {
        this.parte.estado_parte = nuevoEstado;
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