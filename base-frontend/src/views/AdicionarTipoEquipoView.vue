<template>
  <div class="form-container">
    <h2>Adicionar tipo de equipo ferroviario</h2>
    <form @submit.prevent="saveTipoEquipo" class="form-grid">
      <div class="form-group">
        <label for="tipo_equipo">Tipo de equipo:<span style="color: red;">*</span></label>
        <select style="padding: 5px;" v-model="tipo_equipo" required>
          <option v-for="equipo in t_equipo_options" :value="equipo.value" :key="equipo.value">
            {{ equipo.text }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="tipo_carga">Tipo de carga:<span style="color: red;">*</span></label>
        <select style="padding: 5px;" v-model="tipo_carga" required>
          <option v-for="carga in t_carga_options" :value="carga.value" :key="carga.value">
            {{ carga.text }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="tipo_combustible">Tipo de combustible:<span style="color: red;">*</span></label>
        <select style="padding: 5px;" v-model="tipo_combustible" required>
          <option v-for="combustible in t_combustible_options" :value="combustible.value" :key="combustible.value">
            {{ combustible.text }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="longitud">Longitud (ft):</label>
        <input style="padding: 3px;" type="number" v-model="longitud" step="0.01" required />
      </div>
      <div class="form-group">
        <label for="peso_neto_sin_carga">Peso neto sin carga (t):</label>
        <input style="padding: 3px;" type="number" v-model="peso_neto_sin_carga" step="0.01" required />
      </div>
      <div class="form-group">
        <label for="peso_maximo_con_carga">Peso máximo con carga (t):</label>
        <input style="padding: 3px;" type="number" v-model="peso_maximo_con_carga" step="0.01" required />
      </div>
      <div class="form-group">
        <label for="capacidad_cubica_maxima">Capacidad cúbica máxima (ft3):</label>
        <input style="padding: 3px;" type="number" v-model="capacidad_cubica_maxima" step="0.01" required />
      </div>
      <div class="form-group">
        <label for="descripcion">Descripción:</label>
        <input style="padding: 3px;" type="text" v-model="descripcion" required />
      </div>
      <!-- Botones -->
      <div class="form-buttons">
        <button type="button" @click="confirmCancel" style="color:white;text-decoration:none">Cancelar</button>
        <button>Aceptar</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.form-container {
  max-width: 600px; /* Ajusta el ancho máximo del contenedor */
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
  width: 260px;
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


<script>
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
  data() {
    return {
      tipo_equipo: '',
      tipo_carga: '',
      tipo_combustible: '',
      longitud: '',
      peso_neto_sin_carga: '',
      peso_maximo_con_carga: '',
      capacidad_cubica_maxima: '',
      descripcion: '',
      t_equipo_options: [
        { value: 'casilla', text: 'Casilla' },
        { value: 'caj_gon', text: 'Cajones o Góndola' },
        { value: 'planc_plat', text: 'Plancha o Plataforma' },
        { value: 'Plan_porta_cont', text: 'Plancha porta contenedores' },
        { value: 'cist_liquidos', text: 'Cisterna para líquidos' },
        { value: 'cist_solidos', text: 'Cisterna para sólidos' },
        { value: 'tolva_g_mineral', text: 'Tolva granelera(mineral)' },
        { value: 'tolva_g_agric', text: 'Tolva granelera(agrícola)' },
        { value: 'tolva_g_cemento', text: 'Tolva para cemento' },
        { value: 'volqueta', text: 'Volqueta' },
        { value: 'Vagon_ref', text: 'Vagón refrigerado' },
        { value: 'jaula', text: 'Jaula' },
        { value: 'locomotora', text: 'Locomotora' },
        { value: 'tren', text: 'Tren' },
      ],
      t_carga_options: [
        { value: 'combustible', text: 'Combustible' },
        { value: 'aceite', text: 'Aceite' },
        { value: 'miel', text: 'Miel' },
        { value: 'alcohol', text: 'Alcohol' },
        { value: 'quimicos', text: 'Químicos' },
        { value: 'contenedores', text: 'Contenedores' },
        { value: 'otros', text: 'Otros' },
      ],
      t_combustible_options: [
        { value: '-', text: '-' },
        { value: 'combust_blanco', text: 'Combustible blanco' },
        { value: 'combustible_negro', text: 'Combustible negro' },
        { value: 'combustible_turbo', text: 'Combustible turbo' },
      ],
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
    async saveTipoEquipo() {
      const data = {
        tipo_equipo: this.tipo_equipo,
        tipo_carga: this.tipo_carga,
        tipo_combustible: this.tipo_combustible,
        longitud: this.longitud,
        peso_neto_sin_carga: this.peso_neto_sin_carga,
        peso_maximo_con_carga: this.peso_maximo_con_carga,
        capacidad_cubica_maxima: this.capacidad_cubica_maxima,
        descripcion: this.descripcion,
      };

      try {
        await axios.post('/api/tipos_equipos/', data);
        Swal.fire('Agregado!', 'El tipo de equipo ferroviario ha sido añadido exitosamente.', 'success');
        this.$router.push('/TipoEquipoFerro');
      } catch (error) {
        console.log(error);
        Swal.fire('Error', 'Hubo un error al agregar el tipo de equipo ferroviario.', 'error');
      }
    }
  }
};
</script>