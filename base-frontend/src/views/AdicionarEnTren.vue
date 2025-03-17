<template>
  <Navbar-Component />
  <div class="container mt-5" style="padding-left: 20%">
    <h2 class="mb-4">Nuevo registro de vagón</h2>
    <form @submit.prevent="submitForm">
      <div class="row">
        <!-- Columna 1 -->
        <div class="col-md-6">
          <!-- Campo: locomotora -->
          <div class="mb-3">
            <label for="locomotora" class="form-label"
              >Locomotora<span style="color: red">*</span></label
            >
            <select
              class="form-select"
              v-model="formData.locomotora"
              id="locomotora"
              name="Locomotora"
              required
            >
              <option
                v-for="locomotora in locomotoras"
                :key="locomotora.id"
                :value="locomotora.id"
              >
                {{ locomotora.id }}-{{ locomotora.numero_identificacion }} -
                {{ locomotora.tipo_equipo_name }}
              </option>
            </select>
          </div>

          <!-- Campo: tipo_origen -->
          <div class="mb-3">
            <label for="tipo_origen" class="form-label">Tipo de Origen</label>
            <select
              class="form-select"
              v-model="formData.tipo_origen"
              id="tipo_origen"
              name="tipo_origen"
            >
              <option value="ac_ccd">Acceso Comercial</option>
              <option value="puerto">Puerto</option>
            </select>
          </div>

          <!-- Campo: origen -->
          <div class="mb-3">
            <label for="origen" class="form-label">Origen</label>
            <select
              v-if="formData.tipo_origen !== 'puerto'"
              class="form-select"
              v-model="formData.origen"
              id="origen"
              name="origen"
            >
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
            >
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
              >Tipo de Equipo<span style="color: red">*</span></label
            >
            <select
              class="form-select"
              v-model="formData.tipo_equipo"
              id="equipo"
              name="equipo"
              required
            >
              <option
                v-for="equipo in equipos"
                :key="equipo.id"
                :value="equipo.tipo_equipo"
              >
                {{ equipo.id }}-{{ equipo.tipo_equipo_name }}-{{
                  equipo.tipo_carga
                }}
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
        </div>

        <!-- Columna 2 -->
        <div class="col-md-6">
          <!-- Campo: tipo_destino -->
          <div class="mb-3">
            <label for="tipo_destino" class="form-label"
              >Tipo de Destino <span style="color: red">*</span></label
            >
            <select
              class="form-select"
              v-model="formData.tipo_destino"
              id="tipo_destino"
              name="tipo_destino"
              required
            >
              <option value="ac_ccd">Acceso Comercial</option>
              <option value="puerto">Puerto</option>
            </select>
          </div>

          <!-- Campo: destino -->
          <div class="mb-3">
            <label for="destino" class="form-label">Destino</label>
            <select
              v-if="formData.tipo_destino !== 'puerto'"
              class="form-select"
              v-model="formData.destino"
              id="destino"
              name="destino"
            >
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
              v-model="formData.destino"
              id="destino"
              name="destino"
            >
              <option
                v-for="puerto in puertos"
                :key="puerto.id"
                :value="puerto.nombre_puerto"
              >
                {{ puerto.id }}- {{ puerto.nombre_puerto }}
              </option>
            </select>
          </div>

          <!-- Campo: producto -->
          <div class="mb-3">
            <label for="producto" class="form-label">Producto</label>
            <select
              class="form-select"
              v-model="formData.producto"
              id="producto"
              name="producto"
            >
              <option v-for="producto in productos" :value="producto.id">
                {{ producto.id }}-{{ producto.producto_name }}
              </option>
            </select>
          </div>

          <!-- Campo: cantidad_vagones -->
          <div class="mb-3">
            <label for="cantidad_vagones" class="form-label"
              >Cantidad de Vagones</label
            >
            <input
              type="number"
              class="form-control"
              v-model="formData.cantidad_vagones"
              id="cantidad_vagones"
              name="cantidad_vagones"
            />
          </div>

          <!-- Campo: observaciones -->
          <div class="mb-3">
            <label for="observaciones" class="form-label"
              >Observaciones <span style="color: red">*</span></label
            >
            <textarea
              class="form-control"
              v-model="formData.observaciones"
              id="observaciones"
              name="observaciones"
              rows="3"
              required
            ></textarea>
          </div>
        </div>
      </div>

      <!-- Botón de envío -->
      <div class="text-center">
        <button type="submit" class="btn btn-primary">Guardar</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
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
  name: "AdicionarAtraqueView",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      formData: {
        locomotora: "",
        tipo_origen: "acc_d",
        origen: "",
        tipo_equipo: "",
        estado: "cargado",
        tipo_destino: "ac_ccd",
        destino: "",
        producto: "",
        cantidad_vagones: 0,
        observaciones: "",
        puerto: "",
        entidad: "",
      },
      productos: [], // Almacena las terminales obtenidas
      equipos: [], // Almacena los puertos obtenidos
      locomotoras: [],
      puertos: [],
      entidades: [],
    };
  },

  mounted() {
    // Llama al método para obtener los puertos
    this.getProductos();
    this.getEquipos();
    this.getLocomotoras();
    this.getEntidades();
    this.getPuertos();
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
    async submitForm() {
      try {
        await axios.post("/ufc/en-trenes/", this.formData);
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
        locomotora: "puerto",
        tipo_origen: "acc_d",
        origen: "",
        tipo_equipo: "",
        estado: "cargado",
        tipo_destino: "ac_ccd",
        destino: "",
        producto: "",
        cantidad_vagones: 0,
        observaciones: "",
        puerto: "",
        entidad: "",
      };
    },
    async getLocomotoras() {
      try {
        const response = await axios.get(
          "/api/equipos_ferroviarios/?id_tipo_equipo_territorio=locomo"
        );
        this.locomotoras = response.data;
      } catch (error) {
        console.error("Error al obtener las Locomotoras:", error);
        Swal.fire(
          "Error",
          "Hubo un error al obtener las Locomotoras.",
          "error"
        );
      }
    },

    async getEntidades() {
      try {
        const response = await axios.get("/api/entidades/");
        this.entidades = response.data;
      } catch (error) {
        console.error("Error al obtener las entidades:", error);
        Swal.fire("Error", "Hubo un error al obtener las entidades.", "error");
      }
    },

    async getPuertos() {
      try {
        const response = await axios.get("/api/puertos/");
        this.puertos = response.data;
      } catch (error) {
        console.error("Error al obtener los puertos:", error);
        Swal.fire("Error", "Hubo un error al obtener los puertos.", "error");
      }
    },

    async getEquipos() {
      try {
        const response = await axios.get("/api/tipos_equipos/");
        this.equipos = response.data;
      } catch (error) {
        console.error("Error al obtener los equipos:", error);
        Swal.fire("Error", "Hubo un error al obtener los equipos.", "error");
      }
    },

    async getProductos() {
      try {
        const response = await axios.get(
          "/ufc/productos-vagones-cargados-descargados/"
        );
        this.productos = response.data;
      } catch (error) {
        console.error("Error al obtener los productos:", error);
        Swal.fire("Error", "Hubo un error al obtener los productos.", "error");
      }
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
