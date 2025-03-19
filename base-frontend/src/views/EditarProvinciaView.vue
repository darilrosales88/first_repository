<template>
  <div>
    <Navbar-Component />
    
    <div class="form-container">
      <h3 style="color: #002A68;">Editar Provincia</h3>
      <form @submit.prevent="saveItem" class="form-grid">
        <!-- Campo Código -->
        <div class="mb-3">
          <label for="codigo" class="form-label">Código:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="codigo" v-model="codigo" required />
        </div>

        <!-- Campo Nombre -->
        <div class="mb-3">
          <label for="nombre" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre" v-model="nombre_provincia" required />
        </div>

        <!-- Campo País -->
        <div class="mb-3">
          <label for="pais" class="form-label">País:<span style="color: red;">*</span></label>
          <select class="form-control" id="pais" v-model="pais" required>
            <option v-for="item in selectedPais" :key="item.id" :value="item.id">{{ item.nombre_pais }}</option>
          </select>
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
  max-width: 680px; /* Ancho reducido */
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
  name: 'EditarProvinciaView',
  components: {
    NavbarComponent,
  },

  data() {
    return {
      selectedPais: [], // Almacena los países obtenidos
      codigo: '',
      codigo_error: null,
      pais: '',
      nombre_provincia: '',
      nombre_provincia_error: null,
      provinciaId: null, // ID de la provincia que se está editando
    };
  },

  mounted() {
    this.getPaises(); // Obtener la lista de países
    this.getProvincia(); // Obtener los datos de la provincia a editar
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
    // Obtener los datos de la provincia a editar
    async getProvincia() {
      this.provinciaId = this.$route.params.id; // Obtener el ID de la provincia desde la URL
      try {
        const response = await axios.get(`/api/provincias/${this.provinciaId}/`);
        const provincia = response.data;
        this.codigo = provincia.codigo;
        this.nombre_provincia = provincia.nombre_provincia;
        this.pais = provincia.pais;
      } catch (error) {
        console.error('Error al obtener la provincia:', error);
        Swal.fire('Error', 'No se pudo cargar la provincia.', 'error');
        this.$router.push('/Provincia'); // Redirigir si hay un error
      }
    },

    // Validar el formulario
    validateForm() {
      const codigo_regex = /[0-9]{2}$/;
      const nombre_provincia_regex = /^[A-Z][a-zA-ZáéíóúÁÉÍÓÚñÑäëöüÄËÏÜ ]{2,99}$/;

      let valid = true;

      if (!codigo_regex.test(this.codigo)) {
        this.codigo_error = 'Este campo sólo admite dos números.';
        Swal.fire({
          icon: 'error',
          title: 'Error en el código',
          text: this.codigo_error,
        });
        valid = false;
      } else {
        this.codigo_error = null;
      }

      if (!nombre_provincia_regex.test(this.nombre_provincia)) {
        this.nombre_provincia_error =
          'Este campo comienza con mayúscula seguido de espacio, caracteres alfabéticos y no puede exceder los 100 caracteres.';
        Swal.fire({
          icon: 'error',
          title: 'Error en el nombre de la provincia',
          text: this.nombre_provincia_error,
        });
        valid = false;
      } else {
        this.nombre_provincia_error = null;
      }

      return valid;
    },

    // Obtener la lista de países
    async getPaises() {
      try {
        const response = await axios.get('/api/paises/');
        this.selectedPais = response.data;
      } catch (error) {
        console.error('Error al obtener los países:', error);
      }
    },

    // Guardar los cambios
    async saveItem() {
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      const data = {
        nombre_provincia: this.nombre_provincia,
        pais: this.pais,
        codigo: this.codigo,
      };

      try {
        await axios.put(`/api/provincias/${this.provinciaId}/`, data);
        Swal.fire('Actualizado!', 'La provincia ha sido actualizada exitosamente.', 'success');
        this.$router.push('/Provincia');
      } catch (error) {
        console.log(error);
        Swal.fire('Error', 'Hubo un error al actualizar la provincia.', 'error');
      }
    },
  },
};
</script>