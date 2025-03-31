<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    <div class="form-container">
      <h3 style="color: #002A68;">Adicionar atraque:</h3>
      <form @submit.prevent="saveAtraque">
        <div class="form-row">
          <div class="mb-3">
            <label for="nombre_atraque" class="form-label">Nombre:<span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="nombre_atraque" v-model="nombre_atraque" required />
          </div>

          <div class="mb-3">
            <label for="puerto" class="form-label">Puerto:<span style="color: red;">*</span></label>
            <select class="form-control" id="puerto" v-model="puerto" required>
              <option v-for="puerto in puertos" :value="puerto.id" :key="puerto.id">
                {{ puerto.nombre_puerto }}
              </option>
            </select>
          </div>

          <div class="mb-3">
            <label for="terminal" class="form-label">Terminal:<span style="color: red;">*</span></label>
            <select class="form-control" id="terminal" v-model="terminal" required>
              <option v-for="terminal in terminales" :value="terminal.id" :key="terminal.id">
                {{ terminal.nombre_terminal }}
              </option>
            </select>
          </div>
        </div>

        <div class="form-buttons">
          <button type="button" @click="confirmCancel" style="color:white;text-decoration:none">Cancelar</button>
          <button type="submit">Adicionar</button>
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
import axios from 'axios';
import Swal from 'sweetalert2';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'AdicionarAtraqueView',
  components: {
    NavbarComponent,
  },
  data() {
    return {
      terminales: [], // Almacena las terminales obtenidas
      puertos: [], // Almacena los puertos obtenidos
      nombre_atraque: '',
      terminal: '',
      puerto: '',
    };
  },

  mounted() {
    this.getTerminales(); // Llama al método para obtener las terminales
    this.getPuertos(); // Llama al método para obtener los puertos
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
      const nombre_atraque_regex = /^[A-Z][A-Za-z ]{2,99}$/;
      let errorMessage = '';

      if (!nombre_atraque_regex.test(this.nombre_atraque)) {
        errorMessage +=
          'El campo "Nombre" debe comenzar con mayúscula, seguir con letras y espacios, y tener entre 3 y 100 caracteres.\n';
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

    async getTerminales() {
      try {
        const response = await axios.get('/api/terminales/');
        this.terminales = response.data;
      } catch (error) {
        console.error('Error al obtener las terminales:', error);
        Swal.fire('Error', 'Hubo un error al obtener las terminales.', 'error');
      }
    },

    async getPuertos() {
      try {
        const response = await axios.get('/api/puertos/');
        this.puertos = response.data;
      } catch (error) {
        console.error('Error al obtener los puertos:', error);
        Swal.fire('Error', 'Hubo un error al obtener los puertos.', 'error');
      }
    },

    async saveAtraque() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      const data = {
        nombre_atraque: this.nombre_atraque,
        terminal: this.terminal,
        puerto: this.puerto,
      };

      try {
        await axios.post('/api/atraques/', data);
        Swal.fire('Agregado!', 'El atraque ha sido añadido exitosamente.', 'success');
        this.$router.push('/Atraques');
      } catch (error) {
        console.log(error);
        Swal.fire('Error', 'Hubo un error al agregar el atraque.', 'error');
      }
    },
  },
};
</script>