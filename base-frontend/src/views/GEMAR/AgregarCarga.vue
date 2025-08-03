<template>
  <div>
    <div class="ufc-header">
      <h6>Agregar Carga</h6>
    </div>
    <Navbar-Component />
    <div class="container py-3" style="margin-left: 20em; width: 70%">
      <div class="card border">
        <div class="card-header bg-light border-bottom">
          <h5 class="mb-0 text-dark fw-semibold">
            <i class="bi bi-box-seam me-2"></i> Nueva Carga
          </h5>
        </div>
        <div class="card-body p-3">
          <form @submit.prevent="guardarCarga">
            <div class="row">
              <!-- Campo: Parte PBIP -->
              <div class="col-md-6">
                <div class="mb-3">
                  <label for="parte" class="form-label small fw-semibold text-secondary">Parte PBIP*</label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="carga.parte_id"
                    required
                    @change="cargarDatosParte"
                    oninvalid="this.setCustomValidity('Por favor, seleccione un Parte PBIP')"
                    oninput="this.setCustomValidity('')"
                  >
                    <option value="" disabled>Seleccione un Parte PBIP</option>
                    <option
                      v-for="parte in partesPBIP"
                      :key="parte.id"
                      :value="parte.id"
                    >
                      PBIP - {{ parte.buque?.nombre || 'Sin buque' }} - {{ parte.puerto?.nombre || 'Sin puerto' }} - Nivel {{ parte.nivel }}
                    </option>
                  </select>
                </div>
              </div>

              <!-- Campo: Puerto -->
              <div class="col-md-6">
                <div class="mb-3">
                  <label for="puerto" class="form-label small fw-semibold text-secondary">Puerto*</label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="carga.puerto_id"
                    required
                    @change="carga.terminal_id = ''"
                    oninvalid="this.setCustomValidity('Por favor, seleccione un puerto')"
                    oninput="this.setCustomValidity('')"
                  >
                    <option value="" disabled>Seleccione un puerto</option>
                    <option
                      v-for="puerto in puertos"
                      :key="puerto.id"
                      :value="puerto.id"
                    >
                      {{ puerto.id }}-{{ puerto.nombre_puerto }}
                    </option>
                  </select>
                </div>
              </div>

              <!-- Campo: Terminal -->
              <div class="col-md-6">
                <div class="mb-3">
                  <label for="terminal" class="form-label small fw-semibold text-secondary">Terminal*</label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="carga.terminal_id"
                    required
                    :disabled="!carga.puerto_id"
                    oninvalid="this.setCustomValidity('Por favor, seleccione una terminal')"
                    oninput="this.setCustomValidity('')"
                  >
                    <option value="" disabled>Seleccione una terminal</option>
                    <option
                      v-for="terminal in terminalesFiltradas"
                      :key="terminal.id"
                      :value="terminal.id"
                    >
                      {{ terminal.nombre_terminal }} ({{ terminal.puerto_name }})
                    </option>
                  </select>
                  <small v-if="carga.puerto_id && terminalesFiltradas.length === 0" class="text-danger">
                    No hay terminales disponibles para este puerto
                  </small>
                </div>
              </div>

              <!-- Campo: Producto -->
              <div class="col-md-6">
                <div class="mb-3">
                  <label for="producto" class="form-label small fw-semibold text-secondary">Producto*</label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="carga.producto_id"
                    required
                    oninvalid="this.setCustomValidity('Por favor, seleccione un producto')"
                    oninput="this.setCustomValidity('')"
                  >
                    <option value="" disabled>Seleccione un producto</option>
                    <option
                      v-for="producto in productos"
                      :key="producto.id"
                      :value="producto.id"
                    >
                      {{ producto.id }}-{{ producto.nombre_producto }}
                    </option>
                  </select>
                </div>
              </div>

              <!-- Campo: Manifiesto -->
              <div class="col-md-6">
                <div class="mb-3">
                  <label for="manifiesto" class="form-label small fw-semibold text-secondary">Manifiesto*</label>
                  <input
                    type="text"
                    class="form-control form-control-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="carga.manifiesto"
                    id="manifiesto"
                    name="manifiesto"
                    required
                    oninvalid="this.setCustomValidity('Por favor, ingrese el manifiesto')"
                    oninput="this.setCustomValidity('')"
                  />
                </div>
              </div>

              <!-- Campo: Organismo -->
              <div class="col-md-6">
                <div class="mb-3">
                  <label for="organismo" class="form-label small fw-semibold text-secondary">Organismo*</label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="carga.organismo_id"
                    required
                    oninvalid="this.setCustomValidity('Por favor, seleccione un organismo')"
                    oninput="this.setCustomValidity('')"
                  >
                    <option value="" disabled>Seleccione un organismo</option>
                    <option
                      v-for="organismo in organismos"
                      :key="organismo.id"
                      :value="organismo.id"
                    >
                      {{ organismo.id }}-{{ organismo.nombre }}
                    </option>
                  </select>
                </div>
              </div>

              <!-- Campos numéricos -->
              <div class="col-md-4">
                <div class="mb-3">
                  <label for="toneladas_ayer" class="form-label small fw-semibold text-secondary">Toneladas Ayer*</label>
                  <input
                    type="number"
                    class="form-control form-control-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model.number="carga.toneladas_ayer"
                    id="toneladas_ayer"
                    name="toneladas_ayer"
                    step="0.01"
                    min="0"
                    required
                    oninvalid="this.setCustomValidity('Por favor, ingrese las toneladas de ayer')"
                    oninput="this.setCustomValidity('')"
                  />
                </div>
              </div>

              <div class="col-md-4">
                <div class="mb-3">
                  <label for="toneladas_hoy" class="form-label small fw-semibold text-secondary">Toneladas Hoy*</label>
                  <input
                    type="number"
                    class="form-control form-control-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model.number="carga.toneladas_hoy"
                    id="toneladas_hoy"
                    name="toneladas_hoy"
                    step="0.01"
                    min="0"
                    required
                    oninvalid="this.setCustomValidity('Por favor, ingrese las toneladas de hoy')"
                    oninput="this.setCustomValidity('')"
                  />
                </div>
              </div>

              <div class="col-md-4">
                <div class="mb-3">
                  <label for="dias_almacen" class="form-label small fw-semibold text-secondary">Días en Almacén*</label>
                  <input
                    type="number"
                    class="form-control form-control-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model.number="carga.dias_almacen"
                    id="dias_almacen"
                    name="dias_almacen"
                    min="0"
                    required
                    oninvalid="this.setCustomValidity('Por favor, ingrese los días en almacén')"
                    oninput="this.setCustomValidity('')"
                  />
                </div>
              </div>

              <!-- Campos de plan y real -->
              <div class="col-md-4">
                <div class="mb-3">
                  <label for="plan" class="form-label small fw-semibold text-secondary">Plan*</label>
                  <input
                    type="number"
                    class="form-control form-control-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model.number="carga.plan"
                    id="plan"
                    name="plan"
                    step="0.01"
                    min="0"
                    required
                    oninvalid="this.setCustomValidity('Por favor, ingrese el plan')"
                    oninput="this.setCustomValidity('')"
                  />
                </div>
              </div>

              <div class="col-md-4">
                <div class="mb-3">
                  <label for="real" class="form-label small fw-semibold text-secondary">Real*</label>
                  <input
                    type="number"
                    class="form-control form-control-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model.number="carga.real"
                    id="real"
                    name="real"
                    step="0.01"
                    min="0"
                    required
                    oninvalid="this.setCustomValidity('Por favor, ingrese el real')"
                    oninput="this.setCustomValidity('')"
                  />
                </div>
              </div>

              <!-- Campo: Estado -->
              <div class="col-md-4">
                <div class="mb-3">
                  <label for="estado" class="form-label small fw-semibold text-secondary">Estado*</label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="carga.estado"
                    required
                    oninvalid="this.setCustomValidity('Por favor, seleccione un estado')"
                    oninput="this.setCustomValidity('')"
                  >
                    <option value="CREADO">Creado</option>
                    <option value="APROBADO">Aprobado</option>
                    <option value="CANCELADO">Cancelado</option>
                  </select>
                </div>
              </div>

              <!-- Campo: Observaciones -->
              <div class="col-md-12">
                <div class="mb-3">
                  <label for="observaciones" class="form-label small fw-semibold text-secondary">Observaciones</label>
                  <textarea
                    class="form-control form-control-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="carga.observaciones"
                    id="observaciones"
                    name="observaciones"
                    rows="2"
                  ></textarea>
                </div>
              </div>
            </div>

            <!-- Botones de acción -->
            <div class="modal-footer">
              <div class="d-flex justify-content-between align-items-center mb-4">
                <button type="button" class="ufc-button secondary" @click="confirmCancel">
                  <i class="bi bi-x-circle me-1"></i>Cancelar
                </button>
                <button type="submit" class="ufc-button primary">
                  <i class="bi bi-check-circle me-1"></i>Guardar Carga
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
  name: 'AgregarCarga',
  components: {
    NavbarComponent
  },
  data() {
    return {
      carga: {
        parte_id: null,
        puerto_id: '',
        terminal_id: '',
        producto_id: '',
        manifiesto: '',
        toneladas_ayer: 0,
        toneladas_hoy: 0,
        organismo_id: '',
        dias_almacen: 0,
        plan: 0,
        real: 0,
        estado: 'CREADO',
        observaciones: '',
        aprobado_por: null
      },
      partesPBIP: [],
      puertos: [],
      terminales: [],
      productos: [],
      organismos: [],
      loading: false
    }
  },
  computed: {
    terminalesFiltradas() {
      if (!this.carga.puerto_id) return [];
      return this.terminales.filter(t => {
        const puertoId = t.puerto?.id || t.puerto_id;
        return puertoId == this.carga.puerto_id;
      });
    }
  },
  async created() {
    await this.cargarDatosIniciales();
  },
  methods: {
    async cargarDatosIniciales() {
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

        // Cargar todos los datos necesarios
        const [puertosRes, productosRes, organismosRes, terminalesRes, partesRes] = await Promise.all([
          axios.get('/api/puertos/', { headers }),
          axios.get('/api/productos/', { headers }),
          axios.get('/api/osde/', { headers }),
          axios.get('/api/terminales/', { 
            headers,
            params: { 
              limit: 1000,
              expand: 'puerto'
            }
          }),
          axios.get('/api/gemar/partes-pbip/', { 
            headers,
            params: { 
              estado: 'CREADO', 
              limit: 1000,
              expand: 'buque,puerto'
            }
          })
        ]);

        // Procesar puertos
        this.puertos = (puertosRes.data.results || puertosRes.data || []).map(p => ({
          id: p.id,
          nombre_puerto: p.nombre_puerto || p.nombre || 'Sin nombre'
        }));

        // Procesar productos
        this.productos = (productosRes.data.results || productosRes.data || []).map(p => ({
          id: p.id,
          nombre_producto: p.nombre_producto || p.nombre || 'Sin nombre'
        }));

        // Procesar organismos
        this.organismos = (organismosRes.data.results || organismosRes.data || []).map(o => ({
          id: o.id,
          nombre: o.nombre || o.nombre_organismo || 'Sin nombre'
        }));

        // Procesar terminales
        this.terminales = (terminalesRes.data.results || terminalesRes.data || []).map(t => {
          const puerto = t.puerto || {};
          return {
            id: t.id,
            nombre_terminal: t.nombre_terminal || t.nombre || 'Sin nombre',
            puerto: {
              id: puerto.id || t.puerto_id,
              nombre: puerto.nombre_puerto || puerto.nombre || 'Sin nombre'
            },
            puerto_id: puerto.id || t.puerto_id,
            puerto_name: puerto.nombre_puerto || puerto.nombre || 'Sin puerto'
          };
        });

        // Procesar partes PBIP
        this.partesPBIP = (partesRes.data.results || partesRes.data || []).map(p => {
          const buque = p.buque || {};
          const puerto = p.puerto || {};
          return {
            id: p.id,
            buque: {
              id: buque.id || p.buque_id,
              nombre: buque.nombre_embarcacion || buque.nombre || 'Sin nombre'
            },
            puerto: {
              id: puerto.id || p.puerto_id,
              nombre: puerto.nombre_puerto || puerto.nombre || 'Sin nombre'
            },
            nivel: p.nivel,
            estado: p.estado
          };
        });

      } catch (error) {
        console.error('Error al cargar datos:', error);
        this.mostrarError('Error al cargar datos iniciales: ' + (error.response?.data?.detail || error.message));
      } finally {
        this.loading = false;
      }
    },
    
    async cargarDatosParte() {
      if (!this.carga.parte_id) return;
      
      try {
        this.loading = true;
        const token = localStorage.getItem('token');
        const headers = { 
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        };

        const response = await axios.get(`/api/gemar/partes-pbip/${this.carga.parte_id}/`, { 
          headers,
          params: { expand: 'puerto' }
        });
        const parte = response.data;
        
        // Actualizar solo el estado del parte
        this.carga.estado = 'CREADO';

      } catch (error) {
        console.error('Error al cargar datos del parte:', error);
        this.mostrarError('Error al cargar datos del parte PBIP seleccionado');
      } finally {
        this.loading = false;
      }
    },
    
    async guardarCarga() {
      try {
        this.loading = true;
        const token = localStorage.getItem('token');
        const userData = JSON.parse(localStorage.getItem('userData') || '{}');
        const headers = { 
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        };
        
        // Validar campos requeridos
        const requiredFields = [
          'parte_id', 'puerto_id', 'terminal_id', 'producto_id', 
          'manifiesto', 'organismo_id', 'toneladas_ayer', 
          'toneladas_hoy', 'dias_almacen', 'plan', 'real', 'estado'
        ];
        
        const missingFields = requiredFields.filter(field => !this.carga[field]);
        if (missingFields.length > 0) {
          throw new Error(`Los siguientes campos son requeridos: ${missingFields.join(', ')}`);
        }

        // Construir payload con los nombres que espera el backend
        const payload = {
          parte: this.carga.parte_id,
          puerto: this.carga.puerto_id,
          terminal: this.carga.terminal_id,
          producto: this.carga.producto_id,
          manifiesto: this.carga.manifiesto,
          toneladas_ayer: parseFloat(this.carga.toneladas_ayer),
          toneladas_hoy: parseFloat(this.carga.toneladas_hoy),
          organismo: this.carga.organismo_id,
          dias_almacen: parseInt(this.carga.dias_almacen),
          plan: parseFloat(this.carga.plan),
          real: parseFloat(this.carga.real),
          estado: this.carga.estado,
          observaciones: this.carga.observaciones,
          creado_por: userData.id
        };

        // Si está aprobado, agregar quien aprueba
        if (this.carga.estado === 'APROBADO') {
          payload.aprobado_por = userData.id;
        }

        const response = await axios.post('/api/gemar/cargas-viejas/', payload, { headers });
        
        if (response.status === 201) {
          this.mostrarExito('Carga guardada correctamente');
          this.$router.push({ name: 'CargasViejas' });
        }
      } catch (error) {
        console.error('Error al guardar:', error);
        let errorDetails = '';
        
        if (error.response?.data) {
          if (typeof error.response.data === 'object') {
            errorDetails = Object.entries(error.response.data)
              .map(([field, errors]) => {
                const errorList = Array.isArray(errors) ? errors.join(', ') : errors;
                return `<strong>${field}:</strong> ${errorList}`;
              })
              .join('<br>');
          } else {
            errorDetails = error.response.data;
          }
        }
        
        const errorMessage = `
          <div>
            <p>Error al guardar la carga:</p>
            <div class="text-start">${errorDetails || error.message}</div>
          </div>
        `;
        
        Swal.fire({
          title: 'Error',
          html: errorMessage,
          icon: 'error',
          confirmButtonText: 'Entendido'
        });
      } finally {
        this.loading = false;
      }
    },
    
    confirmCancel() {
      Swal.fire({
        title: "¿Volver a la página principal?",
        text: "Los datos no guardados se perderán",
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