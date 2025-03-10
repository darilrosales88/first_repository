<template>
  <div class="form-container">
    <h2>Adicionar estructura de ubicación</h2>
    <form @submit.prevent="save_estructura" class="form-grid">
      <div class="form-group">
        <label for="terminal">Terminal:<span style="color: red;">*</span></label>
        <select style="padding: 5px;" v-model="terminal" required>
          <option v-for="terminal in terminales" :value="terminal.id" :key="terminal.id">
            {{ terminal.nombre_terminal }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="tipo_estructura">Tipo de estructura:<span style="color: red;">*</span></label>
        <select style="padding: 5px;" v-model="tipo_estructura" required>
          <option v-for="tipo_estructura in tipos_estructuras" :value="tipo_estructura.id" :key="tipo_estructura.id">
            {{ tipo_estructura.nombre_tipo_estructura_ubicacion }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="tipo_estructura">Estructura padre:</label>
        <select style="padding: 5px;" v-model="estructura_padre">
          <option v-for="estructura in estructuras" :value="estructura.id" :key="estructura.id">
            {{ estructura.nombre_estructura_ubicacion }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="nombre_estructura_ubicacion">Nombre:<span style="color: red;">*</span></label>
        <input type="text" style="padding: 3px;" v-model="nombre_estructura_ubicacion" step="0.01" required />
      </div>

      <div class="form-group">
        <label for="capacidad">Capacidad:<span style="color: red;">*</span></label>
        <input style="padding: 3px;" type="number" v-model="capacidad" step="0.01" required />
      </div>

      <div class="form-buttons">
        <button type="button" @click="confirmCancel" style="color:white;text-decoration:none">Cancelar</button>
        <button>Aceptar</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.form-container {
  max-width: 600px; /* Ajusta el ancho máximo del contenedor */
  margin: 50px; /* Centra el contenedor */
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

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 4 columnas de igual tamaño */
  gap: 15px; /* Espacio entre los elementos */
}

.form-group {
  text-align: left;
  width: 260px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 13px;
}

label {
  font-weight: bold;
}

input, select {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.form-buttons {
  grid-column: span 2; /* Los botones ocupan las 4 columnas */
  display: flex;
  justify-content: end;
  font-size: 15px;
  margin-top: 20px;
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
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
  name: 'CrearEstructuradeUbicacion',
  data() {
    return {
      terminales: [], // Almacena las terminales obtenidas
      tipos_estructuras: [], // Almacena los tipos de estructuras obtenidas
      estructuras: [], // Almacena las estructuras obtenidas
      nombre_estructura_ubicacion: '',
      terminal: '',
      tipo_estructura: '',
      estructura_padre: '',
      capacidad: '',
    };
  },
  mounted() {
    this.getTerminales(); // Llama al método para obtener las terminales
    this.getTiposEstructuras(); // Llama al método para obtener los tipos de estructuras
    this.getEstructuras(); // Llama al método para obtener las estructuras
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
      const nombre_estructura_ubicacion_regex = /^[A-Z][\w\d\W]{2,99}$/;

      if (!nombre_estructura_ubicacion_regex.test(this.nombre_estructura_ubicacion)) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'El nombre debe comenzar con mayúscula, aceptar letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y máximo 100 caracteres.',
        });
        return false;
      }

      return true;
    },
    async getTerminales() {
      try {
        const response = await axios.get('/api/terminales/');
        this.terminales = response.data;
      } catch (error) {
        console.error('Error al obtener las terminales:', error);
      }
    },
    async getTiposEstructuras() {
      try {
        const response = await axios.get('/api/tipos_estructuras_ubicacion/');
        this.tipos_estructuras = response.data;
      } catch (error) {
        console.error('Error al obtener los tipos de estructuras:', error);
      }
    },
    async getEstructuras() {
      try {
        const response = await axios.get('/api/estructuras_ubicacion/');
        this.estructuras = response.data;
      } catch (error) {
        console.error('Error al obtener las estructuras:', error);
      }
    },
    async save_estructura() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      const data = {
        terminal: this.terminal,
        tipo_estructura: this.tipo_estructura,
        estructura_padre: this.estructura_padre,
        nombre_estructura_ubicacion: this.nombre_estructura_ubicacion,
        capacidad: this.capacidad,
      };

      try {
        await axios.post('/api/estructuras_ubicacion/', data);
        Swal.fire('Agregado!', 'La estructura de ubicación ha sido añadida exitosamente.', 'success');
        this.$router.push('/EstructuraUbicacion');
      } catch (error) {
        console.log(error);
        Swal.fire('Error', 'Hubo un error al agregar la estructura de ubicación.', 'error');
      }
    },
  },
};
</script>