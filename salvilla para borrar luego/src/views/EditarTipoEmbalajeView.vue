<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container">
      <h3 style="color: #002A68;">Editar tipo de embalaje <strong>{{ embalaje.nombre_tipo_embalaje }}</strong></h3>
      <form @submit.prevent="submitForm" class="form-grid">
        <!-- Campo Nombre -->
        <div class="mb-3">
          <label for="nombre" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre" v-model="embalaje.nombre_tipo_embalaje" required />
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
  margin: 20px; /* Centra el formulario */
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

.form-label {
  font-size: 14px;
  text-align: left;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 3 columnas de igual tamaño */
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
  color: #000; /* Asegura que el texto sea negro */
  background-color: #fff; /* Asegura que el fondo sea blanco */
}

select option {
  color: #000; /* Asegura que el texto de las opciones sea negro */
  background-color: #fff; /* Asegura que el fondo de las opciones sea blanco */
}

.form-buttons {
  grid-column: span 3; /* Los botones ocupan las 3 columnas */
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
  name: 'EditarTipoEmbalajeView',
  components: {
    NavbarComponent,
  },
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