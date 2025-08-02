<template>
  <div class="gemar-header">
    <h6>Partes GEMAR</h6>
  </div>
  <Navbar-Component />
  <div class="container py-3" style="margin-left: 20em; width: 70%">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-clipboard-data me-2"></i>Nuevo registro de programación de maniobras
        </h5>
      </div>
      <div class="card-body p-3">
        <form @submit.prevent="submitForm">
          <div class="row">
            <!-- Columna 1 -->
            <div class="col-md-6">
                
            <!-- Campo: Fecha de operación -->
              <div class="mb-3">
                <label for="fecha_actual" class="form-label small fw-semibold text-secondary">Fecha actual</label>
                <input type="date" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" 
                       v-model="formData.fecha_operacion" id="fecha_actual" name="fecha_actual" required disabled />
              </div>

              <!-- Campo: Fecha de operación -->
              <div class="mb-3">
                <label for="fecha_operacion" class="form-label small fw-semibold text-secondary">Fecha de operación</label>
                <input type="date" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" 
                       v-model="formData.fecha_operacion" id="fecha_operacion" name="fecha_operacion" required />
              </div>

              

              <!-- Campo: Puerto -->
              <div class="mb-3">
                <label for="puerto" class="form-label small fw-semibold text-secondary">Puerto</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" 
                        v-model="formData.puerto" id="puerto" name="puerto" @change="getTerminalesPorPuerto" required>
                  <option value="" disabled selected>Seleccione un puerto</option>
                  <option v-for="puerto in puertos" :key="puerto.id" :value="puerto.id">
                    {{ puerto.nombre_puerto }}
                  </option>
                </select>
              </div>

              <!-- Campo: Terminal -->
              <div class="mb-3">
                <label for="terminal" class="form-label small fw-semibold text-secondary">Terminal</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" 
                        v-model="formData.terminal" id="terminal" name="terminal" @change="getAtraquesPorTerminal" required>
                  <option value="" disabled selected>Seleccione una terminal</option>
                  <option v-for="terminal in terminales" :key="terminal.id" :value="terminal.id">
                    {{ terminal.nombre_terminal }}
                  </option>
                </select>
              </div>

              <!-- Campo: Atraque -->
              <div class="mb-3">
                <label for="atraque" class="form-label small fw-semibold text-secondary">Atraque</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" 
                        v-model="formData.atraque" id="atraque" name="atraque" required>
                  <option value="" disabled selected>Seleccione un atraque</option>
                  <option v-for="atraque in atraques" :key="atraque.id" :value="atraque.id">
                    {{ atraque.nombre_atraque }}
                  </option>
                </select>
              </div>
            </div>

            <!-- Columna 2 -->
            <div class="col-md-6">
              <!-- Campo: Buque -->
              <div class="mb-3">
                <label for="buque" class="form-label small fw-semibold text-secondary">Buque</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" 
                        v-model="formData.buque" id="buque" name="buque" required>
                  <option value="" disabled selected>Seleccione un buque</option>
                  <option v-for="buque in buques" :key="buque.id" :value="buque.id">
                    {{ buque.nombre_embarcacion }}
                  </option>
                </select>
              </div>

              <!-- Campo: Puerto procedencia -->
              <div class="mb-3">
                <label for="puerto_procedencia" class="form-label small fw-semibold text-secondary">Puerto procedencia</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" 
                        v-model="formData.puerto_procedencia" id="puerto_procedencia" name="puerto_procedencia">
                  <option value="" disabled selected>Seleccione un puerto</option>
                  <option v-for="puerto in puertos" :key="puerto.id" :value="puerto.id">
                    {{ puerto.nombre_puerto }}
                  </option>
                </select>
              </div>

              <!-- Campo: Tipo de maniobra -->
              <div class="mb-3">
                <label for="tipo_maniobra" class="form-label small fw-semibold text-secondary">Tipo de maniobra</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" 
                        v-model="formData.tipo_maniobra" id="tipo_maniobra" name="tipo_maniobra" required>
                  <option value="" disabled selected>Seleccione un tipo</option>
                  <option v-for="maniobra in tiposManiobra" :key="maniobra.id" :value="maniobra.id">
                    {{ maniobra.nombre_maniobra }}
                  </option>
                </select>
              </div>

              <!-- Campo: Cantidad remolcadores -->
              <div class="mb-3">
                <label for="cantidad_remolcadores" class="form-label small fw-semibold text-secondary">Cantidad de remolcadores</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" 
                        v-model="formData.cantidad_remolcadores" id="cantidad_remolcadores" name="cantidad_remolcadores" required>
                  <option value="" disabled selected>Seleccione cantidad</option>
                  <option v-for="n in 11" :key="n" :value="n-1">{{ n-1 }}</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Campos ETA -->
          <div class="row mt-3">
            <div class="col-md-6">
              <h6 class="fw-semibold">Datos ETA (Estimated Time of Arrival)</h6>
              
              <!-- Campo: Formato ETA -->
              <div class="mb-3">
                <label for="formato_eta" class="form-label small fw-semibold text-secondary">Formato ETA</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" 
                        v-model="formData.formato_eta" id="formato_eta" name="formato_eta" @change="handleFormatoEtaChange" required>
                  <option value="" disabled selected>Seleccione formato</option>
                  <option value="1">24 horas</option>
                  <option value="2">AM/PM</option>
                  <option value="3">SIN DETERMINAR</option>
                </select>
              </div>

              <!-- Campo: Fecha ETA -->
              <div class="mb-3">
                <label for="fecha_eta" class="form-label small fw-semibold text-secondary">Fecha ETA</label>
                <input type="date" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" 
                       v-model="formData.fecha_eta" id="fecha_eta" name="fecha_eta" :disabled="formData.formato_eta === '3'" />
              </div>

              <!-- Campo: Hora ETA (24h) -->
              <div class="mb-3" v-if="formData.formato_eta === '1'">
                <label for="hora_eta" class="form-label small fw-semibold text-secondary">Hora ETA (24h)</label>
                <input type="time" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" 
                       v-model="formData.hora_eta" id="hora_eta" name="hora_eta" />
              </div>

              <!-- Campo: Hora ETA (AM/PM) -->
              <div class="mb-3" v-if="formData.formato_eta === '2'">
                <label for="hora_eta_am_pm" class="form-label small fw-semibold text-secondary">Hora ETA (AM/PM)</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" 
                        v-model="formData.hora_eta_am_pm" id="hora_eta_am_pm" name="hora_eta_am_pm">
                  <option value="" disabled selected>Seleccione</option>
                  <option value="1">AM</option>
                  <option value="2">PM</option>
                </select>
              </div>
            </div>

            <!-- Campos ETS -->
            <div class="col-md-6">
              <h6 class="fw-semibold">Datos ETS (Estimated Time of Sailing)</h6>
              
              <!-- Campo: Formato ETS -->
              <div class="mb-3">
                <label for="formato_ets" class="form-label small fw-semibold text-secondary">Formato ETS</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" 
                        v-model="formData.formato_ets" id="formato_ets" name="formato_ets" @change="handleFormatoEtsChange" required>
                  <option value="" disabled selected>Seleccione formato</option>
                  <option value="1">24 horas</option>
                  <option value="2">AM/PM</option>
                  <option value="3">SIN DETERMINAR</option>
                </select>
              </div>

              <!-- Campo: Fecha ETS -->
              <div class="mb-3">
                <label for="fecha_ets" class="form-label small fw-semibold text-secondary">Fecha ETS</label>
                <input type="date" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" 
                       v-model="formData.fecha_ets" id="fecha_ets" name="fecha_ets" :disabled="formData.formato_ets === '3'" />
              </div>

              <!-- Campo: Hora ETS (24h) -->
              <div class="mb-3" v-if="formData.formato_ets === '1'">
                <label for="hora_ets" class="form-label small fw-semibold text-secondary">Hora ETS (24h)</label>
                <input type="time" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" 
                       v-model="formData.hora_ets" id="hora_ets" name="hora_ets" />
              </div>

              <!-- Campo: Hora ETS (AM/PM) -->
              <div class="mb-3" v-if="formData.formato_ets === '2'">
                <label for="hora_ets_am_pm" class="form-label small fw-semibold text-secondary">Hora ETS (AM/PM)</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" 
                        v-model="formData.hora_ets_am_pm" id="hora_ets_am_pm" name="hora_ets_am_pm">
                  <option value="" disabled selected>Seleccione</option>
                  <option value="1">AM</option>
                  <option value="2">PM</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Campo: Observaciones -->
          <div class="mb-3">
            <label for="observaciones" class="form-label small fw-semibold text-secondary">Observaciones</label>
            <textarea class="form-control form-control-sm border-secondary" v-model="formData.observaciones" 
                      id="observaciones" name="observaciones" rows="4"></textarea>
          </div>

          <div class="modal-footer mt-3">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <button class="gemar-button secondary" @click="volver_principal">
                <i class="bi bi-x-circle" me-1></i>Cancelar
              </button>
              <button type="submit" class="gemar-button primary">
                <i class="bi bi-check-circle" me-1></i>Agregar
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
  name: "AdicionarProgramacionManiobras",
  components: {
    NavbarComponent,
  },
  data() {
    const now = new Date();
    const offset = now.getTimezoneOffset() * 60000;
    const localISOTime = new Date(now - offset).toISOString().split("T")[0];
    return {
      formData: {
        fecha_actual: localISOTime,
        fecha_operacion: localISOTime,
        puerto: "",
        terminal: "",
        atraque: "",
        buque: "",
        puerto_procedencia: "",
        tipo_maniobra: "",
        formato_eta: "",
        fecha_eta: "",
        hora_eta: "",
        hora_eta_am_pm: "",
        formato_ets: "",
        fecha_ets: "",
        hora_ets: "",
        hora_ets_am_pm: "",
        cantidad_remolcadores: "",
        observaciones: "",
        parte_programacion_maniobra: null,
      },
      puertos: [],
      terminales: [],
      atraques: [],
      buques: [],
      tiposManiobra: [],
      informeOperativoId: null,
      errors: '',
    };
  },

  computed: {
    formattedFechaActual() {
      return new Date().toLocaleString();
    }
  },

  mounted() {
    this.getPuertos();
    this.getBuques();
    this.getTiposManiobra();
    this.verificarExistePartePM();
  },

  methods: {
    handleFormatoEtaChange() {
      if (this.formData.formato_eta === '3') {
        this.formData.fecha_eta = "";
        this.formData.hora_eta = "";
        this.formData.hora_eta_am_pm = "";
      }
    },

    handleFormatoEtsChange() {
      if (this.formData.formato_ets === '3') {
        this.formData.fecha_ets = "";
        this.formData.hora_ets = "";
        this.formData.hora_ets_am_pm = "";
      }
    },

    validateForm() {
      this.errors = '';
      let valid = true;
      
      if (!this.formData.fecha_operacion || !this.formData.puerto || 
          !this.formData.terminal || !this.formData.atraque || 
          !this.formData.buque || !this.formData.tipo_maniobra || 
          !this.formData.formato_eta || !this.formData.formato_ets || 
          !this.formData.cantidad_remolcadores) {          
        this.errors += 'Los siguientes campos son obligatorios:<br>';
      }
      
      if (!this.formData.fecha_operacion) {
        this.errors += '- Fecha de operación.<br>';
        valid = false;
      }

      if (!this.formData.puerto) {
        this.errors += '- Puerto.<br>';
        valid = false;
      }

      if (!this.formData.terminal) {
        this.errors += '- Terminal.<br>';
        valid = false;
      }

      if (!this.formData.atraque) {
        this.errors += '- Atraque.<br>';
        valid = false;
      }

      if (!this.formData.buque) {
        this.errors += '- Buque.<br>';
        valid = false;
      }

      if (!this.formData.tipo_maniobra) {
        this.errors += '- Tipo de maniobra.<br>';
        valid = false;
      }

      if (!this.formData.formato_eta) {
        this.errors += '- Formato ETA.<br>';
        valid = false;
      }

      if (!this.formData.formato_ets) {
        this.errors += '- Formato ETS.<br>';
        valid = false;
      }

      if (!this.formData.cantidad_remolcadores) {
        this.errors += '- Cantidad de remolcadores.<br>';
        valid = false;
      }

      return valid;
    },

    async verificarExistePartePM() {
      try {
        const today = new Date();
        const fechaFormateada = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;

        const response = await axios.get('/gemar/gemar-verificar-informe-programacion-maniobra-existente/', {
          params: { fecha_actual: fechaFormateada }
        });

        if (response.data.existe) {
          this.informeOperativoId = response.data.id;
          this.formData.parte_programacion_maniobra = response.data.id;
          return true;
        }
        return false;
      } catch (error) {
        console.error("Error al verificar informe:", error);
        return false;
      }
    },
    
    async getPuertos() {
      try {
        const response = await axios.get("/api/puertos/");
        this.puertos = response.data.results;
      } catch (error) {
        console.error("Error al obtener los puertos:", error);
        Swal.fire("Error", "Hubo un error al obtener los puertos.", "error");
      }
    },

    async getTerminalesPorPuerto() {
      if (!this.formData.puerto) return;
      
      try {
        const response = await axios.get(`/api/terminales/?puerto=${this.formData.puerto}`);
        this.terminales = response.data.results;
        this.formData.terminal = "";
        this.formData.atraque = "";
        this.atraques = [];
      } catch (error) {
        console.error("Error al obtener las terminales:", error);
        Swal.fire("Error", "Hubo un error al obtener las terminales.", "error");
      }
    },

    async getAtraquesPorTerminal() {
      if (!this.formData.terminal) return;
      
      try {
        const response = await axios.get(`/api/atraques/?terminal=${this.formData.terminal}`);
        this.atraques = response.data.results;
        this.formData.atraque = "";
      } catch (error) {
        console.error("Error al obtener los atraques:", error);
        Swal.fire("Error", "Hubo un error al obtener los atraques.", "error");
      }
    },

    async getBuques() {
      try {
        const response = await axios.get("/api/embarcaciones/?tipo_embarcacion=buque");
        this.buques = response.data.results;
      } catch (error) {
        console.error("Error al obtener los buques:", error);
        Swal.fire("Error", "Hubo un error al obtener los buques.", "error");
      }
    },

    async getTiposManiobra() {
      try {
        const response = await axios.get("/api/tipo_maniobras/");
        this.tiposManiobra = response.data.results;
      } catch (error) {
        console.error("Error al obtener los tipos de maniobra:", error);
        Swal.fire("Error", "Hubo un error al obtener los tipos de maniobra.", "error");
      }
    },

    async submitForm() {
      if (!this.validateForm()) {
        Swal.fire('Errores en la entrada de datos', this.errors, 'error');
        return;
      }

      try {
        const existeInforme = await this.verificarExistePartePM();
        if (!existeInforme) {
          Swal.fire(
            "Error",
            "No existe un informe de programación de maniobras creado para la fecha actual. Debe crear uno primero.",
            "error"
          );
          this.$router.push({ name: "gemar_parte_programacion_maniobras" });
          return;
        }

        // Preparar datos para enviar
        const datosEnvio = {
          ...this.formData,
          parte_programacion_maniobra: this.informeOperativoId
        };
        console.log("Manololololo, ", datosEnvio);

        // Enviar datos
        const response = await axios.post("/gemar/gemar-programacion-maniobras/", datosEnvio);
        
        // Mostrar mensaje de éxito
        this.showSuccessToast("La programación de maniobras se ha adicionado satisfactoriamente.");
        this.resetForm();
        this.$router.push({ name: "gemar_parte_programacion_maniobras" });
        
      } catch (error) {
        console.error("Error detallado:", error.response?.data);
        let errorMsg = "Error al registrar la programación de maniobras";
        this.MensajeTemporaldeError("Error al registrar la programación de maniobras");
        if (error.response?.data) {
          if (typeof error.response.data === 'object') {
            errorMsg += ": " + JSON.stringify(error.response.data);
          } else {
            errorMsg += ": " + error.response.data;
          }
        }
        
        Swal.fire("Error", errorMsg, "error");
      }
    },

    resetForm() {
      this.formData = {
        fecha_operacion: "",        
        fecha_actual: "",
        puerto: "",
        terminal: "",
        atraque: "",
        buque: "",
        puerto_procedencia: "",
        tipo_maniobra: "",
        formato_eta: "",
        fecha_eta: "",
        hora_eta: "",
        hora_eta_am_pm: "",
        formato_ets: "",
        fecha_ets: "",
        hora_ets: "",
        hora_ets_am_pm: "",
        cantidad_remolcadores: "",
        observaciones: "",
        parte_programacion_maniobra: null,
      };
    },

    volver_principal() {
      event.preventDefault();
      event.stopPropagation();
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
          this.resetForm();
          this.$router.push({ name: "gemar_parte_programacion_maniobras" });
        }
      });
    },

    showSuccessToast(message) {
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
        title: message,
      });
    },

    MensajeTemporaldeError(message) {
      const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 4000,
        timerProgressBar: true,
        background: "#ff4444",
        color: "#fff",
        iconColor: "#fff",
        didOpen: (toast) => {
          toast.addEventListener("mouseenter", Swal.stopTimer);
          toast.addEventListener("mouseleave", Swal.resumeTimer);
        },
      });

      Toast.fire({
        icon: "error",
        title: message,
      });
    },
  },
};
</script>

<style scoped>
/* Estilos para el select personalizado de productos */
.gemar-custom-select {
  position: relative;
  width: 100%;
  cursor: pointer;
}

.gemar-select-display {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.85rem;
  background-color: white;
  min-height: 36px;
  display: flex;
  align-items: center;
  border-color: rgba(var(--bs-secondary-rgb),var(--bs-border-opacity)) !important;
}

.gemar-select-arrow {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  transition: transform 0.2s;
}

.gemar-custom-select.open .gemar-select-arrow {
  transform: translateY(-50%) rotate(180deg);
}

.gemar-productos-dropdown {
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

.gemar-productos-search-container {
  padding: 8px;
  border-bottom: 1px solid #eee;
  background: #f8f9fa;
}

.gemar-productos-search {
  width: 100%;
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.85rem;
}

.gemar-productos-search:focus {
  outline: none;
  border-color: #002a68;
}

.gemar-productos-options {
  max-height: 250px;
  overflow-y: auto;
}

.gemar-producto-option {
  padding: 8px 12px;
  font-size: 0.85rem;
  border-bottom: 1px solid #f0f0f0;
}

.gemar-producto-option:hover {
  background-color: #f5f5f5;
}

.gemar-producto-option.selected {
  background-color: #002a68;
  color: white;
}

/* Estilo para el botón de agregar */
.gemar-add-button {
  margin-left: 8px;
}

.gemar-select[multiple] {
  height: auto;
  min-height: 100px;
  padding: 8px;
}

.gemar-select[multiple] option {
  padding: 6px 8px;
  margin: 2px 0;
  border-radius: 4px;
}

.gemar-select[multiple] option:checked {
  background-color: #002a68;
  color: white;
}

.gemar-selected-products {
  font-size: 0.8rem;
  color: #666;
  margin-top: 5px;
}

.gemar-form-container {
  font-family: "Segoe UI", Roboto, -apple-system, sans-serif;
  color: #333;
  padding-bottom: 20px;
}

.gemar-header {
  background-color: #002a68;
  color: white;
  text-align: right;
  padding: 10px 15px;
  margin-bottom: 20px;
}

.gemar-header h6 {
  margin: 0;
  font-size: 1rem;
  font-weight: 500;
}

.gemar-form-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 15px;
}

.gemar-form-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.gemar-form-title {
  color: #002a68;
  font-size: 1.3rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}

.gemar-form-title i {
  font-size: 1.4rem;
}

.gemar-form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

@media (max-width: 768px) {
  .gemar-form-grid {
    grid-template-columns: 1fr;
  }
}

.gemar-input-group {
  margin-bottom: 15px;
}

.gemar-input-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 0.85rem;
  font-weight: 500;
  color: #444;
}

.gemar-input-group .required {
  color: #e74c3c;
}

.gemar-select,
.gemar-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.85rem;
  transition: all 0.2s;
  background-color: white;
}

.gemar-select:focus,
.gemar-input:focus {
  border-color: #002a68;
  box-shadow: 0 0 0 3px rgba(0, 42, 104, 0.1);
  outline: none;
}

.gemar-textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  resize: vertical;
  min-height: 70px;
  font-family: inherit;
  font-size: 0.85rem;
}

.gemar-textarea:focus {
  border-color: #002a68;
  box-shadow: 0 0 0 3px rgba(0, 42, 104, 0.1);
  outline: none;
}

.gemar-input-with-action {
  display: flex;
  gap: 8px;
}

.gemar-add-button {
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

.gemar-add-button:hover {
  background: #e9ecef;
  color: #001a3d;
}

.gemar-add-button i {
  font-size: 1.1rem;
}

.gemar-disabled {
  font-size: 0.8rem;
  color: #777;
  padding: 8px 0;
}

/* Estilo especial para el campo por situar */
.gemar-por-situar-container {
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 6px;
  overflow: hidden;
  border-color: rgba(var(--bs-secondary-rgb),var(--bs-border-opacity)) !important;
}

.gemar-por-situar-input {
  flex: 1;
  border: none;
  padding: 8px 12px;
  font-size: 0.85rem;
  min-width: 0;
}

.gemar-por-situar-suffix {
  background: #f8f9fa;
  padding: 8px 12px;
  font-size: 0.8rem;
  color: #666;
  border-left: 1px solid #ddd;
}

/* Botones de acción */
.gemar-form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.gemar-button {
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

.gemar-button.primary {
  background: #002a68;
  color: white;
}

.gemar-button.primary:hover {
  background: #003d8f;
}

.gemar-button.secondary {
    background:rgb(241, 81, 63);
    color: white;
}

.gemar-button.secondary:hover {
    background:rgb(228, 56, 37);
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
.gemar-select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 12px;
}

/* Estilos para el modal */
.gemar-modal-overlay {
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

.gemar-modal-container {
  background: white;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow: auto;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
  animation: modalFadeIn 0.3s ease-out;
}

.gemar-modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #002a68;
  color: white;
  border-radius: 10px 10px 0 0;
}

.gemar-modal-header h3 {
  margin: 0;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.gemar-modal-close {
  background: transparent;
  border: none;
  color: white;
  font-size: 1.3rem;
  cursor: pointer;
  padding: 5px;
  transition: all 0.2s;
}

.gemar-modal-close:hover {
  color: #ccc;
}

.gemar-modal-body {
  padding: 20px;
}

.gemar-form-row {
  display: flex;
  gap: 15px;
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