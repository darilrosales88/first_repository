<template>
  <div>
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h6 class="mb-0 text-dark fw-semibold">
          Editar Parte PBIP
        </h6>
      </div>
      <div class="card-body p-3">
        <form @submit.prevent="guardarCambios">
          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">Buque*</label>
              <select v-model="buque.buque_id" class="form-select" required>
                <option value="">Seleccione un buque...</option>
                <option 
                  v-for="buque in listaBuques" 
                  :value="buque.id"
                  :key="buque.id"
                >
                  {{ buque.nombre }}
                </option>
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label">Puerto de Arribo*</label>
              <select v-model="buque.puerto_id" class="form-select" required>
                <option value="">Seleccione un puerto...</option>
                <option 
                  v-for="puerto in listaPuertos" 
                  :value="puerto.id"
                  :key="puerto.id"
                >
                  {{ puerto.nombre }}
                </option>
              </select>
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">Fecha y Hora*</label>
              <input 
                type="datetime-local" 
                v-model="buque.fecha_hora" 
                class="form-control"
                required
              >
            </div>
            <div class="col-md-6">
              <label class="form-label">Nivel de Protección*</label>
              <select v-model="buque.nivel" class="form-select" required>
                <option value="1">Nivel 1</option>
                <option value="2">Nivel 2</option>
                <option value="3">Nivel 3</option>
              </select>
            </div>
          </div>

          <div class="d-flex justify-content-center gap-3 mt-4">
            <button type="submit" class="btn btn-primary">
              <i class="bi bi-save me-1"></i> Guardar Cambios
            </button>
            <button 
              type="button" 
              @click="cancelar" 
              class="btn btn-outline-secondary"
            >
              <i class="bi bi-x me-1"></i> Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";

export default {
  name: 'EditarPartePBIP',
  data() {
    return {
      buque: {
        buque_id: null,
        puerto_id: null,
        fecha_hora: '',
        nivel: '1'
      },
      listaBuques: [],
      listaPuertos: []
    }
  },
  created() {
    this.cargarDatosIniciales();
  },
  methods: {
    cargarDatosIniciales() {
      try {
        // Recuperar datos del buque a editar
        const buqueData = JSON.parse(this.$route.params.buqueData || '{}');
        this.buque = {
          buque_id: buqueData.buque_id,
          puerto_id: buqueData.puerto_id,
          fecha_hora: buqueData.fecha_hora,
          nivel: buqueData.nivel || '1'
        };
        
        // Recuperar listas de buques y puertos
        this.listaBuques = JSON.parse(this.$route.params.listaBuques || '[]');
        this.listaPuertos = JSON.parse(this.$route.params.listaPuertos || '[]');
        
      } catch (error) {
        console.error('Error al cargar datos:', error);
        this.mostrarError('Error al cargar los datos del buque');
        this.$router.go(-1);
      }
    },
    
    guardarCambios() {
      // Validar formulario
      if (!this.buque.buque_id || !this.buque.puerto_id || !this.buque.fecha_hora) {
        this.mostrarError('Todos los campos marcados con * son requeridos');
        return;
      }
      
      // Emitir evento con los cambios
      this.$emit('buque-editado', this.buque);
      
      // Mostrar mensaje de éxito y regresar
      this.mostrarExito('Cambios guardados correctamente');
      this.$router.go(-1);
    },
    
    cancelar() {
      this.$router.go(-1);
    },
    
    mostrarError(mensaje) {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: mensaje,
        confirmButtonText: 'Aceptar'
      });
    },
    
    mostrarExito(mensaje) {
      Swal.fire({
        icon: 'success',
        title: 'Éxito',
        text: mensaje,
        confirmButtonText: 'Aceptar'
      });
    }
  }
}
</script>

<style scoped>
/* Estilos consistentes con el componente principal */
.card {
  border-radius: 0.25rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.form-control, .form-select {
  margin-bottom: 1rem;
}

.btn {
  min-width: 120px;
}
</style>