<template>
  <div>
    <div style="background-color: #002a68; color: white; text-align: right">
      <h6>Bienvenido:</h6>
    </div>
    <br />
    <Navbar-Component />

    <div class="form-container" style="margin-left: 18em; width: 75%">
      <h3 style="color: #002a68">
        Editar atraque <strong>{{ atraque.nombre_atraque }}</strong>
      </h3>
      <form @submit.prevent="submitForm">
        <div class="form-row">
          <!-- Campo Nombre del Atraque -->
          <div class="mb-3">
            <label for="nombre_atraque" class="form-label"
              >Nombre:<span style="color: red">*</span></label
            >
            <input
              type="text"
              class="form-control"
              id="nombre_atraque"
              v-model="atraque.nombre_atraque"
              required
            />
          </div>

          <!-- Campo Puerto -->
          <div class="mb-3">
            <label for="puerto" class="form-label"
              >Puerto:<span style="color: red">*</span></label
            >
            <select
              class="form-control"
              id="puerto"
              v-model="atraque.puerto"
              required
            >
              <option
                v-for="puerto in puertos"
                :value="puerto.id"
                :key="puerto.id"
              >
                {{ puerto.nombre_puerto }}
              </option>
            </select>
          </div>

          <!-- Campo Terminal -->
          <div class="mb-3">
            <label for="terminal" class="form-label"
              >Terminal:<span style="color: red">*</span></label
            >
            <select
              class="form-control"
              id="terminal"
              v-model="atraque.terminal"
              required
            >
              <option
                v-for="terminal in terminales"
                :value="terminal.id"
                :key="terminal.id"
              >
                {{ terminal.nombre_terminal }}
              </option>
            </select>
          </div>
        </div>

        <!-- Botones -->
        <div class="form-buttons">
          <button
            type="button"
            @click="confirmCancel"
            style="color: white; text-decoration: none"
          >
            Cancelar
          </button>
          <button type="submit">Aceptar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
body {
  background-color: #f2f2f2;
}

.form-container {
  max-width: 600px; /* Ancho reducido */
  margin: 20px; /* Centra el formulario */
  padding: 20px;
  margin-left: 220px;
  background-color: rgb(245, 245, 245);
  border-radius: 8px;
}

h3 {
  text-align: left;
  margin-bottom: 20px;
  font-size: 18px;
}

.form-label {
  font-size: 14px;
  text-align: left;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-row {
  display: flex;
  flex-direction: row;
  gap: 15px;
}

.mb-3 {
  width: 200px;
  display: flex;
  flex-direction: column;
}

.form-control {
  padding: 1px 0px; /* Padding reducido */
  height: 25px; /* Altura reducida */
  font-size: 14px; /* Tamaño de fuente reducido */
  border: 1px solid #ccc;
  border-radius: 2px;
  color: #000; /* Asegura que el texto sea negro */
  background-color: #fff; /* Asegura que el fondo sea blanco */
}

select option {
  color: #000; /* Asegura que el texto de las opciones sea negro */
  background-color: #fff; /* Asegura que el fondo de las opciones sea blanco */
}

.form-buttons {
  display: flex;
  justify-content: flex-end;
  font-size: 14px;
}

button {
  margin-left: 10px;
  padding: 6px 15px; /* Padding reducido */
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  font-size: 14px; /* Tamaño de fuente reducido */
}

button[type="button"] {
  background-color: gray;
  color: white;
}

button[type="submit"] {
  background-color: #007bff;
  color: white;
}
</style>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "EditarAtraqueView",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      atraque: {
        nombre_atraque: "",
        puerto: "", // Asegúrate de que este campo coincida con el valor del backend
        terminal: "", // Asegúrate de que este campo coincida con el valor del backend
      },
      terminales: [], // Almacena las terminales obtenidas
      puertos: [], // Almacena los puertos obtenidos
    };
  },

  mounted() {
    this.getTerminales(); // Llama al método para obtener las terminales
    this.getPuertos(); // Llama al método para obtener los puertos
    this.get_atraque(); // Llama al método para obtener el atraque que se edita
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
    validateForm() {
      const nombre_atraque_regex = /^[A-Z][A-Za-z ]{2,99}$/;

      if (!nombre_atraque_regex.test(this.atraque.nombre_atraque)) {
        Swal.fire({
          icon: "error",
          title: "Error de validación",
          text: "El nombre del atraque debe comenzar con mayúscula, seguido de letras y espacios. No puede exceder los 100 caracteres.",
        });
        return false; // Detener el envío del formulario
      }

      return true; // El formulario es válido
    },

    async getTerminales() {
      try {
        const response = await axios.get("/api/terminales/");
        this.terminales =
          response.data.results; /* .results es lo que hay que agregar cada vez que hagas una peticion a la api, esto es debido a la estructura que vienen los objetos de la Api */
      } catch (error) {
        console.error("Error al obtener las terminales:", error);
      }
    },

    async getPuertos() {
      try {
        const response = await axios.get("/api/puertos/");
        this.puertos = response.data.results;
      } catch (error) {
        console.error("Error al obtener los puertos:", error);
      }
    },

    async get_atraque() {
      this.$store.commit("setIsLoading", true);
      const atraque_id = this.$route.params.id;

      try {
        const response = await axios.get(`/api/atraques/${atraque_id}/`);
        this.atraque = response.data; // Asegúrate de que los campos coincidan con el backend
        console.log("Datos del atraque:", this.atraque);
      } catch (error) {
        console.error("Error al obtener el atraque:", error);
        Swal.fire("Error", "No se pudo cargar el atraque.", "error");
      } finally {
        this.$store.commit("setIsLoading", false);
      }
    },

    async submitForm() {
      if (!this.validateForm()) {
        return; // Detener el envío si la validación falla
      }

      this.$store.commit("setIsLoading", true);
      const atraque_id = this.$route.params.id;

      try {
        // Envía solo los campos editables
        const data = {
          nombre_atraque: this.atraque.nombre_atraque,
          puerto: this.atraque.puerto,
          terminal: this.atraque.terminal,
        };

        await axios.patch(`/api/atraques/${atraque_id}/`, data);
        this.$router.push("/Atraques");
        Swal.fire(
          "Actualizado!",
          "El atraque ha sido modificado exitosamente.",
          "success"
        );
      } catch (error) {
        console.error("Error al actualizar el atraque:", error);
        Swal.fire("Error", "Hubo un error al actualizar el atraque.", "error");
      } finally {
        this.$store.commit("setIsLoading", false);
      }
    },
  },
};
</script>
