<template>
  <div class="form-container">
    <h2>Crear atraque</h2>
    <form @submit.prevent="saveAtraque">
      <div class="form-group">
        <label for="nombre_atraque">Nombre</label>
        <input type="text" v-model="nombre_atraque" step="0.01" required />
      </div>

      <div class="form-group">
        <label for="puerto">Puerto</label>
        <select v-model="puerto" required>
          <option v-for="puerto in puertos" :value="puerto.id" :key="puerto.id">
            {{ puerto.nombre_puerto }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="terminal">Terminal:</label>
        <select v-model="terminal" required>
          <option v-for="terminal in terminales" :value="terminal.id" :key="terminal.id">
            {{ terminal.nombre_terminal }}
          </option>
        </select>
      </div>

      <div class="form-buttons">
        <button type="button"><router-link style="color:white;text-decoration:none" to="/atraques">Cancelar</router-link> </button>
        <button>Aceptar</button>
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
font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
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

input,select {
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
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
  name: 'AdicionarAtraqueView',

  data() {
    return {
      terminales: [], // Almacena las terminales obtenidas
      puertos: [], // Almacena los puertos obtenidos
      nombre_atraque: '',
      terminal: '',
      puerto: '',
    };
  },

  mounted() {
    this.getTerminales(); // Llama al método para obtener las terminales
    this.getPuertos(); // Llama al método para obtener los puertos
  },

  methods: {
    validateForm() {
      const nombre_atraque_regex = /^[A-Z][A-Za-z ]{2,99}$/;
      let errorMessage = '';

      if (!nombre_atraque_regex.test(this.nombre_atraque)) {
        errorMessage +=
          'El campo "Nombre" debe comenzar con mayúscula, seguir con letras y espacios, y tener entre 3 y 100 caracteres.\n';
      }

      if (errorMessage) {
        Swal.fire({
          icon: 'error',
          title: 'Error de validación',
          text: errorMessage,
        });
        return false; // Detener el envío del formulario
      }

      return true; // El formulario es válido
    },

    async getTerminales() {
      try {
        const response = await axios.get('/api/terminales/');
        this.terminales = response.data;
      } catch (error) {
        console.error('Error al obtener las terminales:', error);
        Swal.fire('Error', 'Hubo un error al obtener las terminales.', 'error');
      }
    },

    async getPuertos() {
      try {
        const response = await axios.get('/api/puertos/');
        this.puertos = response.data;
      } catch (error) {
        console.error('Error al obtener los puertos:', error);
        Swal.fire('Error', 'Hubo un error al obtener los puertos.', 'error');
      }
    },

    async saveAtraque() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      const data = {
        nombre_atraque: this.nombre_atraque,
        terminal: this.terminal,
        puerto: this.puerto,
      };

      try {
        await axios.post('/api/atraques/', data);
        Swal.fire('Agregado!', 'El atraque ha sido añadido exitosamente.', 'success');
        this.$router.push('/Atraques');
      } catch (error) {
        console.log(error);
        Swal.fire('Error', 'Hubo un error al agregar el atraque.', 'error');
      }
    },
  },
};
</script>