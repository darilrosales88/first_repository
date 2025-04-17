<template>
  <div class="form-container">
    <h2>Adicionar Puerto</h2>
    <form @submit.prevent="saveItem">
      <!-- Campo Nombre del Puerto -->
      <div class="form-group">
        <label for="nombre_puerto">Nombre del Puerto:</label>
        <input type="text" v-model="nombre_puerto" required />
      </div>

      <!-- Campo País -->
      <div class="form-group">
        <label for="pais">País:</label>
        <select v-model="pais" required>
          <option v-for="item in paisOptions" :key="item.id" :value="item.id">{{ item.nombre_pais }}</option>
        </select>
      </div>

      <!-- Campo Provincia -->
      <div class="form-group">
        <label for="provincia">Provincia:</label>
        <select v-model="provincia">
          <option v-for="item in provinciaOptions" :key="item.id" :value="item.id">{{ item.nombre_provincia }}</option>
        </select>
      </div>

      <!-- Campo Servicio Portuario -->
      <div class="form-group">
        <label for="servicio_portuario">Servicio Portuario:</label>
        <select v-model="servicio_portuario">
          <option v-for="item in servicioPortuarioOptions" :key="item.id" :value="item.id">{{ item.nombre_territorio }}</option>
        </select>
      </div>

      <!-- Campo Latitud -->
      <div class="form-group">
        <label for="latitud">Latitud:</label>
        <input type="text" v-model="latitud" required />
      </div>

      <!-- Campo Longitud -->
      <div class="form-group">
        <label for="longitud">Longitud:</label>
        <input type="text" v-model="longitud" required />
      </div>

      <!-- Botones -->
      <div class="form-buttons">
        <button type="button">
          <router-link style="color: white; text-decoration: none" to="/Puertos">Cancelar</router-link>
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
import Swal from 'sweetalert2';
import axios from 'axios';

export default {
  data() {
    return {
      nombre_puerto: '',
      pais: '',
      provincia: '',
      servicio_portuario: '',
      latitud: '',
      longitud: '',
      paisOptions: [],
      provinciaOptions: [],
      servicioPortuarioOptions: []
    };
  },
  mounted() {
    this.fetchOptions();
  },
  methods: {
    validateForm() {
      const nombrePuertoRegex = /^[A-Z][a-zA-ZáéíóúÁÉÍÓÚñÑäëöüÄËÏÜ ]{2,99}$/;
      const latitudRegex = /^[\d\.]+$/;
      const longitudRegex = /^[\d\.]+$/;
      let errorMessage = '';

      if (!nombrePuertoRegex.test(this.nombre_puerto)) {
        errorMessage += 'El campo "Nombre del Puerto" comienza con mayúscula y admite letras y espacios. Tamaño mínimo 3 caracteres y máximo 100 caracteres.\n';
      }
      if (!latitudRegex.test(this.latitud)) {
        errorMessage += 'El campo "Latitud" admite únicamente números y puntos.\n';
      }
      if (!longitudRegex.test(this.longitud)) {
        errorMessage += 'El campo "Longitud" admite únicamente números y puntos.\n';
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
    async fetchOptions() {
      try {
        const [paisResponse, provinciaResponse, servicioPortuarioResponse] = await Promise.all([
          axios.get('/api/paises/'),
          axios.get('/api/provincias/'),
          axios.get('/api/territorios/')
        ]);

        this.paisOptions = paisResponse.data;
        this.provinciaOptions = provinciaResponse.data;
        this.servicioPortuarioOptions = servicioPortuarioResponse.data;
      } catch (error) {
        console.error('Error al obtener las opciones:', error);
      }
    },
    async saveItem() {
      if (!this.validateForm()) {
        return; // Detener el envío si la validación falla
      }

      this.$store.commit('setIsLoading', true);
      const puerto = {
        nombre_puerto: this.nombre_puerto,
        pais: this.pais,
        provincia: this.provincia,
        servicio_portuario: this.servicio_portuario,
        latitud: this.latitud,
        longitud: this.longitud,
      };

      try {
        await axios.post('/api/puertos/', puerto);
        this.$router.push('/Puertos');
        Swal.fire('Agregado!', 'El puerto ha sido insertado exitosamente.', 'success');
      } catch (error) {
        console.error('Error al agregar el puerto:', error);
        Swal.fire('Error', 'Hubo un error al agregar el puerto.', 'error');
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    },
  },
};
</script>