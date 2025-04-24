<template>
  <div class="ufc-header">
    <h6>Bienvenido:</h6>
  </div>
  <Navbar-Component />
  <Producto-Vagones />
  <div class="ufc-form-container">
    <div class="ufc-form-wrapper">
      <div class="ufc-form-card">
        <h2 class="ufc-form-title">
          <i class="bi bi-clipboard-plus"></i>
          Nuevo registro de situados
        </h2>

        <form @submit.prevent="submitForm">
          <div class="ufc-form-grid">
            <!-- Columna 1 -->
            <div>
              <!-- Campo: tipo_origen -->
              <div class="ufc-input-group">
                <label for="tipo_origen">
                  Tipo de Origen <span class="required">*</span>
                </label>
                <select
                  class="ufc-select"
                  v-model="formData.tipo_origen"
                  id="tipo_origen"
                  name="tipo_origen"
                  required
                  :disabled="isSubmitting"
                  @change="handleTipoOrigenChange"
                >
                  <option value="" disabled>Seleccione un tipo</option>
                  <option 
                    v-for="option in tipo_origen_options" 
                    :key="option.id"
                    :value="option.id"
                  >
                    {{ option.text }}
                  </option>
                </select>
              </div>

              <!-- Campo: origen -->
<div class="ufc-input-group">
  <label for="origen">
    Origen <span class="required">*</span>
  </label>
  <select
    v-if="formData.tipo_origen === 'ac_ccd'"
    class="ufc-select"
    v-model="formData.origen"
    id="origen"
    name="origen"
    required
    :disabled="isSubmitting"
  >
    <option value="" disabled>Seleccione un origen</option>
    <option
      v-for="entidad in entidades"
      :key="entidad.id"
      :value="entidad.nombre"
    >
      {{ entidad.id }}-{{ entidad.nombre }}
    </option>
  </select>

  <select
    v-else-if="formData.tipo_origen === 'puerto'"
    class="ufc-select"
    v-model="formData.origen"
    id="origen"
    name="origen"
    required
    :disabled="isSubmitting"
  >
    <option value="" disabled>Seleccione un puerto</option>
    <option
      v-for="puerto in puertos"
      :key="puerto.id"
      :value="puerto.nombre_puerto"
    >
      {{ puerto.id }}- {{ puerto.nombre_puerto }}
    </option>
  </select>
  
  <select
    v-else
    class="ufc-select"
    disabled
  >
    <option value="">Seleccione primero el tipo de origen</option>
  </select>
</div>

              <!-- Campo: tipo_equipo -->
              <div class="ufc-input-group">
  <label for="tipo_equipo">
    Tipo de Equipo <span class="required">*</span>
  </label>
  <select
    class="ufc-select"
    v-model="formData.tipo_equipo"
    id="tipo_equipo"
    name="tipo_equipo"
    required
    :disabled="isSubmitting"
  >
    <option value="" disabled>Seleccione un tipo</option>
    <option 
      v-for="option in tipo_equipo_options" 
      :key="option.id"
      :value="option.id"
    >
      {{ option.text }}
    </option>
  </select>
</div>

              <!-- Campo: estado -->
              <div class="ufc-input-group">
                <label for="estado">
                  Estado <span class="required">*</span>
                </label>
                <select
                  class="ufc-select"
                  v-model="formData.estado"
                  id="estado"
                  name="estado"
                  required
                  :disabled="isSubmitting"
                >
                  <option value="cargado">Cargado</option>
                  <option value="vacio">Vacio</option>
                </select>
              </div>

              <!-- Campo: operacion -->
<div class="ufc-input-group">
  <label for="operacion">
    Operación <span class="required">*</span>
  </label>
  <select
    class="ufc-select"
    v-model="formData.operacion"
    id="operacion"
    name="operacion"
    required
    :disabled="isSubmitting"
  >
    <option value="" disabled>Seleccione una operación</option>
    <option 
      v-for="option in t_operacion_options" 
      :key="option.id"
      :value="option.id"
    >
      {{ option.text }}
    </option>
  </select>
</div>
            </div>

            <!-- Columna 2 -->
            <div>
              <!-- Campo: producto -->
              <div class="ufc-input-group">
                <label for="productos">Productos</label>
                <div class="ufc-input-with-action">
                  <select
                    v-if="formData.estado === 'cargado'"
                    class="ufc-select"
                    v-model="formData.productos"
                    multiple
                    :disabled="isSubmitting || loadingProducts"
                    :required="formData.estado === 'cargado' && formData.productos.length === 0"
                  >
                    <option value="" disabled>Seleccione uno o más productos</option>
                    <option
                      v-for="producto in productos"
                      :key="producto.id"
                      :value="producto.id"
                    >
                      {{ producto.id }}-{{ producto.producto_name }} - {{ producto.producto_codigo }}
                    </option>
                  </select>
                  <button
                    v-if="formData.estado === 'cargado'"
                    class="ufc-add-button"
                    @click.prevent="abrirModalAgregarProducto"
                    :disabled="isSubmitting"
                  >
                    <i class="bi bi-plus-lg"></i>
                  </button>
                  <div v-if="loadingProducts" class="ufc-disabled">
                    <i class="bi bi-arrow-repeat"></i> Cargando productos...
                  </div>
                </div>
                <div v-if="formData.estado !== 'cargado'" class="ufc-disabled">
                  (Seleccione "Cargado" para ver los productos)
                </div>
                <div v-if="formData.productos.length > 0" class="ufc-selected-products">
                  Seleccionados: {{ formData.productos.length }}
                </div>
              </div>
              
              <ModalAgregarProducto
                v-if="mostrarModal"
                :visible="mostrarModal"
                @cerrar-modal="cerrarModal"
              />

              <!-- Campo: situados -->
              <div class="ufc-input-group">
                <label for="situados">
                  Situados <span class="required">*</span>
                </label>
                <div class="ufc-por-situar-container">
                  
                  <input
                    type="number"
                    class="ufc-por-situar-input"
                    v-model.number="formData.situados"
                    id="situados"
                    name="situados"
                    min="1"
                    required
                    :disabled="isSubmitting"
                  />
                  
                </div>
              </div>

              <!-- Campo: pendiente_proximo_dia -->
              <div class="ufc-input-group">
                <label for="pendiente_proximo_dia">
                  Pendientes al próximo día <span class="required">*</span>
                </label>
                <div class="ufc-por-situar-container">
                  
                  <input
                    type="number"
                    class="ufc-por-situar-input"
                    v-model.number="formData.pendiente_proximo_dia"
                    id="pendiente_proximo_dia"
                    name="pendiente_proximo_dia"
                    min="0"
                    required
                    :disabled="isSubmitting"
                  />
                  
                </div>
              </div>

              <!-- Campo: observaciones -->
              <div class="ufc-input-group">
                <label for="observaciones">Observaciones</label>
                <textarea
                  class="ufc-textarea"
                  v-model="formData.observaciones"
                  id="observaciones"
                  name="observaciones"
                  rows="3"
                  :disabled="isSubmitting"
                ></textarea>
              </div>
            </div>
          </div>

          <div class="ufc-form-actions">
            <button
              type="submit"
              class="ufc-button primary"
              :disabled="isSubmitting"
            >
              <span v-if="isSubmitting">
                <span class="spinner" role="status" aria-hidden="true"></span>
                Procesando...
              </span>
              <span v-else>Agregar</span>
            </button>
            <button
              type="button"
              @click="confirmCancel"
              class="ufc-button secondary"
              :disabled="isSubmitting"
            >
              Cancelar
            </button>
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
import ModalAgregarProducto from "@/components/ModalAgregarProducto.vue";

export default {
  name: "AdicionarSituados",
  components: {
    NavbarComponent,
    ModalAgregarProducto,
  },
  data() {
    return {
        formData: {
        tipo_origen: "",
        origen: "",
        tipo_equipo: "",
        estado: "cargado",
        operacion: "",
        productos: [], // Cambiamos de producto (singular) a productos (array)
        situados: 1,
        pendiente_proximo_dia: 0,
        observaciones: "",
      },
      entidades: [],
      puertos: [],
      productos: [],
      mostrarModal: false,
      loadingProducts: false,
      isSubmitting: false,

      tipo_origen_options: [
        { id: "ac_ccd", text: "comercial/AccesoCCD" },
        { id: "puerto", text: "Puerto" },
      ],
      tipo_equipo_options: [
        { id: "casilla", text: "Casilla" },
        { id: "caj_gon", text: "Cajon o Gondola" },
      ],
      t_operacion_options: [
        { id: "carga", text: "Carga" },
        { id: "descarga", text: "Descarga" },
      ],
    };
  },
  mounted() {
    this.getProductos();
    this.getEntidades();
    this.getPuertos();
  },
  methods: {
    async getEntidades() {
      try {
        const response = await axios.get("/api/entidades/");
        this.entidades = response.data.results;
      } catch (error) {
        console.error("Error al obtener entidades:", error);
        Swal.fire("Error", "No se pudieron obtener las entidades", "error");
      }
    },

    async getProductos() {
      try {
        let allProductos = [];
        let nextPage = "/ufc/producto-vagon/"; // URL inicial

        while (nextPage) {
          const response = await axios.get(nextPage);
          allProductos = [...allProductos, ...response.data.results];

          // Actualiza nextPage con la URL de la siguiente página (null si no hay más)
          nextPage = response.data.next;
        }

        this.productos = allProductos;
      } catch (error) {
        console.error("Error al obtener los productos:", error);
        Swal.fire("Error", "Hubo un error al obtener los productos.", "error");
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

    handleTipoOrigenChange() {
      this.formData.origen = "";
      if (this.formData.tipo_origen === 'ac_ccd') {
        this.formData.tipo_origen = 'ac_ccd';
      } else if (this.formData.tipo_origen === 'puerto') {
        this.formData.tipo_origen = 'puerto';
      }
    },

    abrirModalAgregarProducto() {
      this.mostrarModal = true;
    },

    cerrarModal() {
      this.mostrarModal = false;
      this.getProductos();
    },

    increment(field) {
      this.formData[field] += 1;
    },

    decrement(field) {
      if (this.formData[field] > (field === 'situados' ? 1 : 0)) {
        this.formData[field] -= 1;
      }
    },

    async submitForm() {
      this.isSubmitting = true;
      try {
        // Validación mejorada
        const errors = [];

        if (!this.formData.tipo_origen || 
    !this.tipo_origen_options.some(opt => opt.id === this.formData.tipo_origen)) {
  errors.push("Seleccione un tipo de origen válido");
}

        if (!this.formData.origen) {
          errors.push("El campo Origen es requerido");
        }

        if (!this.formData.tipo_equipo) {
          errors.push("El campo Tipo de Equipo es requerido");
        }

        if (!this.formData.operacion) {
          errors.push("El campo Operación es requerido");
        }

        if (this.formData.estado === "cargado" && this.formData.productos.length === 0) {
          throw new Error("Debe seleccionar al menos un producto cuando el estado es Cargado");
        }

        if (this.formData.situados === null || this.formData.situados < 1) {
          errors.push("La cantidad de situados debe ser al menos 1");
        }

        if (
          this.formData.pendiente_proximo_dia === null ||
          this.formData.pendiente_proximo_dia < 0
        ) {
          errors.push(
            "Los pendientes al próximo día deben ser un número positivo"
          );
        }

        if (errors.length > 0) {
          throw new Error(errors.join("\n"));
        }

        // Preparar datos para enviar
        const payload = {
          tipo_origen: this.formData.tipo_origen,
          origen: this.formData.origen,
          tipo_equipo: this.formData.tipo_equipo,
          estado: this.formData.estado,
          operacion: this.formData.operacion,
          producto: this.formData.productos, // Array de IDs
          situados: this.formData.situados,
          pendiente_proximo_dia: this.formData.pendiente_proximo_dia,
          observaciones: this.formData.observaciones,
        };
        // Configuración de axios para manejar mejor los errores
        const config = {
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          validateStatus: function (status) {
            return status >= 200 && status < 500;
          },
        };

        // Enviar datos al endpoint
        const response = await axios.post(
          "http://127.0.0.1:8000/ufc/situados/",
          payload,
          config
        );

        if (response.status === 201) {
          await Swal.fire({
            title: "Éxito",
            text: "Registro creado correctamente",
            icon: "success",
          });
          this.resetForm();
          this.$router.push({ name: "InfoOperativo" });
        } else {
          let errorMessage = "Error al crear el registro";
          if (response.data) {
            // Procesar errores del backend
            if (typeof response.data === "string") {
              errorMessage = response.data;
            } else if (response.data.detail) {
              errorMessage = response.data.detail;
            } else if (response.data.non_field_errors) {
              errorMessage = response.data.non_field_errors.join(", ");
            } else {
              errorMessage = Object.entries(response.data)
                .map(
                  ([key, value]) =>
                    `${key}: ${Array.isArray(value) ? value.join(", ") : value}`
                )
                .join("\n");
            }
          }
          throw new Error(errorMessage);
        }
      } catch (error) {
        console.error("Error en submitForm:", error);
        Swal.fire({
          title: "Error",
          text: error.message || "Ocurrió un error al procesar la solicitud",
          icon: "error",
        });
      } finally {
        this.isSubmitting = false;
      }
    },

    resetForm() {
      this.formData = {
        tipo_origen: "",
        origen: "",
        tipo_equipo: "",
        estado: "cargado",
        operacion: "",
        productos: [], // Resetear a array vacío
        situados: 1,
        pendiente_proximo_dia: 0,
        observaciones: "",
      };
    },

    async confirmCancel() {
      const result = await Swal.fire({
        title: "¿Cancelar operación?",
        text: "Los datos no guardados se perderán",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, cancelar",
        cancelButtonText: "No, continuar",
        reverseButtons: true,
      });

      if (result.isConfirmed) {
        this.resetForm();
        this.$router.push({ name: "InfoOperativo" });
      }
    },
  },
};
</script>


<style scoped>

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
  font-family: 'Segoe UI', Roboto, -apple-system, sans-serif;
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

.ufc-select, .ufc-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.85rem;
  transition: all 0.2s;
  background-color: white;
}

.ufc-select:focus, .ufc-input:focus {
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
  font-size: 0.85rem;
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
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.ufc-button.secondary {
  background: white;
  color: #555;
  border: 1px solid #ddd;
}

.ufc-button.secondary:hover {
  background: #f8f9fa;
  border-color: #ccc;
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
</style>