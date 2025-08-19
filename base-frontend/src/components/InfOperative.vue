<template>
  <div class="container py-3">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h6 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-clipboard-data me-2"></i>Registros de operaciones -
          UFC
        </h6>
      </div>

      <div class="card-body p-3">
        <form @submit.prevent="submitForm">
          <!-- Fila 2 - Modificada para mejor responsividad -->
          <div class="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-3 mb-4">
            <div class="col">
              <div class="form-group">
                <label
                  for="planMensualTotal"
                  class="form-label small fw-semibold text-secondary">
                  <i class="bi bi-calendar-month me-2 text-primary"></i>Plan
                  Mensual Total
                </label>
                <input
                  type="text"
                  class="form-control form-control-sm border-secondary mt-2"
                  id="planMensualTotal"
                  v-model="formData.plan_mensual_total"
                  :disabled="isExistingRecord" readonly
                />
              </div>
            </div>

            <div class="col">
              <div class="form-group">
                <label
                  for="planDiarioTotal"
                  class="form-label small fw-semibold text-secondary"
                >
                  <i class="bi bi-calendar-day me-2 text-primary"></i>Plan
                  Diario Total
                </label>
                <input
                  type="text"
                  class="form-control form-control-sm border-secondary mt-2"
                  id="planDiarioTotal"
                  v-model="formData.plan_diario_total_vagones_cargados"
                  :disabled="isExistingRecord" readonly
                />
              </div>
            </div>

            <div class="col">
              <div class="form-group">
                <label
                  for="realTotalVagones"
                  class="form-label small fw-semibold text-secondary"
                >
                  <i class="bi bi-train-freight-front me-2 text-primary"></i
                  >Real Total Vagones
                </label>
                <input
                  type="text"
                  class="form-control form-control-sm border-secondary mt-2"
                  id="realTotalVagones"
                  v-model="formData.real_total_vagones_cargados"
                  :disabled="isExistingRecord" readonly
                />
              </div>
            </div>

            <div class="col">
              <div class="form-group">
                <label
                  for="totalVagonesSituados"
                  class="form-label small fw-semibold text-secondary"
                >
                  <i class="bi bi-pin-map me-2 text-primary"></i>Total Vagones
                  Situados
                </label>
                <input
                  type="text"
                  class="form-control form-control-sm border-secondary mt-2"
                  id="totalVagonesSituados"
                  v-model="formData.total_vagones_situados"
                  :disabled="isExistingRecord" readonly
                />
              </div>
            </div>
          </div>

          <!-- Fila 3 - Modificada -->
          <div class="row row-cols-1 row-cols-md-2 g-3 mb-4">
            <div class="col">
              <div class="form-group">
                <label
                  for="planTotalAcumulado"
                  class="form-label small fw-semibold text-secondary"
                >
                  <i class="bi bi-graph-up me-2 text-primary"></i>Plan Total
                  Acumulado
                </label>
                <input
                  type="text"
                  class="form-control form-control-sm border-secondary"
                  id="planTotalAcumulado"
                  v-model="formData.plan_total_acumulado_actual"
                  :disabled="isExistingRecord" readonly
                />
              </div>
            </div>

            <div class="col">
              <div class="form-group">
                <label
                  for="realTotalAcumulado"
                  class="form-label small fw-semibold text-secondary"
                >
                  <i class="bi bi-graph-up-arrow me-2 text-primary"></i>Real
                  Total Acumulado
                </label>
                <input
                  type="text"
                  class="form-control form-control-sm border-secondary"
                  id="realTotalAcumulado"
                  v-model="formData.real_total_acumulado_actual"
                  :disabled="isExistingRecord" readonly
                />
              </div>
            </div>
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
  props: {
    fechaActual: {
      type: Date,
      required: true,
    },
    fechaOperacion: {
      type: Date,
      required: true,
    },
    informeID: {
      type: Number,
      required: false,
    },
  },
  data() {
    return {
      informeOperativoId: null,
      isExistingRecord: false,
      fecha_actual: this.fechaActual,
      fecha_operacion: this.fechaOperacion,
      formData: {
        fecha_actual: "",
        fecha_operacion: "",
        plan_mensual_total: 0,
        plan_diario_total_vagones_cargados: 0,
        real_total_vagones_cargados: 0,
        total_vagones_situados: 0,
        plan_total_acumulado_actual: 0,
        real_total_acumulado_actual: 0,
        provincia: null,
        creado_por: null,
        aprobado_por: null,
      },
      isLoading: false,
      checkInterval: null, // Almacenaremos el intervalo aquí
    };
  },
  async mounted() {
    await this.obtenerUsername(); //Busca el nombre del usuario
    await this.checkExistingRecord();
  },

  beforeUnmount() {
    // Limpiar el intervalo cuando el componente se desmonte
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
    }
  },

  methods: {
    visualizarInforme() {
      if (this.informeOperativoId) {
        // Abre en una nueva pestaña
        const route = this.$router.resolve({
          path: `/VisualizarInfoOperative/${this.informeOperativoId}`,
        });
        window.open(route.href, "_blank");
      }
    },

    async checkExistingRecord() {
      try {
        // Enviar la fecha ya ajustada a la vista para ver si existe el parte
        const response = await axios.get("/ufc/verificar-informe-existente/", {
          params: { fecha_operacion: this.fecha_actual },
        });

        if (response.data.existe) {
          this.informeOperativoId = response.data.id;
          this.isExistingRecord = true;

          this.$emit("record-status-changed", {
            isExisting: true,
          });

          // Cargar datos del informe creado
          const recordResponse = await axios.get(
            `/ufc/informe-operativo/${
              this.informeID ? this.informeID : this.informeOperativoId
            }/`
          );

          // Formatear la fecha para mostrar solo YYYY-MM-DD
          if (recordResponse.data.fecha_operacion) {
            this.fecha_actual = recordResponse.data.fecha_operacion;
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
    async obtenerUsername() {
      try {
        const userId = localStorage.getItem("userid");
        if (userId) {
          const response = await axios.get(`/apiAdmin/users/${userId}/`);
          
          console.log("El dato del usuario es ", response.data);
          this.formData.creado_por = response.data.id;
        }
      } catch (error) {
        console.error("Error al obtener Nombre de Usuario:", error);
        Swal.fire("Error", "Error al obtener Nombre de Usuario:", "error");
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
          fecha_actual: this.fecha_actual, // Usamos la fecha ya ajustada
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
          provincia: this.formData.provincia,
          creado_por: this.formData.creado_por,
          aprobado_por: this.formData.aprobado_por,
        };


        const response = await axios.post(
          "/ufc/informe-operativo/",
          dataToSend
        );
        this.informeOperativoId = response.data.id;
        this.isExistingRecord = true;

        this.$emit("record-status-changed", {
          isExisting: true,
        });
        
        this.showSuccessToast("Informe creado correctamente");
      } catch (error) {
        console.error("Error al guardar operación:", error);
        this.showErrorToast("Error al crear el informe");
        let errorMessage = "Ocurrió un error al guardar los datos.";
        if (error.response?.data) {
          errorMessage = Object.values(error.response.data).join("<br>");
        }
      } finally {
        this.isLoading = false;
      }
    },

    showSuccessToast(message) {
      const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        background: "#4BB543",
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
  },
};
</script>
<style scoped>
/* Estilos responsivos adicionales */
@media (max-width: 768px) {
  .form-label {
    font-size: 0.8rem;
  }

  .form-control {
    font-size: 0.9rem;
  }

  .card-body {
    padding: 1rem !important;
  }
}
</style>
