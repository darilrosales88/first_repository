<template>
  <div class="form-container">
    <h2>Editar Equipo Ferroviario</h2>
    <form @submit.prevent="update_equipo_ferroviario" class="form-grid">
      <!-- Tipo de equipo -->
      <div class="form-group">
        <label for="tipo_equipo">Tipo de equipo:<span style="color: red;">*</span></label>
        <select style="padding: 5px;" v-model="tipo_equipo" required>
          <option v-for="tef in tipos_equipos" :key="tef.id" :value="tef.id">{{ tef.tipo_equipo_name }} - {{ tef.tipo_carga_name }} - {{tef.peso_maximo_con_carga}}</option>
        </select>
      </div>


      <!-- Número de identificación -->
      <div class="form-group">
        <label for="numero_identificacion">Número de identificación:<span style="color: red;">*</span></label>
        <input style="padding: 3px;" type="text" v-model="numero_identificacion" required />
      </div>

      <!-- Territorio -->
      <div class="form-group">
        <label for="territorio">Territorio:<span style="color: red;">*</span></label>
        <select style="padding: 5px;" v-model="territorio" required>
          <option value="-">-</option>
          <option value="oriente">Oriente</option>
          <option value="centro">Centro</option>
          <option value="occidente">Occidente</option>
        </select>
      </div>

      <!-- Tipo de carga -->
      <div class="form-group">
        <label for="tipo_carga">Tipo de carga</label>
        <input style="padding: 3px;" type="text" v-model="tipo_carga" disabled />
      </div>

      <!-- Tipo de combustible -->
      <div class="form-group">
        <label for="tipo_combustible">Tipo de combustible</label>
        <input style="padding: 3px;" type="text" v-model="tipo_combustible" disabled />
      </div>

      <!-- Peso máximo -->
      <div class="form-group">
        <label for="peso_maximo">Peso máximo (t)</label>
        <input style="padding: 3px;" type="number" v-model="peso_maximo" step="0.01" disabled />
      </div>

      <!-- Botones -->
      <div class="form-buttons">
        <button type="button" @click="confirmCancel" style="color:white;text-decoration:none">Cancelar</button>
        <button>Aceptar</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
  name: 'EditarEquipoFerroviario',
  data() {
    return {
      tipo_equipo: '',
      numero_identificacion: '',
      territorio: '-',
      tipo_carga: '',
      tipo_combustible: '',
      peso_maximo: '',
      tipos_equipos: [], // Almacenará los tipos de equipos ferroviarios
    };
  },
  async mounted() {
    const id = this.$route.params.id; // Obtener el ID de la URL
    await this.getTiposEquipos(); // Obtener los tipos de equipos
    await this.getEquipoFerroviario(id); // Obtener el equipo ferroviario por su ID
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
    // Obtener los tipos de equipos ferroviarios
    async getTiposEquipos() {
      try {
        const response = await axios.get('/api/tipos_equipos/');
        this.tipos_equipos = response.data;
      } catch (error) {
        console.error('Error al obtener los tipos de equipos ferroviarios:', error);
      }
    },

    // Obtener el equipo ferroviario por su ID
    async getEquipoFerroviario(id) {
      try {
        const response = await axios.get(`/api/equipos_ferroviarios/${id}/`);
        const data = response.data;
        this.tipo_equipo = data.tipo_equipo;
        this.numero_identificacion = data.numero_identificacion;
        this.territorio = data.territorio;
        this.tipo_carga = data.tipo_carga;
        this.tipo_combustible = data.tipo_combustible;
        this.peso_maximo = data.peso_maximo;

        // Actualizar los campos automáticamente al cargar el equipo
        this.updateFieldsBasedOnTipoEquipo();
      } catch (error) {
        console.error('Error al obtener el equipo ferroviario:', error);
        Swal.fire('Error', 'No se pudo cargar el registro para editar.', 'error');
      }
    },

    // Actualizar los campos automáticamente en función del tipo de equipo seleccionado
    updateFieldsBasedOnTipoEquipo() {
      if (this.tipo_equipo) {
        const selectedTipoEquipo = this.tipos_equipos.find(tef => tef.id === this.tipo_equipo);
        if (selectedTipoEquipo) {
          this.tipo_carga = selectedTipoEquipo.tipo_carga_name;
          this.tipo_combustible = selectedTipoEquipo.tipo_combustible_name;
          this.peso_maximo = selectedTipoEquipo.peso_maximo_con_carga;
        }
      }
    },

    // Validar el formulario
    validateForm() {
      const numero_identificacion_regex = /^[\d\w\W\s]{3,10}$/; // Acepta letras, números y caracteres especiales (3-10 caracteres)
      let errorMessage = '';

      if (!numero_identificacion_regex.test(this.numero_identificacion)) {
        errorMessage +=
          'El campo "Número de identificación" acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y máximo 10 caracteres.\n';
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

    // Actualizar el equipo ferroviario
    async update_equipo_ferroviario() {
      if (!this.validateForm()) {
        return; // Detener el envío si la validación falla
      }

      const id = this.$route.params.id; // Obtener el ID de la URL
      const data = {
        tipo_equipo: this.tipo_equipo,
        numero_identificacion: this.numero_identificacion,
        territorio: this.territorio,
        tipo_carga: this.tipo_carga,
        tipo_combustible: this.tipo_combustible,
        peso_maximo: this.peso_maximo,
      };

      try {
        await axios.put(`/api/equipos_ferroviarios/${id}/`, data);
        Swal.fire('Actualizado!', 'El equipo ferroviario ha sido actualizado exitosamente.', 'success');
        this.$router.push('/EquipoFerro');
      } catch (error) {
        console.error('Error al actualizar el equipo ferroviario:', error);
        Swal.fire('Error', 'Hubo un error al actualizar el equipo ferroviario.', 'error');
      }
    },
  },
  watch: {
    // Observar cambios en el campo tipo_equipo
    tipo_equipo(newVal) {
      if (newVal) {
        this.updateFieldsBasedOnTipoEquipo();
      }
    },
  },
};
</script>

<style scoped>
.form-container {
  max-width: 690px; /* Ajusta el ancho máximo del contenedor */
  margin: 50px; /* Centra el contenedor */
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

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 4 columnas de igual tamaño */
  gap: 15px; /* Espacio entre los elementos */
}

.form-group {
  text-align: left;
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 14px;
}

label {
  font-weight: bold;
}

input, select {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.form-buttons {
  grid-column: span 2; /* Los botones ocupan las 4 columnas */
  display: flex;
  justify-content: end;
  font-size: 15px;
  margin-top: 20px;
}

button {
  margin-left: 10px;
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