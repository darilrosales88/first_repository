<template>
  <div class="ufc-header">
    <h6>Agregar Buque</h6>
  </div>
  <Navbar-Component />
  <div class="container py-3" style="margin-left: 20em; width: 70%">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-ship me-2"></i> Nuevo Buque
        </h5>
      </div>
      <div class="card-body p-3">
        <form @submit.prevent="guardarBuque">
          <div class="row">
            <!-- Columna Izquierda -->
            <div class="col-md-6">
              <!-- Campo: Nombre del Buque -->
              <div class="mb-3">
                <label for="buque_id" class="form-label small fw-semibold text-secondary"
                  >Buque*</label>
                <select
                  class="form-select form-select-sm border-secondary"
                  style="padding: 8px 12px"
                  v-model="nuevoBuque.buque_id"
                  id="buque_id"
                  name="buque_id"
                  required
                  @change="console.log('Buque seleccionado:', nuevoBuque.buque_id)"
                >
                  <option value="" disabled>Seleccione un buque</option>
                  <option
                    v-for="buque in listaBuques"
                    :key="buque.id"
                    :value="buque.id"
                  >
                    {{ buque.nombre_embarcacion || buque.nombre }}
                  </option>
                </select>
              </div>

              <!-- Campo: Puerto de Arribo -->
              <div class="mb-3">
                <label
                  for="puerto_id"
                  class="form-label small fw-semibold text-secondary"
                  >Puerto de Arribo*</label>
                <select
                  class="form-select form-select-sm border-secondary"
                  style="padding: 8px 12px"
                  v-model="nuevoBuque.puerto_id"
                  id="puerto_id"
                  name="puerto_id"
                  required
                >
                  <option value="" disabled>Seleccione un puerto</option>
                  <option
                    v-for="puerto in listaPuertos"
                    :key="puerto.id"
                    :value="puerto.id"
                  >
                    {{ puerto.nombre_puerto || puerto.nombre }}
                  </option>
                </select>
              </div>
            </div>

            <!-- Columna Derecha -->
            <div class="col-md-6">
              <!-- Campo: Fecha y Hora -->
              <div class="mb-3">
                <label
                  for="fecha_hora"
                  class="form-label small fw-semibold text-secondary"
                  >Fecha y Hora*</label>
                <input
                  type="datetime-local"
                  class="form-control form-control-sm border-secondary"
                  style="padding: 8px 12px"
                  v-model="nuevoBuque.fecha_hora"
                  id="fecha_hora"
                  name="fecha_hora"
                  required
                />
              </div>

              <!-- Campo: Nivel -->
              <div class="mb-3">
                <label
                  for="nivel"
                  class="form-label small fw-semibold text-secondary"
                  >Nivel*</label>
                <select
                  class="form-select form-select-sm border-secondary"
                  style="padding: 8px 12px"
                  v-model="nuevoBuque.nivel"
                  id="nivel"
                  name="nivel"
                  required
                >
                  <option value="" disabled>Seleccione un nivel</option>
                  <option value="1">1 - Nivel Básico</option>
                  <option value="2">2 - Nivel Intermedio</option>
                  <option value="3">3 - Nivel Alto</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Botones de acción -->
          <div class="modal-footer">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <button type="button" class="ufc-button secondary" @click="cancelar">
                <i class="bi bi-x-circle me-1"></i>Cancelar
              </button>
              <button type="submit" class="ufc-button primary">
                <i class="bi bi-check-circle me-1"></i>Guardar
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import NavbarComponent from "@/components/NavbarComponent.vue";
import Swal from "sweetalert2";
import axios from "axios";

export default {
  name: 'AgregarBuque',
  components: {
    NavbarComponent
  },
  data() {
    return {
      nuevoBuque: {
        buque_id: null,
        puerto_id: null,
        fecha_hora: new Date().toISOString().slice(0, 16),
        nivel: '1'
      },
      listaBuques: [],
      listaPuertos: [],
      loading: false
    }
  },
  async created() {
    await this.cargarBuques();
    await this.cargarPuertos();
  },
  methods: {
    async cargarBuques() {
      try {
        this.loading = true;
        const token = localStorage.getItem('token');
        
        if (!token) {
          this.mostrarError('No se encontró el token de autenticación');
          return;
        }
        
        const headers = { 
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        };

        const response = await axios.get('/api/embarcaciones/', { 
          headers,
          params: { limit: 1000 }
        });

        this.listaBuques = response.data.results || response.data || [];
        
        this.listaBuques = this.listaBuques.map(buque => ({
          id: buque.id,
          nombre: buque.nombre_embarcacion || buque.nombre || 'Buque sin nombre'
        }));

      } catch (error) {
        console.error('Error al cargar buques:', error);
        this.mostrarError('Error al cargar la lista de buques: ' + (error.response?.data?.detail || error.message));
      } finally {
        this.loading = false;
      }
    },
    
    async cargarPuertos() {
      try {
        this.loading = true;
        const token = localStorage.getItem('token');
        
        if (!token) {
          this.mostrarError('No se encontró el token de autenticación');
          return;
        }
        
        const headers = { 
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        };

        const response = await axios.get('/api/puertos/', { 
          headers,
          params: { limit: 1000 }
        });

        this.listaPuertos = response.data.results || response.data || [];
        
        this.listaPuertos = this.listaPuertos.map(puerto => ({
          id: puerto.id,
          nombre: puerto.nombre_puerto || puerto.nombre || 'Puerto sin nombre'
        }));

      } catch (error) {
        console.error('Error al cargar puertos:', error);
        this.mostrarError('Error al cargar la lista de puertos: ' + (error.response?.data?.detail || error.message));
      } finally {
        this.loading = false;
      }
    },
    
    async guardarBuque() {
      // Validar datos
      if (!this.nuevoBuque.buque_id || !this.nuevoBuque.puerto_id || !this.nuevoBuque.fecha_hora) {
        this.mostrarError('Todos los campos marcados con * son obligatorios');
        return;
      }
      
      try {
        const token = localStorage.getItem('token');
        const headers = {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        };

        // Crear payload con la estructura exacta que espera el backend
        const payload = {
          buque_id: this.nuevoBuque.buque_id,
          puerto_id: this.nuevoBuque.puerto_id,
          fecha_operacion: new Date().toISOString().split('T')[0], // Fecha actual
          fecha_hora: this.nuevoBuque.fecha_hora,
          nivel: parseInt(this.nuevoBuque.nivel)
        };

        console.log("Enviando payload:", payload);

        const response = await axios.post('/api/gemar/partes-pbip/', payload, { headers });
        
        this.mostrarExito('Buque agregado correctamente al parte PBIP');
        this.$router.push({ name: 'PartesPBIP' });
      } catch (error) {
        console.error('Error completo:', error);
        console.error('Respuesta del error:', error.response?.data);
        
        let errorMessage = 'Error al guardar el buque';
        if (error.response?.data) {
          // Mostrar todos los errores del backend
          errorMessage += ':\n';
          for (const [key, value] of Object.entries(error.response.data)) {
            errorMessage += `${key}: ${Array.isArray(value) ? value.join(', ') : value}\n`;
          }
        } else {
          errorMessage += ': ' + error.message;
        }
        
        this.mostrarError(errorMessage);
      }
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
        title: mensaje,
      });
    }
  }
}
</script>

<style scoped>
/* Estilos para el select personalizado de productos */
.ufc-custom-select {
  position: relative;
  width: 100%;
  cursor: pointer;
}

.ufc-select-display {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.85rem;
  background-color: white;
  min-height: 36px;
  display: flex;
  align-items: center;
  border-color: rgba(
    var(--bs-secondary-rgb),
    var(--bs-border-opacity)
  ) !important;
}

.ufc-select-arrow {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  transition: transform 0.2s;
}

.ufc-custom-select.open .ufc-select-arrow {
  transform: translateY(-50%) rotate(180deg);
}

.ufc-productos-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  max-height: 300px;
  overflow-y: auto;
  background: white;
  border: 1px solid #ddd;
  border-radius: 0 0 6px 6px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 10;
  margin-top: 2px;
}

.ufc-productos-search-container {
  padding: 8px;
  border-bottom: 1px solid #eee;
  background: #f8f9fa;
}

.ufc-productos-search {
  width: 100%;
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.85rem;
}

.ufc-productos-search:focus {
  outline: none;
  border-color: #002a68;
}

.ufc-productos-options {
  max-height: 250px;
  overflow-y: auto;
}

.ufc-producto-option {
  padding: 8px 12px;
  font-size: 0.85rem;
  border-bottom: 1px solid #f0f0f0;
}

.ufc-producto-option:hover {
  background-color: #f5f5f5;
}
/* Estilos para el grid dentro del modal */

/* Ajustes para los botones del modal */
.ufc-modal-body .ufc-form-actions {
  border-top: 1px solid #eee;
  padding-top: 15px;
  margin-top: 0;
}

.ufc-producto-option.selected {
  background-color: #002a68;
  color: white;
}

/* Estilo para el botón de agregar */
.ufc-add-button {
  margin-left: 8px;
}

.ufc-select[multiple] {
  height: auto;
  min-height: 100px;
  padding: 8px;
}

.ufc-select[multiple] option {
  padding: 6px 8px;
  margin: 2px 0;
  border-radius: 4px;
}

.ufc-select[multiple] option:checked {
  background-color: #002a68;
  color: white;
}

.ufc-selected-products {
  font-size: 0.8rem;
  color: #666;
  margin-top: 5px;
}

.ufc-form-container {
  font-family: "Segoe UI", Roboto, -apple-system, sans-serif;
  color: #333;
  padding-bottom: 20px;
}

.ufc-header {
  background-color: #002a68;
  color: white;
  text-align: right;
  padding: 10px 15px;
  margin-bottom: 20px;
}

.ufc-header h6 {
  margin: 0;
  font-size: 1rem;
  font-weight: 500;
}

.ufc-form-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 15px;
}

.ufc-form-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.ufc-form-title {
  color: #002a68;
  font-size: 1.3rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}

.ufc-form-title i {
  font-size: 1.4rem;
}

.ufc-form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

@media (max-width: 768px) {
  .ufc-form-grid {
    grid-template-columns: 1fr;
  }
}

.ufc-input-group {
  margin-bottom: 15px;
}

.ufc-input-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 0.85rem;
  font-weight: 500;
  color: #444;
}

.ufc-input-group .required {
  color: #e74c3c;
}

.ufc-select,
.ufc-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.85rem;
  transition: all 0.2s;
  background-color: white;
}

.ufc-select:focus,
.ufc-input:focus {
  border-color: #002a68;
  box-shadow: 0 0 0 3px rgba(0, 42, 104, 0.1);
  outline: none;
}

.ufc-textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  resize: vertical;
  min-height: 70px;
  font-family: inherit;
  font-size: 0.85rem;
}

.ufc-textarea:focus {
  border-color: #002a68;
  box-shadow: 0 0 0 3px rgba(0, 42, 104, 0.1);
  outline: none;
}

.ufc-input-with-action {
  display: flex;
  gap: 8px;
}

.ufc-add-button {
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  width: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #002a68;
  transition: all 0.2s;
}

.ufc-add-button:hover {
  background: #e9ecef;
  color: #001a3d;
}

.ufc-add-button i {
  font-size: 1.1rem;
}

.ufc-disabled {
  font-size: 0.8rem;
  color: #777;
  padding: 8px 0;
}

/* Estilo especial para el campo por situar */
.ufc-por-situar-container {
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 6px;
  overflow: hidden;
  border-color: rgba(
    var(--bs-secondary-rgb),
    var(--bs-border-opacity)
  ) !important;
}

.ufc-por-situar-input {
  flex: 1;
  border: none;
  padding: 8px 12px;
  font-size: 0.85rem;
  min-width: 0;
}

.ufc-por-situar-suffix {
  background: #f8f9fa;
  padding: 8px 12px;
  font-size: 0.8rem;
  color: #666;
  border-left: 1px solid #ddd;
}

/* Botones de acción */
.ufc-form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.ufc-button {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 1 rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  display: flex;
  align-items: center;
  gap: 6px;
}

.ufc-button.primary {
  background: #002a68;
  color: white;
}

.ufc-button.primary:hover {
  background: #003d8f;
}

.ufc-button.secondary {
  background: #f1513f;
  color: white;
}

.ufc-button.secondary:hover {
  background: rgb(228, 56, 37);
}

.create-button {
  text-decoration: none;
  border: none;
  color: green;
  margin-left: 940px;
}

button {
  margin-left: 10px;
  padding: 5px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
}

.btn-outline-danger:hover {
  color: #fff;
}

button[type="button"] {
  background-color: #007bff;
  color: white;
}

button[type="submit"] {
  margin-left: 15px;
  background-color: #007bff;
  color: white;
}

/* Estilos para selects */
.ufc-select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 12px;
}

/* Estilos para el modal */
.ufc-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.ufc-modal-container {
  background: white;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow: auto;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
  animation: modalFadeIn 0.3s ease-out;
}

.ufc-modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #002a68;
  color: white;
  border-radius: 10px 10px 0 0;
}

.ufc-modal-header h3 {
  margin: 0;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.ufc-modal-close {
  background: transparent;
  border: none;
  color: white;
  font-size: 1.3rem;
  cursor: pointer;
  padding: 5px;
  transition: all 0.2s;
}

.ufc-modal-close:hover {
  color: #ccc;
}

.ufc-modal-body {
  padding: 20px;
}

.ufc-validation-message {
  padding: 10px;
  border-radius: 6px;
  font-size: 0.85rem;
  margin-top: 10px;
}

.ufc-validation-message.warning {
  background-color: #fff3cd;
  color: #856404;
  border-left: 4px solid #ffeeba;
}

.ufc-validation-message.success {
  background-color: #d4edda;
  color: #155724;
  border-left: 4px solid #c3e6cb;
}

.ufc-validation-message.error {
  background-color: #f8d7da;
  color: #721c24;
  border-left: 4px solid #f5c6cb;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.form-select:focus {
  border-color: #dc3545;
  box-shadow: 0 0 0 0.25rem rgba(220, 53, 69, 0.25);
  outline: 0;
}
.form-control:focus {
  border-color: #dc3545;
  box-shadow: 0 0 0 0.25rem rgba(220, 53, 69, 0.25);
  outline: 0;
}
</style>