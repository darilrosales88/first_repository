<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container">
      <h3 style="color: #002A68;">Editar estructura de ubicación {{ estructura.nombre_estructura_ubicacion }}</h3>
      <form @submit.prevent="submitForm" class="form-grid">
        <!-- Campo Terminal -->
        <div class="mb-3">
          <label for="terminal" class="form-label">Terminal:<span style="color: red;">*</span></label>
          <select class="form-control" id="terminal" v-model="estructura.terminal" required>
            <option v-for="terminal in terminales" :value="terminal.id" :key="terminal.id">
              {{ terminal.nombre_terminal }}
            </option>
          </select>
        </div>

        <!-- Campo Tipo de estructura -->
        <div class="mb-3">
          <label for="tipo_estructura" class="form-label">Tipo de estructura:<span style="color: red;">*</span></label>
          <select class="form-control" id="tipo_estructura" v-model="estructura.tipo_estructura" required>
            <option v-for="tipo_estructura in tipos_estructuras" :value="tipo_estructura.id" :key="tipo_estructura.id">
              {{ tipo_estructura.nombre_tipo_estructura_ubicacion }}
            </option>
          </select>
        </div>

        <!-- Campo Estructura padre -->
        <div class="mb-3">
          <label for="estructura_padre" class="form-label">Estructura padre:</label>
          <select class="form-control" id="estructura_padre" v-model="estructura.estructura_padre">
            <option v-for="estructura in estructuras" :value="estructura.id" :key="estructura.id">
              {{ estructura.nombre_estructura_ubicacion }}
            </option>
          </select>
        </div>

        <!-- Campo Nombre -->
        <div class="mb-3">
          <label for="nombre_estructura_ubicacion" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre_estructura_ubicacion" v-model="estructura.nombre_estructura_ubicacion" required />
        </div>

        <!-- Campo Capacidad -->
        <div class="mb-3">
          <label for="capacidad" class="form-label">Capacidad:<span style="color: red;">*</span></label>
          <input type="number" class="form-control" id="capacidad" v-model="estructura.capacidad" step="0.01" required />
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
  grid-template-columns: repeat(3, 1fr); /* 3 columnas de igual tamaño */
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
  grid-column: span 3; /* Los botones ocupan las 2 columnas */
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
  name: 'EditarEstructuradeUbicacion',
  components: {
    NavbarComponent,
  },
  data() {
    return {
      estructura: {},
      terminales: [], // Almacena las terminales obtenidas
      tipos_estructuras: [], // Almacena los tipos de estructuras obtenidas
      estructuras: [], // Almacena las estructuras obtenidas
    };
  },

  mounted() {
    this.getTerminales(); // Llama al método para obtener las terminales
    this.getTiposEstructuras(); // Llama al método para obtener los tipos de estructuras
    this.getEstructuras(); // Llama al método para obtener las estructuras
    this.get_estructura();
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
    async getTerminales() {
      try {
        const response = await axios.get('/api/terminales/');
        this.terminales = response.data;
      } catch (error) {
        console.error('Error al obtener las terminales:', error);
      }
    },

    async getTiposEstructuras() {
      try {
        const response = await axios.get('/api/tipos_estructuras_ubicacion/');
        this.tipos_estructuras = response.data;
      } catch (error) {
        console.error('Error al obtener los tipos de estructuras:', error);
      }
    },

    async getEstructuras() {
      try {
        const response = await axios.get('/api/estructuras_ubicacion/');
        this.estructuras = response.data;
      } catch (error) {
        console.error('Error al obtener las estructuras:', error);
      }
    },

    validateForm() {
      const nombre_estructura_ubicacion_regex = /^[A-Z][\w\d\W]{2,99}$/;

      if (!nombre_estructura_ubicacion_regex.test(this.estructura.nombre_estructura_ubicacion)) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'El nombre debe comenzar con mayúscula, aceptar letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y máximo 100 caracteres.',
        });
        return false;
      }

      return true;
    },

    async get_estructura() {
      this.$store.commit('setIsLoading', true);
      const estructura_id = this.$route.params.id;
      try {
        const response = await axios.get(`/api/estructuras_ubicacion/${estructura_id}/`);
        this.estructura = response.data;
      } catch (error) {
        console.log(error);
      }
      this.$store.commit('setIsLoading', false);
    },

    async submitForm() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      this.$store.commit('setIsLoading', true);
      const estructura_id = this.$route.params.id;
      const data = {
        ...this.estructura,
      };

      try {
        await axios.patch(`/api/estructuras_ubicacion/${estructura_id}/`, data);
        this.$router.push('/EstructuraUbicacion');
        Swal.fire('Actualizado!', 'La estructura de ubicación ha sido modificada exitosamente.', 'success');
      } catch (error) {
        console.log(error);
        Swal.fire('Error', 'Hubo un error al actualizar la estructura de ubicación.', 'error');
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    },
  },
};
</script>