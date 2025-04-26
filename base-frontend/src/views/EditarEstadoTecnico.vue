<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container">
      <h3 style="color: #002A68;">Editar estado técnico {{ estado_tecnico.nombre_estado_tecnico }}</h3>
      <form @submit.prevent="submitForm" class="form-grid">
        <!-- Campo Código -->
        <div class="mb-3">
          <label for="código" class="form-label">Código:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="código" v-model="estado_tecnico.codigo_estado_tecnico" required />
          <p v-if="codigo_estado_tecnico_error" class="help is-danger">{{ codigo_estado_tecnico_error }}</p>
        </div>

        <!-- Campo Nombre -->
        <div class="mb-3">
          <label for="nombre" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre" v-model="estado_tecnico.nombre_estado_tecnico" required />
          <p v-if="nombre_estado_tecnico_error" class="help is-danger">{{ nombre_estado_tecnico_error }}</p>
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

.help.is-danger {
  color: red;
  font-size: 12px;
  margin-top: 5px;
}
</style>

  <script>
  import axios from 'axios';
  import Swal from 'sweetalert2'
  import NavbarComponent from '@/components/NavbarComponent.vue';

  export default {
          name: 'EditarEstadoTecnico',
          components: {
    NavbarComponent,
  },

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
