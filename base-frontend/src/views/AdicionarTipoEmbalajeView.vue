<template>
  <div>
    <Navbar-Component />
    
    <div class="form-container">
      <h2>Adicionar tipo de embalaje</h2>
      <form @submit.prevent="saveItem">
        <!-- Campo Nombre del Tipo de Embalaje -->
        <div class="mb-3">
          <label for="nombre_tipo_embalaje" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre_tipo_embalaje" v-model="nombre_tipo_embalaje" required />
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
  max-width: 450px; /* Ajusta el ancho máximo del contenedor */
  margin: 20px; /* Centra el formulario */
  padding: 20px;
  margin-left: 220px;
  
  border-radius: 8px;
  background-color: rgb(245, 245, 245);
}

h2 {
  text-align: left;
  margin-bottom: 20px;
  font-size: 18px;
}

.form-label {
  font-size: 14px;
  text-align: left;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
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
  color: #000; /* Asegura que el texto sea negro */
  background-color: #fff; /* Asegura que el fondo sea blanco */
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
import Swal from 'sweetalert2';
import axios from 'axios';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  components: {
    NavbarComponent,
  },
  data() {
    return {
      nombre_tipo_embalaje: '',
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
      // Expresión regular para el nombre del tipo de embalaje
      const nombre_tipo_embalaje_regex = /^[A-Z][\w\s]{1,99}$/;

      // Validar el nombre del tipo de embalaje
      if (!nombre_tipo_embalaje_regex.test(this.nombre_tipo_embalaje)) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'El nombre debe comenzar con mayúscula, aceptar letras minúsculas y espacios. Tamaño mínimo 2 caracteres y máximo 100 caracteres.',
        });
        return false;
      }

      return true;
    },

    async saveItem() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      this.$store.commit('setIsLoading', true);

      const embalaje = {
        nombre_tipo_embalaje: this.nombre_tipo_embalaje,
      };

      try {
        await axios.post('/api/embalajes/', embalaje);
        this.$router.push('/TipoEmbalaje');
        Swal.fire('Agregado!', 'El tipo de embalaje ha sido insertado exitosamente.', 'success');
      } catch (error) {
        console.error(error);
        Swal.fire('Error', 'Hubo un error al agregar el tipo de embalaje.', 'error');
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    },
  },
};
</script>
