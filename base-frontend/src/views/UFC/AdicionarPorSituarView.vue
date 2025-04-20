<template>
  <div style="background-color: #002a68; color: white; text-align: right">
    <h6>Partes UFC</h6>
  </div>
  <Navbar-Component />
  <Producto-Vagones />
  <div class="container mt-2 px-6" style="padding-left: 10%">
    <div class="row mb-4">
      <h2 class="mb-4">Nuevo registro por situar</h2>

      <form @submit.prevent="submitForm">
        <div class="row">
          <!-- Columna 1 -->
          <div class="col-md-6">
            <!-- Campo: tipo_origen -->
            <div class="mb-3">
              <label for="tipo_origen" class="form-label"
                >Tipo de Origen <span style="color: red">*</span></label
              >
              <select
                class="form-select"
                v-model="formData.tipo_origen"
                id="tipo_origen"
                name="tipo_origen"
                required
                :disabled="loading"
              >
                <option
                  v-for="item in tipo_origen_options"
                  :key="item.id"
                  :value="item.id"
                >
                  {{ item.text }}
                </option>
              </select>
            </div>

            <!-- Campo: origen -->
            <div class="mb-3">
              <label for="origen" class="form-label"
                >Origen <span style="color: red">*</span></label
              >
              <select
                v-if="formData.tipo_origen !== 'puerto'"
                class="form-select"
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
                v-else
                class="form-select"
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
            </div>

            <!-- Campo: tipo_equipo -->
            <div class="mb-3">
              <label for="tipo_equipo" class="form-label"
                >Tipo de Equipo <span style="color: red">*</span></label
              >
              <select
                class="form-select"
                v-model="formData.tipo_equipo"
                id="tipo_equipo"
                name="tipo_equipo"
                @change="buscarEquipos"
                required
              >
                <option value="">Seleccione un tipo</option>
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
                <option value="cargado">Cargado</option>
                <option value="vacio">Vacio</option>
              </select>
            </div>

            <div class="mb-3">
              <label for="operacion" class="form-label"
                >Operación <span style="color: red">*</span></label
              >
              <select
                class="form-select"
                v-model="formData.operacion"
                id="operacion"
                name="operacion"
                required
              >
                <option value="">Seleccione una operación</option>
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
          <div class="col-md-6">
            <!-- Campo: producto -->
            <div class="mb-3">
              <label for="producto" class="form-label">
                Producto
                <button
                  class="create-button ms-2"
                  @click.prevent="abrirModalAgregarProducto"
                >
                  <i class="bi bi-plus-circle large-icon"></i>
                </button>
              </label>

              <template v-if="formData.estado === 'cargado'">
                <select
                  v-if="!loading"
                  class="form-select"
                  v-model="formData.producto"
                  id="producto"
                  name="producto"
                  required
                >
                  <option value="" disabled>Seleccione un producto</option>
                  <option
                    v-for="producto in productos"
                    :key="producto.id"
                    :value="producto.id"
                  >
                    {{ producto.id }}-{{ producto.producto_name }} -
                    {{ producto.producto_codigo }}
                  </option>
                </select>
                <div v-else class="text-muted">
                  <i class="bi bi-arrow-repeat"></i> Cargando productos...
                </div>
              </template>

              <div v-else class="text-muted">
                (Seleccione "Cargado" para ver los productos)
              </div>
            </div>
            <ModalAgregarProducto
              v-if="mostrarModal"
              :visible="mostrarModal"
              @cerrar-modal="cerrarModal"
            />

            <!-- Campo: cantidad_vagones -->
            <div class="mb-3">
              <label for="cantidad_vagones" class="form-label">
                Por Situar <span style="color: red">*</span>
              </label>
              <input
                type="number"
                class="form-control"
                v-model.number="formData.por_situar"
                id="cantidad_vagones"
                name="cantidad_vagones"
                min="1"
                required
              />
            </div>

            <!-- Campo: observaciones -->
            <div class="mb-3">
              <label for="observaciones" class="form-label"
                >Observaciones
              </label>
              <textarea
                class="form-control"
                v-model="formData.observaciones"
                id="observaciones"
                name="observaciones"
                rows="3"
              ></textarea>
            </div>
          </div>
        </div>
      </form>
      <div class="text-center">
        <button type="button" class="btn btn-primary" @click="submitForm">
          Agregar
        </button>
        <button type="menu" @click="confirmCancel" class="btn btn-secondary">
          Cancelar
        </button>
      </div>
    </div>

    <!-- Segunda fila: Lista de vagones -->
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import NavbarComponent from "@/components/NavbarComponent.vue";
import ModalAgregarProducto from "@/components/ModalAgregarProducto.vue";

export default {
  name: "AdicionarPorSituar",
  components: {
    NavbarComponent,
    ModalAgregarProducto,
  },
  data() {
    return {
      formData: {
        tipo_origen: "", // Asegúrarse que este valor coincide con tus opciones
        origen: "",
        tipo_equipo: "",
        estado: "cargado",
        operacion: "",
        producto: "",
        por_situar: 1, // Nombre consistente en todo el código
        observaciones: "",
      },
      entidades: [],
      puertos: [],
      productos: [],
      mostrarModal: false,
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
    abrirModalAgregarProducto() {
      this.mostrarModal = true;
    },
    cerrarModal() {
      this.mostrarModal = false;
      this.getProductos();
    },

    async getPuertos() {
      try {
        let allPuertos = [];
        let nextPage = "/api/puertos/"; // URL inicial

        while (nextPage) {
          const response = await axios.get(nextPage);
          allPuertos = [...allPuertos, ...response.data.results];

          // Actualizamos nextPage con la URL de la siguiente página (o null si no hay más)
          nextPage = response.data.next;
        }

        this.puertos = allPuertos;
      } catch (error) {
        console.error("Error al obtener los puertos:", error);
        Swal.fire("Error", "Hubo un error al obtener los puertos.", "error");
      }
    },

    abrirModalAgregarProducto() {
      this.mostrarModal = true;
    },

    cerrarModal() {
      this.mostrarModal = false;
      this.getProductos();
    },

    async submitForm() {
      try {
        // Validación mejorada
        const errors = [];

        if (!this.formData.origen) {
          errors.push("El campo Origen es requerido");
        }

        if (!this.formData.tipo_equipo) {
          errors.push("El campo Tipo de Equipo es requerido");
        }

        if (!this.formData.operacion) {
          errors.push("El campo Operación es requerido");
        }

        if (this.formData.estado === "cargado" && !this.formData.producto) {
          errors.push(
            "El campo Producto es requerido cuando el estado es Cargado"
          );
        }

        if (!this.formData.por_situar || this.formData.por_situar < 1) {
          errors.push("La cantidad de vagones debe ser al menos 1");
        }

        // Verificar tipo_origen
        if (!["ac_ccd", "puerto"].includes(this.formData.tipo_origen)) {
          errors.push("Tipo de origen no válido");
        }

        if (errors.length > 0) {
          throw new Error(errors.join("\n"));
        }

        // Preparar datos para enviar (nombres de campos consistentes)
        const payload = {
          tipo_origen: this.formData.tipo_origen,
          origen: this.formData.origen,
          tipo_equipo: this.formData.tipo_equipo,
          estado: this.formData.estado,
          operacion: this.formData.operacion,
          producto: this.formData.producto || null,
          por_situar: this.formData.por_situar.toString(), // Convertir a string como espera el backend
          observaciones: this.formData.observaciones || "",
        };

        console.log("Enviando payload:", payload); // Para debug

        const response = await axios.post("/ufc/por-situar/", payload);
        console.log("Respuesta:", response.data); // Para debug

        await Swal.fire(
          "Agregado!",
          "El formulario ha sido añadido exitosamente.",
          "success"
        );

        this.$router.push({ name: "InfoOperativo" });
      } catch (error) {
        console.error("Error al agregar el formulario:", error);
        let errorMessage = "Hubo un error al agregar el formulario.";
        if (error.response?.data) {
          errorMessage += "\nDetalles: " + JSON.stringify(error.response.data);
        }
        Swal.fire("Error", errorMessage, "error");
      }
    },

    resetForm() {
      this.formData = {
        tipo_origen: "",
        origen: "",
        tipo_equipo: "",
        estado: "cargado",
        operacion: "",
        producto: "",
        por_situar: 1, // Nombre consistente con el formulario
        observaciones: "",
      };
    },

    confirmCancel() {
      this.resetForm();
      Swal.fire({
        title: "¿Cancelar operación?",
        text: "Los datos no guardados se perderán",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, cancelar",
        cancelButtonText: "No, continuar",
      }).then((result) => {
        if (result.isConfirmed) {
          this.$router.push({ name: "InfoOperativo" });
        }
      });
    },
  },
};
</script>

<style scoped>
.create-button {
  background: none;
  border: none;
  color: green;
  padding: 0;
  cursor: pointer;
}

.create-button:hover {
  color: darkgreen;
}

.large-icon {
  font-size: 1.2rem;
}

.form-container {
  max-width: 300px;
  margin: 50px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  font-family: "Franklin Gothic Medium", "Arial Narrow", Arial, sans-serif;
  text-align: left;
  margin-bottom: 20px;
  font-size: 20px;
}

.form-group {
  text-align: left;
  display: flex;
  width: 260px;
  flex-direction: column;
  gap: 5px;
  font-size: 14px;
}

label {
  font-weight: bold;
}

input,
select,
textarea {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
}

.btn {
  margin: 0 5px;
  padding: 8px 16px;
}

.text-warning {
  color: #ffc107;
}

.text-success {
  color: #28a745;
}

.text-danger {
  color: #dc3545;
}
</style>
