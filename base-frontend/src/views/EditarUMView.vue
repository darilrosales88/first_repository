<template>
  <div class="form-container">
    <h2>Editar unidad de medida {{ u_medida.unidad_medida }}</h2>
    <form @submit.prevent="submitForm">
      <!-- Campo Magnitud -->
      <div class="form-group">
        <label for="magnitud">Magnitud:</label>
        <input type="text" v-model="u_medida.magnitud" required />
      </div>

      <!-- Campo Unidad de Medida -->
      <div class="form-group">
        <label for="unidad_medida">Unidad de medida:</label>
        <input type="text" v-model="u_medida.unidad_medida" required />
      </div>

      <!-- Campo Símbolo -->
      <div class="form-group">
        <label for="simbolo">Símbolo:</label>
        <input type="text" v-model="u_medida.simbolo" required />
      </div>

      <!-- Botones -->
      <div class="form-buttons">
        <button type="button">
          <router-link style="color: white; text-decoration: none" to="/UM">Cancelar</router-link>
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
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
  name: 'EditarUMView',

  data() {
    return {
      u_medida: {
        magnitud: '',
        unidad_medida: '',
        simbolo: '',
      },
    };
  },

  mounted() {
    this.get_unidad_medida();
  },

  methods: {
    validateForm() {
      const magnitud_u_m_regex = /^[A-Za-záíóúé][A-Za-záíóúé\s]{1,49}$/;
      const simbolo_regex = /^[\d\w]{1,3}$/;
      let errorMessage = '';

      if (!magnitud_u_m_regex.test(this.u_medida.magnitud)) {
        errorMessage += 'El campo "Magnitud" admite letras y espacios. Tamaño mínimo 2 caracteres y máximo 50 caracteres.\n';
      }

      if (!magnitud_u_m_regex.test(this.u_medida.unidad_medida)) {
        errorMessage += 'El campo "Unidad de medida" admite letras y espacios. Tamaño mínimo 2 caracteres y máximo 50 caracteres.\n';
      }

      if (!simbolo_regex.test(this.u_medida.simbolo)) {
        errorMessage += 'El campo "Símbolo" admite caracteres alfanuméricos. Tamaño mínimo 1 y máximo 3 caracteres.\n';
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

    async get_unidad_medida() {
      this.$store.commit('setIsLoading', true);
      const unidad_medida_id = this.$route.params.id;

      try {
        const response = await axios.get(`/api/unidades_medida/${unidad_medida_id}/`);
        this.u_medida = response.data;
      } catch (error) {
        console.error('Error al obtener la unidad de medida:', error);
        Swal.fire('Error', 'No se pudo cargar la unidad de medida.', 'error');
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    },

    async submitForm() {
      if (!this.validateForm()) {
        return; // Detener el envío si la validación falla
      }

      this.$store.commit('setIsLoading', true);
      const unidad_medida_id = this.$route.params.id;

      try {
        await axios.patch(`/api/unidades_medida/${unidad_medida_id}/`, this.u_medida);
        this.$router.push('/UM');
        Swal.fire('Actualizado!', 'La unidad de medida ha sido modificada exitosamente.', 'success');
      } catch (error) {
        console.error('Error al actualizar la unidad de medida:', error);
        Swal.fire('Error', 'Hubo un error al actualizar la unidad de medida.', 'error');
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    },
  },
};
</script>