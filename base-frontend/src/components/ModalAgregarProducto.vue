<template>
  <div class="ufc-modal-overlay" >
    <div class="ufc-modal-container">
      <div class="ufc-modal-header">
        <h3><i class="bi bi-file-earmark-plus"></i> Nuevo registro de producto en vagón</h3>
        <button class="ufc-modal-close">
          <i class="bi bi-x" @click.self="cerrarModal"></i>
        </button>
      </div>
      <div class="ufc-modal-body">
        <div class="ufc-form-grid">
          <form @submit.prevent="submitForm">
            <div class="row">
              <!-- Columna Izquierda -->
              <div class="col-md-6">
                <div class="ufc-input-group"> 
                  <label for="embalaje" class="form-label small fw-semibold text-secondary">
                    Productos<span class="required-asterisk">*</span>
                  </label>
                  <div class="ufc-input-with-action">
                    <select
                      class="form-select form-select-sm border-secondary"
                      style="padding: 8px 12px"
                      v-model="formData.producto"
                      id="producto"
                      name="Producto"
                      required
                      oninvalid="this.setCustomValidity('Por favor, seleccione un Producto')"
                      oninput="this.setCustomValidity('')">
                      <option value="" disabled>Seleccione un Producto</option>
                      <option
                        v-for="producto in productos"
                        :key="producto.id"
                        :value="producto.id">
                        {{producto.nombre_producto}}-{{producto.codigo_producto}}
                      </option>
                    </select>
                    <button class="create-button ms-2" @click.stop.prevent="agregarProducto">
                      <i class="bi bi-plus-circle large-icon"></i>
                    </button>
                  </div>
                </div>
                
                <!-- Campo: Embalaje -->
                <div class="ufc-input-group">
                  <label for="embalaje" class="form-label small fw-semibold text-secondary">Embalaje</label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="formData.tipo_embalaje"
                    id="embalaje"
                    name="embalaje"
                    required>
                    <option
                      v-for="embalaje in embalajes"
                      :key="embalaje.id"
                      :value="embalaje.id">
                      {{ embalaje.id }}-{{ embalaje.nombre_tipo_embalaje }}
                    </option>
                  </select>
                </div>
                
                <!-- Campo: estado -->
                <div class="ufc-input-group">
                  <label for="estado" class="form-label small fw-semibold text-secondary">Estado</label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="formData.estado"
                    id="estado"
                    name="estado"
                    required>
                    <option value="lleno">Lleno</option>
                    <option value="vacio">Vacio</option>
                  </select>
                </div>
              </div>

              <!-- Columna Derecha -->
              <div class="col-md-6">
                <!-- Campo: unidad_medida -->
                <div class="ufc-input-group">
                  <label for="unidad_medida" class="form-label small fw-semibold text-secondary">Unidad de medida</label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="formData.unidad_medida"
                    id="unidad_medida"
                    name="unidad_medida"
                    required>
                    <option
                      v-for="unidad in unidades"
                      :key="unidad.id"
                      :value="unidad.id">
                      {{ unidad.unidad_medida }}
                    </option>
                  </select>
                </div>
                
                <!-- Campo: cantidad_vagones -->
                <div class="ufc-input-group">
                  <label for="cantidad" class="form-label small fw-semibold text-secondary">Cantidad</label>
                  <div class="ufc-por-situar-container">
                    <input
                      type="number"
                      class="ufc-por-situar-input"
                      v-model="formData.cantidad"
                      id="cantidad"
                      name="cantidad"
                      min="0"/>
                  </div>
                </div>

                <!-- Campo: contiene -->
                <div class="ufc-input-group">
                  <label for="contiene" class="form-label small fw-semibold text-secondary">Contiene</label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="formData.contiene"
                    id="contiene"
                    name="contiene"
                    required>
                    <option value="alimentos">Alimentos</option>
                    <option value="prod_varios">Productos varios</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Botones del modal -->
            <div class="ufc-form-actions">
              <button
                type="button"
                class="ufc-button secondary"
                @click="cerrarModal">
                <i class="bi bi-x-circle"></i> Cancelar
              </button>
              <button
                type="submit"
                class="ufc-button primary">
                <i class="bi bi-check-circle"></i> Agregar
              </button>
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

export default {
  name: "ModalAgregarProducto",
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      formData: {
        producto: "",
        tipo_embalaje: "",
        unidad_medida: "",
        cantidad: 0,
        estado: "vacio",
        contiene: "",
      },
      productos: [],
      embalajes: [],
      unidades: [],
    };
  },
  mounted() {
    this.getProductos();
    this.getEmbalaje();
    this.getUnidades();
  },
  methods: {
    async submitForm() {
      try {
        await axios.post("/ufc/producto-vagon/", this.formData);
        this.showSuccessToast("El formulario ha sido añadido");
        this.$emit("cerrar-modal");
      } catch (error) {
        this.showErrorToast("Error al añadir el formulario");
        console.log(error);
      }
    },
    cerrarModal() {
      this.$emit("cerrar-modal");
    },

    agregarProducto() {
      this.$router.push({ name: "CrearProducto" });
    },

    async getProductos() {
      try {
        const response = await axios.get("/api/productos/");
        this.productos = response.data.results;
      } catch (error) {
        this.showErrorToast("Error al obtener los productos");
        console.log(error);
      }
    },

    async getEmbalaje() {
      try {
        const response = await axios.get("/api/embalajes/");
        this.embalajes = response.data.results;
      } catch (error) {
        this.showErrorToast("Error al obtener los embalajes");
        console.log(error);
      }
    },

    async getUnidades() {
      try {
        const response = await axios.get("/api/unidades_medida/");
        this.unidades = response.data.results;
      } catch (error) {
        this.showErrorToast("Error al obtener las unidades de medida");
        console.log(error);
      }
    },
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
};
</script>

<style scoped>
/* Estilos para la sección de vagones asociados */
.ufc-vagones-container {
  margin-top: 30px;
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.ufc-vagones-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.ufc-vagones-header h3 {
  color: #002a68;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
}

.ufc-button.small {
  padding: 6px 12px;
  font-size: 0.8rem;
}

.ufc-vagones-table-container {
  overflow-x: auto;
}

.ufc-vagones-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.ufc-vagones-table th {
  background-color: #002a68;
  color: white;
  padding: 10px 12px;
  text-align: left;
  font-weight: 500;
  font-size: 0.85rem;
}

.ufc-vagones-table td {
  padding: 12px;
  border-bottom: 1px solid #eee;
  font-size: 0.85rem;
}

.ufc-vagones-table tr:hover {
  background-color: #f8f9fa;
}

.ufc-actions-cell {
  display: flex;
  gap: 8px;
}

.ufc-icon-button {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.ufc-icon-button i {
  font-size: 0.9rem;
}

.ufc-icon-button.warning {
  background-color: #ffc107;
  color: #212529;
}

.ufc-icon-button.warning:hover {
  background-color: #e0a800;
}

.ufc-icon-button.danger {
  background-color: #dc3545;
  color: white;
}

.ufc-icon-button.danger:hover {
  background-color: #c82333;
}

/* Estilo para estado vacío */
.ufc-vagones-empty {
  margin-top: 20px;
  text-align: center;
  padding: 30px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.ufc-empty-state {
  color: #6c757d;
}

.ufc-empty-state i {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #adb5bd;
}

.ufc-empty-state p {
  margin: 0;
  font-size: 0.9rem;
}

/* Estilos para el modal de vagón */
.ufc-modal-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.ufc-modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

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
.ufc-vagones-agregados {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.ufc-subtitle {
  color: #002a68;
  font-size: 1.1rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.ufc-table-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

.ufc-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

.ufc-table th {
  background-color: #f8f9fa;
  padding: 10px;
  text-align: left;
  border-bottom: 2px solid #ddd;
  color: #555;
}

.ufc-table td {
  padding: 10px;
  border-bottom: 1px solid #eee;
  vertical-align: middle;
}

.ufc-table tr:hover {
  background-color: #f5f5f5;
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

.ufc-button.primary:hover {
  background: #003d8f;
}

.ufc-button.secondary {
  background: rgb(241, 81, 63);
  color: white;
}

.ufc-button.secondary:hover {
  background: rgb(228, 56, 37);
}

.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
}

.btn-outline-danger:hover {
  color: #fff;
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
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.ufc-modal-container {
  background: white;
  border-radius: 10px;
  width: 90%;
  max-width: 600px;
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

