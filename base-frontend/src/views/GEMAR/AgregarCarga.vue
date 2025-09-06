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
                <button type="submit" class="ufc-button primary" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-1" role="status"></span>
                  <i v-else class="bi bi-check-circle me-1"></i>
                  {{ loading ? 'Guardando...' : 'Guardar Carga' }}
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
        observaciones: '',
      },
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
      return this.terminales.filter(t => t.puerto_id == this.carga.puerto_id);
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
        const [puertosRes, productosRes, organismosRes, terminalesRes] = await Promise.all([
          axios.get('/api/puertos/', { headers }),
          axios.get('/api/productos/', { headers }),
          axios.get('/api/osde/', { headers }),
          axios.get('/api/terminales/', { 
            headers,
            params: { 
              limit: 1000
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
        this.terminales = (terminalesRes.data.results || terminalesRes.data || []).map(t => ({
          id: t.id,
          nombre_terminal: t.nombre_terminal || t.nombre || 'Sin nombre',
          puerto_id: t.puerto?.id || t.puerto_id || null,
          puerto_name: t.puerto?.nombre_puerto || t.puerto?.nombre || 'Sin puerto'
        }));

      } catch (error) {
        console.error('Error al cargar datos:', error);
        let errorMessage = 'Error al cargar datos iniciales';
        if (error.response) {
          if (error.response.status === 403) {
            errorMessage = 'No tiene permisos para acceder a estos datos';
          } else if (error.response.data?.detail) {
            errorMessage = error.response.data.detail;
          }
        }
        this.mostrarError(errorMessage);
      } finally {
        this.loading = false;
      }
    },

    async guardarCarga() {
      try {
        this.loading = true;
        const token = localStorage.getItem('token');
        const headers = {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        };

        // Preparar datos para enviar
        const payload = {
          puerto_id: this.carga.puerto_id,
          terminal_id: this.carga.terminal_id,
          producto_id: this.carga.producto_id,
          manifiesto: this.carga.manifiesto,
          toneladas_ayer: parseFloat(this.carga.toneladas_ayer),
          toneladas_hoy: parseFloat(this.carga.toneladas_hoy),
          organismo_id: this.carga.organismo_id,
          dias_almacen: parseInt(this.carga.dias_almacen),
          plan: parseFloat(this.carga.plan),
          real: parseFloat(this.carga.real || 0),
          observaciones: this.carga.observaciones
        };

        // Enviar al backend
        const response = await axios.post('/api/gemar/cargas-viejas/', payload, { headers });

        if (response.status === 201) {
          this.mostrarExito('Carga guardada correctamente');
          this.$router.push({ name: 'CargasViejas' });
        }
      } catch (error) {
        console.error('Error al guardar:', error);
        let errorMessage = 'Error al guardar la carga';
        if (error.response) {
          if (error.response.status === 400) {
            if (error.response.data.non_field_errors) {
              errorMessage = error.response.data.non_field_errors.join(', ');
            } else {
              errorMessage = 'Datos inválidos: ' + JSON.stringify(error.response.data);
            }
          } else if (error.response.status === 403) {
            errorMessage = 'No tiene permisos para realizar esta acción';
          } else if (error.response.status === 500) {
            errorMessage = 'Error interno del servidor';
          }
        }
        this.mostrarError(errorMessage);
      } finally {
        this.loading = false;
      }
    },

    confirmCancel() {
      Swal.fire({
        title: '¿Cancelar?',
        text: 'Los cambios no guardados se perderán',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, cancelar',
        cancelButtonText: 'No, continuar'
      }).then((result) => {
        if (result.isConfirmed) {
          this.$router.push({ name: 'CargasViejas' });
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
.ufc-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  padding: 1rem;
  margin-bottom: 1rem;
}

.ufc-header h6 {
  margin: 0;
  color: #495057;
  font-weight: 600;
}

.ufc-button {
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.ufc-button.primary {
  background-color: #0d6efd;
  color: white;
}

.ufc-button.primary:hover:not(:disabled) {
  background-color: #0b5ed7;
}

.ufc-button.secondary {
  background-color: #6c757d;
  color: white;
}

.ufc-button.secondary:hover {
  background-color: #5c636a;
}

.ufc-button:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.form-label {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.form-control:focus,
.form-select:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.card {
  border-radius: 0.5rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  padding: 1rem 1.25rem;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
</style>