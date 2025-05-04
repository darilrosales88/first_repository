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
import Swal from 'sweetalert2';
import axios from 'axios';

export default {
  name: 'InfOperative',
  data() {
    return {
      formData: {
        fechaOperacion: '',
        fechaActual: '',

      },
      errores: '',
      isLoading: false
    }
  },
  methods: {
    validateForm() {
      this.errores = '';
      let isValid = true;


      // Validación de fechas
      const today = new Date().toISOString().split('T')[0];
      if (this.formData.fechaActual !== today) {
        this.errores += 'La fecha actual debe ser la de hoy.<br>';
        isValid = false;
      }

      if (new Date(this.formData.fechaOperacion) > new Date()) {
        this.errores += 'La fecha de operación no puede ser futura.<br>';
        isValid = false;
      }

      return isValid;
    },

    getFieldLabel(field) {
      const labels = {
        fechaOperacion: 'Fecha de Operación',        
        fechaActual: 'Fecha Actual',
      };
      return labels[field] || field;
    },

    async submitForm() {
      if (!this.validateForm()) {
        await Swal.fire({
          title: 'Errores en el formulario',
          html: this.errores,
          icon: 'error',
          confirmButtonText: 'Entendido'
        });
        return;
      }

      this.isLoading = true;
      try {
        const dataToSend = {
          fecha_operacion: this.formData.fechaOperacion,
          fecha_actual: this.formData.fechaActual,
          plan_mensual_total: this.formData.planMensualTotal,
          plan_diario_total_vagones_cargados: this.formData.planDiarioTotal,
          real_total_vagones_cargados: this.formData.realTotalVagones,
          total_vagones_situados: this.formData.totalVagonesSituados,
          plan_total_acumulado_actual: this.formData.planTotalAcumulado,
          real_total_acumulado_actual: this.formData.realTotalAcumulado
        };
        console.log("INfomracion a enviarrrrrrrrrrrrrr: ",dataToSend)

        const response = await axios.post('/ufc/informe-operativo/', dataToSend);

        await Swal.fire({
          title: '¡Éxito!',
          text: 'Los datos operativos se han guardado correctamente.',
          icon: 'success',
          confirmButtonText: 'Aceptar'
        });
        this.resetForm();
      } catch (error) {
        console.error('Error al guardar operación:', error);
        
        let errorMessage = 'Ocurrió un error al guardar los datos.';
        if (error.response?.data) {
          errorMessage = Object.values(error.response.data).join('<br>');
        }
        
        await Swal.fire({
          title: 'Error',
          html: errorMessage,
          icon: 'error',
          confirmButtonText: 'Entendido'
        });
      } finally {
        this.isLoading = false;
      }
    },

    async getRelatedData() {
      try {
        // Obtener datos de otros componentes/API endpoints
        const [
          vagonesproductosRes,
          vagonesRes,
          registrosRes,
          productosRes,
          situadosRes,
          enTrenesRes,
          arrastresRes,
          rotacionesRes
        ] = await Promise.all([
          axios.get('/ufc/vagones-productos/'),
          axios.get('/ufc/vagones-cargados-descargados/'),
          axios.get('/ufc/registro-vagones-cargados/'),
          axios.get('/ufc/productos-ufc/'),
          axios.get('/ufc/situados/'),
          axios.get('/ufc/en-trenes/'),
          axios.get('/ufc/pendiente-arrastre/'),
          axios.get('/ufc/rotaciones/')
        ]);

        return {
          vagones_y_productos: vagonesproductosRes.data,
          vagones_cargados_descargados: vagonesRes.data,
          registros_vagones: registrosRes.data,
          productos: productosRes.data,
          situados_carga_descarga: situadosRes.data,
          en_trenes_list: enTrenesRes.data,
          arrastres_list: arrastresRes.data,
          rotaciones_vagones: rotacionesRes.data
        };
      } catch (error) {
        console.error('Error obteniendo datos relacionados:', error);
        return {};
      }
    },

    confirmCancel() {
      Swal.fire({
        title: '¿Cancelar operación?',
        text: '¿Está seguro de que desea cancelar? Los datos no guardados se perderán.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, cancelar',
        cancelButtonText: 'No, continuar'
      }).then((result) => {
        if (result.isConfirmed) {
          this.resetForm();
          this.$router.back();
        }
      });
    },

    resetForm() {
      const today = new Date().toISOString().split('T')[0];
      this.formData = {
        fechaOperacion: today,       
        fechaActual: today,

      };
    }
  },
  mounted() {
    const today = new Date().toISOString().split('T')[0];
    this.formData.fechaActual = today;
    this.formData.fechaOperacion = today;
  }
}
</script>