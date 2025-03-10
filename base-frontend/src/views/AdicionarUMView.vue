<template>
  <div class="form-container">
    <h2>Adicionar unidad de medida:</h2>
    <form @submit.prevent="saveItem">
      <!-- Campo Magnitud -->
      <div class="form-group">
        <label for="magnitud">Magnitud:<span style="color: red;">*</span></label>
        <input type="text" style="padding: 3px;" v-model="magnitud" required />
      </div>

      <!-- Campo Unidad de Medida -->
      <div class="form-group">
        <label for="unidad_medida">Unidad de medida:<span style="color: red;">*</span></label>
        <input type="text" style="padding: 3px;" v-model="unidad_medida" required />
      </div>

      <!-- Campo Símbolo -->
      <div class="form-group">
        <label for="simbolo">Símbolo:<span style="color: red;">*</span></label>
        <input type="text" style="padding: 3px;" v-model="simbolo" required />
      </div>

      <div class="form-buttons">
        <button type="button" @click="confirmCancel" style="color:white;text-decoration:none">Cancelar</button>
        <button>Aceptar</button>
      </div>
    </form>
  </div>
</template>

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

<script>
import Swal from 'sweetalert2';
import axios from 'axios';

export default {
  data() {
    return {
      magnitud: '',
      unidad_medida: '',
      simbolo: '',
    };
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
      const magnitud_regex = /^[A-Záíóúé\w\s]{1,49}$/;
      const simbolo_regex = /^[\d\w]{1,3}$/;
      let errorMessage = '';

      if (!magnitud_regex.test(this.magnitud)) {
        errorMessage += 'El campo "Magnitud" admite letras y espacios. Tamaño mínimo 2 caracteres y máximo 50 caracteres.\n';
      }

      if (!magnitud_regex.test(this.unidad_medida)) {
        errorMessage += 'El campo "Unidad de medida" admite letras y espacios. Tamaño mínimo 2 caracteres y máximo 50 caracteres.\n';
      }

      if (!simbolo_regex.test(this.simbolo)) {
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
    async saveItem() {
      if (!this.validateForm()) {
        return; // Detener el envío si la validación falla
      }

      this.$store.commit('setIsLoading', true);
      const u_medida = {
        magnitud: this.magnitud,
        unidad_medida: this.unidad_medida,
        simbolo: this.simbolo,
      };

      try {
        await axios.post('/api/unidades_medida/', u_medida);
        this.$router.push('/UM');
        Swal.fire('Agregado!', 'La unidad de medida ha sido insertada exitosamente.', 'success');
      } catch (error) {
        console.error('Error al agregar la unidad de medida:', error);
        Swal.fire('Error', 'Hubo un error al agregar la unidad de medida.', 'error');
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    },
  },
};
</script>