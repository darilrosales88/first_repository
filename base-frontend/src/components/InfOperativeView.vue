<template>
  <div class="card border">
    <div class="card-header bg-light border-bottom">
      <h6 class="mb-0 text-dark fw-semibold">
        <i class="bi bi-clipboard-data me-2"></i>Registros de operaciones UFC
      </h6>
    </div>

    <div class="card-body p-3">
      <!-- Fila 1 - Fecha Actual -->
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

      <!-- Fila 2 - Plan Mensual y Diario -->
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

      <!-- Fila 3 - Vagones Cargados y Situados -->
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

      <!-- Fila 4 - Acumulados -->
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
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'InfOperativeView',
  props: {
    informeId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      formData: {
        fecha_actual: '',
        plan_mensual_total: 0,
        plan_diario_total_vagones_cargados: 0,
        real_total_vagones_cargados: 0,
        total_vagones_situados: 0,
        plan_total_acumulado_actual: 0,
        real_total_acumulado_actual: 0,
        provincia: null,
        creado_por: null,
        aprobado_por: null,
      }
    };
  },
  async mounted() {
    await this.cargarInforme();
  },
  methods: {
    async cargarInforme() {
      try {
        const response = await axios.get(`/ufc/informe-operativo/${this.informeId}/`);
        this.formData = response.data;
        
        // Formatear la fecha si es necesario
        if (this.formData.fecha_operacion) {
          this.formData.fecha_actual = this.formData.fecha_operacion.split('T')[0];
        }
      } catch (error) {
        console.error('Error al cargar el informe:', error);
      }
    }
  }
};
</script>
<template>
  <div class="card border">
    <div class="card-header bg-light border-bottom">
      <h5 class="mb-0 text-dark fw-semibold">
        <i class="bi bi-clipboard-data me-2"></i>Registros de operaciones UFC
      </h5>
    </div>

    <div class="card-body p-3">
      <!-- Fila 1 - Fecha Actual -->
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

      <!-- Fila 2 - Plan Mensual y Diario -->
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

      <!-- Fila 3 - Vagones Cargados y Situados -->
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

      <!-- Fila 4 - Acumulados -->
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
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'InfOperativeView',
  props: {
    informeId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      formData: {
        fecha_actual: '',
        plan_mensual_total: 0,
        plan_diario_total_vagones_cargados: 0,
        real_total_vagones_cargados: 0,
        total_vagones_situados: 0,
        plan_total_acumulado_actual: 0,
        real_total_acumulado_actual: 0,
        provincia: null,
        creado_por: null,
        aprobado_por: null,
      }
    };
  },
  async mounted() {
    await this.cargarInforme();
  },
  methods: {
    async cargarInforme() {
      try {
        const response = await axios.get(`/ufc/informe-operativo/${this.informeId}/`);
        this.formData = response.data;
        
        // Formatear la fecha si es necesario
        if (this.formData.fecha_operacion) {
          this.formData.fecha_actual = this.formData.fecha_operacion.split('T')[0];
        }
      } catch (error) {
        console.error('Error al cargar el informe:', error);
      }
    }
  }
};
</script>