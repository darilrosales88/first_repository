<template>
  <div class="form-container">
    <h2>Editar Contenedor</h2>
    <form @submit.prevent="update_contenedor">
      <div class="form-group">
        <label for="id_contenedor">Id</label>
        <input type="text" v-model="contenedor.id_contenedor" required disabled/>
      </div>

      <div class="form-group">
        <label for="tipo_contenedor">Tipo de contenedor:</label>
        <select v-model="contenedor.tipo_contenedor" required>
          <option v-for="t_contenedor in contenedores_options" :value="t_contenedor.value" :key="t_contenedor.value">
            {{ t_contenedor.text }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="longitud">Longitud:</label>
        <select v-model="contenedor.longitud" required>
          <option v-for="longit in longitud_options" :value="longit.value" :key="longit.value">
            {{ longit.text }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="codigo_iso">Código ISO</label>
        <input type="text" v-model="contenedor.codigo_iso" required />
      </div>

      <div class="form-buttons">
        <button type="button">
          <router-link style="color:white;text-decoration:none" to="/contenedor">Cancelar</router-link>
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
  color: #000;
  background-color: #fff;
}

select option {
  color: #000;
  background-color: #fff;
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
  name: 'EditarContenedorView',
  data() {
    return {
      contenedor: {
        id_contenedor: '',
        tipo_contenedor: '',
        longitud: '',
        codigo_iso: '',
      },
      contenedores_options: [
        { value: 'DC', text: 'Dry Container' },
        { value: 'RC', text: 'Reefer Container' },
        { value: 'GP', text: 'GP' },
        { value: 'HC', text: 'High Cube' },
        { value: 'OT', text: 'Open Top' },
        { value: 'FR', text: 'Flat Rack' },
        { value: 'RH', text: 'RH' },
        { value: 'OS', text: 'Open Side' },
        { value: 'TC', text: 'Tank Container' },
      ],
      longitud_options: [
        { value: '1-20', text: '1-20' },
        { value: '2-40', text: '2-40' },
      ],
    };
  },

  mounted() {
    this.get_contenedor();
  },

  methods: {
    async get_contenedor() {
      const contenedor_id = this.$route.params.id; // Obtener el ID del contenedor desde la URL
      try {
        const response = await axios.get(`/api/contenedores/${contenedor_id}/`);
        this.contenedor = response.data; // Llenar el formulario con los datos del contenedor
      } catch (error) {
        console.error('Error al obtener el contenedor:', error);
        Swal.fire('Error', 'No se pudo cargar el contenedor.', 'error');
      }
    },

    validateForm() {
      const id_contenedor_regex = /^[A-Z]{4}[0-9]{7}$/;
      const codigo_iso_regex = /^[0-9]{2}[A-Z]{1}[0-9]{1}$/;
      let errorMessage = '';

      if (!id_contenedor_regex.test(this.contenedor.id_contenedor)) {
        errorMessage +=
          'El campo "Id" debe comenzar con cuatro letras mayúsculas seguidas de siete dígitos.<br>';
      }

      if (!codigo_iso_regex.test(this.contenedor.codigo_iso)) {
        errorMessage +=
          'El campo "Código ISO" admite un formato de: 2 números + 1 letra mayúscula + 1 número; ejemplo: 22G1. <br>';
      }

      if (errorMessage) {
        Swal.fire({
          icon: 'error',
          title: 'Error de validación',
          html: errorMessage,
        });
        return false; // Detener el envío del formulario
      }

      return true; // El formulario es válido
    },

    async update_contenedor() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      const contenedor_id = this.$route.params.id; // Obtener el ID del contenedor desde la URL
      try {
        await axios.put(`/api/contenedores/${contenedor_id}/`, this.contenedor); // Usar PUT para actualizar
        Swal.fire('Actualizado!', 'El contenedor ha sido modificado exitosamente.', 'success');
        this.$router.push('/contenedor'); // Redirigir a la lista de contenedores
      } catch (error) {
        console.error('Error al actualizar el contenedor:', error);
        Swal.fire('Error', 'Hubo un error al actualizar el contenedor.', 'error');
      }
    },
  },
};
</script>