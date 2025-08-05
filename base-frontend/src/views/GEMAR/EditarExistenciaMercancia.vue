<template>
  <div>
    <div class="ufc-header">
      <h6>Editar Existencia de Mercancía</h6>
    </div>
    <Navbar-Component />
    <div class="container py-3" style="margin-left: 20em; width: 70%">
      <div class="card border">
        <div class="card-header bg-light border-bottom">
          <h5 class="mb-0 text-dark fw-semibold">
            <i class="bi bi-box-seam me-2"></i> Editar Existencia de Mercancía
          </h5>
        </div>
        <div class="card-body p-3">
          <form @submit.prevent="guardarCambios">
            <div class="row">
              <!-- Columna Izquierda -->
              <div class="col-md-6">
                <!-- Campo: Terminal -->
                <div class="mb-3">
                  <label for="terminal" class="form-label small fw-semibold text-secondary">
                    Terminal*
                  </label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="existencia.terminal_id"
                    required
                    :disabled="loading"
                  >
                    <option value="" disabled>Seleccione una terminal</option>
                    <option
                      v-for="terminal in terminales"
                      :key="terminal.id"
                      :value="terminal.id"
                    >
                      {{ terminal.nombre_terminal }}
                    </option>
                  </select>
                </div>

                <!-- Campo: Tipo -->
                <div class="mb-3">
                  <label for="tipo" class="form-label small fw-semibold text-secondary">
                    Tipo*
                  </label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="existencia.tipo"
                    required
                    :disabled="loading"
                  >
                    <option value="" disabled>Seleccione un tipo</option>
                    <option value="1">Importación</option>
                    <option value="2">Exportación</option>
                  </select>
                </div>

                <!-- Campo: Tipo de Producto -->
                <div class="mb-3">
                  <label for="tipo_producto" class="form-label small fw-semibold text-secondary">
                    Tipo de Producto*
                  </label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="existencia.tipo_producto"
                    required
                    @change="actualizarCamposPorTipo"
                    :disabled="loading"
                  >
                    <option value="" disabled>Seleccione un tipo</option>
                    <option value="1">Producto</option>
                    <option value="2">Contenedor</option>
                  </select>
                </div>

                <!-- Campo: Producto -->
                <div class="mb-3">
                  <label for="producto" class="form-label small fw-semibold text-secondary">
                    Producto*
                  </label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="existencia.producto_id"
                    required
                    :disabled="loading"
                  >
                    <option value="" disabled>Seleccione un producto</option>
                    <option
                      v-for="producto in productos"
                      :key="producto.id"
                      :value="producto.id"
                    >
                      {{ producto.nombre_producto }}
                    </option>
                  </select>
                </div>
              </div>

              <!-- Columna Derecha -->
              <div class="col-md-6">
                <!-- Campo: Tipo de Embalaje (condicional) -->
                <div class="mb-3" v-if="existencia.tipo_producto == 1">
                  <label for="tipo_embalaje" class="form-label small fw-semibold text-secondary">
                    Tipo de Embalaje
                  </label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="existencia.tipo_embalaje_id"
                    :disabled="loading"
                  >
                    <option value="" disabled>Seleccione un tipo de embalaje</option>
                    <option
                      v-for="embalaje in tiposEmbalaje"
                      :key="embalaje.id"
                      :value="embalaje.id"
                    >
                      {{ embalaje.nombre_tipo_embalaje }}
                    </option>
                  </select>
                </div>

                <!-- Campo: Estado del Contenedor (condicional) -->
                <div class="mb-3" v-if="existencia.tipo_producto == 2">
                  <label for="estado" class="form-label small fw-semibold text-secondary">
                    Estado del Contenedor*
                  </label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="existencia.estado"
                    required
                    :disabled="loading"
                  >
                    <option value="" disabled>Seleccione un estado</option>
                    <option value="1">Vacío</option>
                    <option value="2">Lleno</option>
                  </select>
                </div>

                <!-- Campo: Contenido (condicional) -->
                <div class="mb-3" v-if="existencia.tipo_producto == 2 && existencia.estado == 2">
                  <label for="contiene" class="form-label small fw-semibold text-secondary">
                    Contenido*
                  </label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="existencia.contiene"
                    required
                    :disabled="loading"
                  >
                    <option value="" disabled>Seleccione contenido</option>
                    <option value="1">Alimentos</option>
                    <option value="2">Productos varios</option>
                  </select>
                </div>

                <!-- Campo: Unidad de Medida -->
                <div class="mb-3">
                  <label for="unidad_medida" class="form-label small fw-semibold text-secondary">
                    Unidad de Medida*
                  </label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="existencia.unidad_medida_id"
                    required
                    :disabled="loading"
                  >
                    <option value="" disabled>Seleccione una unidad</option>
                    <option
                      v-for="unidad in unidadesMedida"
                      :key="unidad.id"
                      :value="unidad.id"
                    >
                      {{ unidad.unidad_medida }} ({{ unidad.simbolo }})
                    </option>
                  </select>
                </div>

                <!-- Campo: Existencia -->
                <div class="mb-3">
                  <label for="existencia" class="form-label small fw-semibold text-secondary">
                    Existencia*
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    class="form-control form-control-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="existencia.existencia"
                    required
                    :disabled="loading"
                  />
                </div>
              </div>
            </div>

            <!-- Botones de acción -->
            <div class="modal-footer">
              <div class="d-flex justify-content-between align-items-center mb-4">
                <button type="button" class="ufc-button secondary" @click="confirmCancel" :disabled="loading">
                  <i class="bi bi-x-circle me-1"></i>Cancelar
                </button>
                <button type="submit" class="ufc-button primary" :disabled="loading">
                  <i class="bi bi-check-circle me-1"></i>Guardar Cambios
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: 'EditarExistenciaMercancia',
  components: {
    NavbarComponent
  },
  data() {
    return {
      existencia: {
        terminal_id: '',
        tipo: '',
        tipo_producto: '',
        producto_id: '',
        tipo_embalaje_id: null,
        unidad_medida_id: '',
        estado: null,
        contiene: null,
        existencia: 0
      },
      terminales: [],
      productos: [],
      tiposEmbalaje: [],
      unidadesMedida: [],
      loading: false
    }
  },
  async created() {
    await this.cargarDatosIniciales();
    await this.cargarExistencia();
  },
  methods: {
    async cargarDatosIniciales() {
      try {
        this.loading = true;
        const token = localStorage.getItem('token');
        
        // Cargar terminales
        const terminalesResponse = await axios.get('/api/terminales/', {
          headers: { 'Authorization': `Token ${token}` }
        });
        this.terminales = terminalesResponse.data.results || [];
        
        // Cargar productos
        const productosResponse = await axios.get('/api/productos/', {
          headers: { 'Authorization': `Token ${token}` }
        });
        this.productos = productosResponse.data.results || [];
        
        // Cargar tipos de embalaje
        const embalajesResponse = await axios.get('/api/embalajes/', {
          headers: { 'Authorization': `Token ${token}` }
        });
        this.tiposEmbalaje = embalajesResponse.data.results || [];
        
        // Cargar unidades de medida
        const unidadesResponse = await axios.get('/api/unidades_medida/', {
          headers: { 'Authorization': `Token ${token}` }
        });
        this.unidadesMedida = unidadesResponse.data.results || [];
        
      } catch (error) {
        console.error('Error al cargar datos iniciales:', error);
        this.mostrarError('Error al cargar los datos iniciales');
      } finally {
        this.loading = false;
      }
    },
    
    async cargarExistencia() {
      try {
        this.loading = true;
        const existenciaId = this.$route.params.id;
        if (!existenciaId) {
          this.mostrarError('ID de existencia no especificado');
          return;
        }
        
        const token = localStorage.getItem('token');
        const response = await axios.get(`/api/gemar/existencias-mercancia/${existenciaId}/`, {
          headers: { 'Authorization': `Token ${token}` }
        });
        
        if (response.data) {
          this.existencia = {
            fecha_operacion: response.data.fecha_operacion,  // Añadimos esta línea
            terminal_id: response.data.terminal?.id || '',
            tipo: response.data.tipo.toString(),
            tipo_producto: response.data.tipo_producto.toString(),
            producto_id: response.data.producto?.id || '',
            tipo_embalaje_id: response.data.tipo_embalaje?.id || null,
            unidad_medida_id: response.data.unidad_medida?.id || '',
            estado: response.data.estado ? response.data.estado.toString() : null,
            contiene: response.data.contiene ? response.data.contiene.toString() : null,
            existencia: response.data.existencia || 0
          };
        }
      } catch (error) {
        console.error('Error al cargar la existencia:', error);
        this.mostrarError('Error al cargar los datos de la existencia');
      } finally {
        this.loading = false;
      }
    },
    
    actualizarCamposPorTipo() {
      if (this.existencia.tipo_producto == 1) { // Producto
        this.existencia.estado = null;
        this.existencia.contiene = null;
      } else { // Contenedor
        this.existencia.tipo_embalaje_id = null;
      }
    },
    
    async guardarCambios() {
      try {
        this.loading = true;
        const token = localStorage.getItem('token');
        const existenciaId = this.$route.params.id;
        
        // Validación básica
        if (!this.existencia.terminal_id || !this.existencia.tipo || 
            !this.existencia.tipo_producto || !this.existencia.producto_id || 
            !this.existencia.unidad_medida_id || this.existencia.existencia < 0) {
          this.mostrarError('Los campos marcados con * son obligatorios y la existencia no puede ser negativa');
          return;
        }
        
        // Validaciones específicas para contenedores
        if (this.existencia.tipo_producto == 2) {
          if (!this.existencia.estado) {
            this.mostrarError('Para contenedores debe especificar el estado');
            return;
          }
          if (this.existencia.estado == 2 && !this.existencia.contiene) {
            this.mostrarError('Para contenedores llenos debe especificar qué contienen');
            return;
          }
        }
        
        // Preparar los datos para enviar
        const datosParaEnviar = {
          fecha_operacion: this.existencia.fecha_operacion,  // Añadimos este campo
          terminal_id: this.existencia.terminal_id,
          tipo: parseInt(this.existencia.tipo),
          tipo_producto: parseInt(this.existencia.tipo_producto),
          producto_id: this.existencia.producto_id,
          tipo_embalaje_id: this.existencia.tipo_embalaje_id,
          unidad_medida_id: this.existencia.unidad_medida_id,
          estado: this.existencia.estado ? parseInt(this.existencia.estado) : null,
          contiene: this.existencia.contiene ? parseInt(this.existencia.contiene) : null,
          existencia: parseFloat(this.existencia.existencia)
        };
        
        const response = await axios.put(
          `/api/gemar/existencias-mercancia/${existenciaId}/`, 
          datosParaEnviar, 
          {
            headers: {
              'Authorization': `Token ${token}`,
              'Content-Type': 'application/json'
            }
          }
        );
        
        if (response.status === 200) {
          this.mostrarExito('Existencia de mercancía actualizada correctamente');
          this.$router.push({ name: 'ExistenciasMercancia' });
        }
      } catch (error) {
        console.error('Error al guardar cambios:', error);
        let errorMessage = 'Error al actualizar la existencia de mercancía';
        if (error.response?.data) {
          errorMessage = Object.values(error.response.data).join(', ');
        }
        this.mostrarError(errorMessage);
      } finally {
        this.loading = false;
      }
    },
    
    confirmCancel() {
      Swal.fire({
        title: "¿Volver a la página principal?",
        text: "Los cambios no guardados se perderán",
        icon: "warning",
        showCancelButton: true,
        cancelButtonText: '<i class="bi bi-x-circle me-1"></i>Continuar',
        cancelButtonColor: "#f1513f",
        confirmButtonText: '<i class="bi bi-box-arrow-right me-1"></i>Volver',
        confirmButtonColor: "#007bff",
        reverseButtons: true,
      }).then((result) => {
        if (result.isConfirmed) {
          this.$router.go(-1);
        }
      });
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

.ufc-modal-body .ufc-form-actions {
  border-top: 1px solid #eee;
  padding-top: 15px;
  margin-top: 0;
}

.ufc-producto-option.selected {
  background-color: #002a68;
  color: white;
}

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

.ufc-select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 12px;
}

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