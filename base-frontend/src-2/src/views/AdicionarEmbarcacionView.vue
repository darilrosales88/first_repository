<template>
  <div class="form-container">
    <h2>Adicionar embarcación</h2>
    <form @submit.prevent="save_embarcacion">
      <div class="form-group">
        <label for="nombre_embarcacion">Nombre</label>
        <input type="text" v-model="nombre_embarcacion" required />
      </div>

      <div class="form-group">
        <label for="nacionalidad">Nacionalidad</label>
        <select v-model="nacionalidad" required>
          <option v-for="nacionalidad in nationalities" :value="nacionalidad.id" :key="nacionalidad.id">
            {{ nacionalidad.nombre_pais }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="eslora">Eslora</label>
        <input type="number" v-model="eslora" step="0.01" required />
      </div>

      <div class="form-group">
        <label for="manga">Manga</label>
        <input type="number" v-model="manga" step="0.01" required />
      </div>

      <div class="form-group">
        <label for="calado_maximo">Calado máximo</label>
        <input type="number" v-model="calado_maximo" step="0.01" required />
      </div>

      <div class="form-group">
        <label for="desplazamiento_maximo">Desplazamiento máximo</label>
        <input type="number" v-model="desplazamiento_maximo" step="0.01" required />
      </div>

      <div class="form-group">
        <label for="tipo_embarcacion">Tipo de embarcación:</label>
        <select v-model="tipo_embarcacion" required>
          <option v-for="t_embarcacion in t_embarcacion_options" :value="t_embarcacion.value" :key="t_embarcacion.value">
            {{ t_embarcacion.text }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="tipo_buque">Tipo de buque:</label>
        <select v-model="tipo_buque" required>
          <option v-for="t_buque in t_buque_options" :value="t_buque.value" :key="t_buque.value">
            {{ t_buque.text }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="tipo_patana">Tipo de patana:</label>
        <select v-model="tipo_patana" required>
          <option v-for="t_patana in t_patana_options" :value="t_patana.value" :key="t_patana.value">
            {{ t_patana.text }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="imo">IMO</label>
        <input type="text" v-model="imo" required />
      </div>

      <div class="form-group">
        <label for="potencia">Potencia</label>
        <input type="number" v-model="potencia" step="0.01" required />
      </div>

      <div class="form-buttons">
        <button type="button" @click="confirmCancel" style="color:white;text-decoration:none">Cancelar</button>
        <button>Aceptar</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.form-container {
  max-width: 450px;
  margin: 50px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  text-align: left;
  margin-bottom: 20px;
  font-size: 20px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  font-size: 13px;
}

label {
  flex: 1;
  text-align: right;
  font-weight: bold;
}

input,
select {
  flex: 2;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.form-buttons {
  display: flex;
  justify-content: end;
  font-size: 15px;
}

button {
  padding: 5px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

button[type="button"] {
  background-color: #007bff;
  color: white;
}

button[type="submit"] {
  margin-left: 15px;
  background-color: #007bff;
  color: white;
}
</style>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
  name: 'AdicionarEmbarcacionView',
  data() {
    return {
      nationalities: [], // Almacena las nacionalidades obtenidas
      nombre_embarcacion: '',
      nacionalidad: '',
      eslora: '',
      manga: '',
      calado_maximo: '',
      desplazamiento_maximo: '',
      tipo_embarcacion: '',
      tipo_buque: '',
      tipo_patana: '',
      imo: '',
      potencia: '',
      t_embarcacion_options: [
        { value: 'buque', text: 'Buque' },
        { value: 'remolcador', text: 'Remolcador' },
        { value: 'patana', text: 'Patana' },
        { value: 'otros', text: 'Otros' },
      ],
      t_buque_options: [
        { value: 'buque_carga_gral', text: 'Buque de carga general' },
        { value: 'buque_granelero', text: 'Buque granelero' },
        { value: 'buque_ro_ro', text: 'Buque Ro Ro' },
        { value: 'buque_frig', text: 'Buque frigorífico' },
        { value: 'buque_tanque', text: 'Buque tanque' },
        { value: 'buque_gases', text: 'Buque de gases' },
      ],
      t_patana_options: [
        { value: '-', text: '-' },
        { value: 'pat_carga_seca', text: 'Patana de carga seca' },
        { value: 'pat_carga_liquida', text: 'Patana de carga líquida' },
        { value: 'patana_comb', text: 'Patana de combustible' },
        { value: 'patana_ro_ro', text: 'Patana Ro Ro' },
      ],
    };
  },
  mounted() {
    this.getNationalities(); // Llama al método para obtener las nacionalidades
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
      const nombre_embarcacion_regex = /^[A-Z][A-Za-z ]{3,100}$/;
      const imo_regex = /^[A-Za-z]{3}[0-9]{7}$/;
      let errorMessage = '';

      if (!nombre_embarcacion_regex.test(this.nombre_embarcacion)) {
        errorMessage +=
          'El campo "Nombre" debe comenzar con una mayúscula, seguir con letras y espacios, y tener entre 4 y 100 caracteres.\n';
      }

      if (!imo_regex.test(this.imo)) {
        errorMessage += 'El campo "IMO" debe comenzar con 3 letras seguidas de 7 dígitos.\n';
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

    async getNationalities() {
      try {
        const response = await axios.get('/api/paises/');
        this.nationalities = response.data;
      } catch (error) {
        console.error('Error al obtener las nacionalidades:', error);
        Swal.fire('Error', 'Hubo un error al obtener las nacionalidades.', 'error');
      }
    },

    async save_embarcacion() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      const data = {
        nombre_embarcacion: this.nombre_embarcacion,
        nacionalidad: this.nacionalidad,
        eslora: this.eslora,
        manga: this.manga,
        calado_maximo: this.calado_maximo,
        desplazamiento_maximo: this.desplazamiento_maximo,
        tipo_embarcacion: this.tipo_embarcacion,
        tipo_buque: this.tipo_buque,
        tipo_patana: this.tipo_patana,
        imo: this.imo,
        potencia: this.potencia,
      };

      try {
        await axios.post('/api/embarcaciones/', data);
        Swal.fire('Agregado!', 'La embarcación ha sido añadida exitosamente.', 'success');
        this.$router.push('/Embarcaciones');
      } catch (error) {
        console.error('Error al agregar la embarcación:', error);
        Swal.fire('Error', 'Hubo un error al agregar la embarcación.', 'error');
      }
    },
  },
};
</script>