<template>
  <div>
    <div class="card border" style="margin-left: 15.8em; width: 79%">
      <Navbar-Component />
      <div class="card-header bg-light border-bottom">
        <h6 class="mb-0 text-dark fw-semibold">
          Sistema de Partes Controlados
        </h6>
        <button
          class="btn btn-sm btn-outline-secondary"
          style="margin-top: 10px"
          @click="$router.push({ name: 'GEMAR' })"
        >
          <i class="bi bi-arrow-left me-1"></i> Volver a GEMAR
        </button>
      </div>
      <div class="card-body p-3">
        <!-- Formulario de PBIP -->
        <div class="form-section mb-4">
          <h6 class="text-dark fw-semibold mb-3">Parte de PBIP</h6>

          <div class="row mb-3">
            <div class="col-md-6">
              <div class="row align-items-center">
                <label class="col-sm-4 col-form-label">Fecha operación:</label>
                <div class="col-sm-8">
                  <input
                    type="date"
                    v-model="fechaOperacion"
                    class="form-control form-control-sm"
                    required
                  />
                </div>
              </div>
            </div>

            <div class="col-md-6">
              <div class="row align-items-center">
                <label class="col-sm-4 col-form-label">Fecha actual:</label>
                <div class="col-sm-8">
                  <input
                    type="datetime-local"
                    v-model="fechaActual"
                    class="form-control form-control-sm"
                    readonly
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tabla de Protección de Buques -->
        <div class="table-section">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h6 class="text-dark fw-semibold mb-0">
              Protección de Buques en Instalaciones Portuarias
            </h6>
            <button @click="addBuque" class="btn btn-sm btn-primary">
              <i class="bi bi-plus-circle me-1"></i> Agregar Buque
            </button>
          </div>

          <div class="table-responsive">
            <table class="table table-sm table-bordered table-hover">
              <thead class="table-light">
                <tr>
                  <th scope="col">No.</th>
                  <th scope="col">Buque</th>
                  <th scope="col">Puerto de Arribo</th>
                  <th scope="col">Fecha de Creación</th>
                  <th scope="col">Nivel</th>
                  <th scope="col">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in partesPBIP" :key="item.id">
                  <td>{{ index + 1 }}</td>
                  <td>
                    {{ item.buque.nombre_embarcacion || item.buque.nombre }}
                  </td>
                  <td>{{ item.puerto.nombre_puerto || item.puerto.nombre }}</td>
                  <td>{{ formatDate(item.fecha_creacion) }}</td>
                  <td>Nivel {{ item.nivel }}</td>
                  <td>
                    <div class="d-flex gap-1">
                      <button
                        @click="editarPartePBIP(item)"
                        class="btn btn-sm btn-outline-primary"
                      >
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button
                        @click="eliminarPartePBIP(item.id)"
                        class="btn btn-sm btn-outline-danger"
                      >
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Paginación -->
          <div
            class="io-pagination d-flex justify-content-between align-items-center mt-3"
          >
            <div class="text-muted small">
              Mostrando {{ partesPBIP.length }} registros
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
      </div>
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "PartesPBIPView",
  components: {
    NavbarComponent,
  },
  data() {
    const now = new Date();
    const offset = now.getTimezoneOffset() * 60000;
    const localISOTime = new Date(now - offset).toISOString().split("T")[0];
    
    return {
      // Datos para gestión de partes
      informeParteId: null,
      isExistingRecord: false,
      existingRecordData: null,
      checkingExisting: true,
      
      // Datos del formulario
      formData: {
        fecha_actual: localISOTime,
        fecha_operacion: localISOTime,
      },
      
      // Listas y datos
      partesPBIP: [],
      listaBuques: [],
      listaPuertos: [],
      
      // Estados
      loading: false,
      error: null,
      success: false,
      fechaOperacion: localISOTime,
      fechaActual: new Date().toISOString().slice(0, 16),
    };
  },

  async created() {
    await this.cargarDatosIniciales();
  },

  methods: {
    // Método para agregar buque - NUEVO MÉTODO
    addBuque() {
      this.$router.push({ name: 'AgregarBuque' });
    },
    
    // Métodos de verificación y carga inicial
    async verificarPartesExistentes() {
      this.checkingExisting = true;
      try {
        const today = new Date();
        const fechaFormateada = `${today.getFullYear()}-${String(
          today.getMonth() + 1
        ).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;

        const response = await axios.get("/api/gemar/registros-pbip/", {
          params: { fecha_actual: fechaFormateada },
        });

        if (response.data.existe) {
          this.informeParteId = response.data.id;
          this.isExistingRecord = true;
          this.existingRecordData = response.data;
          return true;
        } else {
          this.informeParteId = null;
          this.isExistingRecord = false;
          this.existingRecordData = null;
        }
        return false;
      } catch (error) {
        console.error("Error al verificar partes:", error);
        this.showErrorToast("Error al verificar partes existentes");
        return false;
      } finally {
        this.checkingExisting = false;
      }
    },
    
    async cargarDatosIniciales() {
      try {
        this.loading = true;
        const token = localStorage.getItem("token");
        const headers = {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        };

        const [buquesRes, puertosRes, partesRes] = await Promise.all([
          axios.get("/api/embarcaciones/", { headers }),
          axios.get("/api/puertos/", { headers }),
          axios.get("/api/gemar/registros-pbip/", { headers })
        ]);

        this.listaBuques = buquesRes.data.results || buquesRes.data || [];
        this.listaPuertos = puertosRes.data.results || puertosRes.data || [];
        this.partesPBIP = partesRes.data.results || partesRes.data || [];
      } catch (error) {
        console.error("Error al cargar datos:", error);
        this.showErrorToast("Error al cargar datos iniciales");
      } finally {
        this.loading = false;
      }
    },

    // Métodos de gestión de partes
    async crearPartePBIP() {
      this.loading = true;
      this.error = null;
      this.success = false;

      try {
        // Verificar si ya existe un parte
        const verificacion = await axios.get(
          "/api/gemar/verificar-partes-pbip-existente/",
          {
            params: {
              fecha_actual: this.formData.fecha_actual
            }
          }
        );

        if (verificacion.data.existe) {
          this.isExistingRecord = true;
          await Swal.fire({
            icon: "info",
            title: "Parte existente",
            text: `Ya existe un parte para la fecha ${this.formData.fecha_actual}`,
            confirmButtonColor: "#002a68",
          });
          return;
        }

        // Crear el nuevo parte
        const response = await axios.post(
          "/api/gemar/partes-pbip/",
          {
            fecha_operacion: this.formData.fecha_operacion,
            buque_id: this.formData.buqueSeleccionado,
            puerto_id: this.formData.puertoSeleccionado,
            fecha_hora: this.formData.fechaHoraBuque,
            nivel: this.formData.nivelSeleccionado,
          }
        );

        // Manejar respuesta exitosa
        this.success = true;
        this.isExistingRecord = true;
        this.informeParteId = response.data.id;
        this.existingRecordData = response.data;

        await Swal.fire({
          icon: "success",
          title: "Éxito",
          text: "Parte PBIP creado correctamente",
          confirmButtonColor: "#002a68",
        });

        this.$forceUpdate();
        await this.cargarDatosIniciales();

      } catch (error) {
        console.error("Error al crear parte:", error);
        this.error = error.response?.data || "Error al crear el parte";
        
        await Swal.fire({
          icon: "error",
          title: "Error",
          text: JSON.stringify(this.error),
          confirmButtonColor: "#002a68",
        });
      } finally {
        this.loading = false;
      }
    },

    async editarPartePBIP(parte) {
      this.$router.push({
        name: "Editar-Partes-PBIP",
        params: { id: parte.id },
      });
    },

    async eliminarPartePBIP(id) {
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
          this.loading = true;
          const token = localStorage.getItem("token");
          const headers = {
            Authorization: `Token ${token}`,
            "Content-Type": "application/json",
          };

          await axios.delete(`/api/gemar/registros-pbip/${id}/`, { headers });
          this.showSuccessToast("Parte eliminado correctamente");
          await this.cargarDatosIniciales();
        }
      } catch (error) {
        console.error("Error al eliminar parte PBIP:", error);
        this.showErrorToast("Error al eliminar el parte PBIP");
      } finally {
        this.loading = false;
      }
    },

    // Métodos de estado
    async CambiarEstado(NuevoEstado) {
      try {
        if (!this.informeParteId) {
          await Swal.fire({
            icon: "error",
            title: "Error",
            text: "No se ha encontrado un parte para modificar.",
            confirmButtonColor: "#002a68",
          });
          return;
        }

        const response = await axios.patch(
          `/gemar/partes-pbip/${this.informeParteId}/`,
          { estado_parte: NuevoEstado },
          { headers: { "Content-Type": "application/json" } }
        );

        if (response.status === 200) {
          await Swal.fire({
            icon: "success",
            title: "Éxito",
            text: `Estado actualizado a "${NuevoEstado}" correctamente.`,
            confirmButtonColor: "#002a68",
          });

          // Actualizar el estado y forzar recarga del componente
          this.existingRecordData.estado = NuevoEstado;
          this.componentKey += 1;
          await this.cargarDatosIniciales();
        }
      } catch (error) {
        console.error("Error al cambiar estado:", {
          url: error.config?.url,
          status: error.response?.status,
          data: error.response?.data,
        });
        await Swal.fire({
          icon: "error",
          title: "Error",
          text: error.response?.data?.detail || "Error al actualizar el estado.",
          confirmButtonColor: "#002a68",
        });
      }
    },

    async rechazar() {
      if (!this.hasGroup("RevisorGEMAR")) {
        await Swal.fire({
          icon: "error",
          title: "Acceso denegado",
          text: "No tienes permiso para rechazar el parte PBIP.",
          confirmButtonColor: "#002a68",
        });
        return;
      }
      const result = await Swal.fire({
        title: "¿Estás seguro?",
        text: "¿Está seguro que desea rechazar este parte PBIP?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#002a68",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, rechazar",
        cancelButtonText: "Cancelar",
      });

      if (result.isConfirmed) {
        await this.CambiarEstado("Rechazado");
      }
    },

    async aprobar() {
      if (!this.hasGroup("RevisorGEMAR")) {
        await Swal.fire({
          icon: "error",
          title: "Acceso denegado",
          text: "No tienes permiso para aprobar el parte PBIP.",
          confirmButtonColor: "#002a68",
        });
        return;
      }

      const result = await Swal.fire({
        title: "¿Estás seguro?",
        text: "¿Está seguro que desea aprobar este parte PBIP?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#002a68",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, aprobar",
        cancelButtonText: "Cancelar",
      });

      if (result.isConfirmed) {
        await this.CambiarEstado("Aprobado");
      }
    },

    async listo() {
      if (!this.hasGroup("AdminGEMAR")) {
        await Swal.fire({
          icon: "error",
          title: "Acceso denegado",
          text: "No tienes permiso para cambiar el estado del parte PBIP a 'Listo'.",
          confirmButtonColor: "#002a68",
        });
        return;
      }
      const result = await Swal.fire({
        title: "¿Estás seguro?",
        text: "¿Está seguro que desea poner a 'Listo' este parte PBIP?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#002a68",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, poner a listo",
        cancelButtonText: "Cancelar",
      });

      if (result.isConfirmed) {
        await this.CambiarEstado("Listo");
      }
    },

    // Métodos de utilidad
    hasPermission(permission) {
      if (!this.userPermissions || !Array.isArray(this.userPermissions)) {
        console.warn("userPermissions no está disponible o no es un array");
        return false;
      }
      return this.userPermissions.some((p) => p.codename === permission);
    },

    hasGroup(group) {
      if (!this.userGroups || !Array.isArray(this.userGroups)) {
        return false;
      }
      return this.userGroups.some((g) => g.name === group);
    },

    async fetchUserPermissionsAndGroups() {
      this.loadingPermissions = true;
      try {
        const userId = localStorage.getItem("userid");
        if (userId) {
          const response = await axios.get(
            `/apiAdmin/user/${userId}/permissions-and-groups/`
          );
          
          this.userPermissions = response.data?.permissions || [];
          this.userGroups = response.data?.groups || [];
          
          // Eliminar la verificación de grupos GEMAR para permitir acceso a cualquier usuario autenticado
          // Solo verificar que el usuario esté autenticado
          if (!userId) {
            this.$router.push('/unauthorized');
          }
        }
      } catch (error) {
        console.error("Error al obtener permisos:", error);
        this.userPermissions = [];
        this.userGroups = [];
      } finally {
        this.loadingPermissions = false;
      }
    },

    formatDateTime(dateTime) {
      if (!dateTime) return "";
      const [date, time] = dateTime.split("T");
      const [h, m] = time.split(":");
      return `${date} ${h}:${m}`;
    },

    formatDate(dateString) {
      if (!dateString) return "";
      const date = new Date(dateString);
      return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      });
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
    },
    
    // Métodos para los botones de acción
    cancelar() {
      this.$router.go(-1);
    },
    
    aceptar() {
      // Lógica para aceptar el parte
      console.log("Aceptar parte PBIP");
    }
  },
};
</script>

<style scoped>
.card {
  border-radius: 0.25rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 2px solid #e0e0e0 !important;
  padding: 0.75rem 1.25rem;
}

.form-section {
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 0.25rem;
  margin-bottom: 1rem;
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

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
}

.form-control,
.form-select {
  font-size: 0.875rem;
  padding: 0.25rem 0.5rem;
}

.form-control:focus,
.form-select:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}
</style>