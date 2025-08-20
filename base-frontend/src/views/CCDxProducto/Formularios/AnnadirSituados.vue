<template>
  <div class="ufc-header">
    <h6>Partes UFC</h6>
  </div>
  <Navbar-Component />
  <div class="container py-3" style="margin-left: 20em; width: 70%">
    <div class="card border">  
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-file-earmark-plus me-2"></i> Nuevo registro vagón situado
        </h5>
      </div>
      <div class="card-body p-3">
        <form @submit.prevent="submitForm">
          <div class="row">
            <div class="col-md-6">

              <div class="mb-3">
                <label for="fecha_registro" class="form-label small fw-semibold text-secondary"> Fecha de registro</label>
                <input
                  disabled
                  type="text"
                  class="form-control form-control-sm border-secondary"
                  style="padding: 8px 12px"
                  :value="formData.fecha_registro"
                  id="fecha_registro"
                  name="fecha_registro"
                  readonly/>
              </div>

              <div class="mb-3">
                <label for="tipo_origen" class="form-label small fw-semibold text-secondary">Tipo de Acceso</label>
                <select
                  class="form-select form-select-sm border-secondary"
                  style="padding: 8px 12px"
                  v-model="formData.acceso_id"
                  required
                  oninvalid="this.setCustomValidity('Por favor, seleccione un tipo de')"
                  oninput="this.setCustomValidity('')">
                  <option value="" disabled>Seleccione un acceso</option>
                  <option v-for="item in accesosList" :key="item.id" :value="item.id">
                    {{ item.nombre }}
                  </option>
                </select>
              </div>

              <div class="mb-3">
                <label for="tipo_equipo" class="form-label small fw-semibold text-secondary">Tipo de Equipo Ferroviario</label>
                <select 
                  class="form-select form-select-sm border-secondary"
                  style="padding: 8px 12px"
                  v-model="formData.tipo_equipo_id"
                  @change="get_equipos"
                  required
                  oninvalid="this.setCustomValidity('Por favor, seleccione un tipo de equipo ferroviario')"
                  oninput="this.setCustomValidity('')">
                  <option value="" disabled>Seleccione un tipo</option>
                  <option v-for="equipo in tipoEquiposList" :key="equipo.id" :value="equipo.id">
                    {{equipo.tipo_equipo_name}}-{{equipo.tipo_carga_name}}
                  </option>
                </select>
              </div>

              <div class="mb-3">
                <label for="cantidad_vagones" v-if="equiposList.length == 0 && equipoSeleccionado" class="form-label small fw-semibold text-secondary">Deshabilitado - No existen vagones</label>
                <label for="cantidad_vagones" v-if="formData.tipo_equipo_id < 0" class="form-label small fw-semibold text-secondary">Deshabilitado - Seleccione un tipo de equipo ferroviario</label>
                <label for="cantidad_vagones" v-if="equiposList.length != 0 && formData.tipo_equipo_id > 0" class="form-label small fw-semibold text-secondary">Vagones en tren - Cantidad Máxima {{this.equiposList.length}}</label>
                <div class="ufc-por-situar-container">
                  <input  oninvalid="this.setCustomValidity('Por favor, seleccione un tipo de equipo ferroviario')" :disabled="formData.tipo_equipo_id < 0 || equiposList.length == 0" type="number" class="ufc-por-situar-input" v-model="formData.cantidad_vagones" :max="`${this.equiposList.length}`" min="1" required/>
                  <span class="ufc-por-situar-suffix">unidades</span>
                </div>
              </div>
            </div>
             
            <div class="col-md-6">
              <div class="mb-3">
                <label for="estado" class="form-label small fw-semibold text-secondary">Estado</label>
                <select
                  class="form-select form-select-sm border-secondary"
                  style="padding: 8px 12px"
                  v-model="formData.estado">
                  <option value="cargado">Cargado</option>
                  <option value="vacio">Vacío</option>
                </select>
              </div>

              <div class="mb-3">
                <label for="operacion"class="form-label small fw-semibold text-secondary">Operación</label>
                <input
                  type="text"
                  class="form-control form-control-sm border-secondary"
                  style="padding: 8px 12px"
                  v-model="formData.operacion"
                  id="operacion"
                  name="operacion"
                  readonly/>
              </div>

              <div class="mb-3">
                <div class="mb-3">
                  <label for="productos" class="form-label small fw-semibold text-secondary">Productos</label>
                  <div class="ufc-input-with-action">
                    <select v-if="productosList.length > 0"
                      class="form-select form-select-sm border-secondary"
                      style="padding: 8px 12px"
                      v-model="formData.producto_id"
                      @change="get_realCargaDescarga"
                      required
                      oninvalid="this.setCustomValidity('Por favor, seleccione un Producto')"
                      oninput="this.setCustomValidity('')">
                      <option value="" disabled>Seleccione un Producto</option>
                      <option v-for="producto in productosList" :key="producto.id" :value="producto.id">
                        {{producto.producto.nombre_producto}}-{{producto.producto.codigo_producto}}-{{ producto.tipo_embalaje.nombre_tipo_embalaje }}
                      </option>
                    </select>
                    <select v-else
                      class="form-select form-select-sm border-secondary"
                      style="padding: 8px 12px"
                      disabled>
                      <option value="">Seleccione primero el tipo de equipo</option>
                    </select>
                    <button class="create-button ms-2" @click.stop.prevent="abrirModal">
                      <i class="bi bi-plus-circle large-icon"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div class="mb-3">
              <label for="causas" class="form-label small fw-semibold text-secondary">Causas del Incumplimiento</label>
              <textarea
                class="form-control form-control-sm border-secondary"
                v-model="formData.causas_incumplimiento"
                rows="3">
              </textarea>
            </div>
          </div>
          <div class="modal-footer">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <button class="ufc-button secondary" @click="volver_principal">
                <i class="bi bi-x-circle" me-1></i>Cancelar
              </button>
              <button type="submit" class="ufc-button primary">
                <i class="bi bi-check-circle" me-1></i>Añadir
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>

  <div v-if="mostrarModalVagon" class="ufc-modal-overlay">
    <div class="ufc-modal-container">
      <div class="ufc-modal-header">
        <h3><i class="bi bi-train-freight-front"></i> Añadir</h3>
        <button @click="cerrarModalVagon" class="ufc-modal-close">
          <i class="bi bi-x"></i>
        </button>
      </div>
      <div class="ufc-modal-body">
        <div class="ufc-form-grid">
          <div class="ufc-input-group">
            <label for="equipo_ferroviario">Equipo Ferroviario</label>
            <select
              class="ufc-select"
              v-model="nuevoVagon.equipo_ferroviario"
              required>
              <option value="" disabled>Seleccione un equipo</option>
              <option v-for="equipo in equiposList" :key="equipo.id"  :value="equipo.id">
                {{ equipo.numero_identificacion }} -{{ equipo.tipo_equipo_name }}
              </option>
            </select>
          </div>

          <div class="ufc-input-group">
            <label for="cant_dias">Cantidad de días</label>
            <input
              type="number"
              class="ufc-input"
              v-model.number="nuevoVagon.cant_dias"
              min="1"
              required/>
          </div>
        </div>

        <div class="ufc-form-actions">
          <button
            type="button"
            class="ufc-button secondary"
            @click="cerrarModalVagon">
            <i class="bi bi-x-circle"></i> Cancelar
          </button>
          <button
            type="button"
            class="ufc-button primary"
            @click="annadirNuevoVagon()">
            <i class="bi bi-check-circle"></i> Añadir
          </button>
        </div>
      </div>
    </div>
  </div>

  <ModalAgregarProductoCCD 
    v-if="mostrarModalProducto" 
    :visible="mostrarModalProducto" 
    @cerrar-modal="cerrarModal"/>

  <div class="container py-3" style="margin-left: 20em; width: 70%">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-train-freight-front"></i> Vagones 
        </h5>
      </div>
      <div class="card-body p-3">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <button class="btn btn-primary" @click="abrirModalVagon()">
            <i class="bi bi-plus-circle"></i> Añadir
          </button>
        </div>
        <!-- Tabla responsive con mejoras -->
        <div class="table table-responsive">
          <table class="table table-sm table-bordered table-hover">
            <thead class="table-light">
              <tr>
                <th scope="col">No.</th>
                <th scope="col">No. ID en trenes</th>
                <th>Cant. días</th>
                <th scope="col">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in vagonesAnnadidos" :key="index">
                <td>{{ index + 1 }}</td>
                <td>
                  {{item.datos?.equipo_vagon || item.equipo_ferroviario.numero_identificacion}}
                </td>
                <td>
                  {{ item.cant_dias }}
                </td>
                <td>
                  <button
                    class="btn btn-sm btn-outline-danger"
                    @click="eliminarVagon(index)">
                    <i class="bi bi-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Validación de cantidad de vagones -->
        <div class="ufc-validation-message" :class="{ warning: vagonesAnnadidos.length < formData.cantidad_vagones, success: vagonesAnnadidos.length === formData.cantidad_vagones, error: vagonesAnnadidos.length > formData.cantidad_vagones,}">
          <p v-if="vagonesAnnadidos.length < formData.cantidad_vagones">
            Faltan
            {{ formData.cantidad_vagones - vagonesAnnadidos.length }}
            vagones por añadir.
          </p>
          <p v-if="vagonesAnnadidos.length > formData.cantidad_vagones">
            Existen
            {{ vagonesAnnadidos.length  - formData.cantidad_vagones}}
            vagones sobrantes.
          </p>
          <p v-else-if="vagonesAnnadidos.length === formData.cantidad_vagones">
            Todos los vagones han sido añadidos.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";
import NavbarComponent from "@/components/NavbarComponent.vue";
import ModalAgregarProductoCCD from "@/components/CCDxProductosComponents/ModalAgregarProductoCCD.vue";


export default {
  name: "AnnadirSituados",
  components: {
    NavbarComponent,
    ModalAgregarProductoCCD,
  },
  props: {

  },
  data() {
    return {
      formData: {
        fecha_registro:'',
        estado: 'cargado',
        operacion: '',
        cantidad_vagones: 1,
        causas_incumplimiento: '',
        acceso_id: -1,
        tipo_equipo_id: -1,
        producto_id: -1,
        equipo_vagon:[]
      },
      equipoSeleccionado:false,
      vagonesAnnadidos: [],

      mostrarModalProducto: false,
      mostrarModalVagon: false,

      nuevoVagon: {
        equipo_ferroviario: "",
        cant_dias: 1,
      },

      informeCCDxProductoId: '',
      accesosList: [],
      tipoEquiposList: [],
      equiposList: [],
      productosList: [],
      realCargaDescarga: null,

      userGroups: [], 
      userPermissions: [], 
    };
  },

  watch: {
    "formData.estado": {
      immediate: true,
      handler(newVal) {
        if (newVal === "vacio") {
          this.formData.operacion = "carga";
        } else if (newVal === "cargado") {
          this.formData.operacion = "descarga";
        }
      },
    },
  },

  methods: {
    formatFechaRegistro() {
      const d = new Date();
      const year = d.getFullYear();
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      this.formData.fecha_registro = `${year}-${month}-${day}`;
    },

    async get_accesos() {
      try {
        const response = await axios.get("/api/entidades-acceso-ccd/");
        this.accesosList = response.data;
      } catch (error) {
        this.showErrorToast("Error al obtener los accesos");
      }
    },

    async get_tipoEquipos() {
      try {
        const response = await axios.get("/api/tipo-e-f-no-locomotora/");
        this.tipoEquiposList = response.data;
        //console.log(this.tipoEquiposList)
      } catch (error) {
        this.showErrorToast("Error al obtener los tipos de equipos");
      }
    },

    async get_equipos() {
      try {
        this.equipoSeleccionado=true;
        this.vagonesAnnadidos =[];
        this.formData.cantidad_vagones=1;
        const response = await axios.get(`/api/e-f-no-locomotora/?tipo_equipo=${this.formData.tipo_equipo_id}`);
        this.equiposList = response.data;
        this.get_productosXEquipos();
        //console.log(this.equiposList);
      } catch (error) {
        this.showErrorToast("Error al obtener los equipos");
      }
    },

    async get_productosXEquipos() {
      try {
        const response = await axios.get(`/ufc/ccd-productos/?tipo_equipo__id=${this.formData.tipo_equipo_id}`);
        this.productosList = response.data.results;
        if(this.productosList.length==0){
            this.formData.producto_id=-1;
        }
        console.log(this.productosList);
      } catch (error) {
        this.showErrorToast("Error al obtener los productos");
      }
    },

    async get_realCargaDescarga() {
      try {
        const response = await axios.get(`/ufc/obtener-real-carga-ccd/?tipo_equipo=${this.formData.tipo_equipo_id}&informe=${this.informeCCDxProductoId}&producto=${this.formData.producto_id}`);
        this.realCargaDescarga = response.data;
        console.log(this.realCargaDescarga);
      } catch (error) {
        this.showErrorToast("Error al obtener los equipos");
      }
    },

    abrirModalVagon() {
      if (this.equiposList.length == 0) {
        Swal.fire({
          title: "Error",
          text: "Seleccione el tipo de equipo ferroviario",
          icon: "error",
          showCancelButton: false,
          confirmButtonText: "Aceptar",
          confirmButtonColor: "#ff4444"
        });
        return;
      }
      if (this.vagonesAnnadidos.length == this.formData.cantidad_vagones) {
        Swal.fire({
          title: "Error",
          text: "Ya añadió todos los vagones según la cantidad de vagones definida",
          icon: "error",
          showCancelButton: false,
          confirmButtonText: "Aceptar",
          confirmButtonColor: "#ff4444"
        });
        return;
      }
      this.mostrarModalVagon = true;
    },

    cerrarModalVagon() {
      this.mostrarModalVagon = false;
      this.nuevoVagon = {
        equipo_ferroviario: "",
        cant_dias: 1,
      };
    },

    annadirNuevoVagon() {
      if (this.nuevoVagon.equipo_ferroviario == "") {
        this.showErrorToast("Complete todos los campos");
        return;
      }

      const equipoSeleccionado = this.equiposList.find((e) => e.id === this.nuevoVagon.equipo_ferroviario);
      const yaExistente = this.vagonesAnnadidos.some((vagon) => vagon.equipo_ferroviario.id === this.nuevoVagon.equipo_ferroviario);
      if (yaExistente) {
        this.showErrorToast("Este vagón ya existe");
        return;
      }
      const vagonAgregado = {
        equipo_ferroviario: equipoSeleccionado,
        cant_dias: this.nuevoVagon.cant_dias,
        datos: {
          equipo_vagon: equipoSeleccionado.numero_identificacion,
        },
      };

      this.vagonesAnnadidos.push(vagonAgregado);
      this.cerrarModalVagon();
      this.showSuccessToast("Vagón añadido");
    },

    eliminarVagon(index) {
      this.vagonesAnnadidos.splice(index, 1);
      this.showSuccessToast("Vagón eliminado");
    },

    async submitForm() {
      try {
        if (!this.informeCCDxProductoId) {
          this.showErrorToast("No existe un informe operativo creado para la fecha actual");
          this.$router.push({ name: "ccdxproducto" });
        }
        
        if (this.vagonesAnnadidos.length==0) {
          this.showErrorToast("Añada al menos un vagón");
          return;
        }

        if (this.formData.estado === "cargado" && this.formData.producto_id == -1) {
          this.showErrorToast("Seleccione al menos un producto");
          return;
        }

        if (this.vagonesAnnadidos.length != this.formData.cantidad_vagones) {
          Swal.fire({
            title: "Advertencia",
            text: `El número de vagones asociados (${this.vagonesAnnadidos.length}) no coincide con la cantidad de vagones (${this.formData.por_situar}) definida.`,
            icon: "warning",
            showCancelButton: false,
            confirmButtonText: "Aceptar",
            confirmButtonColor: "#007bff"
          });
          return;
        }

        const payload = {
          fecha_registro: this.formData.fecha_registro,
          estado: this.formData.estado,
          operacion: this.formData.operacion,
          cantidad_vagones: this.formData.cantidad_vagones,
          causas_incumplimiento: this.formData.causas_incumplimiento,
          real_carga_descarga: this.realCargaDescarga.real_carga + this.realCargaDescarga.real_descarga,
          informe_ccd: this.informeCCDxProductoId,
          acceso_id: this.formData.acceso_id,
          tipo_equipo_id: this.formData.tipo_equipo_id,
          producto_id: this.formData.producto_id,

          equipo_vagon: 
            this.vagonesAnnadidos.map((vagon) => ({
              equipo_ferroviario: vagon.equipo_ferroviario.id,
              cant_dias: vagon.cant_dias,
            })),
        };
        
        const response = await axios.post("/ufc/ccd-situados/", payload);
        this.resetForm();
        this.$router.push({ name: "ccdxproducto" });
        this.showSuccessToast("Registro creado");
      } catch (error) {
        this.showErrorToast("Error al enviar el formulario");
        console.log(error)
      }
    },

    async verificarInformeCCDxProducto() {
      try {
        const today = new Date();
        const fechaFormateada = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;
        const response = await axios.get("/ufc/verificar-informe-ccd-existente/", {params: { fecha_operacion: fechaFormateada },});
        if (response.data.existe) {
          this.informeCCDxProductoId = response.data.id;
          return true;
        } 
        return false;
      } catch (error) {
        this.showErrorToast("Error al verificar informe");
        return false;
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
          this.$router.push({ name: "ccdxproducto" });
        }
      });
    },

    resetForm() {
      this.formData = {
        fecha_registro:'',
        estado: 'cargado',
        operacion: '',
        cantidad_vagones: 1,
        causas_incumplimiento: '',
        real_carga_descarga: -1,
        acceso_id: -1,
        tipo_equipo_id: -1,
        producto_id: -1,
        equipo_vagon:[]
      };
    },    

    abrirModal() {
      this.mostrarModalProducto = true;
    },

    cerrarModal() {
      this.mostrarModalProducto = false;
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

    showErrorToast(message) {
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

  async created() {
    this.verificarInformeCCDxProducto();
    this.formatFechaRegistro();
    this.get_accesos();
    this.get_tipoEquipos();

  },
};
</script>

<style scoped>

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

