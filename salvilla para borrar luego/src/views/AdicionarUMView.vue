<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container" style="margin-left: 18em; width: 75%">
      <h3>Adicionar unidad de medida</h3>
      <form @submit.prevent="saveItem">
        <!-- Campo Magnitud -->
        <div class="form-row">
        <div class="mb-3">
          <label for="magnitud" class="form-label">Magnitud:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="magnitud" v-model="magnitud" required />
        </div>

        <!-- Campo Unidad de Medida -->
        <div class="mb-3">
          <label for="unidad_medida" class="form-label">Unidad de medida:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="unidad_medida" v-model="unidad_medida" required />
        </div>

        <!-- Campo Símbolo -->
        <div class="mb-3">
          <label for="simbolo" class="form-label">Símbolo:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="simbolo" v-model="simbolo" required />
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
import Swal from 'sweetalert2';
import axios from 'axios';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  components: {
    NavbarComponent,
  },
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