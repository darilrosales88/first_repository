<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container" style="margin-left: 18em; width: 75%">
      <h2>Adicionar embarcación</h2>
      <form @submit.prevent="save_embarcacion" class="form-grid">
        <div class="mb-3">
          <label for="nombre_embarcacion" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre_embarcacion" v-model="nombre_embarcacion" required />
        </div>

        <div class="mb-3">
          <label for="nacionalidad" class="form-label">Nacionalidad:<span style="color: red;">*</span></label>
          <select class="form-control" id="nacionalidad" v-model="nacionalidad" required>
            <option v-for="nacionalidad in nationalities" :value="nacionalidad.id" :key="nacionalidad.id">
              {{ nacionalidad.nombre_pais }}
            </option>
          </select>
        </div>

        <div class="mb-3">
          <label for="eslora" class="form-label">Eslora:<span style="color: red;">*</span></label>
          <input type="number" class="form-control" id="eslora" v-model="eslora" step="0.01" required />
        </div>

        <div class="mb-3">
          <label for="manga" class="form-label">Manga:<span style="color: red;">*</span></label>
          <input type="number" class="form-control" id="manga" v-model="manga" step="0.01" required />
        </div>

        <div class="mb-3">
          <label for="calado_maximo" class="form-label">Calado máximo:<span style="color: red;">*</span></label>
          <input type="number" class="form-control" id="calado_maximo" v-model="calado_maximo" step="0.01" required />
        </div>

        <div class="mb-3">
          <label for="desplazamiento_maximo" class="form-label">Desplazamiento máximo:<span style="color: red;">*</span></label>
          <input type="number" class="form-control" id="desplazamiento_maximo" v-model="desplazamiento_maximo" step="0.01" required />
        </div>

        <div class="mb-3">
          <label for="tipo_embarcacion" class="form-label">Tipo de embarcación:<span style="color: red;">*</span></label>
          <select class="form-control" id="tipo_embarcacion" v-model="tipo_embarcacion" required>
            <option v-for="t_embarcacion in t_embarcacion_options" :value="t_embarcacion.value" :key="t_embarcacion.value">
              {{ t_embarcacion.text }}
            </option>
          </select>
        </div>

        <div class="mb-3" v-if="tipo_embarcacion === 'buque'">
          <label for="tipo_buque" class="form-label">Tipo de buque:<span style="color: red;">*</span></label>
          <select class="form-control" id="tipo_buque" v-model="tipo_buque" required>
            <option v-for="t_buque in t_buque_options" :value="t_buque.value" :key="t_buque.value">
              {{ t_buque.text }}
            </option>
          </select>
        </div>

        <div class="mb-3" v-if="tipo_embarcacion === 'patana'">
          <label for="tipo_patana" class="form-label">Tipo de patana:<span style="color: red;">*</span></label>
          <select class="form-control" id="tipo_patana" v-model="tipo_patana" required>
            <option v-for="t_patana in t_patana_options" :value="t_patana.value" :key="t_patana.value">
              {{ t_patana.text }}
            </option>
          </select>
        </div>

        <div class="mb-3" v-if="tipo_embarcacion === 'buque'">
          <label for="imo" class="form-label">IMO:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="imo" v-model="imo" required />
        </div>

        <div class="mb-3" v-if="tipo_embarcacion === 'remolcador'">
          <label for="potencia" class="form-label">Potencia:<span style="color: red;">*</span></label>
          <input type="number" class="form-control" id="potencia" v-model="potencia" step="0.01" required />
        </div>

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
  border-radius: 8px;
  background-color: rgb(245, 245, 245);
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
  padding: 1px 0px; /* Padding reducido */
  height: 25px; /* Altura reducida */
  font-size: 14px; /* Tamaño de fuente reducido */
  border: 1px solid #ccc;
  border-radius: 2px;
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
    console.log('Potencia inicializada:', this.potencia); // Verificar que potencia esté definidas
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
      const nombre_embarcacion_regex = /^[A-Z][A-Za-z ]{2,100}$/;
      const imo_regex = /^[A-Za-z]{3}[0-9]{7}$/;
      this.errorMessage = '';

      if (!nombre_embarcacion_regex.test(this.nombre_embarcacion)) {
        this.errorMessage +=
          'El campo "Nombre" debe comenzar con una mayúscula, seguir con letras y espacios, y tener entre 4 y 100 caracteres.\n';
      }

      if (this.tipo_embarcacion === 'buque' && !imo_regex.test(this.imo)) {
        this.errorMessage += 'El campo "IMO" debe comenzar con 3 letras seguidas de 7 dígitos.\n';
      }

      if (this.errorMessage) {
        Swal.fire({
          icon: 'error',
          title: 'Error de validación',
          text: this.errorMessage,
        });
        return false; // Detener el envío del formulario
      }

      return true; // El formulario es válido
    },

    async getNationalities() {
      try {
        const response = await axios.get('/api/paises/');
        this.nationalities = response.data.results;
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

  // Asignar valores por defecto según el tipo de embarcación
  const data = {
    nombre_embarcacion: this.nombre_embarcacion,
    nacionalidad: this.nacionalidad, // Asegúrate de que sea un ID válido
    eslora: parseFloat(this.eslora), // Convertir a número
    manga: parseFloat(this.manga), // Convertir a número
    calado_maximo: parseFloat(this.calado_maximo), // Convertir a número
    desplazamiento_maximo: parseFloat(this.desplazamiento_maximo), // Convertir a número
    tipo_embarcacion: this.tipo_embarcacion,
    tipo_buque: this.tipo_embarcacion === 'buque' ? this.tipo_buque : null,
    tipo_patana: this.tipo_embarcacion === 'patana' ? this.tipo_patana : null,
    imo: this.tipo_embarcacion === 'buque' ? this.imo : null, // No enviar 'imo' si no es un buque
    potencia: this.tipo_embarcacion === 'remolcador' ? parseFloat(this.potencia) : null, // Convertir a número
  };
  console.log('Datos enviados:', data); // Verificar los datos antes de enviar

  try {
    //enviar una solicitud POST para crear un nuevo registro
    await axios.post('/api/embarcaciones/', data);
    Swal.fire('Agregado!', 'La embarcación ha sido añadida exitosamente.', 'success');
    this.$router.push('/Embarcaciones');
  } catch (error) {
    console.error('Error al agregar la embarcación:', error);
    let errorMessage = 'Hubo un error al agregar la embarcación.';
    if (error.response && error.response.data) {
      errorMessage += ` Detalles: ${JSON.stringify(error.response.data)}`;
    }
    Swal.fire('Error', errorMessage, 'error');
  }
}
  },
};
</script>