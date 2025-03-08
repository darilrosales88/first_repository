<template>
    <div class="form-container">
      <h2>Adicionar estado técnico</h2>
      <form @submit.prevent="saveItem">
        <div class="form-group">
          <label for="nombre"> Código:</label>
          <input type="text" v-model="codigo_estado_tecnico" required />
          <p v-if="codigo_estado_tecnico_error" class="help is-danger">{{ codigo_estado_tecnico_error }}</p>
        </div>

        <div class="form-group">
          <label for="nombre"> Nombre:</label>
          <input type="text" v-model="nombre_estado_tecnico" required />
          <p v-if="nombre_estado_tecnico_error" class="help is-danger">{{ nombre_estado_tecnico_error }}</p>
        </div>

        <div class="form-buttons">
          <button type="button"><router-link style="color:white;text-decoration:none" to="/EstadoTecnico">Cancelar</router-link> </button>
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
  data(){
    return{
      nombre_estado_tecnico: '',
      codigo_estado_tecnico: '',
      codigo_estado_tecnico_error : null,
      nombre_estado_tecnico_error : null    
    }
  },

  methods:{
    validateForm() {
            const nombre_estado_tecnico_regex = /^[\w\d\W ]{3,100}$/;
            const codigo_estado_tecnico_regex = /^[A-Za-zÁÉÍÓÚáéíóú]{2,5}$/;
            let valid = true;
            
            if (!codigo_estado_tecnico_regex.test(this.codigo_estado_tecnico)) {
                this.codigo_estado_tecnico_error = 'Este campo acepta letras. Tamaño mínimo 2 caracteres y tamaño máximo 5 caracteres.';
                valid = false;
            } else {
                this.codigo_estado_tecnico_error = null;
            }

            if (!nombre_estado_tecnico_regex.test(this.nombre_estado_tecnico)) {
                this.nombre_estado_tecnico_error = 'Este campo acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y tamaño máximo 100 caracteres.';
                valid = false;
            } else {
                this.nombre_estado_tecnico_error = null;
            }

            return valid;
        },
    async saveItem(){
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
                return; // Si la validación falla, no enviar el formulario
            }
      this.$store.commit('setIsLoading', false);
      const estado_tecnico = {
        nombre_estado_tecnico: this.nombre_estado_tecnico,
        codigo_estado_tecnico: this.codigo_estado_tecnico,
              };
      await axios
                .post('/api/estados/', estado_tecnico)
                .then(response => {
                    
                    this.$router.push('/EstadoTecnico');
                    Swal.fire('Agregado!', 'El estado técnico ha sido insertado exitosamente.', 'success')
                })
                .catch(error => {
                    console.log(error);
                });

      this.$store.commit('setIsLoading', false);
      
      this.$router.push('/EstadoTecnico') 
    }
  }
}
</script>