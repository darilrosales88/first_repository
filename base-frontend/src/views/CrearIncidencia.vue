<template>
  <div>
    <div style="background-color: #002a68; color: white; text-align: right">
      <h6>Bienvenido:</h6>
    </div>
    <br />
    <Navbar-Component />
    <div class="form-container" style="margin-left: 18em; width: 75%">
      <h3 style="color: #002a68">Adicionar Incidencia</h3>
      <form @submit.prevent="save_incidencia">
        <div class="form-row">
          <div class="mb-3">
            <label for="codigo_incidencia" class="form-label"
              >Código de Incidencia:<span style="color: red">*</span></label
            >
            <input
              type="text"
              class="form-control"
              id="codigo_incidencia"
              v-model="codigo_incidencia"
              required
            />
          </div>

          <div class="mb-3">
            <label for="nombre_incidencia" class="form-label"
              >Nombre:<span style="color: red">*</span></label
            >
            <input
              type="text"
              class="form-control"
              id="nombre_incidencia"
              v-model="nombre_incidencia"
              required
            />
          </div>

          <div class="mb-3">
            <label for="tipo_imputable" class="form-label"
              >Tipo Imputable:</label
            >
            <select
              class="form-control"
              id="tipo_imputable"
              v-model="tipo_imputable"
              required
            >
              <option value="-">-</option>
              <option value="imputables_buque">Imputables al buque</option>
              <option value="imputables_puerto">Imputables al puerto</option>
              <option value="imputables_receptor">Imputables al receptor</option>
              <option value="imputables_otras_causas">Imputables a otras causas</option>
              <option value="imputables_imp_exp">Imputables al importador / exportador</option>
              <option value="imputables_aut_portuarias">Imputables a las autoridades portuarias</option>
            </select>
          </div>
        </div>

        <div class="form-buttons">
          <button
            type="button"
            @click="$router.push('/Incidencias')"
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
import axios from 'axios';
import Swal from 'sweetalert2';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'CrearIncidencia',
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
    async save_incidencia() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      const data = {
        codigo_incidencia: this.codigo_incidencia,
        nombre_incidencia: this.nombre_incidencia,
        tipo_imputable: this.tipo_imputable,
      };

      try {
        await axios.post('/api/incidencias/', data);
        Swal.fire('Agregado!', 'La incidencia ha sido añadida exitosamente.', 'success');
        this.$router.push('/Incidencias');
      } catch (error) {
        console.log(error);
        Swal.fire('Error', 'Hubo un error al agregar la incidencia.', 'error');
      }
    },
  },
};
</script>