<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container">
      <h3>Adicionar Puerto</h3>
      <form @submit.prevent="saveItem" class="form-grid">
        <!-- Campo Nombre del Puerto -->
       
        <div class="mb-3">
          <label for="nombre_puerto" class="form-label">Nombre del Puerto:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre_puerto" v-model="nombre_puerto" required />
        </div>

        <!-- Campo País -->
        <div class="mb-3">
          <label for="pais" class="form-label">País:<span style="color: red;">*</span></label>
          <select class="form-control" id="pais" v-model="pais" required>
            <option v-for="item in paisOptions" :key="item.id" :value="item.id">{{ item.nombre_pais }}</option>
          </select>
        </div>

        <!-- Campo Provincia -->
        <div class="mb-3">
          <label for="provincia" class="form-label">Provincia:</label>
          <select class="form-control" id="provincia" v-model="provincia">
            <option v-for="item in provinciaOptions" :key="item.id" :value="item.id">{{ item.nombre_provincia }}</option>
          </select>
        </div>

        <!-- Campo Servicio Portuario -->
        <div class="mb-3">
          <label for="servicio_portuario" class="form-label">Servicio Portuario:</label>
          <select class="form-control" id="servicio_portuario" v-model="servicio_portuario">
            <option v-for="item in servicioPortuarioOptions" :key="item.id" :value="item.id">{{ item.nombre_territorio }}</option>
          </select>
        </div>

        <!-- Campo Latitud -->
        <div class="mb-3">
          <label for="latitud" class="form-label">Latitud:</label>
          <input type="text" class="form-control" id="latitud" v-model="latitud" required />
        </div>

        <!-- Campo Longitud -->
        <div class="mb-3">
          <label for="longitud" class="form-label">Longitud:</label>
          <input type="text" class="form-control" id="longitud" v-model="longitud" required />
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
.form-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 2 columnas de igual tamaño */
  gap: 15px; /* Espacio entre los elementos */
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
  grid-column: span 3; /* Los botones ocupan las 2 columnas */
  display: flex;
  justify-content: flex-end;
  font-size: 14px;
  margin-top: 20px;
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
      nombre_puerto: '',
      pais: '',
      provincia: '',
      servicio_portuario: '',
      latitud: '',
      longitud: '',
      paisOptions: [],
      provinciaOptions: [],
      servicioPortuarioOptions: []
    };
  },
  mounted() {
    this.fetchOptions();
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
      const nombrePuertoRegex = /^[A-Z][a-zA-ZáéíóúÁÉÍÓÚñÑäëöüÄËÏÜ ]{2,99}$/;
      const latitudRegex = /^[\d\.]+$/;
      const longitudRegex = /^[\d\.]+$/;
      let errorMessage = '';

      if (!nombrePuertoRegex.test(this.nombre_puerto)) {
        errorMessage += 'El campo "Nombre del Puerto" comienza con mayúscula y admite letras y espacios. Tamaño mínimo 3 caracteres y máximo 100 caracteres.\n';
      }
      if (!latitudRegex.test(this.latitud)) {
        errorMessage += 'El campo "Latitud" admite únicamente números y puntos.\n';
      }
      if (!longitudRegex.test(this.longitud)) {
        errorMessage += 'El campo "Longitud" admite únicamente números y puntos.\n';
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
    async fetchOptions() {
      try {
        const [paisResponse, provinciaResponse, servicioPortuarioResponse] = await Promise.all([
          axios.get('/api/paises/'),
          axios.get('/api/provincias/'),
          axios.get('/api/territorios/')
        ]);

        this.paisOptions = paisResponse.data.results;
        this.provinciaOptions = provinciaResponse.data.results;
        this.servicioPortuarioOptions = servicioPortuarioResponse.data.results;
      } catch (error) {
        console.error('Error al obtener las opciones:', error);
      }
    },
    async saveItem() {
      if (!this.validateForm()) {
        return; // Detener el envío si la validación falla
      }

      this.$store.commit('setIsLoading', true);
      const puerto = {
        nombre_puerto: this.nombre_puerto,
        pais: this.pais,
        provincia: this.provincia,
        servicio_portuario: this.servicio_portuario,
        latitud: this.latitud,
        longitud: this.longitud,
      };

      try {
        await axios.post('/api/puertos/', puerto);
        this.$router.push('/Puertos');
        Swal.fire('Agregado!', 'El puerto ha sido insertado exitosamente.', 'success');
      } catch (error) {
        console.error('Error al agregar el puerto:', error);
        Swal.fire('Error', 'Hubo un error al agregar el puerto.', 'error');
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    },
  },
};
</script>