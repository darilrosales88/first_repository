<template>
  <div class="form-container">
    <h2>Editar Puerto {{nombre_puerto}}</h2>
    <form @submit.prevent="updateItem" class="form-grid">
      <!-- Campo Nombre del Puerto -->
      <div class="form-group">
        <label for="nombre_puerto">Nombre del Puerto:</label>
        <input type="text" style="padding: 3px;" v-model="nombre_puerto" required />
      </div>

      <!-- Campo País -->
      <div class="form-group">
        <label for="pais">País:</label>
        <select v-model="pais" required>
          <option style="padding: 5px;" v-for="item in paisOptions" :key="item.id" :value="item.id">{{ item.nombre_pais }}</option>
        </select>
      </div>

      <!-- Campo Provincia -->
      <div class="form-group">
        <label for="provincia">Provincia:</label>
        <select style="padding: 5px;" v-model="provincia">
          <option v-for="item in provinciaOptions" :key="item.id" :value="item.id">{{ item.nombre_provincia }}</option>
        </select>
      </div>

      <!-- Campo Servicio Portuario -->
      <div class="form-group">
        <label for="servicio_portuario">Servicio Portuario:</label>
        <select style="padding: 5px;" v-model="servicio_portuario">
          <option v-for="item in servicioPortuarioOptions" :key="item.id" :value="item.id">{{ item.nombre_territorio }}</option>
        </select>
      </div>

      <!-- Campo Latitud -->
      <div class="form-group">
        <label for="latitud">Latitud:</label>
        <input style="padding: 3px;" type="text" v-model="latitud" required />
      </div>

      <!-- Campo Longitud -->
      <div class="form-group">
        <label for="longitud">Longitud:</label>
        <input style="padding: 3px;" type="text" v-model="longitud" required />
      </div>

      <!-- Botones -->
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
import Swal from 'sweetalert2';
import axios from 'axios';

export default {
  data() {
    return {
      puertoId: this.$route.params.id, // Asumimos que el ID de puerto se pasa como parámetro de la ruta
      nombre_puerto: '',
      pais: '',
      provincia: '',
      servicio_portuario: '',
      latitud: '',
      longitud: '',
      paisOptions: [],
      provinciaOptions: [],
      servicioPortuarioOptions: [],
    };
  },
  mounted() {
    this.fetchOptions();
    this.fetchPuerto();
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
    // Validación del formulario (igual que en AdicionarPuerto.vue)
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

    // Obtener las opciones para los select (igual que en AdicionarPuerto.vue)
    async fetchOptions() {
      try {
        const [paisResponse, provinciaResponse, servicioPortuarioResponse] = await Promise.all([
          axios.get('/api/paises/'),
          axios.get('/api/provincias/'),
          axios.get('/api/territorios/'),
        ]);

        this.paisOptions = paisResponse.data;
        this.provinciaOptions = provinciaResponse.data;
        this.servicioPortuarioOptions = servicioPortuarioResponse.data;
      } catch (error) {
        console.error('Error al obtener las opciones:', error);
      }
    },
    
    // Obtener los datos del puerto a editar
    async fetchPuerto() {
      try {
        const response = await axios.get(`/api/puertos/${this.puertoId}/`);
        const puerto = response.data;
        this.nombre_puerto = puerto.nombre_puerto;
        this.pais = puerto.pais;
        this.provincia = puerto.provincia;
        this.servicio_portuario = puerto.servicio_portuario;
        this.latitud = puerto.latitud;
        this.longitud = puerto.longitud;
      } catch (error) {
        console.error('Error al obtener los datos del puerto:', error);
      }
    },

    // Actualizar los datos del puerto
    async updateItem() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }
      
      const payload = {
        nombre_puerto: this.nombre_puerto,
        pais: this.pais,
        provincia: this.provincia,
        servicio_portuario: this.servicio_portuario,
        latitud: this.latitud,
        longitud: this.longitud,
      };

      try {
        await axios.put(`/api/puertos/${this.puertoId}/`, payload);
        Swal.fire("Actualizado!", "El puerto ha sido actualizado exitosamente.", "success");
        this.$router.push("/Puertos");
      } catch (error) {
        console.error("Error al actualizar el puerto:", error);
        Swal.fire("Error", "Hubo un error al actualizar el puerto.", "error");
      }
    },
  },
};
</script>