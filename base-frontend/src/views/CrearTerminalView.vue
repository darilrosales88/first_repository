<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container">
      <h3>Crear Terminal</h3>
      <form @submit.prevent="createTerminal" class="form-grid">
        <!-- Campo Nombre de la Terminal -->
       
        <div class="mb-3">
          <label for="nombre_terminal" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre_terminal" v-model="nombre_terminal" required />
        </div>

        <!-- Campo Puerto -->
        <div class="mb-3">
          <label for="puerto" class="form-label">Puerto:<span style="color: red;">*</span></label>
          <select class="form-control" id="puerto" v-model="puerto" required>
            <option value="">-Seleccione-</option>
            <option v-for="item in puertoOptions" :key="item.id" :value="item.id">{{ item.nombre_puerto }}</option>
          </select>
        </div>

        <!-- Campo Capacidad de Almacén de Importación -->
        <div class="mb-3">
          <label for="capacidad_almacen_importacion" class="form-label">Cap. almacén importación:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="capacidad_almacen_importacion" v-model="capacidad_almacen_importacion" required />
        </div>

        <!-- Campo Capacidad de Almacén de Exportación -->
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
  margin: 20px ; /* Centra el formulario */
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
.form-label{
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
.form-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 2 columnas de igual tamaño */
  gap: 15px; /* Espacio entre los elementos */
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
}

.form-buttons {
  grid-column: span 3; /* Los botones ocupan las 3 columnas */
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
  name: "CrearTerminalView",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      terminales: [],
      puertoOptions: [],
      nombre_terminal: "",
      puerto: "",
      puerto_options: [
        { value: "1", text: "Puerto escondido" },
        { value: "2", text: "Puerto Dos" },
      ],
      capacidad_almacen_importacion: "",
      capacidad_almacen_exportacion: "",
    };
  },
  mounted() {
    this.getPuertos(); // Obtener la lista de países
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

  // Obtener la lista de países
  async getPuertos() {
      try {
        const response = await axios.get('/api/puertos/');
        this.puertoOptions = response.data;
      } catch (error) {
        console.error('Error al obtener los puertos:', error);
      }
    },

  async createTerminal() {
    if (!this.validateForm()) {
      return;
    }

    const payload = {
      nombre_terminal: this.nombre_terminal,
      puerto: this.puerto,
      capacidad_almacen_importacion: parseFloat(this.capacidad_almacen_importacion).toFixed(2),
      capacidad_almacen_exportacion: parseFloat(this.capacidad_almacen_exportacion).toFixed(2),
    };

    try {
      console.log("Payload:", payload);
      const response = await axios.post("/api/terminales/", payload);
      console.log("Response:", response);
      Swal.fire("Creado!", "La terminal ha sido creada exitosamente.", "success");
      this.$router.push("/Terminal");
    } catch (error) {
      if (error.response && error.response.data) {
        console.error("Error response data:", error.response.data);
      }
      console.error("Error al crear la terminal:", error);
      Swal.fire("Error", "Hubo un error al crear la terminal.", "error");
    }
  },
},
};
</script>
