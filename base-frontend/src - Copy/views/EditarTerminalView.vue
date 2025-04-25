<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container">
      <h3 style="color: #002A68;">Editar Terminal</h3>
      <form @submit.prevent="updateTerminal" class="form-grid">
        <!-- Campo Nombre -->
        <div class="mb-3">
          <label for="nombre" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre" v-model="nombre_terminal" required />
        </div>

        <!-- Campo Puerto -->
        <div class="mb-3">
          <label for="puerto" class="form-label">Puerto:<span style="color: red;">*</span></label>
          <select class="form-control" id="puerto" v-model="puerto" required>
            <option value="">-Seleccione-</option>
            <option v-for="item in puertoOptions" :key="item.id" :value="item.id">{{ item.nombre_puerto }}</option>
          </select>
        </div>

        <!-- Campo Capacidad Almacén Importación -->
        <div class="mb-3">
          <label for="capacidad_almacen_importacion" class="form-label">Cap. almacén importación:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="capacidad_almacen_importacion" v-model="capacidad_almacen_importacion" required />
        </div>

        <!-- Campo Capacidad Almacén Exportación -->
        <div class="mb-3">
          <label for="capacidad_almacen_exportacion" class="form-label">Cap. almacén exportación:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="capacidad_almacen_exportacion" v-model="capacidad_almacen_exportacion" required />
        </div>

        <!-- Botones -->
        <div class="form-buttons">
          <button type="button" @click="confirmCancel" style="color:white;text-decoration:none">Cancelar</button>
          <button type="submit">Aceptar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
body {
  background-color: #F2F2F2;
}

.form-container {
  max-width: 680px; /* Ancho reducido */
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

.form-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 3 columnas de igual tamaño */
  gap: 15px; /* Espacio entre los elementos */
}

.mb-3 {
  width: 200px;
  display: flex;
  flex-direction: column;
  gap: 5px;
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
  grid-column: span 3; /* Los botones ocupan las 2 columnas */
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
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: "EditarTerminalView",
  components: {
    NavbarComponent,
  },
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
