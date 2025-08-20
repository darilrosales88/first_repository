<template>
  <div>
    <div style="background-color: #002a68; color: white; text-align: right">
      <h6>Bienvenido:</h6>
    </div>
    <br />
    <Navbar-Component />
    <div class="form-container" style="margin-left: 18em; width: 75%">
      <h3 style="color: #002a68">Adicionar Cargo</h3>
      <form @submit.prevent="saveItem">
        <div class="form-row">
          <div class="mb-3">
            <label for="nombre" class="form-label"
              >Nombre:<span style="color: red">*</span></label
            >
            <input
              type="text"
              class="form-control"
              id="nombre"
              v-model="nombre_cargo"
              required
            />
          </div>
        </div>

        <div class="form-buttons">
          <button
            type="button"
            @click="confirmCancel"
            style="color: white; text-decoration: none"
          >
            Cancelar
          </button>
          <button type="submit">Aceptar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
body {
  background-color: #f2f2f2;
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
import Swal from 'sweetalert2'
import axios from 'axios';
import NavbarComponent from '@/components/NavbarComponent.vue';
export default {
name: 'AdicionarCargoView',
components: {
    NavbarComponent,
  },
data(){
  return{
    nombre_cargo: '',
    nombre_cargo_error : null    
  }
},

methods:{
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
    // Expresión regular para el tipo de cargo
    const nombre_cargoRegex = /^[A-Z][\w\sáéíóú]{1,19}$/;
    let valid = true;

    // Validar el nombre del cargo
    if (!nombre_cargoRegex.test(this.nombre_cargo)) {
      this.nombre_cargo_error = 'Este campo comienza con mayúscula, acepta letras minúsculas y espacios. Tamaño mínimo 2 caracteres y tamaño máximo 20 caracteres.';
      valid = false;
    } else {
      this.nombre_cargo_error = null;
    }

    return valid;
  },
  async saveItem(){
    // Validar el formulario antes de enviarlo
    if (!this.validateForm()) {
      Swal.fire({
        icon: 'error',
        title: 'Error de validación en el campo nombre',
        text: this.nombre_cargo_error,
      });
      return; // Si la validación falla, no enviar el formulario
    }

    this.$store.commit('setIsLoading', true);
    const cargo = {
      nombre_cargo: this.nombre_cargo,
    };

    try {
      const response = await axios.post("/api/cargos/", cargo);
      this.$router.push('/Cargos');
      Swal.fire('Agregado!', 'El Cargo ha sido insertado exitosamente.', 'success');
    } catch (error) {
      console.log(error);
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Hubo un problema al intentar agregar el cargo. Por favor, inténtalo de nuevo.',
      });
    } finally {
      this.$store.commit('setIsLoading', false);
    }
  }
}
}
</script>