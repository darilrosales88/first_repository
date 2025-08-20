<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container">
      <h3>Adicionar contenedor</h3>
      <form @submit.prevent="save_contenedor" class="form-grid">
        <!-- Campo Id del Contenedor -->
        
        <div class="mb-3">
          <label for="id_contenedor" class="form-label">Id:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="id_contenedor" v-model="id_contenedor" required />
        </div>

        <!-- Campo Tipo de Contenedor -->
        <div class="mb-3">
          <label for="tipo_contenedor" class="form-label">Tipo de contenedor:<span style="color: red;">*</span></label>
          <select class="form-control" id="tipo_contenedor" v-model="tipo_contenedor" required>
            <option v-for="t_contenedor in contenedores_options" :value="t_contenedor.value" :key="t_contenedor.value">
              {{ t_contenedor.text }}
            </option>
          </select>
        </div>

        <!-- Campo Longitud -->
        <div class="mb-3">
          <label for="longitud" class="form-label">Longitud:<span style="color: red;">*</span></label>
          <select class="form-control" id="longitud" v-model="longitud" required>
            <option v-for="longit in longitud_options" :value="longit.value" :key="longit.value">
              {{ longit.text }}
            </option>
          </select>
        </div>

        <!-- Campo Código ISO -->
        <div class="mb-3">
          <label for="codigo_iso" class="form-label">Código ISO:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="codigo_iso" v-model="codigo_iso" required />
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
  max-width: 680px; /* Ajusta el ancho máximo del contenedor */
  margin: 20px; /* Centra el formulario */
  padding: 20px;
  margin-left: 220px;
  border-radius: 8px;
  background-color: rgb(245, 245, 245);
}

h3 {
  text-align: left;
  margin-bottom: 20px;
  font-size: 18px;
}

.form-label {
  font-size: 14px;
  text-align: left;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 2 columnas de igual tamaño */
  gap: 15px; /* Espacio entre los elementos */
}

.mb-3 {
  width: 200px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-control {
  padding: 1px 0px; /* Padding reducido */
  height: 25px; /* Altura reducida */
  font-size: 14px; /* Tamaño de fuente reducido */
  border: 1px solid #ccc;
  border-radius: 2px;
}

.form-buttons {
  grid-column: span 3; /* Los botones ocupan las 2 columnas */
  display: flex;
  justify-content: flex-end;
  font-size: 14px;
  margin-top: 20px;
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
  name: 'CrearContenedorView',
  components: {
    NavbarComponent,
  },
  data() {
    return {
      id_contenedor: '',
      id_contenedor_error: null,
      tipo_contenedor: '',
      longitud: '',
      codigo_iso: '',
      codigo_iso_error: null,
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

      if (!id_contenedor_regex.test(this.id_contenedor)) {
        errorMessage +=
          'El campo "Id" debe comenzar con cuatro letras mayúsculas seguidas de siete dígitos.\n';
      }

      if (!codigo_iso_regex.test(this.codigo_iso)) {
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

    async save_contenedor() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      const data = {
        id_contenedor: this.id_contenedor,
        tipo_contenedor: this.tipo_contenedor,
        longitud: this.longitud,
        codigo_iso: this.codigo_iso,
      };

      try {
        await axios.post('/api/contenedores/', data);
        Swal.fire('Agregado!', 'El contenedor ha sido añadido exitosamente.', 'success');
        this.$router.push('/contenedor');
      } catch (error) {
        console.log(error);
        Swal.fire('Error', 'Hubo un error al agregar el contenedor.', 'error');
      }
    },
  },
};
</script>