<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container" style="margin-left: 18em; width: 75%">
      <h3>Adicionar territorio</h3>
      <form @submit.prevent="saveItem">
        <!-- Campo Nombre del Territorio -->
        <div class="form-row">
        <div class="mb-3">
          <label for="nombre_territorio" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre_territorio" v-model="nombre_territorio" required />
        </div>

        <!-- Campo Abreviatura -->
        <div class="mb-3">
          <label for="abreviatura" class="form-label">Abreviatura:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="abreviatura" v-model="abreviatura" required />
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
      nombre_territorio: '',
      abreviatura: '',
      errores:''
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
      const nombre_territorio_regex = /^[A-Z][\w\d\W]{2,99}$/;
      const abreviatura_regex = /^[\d\w\W\s]{3,20}$/;
      let valid = true;
      this.errores='';

      if (!nombre_territorio_regex.test(this.nombre_territorio)) {
        this.errores += 'El campo Nombre comienza con mayúscula, acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y tamaño máximo 100 caracteres.<br>';
        valid = false;
      }

      if (!abreviatura_regex.test(this.abreviatura)) {
        this.errores += 'El campo Abreviatura acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y tamaño máximo 20 caracteres.<br>';
        valid = false;
      }
      

      return valid;
    },

    async saveItem() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        Swal.fire('Errores en la entrada de datos', this.errores, 'error');
        
        return; // Si la validación falla, no enviar el formulario
      }
      
      this.$store.commit('setIsLoading', true);

      const territorio = {
        nombre_territorio: this.nombre_territorio,
        abreviatura: this.abreviatura
      };

      try {
        await axios.post('/api/territorios/', territorio);
        this.$router.push('/Territorio');
        Swal.fire('Agregado!', 'El territorio ha sido insertado exitosamente.', 'success');
      } catch (error) {
        console.error('Error al insertar el territorio:', error);
        Swal.fire('Error', 'Hubo un error al insertar el territorio.', 'error');
      }

      this.$store.commit('setIsLoading', false);
    }
  }
};
</script>