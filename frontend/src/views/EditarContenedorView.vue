<template>
  <div class="form-container">
    <h2>Editar contenedor {{ contenedor.id_contenedor }}</h2>
    <form @submit.prevent="submitForm" class="form-grid">
      <!-- Campo ID (solo lectura) -->
      <div class="form-group" >
        <label for="id_contenedor">Id:<span style="color: red;">*</span></label>
        <input type="text" style="padding: 3px;" v-model="contenedor.id_contenedor" disabled />
      </div>

      <!-- Campo Tipo de Contenedor -->
      <div class="form-group">
        <label for="tipo_contenedor">Tipo de contenedor:<span style="color: red;">*</span></label>
        <select v-model="contenedor.tipo_contenedor" required>
          <option v-for="t_contenedor in contenedores_options" :value="t_contenedor.value" :key="t_contenedor.value">
            {{ t_contenedor.text }}
          </option>
        </select>
      </div>

      <!-- Campo Longitud -->
      <div class="form-group">
        <label for="longitud">Longitud:<span style="color: red;">*</span></label>
        <select v-model="contenedor.longitud" required>
          <option v-for="longit in longitud_options" :value="longit.value" :key="longit.value">
            {{ longit.text }}
          </option>
        </select>
      </div>

      <!-- Campo Código ISO -->
      <div class="form-group">
        <label for="codigo_iso">Código ISO:<span style="color: red;">*</span></label>
        <input type="text" style="padding: 3px;" v-model="contenedor.codigo_iso" required />
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
      const id_contenedor_regex = /^[A-Z]{4}[0-9]{7}$/;
      const codigo_iso_regex = /^[0-9]{2}[A-Z]{1}[0-9]{1}$/;
      let errorMessage = '';

      if (!id_contenedor_regex.test(this.contenedor.id_contenedor)) {
        errorMessage +=
          'El campo "Id" debe comenzar con cuatro letras mayúsculas seguidas de siete dígitos.\n';
      }

      if (!codigo_iso_regex.test(this.contenedor.codigo_iso)) {
        errorMessage +=
          'El campo "Código ISO" debe comenzar con dos números, seguidos de una letra mayúscula y un número.\n';
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

    async get_contenedor() {
      this.$store.commit('setIsLoading', true);
      const contenedor_id = this.$route.params.id;
      try {
        const response = await axios.get(`/api/contenedores/${contenedor_id}/`);
        this.contenedor = response.data;
      } catch (error) {
        console.error('Error al obtener el contenedor:', error);
        Swal.fire('Error', 'No se pudo cargar el contenedor.', 'error');
      }
      this.$store.commit('setIsLoading', false);
    },

    async submitForm() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      this.$store.commit('setIsLoading', true);
      const contenedor_id = this.$route.params.id;

      try {
        // Envía solo los campos editables
        const data = {
          tipo_contenedor: this.contenedor.tipo_contenedor,
          longitud: this.contenedor.longitud,
          codigo_iso: this.contenedor.codigo_iso,
        };

        await axios.patch(`/api/contenedores/${contenedor_id}/`, data);
        Swal.fire('Actualizado!', 'El contenedor ha sido modificado exitosamente.', 'success');
        this.$router.push('/contenedor');
      } catch (error) {
        console.error('Error al actualizar el contenedor:', error);
        Swal.fire('Error', 'Hubo un error al actualizar el contenedor.', 'error');
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    },
  },
};
</script>