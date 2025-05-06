<template>
  <Navbar-Component />

  <div class="container mt-5" style="padding-left: 20%">
    <h2 class="mb-4">Nuevo registro de producto en vagón</h2>
    <form @submit.prevent="submitForm">
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

      <!-- Botón de envío -->
      <div class="text-center">
        <button type="submit" class="btn btn-primary">Guardar</button>
        <button @click="volverAdicionarEnTren" class="btn btn-secondary">
          Volver
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.create-button {
  text-decoration: none;
  color: green;
  margin-left: 940px;
}

.form-container {
  max-width: 300px;
  margin: 50px;
  padding: 20px;
  background-color: f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  font-family: "Franklin Gothic Medium", "Arial Narrow", Arial, sans-serif;
  text-align: left;
  margin-bottom: 20px;
  font-size: 20px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
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
select {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.form-buttons {
  display: flex;
  justify-content: end;
  font-size: 15px;
}

button {
  margin-left: 10px;
  padding: 5px 15px;
  border: none;
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
</style>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import NavbarComponent from "@/components/NavbarComponent.vue";
export default {
  name: "AdicionarProducto",
  components: {
    NavbarComponent,
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
      productos: [], // Almacena las terminales obtenidas
      embalajes: [],
      unidades: [],
    };
  },
  
  mounted() {
    // Llama al método para obtener los puertos
    this.getProductos();
    this.getEmbalaje();
    this.getUnidades();
  },
  computed{
    formattedFechaRegistro() {
      if (this.formData.fecha) {
        return new Date(this.formData.fecha).toLocaleString();
      }
      return new Date().toLocaleString();
    }
  },

  methods: {
    confirmCancel() {
      Swal.fire({
        title: "¿Está seguro de que quiere cancelar la operación?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        cancelmButtonText: "Cancelar",
        confirmButtonText: "Aceptar",
      }).then((result) => {
        if (result.isConfirmed) {
          window.history.back();
        }
      });
    },
    agregarProducto() {
      // Redirige a la vista "CrearProducto"
      this.$router.push({ name: "CrearProducto" });
    },
    async verificarInformeOperativo() {
      try {
            this.formData.fecha = new Date().toISOString();
            const today = new Date();
            const fechaFormateada = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;

            const response = await axios.get('/ufc/verificar-informe-existente/', {
              params: { fecha_operacion: fechaFormateada }
            });

            if (response.data.existe) {
              this.informeOperativoId = response.data.id;
              return true;
            }
            return false;
          } catch (error) {
            console.error("Error al verificar informe:", error);
            return false;
          }
        },
    async submitForm() {
      try {
        // 1. Verifificar que el informe operativo existe ya para la fecha creada
          const existeInforme = await this.verificarInformeOperativo();
          if (!existeInforme) {
            Swal.fire(
              "Error",
              "No existe un informe operativo creado para la fecha actual. Debe crear uno primero.",
              "error"
            );
            this.$router.push({ name: "InfoOperativo" });
            return;
            
          }
        await axios.post("/ufc/producto-vagon/", this.formData);
        Swal.fire(
          "Agregado!",
          "El formulario sido añadido exitosamente.",
          "success"
        );
      } catch (error) {
        console.error("Error al agregar el formulario:", error);
        Swal.fire("Error", "Hubo un error al agregar el formulario.", "error");
      }
      this.resetForm;
    },
    resetForm() {
      // Restablece los valores del formulario
      this.formData = {
        producto: "",
        tipo_embalaje: "",
        unidad_medida: "",
        cantidad: 0,
        estado: "vacio",
        contiene: "alimentos",
      };
    },
    async getProductos() {
      try {
        const response = await axios.get("/api/productos/");
        this.productos = response.data;
      } catch (error) {
        console.error("Error al obtener los productos:", error);
        Swal.fire("Error", "Hubo un error al obtener los productos.", "error");
      }
    },
    async getEmbalaje() {
      try {
        const response = await axios.get("/api/embalajes/");
        this.embalajes = response.data;
      } catch (error) {
        console.error("Error al obtener los embalajes:", error);
        Swal.fire("Error", "Hubo un error al obtener los embalajes.", "error");
      }
    },
    async getUnidades() {
      try {
        const response = await axios.get("/api/unidades_medida/");
        this.unidades = response.data;
      } catch (error) {
        console.error("Error al obtener las unidades de medida:", error);
        Swal.fire(
          "Error",
          "Hubo un error al obtener las unidades de medida.",
          "error"
        );
      }
    },
    volverAdicionarEnTren() {
      // Redirige a la vista "AdicionarProductoVagon"
      this.$router.push({ name: "AdicionarVagon" });
    },

    validateForm() {
      const nombre_atraque_regex = /^[A-Z][A-Za-z ]{2,99}$/;
      let errorMessage = "";

      if (!nombre_atraque_regex.test(this.nombre_atraque)) {
        errorMessage +=
          'El campo "Nombre" debe comenzar con mayúscula, seguir con letras y espacios, y tener entre 3 y 100 caracteres.\n';
      }

      if (errorMessage) {
        Swal.fire({
          icon: "error",
          title: "Error de validación",
          text: errorMessage,
        });
        return false; // Detener el envío del formulario
      }

      return true; // El formulario es válido
    },
  },
};
</script>
