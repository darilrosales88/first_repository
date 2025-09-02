<template>
  <div>
    <div class="card border" style="margin-left: 15.8em; width: 79%">
      <Navbar-Component />
      <div class="card-header bg-light border-bottom">
        <div class="d-flex justify-content-between align-items-center">
          <h6 class="mb-0 text-dark fw-semibold">
            Detalles del Parte de Cargas Viejas #{{ parteId }}
          </h6>
          <button
            class="btn btn-sm btn-outline-secondary"
            @click="$router.push({ name: 'GEMAR' })"
          >
            <i class="bi bi-arrow-left me-1"></i> Volver
          </button>
        </div>
      </div>
      <div class="card-body p-3">
        <!-- Información del parte -->
        <div class="row mb-4">
          <div class="col-md-3">
            <div class="card bg-light">
              <div class="card-body py-2">
                <h6 class="card-title mb-1 small text-muted">Fecha Operación</h6>
                <p class="card-text mb-0 fw-semibold">{{ formatDate(parte.fecha_operacion) }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card bg-light">
              <div class="card-body py-2">
                <h6 class="card-title mb-1 small text-muted">Fecha Creación</h6>
                <p class="card-text mb-0 fw-semibold">{{ formatDateTime(parte.fecha_creacion) }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card bg-light">
              <div class="card-body py-2">
                <h6 class="card-title mb-1 small text-muted">Total Registros</h6>
                <p class="card-text mb-0 fw-semibold">{{ parte.cantidad_registros }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card bg-light">
              <div class="card-body py-2">
                <h6 class="card-title mb-1 small text-muted">Estado</h6>
                <p class="card-text mb-0">
                  <span 
                    :class="{
                      'badge bg-success': parte.estado === 'APROBADO',
                      'badge bg-warning': parte.estado === 'PENDIENTE',
                      'badge bg-danger': parte.estado === 'RECHAZADO'
                    }"
                  >
                    {{ parte.estado || 'PENDIENTE' }}
                  </span>
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Tabla de registros del parte -->
        <div class="table-responsive">
          <table class="table table-sm table-bordered table-hover">
            <thead class="table-light">
              <tr>
                <th scope="col">No.</th>
                <th scope="col">Puerto</th>
                <th scope="col">Terminal</th>
                <th scope="col">Producto</th>
                <th scope="col">Manifiesto</th>
                <th scope="col">Tons. Ayer</th>
                <th scope="col">Tons. Hoy</th>
                <th scope="col">Organismo</th>
                <th scope="col">Días almacén</th>
                <th scope="col">Plan</th>
                <th scope="col">Real</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="11" class="text-center py-4">
                  <div class="spinner-border spinner-border-sm" role="status"></div>
                  <span class="ms-2">Cargando registros...</span>
                </td>
              </tr>
              <tr v-else-if="!parte.registros || parte.registros.length === 0">
                <td colspan="11" class="text-center py-4 text-muted">
                  No se encontraron registros para este parte
                </td>
              </tr>
              <tr v-else v-for="(registro, index) in parte.registros" :key="registro.id">
                <td>{{ index + 1 }}</td>
                <td>{{ getPuertoNombre(registro.puerto_id) }}</td>
                <td>{{ getTerminalNombre(registro.terminal_id) }}</td>
                <td>{{ getProductoNombre(registro.producto_id) }}</td>
                <td>{{ registro.manifiesto }}</td>
                <td class="text-end">{{ formatNumber(registro.toneladas_ayer) }}</td>
                <td class="text-end">{{ formatNumber(registro.toneladas_hoy) }}</td>
                <td>{{ getOrganismoNombre(registro.organismo_id) }}</td>
                <td class="text-center">{{ registro.dias_almacen }}</td>
                <td class="text-end">{{ formatNumber(registro.plan) }}</td>
                <td class="text-end">{{ formatNumber(registro.real) }}</td>
              </tr>
              <!-- Totales -->
              <tr v-if="parte.registros && parte.registros.length > 0" class="table-info fw-semibold">
                <td colspan="5" class="text-end">TOTALES:</td>
                <td class="text-end">{{ formatNumber(parte.total_toneladas_ayer) }}</td>
                <td class="text-end">{{ formatNumber(parte.total_toneladas_hoy) }}</td>
                <td colspan="2"></td>
                <td class="text-end">{{ formatNumber(parte.total_plan) }}</td>
                <td class="text-end">{{ formatNumber(parte.total_real) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Botones de acción -->
        <div class="d-flex justify-content-center gap-3 mt-4">
          <button 
            @click="exportarRegistroExcel" 
            class="btn btn-sm btn-outline-success"
            :disabled="!parte.registros || parte.registros.length === 0"
          >
            <i class="bi bi-file-earmark-excel me-1"></i> Exportar Excel
          </button>
          <button 
            v-if="isGemarUser && parte.estado !== 'APROBADO'" 
            @click="editarParte" 
            class="btn btn-sm btn-primary"
          >
            <i class="bi bi-pencil me-1"></i> Editar Parte
          </button>
          <button 
            v-if="isAdmin" 
            @click="eliminarParte" 
            class="btn btn-sm btn-outline-danger"
          >
            <i class="bi bi-trash me-1"></i> Eliminar Parte
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "VerParteCargaVieja",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      parteId: this.$route.params.id,
      parte: {
        registros: []
      },
      puertos: [],
      terminales: [],
      productos: [],
      organismos: [],
      loading: false,
    };
  },
  computed: {
    isAdmin() {
      const userData = JSON.parse(localStorage.getItem("userData") || "{}");
      return userData.is_superuser;
    },
    isGemarUser() {
      const userData = JSON.parse(localStorage.getItem("userData") || "{}");
      return userData.rol === "GEMAR" || userData.is_superuser;
    },
  },
  async created() {
    await this.cargarDatosIniciales();
    await this.cargarParte();
  },
  methods: {
    async cargarDatosIniciales() {
      try {
        const token = localStorage.getItem("token");

        if (!token) {
          this.mostrarError("No se encontró el token de autenticación");
          return;
        }

        const headers = {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        };

        const [puertosRes, productosRes, organismosRes, terminalesRes] = await Promise.all([
          axios.get("/api/puertos/", { headers }),
          axios.get("/api/productos/", { headers }),
          axios.get("/api/osde/", { headers }),
          axios.get("/api/terminales/", { headers }),
        ]);

        this.puertos = puertosRes.data.results || puertosRes.data || [];
        this.productos = productosRes.data.results || productosRes.data || [];
        this.organismos = organismosRes.data.results || organismosRes.data || [];
        this.terminales = terminalesRes.data.results || terminalesRes.data || [];

      } catch (error) {
        console.error("Error al cargar datos:", error);
        this.mostrarError("Error al cargar datos iniciales");
      }
    },

    async cargarParte() {
      try {
        this.loading = true;
        const token = localStorage.getItem("token");
        const headers = {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        };

        const response = await axios.get(`/api/gemar/partes-carga-vieja/${this.parteId}/`, { headers });
        this.parte = response.data;

      } catch (error) {
        console.error("Error al cargar el parte:", error);
        let errorMessage = "Error al cargar el parte";
        if (error.response) {
          if (error.response.status === 404) {
            errorMessage = "Parte no encontrado";
          } else if (error.response.status === 403) {
            errorMessage = "No tiene permisos para ver este parte";
          }
        }
        this.mostrarError(errorMessage);
        this.$router.push({ name: 'GEMAR' });
      } finally {
        this.loading = false;
      }
    },

    getPuertoNombre(puertoId) {
      const puerto = this.puertos.find(p => p.id === puertoId);
      return puerto ? (puerto.nombre_puerto || puerto.nombre || 'N/A') : 'N/A';
    },

    getTerminalNombre(terminalId) {
      const terminal = this.terminales.find(t => t.id === terminalId);
      return terminal ? (terminal.nombre_terminal || terminal.nombre || 'N/A') : 'N/A';
    },

    getProductoNombre(productoId) {
      const producto = this.productos.find(p => p.id === productoId);
      return producto ? (producto.nombre_producto || producto.nombre || 'N/A') : 'N/A';
    },

    getOrganismoNombre(organismoId) {
      const organismo = this.organismos.find(o => o.id === organismoId);
      return organismo ? (organismo.nombre || organismo.nombre_organismo || 'N/A') : 'N/A';
    },

    async exportarRegistroExcel() {
      try {
        const token = localStorage.getItem("token");
        const headers = {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        };

        const response = await axios.get(`/api/gemar/partes-carga-vieja/${this.parteId}/export/`, {
          headers,
          responseType: "blob",
        });

        // Crear enlace para descargar el archivo
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `parte_carga_vieja_${this.parteId}_${new Date().toISOString().split('T')[0]}.xlsx`);
        document.body.appendChild(link);
        link.click();
        link.remove();

        this.mostrarExito("Archivo exportado correctamente");
      } catch (error) {
        console.error("Error al exportar:", error);
        this.mostrarError("Error al exportar el archivo Excel");
      }
    },

    editarParte() {
      this.$router.push({ 
        name: "CargasViejas", 
        params: { id: this.parteId } 
      });
    },

    async eliminarParte() {
      try {
        const result = await Swal.fire({
          title: "¿Está seguro?",
          text: "Esta acción no se puede deshacer",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#d33",
          cancelButtonColor: "#3085d6",
          confirmButtonText: "Sí, eliminar",
          cancelButtonText: "Cancelar",
        });

        if (result.isConfirmed) {
          const token = localStorage.getItem("token");
          const headers = {
            Authorization: `Token ${token}`,
          };

          await axios.delete(`/api/gemar/partes-carga-vieja/${this.parteId}/`, { headers });
          
          this.mostrarExito("Parte eliminado correctamente");
          this.$router.push({ name: 'GEMAR' });
        }
      } catch (error) {
        console.error("Error al eliminar:", error);
        let errorMessage = "Error al eliminar el parte";
        if (error.response) {
          if (error.response.status === 403) {
            errorMessage = "No tiene permisos para eliminar este parte";
          } else if (error.response.data?.detail) {
            errorMessage = error.response.data.detail;
          }
        }
        this.mostrarError(errorMessage);
      }
    },

    formatDate(dateString) {
      if (!dateString) return "N/A";
      return new Date(dateString).toLocaleDateString("es-ES");
    },

    formatDateTime(dateTimeString) {
      if (!dateTimeString) return "N/A";
      return new Date(dateTimeString).toLocaleString("es-ES");
    },

    formatNumber(value) {
      if (value === null || value === undefined) return "0.00";
      return parseFloat(value).toLocaleString("es-ES", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });
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

.badge {
  font-size: 0.75em;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

.btn:disabled {
  cursor: not-allowed;
  opacity: 0.65;
}
</style>