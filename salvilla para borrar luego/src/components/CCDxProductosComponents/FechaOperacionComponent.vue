<template>
    <div class="container py-3">
      <div class="card border">
        <div class="card-header bg-light border-bottom">
          <h6 class="mb-0 text-dark fw-semibold">
            <i class="bi bi-clipboard-data me-2"></i>UFC - CCD por producto
          </h6>
        </div>

        <div class="card-body p-3">
          <form @submit.prevent="submitForm">
            <div class="row mb-3 g-2">
              <div class="col-md-6">
                <div class="form-group">
                  <label for="fechaActual" class="form-label small fw-semibold text-secondary">
                    <i class="bi bi-calendar-check me-2 text-primary"></i>Fecha Actual
                  </label>
                  <input
                    type="date"
                    class="form-control form-control-sm border-secondary"
                    id="fechaActual"
                    v-model="formData.fecha_actual"
                    required/>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label for="fechaOperacion" class="form-label small fw-semibold text-secondary">
                    <i class="bi bi-calendar-check me-2 text-primary"></i>Fecha Operación
                  </label>
                  <input
                    type="date"
                    class="form-control form-control-sm border-secondary"
                    id="fechaOperacion"
                    v-model="formData.fecha_operacion"
                    required/>
                </div>
              </div>
            </div>

            <div class="d-flex justify-content-end gap-2 mt-4">
              <button type="submit" class="btn btn-primary">
                <i class="bi bi-save me-2"></i>Crear informe operativo
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
  name: "FechaOperacionComponent",

  data() {
    const now = new Date();
    const offset = now.getTimezoneOffset() * 60000; // offset en milisegundos
    const localISOTime = new Date(now - offset).toISOString().split("T")[0];
    return {
        formData: {
            fecha_actual: localISOTime,
            fecha_operacion: localISOTime,
        },
    };
  },

  async mounted() {},

  beforeUnmount() {},

  methods: {},
};
</script>
<style>

</style>