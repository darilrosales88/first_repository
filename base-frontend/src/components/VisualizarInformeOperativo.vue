<template>
  <div class="container py-3">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-eye me-2"></i>Visualizar Informe Operativo
        </h5>
      </div>

      <div class="card-body p-3">
        <!-- Mostrar datos del informe -->
        <div class="row mb-3 g-2">
          <div class="col-md-6">
            <div class="form-group">
              <label class="form-label small fw-semibold text-secondary">
                <i class="bi bi-calendar-check me-2 text-primary"></i>Fecha Actual
              </label>
              <input
                type="date"
                class="form-control form-control-sm border-secondary"
                :value="formData.fecha_actual"
                readonly
              />
            </div>
          </div>
        </div>

        <div class="row mb-3 g-2">
          <div class="col-md-6">
            <div class="form-group">
              <label class="form-label small fw-semibold text-secondary">
                <i class="bi bi-calendar-month me-2 text-primary"></i>Plan Mensual Total
              </label>
              <input
                type="number"
                class="form-control form-control-sm border-secondary"
                :value="formData.plan_mensual_total"
                readonly
              />
            </div>
          </div>

          <div class="col-md-6">
            <div class="form-group">
              <label class="form-label small fw-semibold text-secondary">
                <i class="bi bi-calendar-day me-2 text-primary"></i>Plan Diario Total Vagones Cargados
              </label>
              <input
                type="number"
                class="form-control form-control-sm border-secondary"
                :value="formData.plan_diario_total_vagones_cargados"
                readonly
              />
            </div>
          </div>
        </div>

        <div class="row mb-3 g-2">
          <div class="col-md-6">
            <div class="form-group">
              <label class="form-label small fw-semibold text-secondary">
                <i class="bi bi-train-freight-front me-2 text-primary"></i>Real Total Vagones Cargados
              </label>
              <input
                type="number"
                class="form-control form-control-sm border-secondary"
                :value="formData.real_total_vagones_cargados"
                readonly
              />
            </div>
          </div>

          <div class="col-md-6">
            <div class="form-group">
              <label class="form-label small fw-semibold text-secondary">
                <i class="bi bi-pin-map me-2 text-primary"></i>Total de Vagones Situados
              </label>
              <input
                type="number"
                class="form-control form-control-sm border-secondary"
                :value="formData.total_vagones_situados"
                readonly
              />
            </div>
          </div>
        </div>

        <div class="row mb-4 g-2">
          <div class="col-md-6">
            <div class="form-group">
              <label class="form-label small fw-semibold text-secondary">
                <i class="bi bi-graph-up me-2 text-primary"></i>Plan Total Acumulado Actual
              </label>
              <input
                type="number"
                class="form-control form-control-sm border-secondary"
                :value="formData.plan_total_acumulado_actual"
                readonly
              />
            </div>
          </div>

          <div class="col-md-6">
            <div class="form-group">
              <label class="form-label small fw-semibold text-secondary">
                <i class="bi bi-graph-up-arrow me-2 text-primary"></i>Real Total Acumulado Actual
              </label>
              <input
                type="number"
                class="form-control form-control-sm border-secondary"
                :value="formData.real_total_acumulado_actual"
                readonly
              />
            </div>
          </div>
        </div>

        <div class="row mb-4 g-2">
          <div class="col-md-6">
            <div class="form-group">
              <label class="form-label small fw-semibold text-secondary">
                <i class="bi bi-person me-2 text-primary"></i>Creado por
              </label>
              <input
                type="text"
                class="form-control form-control-sm border-secondary"
                :value="formData.creado_por_detalle ? formData.creado_por_detalle.username : ''"
                readonly
              />
            </div>
          </div>
          <div class="col-md-6">
            <div class="form-group">
              <label class="form-label small fw-semibold text-secondary">
                <i class="bi bi-check-circle me-2 text-primary"></i>Estado
              </label>
              <input
                type="text"
                class="form-control form-control-sm border-secondary"
                :value="formData.estado_parte"
                readonly
                :class="{
                  'text-success': formData.estado_parte === 'Aprobado',
                  'text-danger': formData.estado_parte === 'Rechazado',
                  'text-primary': formData.estado_parte === 'Creado'
                }"
              />
            </div>
          </div>
        </div>

        <!-- Botones de aprobación/rechazo -->
        <div class="d-flex justify-content-end gap-2 mt-4" v-if="formData.estado_parte === 'Creado'">
          <button
            type="button"
            class="btn btn-sm btn-danger"
            @click="rechazarInforme"
            :disabled="isLoading"
          >
            <i class="bi bi-x-circle me-1"></i>Rechazar
          </button>
          <button
            type="button"
            class="btn btn-sm btn-success"
            @click="aprobarInforme"
            :disabled="isLoading"
          >
            <i class="bi bi-check-circle me-1"></i>Aprobar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";

export default {
  name: "VisualizarInformeOperativo",
  data() {
    return {
      formData: {
        fecha_actual: "",
        plan_mensual_total: 0,
        plan_diario_total_vagones_cargados: 0,
        real_total_vagones_cargados: 0,
        total_vagones_situados: 0,
        plan_total_acumulado_actual: 0,
        real_total_acumulado_actual: 0,
        estado_parte: "Creado",
        creado_por_detalle: null,
        aprobado_por_detalle: null,
      },
      isLoading: false,
      informeId: null,
    };
  },
  async mounted() {
    this.informeId = this.$route.params.id;
    await this.cargarInforme();
  },
  methods: {
    async cargarInforme() {
      try {
        this.isLoading = true;
        const response = await axios.get(`/ufc/informe-operativo/${this.informeId}/`);
        this.formData = response.data;
        
        // Formatear la fecha para mostrarla correctamente
        if (this.formData.fecha_operacion) {
          const fecha = new Date(this.formData.fecha_operacion);
          const fechaFormateada = `${fecha.getFullYear()}-${String(fecha.getMonth() + 1).padStart(2, '0')}-${String(fecha.getDate()).padStart(2, '0')}`;
          this.formData.fecha_actual = fechaFormateada;
        }
      } catch (error) {
        console.error("Error al cargar el informe:", error);
        Swal.fire("Error", "No se pudo cargar el informe operativo", "error");
        this.$router.go(-1); // Regresar a la página anterior
      } finally {
        this.isLoading = false;
      }
    },
    
    async aprobarInforme() {
      await this.cambiarEstado("Aprobado");
    },
    
    async rechazarInforme() {
      await this.cambiarEstado("Rechazado");
    },
    
    async cambiarEstado(nuevoEstado) {
      try {
        const confirmText = nuevoEstado === "Aprobado" 
          ? "¿Está seguro que desea aprobar este informe?" 
          : "¿Está seguro que desea rechazar este informe?";
        
        const result = await Swal.fire({
          title: "Confirmar acción",
          text: confirmText,
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: nuevoEstado === "Aprobado" ? "#28a745" : "#dc3545",
          cancelButtonColor: "#6c757d",
          confirmButtonText: nuevoEstado === "Aprobado" ? "Sí, aprobar" : "Sí, rechazar",
          cancelButtonText: "Cancelar",
        });
        
        if (result.isConfirmed) {
          this.isLoading = true;
          
          // Obtener el ID del usuario actual
          const userId = localStorage.getItem("userid");
          
          // Actualizar el estado y quien lo aprobó/rechazó
          const response = await axios.patch(
            `/ufc/informe-operativo/${this.informeId}/`,
            {
              estado_parte: nuevoEstado,
              aprobado_por: userId
            }
          );
          
          this.formData.estado_parte = nuevoEstado;
          this.formData.aprobado_por_detalle = response.data.aprobado_por_detalle;
          
          Swal.fire(
            "¡Éxito!",
            `El informe ha sido ${nuevoEstado.toLowerCase()} correctamente.`,
            "success"
          );
          
          // Opcional: Redirigir después de 2 segundos
          setTimeout(() => {
            this.$router.go(-1); // Regresar a la página anterior
          }, 2000);
        }
      } catch (error) {
        console.error(`Error al ${nuevoEstado.toLowerCase()} el informe:`, error);
        Swal.fire(
          "Error",
          `Ocurrió un error al ${nuevoEstado.toLowerCase()} el informe.`,
          "error"
        );
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.text-success {
  color: #28a745 !important;
}
.text-danger {
  color: #dc3545 !important;
}
.text-primary {
  color: #007bff !important;
}
</style>