<template>
  <div class="form-container">
    <h2>Editar estructura de ubicación {{ estructura.nombre_estructura_ubicacion }}</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="terminal">Terminal</label>
        <select v-model="estructura.terminal" required>
          <option v-for="terminal in terminales" :value="terminal.id" :key="terminal.id">
            {{ terminal.nombre_terminal }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="tipo_estructura">Tipo de estructura</label>
        <select v-model="estructura.tipo_estructura" required>
          <option v-for="tipo_estructura in tipos_estructuras" :value="tipo_estructura.id" :key="tipo_estructura.id">
            {{ tipo_estructura.nombre_tipo_estructura_ubicacion }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="tipo_estructura">Estructura padre</label>
        <select v-model="estructura.estructura_padre">
          <option v-for="estructura in estructuras" :value="estructura.id" :key="estructura.id">
            {{ estructura.nombre_estructura_ubicacion }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="nombre_estructura_ubicacion">Nombre</label>
        <input type="text" v-model="estructura.nombre_estructura_ubicacion" step="0.01" required />
      </div>

      <div class="form-group">
        <label for="capacidad">Capacidad</label>
        <input type="number" v-model="estructura.capacidad" step="0.01" required />
      </div>

      <div class="form-buttons">
        <button type="button">
          <router-link style="color:white;text-decoration:none" to="/EstructuraUbicacion">Cancelar</router-link>
        </button>
        <button type="submit">Aceptar</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
/* Estilos sin cambios */
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
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
  name: 'EditarEstructuradeUbicacion',

  data() {
    return {
      estructura: {},
      terminales: [], // Almacena las terminales obtenidas
      tipos_estructuras: [], // Almacena los tipos de estructuras obtenidas
      estructuras: [], // Almacena las estructuras obtenidas
    };
  },

  mounted() {
    this.getTerminales(); // Llama al método para obtener las terminales
    this.getTiposEstructuras(); // Llama al método para obtener los tipos de estructuras
    this.getEstructuras(); // Llama al método para obtener las estructuras
    this.get_estructura();
  },

  methods: {
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

    validateForm() {
      const nombre_estructura_ubicacion_regex = /^[A-Z][\w\d\W]{2,99}$/;

      if (!nombre_estructura_ubicacion_regex.test(this.estructura.nombre_estructura_ubicacion)) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'El nombre debe comenzar con mayúscula, aceptar letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y máximo 100 caracteres.',
        });
        return false;
      }

      return true;
    },

    async get_estructura() {
      this.$store.commit('setIsLoading', true);
      const estructura_id = this.$route.params.id;
      try {
        const response = await axios.get(`/api/estructuras_ubicacion/${estructura_id}/`);
        this.estructura = response.data;
      } catch (error) {
        console.log(error);
      }
      this.$store.commit('setIsLoading', false);
    },

    async submitForm() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      this.$store.commit('setIsLoading', true);
      const estructura_id = this.$route.params.id;
      const data = {
        ...this.estructura,
      };

      try {
        await axios.patch(`/api/estructuras_ubicacion/${estructura_id}/`, data);
        this.$router.push('/EstructuraUbicacion');
        Swal.fire('Actualizado!', 'La estructura de ubicación ha sido modificada exitosamente.', 'success');
      } catch (error) {
        console.log(error);
        Swal.fire('Error', 'Hubo un error al actualizar la estructura de ubicación.', 'error');
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    },
  },
};
</script>