<template>
  <div class="form-container">
    <h2>Adicionar OSDE/OACE u Organismo</h2>
    <form @submit.prevent="save_osde_oace_organismo">
      <div class="form-group">
        <label for="nombre">Nombre</label>
        <input type="text" v-model="nombre" required />
      </div>

      <div class="form-group">
        <label for="abreviatura">Abreviatura</label>
        <input type="text" v-model="abreviatura" required />
      </div>

      <div class="form-group">
        <label for="codigo_reeup">Código REEUP</label>
        <input type="number" v-model="codigo_reeup" />
      </div>

      <div class="form-buttons">
        <button type="button">
          <router-link style="color:white;text-decoration:none" to="/Organismos">Cancelar</router-link>
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
  name: 'AdicionarOrganismoView',
  data() {
    return {
      nombre: '',
      abreviatura: '',
      codigo_reeup: null,
    };
  },
  methods: {
    validateForm() {
      const nombre_regex = /^[A-Z][\w\d\W]{2,99}$/;
      const abreviatura_regex = /^[A-ZÁÉÍÓÚ]{1}[A-Za-zÁÉÍÓÚáéíóú\s]{2,19}$/;
      const codigo_reeup_regex = /^[0-9]{5,11}$/;

      if (!nombre_regex.test(this.nombre)) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'El nombre debe comenzar con mayúscula, aceptar letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y máximo 100 caracteres.',
        });
        return false;
      }

      if (!abreviatura_regex.test(this.abreviatura)) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'La abreviatura debe comenzar con mayúscula seguido de espacio o caracteres alfabéticos. Tamaño mínimo 3 caracteres y máximo 20 caracteres.',
        });
        return false;
      }

      if (this.codigo_reeup && !codigo_reeup_regex.test(this.codigo_reeup)) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'El código REEUP sólo admite números. Tamaño mínimo 5 caracteres y máximo 11 caracteres.',
        });
        return false;
      }

      return true;
    },
    async save_osde_oace_organismo() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      const data = {
        nombre: this.nombre,
        abreviatura: this.abreviatura,
        codigo_reeup: this.codigo_reeup,
      };

      try {
        await axios.post('/api/osde/', data);
        Swal.fire('Agregado!', 'El OSDE/OACE u Organismo ha sido añadido exitosamente.', 'success');
        this.$router.push('/Organismos');
      } catch (error) {
        console.log(error);
        Swal.fire('Error', 'Hubo un error al agregar el OSDE/OACE u Organismo.', 'error');
      }
    },
  },
};
</script>