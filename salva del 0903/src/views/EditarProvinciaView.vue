<template>
  <div class="form-container">
    <h2>Editar Provincia</h2>
    <form @submit.prevent="saveItem">
      <div class="form-group">
        <label for="codigo">Código:*</label>
        <input type="text" v-model="codigo" required />
      </div>
      <div class="form-group">
        <label for="nombre">Nombre*:</label>
        <input type="text" v-model="nombre_provincia" required />
      </div>
      <div class="form-group">
        <label for="pais">País*:</label>
        <select id="pais" v-model="pais" required>
          <option v-for="item in selectedPais" :key="item.id" :value="item.id">{{ item.nombre_pais }}</option>
        </select>
      </div>
      <div class="form-buttons">
        <button type="button">
          <router-link style="color:white;text-decoration:none" to="/Provincia">Cancelar</router-link>
        </button>
        <button type="submit">Guardar Cambios</button>
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
  name: 'EditarProvinciaView',

  data() {
    return {
      selectedPais: [], // Almacena los países obtenidos
      codigo: '',
      codigo_error: null,
      pais: '',
      nombre_provincia: '',
      nombre_provincia_error: null,
      provinciaId: null, // ID de la provincia que se está editando
    };
  },

  mounted() {
    this.getPaises(); // Obtener la lista de países
    this.getProvincia(); // Obtener los datos de la provincia a editar
  },

  methods: {
    // Obtener los datos de la provincia a editar
    async getProvincia() {
      this.provinciaId = this.$route.params.id; // Obtener el ID de la provincia desde la URL
      try {
        const response = await axios.get(`/api/provincias/${this.provinciaId}/`);
        const provincia = response.data;
        this.codigo = provincia.codigo;
        this.nombre_provincia = provincia.nombre_provincia;
        this.pais = provincia.pais;
      } catch (error) {
        console.error('Error al obtener la provincia:', error);
        Swal.fire('Error', 'No se pudo cargar la provincia.', 'error');
        this.$router.push('/Provincia'); // Redirigir si hay un error
      }
    },

    // Validar el formulario
    validateForm() {
      const codigo_regex = /[0-9]{2}$/;
      const nombre_provincia_regex = /^[A-Z][a-zA-ZáéíóúÁÉÍÓÚñÑäëöüÄËÏÜ ]{2,99}$/;

      let valid = true;

      if (!codigo_regex.test(this.codigo)) {
        this.codigo_error = 'Este campo sólo admite dos números.';
        Swal.fire({
          icon: 'error',
          title: 'Error en el código',
          text: this.codigo_error,
        });
        valid = false;
      } else {
        this.codigo_error = null;
      }

      if (!nombre_provincia_regex.test(this.nombre_provincia)) {
        this.nombre_provincia_error =
          'Este campo comienza con mayúscula seguido de espacio, caracteres alfabéticos y no puede exceder los 100 caracteres.';
        Swal.fire({
          icon: 'error',
          title: 'Error en el nombre de la provincia',
          text: this.nombre_provincia_error,
        });
        valid = false;
      } else {
        this.nombre_provincia_error = null;
      }

      return valid;
    },

    // Obtener la lista de países
    async getPaises() {
      try {
        const response = await axios.get('/api/paises/');
        this.selectedPais = response.data;
      } catch (error) {
        console.error('Error al obtener los países:', error);
      }
    },

    // Guardar los cambios
    async saveItem() {
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      const data = {
        nombre_provincia: this.nombre_provincia,
        pais: this.pais,
        codigo: this.codigo,
      };

      try {
        await axios.put(`/api/provincias/${this.provinciaId}/`, data);
        Swal.fire('Actualizado!', 'La provincia ha sido actualizada exitosamente.', 'success');
        this.$router.push('/Provincia');
      } catch (error) {
        console.log(error);
        Swal.fire('Error', 'Hubo un error al actualizar la provincia.', 'error');
      }
    },
  },
};
</script>