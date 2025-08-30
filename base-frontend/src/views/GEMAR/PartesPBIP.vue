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
    };
  },

  async created() {
    await this.cargarDatosIniciales();
  },

  methods: {
    addBuque() {
      this.$router.push({ name: "Agregar-Partes-PBIP" });
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
          axios.get("/gemar/partes-pbip/", { headers })
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

          await axios.delete(`/gemar/partes-pbip/${id}/`, { headers });
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