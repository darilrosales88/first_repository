<template>
  <div>
    <div style="background-color: #002a68; color: white; text-align: right">
      <h6>Bienvenido:</h6>
    </div>
    <br />
    <Navbar-Component />
    <div class="form-container" style="margin-left: 18em; width: 75%">
      <h3 style="color: #002a68">Adicionar estado técnico</h3>
      <form @submit.prevent="saveItem">
        <div class="form-row">
          <div class="mb-3">
            <label for="codigo_estado_tecnico" class="form-label"
              >Código:<span style="color: red">*</span></label
            >
            <input
              type="text"
              class="form-control"
              id="codigo_estado_tecnico"
              v-model="codigo_estado_tecnico"
              required
            />
            <p 
              v-if="codigo_estado_tecnico_error" 
              class="help is-danger"
            >
              {{ codigo_estado_tecnico_error }}
            </p>
          </div>

          <div class="mb-3">
            <label for="nombre_estado_tecnico" class="form-label"
              >Nombre:<span style="color: red">*</span></label
            >
            <input
              type="text"
              class="form-control"
              id="nombre_estado_tecnico"
              v-model="nombre_estado_tecnico"
              required
            />
            <p 
              v-if="nombre_estado_tecnico_error" 
              class="help is-danger"
            >
              {{ nombre_estado_tecnico_error }}
            </p>
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
  max-width: 600px;
  margin: 20px;
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
  padding: 1px 0px;
  height: 25px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 2px;
}

.help.is-danger {
  color: #ff3860;
  font-size: 12px;
  margin-top: 4px;
}

.form-buttons {
  display: flex;
  justify-content: flex-end;
  font-size: 14px;
}

button {
  margin-left: 10px;
  padding: 6px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  font-size: 14px;
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
  components: {
    NavbarComponent,
  },
  data(){
    return{
      nombre_estado_tecnico: '',
      codigo_estado_tecnico: '',
      codigo_estado_tecnico_error : null,
      nombre_estado_tecnico_error : null    
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