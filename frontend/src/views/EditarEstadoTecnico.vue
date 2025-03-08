<template>
  <div class="form-container">
  <h2>Editar estado técnico {{ estado_tecnico.nombre_estado_tecnico }}</h2>
  <form @submit.prevent="submitForm">

  <div class="form-group">
  <label for="código"> Código:</label>
  <input type="text" v-model="estado_tecnico.codigo_estado_tecnico" required />
  <p v-if="codigo_estado_tecnico_error" class="help is-danger">{{ codigo_estado_tecnico_error }}</p>
  </div>
  
  <div class="form-group">
  <label for="nombre"> Nombre:</label>
  <input type="text" v-model="estado_tecnico.nombre_estado_tecnico" required />
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
  import axios from 'axios';
  import Swal from 'sweetalert2'
  export default {
          name: 'EditarEstadoTecnico',

          data(){
          return{      
          estado_tecnico: {}, 
          codigo_estado_tecnico: '',
          nombre_estado_tecnico: '',          
          codigo_estado_tecnico_error: null,
          nombre_estado_tecnico_error: null,    

          }
          },
          mounted() {
          this.get_estado_tecnico()
          },
          methods:{
            validateForm() {
              const nombre_estado_tecnico_regex = /^[\w\d\W ]{3,100}$/;
              const codigo_estado_tecnico_regex = /^[A-Za-zÁÉÍÓÚáéíóú]{2,5}$/;
              let valid = true;
              
              if (!codigo_estado_tecnico_regex.test(this.estado_tecnico.codigo_estado_tecnico)) {
                  this.codigo_estado_tecnico_error = 'Este campo acepta letras. Tamaño mínimo 2 caracteres y tamaño máximo 5 caracteres.';
                  valid = false;
              } else {
                  this.codigo_estado_tecnico_error = null;
              }

              if (!nombre_estado_tecnico_regex.test(this.estado_tecnico.nombre_estado_tecnico)) {
                  this.nombre_estado_tecnico_error = 'Este campo acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y tamaño máximo 100 caracteres.';
                  valid = false;
              } else {
                  this.nombre_estado_tecnico_error = null;
              }

              return valid;
          },
          async get_estado_tecnico(){
          this.$store.commit('setIsLoading', true)
                  /* creamos una const para guardar el id seleccionado */
                  const estado_tecnico_id = this.$route.params.id /*ese id es el que se declaro en el path para estado_tecnico en la ruta /router/index.vue*/
                  console.log('estadoooooooooooo: ',estado_tecnico_id)
                  /*ahora llamamos a axios */
                  axios
                  /*con la comilla invertida y el nombre de la variable entre llaves y el simbolo $ se conforma una cadena para formar el path
                  que da solucion a la seleccion del usuario*/
                      .get(`/api/estados/${estado_tecnico_id}/`)                    
                      .then(response => {                                
                          this.estado_tecnico = response.data                        
                      })

                      .catch(error =>{
                          console.log(error)
                      })

                  this.$store.commit('setIsLoading', false)
                  
          },

                  /*funcion para enviar los datos al servidor */
                  async submitForm() {
      if (!this.validateForm()) {
        return;
      }

      this.$store.commit('setIsLoading', true);
      const estado_tecnico_id = this.$route.params.id;

      if (!estado_tecnico_id) {
        console.error('ID no proporcionado');
        return;
      }

      try {
        await axios.patch(`/api/estados/${estado_tecnico_id}/`, this.estado_tecnico);
        this.$router.push('/EstadoTecnico');
        Swal.fire('Actualizado!', 'El estado técnico ha sido modificado exitosamente.', 'success');
      } catch (error) {
        console.error('Error al actualizar el estado técnico:', error);
        Swal.fire('Error', 'Hubo un error al actualizar el estado técnico.', 'error');
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    }    
  }
}
  </script>
