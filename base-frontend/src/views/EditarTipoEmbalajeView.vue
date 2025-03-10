<template>
  <div class="form-container">
    <h2>Editar tipo de embalaje <strong> {{ embalaje.nombre_tipo_embalaje }} </strong></h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="nombre"> Nombre:</label>
        <input type="text" style="padding: 3px;" v-model="embalaje.nombre_tipo_embalaje" required />
      </div>
      <div class="form-buttons">
        <button type="button" @click="confirmCancel" style="color:white;text-decoration:none">Cancelar</button>
        <button>Aceptar</button>
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
  font-size: 14px;
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
  name: 'EditarTipoEmbalajeView',

  data() {
    return {
      embalaje: {},
    };
  },

  mounted() {
    this.get_embalaje();
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
    // Obtener el tipo de embalaje por su ID
    async get_embalaje() {
      this.$store.commit('setIsLoading', true);
      const embalaje_id = this.$route.params.id;

      try {
        const response = await axios.get(`/api/embalajes/${embalaje_id}/`);
        this.embalaje = response.data;
      } catch (error) {
        console.error(error);
        Swal.fire('Error', 'No se pudo cargar el tipo de embalaje.', 'error');
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    },

    // Validar el formulario
    validateForm() {
      const nombre_tipo_embalaje_regex = /^[A-Z][\w\s]{1,99}$/;

      if (!nombre_tipo_embalaje_regex.test(this.embalaje.nombre_tipo_embalaje)) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'El nombre debe comenzar con mayúscula, aceptar letras minúsculas y espacios. Tamaño mínimo 2 caracteres y máximo 100 caracteres.',
        });
        return false;
      }

      return true;
    },

    // Enviar el formulario
    async submitForm() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      this.$store.commit('setIsLoading', true);
      const embalaje_id = this.$route.params.id;

      try {
        await axios.patch(`/api/embalajes/${embalaje_id}/`, this.embalaje);
        this.$router.push('/TipoEmbalaje');
        Swal.fire('Actualizado!', 'El tipo de embalaje ha sido modificado exitosamente.', 'success');
      } catch (error) {
        console.error(error);
        Swal.fire('Error', 'Hubo un error al actualizar el tipo de embalaje.', 'error');
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    },
  },
};
</script>