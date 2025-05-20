<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container">
      <h2>Adicionar tipo de equipo ferroviario</h2>
      <form @submit.prevent="saveTipoEquipo" class="form-grid">
        <!-- Campo Tipo de Equipo -->
        <div class="mb-3">
          <label for="tipo_equipo" class="form-label">Tipo de equipo:<span style="color: red;">*</span></label>
          <select class="form-control" id="tipo_equipo" v-model="tipo_equipo" required>
            <option v-for="equipo in t_equipo_options" :value="equipo.value" :key="equipo.value">
              {{ equipo.text }}
            </option>
          </select>
        </div>

        <!-- Campo Tipo de Carga -->
        <div class="mb-3">
          <label for="tipo_carga" class="form-label">Tipo de carga:<span style="color: red;">*</span></label>
          <select class="form-control" id="tipo_carga" v-model="tipo_carga" required>
            <option v-for="carga in t_carga_options" :value="carga.value" :key="carga.value">
              {{ carga.text }}
            </option>
          </select>
        </div>

        <!-- Campo Tipo de Combustible -->
        <div class="mb-3">
          <label for="tipo_combustible" class="form-label">Tipo de combustible:<span style="color: red;">*</span></label>
          <select class="form-control" id="tipo_combustible" v-model="tipo_combustible" required>
            <option v-for="combustible in t_combustible_options" :value="combustible.value" :key="combustible.value">
              {{ combustible.text }}
            </option>
          </select>
        </div>

        <!-- Campo Longitud -->
        <div class="mb-3">
          <label for="longitud" class="form-label">Longitud (ft):</label>
          <input type="number" class="form-control" id="longitud" v-model="longitud" step="0.01" required />
        </div>

        <!-- Campo Peso Neto Sin Carga -->
        <div class="mb-3">
          <label for="peso_neto_sin_carga" class="form-label">Peso neto sin carga (t):</label>
          <input type="number" class="form-control" id="peso_neto_sin_carga" v-model="peso_neto_sin_carga" step="0.01" required />
        </div>

        <!-- Campo Peso Máximo con Carga -->
        <div class="mb-3">
          <label for="peso_maximo_con_carga" class="form-label">Peso máximo con carga (t):</label>
          <input type="number" class="form-control" id="peso_maximo_con_carga" v-model="peso_maximo_con_carga" step="0.01" required />
        </div>

        <!-- Campo Capacidad Cúbica Máxima -->
        <div class="mb-3">
          <label for="capacidad_cubica_maxima" class="form-label">Capacidad cúbica máxima (ft3):</label>
          <input type="number" class="form-control" id="capacidad_cubica_maxima" v-model="capacidad_cubica_maxima" step="0.01" required />
        </div>

        <!-- Campo Descripción -->
        <div class="mb-3">
          <label for="descripcion" class="form-label">Descripción:</label>
          <input type="text" class="form-control" id="descripcion" v-model="descripcion" required />
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
  max-width: 680px; /* Ajusta el ancho máximo del contenedor */
  margin: 20px; /* Centra el formulario */
  padding: 20px;
  margin-left: 220px;
  background-color: rgb(245, 245, 245);
  border-radius: 8px;
  
}

h2 {
  text-align: left;
  margin-bottom: 20px;
  font-size: 18px;
}

.form-label {
  font-size: 14px;
  text-align: left;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 3 columnas de igual tamaño */
  gap: 15px; /* Espacio entre los elementos */
}

.mb-3 {
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
  grid-column: span 3; /* Los botones ocupan las 3 columnas */
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
import axios from 'axios';
import Swal from 'sweetalert2';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  components: {
    NavbarComponent,
  },
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
        { value: 'combustible_blanco', text: 'Combustible blanco' },
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