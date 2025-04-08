<template>
  <div class="form-container">
    <h2>Adicionar Cargo</h2>
    <form @submit.prevent="saveItem">
      <div class="form-group">
        <label for="nombre"> Nombre:</label>
        <input type="text" v-model="nombre_cargo" required />        
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
max-width: 450px;
margin: 50px;
padding: 20px;
background-color: #f9f9f9;
border-radius: 8px;
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
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

input,select {
flex: 2;
padding: 8px;
border: 1px solid #ccc;
border-radius: 4px;
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
import Swal from 'sweetalert2'
import axios from 'axios';

export default {
name: 'AdicionarCargoView',
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