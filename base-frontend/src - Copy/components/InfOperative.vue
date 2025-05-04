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
                <label for="fechaOperacion" class="form-label small fw-semibold text-secondary">
                  <i class="bi bi-calendar-date me-2 text-primary"></i>Fecha de Operación
                </label>
                <input 
                  type="date" 
                  class="form-control form-control-sm border-secondary" 
                  id="fechaOperacion" 
                  v-model="formData.fechaOperacion"
                  required
                >
              </div>
            </div>
            
            <div class="col-md-6">
              <div class="form-group">
                <label for="fechaActual" class="form-label small fw-semibold text-secondary">
                  <i class="bi bi-calendar-check me-2 text-primary"></i>Fecha Actual
                </label>
                <input 
                  type="date" 
                  class="form-control form-control-sm border-secondary" 
                  id="fechaActual" 
                  v-model="formData.fechaActual"
                  required
                >
              </div>
            </div>
          </div>
          
          <!-- Fila 2 -->
          <div class="row mb-3 g-2">
            <div class="col-md-6">
              <div class="form-group">
                <label for="planMensualTotal" class="form-label small fw-semibold text-secondary">
                  <i class="bi bi-calendar-month me-2 text-primary"></i>Plan Mensual Total
                </label>
                <input 
                  type="text" 
                  class="form-control form-control-sm border-secondary" 
                  id="planMensualTotal" 
                  v-model="formData.planMensualTotal"
                  required
                >
              </div>
            </div>
            
            <div class="col-md-6">
              <div class="form-group">
                <label for="planDiarioTotal" class="form-label small fw-semibold text-secondary">
                  <i class="bi bi-calendar-day me-2 text-primary"></i>Plan Diario Total Vagones Cargados
                </label>
                <input 
                  type="text" 
                  class="form-control form-control-sm border-secondary" 
                  id="planDiarioTotal" 
                  v-model="formData.planDiarioTotal"
                  required
                >
              </div>
            </div>
          </div>
          
          <!-- Fila 3 -->
          <div class="row mb-3 g-2">
            <div class="col-md-6">
              <div class="form-group">
                <label for="realTotalVagones" class="form-label small fw-semibold text-secondary">
                  <i class="bi bi-train-freight-front me-2 text-primary"></i>Real Total Vagones Cargados
                </label>
                <input 
                  type="text" 
                  class="form-control form-control-sm border-secondary" 
                  id="realTotalVagones" 
                  v-model="formData.realTotalVagones"
                  required
                >
              </div>
            </div>
            
            <div class="col-md-6">
              <div class="form-group">
                <label for="totalVagonesSituados" class="form-label small fw-semibold text-secondary">
                  <i class="bi bi-pin-map me-2 text-primary"></i>Total de Vagones Situados
                </label>
                <input 
                  type="text" 
                  class="form-control form-control-sm border-secondary" 
                  id="totalVagonesSituados" 
                  v-model="formData.totalVagonesSituados"
                  required
                >
              </div>
            </div>
          </div>
          
          <!-- Fila 4 -->
          <div class="row mb-4 g-2">
            <div class="col-md-6">
              <div class="form-group">
                <label for="planTotalAcumulado" class="form-label small fw-semibold text-secondary">
                  <i class="bi bi-graph-up me-2 text-primary"></i>Plan Total Acumulado Actual
                </label>
                <input 
                  type="text" 
                  class="form-control form-control-sm border-secondary" 
                  id="planTotalAcumulado" 
                  v-model="formData.planTotalAcumulado"
                  required
                >
              </div>
            </div>
            
            <div class="col-md-6">
              <div class="form-group">
                <label for="realTotalAcumulado" class="form-label small fw-semibold text-secondary">
                  <i class="bi bi-graph-up-arrow me-2 text-primary"></i>Real Total Acumulado Actual
                </label>
                <input 
                  type="text" 
                  class="form-control form-control-sm border-secondary" 
                  id="realTotalAcumulado" 
                  v-model="formData.realTotalAcumulado"
                  required
                >
              </div>
            </div>
          </div>
          
          <!-- Botones -->
          <div class="d-flex justify-content-end gap-2 mt-4">
            <button type="button" class="btn btn-sm btn-outline-secondary" @click="resetForm">
              <i class="bi bi-x-circle me-1"></i>Cancelar
            </button>
            <button type="submit" class="btn btn-sm btn-primary">
              <i class="bi bi-save me-1"></i>Guardar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InfOperative',
  data() {
    return {
      formData: {
        fechaOperacion: '',
        planMensualTotal: '',
        realTotalVagones: '',
        planTotalAcumulado: '',
        fechaActual: '',
        planDiarioTotal: '',
        totalVagonesSituados: '',
        realTotalAcumulado: ''
      }
    }
  },
  methods: {
    submitForm() {
      // Aquí iría la lógica para enviar los datos
      console.log('Datos del formulario:', this.formData);
      // Mostrar mensaje de éxito
      this.$swal.fire(
        '¡Éxito!',
        'El registro ha sido guardado correctamente.',
        'success'
      );
      this.resetForm();
    },
    resetForm() {
      this.formData = {
        fechaOperacion: '',
        planMensualTotal: '',
        realTotalVagones: '',
        planTotalAcumulado: '',
        fechaActual: '',
        planDiarioTotal: '',
        totalVagonesSituados: '',
        realTotalAcumulado: ''
      };
    }
  },
  mounted() {
    // Establecer fecha actual por defecto
    const today = new Date().toISOString().split('T')[0];
    this.formData.fechaActual = today;
    this.formData.fechaOperacion = today;
  }
}
</script>

<style scoped>
.card {
  border-radius: 0.5rem;
  border: 1px solid #e0e0e0;
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 2px solid #e0e0e0 !important;
  padding: 0.75rem 1.25rem;
}

.form-label {
  margin-bottom: 0.3rem;
  letter-spacing: 0.02rem;
}

.form-control {
  border-radius: 0.35rem;
  padding: 0.4rem 0.75rem;
  border: 1px solid #ced4da;
  font-size: 0.875rem;
  transition: border-color 0.15s ease-in-out;
}

.form-control:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.1);
}

.btn {
  border-radius: 0.35rem;
  padding: 0.4rem 0.9rem;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
  letter-spacing: 0.02rem;
}

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  transform: translateY(-1px);
}

.btn-outline-secondary:hover {
  background-color: #f8f9fa;
}

/* Mejor separación entre grupos de formulario */
.form-group {
  margin-bottom: 0.5rem;
}

/* Efecto sutil al pasar el ratón sobre inputs */
.form-control:hover {
  border-color: #adb5bd;
}

/* Responsive */
@media (max-width: 768px) {
  .card-body {
    padding: 1rem;
  }
  
  .btn {
    width: 100%;
  }
  
  .d-flex {
    flex-direction: column;
    gap: 0.5rem !important;
  }
}
</style>