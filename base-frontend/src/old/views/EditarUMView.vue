<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container">
      <h3 style="color: #002A68;">Editar unidad de medida: {{ u_medida.unidad_medida }}</h3>
      <form @submit.prevent="submitForm" class="form-grid">
        <!-- Campo Magnitud -->
         
        <div class="mb-3">
          <label for="magnitud" class="form-label">Magnitud:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="magnitud" v-model="u_medida.magnitud" required />
        </div>

        <!-- Campo Unidad de Medida -->
        <div class="mb-3">
          <label for="unidad_medida" class="form-label">Unidad de medida:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="unidad_medida" v-model="u_medida.unidad_medida" required />
        </div>

        <!-- Campo Símbolo -->
        <div class="mb-3">
          <label for="simbolo" class="form-label">Símbolo:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="simbolo" v-model="u_medida.simbolo" required />
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
  max-width: 670px; /* Ancho reducido */
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

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
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
  color: #000; /* Asegura que el texto sea negro */
  background-color: #fff; /* Asegura que el fondo sea blanco */
}

select option {
  color: #000; /* Asegura que el texto de las opciones sea negro */
  background-color: #fff; /* Asegura que el fondo de las opciones sea blanco */
}

.form-buttons {
  grid-column: span 3; /* Los botones ocupan las 2 columnas */
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
  name: 'EditarUMView',
  components: {
    NavbarComponent,
  },
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