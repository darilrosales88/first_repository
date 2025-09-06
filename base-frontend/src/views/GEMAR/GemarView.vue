<template>
  <div>
    <div class="card border" style="margin-left: 15.8em; width: 79%">
      <Navbar-Component />
      <div class="card-header bg-light border-bottom">
        <h6 class="mb-0 text-dark fw-semibold">Sistema de Partes Controlados - GEMAR</h6>
      </div>
      <div class="card-body p-3">
        <!-- Botones de acción -->
        <div class="d-flex justify-content-between mb-4">
          <div class="d-flex gap-2">
            <div class="dropdown">
              <button 
                class="btn btn-sm btn-primary dropdown-toggle"
                type="button"
                id="nuevoParteDropdown"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                <i class="bi bi-plus-circle me-1"></i> Nuevo Parte
              </button>
              <ul class="dropdown-menu" aria-labelledby="nuevoParteDropdown">
                <li>
                  <router-link class="dropdown-item" to="/PartesPBIP">
                    <i class="bi bi-file-text me-2"></i>Partes PBIP
                  </router-link>
                </li>
                <li>
                  <router-link class="dropdown-item" to="/cargas-viejas">
                    <i class="bi bi-archive me-2"></i>Cargas Viejas
                  </router-link>
                </li>
                <li>
                  <router-link class="dropdown-item" to="/ExistenciasMercancia">
                    <i class="bi bi-box-seam me-2"></i>Existencia de Mercancía
                  </router-link>
                </li>
              </ul>
            </div>
            <button 
              @click="exportarExcel" 
              class="btn btn-sm btn-outline-success"
              :disabled="partesCargasViejas.length === 0"
            >
              <i class="bi bi-file-earmark-excel me-1"></i> Exportar Excel
            </button>
          </div>
          <div class="d-flex gap-2">
            <button @click="refreshData" class="btn btn-sm btn-outline-secondary">
              <i class="bi bi-arrow-clockwise me-1"></i> Actualizar
            </button>
          </div>
        </div>

        <!-- Filtros -->
        <div class="row mb-3">
          <div class="col-md-3">
            <label class="form-label small fw-semibold">Fecha desde:</label>
            <input 
              type="date" 
              v-model="filtros.fechaDesde" 
              class="form-control form-control-sm"
            />
          </div>
          <div class="col-md-3">
            <label class="form-label small fw-semibold">Fecha hasta:</label>
            <input 
              type="date" 
              v-model="filtros.fechaHasta" 
              class="form-control form-control-sm"
            />
          </div>
          <div class="col-md-3">
            <label class="form-label small fw-semibold">Organismo:</label>
            <select 
              v-model="filtros.organismo" 
              class="form-select form-select-sm"
            >
              <option value="">Todos</option>
              <option 
                v-for="org in organismos" 
                :key="org.id" 
                :value="org.id"
              >
                {{ org.nombre }}
              </option>
            </select>
          </div>
          <div class="col-md-3">
            <label class="form-label small fw-semibold">Puerto:</label>
            <select 
              v-model="filtros.puerto" 
              class="form-select form-select-sm"
            >
              <option value="">Todos</option>
              <option 
                v-for="puerto in puertos" 
                :key="puerto.id" 
                :value="puerto.id"
              >
                {{ puerto.nombre_puerto }}
              </option>
            </select>
          </div>
        </div>

        <!-- Tabla de partes -->
        <div class="table-responsive">
          <table class="table table-sm table-bordered table-hover">
            <thead class="table-light">
              <tr>
                <th scope="col">ID</th>
                <th scope="col">Fecha Operación</th>
                <th scope="col">Fecha Creación</th>
                <th scope="col">Cant. Registros</th>
                <th scope="col">Total Tons. Hoy</th>
                <th scope="col">Total Tons. Ayer</th>
                <th scope="col">Creado por</th>
                <th scope="col">Estado</th>
                <th scope="col">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="9" class="text-center py-4">
                  <div class="spinner-border spinner-border-sm" role="status"></div>
                  <span class="ms-2">Cargando datos...</span>
                </td>
              </tr>
              <tr v-else-if="partesFiltrados.length === 0">
                <td colspan="9" class="text-center py-4 text-muted">
                  No se encontraron partes de cargas viejas
                </td>
              </tr>
              <tr 
                v-else 
                v-for="parte in partesFiltrados" 
                :key="parte.id"
                :class="{'table-warning': parte.estado === 'PENDIENTE'}"
              >
                <td>{{ parte.id }}</td>
                <td>{{ formatDate(parte.fecha_operacion) }}</td>
                <td>{{ formatDateTime(parte.fecha_creacion) }}</td>
                <td class="text-center">{{ parte.cantidad_registros }}</td>
                <td class="text-end">{{ formatNumber(parte.total_toneladas_hoy) }}</td>
                <td class="text-end">{{ formatNumber(parte.total_toneladas_ayer) }}</td>
                <td>{{ parte.creado_por || 'N/A' }}</td>
                <td>
                  <span 
                    :class="{
                      'badge bg-success': parte.estado === 'APROBADO',
                      'badge bg-warning': parte.estado === 'PENDIENTE',
                      'badge bg-danger': parte.estado === 'RECHAZADO'
                    }"
                  >
                    {{ parte.estado || 'PENDIENTE' }}
                  </span>
                </td>
                <td>
                  <div class="btn-group btn-group-sm">
                    <button 
                      @click="verParte(parte.id)" 
                      class="btn btn-outline-primary"
                      title="Ver detalles"
                    >
                      <i class="bi bi-eye"></i>
                    </button>
                    <button 
                      v-if="isGemarUser && parte.estado !== 'APROBADO'" 
                      @click="editarParte(parte.id)" 
                      class="btn btn-outline-secondary"
                      title="Editar"
                    >
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button 
                      v-if="isAdmin" 
                      @click="eliminarParte(parte.id)" 
                      class="btn btn-outline-danger"
                      title="Eliminar"
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
        <div class="d-flex justify-content-between align-items-center mt-3" v-if="partesFiltrados.length > 0">
          <div class="text-muted small">
            Mostrando {{ partesFiltrados.length }} de {{ partesCargasViejas.length }} registros
          </div>
          <nav>
            <ul class="pagination pagination-sm mb-0">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <button class="page-link" @click="currentPage--">Anterior</button>
              </li>
              <li 
                v-for="page in totalPages" 
                :key="page" 
                class="page-item" 
                :class="{ active: currentPage === page }"
              >
                <button class="page-link" @click="currentPage = page">{{ page }}</button>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <button class="page-link" @click="currentPage++">Siguiente</button>
              </li>
            </ul>
          </nav>
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
  name: "GEMAR",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      partesCargasViejas: [],
      puertos: [],
      organismos: [],
      loading: false,
      currentPage: 1,
      itemsPerPage: 10,
      filtros: {
        fechaDesde: "",
        fechaHasta: "",
        organismo: "",
        puerto: "",
      },
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
    partesFiltrados() {
      let filtered = this.partesCargasViejas;

      // Filtrar por fechas
      if (this.filtros.fechaDesde) {
        filtered = filtered.filter(
          (parte) => parte.fecha_operacion >= this.filtros.fechaDesde
        );
      }

      if (this.filtros.fechaHasta) {
        filtered = filtered.filter(
          (parte) => parte.fecha_operacion <= this.filtros.fechaHasta
        );
      }

      // Filtrar por organismo
      if (this.filtros.organismo) {
        filtered = filtered.filter(
          (parte) => parte.organismo_id == this.filtros.organismo
        );
      }

      // Filtrar por puerto
      if (this.filtros.puerto) {
        filtered = filtered.filter(
          (parte) => parte.puerto_id == this.filtros.puerto
        );
      }

      // Paginación
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return filtered.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.partesCargasViejas.length / this.itemsPerPage);
    },
  },
  async created() {
    await this.cargarDatos();
  },
  methods: {
    async cargarDatos() {
      try {
        this.loading = true;
        const token = localStorage.getItem("token");

        if (!token) {
          this.mostrarError("No se encontró el token de autenticación");
          return;
        }

        const headers = {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        };

        // Cargar partes de cargas viejas - URL corregida
        const partesRes = await axios.get("/api/gemar/partes-carga-vieja/", { headers });
        
        // Cargar datos adicionales solo si es necesario y las rutas existen
        try {
          const [puertosRes, organismosRes] = await Promise.all([
            axios.get("/api/puertos/", { headers }).catch(() => ({ data: [] })),
            axios.get("/api/osde/", { headers }).catch(() => ({ data: [] })),
          ]);

          this.puertos = puertosRes.data.results || puertosRes.data || [];
          this.organismos = organismosRes.data.results || organismosRes.data || [];
        } catch (error) {
          console.warn("No se pudieron cargar algunos datos adicionales:", error);
          this.puertos = [];
          this.organismos = [];
        }

        this.partesCargasViejas = partesRes.data.results || partesRes.data || [];

        // Normalizar datos
        this.puertos = this.puertos.map((p) => ({
          id: p.id,
          nombre_puerto: p.nombre_puerto || p.nombre || "",
        }));

        this.organismos = this.organismos.map((o) => ({
          id: o.id,
          nombre: o.nombre || o.nombre_organismo || "",
        }));

      } catch (error) {
        console.error("Error al cargar datos:", error);
        let errorMessage = "Error al cargar los datos";
        if (error.response) {
          if (error.response.status === 403) {
            errorMessage = "No tiene permisos para acceder a estos datos";
          } else if (error.response.data?.detail) {
            errorMessage = error.response.data.detail;
          }
        }
        this.mostrarError(errorMessage);
      } finally {
        this.loading = false;
      }
    },

    nuevoParte() {
      this.$router.push({ name: "CargasViejas" });
    },

    verParte(id) {
      this.$router.push({ name: "VerParteCargaVieja", params: { id } });
    },

    editarParte(id) {
      this.$router.push({ 
        name: "CargasViejas", 
        params: { id } 
      });
    },

    async eliminarParte(id) {
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

          await axios.delete(`/api/partes-carga-vieja/${id}/`, { headers });
          
          this.mostrarExito("Parte eliminado correctamente");
          await this.cargarDatos();
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

    async exportarExcel() {
      try {
        const token = localStorage.getItem("token");
        const headers = {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        };

        // Construir parámetros de filtro
        const params = {};
        if (this.filtros.fechaDesde) params.fecha_desde = this.filtros.fechaDesde;
        if (this.filtros.fechaHasta) params.fecha_hasta = this.filtros.fechaHasta;
        if (this.filtros.organismo) params.organismo = this.filtros.organismo;
        if (this.filtros.puerto) params.puerto = this.filtros.puerto;

        // Intentar con diferentes endpoints de exportación
        let response;
        try {
          response = await axios.get("/api/partes-carga-vieja/export/", {
            headers,
            params,
            responseType: "blob",
          });
        } catch (exportError) {
          console.warn("Endpoint de exportación principal falló, intentando alternativa");
          response = await axios.get("/api/partes-carga-vieja/export-excel/", {
            headers,
            params,
            responseType: "blob",
          });
        }

        // Crear enlace para descargar el archivo
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `partes_cargas_viejas_${new Date().toISOString().split('T')[0]}.xlsx`);
        document.body.appendChild(link);
        link.click();
        link.remove();

        this.mostrarExito("Archivo exportado correctamente");
      } catch (error) {
        console.error("Error al exportar:", error);
        this.mostrarError("Error al exportar el archivo Excel. La función de exportación puede no estar implementada.");
      }
    },

    refreshData() {
      this.cargarDatos();
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

.btn-group-sm > .btn {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}

.badge {
  font-size: 0.75em;
}

.pagination {
  margin-bottom: 0;
}

.form-control,
.form-select {
  font-size: 0.875rem;
}

.form-label {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

.btn:disabled {
  cursor: not-allowed;
  opacity: 0.65;
}

.dropdown-toggle::after {
  margin-left: 0.5rem;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
}

.dropdown-item i {
  font-size: 1rem;
  width: 1.5rem;
}
</style>