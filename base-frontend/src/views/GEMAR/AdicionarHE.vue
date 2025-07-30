<template>
  <div class="gemar-header">
    <h6>Partes GEMAR</h6>
  </div>
  <Navbar-Component />
  <div class="container py-3" style="margin-left: 20em; width: 70%">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-clipboard-data me-2"></i>Nuevo registro de hecho extraordinario
        </h5>
      </div>
      <div class="card-body p-3">
        <form @submit.prevent="submitForm">
          <div class="row">
            <!-- Columna 1 -->
            <div class="col-md-6">
              <!-- Campo: Fecha de registro -->
              <div class="mb-3">
                <label for="fecha_registro" class="form-label small fw-semibold text-secondary">Fecha de registro</label>
                <input type="text" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" :value="formattedFechaRegistro" id="fecha_registro" name="fecha_registro" readonly/>
              </div>

              <!-- Campo: Informado -->
              <div class="mb-3">
                <label for="informado" class="form-label small fw-semibold text-secondary">Informado</label>
                <input type="text" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" v-model="formData.informado" id="informado" name="informado" />
              </div>

              <!-- Campo: Garante -->
              <div class="mb-3">
                <label for="garante" class="form-label small fw-semibold text-secondary">Garante/dueño</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" v-model="formData.garante" id="garante" name="garante" >
                  <option value="" disabled>Seleccione un garante</option>
                  <option v-for="entidad in entidades" :key="entidad.id" :value="entidad.id">
                    {{ entidad.id }}-{{ entidad.nombre }}
                  </option>
                </select>
              </div>

              <!-- Campo: Tipo de involucrado -->
              <div class="mb-3">
                <label for="tipo_involucrado" class="form-label small fw-semibold text-secondary">Tipo de involucrado</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" v-model="formData.tipo_involucrado" id="tipo_involucrado" name="tipo_involucrado" >
                  <option value="" disabled selected>Seleccione un tipo</option>
                  <option value="puerto">Puerto</option>
                  <option value="entidad">Entidad</option>
                  <option value="buque">Buque</option>
                </select>
              </div>

              <!-- Campo: Involucrado -->
              <div class="mb-3">
                <label for="involucrado" class="form-label small fw-semibold text-secondary">Involucrado</label>
                <select v-if="formData.tipo_involucrado === 'puerto'" 
                        class="form-select form-select-sm border-secondary" 
                        style="padding: 8px 12px;" 
                        v-model="formData.involucrado" 
                        id="involucrado" 
                        name="involucrado" 
                        >
                  <option value="" disabled>Seleccione un puerto</option>
                  <option v-for="puerto in puertos" :key="puerto.nombre_puerto" :value="puerto.nombre_puerto">
                    {{ puerto.nombre_puerto }}
                  </option>
                </select>
                
                <select v-else-if="formData.tipo_involucrado === 'entidad'" 
                        class="form-select form-select-sm border-secondary" 
                        style="padding: 8px 12px;" 
                        v-model="formData.involucrado" 
                        id="involucrado" 
                        name="involucrado" 
                        >
                  <option value="" disabled>Seleccione una entidad</option>
                  <option v-for="entidad in entidades" :key="entidad.nombre" :value="entidad.nombre">
                    {{ entidad.nombre }}
                  </option>
                </select>
                
                <select v-else-if="formData.tipo_involucrado === 'buque'" 
                        class="form-select form-select-sm border-secondary" 
                        style="padding: 8px 12px;" 
                        v-model="formData.involucrado" 
                        id="involucrado" 
                        name="involucrado" 
                        >
                  <option value="" disabled>Seleccione un buque</option>
                  <option v-for="buque in buques" :key="buque.id" :value="buque.id">
                    {{ buque.nombre_embarcacion }}
                  </option>
                </select>
              </div>

              <!-- Campo: Tipo de origen -->
              <div class="mb-3">
                <label for="tipo_origen" class="form-label small fw-semibold text-secondary">Tipo de origen</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" v-model="formData.tipo_origen" id="tipo_origen" name="tipo_origen" >
                  <option value="" disabled>Seleccione un tipo</option>
                  <option value="puerto">Puerto</option>
                  <option value="entidad">Entidad</option>
                </select>
              </div>
            </div>

            <!-- Columna 2 -->
            <div class="col-md-6">
              <!-- Campo: Origen -->
              <div class="mb-3">
                <label for="origen" class="form-label small fw-semibold text-secondary">Origen</label>
                <select v-if="formData.tipo_origen === 'puerto'" 
                        class="form-select form-select-sm border-secondary" 
                        style="padding: 8px 12px;" 
                        v-model="formData.origen" 
                        id="origen" 
                        name="origen" 
                        >
                  <option value="" disabled>Seleccione un puerto</option>
                  <option v-for="puerto in puertos" :key="puerto.nombre_puerto" :value="puerto.nombre_puerto">
                    {{ puerto.nombre_puerto }}
                  </option>
                </select>
                
                <select v-else-if="formData.tipo_origen === 'entidad'" 
                        class="form-select form-select-sm border-secondary" 
                        style="padding: 8px 12px;" 
                        v-model="formData.origen" 
                        id="origen" 
                        name="origen" 
                        >
                  <option value="" disabled>Seleccione una entidad</option>
                  <option v-for="entidad in entidades" :key="entidad.nombre" :value="entidad.nombre">
                    {{ entidad.nombre }}
                  </option>
                </select>
              </div>

              <!-- Campo: Destino -->
              <div class="mb-3">
                <label for="destino" class="form-label small fw-semibold text-secondary">Destino</label>
                <input type="text" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" v-model="formData.destino" id="destino" name="destino" />
              </div>

              <!-- Campo: Producto involucrado -->
              <div class="mb-3">
                <label for="producto_involucrado" class="form-label small fw-semibold text-secondary">Producto involucrado</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" v-model="formData.producto_involucrado" id="producto_involucrado" name="producto_involucrado" >
                  <option value="" disabled>Seleccione un producto</option>
                  <option v-for="producto in productos" :key="producto.id" :value="producto.id">
                    {{ producto.nombre_producto }}
                  </option>
                </select>
              </div>

              <!-- Campo: Embalaje -->
              <div class="mb-3">
                <label for="embalaje" class="form-label small fw-semibold text-secondary">Embalaje</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" v-model="formData.embalaje" id="embalaje" name="embalaje" >
                  <option value="" disabled>Seleccione un embalaje</option>
                  <option v-for="embalaje in embalajes" :key="embalaje.id" :value="embalaje.id">
                    {{ embalaje.nombre_tipo_embalaje }}
                  </option>
                </select>
              </div>

              <!-- Campo: Unidad de medida -->
              <div class="mb-3">
                <label for="unidad_medida" class="form-label small fw-semibold text-secondary">Unidad de medida</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" v-model="formData.unidad_medida" id="unidad_medida" name="unidad_medida" >
                  <option value="" disabled>Seleccione una unidad</option>
                  <option v-for="unidad in unidadesMedida" :key="unidad.id" :value="unidad.id">
                    {{ unidad.unidad_medida }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <!-- Campos de diferencia -->
          <div class="row mt-3">
            <div class="col-md-6">
              <h6 class="fw-semibold">Datos de diferencia</h6>
              
              <!-- Campo: Tipo de diferencia -->
              <div class="mb-3">
                <label for="tipo_diferencia" class="form-label small fw-semibold text-secondary">Tipo de diferencia</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" v-model="formData.tipo_diferencia" id="tipo_diferencia" name="tipo_diferencia" >
                  <option value="" disabled>Seleccione un tipo</option>
                  <option value="sobrante">Sobrante</option>
                  <option value="faltante">Faltante</option>
                </select>
              </div>

              <!-- Campo: KG Diferencia -->
              <div class="mb-3">
                <label for="kg_diferencia" class="form-label small fw-semibold text-secondary">KG Diferencia</label>
                <input type="number" step="0.01" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" v-model="formData.kg_diferencia" id="kg_diferencia" name="kg_diferencia"/>
              </div>

              <!-- Campo: Cantidad Diferencia -->
              <div class="mb-3">
                <label for="cantidad_diferencia" class="form-label small fw-semibold text-secondary">Cantidad Diferencia</label>
                <input type="number" step="0.01" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" v-model="formData.cantidad_diferencia" id="cantidad_diferencia" name="cantidad_diferencia"/>
              </div>

              <!-- Campo: Valor Diferencia -->
              <div class="mb-3">
                <label for="valor_diferencia" class="form-label small fw-semibold text-secondary">Valor Diferencia</label>
                <input type="number" step="0.01" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" v-model="formData.valor_diferencia" id="valor_diferencia" name="valor_diferencia"/>
              </div>
            </div>

            <div class="col-md-6">
              <h6 class="fw-semibold">Datos de avería</h6>
              
              <!-- Campo: Avería -->
              <div class="mb-3">
                <label for="averia" class="form-label small fw-semibold text-secondary">Avería</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" v-model="formData.averia" id="averia" name="averia">
                  <option value="no">No</option>
                  <option value="si">Sí</option>
                </select>
              </div>

              <!-- Campos de avería (mostrar solo si averia es 'si') -->
              <template v-if="formData.averia === 'si'">
                <!-- Campo: KG Avería -->
                <div class="mb-3">
                  <label for="kg_averia" class="form-label small fw-semibold text-secondary">KG Avería</label>
                  <input type="number" step="0.01" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" v-model="formData.kg_averia" id="kg_averia" name="kg_averia"/>
                </div>

                <!-- Campo: Cantidad Avería -->
                <div class="mb-3">
                  <label for="cantidad_averia" class="form-label small fw-semibold text-secondary">Cantidad Avería</label>
                  <input type="number" step="0.01" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" v-model="formData.cantidad_averia" id="cantidad_averia" name="cantidad_averia"/>
                </div>

                <!-- Campo: Valor Avería -->
                <div class="mb-3">
                  <label for="valor_averia" class="form-label small fw-semibold text-secondary">Valor Avería</label>
                  <input type="number" step="0.01" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" v-model="formData.valor_averia" id="valor_averia" name="valor_averia"/>
                </div>
              </template>
            </div>
          </div>

          <!-- Campo: Incidencia involucrada -->
          <div class="mb-3">
            <label for="incidencia_involucrada" class="form-label small fw-semibold text-secondary">Incidencia involucrada</label>
            <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" v-model="formData.incidencia_involucrada" id="incidencia_involucrada" name="incidencia_involucrada" >
              <option value="" disabled>Seleccione una incidencia</option>
              <option v-for="incidencia in incidencias" :key="incidencia.id" :value="incidencia.id">
                {{ incidencia.id }}-{{ incidencia.nombre_incidencia }}
              </option>
            </select>
          </div>

          <!-- Campo: Descripción del hecho -->
          <div class="mb-3">
            <label for="descripcion_hecho" class="form-label small fw-semibold text-secondary">Descripción del hecho</label>
            <textarea class="form-control form-control-sm border-secondary" v-model="formData.descripcion_hecho" id="descripcion_hecho" name="descripcion_hecho" rows="4" ></textarea>
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
  name: "AdicionarHechoExtraordinario",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      formData: {
        informado: "",
        garante: "",
        tipo_involucrado: "puerto",
        involucrado: "",
        tipo_origen: "puerto",
        origen: "",
        destino: "",
        producto_involucrado: "",
        embalaje: "",
        unidad_medida: "",
        tipo_diferencia: "",
        kg_diferencia: null,
        cantidad_diferencia: null,
        valor_diferencia: null,
        averia: "no",
        kg_averia: null,
        cantidad_averia: null,
        valor_averia: null,
        incidencia_involucrada: "",
        descripcion_hecho: "",
        parte_hecho_extraordinario: null,
      },
      puertos: [],
      buques: [],
      entidades: [],
      productos: [],
      embalajes: [],
      unidadesMedida: [],
      incidencias: [],
      informeOperativoId: null,
      fechaActual: new Date().toISOString().split('T')[0],
      errors: '',
    };
  },

  watch: {
    'formData.tipo_involucrado'(newVal) {
      // Resetear el valor del involucrado cuando cambia el tipo
      this.formData.involucrado = "";
      
      // Cargar los datos correspondientes según el tipo seleccionado
      if (newVal === 'puerto') {
        this.getPuertos();
      } else if (newVal === 'entidad') {
        // Las entidades ya están cargadas en mounted()
      } else if (newVal === 'buque') {
        this.getBuques();
      }
    }
  },

  computed: {
    formattedFechaRegistro() {
      return new Date().toLocaleString();
    }
  },

  mounted() {
    this.getEntidades();
    this.getProductos();
    this.getEmbalajes();
    this.getUnidadesMedida();
    this.getIncidencias();
    this.verificarExisteParteHE();
  },

  methods: {

    validateForm() {
      this.errors = '';
      const validacion_regex = /^[\w\d\W ]{3,100}$/;
      let valid = true;
      //agregando texto inicial a errors en caso de que existaalgun campo requerido vacio
      if (!this.formData.informado || !this.formData.garante || 
            !this.formData.tipo_involucrado || !this.formData.involucrado || 
            !this.formData.tipo_origen || !this.formData.origen || 
            !this.formData.destino || !this.formData.producto_involucrado || 
            !this.formData.descripcion_hecho) {          
          this.errors += 'Los siguientes campos son obligatorios:<br>';
        }
      // Validar campo informado
      if (!this.formData.informado) {
        this.errors += '- Informado.<br>';
        valid = false;
      }

      // Validar campo garante
      if (!this.formData.garante) {
        this.errors += '- Garante/Dueño.<br>';
        valid = false;
      }

      // Validar campo involucrado
      if (!this.formData.involucrado) {
        this.errors += '- Involucrado.<br>';
        valid = false;
      }     

      // Validar campo origen
      if (!this.formData.origen) {
        this.errors += '- Origen.<br>';
        valid = false;
      }

      // Validar campo destino
      if (!this.formData.destino) {
        this.errors += '- Destino.<br>';
        valid = false;
      } 

      // Validar campo producto_involucrado
      if (!this.formData.producto_involucrado) {
        this.errors += '- Producto.<br>';
        valid = false;
      }

      // Validar campo descripcion_hecho
      if (!this.formData.descripcion_hecho) {
        this.errors += '- Descripción del hecho.<br>';
        valid = false;
      }

      if (!validacion_regex.test(this.formData.informado)) {
        this.errors += 'El campo "Informado" acepta letras, números y caracteres especiales, entre 3 y 100 caracteres.<br>';
        valid = false;
      }      
      if (!validacion_regex.test(this.formData.destino)) {
        this.errors += 'El campo "Destino" acepta letras, números y caracteres especiales, entre 3 y 100 caracteres.<br>';
        valid = false;
      }
      if (!validacion_regex.test(this.formData.descripcion_hecho)) {
        this.errors += 'El campo "Descripción del hecho" es un campo de texto enriquecido. Admite números, letras y caracteres especiales.';
        valid = false;
      }

      return valid;
    },

    async verificarExisteParteHE() {
      try {
        const today = new Date();
        const fechaFormateada = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;

        const response = await axios.get('/gemar/gemar-verificar-informe-existente/', {
          //enviando el parametro a la vista del backend
            params: { fecha_actual: fechaFormateada }
        });

        if (response.data.existe) {
          this.informeOperativoId = response.data.id;
          this.formData.parte_hecho_extraordinario = response.data.id;
          return true;
        }
        return false;
      } catch (error) {
        console.error("Error al verificar informe:", error);
        return false;
      }
    },
    
    async submitForm() {
      // Validar el formulario antes de enviarlo
        
      if (!this.validateForm()) {
        Swal.fire('Errores en la entrada de datos', this.errors, 'error');
        
        return; // Si la validación falla, no enviar el formulario
      }

      try {
        const existeInforme = await this.verificarExisteParteHE();
        if (!existeInforme) {
          Swal.fire(
            "Error",
            "No existe un informe de HE creado para la fecha actual. Debe crear uno primero.",
            "error"
          );
          this.$router.push({ name: "gemar_hecho_extraordinario" });
          return;
        }

        

        // Preparar datos para enviar
        const datosEnvio = {
          ...this.formData,
          parte_hecho_extraordinario: this.informeOperativoId
        };

        // Enviar datos
        const response = await axios.post("/gemar/gemar-hechos-extraordinarios/", datosEnvio);
        
        // Mostrar mensaje de éxito
        this.showSuccessToast("El hecho extraordinario ha sido registrado correctamente");
        this.resetForm();
        this.$router.push({ name: "gemar_hecho_extraordinario" });
        
      } catch (error) {
        console.error("Error detallado:", error.response?.data);
        let errorMsg = "Error al registrar el hecho extraordinario";
        this.MensajeTemporaldeError("Error al registrar el hecho extraordinario");
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
        informado: "",
        garante: "",
        tipo_involucrado: "puerto",
        involucrado: "",
        tipo_origen: "puerto",
        origen: "",
        destino: "",
        producto_involucrado: "",
        embalaje: "",
        unidad_medida: "",
        tipo_diferencia: "",
        kg_diferencia: null,
        cantidad_diferencia: null,
        valor_diferencia: null,
        averia: "no",
        kg_averia: null,
        cantidad_averia: null,
        valor_averia: null,
        incidencia_involucrada: "",
        descripcion_hecho: "",
        parte_hecho_extraordinario: null,
      };
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

    async getBuques() {
      try {
        const response = await axios.get("/api/embarcaciones/?tipo_embarcacion=buque");
        this.buques = response.data.results;
        console.log("Aqui estan los buques",this.buques);
      } catch (error) {
        console.error("Error al obtener los buques:", error);
        Swal.fire("Error", "Hubo un error al obtener los buques.", "error");
      }
    },

    async getEntidades() {
      try {
        const response = await axios.get("/api/entidades/");
        this.entidades = response.data.results;
      } catch (error) {
        console.error("Error al obtener las entidades:", error);
        Swal.fire("Error", "Hubo un error al obtener las entidades.", "error");
      }
    },

    async getProductos() {
      try {
        const response = await axios.get("/api/productos/");
        this.productos = response.data.results;
      } catch (error) {
        console.error("Error al obtener los productos:", error);
        Swal.fire("Error", "Hubo un error al obtener los productos.", "error");
      }
    },

    async getEmbalajes() {
      try {
        const response = await axios.get("/api/embalajes/");
        this.embalajes = response.data.results;
      } catch (error) {
        console.error("Error al obtener los embalajes:", error);
        Swal.fire("Error", "Hubo un error al obtener los embalajes.", "error");
      }
    },

    async getUnidadesMedida() {
      try {
        const response = await axios.get("/api/unidades_medida/");
        this.unidadesMedida = response.data.results;
      } catch (error) {
        console.error("Error al obtener las unidades de medida:", error);
        Swal.fire("Error", "Hubo un error al obtener las unidades de medida.", "error");
      }
    },

    async getIncidencias() {
      try {
        const response = await axios.get("/api/incidencias/");
        this.incidencias = response.data.results;
      } catch (error) {
        console.error("Error al obtener las incidencias:", error);
        Swal.fire("Error", "Hubo un error al obtener las incidencias.", "error");
      }
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
          this.$router.push({ name: "gemar_hecho_extraordinario" });
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