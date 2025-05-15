<template>
  <div class="container py-3">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-clipboard-data me-2"></i>Registros de operaciones UFC
        </h5>
      </div>

      <div class="card-body p-3">
        <form @submit.prevent="submitForm">
          <!-- Fila 1 -->
          <div class="row mb-3 g-2">
            <div class="col-md-6">
              <div class="form-group">
                <label
                  for="fechaActual"
                  class="form-label small fw-semibold text-secondary"
                >
                  <i class="bi bi-calendar-check me-2 text-primary"></i>Fecha
                  Actual
                </label>
                <input
                  type="date"
                  class="form-control form-control-sm border-secondary"
                  id="fechaActual"
                  v-model="formData.fecha_actual"
                  required
                  :disabled="isExistingRecord"
                />
              </div>
            </div>
          </div>

          <!-- Fila 2 -->
          <div class="row mb-3 g-2">
            <div class="col-md-6">
              <div class="form-group">
                <label
                  for="planMensualTotal"
                  class="form-label small fw-semibold text-secondary"
                >
                  <i class="bi bi-calendar-month me-2 text-primary"></i>Plan
                  Mensual Total
                </label>
                <input
                  type="number"
                  class="form-control form-control-sm border-secondary"
                  id="planMensualTotal"
                  v-model="formData.plan_mensual_total"
                  :disabled="isExistingRecord"
                />
              </div>
            </div>

            <div class="col-md-6">
              <div class="form-group">
                <label
                  for="planDiarioTotal"
                  class="form-label small fw-semibold text-secondary"
                >
                  <i class="bi bi-calendar-day me-2 text-primary"></i>Plan
                  Diario Total Vagones Cargados
                </label>
                <input
                  type="number"
                  class="form-control form-control-sm border-secondary"
                  id="planDiarioTotal"
                  v-model="formData.plan_diario_total_vagones_cargados"
                  :disabled="isExistingRecord"
                />
              </div>
            </div>
          </div>

          <!-- Fila 3 -->
          <div class="row mb-3 g-2">
            <div class="col-md-6">
              <div class="form-group">
                <label
                  for="realTotalVagones"
                  class="form-label small fw-semibold text-secondary"
                >
                  <i class="bi bi-train-freight-front me-2 text-primary"></i
                  >Real Total Vagones Cargados
                </label>
                <input
                  type="number"
                  class="form-control form-control-sm border-secondary"
                  id="realTotalVagones"
                  v-model="formData.real_total_vagones_cargados"
                  :disabled="isExistingRecord"
                />
              </div>
            </div>

            <div class="col-md-6">
              <div class="form-group">
                <label
                  for="totalVagonesSituados"
                  class="form-label small fw-semibold text-secondary"
                >
                  <i class="bi bi-pin-map me-2 text-primary"></i>Total de
                  Vagones Situados
                </label>
                <input
                  type="number"
                  class="form-control form-control-sm border-secondary"
                  id="totalVagonesSituados"
                  v-model="formData.total_vagones_situados"
                  :disabled="isExistingRecord"
                />
              </div>
            </div>
          </div>

          <!-- Fila 4 -->
          <div class="row mb-4 g-2">
            <div class="col-md-6">
              <div class="form-group">
                <label
                  for="planTotalAcumulado"
                  class="form-label small fw-semibold text-secondary"
                >
                  <i class="bi bi-graph-up me-2 text-primary"></i>Plan Total
                  Acumulado Actual
                </label>
                <input
                  type="number"
                  class="form-control form-control-sm border-secondary"
                  id="planTotalAcumulado"
                  v-model="formData.plan_total_acumulado_actual"
                  :disabled="isExistingRecord"
                />
              </div>
            </div>

            <div class="col-md-6">
              <div class="form-group">
                <label
                  for="realTotalAcumulado"
                  class="form-label small fw-semibold text-secondary"
                >
                  <i class="bi bi-graph-up-arrow me-2 text-primary"></i>Real
                  Total Acumulado Actual
                </label>
                <input
                  type="number"
                  class="form-control form-control-sm border-secondary"
                  id="realTotalAcumulado"
                  v-model="formData.real_total_acumulado_actual"
                  :disabled="isExistingRecord"
                />
              </div>
            </div>
          </div>

          <!-- Botones -->
          <div class="d-flex justify-content-end gap-2 mt-4">
            <button
              type="submit"
              class="btn btn-sm btn-primary"
              :disabled="isExistingRecord || isLoading"
            >
              <i class="bi bi-save me-1"></i>Guardar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";

export default {
  name: "InfOperative",
  data() {
    return {
      informeOperativoId: null,
      isExistingRecord: false,
      formData: {
        fecha_actual: "",
        plan_mensual_total: 0,
        plan_diario_total_vagones_cargados: 0,
        real_total_vagones_cargados: 0,
        total_vagones_situados: 0,
        plan_total_acumulado_actual: 0,
        real_total_acumulado_actual: 0,
      },
      isLoading: false,
      checkInterval: null, // Almacenaremos el intervalo aquí
    };
  },
  async mounted() {
    // Obtener la fecha actual en formato YYYY-MM-DD según la zona horaria local
    const now = new Date();
    const offset = now.getTimezoneOffset() * 60000; // offset en milisegundos
    const localISOTime = new Date(now - offset).toISOString().split("T")[0];
    this.formData.fecha_actual = localISOTime;

    // Check for existing record on load
    await this.checkExistingRecord();

    // Configurar el intervalo para verificar cada 10 segundos
  },
  beforeUnmount() {
    // Limpiar el intervalo cuando el componente se desmonte
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
    }
  },
  methods: {
    async checkExistingRecord() {
      try {
        // Enviar la fecha ya ajustada a la vista para ver si existe el parte
        const response = await axios.get("/ufc/verificar-informe-existente/", {
          params: { fecha_operacion: this.formData.fecha_actual },
        });

        if (response.data.existe) {
          this.informeOperativoId = response.data.id;
          this.isExistingRecord = true;

          // Cargar datos del informe creado
          const recordResponse = await axios.get(
            `/ufc/informe-operativo/${this.informeOperativoId}/`
          );

          // Formatear la fecha para mostrar solo YYYY-MM-DD
          if (recordResponse.data.fecha_actual) {
            this.formData.fecha = new Date().toISOString();
            const today = new Date();
            const fechaFormateada = `${today.getFullYear()}-${String(
              today.getMonth() + 1
            ).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;
            this.formData = {
              ...recordResponse.data,
              fecha_actual: fechaFormateada,
            };
          } else {
            this.formData = recordResponse.data;
          }
        }
      } catch (error) {
        console.error("Error al verificar informe:", error);
      }
    },

    async submitForm() {
      if (this.isExistingRecord) {
        Swal.fire(
          "Error",
          "Ya existe un informe creado para la fecha actual.",
          "error"
        );
        return;
      }

      this.isLoading = true;
      try {
        const dataToSend = {
          fecha_actual: this.formData.fecha_actual, // Usamos la fecha ya ajustada
          plan_mensual_total: this.formData.plan_mensual_total || 0,
          plan_diario_total_vagones_cargados:
            this.formData.plan_diario_total_vagones_cargados || 0,
          real_total_vagones_cargados:
            this.formData.real_total_vagones_cargados || 0,
          total_vagones_situados: this.formData.total_vagones_situados || 0,
          plan_total_acumulado_actual:
            this.formData.plan_total_acumulado_actual || 0,
          real_total_acumulado_actual:
            this.formData.real_total_acumulado_actual || 0,
        };

        const response = await axios.post(
          "/ufc/informe-operativo/",
          dataToSend
        );
        this.informeOperativoId = response.data.id;
        this.isExistingRecord = true;

        await Swal.fire({
          title: "¡Éxito!",
          text: "Los datos operativos se han guardado correctamente.",
          icon: "success",
          confirmButtonText: "Aceptar",
        });
      } catch (error) {
        console.error("Error al guardar operación:", error);

        let errorMessage = "Ocurrió un error al guardar los datos.";
        if (error.response?.data) {
          errorMessage = Object.values(error.response.data).join("<br>");
        }

        await Swal.fire({
          title: "Error",
          html: errorMessage,
          icon: "error",
          confirmButtonText: "Entendido",
        });
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>
