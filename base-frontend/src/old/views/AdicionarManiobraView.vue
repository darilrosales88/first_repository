<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container">
      <h3>Adicionar tipo de maniobra portuaria</h3>
      <form @submit.prevent="save_maniobra">
        <!-- Campo Nombre de la Maniobra -->
        <div class="form-row">
        <div class="mb-3">
          <label for="nombre_maniobra" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre_maniobra" v-model="nombre_maniobra" required />
        </div>

        <!-- Campo Tipo de Maniobra -->
        <div class="mb-3">
          <label for="tipo_maniobra" class="form-label">Tipo:<span style="color: red;">*</span></label>
          <select class="form-control" id="tipo_maniobra" v-model="tipo_maniobra" required>
            <option v-for="t_maniobra in t_maniobra_options" :value="t_maniobra.value" :key="t_maniobra.value">
              {{ t_maniobra.text }}
            </option>
          </select>
        </div>
      </div>
        <!-- Botones -->
        <div class="form-buttons">
          <button type="button" @click="confirmCancel" style="color:white;text-decoration:none">Cancelar</button>
          <button type="submit">Aceptar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
body {
  background-color: #F2F2F2;
}

.form-container {
  max-width: 600px; /* Ancho reducido */
  margin: 20px ; /* Centra el formulario */
  padding: 20px;
  margin-left: 220px;
  background-color: rgb(245, 245, 245);
  border-radius: 8px;
 
}

h3 {
  text-align: left;
  margin-bottom: 20px;
  font-size: 18px;
}
.form-label{
  font-size: 14px;
  text-align: left;
}
form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-row {
  display: flex;
  flex-direction: row;
  gap: 15px;
}

.mb-3 {
  width: 200px;
  display: flex;
  flex-direction: column;
}

.form-control {
  padding: 1px 0px; /* Padding reducido */
  height: 25px; /* Altura reducida */
  font-size: 14px; /* Tamaño de fuente reducido */
  border: 1px solid #ccc;
  border-radius: 2px;
}

.form-buttons {
  display: flex;
  justify-content: flex-end;
  font-size: 14px;
}

button {
  margin-left: 10px;
  padding: 6px 15px; /* Padding reducido */
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  font-size: 14px; /* Tamaño de fuente reducido */
}

button[type="button"] {
  background-color: gray;
  color: white;
}

button[type="submit"] {
  background-color: #007bff;
  color: white;
}
</style>


<script>
import axios from 'axios';
import Swal from 'sweetalert2';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  components: {
    NavbarComponent,
  },
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