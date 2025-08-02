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
        'Creado': 'bg-secondary bg-opacity-10 text-secondary',
        'Aprobado': 'bg-success bg-opacity-10 text-success',
        'Rechazado': 'bg-danger bg-opacity-10 text-danger',
        'Listo': 'bg-info bg-opacity-10 text-info',
      };
      return classes[estado] || 'bg-light text-dark';
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

<style scoped>
/* Estilos mejorados para los botones de acción */
.action-buttons {
  display: flex;
  gap: 15px;
  margin: 30px auto;
  justify-content: center;
  padding: 20px 0;
  width: 100%;
}

.action-btn {
  padding: 12px 25px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 120px;
}

.approve {
  background-color: #28a745;
  color: white;
}

.approve:hover {
  background-color: #218838;
}

.reject {
  background-color: #dc3545;
  color: white;
}

.reject:hover {
  background-color: #c82333;
}

.ready {
  background-color: #17a2b8;
  color: white;
}

.ready:hover {
  background-color: #138496;
}

.action-btn i {
  margin-right: 8px;
  font-size: 18px;
}

/* Estilos generales del navbar */
nav ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 15px;
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

nav ul li {
  display: inline;
}

a {
  text-decoration: none;
  color: #333;
  cursor: pointer;
  padding: 10px 20px;
  border-radius: 5px;
  transition: all 0.3s ease;
  font-weight: 500;
  display: inline-block;
}

nav a:hover {
  background-color: #e9ecef;
  color: #000;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

nav a.active {
  background-color: #007bff;
  color: #fff;
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
  transform: translateY(-2px);
}

nav a:active {
  transform: translateY(0);
}

nav ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 10px;
}

nav ul li {
  display: inline;
}

a {
  text-decoration: none;
  color: inherit;
  cursor: pointer;
}

/* Estilos para la tabla */
.table {
  font-size: 0.875rem;
}

.table th {
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.5px;
}

.badge {
  padding: 0.35em 0.65em;
  font-size: 0.75em;
  font-weight: 600;
}
</style>