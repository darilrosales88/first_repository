<template>
  <div class="form-container">
    <h2>Adicionar tipo de maniobra portuaria</h2>
    <form @submit.prevent="save_maniobra">
      <!-- Campo Nombre de la Maniobra -->
      <div class="form-group">
        <label for="nombre_maniobra">Nombre</label>
        <input type="text" v-model="nombre_maniobra" required />
      </div>

      <!-- Campo Tipo de Maniobra -->
      <div class="form-group">
        <label for="tipo_maniobra">Tipo:</label>
        <select v-model="tipo_maniobra" required>
          <option v-for="t_maniobra in t_maniobra_options" :value="t_maniobra.value" :key="t_maniobra.value">
            {{ t_maniobra.text }}
          </option>
        </select>
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
  color: #000; /* Asegura que el texto sea negro */
  background-color: #fff; /* Asegura que el fondo sea blanco */
}

select option {
  color: #000; /* Asegura que el texto de las opciones sea negro */
  background-color: #fff; /* Asegura que el fondo de las opciones sea blanco */
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
  name: 'AdicionarManiobraView',
  data() {
    return {
      nombre_maniobra: '',
      tipo_maniobra: '',
      t_maniobra_options: [
        { value: 'entrada', text: 'Maniobra de entrada' },
        { value: 'salida', text: 'Maniobra de salida' },
      ],
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
      const nombre_maniobra_regex = /^[A-Z][\w\s]{1,99}$/;

      if (!nombre_maniobra_regex.test(this.nombre_maniobra)) {
        Swal.fire({
          icon: 'error',
          title: 'Error de validación',
          text: 'El campo "Nombre" debe comenzar con mayúscula, seguido de letras y espacios. No puede exceder los 100 caracteres.',
        });
        return false; // Detener el envío del formulario
      }

      return true; // El formulario es válido
    },
    async save_maniobra() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      const data = {
        nombre_maniobra: this.nombre_maniobra,
        tipo_maniobra: this.tipo_maniobra,
      };

      try {
        await axios.post('/api/tipo_maniobras/', data);
        Swal.fire('Agregado!', 'El tipo de maniobra portuaria ha sido añadido exitosamente.', 'success');
        this.$router.push('/TipoManiobra');
      } catch (error) {
        console.error('Error al agregar el tipo de maniobra:', error);
        Swal.fire('Error', 'Hubo un error al agregar el tipo de maniobra portuaria.', 'error');
      }
    },
  },
};
</script>