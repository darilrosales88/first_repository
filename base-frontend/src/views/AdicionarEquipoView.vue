<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container">
      <h2>Adicionar Equipo Ferroviario</h2>
      <form @submit.prevent="save_equipo_ferroviario" class="form-grid">
        <!-- Tipo de equipo -->
        <div class="mb-3">
          <label for="tipo_equipo" class="form-label">Tipo de equipo:<span style="color: red;">*</span></label>
          <select class="form-control" id="tipo_equipo" v-model="tipo_equipo" required>
            <option v-for="tef in tipos_equipos" :key="tef.id" :value="tef.id">
              {{ tef.tipo_equipo_name }} - {{ tef.tipo_carga_name }} - {{ tef.peso_maximo_con_carga }}
            </option>
          </select>
        </div>

        <!-- Número de identificación -->
        <div class="mb-3">
          <label for="numero_identificacion" class="form-label">Número de identificación:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="numero_identificacion" v-model="numero_identificacion" required />
        </div>

        <!-- Territorio -->
        <div class="mb-3">
          <label for="territorio" class="form-label">Territorio:<span style="color: red;">*</span></label>
          <select class="form-control" id="territorio" v-model="territorio" required>
            <option value="-">-</option>
            <option value="oriente">Oriente</option>
            <option value="centro">Centro</option>
            <option value="occidente">Occidente</option>
          </select>
        </div>

        <!-- Tipo de carga -->
        <div class="mb-3">
          <label for="tipo_carga" class="form-label">Tipo de carga</label>
          <input type="text" class="form-control" id="tipo_carga" v-model="tipo_carga" disabled />
        </div>

        <!-- Tipo de combustible -->
        <div class="mb-3">
          <label for="tipo_combustible" class="form-label">Tipo de combustible</label>
          <input type="text" class="form-control" id="tipo_combustible" v-model="tipo_combustible" disabled />
        </div>

        <!-- Peso máximo -->
        <div class="mb-3">
          <label for="peso_maximo" class="form-label">Peso máximo (t)</label>
          <input type="number" class="form-control" id="peso_maximo" v-model="peso_maximo" step="0.01" disabled />
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
  max-width: 675px; /* Ajusta el ancho máximo del contenedor */
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
  width: 200px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-control {
  background-color: white;
  padding: 1px 0px; /* Padding reducido */
  height: 25px; /* Altura reducida */
  font-size: 14px; /* Tamaño de fuente reducido */
  border: 1px solid #ccc;
  border-radius: 2px;
}

.form-buttons {
  grid-column: span 2; /* Los botones ocupan las 2 columnas */
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
  name: 'CrearEquipoFerroviario',
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
    await this.getTiposEquipos();
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
        this.tipos_equipos = response.data.results;
      } catch (error) {
        console.error('Error al obtener los tipos de equipos ferroviarios:', error);
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

    // Guardar el equipo ferroviario
    async save_equipo_ferroviario() {
      if (!this.validateForm()) {
        return; // Detener el envío si la validación falla
      }

      const data = {
        tipo_equipo: this.tipo_equipo,
        numero_identificacion: this.numero_identificacion,
        territorio: this.territorio,
        tipo_carga: this.tipo_carga,
        tipo_combustible: this.tipo_combustible,
        peso_maximo: this.peso_maximo,
      };

      try {
        await axios.post('/api/equipos_ferroviarios/', data);
        Swal.fire('Agregado!', 'El equipo ferroviario ha sido añadido exitosamente.', 'success');
        this.$router.push('/EquipoFerro');
      } catch (error) {
        console.error('Error al agregar el equipo ferroviario:', error);
        Swal.fire('Error', 'Hubo un error al agregar el equipo ferroviario.', 'error');
      }
    },
  },
  watch: {
    // Observar cambios en el campo tipo_equipo
    tipo_equipo(newVal) {
      if (newVal) {
        // Buscar el tipo de equipo seleccionado en la lista de tipos_equipos
        const selectedTipoEquipo = this.tipos_equipos.find(tef => tef.id === newVal);
        if (selectedTipoEquipo) {
          // Actualizar los campos automáticamente
          this.tipo_carga = selectedTipoEquipo.tipo_carga_name;
          this.tipo_combustible = selectedTipoEquipo.tipo_combustible_name;
          this.peso_maximo = selectedTipoEquipo.peso_maximo_con_carga;
        }
      }
    },
  },
};
</script>

