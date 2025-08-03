<template>
  <div style="margin-left: 16em; width: 80%">
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
                  <option value="Creado">Creado</option>
                  <option value="Aprobado">Aprobado</option>
                  <option value="Rechazado">Rechazado</option>
                  <option value="Listo">Listo</option>
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
          <table class="table table-sm table-hover table-bordered">
            <thead class="table-light">
              <tr>
                <th>Tipo</th>
                <th>Fecha</th>
                <th>Estado</th>
                <th>Creado por</th>
                <th>Aprobado por</th>
                <th>Entidad</th>
                <th>Organismo</th>
                <th>Provincia</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loadingData">
                <td colspan="7" class="text-center">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Cargando...</span>
                  </div>
                </td>
              </tr>
              <tr v-else-if="partesCombinados.length === 0">
                <td colspan="7" class="text-center text-muted">No hay registros para mostrar</td>
              </tr>
              <tr v-for="parte in partesCombinados" :key="parte.id">
                <td>
                  {{ getTipoParte(parte.tipo_parte || 'N/A') }}
                </td>
                <td>{{ formatDateTime(parte.fecha_actual) }}</td>
                <td>
                  <span class="badge" :class="getEstadoBadgeClass(parte.estado_parte)">
                    {{ parte.estado_parte }}
                  </span>
                </td>
                <td>{{ parte.creado_por_name || 'N/A' }}</td>
                <td>{{ parte.aprobado_por_name || '-' }}</td>
                <td>{{ parte.entidad_name || 'N/A' }}</td>
                <td>{{ parte.organismo_name || 'N/A' }}</td>
                <td>{{ parte.provincia_name || 'N/A' }}</td>
                <td>
                  <button 
                    class="btn btn-sm btn-outline-primary"
                    @click="verDetalle(parte)"
                    title="Ver detalle"
                  >
                    <i class="bi bi-eye"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="d-flex justify-content-between align-items-center mt-3">
          <div class="text-muted small">
            Mostrando {{ partesCombinados.length }} de {{ totalRegistros }} registros
          </div>
          <nav aria-label="Page navigation">
            <ul class="pagination pagination-sm">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <button class="page-link" @click="prevPage">Anterior</button>
              </li>
              <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: currentPage === page }">
                <button class="page-link" @click="goToPage(page)">{{ page }}</button>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <button class="page-link" @click="nextPage">Siguiente</button>
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
    
    getTipoParte(parte) {
      if (parte == "Parte de hecho extraordinario") {
        return "hecho-extraordinario";
      }
      if (parte == "Parte de programación de maniobras") {
        return "programación-maniobras";
      }
    },
    getEstadoBadgeClass(estado) {
      const classes = {
        'Creado': 'io-status-warning',
        'Aprobado': 'io-status-success',
        'Rechazado': 'io-status-danger',
        'Listo': 'io-status-info',
      };
      return classes[estado] || 'io-status-default';
    },
    formatDateTime(dateTime) {
      if (!dateTime) return 'N/A';
      const date = new Date(dateTime);
      return date.toLocaleString();
    },
    verDetalle(parte) {
      const tipo = this.getTipoParte(parte);
      if (tipo === 'Hecho Extraordinario') {
        this.$router.push(`/gemar/hechos-extraordinarios/detalle/${parte.id}`);
      } else {
        this.$router.push(`/gemar/programacion-maniobras/detalle/${parte.id}`);
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

<!-- En la sección de estilos de RegistrosPartesCombinados.vue -->
<style scoped>
/* Variables de color (copiadas de RegistrosPartesUFC.vue) */
:root {
  --io-primary: #4361ee;
  --io-primary-hover: #3a56d4;
  --io-secondary: #3f37c9;
  --io-accent: #4895ef;
  --io-danger: #f72585;
  --io-success: #4cc9f0;
  --io-warning: #f8961e;
  --io-info: #4895ef;
  --io-light: #f8f9fa;
  --io-dark: #212529;
  --io-gray: #6c757d;
  --io-light-gray: #e9ecef;
  --io-border-radius: 12px;
  --io-box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  --io-transition: all 0.3s ease;
}

/* Tabla - Estilos adaptados de RegistrosPartesUFC */
.io-table-container {
  overflow-x: auto;
  padding: 0.5rem;
}

.table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 0.875rem;
}

.table thead th {
  background-color: #f9fafb;
  border-bottom: 2px solid var(--io-light-gray);
  color: var(--io-dark);
  font-weight: 600;
  padding: 1rem 1.2rem;
  text-align: left;
  position: sticky;
  top: 0;
}

.table tbody tr {
  transition: var(--io-transition);
}

.table tbody tr:hover {
  background-color: rgba(67, 97, 238, 0.03);
}

.table tbody td {
  padding: 1rem 1.2rem;
  border-bottom: 1px solid var(--io-light-gray);
  color: var(--io-dark);
}

/* Badges de estado */
.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
}

/* Clases para los estados (adaptadas de RegistrosPartesUFC) */
.io-status-success {
  background: rgba(76, 201, 240, 0.1);
  color: #06d6a0;
  border: 1px solid rgba(6, 214, 160, 0.2);
}

.io-status-warning {
  background: rgba(248, 150, 30, 0.1);
  color: #f8961e;
  border: 1px solid rgba(248, 150, 30, 0.2);
}

.io-status-danger {
  background: rgba(247, 37, 133, 0.1);
  color: #f72585;
  border: 1px solid rgba(247, 37, 133, 0.2);
}

.io-status-info {
  background: rgba(72, 149, 239, 0.1);
  color: #4895ef;
  border: 1px solid rgba(72, 149, 239, 0.2);
}

.io-status-default {
  background: rgba(108, 117, 125, 0.1);
  color: var(--io-gray);
  border: 1px solid rgba(108, 117, 125, 0.2);
}

/* Botones de acción */
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

/* Paginación */
.io-pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1.5rem;
  padding: 0 0.5rem;
}

.page-link {
  border-radius: var(--io-border-radius) !important;
  margin: 0 2px;
  transition: var(--io-transition);
}

.page-link:hover {
  background-color: var(--io-light-gray);
}

/* Estado de carga */
.io-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.75rem;
  color: var(--io-gray);
  padding: 2rem;
}

.io-empty-state i {
  font-size: 2.5rem;
  color: var(--io-accent);
}

.io-empty-state h3 {
  color: var(--io-dark);
  margin: 0;
  font-size: 1.2rem;
}

.io-empty-state p {
  margin: 0;
  max-width: 400px;
}
</style>