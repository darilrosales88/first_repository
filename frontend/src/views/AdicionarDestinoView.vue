<template>
  <div class="form-container">
    <h2>Crear Destino</h2>
    <form @submit.prevent="createDestino">
      <div class="form-group">
        <label for="cliente">Cliente*:</label>
        <select id="cliente" v-model="cliente" required>
          <option value="">-Seleccione-</option>
          <option v-for="item in clienteOptions" :key="item.id" :value="item.id">
            {{ item.nombre }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="destino">Destino*:</label>
        <input type="text" id="destino" v-model="destino" required />
      </div>
      <div class="form-buttons">
        <button type="button">
          <router-link style="color: white; text-decoration: none" to="/Destino">Cancelar</router-link>
        </button>
        <button type="submit">Aceptar</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.form-container {
  max-width: 450px;
  margin: 50px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
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
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  font-size: 13px;
}

label {
  flex: 1;
  text-align: right;
  font-weight: bold;
}

input,
select {
  flex: 2;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.form-buttons {
  display: flex;
  justify-content: end;
  font-size: 15px;
}

button {
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

export default {
  name: "CrearDestinoView",

  data() {
    return {
      cliente: "",
      clienteOptions: [],
      destino: "",
      errores: "",
    };
  },

  mounted() {
    this.getClientes(); // Obtener la lista de clientes
  },

  methods: {
    // Validar el formulario
    validateForm() {
      this.errores = "";
      const destino_regex = /^[A-Z]{1}[\d\w\W ]{2,99}$/;

      let valid = true;

      if (this.cliente === "") {
        this.errores += "Debe seleccionar un cliente.<br>";
        valid = false;
      }

      if (!destino_regex.test(this.destino)) {
        this.errores +=
          "El destino debe comenzar con mayúscula seguido de letras, números y caracteres especiales. Tamaño mínimo: 3 caracteres. Tamaño máximo: 100 caracteres.";
        valid = false;
      }

      return valid;
    },

    // Obtener la lista de clientes
    async getClientes() {
      try {
        const response = await axios.get("/api/entidades/");
        this.clienteOptions = response.data;
      } catch (error) {
        console.error("Error al obtener los clientes:", error);
      }
    },

    // Verificar si el destino ya existe
    async doesDestinoExist() {
      try {
        const response = await axios.get("/api/destinos/verificar-existencia/", {
          params: {
            cliente: this.cliente,
            destino: this.destino,
          },
        });
        return response.data.exists; // ese exists es la variable declarada en la funcion verificar_destino en el views.py
      } catch (error) {
        console.error("Error al verificar el destino:", error);
        return false; // En caso de error, asumimos que no existe
      }
    },

    // Crear un nuevo destino
    async createDestino() {
      if (!this.validateForm()) {
        Swal.fire("Errores en la entrada de datos", this.errores, "error");
        return; // Si la validación falla, no enviar el formulario
      }

      // Verificar si el destino ya existe
      if (await this.doesDestinoExist()) {
        Swal.fire("Error", "El destino ya existe para el cliente seleccionado.", "error");
        return;
      }

      const payload = {
        cliente: this.cliente,
        destino: this.destino,
      };

      try {
        await axios.post("/api/destinos/", payload);
        Swal.fire("Creado!", "El destino ha sido creado exitosamente.", "success");
        this.$router.push("/Destino");
      } catch (error) {
        console.error("Error al crear el destino:", error);

        // Manejar errores específicos del backend
        if (error.response && error.response.status === 400 && error.response.data.errors) {
          const mensajesErrores = error.response.data.errors.map((err) => err.message).join("<br>");
          Swal.fire("Error", mensajesErrores, "error");
        } else if (error.response && error.response.status === 409) {
          // Código 409 para conflicto de datos duplicados
          Swal.fire("Error", "El destino ya existe para el cliente seleccionado.", "error");
        } else {
          Swal.fire("Error", "Hubo un error al crear el destino.", "error");
        }
      }
    },
  },
};
</script>