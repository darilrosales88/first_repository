<template>
  <div class="container py-3">
    <div class="card border">
      <!-- Encabezado -->
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-search me-2"></i>Consultar rotación de los vagones
        </h5>
      </div>

      <!-- Cuerpo -->
      <div class="card-body p-3">
        <!-- Formulario de búsqueda -->
        <form @submit.prevent="consultarRotacion">
          <div class="row mb-3 g-2">
            <!-- Campo: Fecha inicial -->
            <div class="col-md-6">
              <div class="form-group">
                <label
                  for="fechaInicial"
                  class="form-label small fw-semibold text-secondary"
                >
                  <i class="bi bi-calendar-date me-2 text-primary"></i>Fecha
                  Inicial
                </label>
                <input
                  type="date"
                  class="form-control form-control-sm border-secondary"
                  id="fechaInicial"
                  v-model="formData.fechaInicial"
                  required
                />
              </div>
            </div>

            <!-- Campo: Fecha final -->
            <div class="col-md-6">
              <div class="form-group">
                <label
                  for="fechaFinal"
                  class="form-label small fw-semibold text-secondary"
                >
                  <i class="bi bi-calendar-check me-2 text-primary"></i>Fecha
                  Final
                </label>
                <input
                  type="date"
                  class="form-control form-control-sm border-secondary"
                  id="fechaFinal"
                  v-model="formData.fechaFinal"
                  required
                />
              </div>
            </div>
          </div>

          <!-- Botón de consulta -->
          <div class="d-flex justify-content-end gap-2 mt-4">
            <button
              type="button"
              class="btn btn-sm btn-outline-secondary"
              @click="resetForm"
            >
              <i class="bi bi-x-circle me-1"></i>Limpiar
            </button>
            <button type="submit" class="btn btn-sm btn-primary">
              <i class="bi bi-search me-1"></i>Consultar
            </button>
          </div>
        </form>

        <!-- Resumen general -->
        <div class="mt-4">
          <h6 class="text-secondary fw-semibold mb-3">
            <i class="bi bi-bar-chart-line me-2"></i>Resumen general
          </h6>
          <div class="row g-3">
            <div class="col-md-6">
              <div class="card border-secondary">
                <div class="card-body p-3">
                  <h6 class="card-title text-secondary fw-semibold">
                    Total de vagones en servicio
                  </h6>
                  <p class="card-text display-6 text-center">
                    {{ resumen.totalVagonesEnServicio }}
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card border-secondary">
                <div class="card-body p-3">
                  <h6 class="card-title text-secondary fw-semibold">
                    Plan carga
                  </h6>
                  <p class="card-text display-6 text-center">
                    {{ resumen.planCarga }}
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card border-secondary">
                <div class="card-body p-3">
                  <h6 class="card-title text-secondary fw-semibold">
                    Real carga
                  </h6>
                  <p class="card-text display-6 text-center">
                    {{ resumen.realCarga }}
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card border-secondary">
                <div class="card-body p-3">
                  <h6 class="card-title text-secondary fw-semibold">
                    Plan de rotación
                  </h6>
                  <p class="card-text display-6 text-center">
                    {{ resumen.planRotacion }}
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card border-secondary">
                <div class="card-body p-3">
                  <h6 class="card-title text-secondary fw-semibold">
                    Real de rotación
                  </h6>
                  <p class="card-text display-6 text-center">
                    {{ resumen.realRotacion }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Registro de rotación por tipo de equipo -->
        <div class="mt-4">
          <h6 class="text-secondary fw-semibold mb-3">
            <i class="bi bi-list-ul me-2"></i>Registro de rotación de cada tipo
            de equipo ferroviario
          </h6>
          <table class="table table-sm table-bordered table-hover">
            <thead class="table-light">
              <tr>
                <th scope="col">Tipo de equipo ferroviario</th>
                <th scope="col">En servicio</th>
                <th scope="col">Plan carga</th>
                <th scope="col">Real carga</th>
                <th scope="col">Plan rotación</th>
                <th scope="col">Real rotación</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(equipo, index) in registrosRotacion" :key="index">
                <td>{{ equipo.tipoEquipoFerroviario }}</td>
                <td>{{ equipo.enServicio }}</td>
                <td>{{ equipo.planCarga }}</td>
                <td>{{ equipo.realCarga }}</td>
                <td>{{ equipo.planRotacion }}</td>
                <td>{{ equipo.realRotacion }}</td>
              </tr>
              <tr v-if="registrosRotacion.length === 0">
                <td colspan="6" class="text-center text-muted">
                  No hay resultados disponibles.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "ConsultaRotacionVagones",
  data() {
    return {
      formData: {
        fechaInicial: "",
        fechaFinal: "",
      },
      resumen: {
        totalVagonesEnServicio: 0,
        planCarga: 0,
        realCarga: 0,
        planRotacion: 0,
        realRotacion: 0,
      },
      registrosRotacion: [], // Almacena los registros de rotación
    };
  },
  methods: {
    async consultarRotacion() {
      // Simula una llamada a la API para obtener los resultados
      try {
        const response = await this.simularConsultaAPI();
        this.resumen = response.resumen;
        this.registrosRotacion = response.registrosRotacion;

        if (this.registrosRotacion.length === 0) {
          this.$swal.fire(
            "Sin resultados",
            "No se encontraron registros en el rango de fechas seleccionado.",
            "info"
          );
        }
      } catch (error) {
        console.error("Error al consultar la rotación:", error);
        this.$swal.fire(
          "Error",
          "Hubo un problema al consultar la rotación de los vagones.",
          "error"
        );
      }
    },
    resetForm() {
      this.formData = {
        fechaInicial: "",
        fechaFinal: "",
      };
      this.resumen = {
        totalVagonesEnServicio: 0,
        planCarga: 0,
        realCarga: 0,
        planRotacion: 0,
        realRotacion: 0,
      };
      this.registrosRotacion = [];
    },
    simularConsultaAPI() {
      // Simulación de datos de respuesta de la API
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            resumen: {
              totalVagonesEnServicio: 150,
              planCarga: 120,
              realCarga: 110,
              planRotacion: 90,
              realRotacion: 85,
            },
            registrosRotacion: [
              {
                tipoEquipoFerroviario: "Locomotora",
                enServicio: 10,
                planCarga: 8,
                realCarga: 7,
                planRotacion: 6,
                realRotacion: 5,
              },
              {
                tipoEquipoFerroviario: "Vagón",
                enServicio: 140,
                planCarga: 112,
                realCarga: 103,
                planRotacion: 84,
                realRotacion: 80,
              },
            ],
          });
        }, 1000); // Simula un retraso de 1 segundo
      });
    },
  },
};
</script>

<style scoped>
/* Resumen general */
.card {
  border-radius: 0.5rem;
  border: 1px solid #e0e0e0;
}

.card-body {
  padding: 1rem;
}

.display-6 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #0d6efd;
}

/* Tabla */
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

/* Mensaje sin resultados */
.text-muted {
  font-size: 0.9rem;
  letter-spacing: 0.02rem;
}

/* Responsive */
@media (max-width: 768px) {
  .table-responsive {
    overflow-x: auto;
  }

  .table {
    min-width: 600px;
  }
}
</style>
