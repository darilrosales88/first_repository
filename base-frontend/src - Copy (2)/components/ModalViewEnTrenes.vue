<template>
  <div class="modal-overlay" v-if="visible" @click.self="cerrarModal">
    <div class="modal-content">
      <h2 class="mb-4">Registro de vagón</h2>

      <div class="row">
        <!-- Columna 1 -->
        <div class="col-md-6">
          <!-- Campo: Producto -->
          <div class="mb-3">
            <label for="producto" class="form-label"
              >Producto<span style="color: red">*</span>
            </label>
            <span>
              <button class="create-button ms-2" @click="agregarProducto">
                <i class="bi bi-plus-circle large-icon"></i>
              </button>
            </span>
            <select
              class="form-select"
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
          </div>

          <!-- Campo: Embalaje -->
          <div class="mb-3">
            <label for="embalaje" class="form-label"
              >Embalaje<span style="color: red">*</span></label
            >
            <select
              class="form-select"
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
          <div class="mb-3">
            <label for="estado" class="form-label"
              >Estado <span style="color: red">*</span></label
            >
            <select
              class="form-select"
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
          <div class="mb-3">
            <label for="unidad_medida" class="form-label"
              >Unidad de medida<span style="color: red">*</span></label
            >
            <select
              class="form-select"
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
          <div class="mb-3">
            <label for="cantidad" class="form-label">Cantidad</label>
            <input
              type="number"
              class="form-control"
              v-model="formData.cantidad"
              id="cantidad"
              name="cantidad"
            />
          </div>

          <!-- Campo: contiene -->
          <div class="mb-3">
            <label for="contiene" class="form-label"
              >Contiene <span style="color: red">*</span></label
            >
            <select
              class="form-select"
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
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "ModalEnTrenes",
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
    vagon: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      vagon: [],
    };
  },
  mounted() {},
  methods: {
    async getVagon() {
      const vagon_id = props.vagon;
      const response = await axios.get("/ufc/en-trenes/", { vagon_id });
      this.vagon = response.data;
    },

    cerrarModal() {
      this.$emit("cerrar-modal");
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
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 80%;
  max-width: 600px;
}
</style>
