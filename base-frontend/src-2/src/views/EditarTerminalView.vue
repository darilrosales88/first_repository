<template>
  <div class="form-container">
    <h2>Editar Terminal</h2>
    <form @submit.prevent="updateTerminal">
      <div class="form-group">
        <label for="nombre">Nombre*:</label>
        <input type="text" id="nombre" v-model="nombre_terminal" required />
      </div>
      <div class="form-group">
        <label for="puerto">Puerto:*</label>
        <select id="puerto" v-model="puerto" required>
          <option value="">-Seleccione-</option>
          <option v-for="item in puertoOptions" :key="item.id" :value="item.id">{{ item.nombre_puerto }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="capacidad_almacen_importacion">Cap. almacén importación:*</label>
        <input type="text" id="capacidad_almacen_importacion" v-model="capacidad_almacen_importacion" required />
      </div>
      <div class="form-group">
        <label for="capacidad_almacen_exportacion">Cap. almacén exportación:*</label>
        <input type="text" id="capacidad_almacen_exportacion" v-model="capacidad_almacen_exportacion" required />
      </div>
      <div class="form-buttons">
        <button type="button" @click="confirmCancel" style="color:white;text-decoration:none">Cancelar</button>
        <button>Aceptar</button>
      </div>
    </form>
  </div>
</template>

<style>
.form-container {
  max-width: 450px;
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
  name: "EditarTerminalView",

  data() {
    return {
      terminalId: this.$route.params.id,
      nombre_terminal: "",
      puerto: "",
      puertoOptions: [],
      capacidad_almacen_importacion: "",
      capacidad_almacen_exportacion: "",
    };
  },

  mounted() {
    this.getPuertos(); // Obtener la lista de puertos
    this.getTerminal(); // Obtener los datos de la terminal a editar
  },

  methods: {
    confirmCancel() {
    Swal.fire({
    title: '¿Está seguro de que quiere cancelar la operación?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    cancelmButtonText: 'Cancelar',
    confirmButtonText: 'Aceptar'
  }).then((result) => {
    if (result.isConfirmed) {
      window.history.back();
    }
  });
},
    validateForm() {
      const nombre_terminal_regex = /^[A-Z][a-zA-ZáéíóúÁÉÍÓÚñÑäëöüÄËÏÜ ]{2,99}$/;
      const decimal_regex = /^\d+(\.\d{1,2})?$/; // Validar que tenga máximo 2 decimales

      let valid = true;

      if (!nombre_terminal_regex.test(this.nombre_terminal)) {
        Swal.fire('Error en el nombre', 'El nombre debe comenzar con mayúscula, seguido de letras y espacios. Tamaño mínimo: 3 caracteres. Tamaño máximo: 100 caracteres.', 'error');
        valid = false;
      }

      if (this.puerto === "") {
        Swal.fire('Error en el puerto', 'Debe seleccionar un puerto.', 'error');
        valid = false;
      }

      if (this.capacidad_almacen_importacion === "" || !decimal_regex.test(this.capacidad_almacen_importacion)) {
        Swal.fire('Error en la capacidad de almacén de importación', 'Debe ingresar la capacidad de almacén de importación con máximo 2 decimales.', 'error');
        valid = false;
      }

      if (this.capacidad_almacen_exportacion === "" || !decimal_regex.test(this.capacidad_almacen_exportacion)) {
        Swal.fire('Error en la capacidad de almacén de exportación', 'Debe ingresar la capacidad de almacén de exportación con máximo 2 decimales.', 'error');
        valid = false;
      }

      return valid;
    },

    // Obtener la lista de puertos
    async getPuertos() {
      try {
        const response = await axios.get('/api/puertos/');
        this.puertoOptions = response.data;
      } catch (error) {
        console.error('Error al obtener los puertos:', error);
      }
    },

    // Obtener los datos de la terminal a editar
    async getTerminal() {
      try {
        const response = await axios.get(`/api/terminales/${this.terminalId}/`);
        const terminal = response.data;
        this.nombre_terminal = terminal.nombre_terminal;
        this.puerto = terminal.puerto;
        this.capacidad_almacen_importacion = terminal.capacidad_almacen_importacion;
        this.capacidad_almacen_exportacion = terminal.capacidad_almacen_exportacion;
      } catch (error) {
        console.error('Error al obtener la terminal:', error);
        Swal.fire('Error', 'No se pudo cargar la terminal.', 'error');
        this.$router.push('/Terminal'); // Redirigir si hay un error
      }
    },

    // Guardar los cambios
    async updateTerminal() {
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      const payload = {
        nombre_terminal: this.nombre_terminal,
        puerto: this.puerto,
        capacidad_almacen_importacion: parseFloat(this.capacidad_almacen_importacion).toFixed(2),
        capacidad_almacen_exportacion: parseFloat(this.capacidad_almacen_exportacion).toFixed(2),
      };

      try {
        console.log("Payload:", payload); // Log para verificar el payload
        const response = await axios.put(`/api/terminales/${this.terminalId}/`, payload);
        console.log("Response:", response); // Log para verificar la respuesta
        Swal.fire("Actualizado!", "La terminal ha sido actualizada exitosamente.", "success");
        this.$router.push("/Terminal");
      } catch (error) {
        if (error.response && error.response.data) {
          console.error("Error response data:", error.response.data); // Log del mensaje de error detallado
        }
        console.error("Error al actualizar la terminal:", error);
        Swal.fire("Error", "Hubo un error al actualizar la terminal.", "error");
      }
    },
  },
};
</script>
