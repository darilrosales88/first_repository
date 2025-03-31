<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container">
      <h3 style="color: #002A68;">Editar OSDE/OACE u Organismo</h3>
      <form @submit.prevent="update_osde_oace_organismo" class="form-grid">
        <!-- Campo Nombre -->
        <div class="mb-3">
          <label for="nombre" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre" v-model="nombre" required />
        </div>

        <!-- Campo Abreviatura -->
        <div class="mb-3">
          <label for="abreviatura" class="form-label">Abreviatura:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="abreviatura" v-model="abreviatura" required />
        </div>

        <!-- Campo Código REEUP -->
        <div class="mb-3">
          <label for="codigo_reeup" class="form-label">Código REEUP:</label>
          <input type="number" class="form-control" id="codigo_reeup" v-model="codigo_reeup" />
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
  name: 'EditarOrganismoView',
  components: {
    NavbarComponent,
  },
  data() {
    return {
      nombre: '',
      abreviatura: '',
      codigo_reeup: null,
    };
  },
  mounted() {
    this.getOsdeOaceOrganismo();
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
    // Obtener el registro existente por su ID
    async getOsdeOaceOrganismo() {
      const id = this.$route.params.id; // Obtener el ID de la URL
      try {
        const response = await axios.get(`/api/osde/${id}/`);
        const data = response.data;
        this.nombre = data.nombre;
        this.abreviatura = data.abreviatura;
        this.codigo_reeup = data.codigo_reeup;
      } catch (error) {
        console.error('Error al obtener el OSDE/OACE u Organismo:', error);
        Swal.fire('Error', 'No se pudo cargar el registro para editar.', 'error');
      }
    },

    // Validar el formulario
    validateForm() {
      const nombre_regex = /^[A-Z][\w\d\W]{2,99}$/;
      const abreviatura_regex = /^[A-ZÁÉÍÓÚ]{1}[A-Za-zÁÉÍÓÚáéíóú\s]{2,19}$/;
      const codigo_reeup_regex = /^[0-9]{5,11}$/;

      if (!nombre_regex.test(this.nombre)) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'El nombre debe comenzar con mayúscula, aceptar letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y máximo 100 caracteres.',
        });
        return false;
      }

      if (!abreviatura_regex.test(this.abreviatura)) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'La abreviatura debe comenzar con mayúscula seguido de espacio o caracteres alfabéticos. Tamaño mínimo 3 caracteres y máximo 20 caracteres.',
        });
        return false;
      }

      if (this.codigo_reeup && !codigo_reeup_regex.test(this.codigo_reeup)) {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'El código REEUP sólo admite números. Tamaño mínimo 5 caracteres y máximo 11 caracteres.',
        });
        return false;
      }

      return true;
    },

    // Actualizar el registro
    async update_osde_oace_organismo() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      const id = this.$route.params.id; // Obtener el ID de la URL
      const data = {
        nombre: this.nombre,
        abreviatura: this.abreviatura,
        codigo_reeup: this.codigo_reeup,
      };

      try {
        await axios.put(`/api/osde/${id}/`, data);
        Swal.fire('Actualizado!', 'El OSDE/OACE u Organismo ha sido actualizado exitosamente.', 'success');
        this.$router.push('/Organismos');
      } catch (error) {
        console.log(error);
        Swal.fire('Error', 'Hubo un error al actualizar el OSDE/OACE u Organismo.', 'error');
      }
    },
  },
};
</script>