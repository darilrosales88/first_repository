<template>
  <div class="form-container">
    <h2>Crear Provincia:</h2>
    <form @submit.prevent="createProvincia">
      <div class="form-group">
        <label for="codigo">Código:<span style="color: red;">*</span></label>
        <input style="padding: 3px;" type="text" v-model="codigo" required />
      </div>
      <div class="form-group">
        <label for="nombre">Nombre de la Provincia:<span style="color: red;">*</span></label>
        <input style="padding: 3px;" type="text" v-model="nombre_provincia" required />
      </div>
      <div class="form-group">
        <label for="pais">País:<span style="color: red;">*</span></label>
        <select style="padding: 5px;" id="pais" v-model="pais" required>
          <option value="">-Seleccione-</option>
          <option v-for="item in paisOptions" :key="item.id" :value="item.id">{{ item.nombre_pais }}</option>
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
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
  name: 'CrearProvinciaView',

  data() {
    return {
      codigo: '',
      codigo_error: null,
      pais: '',
      paisOptions: [],
      nombre_provincia: '',
      nombre_provincia_error: null,
    };
  },

  mounted() {
    this.getPaises(); // Obtener la lista de países
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
      const codigo_regex = /^[0-9]{2}$/;
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
        this.paisOptions = response.data;
      } catch (error) {
        console.error('Error al obtener los países:', error);
      }
    },

    // Crear la provincia
    async createProvincia() {
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      const data = {
        nombre_provincia: this.nombre_provincia,
        pais: this.pais,
        codigo: this.codigo,
      };

      try {
        await axios.post('/api/provincias/', data);
        Swal.fire('Creado!', 'La provincia ha sido creada exitosamente.', 'success');
        this.$router.push('/Provincia');
      } catch (error) {
        console.log(error);
        Swal.fire('Error', 'Hubo un error al crear la provincia.', 'error');
      }
    },
  },
};
</script>
