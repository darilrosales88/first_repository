<template>
  <div>
    <div class="ufc-header">
      <h6>Editar Parte PBIP</h6>
    </div>
    <Navbar-Component />
    <div class="card border" style="margin-left: 20em; width: 70%">
      <div class="card-header bg-light border-bottom">
        <h6 class="mb-0 text-dark fw-semibold">
          Editar Parte PBIP
        </h6>
      </div>
      <div class="card-body p-3">
        <form @submit.prevent="guardarCambios">
          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label small fw-semibold text-secondary">Fecha de Operación*</label>
              <input 
                type="date" 
                v-model="parte.fecha_operacion" 
                class="form-control form-control-sm border-secondary"
                style="padding: 8px 12px"
                required
                :disabled="parte.estado !== 'CREADO'"
              >
            </div>
            <div class="col-md-6">
              <label class="form-label small fw-semibold text-secondary">Fecha de Creación</label>
              <input 
                type="text" 
                :value="fechaCreacionFormateada" 
                class="form-control form-control-sm border-secondary"
                style="padding: 8px 12px"
                readonly
              >
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label small fw-semibold text-secondary">Buque*</label>
              <select 
                v-model="parte.buque_id" 
                class="form-select form-select-sm border-secondary"
                style="padding: 8px 12px"
                required
                :disabled="parte.estado !== 'CREADO'"
              >
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
              <label class="form-label small fw-semibold text-secondary">Puerto de Arribo*</label>
              <select 
                v-model="parte.puerto_id" 
                class="form-select form-select-sm border-secondary"
                style="padding: 8px 12px"
                required
                :disabled="parte.estado !== 'CREADO'"
              >
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
              <label class="form-label small fw-semibold text-secondary">Fecha y Hora*</label>
              <input 
                type="datetime-local" 
                v-model="parte.fecha_hora" 
                class="form-control form-control-sm border-secondary"
                style="padding: 8px 12px"
                required
                :disabled="parte.estado !== 'CREADO'"
              >
            </div>
            <div class="col-md-6">
              <label class="form-label small fw-semibold text-secondary">Nivel de Protección*</label>
              <select 
                v-model="parte.nivel" 
                class="form-select form-select-sm border-secondary"
                style="padding: 8px 12px"
                required
                :disabled="parte.estado !== 'CREADO'"
              >
                <option value="1">Nivel 1</option>
                <option value="2">Nivel 2</option>
                <option value="3">Nivel 3</option>
              </select>
            </div>
          </div>

          <div class="row mb-3" v-if="parte.creado_por">
            <div class="col-md-6">
              <label class="form-label small fw-semibold text-secondary">Creado por</label>
              <input 
                type="text" 
                :value="parte.creado_por.username" 
                class="form-control form-control-sm border-secondary"
                style="padding: 8px 12px"
                readonly
              >
            </div>
            <div class="col-md-6" v-if="parte.aprobado_por">
              <label class="form-label small fw-semibold text-secondary">Aprobado por</label>
              <input 
                type="text" 
                :value="parte.aprobado_por.username" 
                class="form-control form-control-sm border-secondary"
                style="padding: 8px 12px"
                readonly
              >
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label small fw-semibold text-secondary">Estado</label>
              <input 
                type="text" 
                :value="parte.estado" 
                class="form-control form-control-sm border-secondary"
                style="padding: 8px 12px"
                readonly
              >
            </div>
          </div>

          <div class="modal-footer">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <button 
                type="button" 
                @click="cancelar" 
                class="ufc-button secondary"
                :disabled="cargando"
              >
                <i class="bi bi-x-circle me-1"></i> Cancelar
              </button>
              <button 
                type="submit" 
                class="ufc-button primary"
                :disabled="cargando || parte.estado !== 'CREADO'"
              >
                <span v-if="cargando" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <i v-else class="bi bi-save me-1"></i> 
                {{ cargando ? 'Guardando...' : 'Guardar Cambios' }}
              </button>
              <button 
                v-if="parte.estado === 'CREADO' && tienePermisoAprobar"
                type="button" 
                @click="aprobarParte" 
                class="ufc-button success"
                :disabled="cargando"
              >
                <i class="bi bi-check-circle me-1"></i> Aprobar
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: 'EditarPartePBIP',
  components: {
    NavbarComponent
  },
  data() {
    return {
      parte: {
        id: null,
        fecha_operacion: '',
        fecha_creacion: '',
        buque_id: null,
        puerto_id: null,
        fecha_hora: '',
        nivel: '1',
        estado: 'CREADO',
        creado_por: null,
        aprobado_por: null
      },
      listaBuques: [],
      listaPuertos: [],
      cargando: false,
      tienePermisoAprobar: false
    }
  },
  computed: {
    fechaCreacionFormateada() {
      return this.formatearFecha(this.parte.fecha_creacion);
    }
  },
  async created() {
    await this.verificarPermisos();
    await this.cargarDatosIniciales();
    await this.cargarPartePBIP();
  },
  methods: {
    async verificarPermisos() {
      try {
        const token = localStorage.getItem('token');
        const user = JSON.parse(localStorage.getItem('user'));
        
        if (user && (user.is_staff || user.groups.some(group => group.name === 'GEMAR'))) {
          this.tienePermisoAprobar = true;
        }
      } catch (error) {
        console.error('Error al verificar permisos:', error);
      }
    },
    
    async cargarDatosIniciales() {
      try {
        this.cargando = true;
        const token = localStorage.getItem('token');
        const headers = {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        };

        const [buquesRes, puertosRes] = await Promise.all([
          axios.get("/api/embarcaciones/", { headers }),
          axios.get("/api/puertos/", { headers }),
        ]);

        this.listaBuques = buquesRes.data.results || buquesRes.data || [];
        this.listaPuertos = puertosRes.data.results || puertosRes.data || [];

        this.listaBuques = this.listaBuques.map((b) => ({
          id: b.id,
          nombre: b.nombre_embarcacion || b.nombre || "",
        }));

        this.listaPuertos = this.listaPuertos.map((p) => ({
          id: p.id,
          nombre: p.nombre_puerto || p.nombre || "",
        }));
      } catch (error) {
        console.error('Error al cargar datos:', error);
        this.mostrarError('Error al cargar los datos iniciales');
      } finally {
        this.cargando = false;
      }
    },
    
    async cargarPartePBIP() {
      try {
        this.cargando = true;
        const parteId = this.$route.params.id;
        if (!parteId) {
          this.mostrarError('No se especificó un ID de parte válido');
          this.$router.go(-1);
          return;
        }

        const token = localStorage.getItem('token');
        const headers = {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        };

        const response = await axios.get(`/gemar/partes-pbip/${parteId}/`, { headers });
        
        // Formatear la fecha_hora para el input datetime-local
        let fechaHora = response.data.fecha_hora;
        if (fechaHora) {
          if (fechaHora.includes('T')) {
            fechaHora = fechaHora.slice(0, 16);
          } else {
            fechaHora = `${fechaHora}T00:00`;
          }
        }

        this.parte = {
          id: response.data.id,
          fecha_operacion: response.data.fecha_operacion,
          fecha_creacion: response.data.fecha_creacion,
          buque_id: response.data.buque.id,
          puerto_id: response.data.puerto.id,
          fecha_hora: fechaHora,
          nivel: response.data.nivel.toString(),
          estado: response.data.estado,
          creado_por: response.data.creado_por,
          aprobado_por: response.data.aprobado_por
        };

      } catch (error) {
        console.error('Error al cargar el parte PBIP:', error);
        this.mostrarError('Error al cargar los datos del parte PBIP');
        this.$router.go(-1);
      } finally {
        this.cargando = false;
      }
    },
    
    async guardarCambios() {
      if (!this.parte.buque_id || !this.parte.puerto_id || !this.parte.fecha_hora || !this.parte.fecha_operacion) {
        this.mostrarError('Todos los campos marcados con * son requeridos');
        return;
      }

      try {
        this.cargando = true;
        const token = localStorage.getItem('token');
        const headers = {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        };

        // Preparar el payload para la actualización
        const payload = {
          fecha_operacion: this.parte.fecha_operacion,
          buque_id: this.parte.buque_id,
          puerto_id: this.parte.puerto_id,
          fecha_hora: this.parte.fecha_hora,
          nivel: parseInt(this.parte.nivel)
        };

        // Usamos PATCH para actualización parcial según convenciones REST
        const response = await axios.patch(
          `/gemar/partes-pbip/${this.parte.id}/`,
          payload,
          { headers }
        );

        this.mostrarExito('Cambios guardados correctamente');
        this.$router.push({ name: 'Gemar-Partes-PBIP' });
        
      } catch (error) {
        console.error('Error al guardar cambios:', error);
        let errorMessage = 'Error al guardar los cambios';
        
        if (error.response) {
          if (error.response.status === 400) {
            errorMessage = error.response.data.detail || 'Datos inválidos';
            if (error.response.data) {
              const errors = [];
              for (const key in error.response.data) {
                if (Array.isArray(error.response.data[key])) {
                  errors.push(`${key}: ${error.response.data[key].join(', ')}`);
                } else {
                  errors.push(`${key}: ${error.response.data[key]}`);
                }
              }
              errorMessage = errors.join('\n');
            }
          } else if (error.response.status === 403) {
            errorMessage = 'No tiene permiso para editar este parte';
          } else if (error.response.status === 404) {
            errorMessage = 'El parte no fue encontrado';
          } else if (error.response.status === 409) {
            errorMessage = 'No se puede editar un parte que no está en estado CREADO';
          }
        } else {
          errorMessage = 'Error de conexión con el servidor';
        }
        
        this.mostrarError(errorMessage);
      } finally {
        this.cargando = false;
      }
    },
    
    async aprobarParte() {
      try {
        this.cargando = true;
        const token = localStorage.getItem('token');
        const headers = {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        };

        const response = await axios.post(
          `/gemar/partes-pbip/${this.parte.id}/aprobar/`,
          {},
          { headers }
        );

        this.mostrarExito('Parte aprobado correctamente');
        await this.cargarPartePBIP(); // Recargar los datos después de aprobar
        
      } catch (error) {
        console.error('Error al aprobar el parte:', error);
        let errorMessage = 'Error al aprobar el parte';
        
        if (error.response) {
          if (error.response.status === 403) {
            errorMessage = 'No tiene permiso para aprobar este parte';
          } else if (error.response.status === 404) {
            errorMessage = 'El parte no fue encontrado';
          } else if (error.response.data && error.response.data.detail) {
            errorMessage = error.response.data.detail;
          }
        }
        
        this.mostrarError(errorMessage);
      } finally {
        this.cargando = false;
      }
    },
    
    cancelar() {
      this.$router.push({ name: 'Gemar-Partes-PBIP' });
    },
    
    formatearFecha(fecha) {
      if (!fecha) return '';
      const date = new Date(fecha);
      return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
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

.ufc-button.success {
  background: #28a745;
  color: white;
}

.ufc-button.success:hover {
  background: #218838;
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