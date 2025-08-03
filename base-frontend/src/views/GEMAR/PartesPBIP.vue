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
                    v-model="parte.fecha_operacion"
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
                    v-model="parte.fecha_actual"
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
                  <th scope="col">Fecha y Hora</th>
                  <th scope="col">Nivel</th>
                  <th scope="col">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in buques" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td>{{ getNombreBuque(item.buque_id) }}</td>
                  <td>{{ getNombrePuerto(item.puerto_id) }}</td>
                  <td>{{ formatDateTime(item.fecha_hora) }}</td>
                  <td>Nivel {{ item.nivel }}</td>
                  <td>
                    <div class="d-flex gap-1">
                      <button
                        @click="editarPartePBIP(item)"
                        class="btn btn-sm btn-outline-primary"
                      >
                        <i class="bi bi-pencil"></i> Editar
                      </button>
                      <button
                        @click="removeBuque(index)"
                        class="btn btn-sm btn-outline-danger"
                      >
                        <i class="bi bi-trash"></i> Eliminar
                      </button>
                    </div>
                    <button
                      @click="removeBuque(index)"
                      class="btn btn-sm btn-outline-danger"
                    >
                      <i class="bi bi-trash"></i> Eliminar
                    </button>
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
              Mostrando 1-15 de {{ buques.length }} registros
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

        <!-- Botones de acción -->
        <div class="d-flex justify-content-center gap-3 mt-4">
          <button @click="rechazar" class="btn btn-sm btn-outline-danger">
            <i class="bi bi-x-circle me-1"></i> Rechazar
          </button>
          <button @click="aprobar" class="btn btn-sm btn-outline-success">
            <i class="bi bi-check-circle me-1"></i> Aprobar
          </button>
          <button @click="listo" class="btn btn-sm btn-outline-primary">
            <i class="bi bi-check-all me-1"></i> Listo
          </button>
          <button @click="cancelar" class="btn btn-sm btn-outline-secondary">
            <i class="bi bi-x me-1"></i> Cancelar
          </button>
          <button @click="aceptar" class="btn btn-sm btn-primary">
            <i class="bi bi-save me-1"></i> Aceptar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import EditarPartePBIP from "./EditarPartePBIP.vue";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "PartesPBIP",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      parte: {
        fecha_operacion: "",
        fecha_actual: new Date().toISOString().slice(0, 16),
      },
      buques: [],
      listaBuques: [],
      listaPuertos: [],
      loading: false,
      error: null,
      debugInfo: {
        buquesResponse: null,
        puertosResponse: null,
      },
    };
  },
  computed: {
    getNombreBuque() {
      return (buqueId) => {
        const buque = this.listaBuques.find((b) => b.id === buqueId);
        return buque ? buque.nombre : "Buque no encontrado";
      };
    },
    getNombrePuerto() {
      return (puertoId) => {
        const puerto = this.listaPuertos.find((p) => p.id === puertoId);
        return puerto ? puerto.nombre : "Puerto no encontrado";
      };
    },
  },
  async created() {
    await this.cargarDatosIniciales();
    console.log("Datos cargados:", {
      buques: this.listaBuques,
      puertos: this.listaPuertos,
      debugInfo: this.debugInfo,
    });
  },
  methods: {
    editarPartePBIP(buque) {
      this.$router.push({
        name: "EditarPartePBIP",
        params: {
          id: buque.buque_id,
          buqueData: JSON.stringify(buque),
          listaBuques: JSON.stringify(this.listaBuques),
          listaPuertos: JSON.stringify(this.listaPuertos),
        },
      });
    },

    async cargarDatosIniciales() {
      try {
        this.loading = true;

        const instance = axios.create({
          baseURL: "http://127.0.0.1:8000",
          withCredentials: true,
        });

        const [buquesRes, puertosRes] = await Promise.all([
          instance.get("/api/embarcaciones/"),
          instance.get("/api/puertos/"),
        ]);

        this.debugInfo.buquesResponse = buquesRes.data;
        this.debugInfo.puertosResponse = puertosRes.data;

        this.listaBuques = buquesRes.data.results || [];
        this.listaPuertos = puertosRes.data.results || [];

        this.listaBuques = this.listaBuques.map((b) => ({
          id: b.id,
          nombre: b.nombre || b.nombre_buque || "",
        }));

        this.listaPuertos = this.listaPuertos.map((p) => ({
          id: p.id,
          nombre: p.nombre || p.nombre_puerto || "",
        }));
      } catch (error) {
        console.error("Error al cargar datos:", error);
        let errorMessage = "Error al cargar datos iniciales";
        if (error.response) {
          console.error("Detalles del error:", error.response.data);
          if (error.response.data?.detail) {
            errorMessage = error.response.data.detail;
          }
        }
        this.mostrarError(errorMessage);
      } finally {
        this.loading = false;
      }
    },
    //cancelar() {
    // Opcional: preguntar confirmación antes de limpiar
    //f (this.cargas.some(c => c.puerto_id || c.producto_id || c.organismo_id)) {
    //Swal.fire({
    //title: '¿Cancelar cambios?',
    //text: "Los datos no guardados se perderán",
    //icon: 'warning',
    //showCancelButton: true,
    //confirmButtonColor: '#3085d6',
    //cancelButtonColor: '#d33',
    //confirmButtonText: 'Sí, cancelar',
    //cancelButtonText: 'No, continuar editando'
    //}).then((result) => {
    //if (result.isConfirmed) {
    //this.resetForm();
    // }
    // });
    // } else {
    // this.resetForm();
    //}
    //},
    addBuque() {
      this.$router.push({
        name: "AgregarBuque",
        params: {
          listaPuertos: this.listaPuertos,
        },
      });
    },

    handleBuqueAgregado(nuevoBuque) {
      this.buques.push({
        buque_id: nuevoBuque.id,
        puerto_id: nuevoBuque.puerto_id,
        fecha_hora: nuevoBuque.fecha_hora,
        nivel: nuevoBuque.nivel,
      });
    },

    removeBuque(index) {
      if (this.buques.length > 1) {
        this.buques.splice(index, 1);
      } else {
        this.mostrarError("Debe haber al menos un buque");
      }
    },

    formatDateTime(dateTime) {
      if (!dateTime) return "";
      const [date, time] = dateTime.split("T");
      const [h, m] = time.split(":");
      return `${date} ${h}:${m}`;
    },

    async aceptar() {
      if (!this.validarFormulario()) return;

      try {
        this.loading = true;

        const instance = axios.create({
          baseURL: "http://127.0.0.1:8000",
          withCredentials: true,
        });

        const payload = {
          fecha_operacion: this.parte.fecha_operacion,
          buques: this.buques.map((b) => ({
            buque_id: b.buque_id,
            puerto_id: b.puerto_id,
            fecha_hora: b.fecha_hora,
            nivel: b.nivel,
          })),
        };

        const response = await instance.post(
          "/api/gemar/partes-pbip/",
          payload
        );

        if (response.status === 201) {
          this.mostrarExito("Parte PBIP creado correctamente");
          this.resetFormulario();
          this.$emit("parte-creado");
        } else {
          this.mostrarError("Error inesperado al crear el parte PBIP");
        }
      } catch (error) {
        console.error("Error al guardar:", error);
        let errorMessage = "Error al crear el parte PBIP";
        if (error.response) {
          if (error.response.status === 400) {
            errorMessage = error.response.data.detail || "Datos inválidos";
          }
        }
        this.mostrarError(errorMessage);
      } finally {
        this.loading = false;
      }
    },

    validarFormulario() {
      if (!this.parte.fecha_operacion) {
        this.error = "La fecha de operación es requerida";
        this.mostrarError(this.error);
        return false;
      }

      if (this.buques.length === 0) {
        this.error = "Debe agregar al menos un buque";
        this.mostrarError(this.error);
        return false;
      }

      for (const buque of this.buques) {
        if (!buque.buque_id || !buque.puerto_id || !buque.fecha_hora) {
          this.error = "Todos los campos son requeridos para cada buque";
          this.mostrarError(this.error);
          return false;
        }
      }

      this.error = null;
      return true;
    },

    resetFormulario() {
      this.parte = {
        fecha_operacion: "",
        fecha_actual: new Date().toISOString().slice(0, 16),
      };
      this.buques = [];
      this.error = null;
    },

    cancelar() {
      his.resetFormulario();
    },

    async rechazar() {
      try {
        this.mostrarExito("Parte rechazado correctamente");
      } catch (error) {
        this.mostrarError("Error al rechazar el parte");
      }
    },

    async aprobar() {
      try {
        this.mostrarExito("Parte aprobado correctamente");
      } catch (error) {
        this.mostrarError("Error al aprobar el parte");
      }
    },

    listo() {
      this.mostrarExito("Parte marcado como listo");
    },

    mostrarError(mensaje) {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: mensaje,
        confirmButtonText: "Aceptar",
      });
    },

    mostrarExito(mensaje) {
      Swal.fire({
        icon: "success",
        title: "Éxito",
        text: mensaje,
        confirmButtonText: "Aceptar",
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