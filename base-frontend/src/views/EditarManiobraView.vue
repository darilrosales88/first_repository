<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container" style="margin-left: 18em; width: 75%">
      <h3 style="color: #002A68;">Editar tipo de maniobra portuaria</h3>
      <form @submit.prevent="save_maniobra" class="form-grid">
        <!-- Campo Nombre de la Maniobra -->
        <div class="mb-3">
          <label for="nombre_maniobra" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre_maniobra" v-model="nombre_maniobra" required />
        </div>

        <!-- Campo Tipo de Maniobra -->
        <div class="mb-3">
          <label for="tipo_maniobra" class="form-label">Tipo:<span style="color: red;">*</span></label>
          <select class="form-control" id="tipo_maniobra" v-model="tipo_maniobra" required>
            <option v-for="t_maniobra in t_maniobra_options" :value="t_maniobra.value" :key="t_maniobra.value">
              {{ t_maniobra.text }}
            </option>
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
  grid-template-columns: repeat(2, 1fr); /* 2 columnas de igual tamaño */
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
  name: 'EditarManiobraView',
  components: {
    NavbarComponent,
  },
  data() {
    return {
      nombre_maniobra: '',
      tipo_maniobra: '',
      t_maniobra_options: [
        { value: 'entrada', text: 'Maniobra de entrada' },
        { value: 'salida', text: 'Maniobra de salida' },
      ],
    };
  },
  mounted() {
    this.get_maniobra(); // Cargar los datos del registro a editar
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
      const nombre_maniobra_regex = /^[A-Z][\w\s]{1,99}$/;

      if (!nombre_maniobra_regex.test(this.nombre_maniobra)) {
        Swal.fire({
          icon: 'error',
          title: 'Error de validación',
          text: 'El campo "Nombre" debe comenzar con mayúscula, seguido de letras y espacios. No puede exceder los 100 caracteres.',
        });
        return false; // Detener el envío del formulario
      }

      return true; // El formulario es válido
    },
    async get_maniobra() {
      const maniobra_id = this.$route.params.id; // Obtener el ID del registro desde la URL
      try {
        const response = await axios.get(`/api/tipo_maniobras/${maniobra_id}/`);
        this.nombre_maniobra = response.data.nombre_maniobra;
        this.tipo_maniobra = response.data.tipo_maniobra;
      } catch (error) {
        console.error('Error al obtener la maniobra:', error);
        Swal.fire('Error', 'No se pudo cargar la maniobra.', 'error');
      }
    },
    async save_maniobra() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      const maniobra_id = this.$route.params.id; // Obtener el ID del registro desde la URL
      const data = {
        nombre_maniobra: this.nombre_maniobra,
        tipo_maniobra: this.tipo_maniobra,
      };

      try {
        await axios.patch(`/api/tipo_maniobras/${maniobra_id}/`, data); // Usar PATCH para actualizar
        Swal.fire('Actualizado!', 'El tipo de maniobra portuaria ha sido modificado exitosamente.', 'success');
        this.$router.push('/TipoManiobra');
      } catch (error) {
        console.error('Error al actualizar la maniobra:', error);
        Swal.fire('Error', 'Hubo un error al actualizar el tipo de maniobra portuaria.', 'error');
      }
    },
  },
};
</script>
