<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container">
      <h3 style="color: #002A68;">Editar Incidencia</h3>
      <form @submit.prevent="update_incidencia" class="form-grid">
        <!-- Campo Código de Incidencia -->
        <div class="mb-3">
          <label for="codigo_incidencia" class="form-label">Código de Incidencia:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="codigo_incidencia" v-model="codigo_incidencia" required />
        </div>

        <!-- Campo Nombre de Incidencia -->
        <div class="mb-3">
          <label for="nombre_incidencia" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre_incidencia" v-model="nombre_incidencia" required />
        </div>

        <!-- Campo Tipo Imputable -->
        <div class="mb-3">
          <label for="tipo_imputable" class="form-label">Tipo Imputable:<span style="color: red;">*</span></label>
          <select class="form-control" id="tipo_imputable" v-model="tipo_imputable" required>
            <option value="-">-</option>
            <option value="imputables_buque">Imputables al buque</option>
            <option value="imputables_puerto">Imputables al puerto</option>
            <option value="imputables_receptor">Imputables al receptor</option>
            <option value="imputables_otras_causas">Imputables a otras causas</option>
            <option value="imputables_imp_exp">Imputables al importador / exportador</option>
            <option value="imputables_aut_portuarias">Imputables a las autoridades portuarias</option>
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
    name: 'EditarIncidencia',
    components: {
    NavbarComponent,
  },
    data() {
      return {
        codigo_incidencia: '',
        nombre_incidencia: '',
        tipo_imputable: '-',
      };
    },
    mounted() {
      this.getIncidencia();
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
      async getIncidencia() {
        const id = this.$route.params.id; // Obtener el ID de la URL
        try {
          const response = await axios.get(`/api/incidencias/${id}/`);
          const data = response.data;
          this.codigo_incidencia = data.codigo_incidencia;
          this.nombre_incidencia = data.nombre_incidencia;
          this.tipo_imputable = data.tipo_imputable;
        } catch (error) {
          console.error('Error al obtener la incidencia:', error);
          Swal.fire('Error', 'No se pudo cargar el registro para editar.', 'error');
        }
      },
  
      // Validar el formulario
      validateForm() {
        const codigo_incidencia_regex = /^[\w\d\W ]{2,5}$/;
        const nombre_incidencia_regex = /^[\w\d\W ]{3,100}$/;
  
        if (!codigo_incidencia_regex.test(this.codigo_incidencia)) {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'El código de incidencia acepta letras, números y caracteres especiales. Tamaño mínimo 2 caracteres y máximo 5 caracteres.',
          });
          return false;
        }
  
        if (!nombre_incidencia_regex.test(this.nombre_incidencia)) {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'El nombre acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y máximo 100 caracteres.',
          });
          return false;
        }
  
        return true;
      },
  
      // Actualizar el registro
      async update_incidencia() {
        // Validar el formulario antes de enviarlo
        if (!this.validateForm()) {
          return; // Si la validación falla, no enviar el formulario
        }
  
        const id = this.$route.params.id; // Obtener el ID de la URL
        const data = {
          codigo_incidencia: this.codigo_incidencia,
          nombre_incidencia: this.nombre_incidencia,
          tipo_imputable: this.tipo_imputable,
        };
  
        try {
          await axios.put(`/api/incidencias/${id}/`, data);
          Swal.fire('Actualizado!', 'La incidencia ha sido actualizada exitosamente.', 'success');
          this.$router.push('/Incidencias');
        } catch (error) {
          console.log(error);
          Swal.fire('Error', 'Hubo un error al actualizar la incidencia.', 'error');
        }
      },
    },
  };
  </script>