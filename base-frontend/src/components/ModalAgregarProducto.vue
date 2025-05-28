<template>
  <div class="modal-overlay" v-if="visible" @click.self="cerrarModal">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Nuevo registro de producto en vagón</h2>
      </div>
      <form @submit.prevent="submitForm">
        <div class="row">
          <!-- Columna 1 -->
          <div class="col-md-6">
            <!-- Campo: Producto -->
            <div class="mb-4">
              <label for="producto" class="form-label">
                Producto<span class="required-asterisk">*</span>
              </label>
              <div class="input-group">
                <select
                  class="form-select styled-select"
                  v-model="formData.producto"
                  id="producto"
                  name="Producto"
                  required
                >
                  <option
                    v-for="producto in productos"
                    :key="producto.id"
                    :value="producto.id"
                  >
                    {{ producto.id }}-{{ producto.nombre_producto }} -
                    {{ producto.codigo_producto }}
                  </option>
                </select>
                <button class="btn btn-icon" @click="agregarProducto" type="button">
                  <i class="bi bi-plus-circle"></i>
                </button>
              </div>
            </div>

            <!-- Campo: Embalaje -->
            <div class="mb-4">
              <label for="embalaje" class="form-label">
                Embalaje<span class="required-asterisk">*</span>
              </label>
              <select
                class="form-select styled-select"
                v-model="formData.tipo_embalaje"
                id="embalaje"
                name="embalaje"
                required
              >
                <option
                  v-for="embalaje in embalajes"
                  :key="embalaje.id"
                  :value="embalaje.id"
                >
                  {{ embalaje.id }}-{{ embalaje.nombre_tipo_embalaje }}
                </option>
              </select>
            </div>

            <!-- Campo: estado -->
            <div class="mb-4">
              <label for="estado" class="form-label">
                Estado <span class="required-asterisk">*</span>
              </label>
              <select
                class="form-select styled-select"
                v-model="formData.estado"
                id="estado"
                name="estado"
                required
              >
                <option value="lleno">Lleno</option>
                <option value="vacio">Vacio</option>
              </select>
            </div>
          </div>

          <!-- Columna 2 -->
          <div class="col-md-6">
            <!-- Campo: unidad_medida -->
            <div class="mb-4">
              <label for="unidad_medida" class="form-label">
                Unidad de medida<span class="required-asterisk">*</span>
              </label>
              <select
                class="form-select styled-select"
                v-model="formData.unidad_medida"
                id="unidad_medida"
                name="unidad_medida"
                required
              >
                <option
                  v-for="unidad in unidades"
                  :key="unidad.id"
                  :value="unidad.id"
                >
                  {{ unidad.id }}-{{ unidad.unidad_medida }}
                </option>
              </select>
            </div>
            <!-- Campo: cantidad_vagones -->
            <div class="mb-4">
              <label for="cantidad" class="form-label">Cantidad</label>
              <input
                type="number"
                class="form-control styled-input"
                v-model="formData.cantidad"
                id="cantidad"
                name="cantidad"
              />
            </div>

            <!-- Campo: contiene -->
            <div class="mb-4">
              <label for="contiene" class="form-label">
                Contiene <span class="required-asterisk">*</span>
              </label>
              <select
                class="form-select styled-select"
                v-model="formData.contiene"
                id="contiene"
                name="contiene"
                required
              >
                <option value="alimentos">Alimentos</option>
                <option value="prod_varios">Productos varios</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Botón de envío -->
        <div class="modal-footer">
          <button type="button" @click="cerrarModal" class="btn btn-outline-secondary">
            Volver
          </button>
          <button type="submit" class="btn btn-primary">
            Guardar
          </button>
        </div>
      </form>
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
        Swal.fire(
          "Agregado!",
          "El formulario ha sido añadido exitosamente.",
          "success"
        );
        this.$emit("cerrar-modal");
      } catch (error) {
        console.error("Error al agregar el formulario:", error);
        Swal.fire("Error", "Hubo un error al agregar el formulario.", "error");
      }
    },
    cerrarModal() {
      this.$emit("cerrar-modal");
    },
    agregarProducto() {
      // Redirige a la vista "CrearProducto"
      this.$router.push({ name: "CrearProducto" });
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
    async getEmbalaje() {
      try {
        const response = await axios.get("/api/embalajes/");
        this.embalajes = response.data.results;
      } catch (error) {
        console.error("Error al obtener los embalajes:", error);
        Swal.fire("Error", "Hubo un error al obtener los embalajes.", "error");
      }
    },
    async getUnidades() {
      try {
        const response = await axios.get("/api/unidades_medida/");
        this.unidades = response.data.results;
      } catch (error) {
        console.error("Error al obtener las unidades de medida:", error);
        Swal.fire(
          "Error",
          "Hubo un error al obtener las unidades de medida.",
          "error"
        );
      }
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
  backdrop-filter: blur(3px);
  transition: all 0.3s ease;
}

.modal-content {
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 700px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  border: none;
  animation: fadeIn 0.3s ease-out;
}

.modal-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h2 {
  color: #2c3e50;
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #495057;
  font-size: 0.9rem;
}

.required-asterisk {
  color: #e74c3c;
  margin-left: 0.2rem;
}

.styled-select,
.styled-input {
  border: 1px solid #ced4da;
  border-radius: 6px;
  padding: 0.6rem 0.75rem;
  font-size: 0.9rem;
  transition: all 0.2s;
  box-shadow: none;
}

.styled-select:focus,
.styled-input:focus {
  border-color: #4a90e2;
  box-shadow: 0 0 0 0.2rem rgba(74, 144, 226, 0.25);
  outline: none;
}

.input-group {
  display: flex;
  align-items: center;
}

.btn-icon {
  background-color: #f8f9fa;
  border: 1px solid #ced4da;
  border-left: none;
  border-radius: 0 6px 6px 0;
  padding: 0.6rem;
  color: #4a90e2;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover {
  background-color: #e9ecef;
  color: #2c7be5;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e9ecef;
}

.btn {
  padding: 0.6rem 1.25rem;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.9rem;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.btn-primary {
  background-color: #4a90e2;
  border-color: #4a90e2;
}

.btn-primary:hover {
  background-color: #3a7bc8;
  border-color: #3a7bc8;
  transform: translateY(-1px);
}

.btn-outline-secondary {
  color: #6c757d;
  border-color: #6c757d;
  background-color: transparent;
}

.btn-outline-secondary:hover {
  background-color: #f8f9fa;
  color: #5a6268;
  border-color: #5a6268;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    padding: 1.5rem;
  }
}
</style>