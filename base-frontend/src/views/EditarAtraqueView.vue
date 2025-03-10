<template>
  <div class="form-container">
    <h2>Editar atraque <strong>{{ atraque.nombre_atraque }}</strong></h2>
    <form @submit.prevent="submitForm">
      <!-- Campo Nombre del Atraque -->
      <div class="form-group">
        <label for="nombre_atraque">Nombre:<span style="color: red;">*</span></label>
        <input type="text" style="padding: 3px;"  v-model="atraque.nombre_atraque" required />
      </div>

      <!-- Campo Puerto -->
      <div class="form-group">
        <label for="puerto">Puerto:<span style="color: red;">*</span></label>
        <select v-model="atraque.puerto" required>
          <option v-for="puerto in puertos" :value="puerto.id" :key="puerto.id">
            {{ puerto.nombre_puerto }}
          </option>
        </select>
      </div>

      <!-- Campo Terminal -->
      <div class="form-group">
        <label for="terminal">Terminal:<span style="color: red;">*</span></label>
        <select v-model="atraque.terminal" required>
          <option v-for="terminal in terminales" :value="terminal.id" :key="terminal.id">
            {{ terminal.nombre_terminal }}
          </option>
        </select>
      </div>

      <!-- Botones -->
      <div class="form-buttons">
        <button type="button" @click="confirmCancel" style="color:white;text-decoration:none">Cancelar</button>
        <button>Aceptar</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
  name: 'EditarAtraqueView',

  data() {
    return {
      atraque: {
        nombre_atraque: '',
        puerto: '', // Asegúrate de que este campo coincida con el valor del backend
        terminal: '', // Asegúrate de que este campo coincida con el valor del backend
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
      const nombre_atraque_regex = /^[A-Z][A-Za-z ]{2,99}$/;

      if (!nombre_atraque_regex.test(this.atraque.nombre_atraque)) {
        Swal.fire({
          icon: 'error',
          title: 'Error de validación',
          text: 'El nombre del atraque debe comenzar con mayúscula, seguido de letras y espacios. No puede exceder los 100 caracteres.',
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
      }
    },

    async getPuertos() {
      try {
        const response = await axios.get('/api/puertos/');
        this.puertos = response.data;
      } catch (error) {
        console.error('Error al obtener los puertos:', error);
      }
    },

    async get_atraque() {
      this.$store.commit('setIsLoading', true);
      const atraque_id = this.$route.params.id;

      try {
        const response = await axios.get(`/api/atraques/${atraque_id}/`);
        this.atraque = response.data; // Asegúrate de que los campos coincidan con el backend
        console.log('Datos del atraque:', this.atraque);
      } catch (error) {
        console.error('Error al obtener el atraque:', error);
        Swal.fire('Error', 'No se pudo cargar el atraque.', 'error');
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    },

    async submitForm() {
      if (!this.validateForm()) {
        return; // Detener el envío si la validación falla
      }

      this.$store.commit('setIsLoading', true);
      const atraque_id = this.$route.params.id;

      try {
        // Envía solo los campos editables
        const data = {
          nombre_atraque: this.atraque.nombre_atraque,
          puerto: this.atraque.puerto,
          terminal: this.atraque.terminal,
        };

        await axios.patch(`/api/atraques/${atraque_id}/`, data);
        this.$router.push('/Atraques');
        Swal.fire('Actualizado!', 'El atraque ha sido modificado exitosamente.', 'success');
      } catch (error) {
        console.error('Error al actualizar el atraque:', error);
        Swal.fire('Error', 'Hubo un error al actualizar el atraque.', 'error');
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    },
  },
};
</script>
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

input, select {
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