<template>
  <div class="form-container">
    <h2>Adicionar Vagón Cargado/Descargado</h2>
    <form @submit.prevent="saveVagon">
      <!-- Tipo de Origen -->
      <div class="form-group">
        <label for="tipo_origen">Tipo de Origen:</label>
        <select id="tipo_origen" v-model="tipo_origen" @change="handleTipoOrigenChange" required>
          <option v-for="tipo in tipo_origen_options" :value="tipo.value" :key="tipo.value">
            {{ tipo.text }}
          </option>
        </select>
      </div>

      <!-- Origen -->
      <div class="form-group">
        <label for="origen">Origen:</label>
        <select id="origen" v-model="origen" required>
          <option v-for="item in origen_options" :value="item.nombre" :key="item.id">
            {{ item.nombre }}
          </option>
        </select>
      </div>

      <!-- Tipo de Equipo Ferroviario -->
      <div class="form-group">
        <label for="tipo_equipo_ferroviario">Tipo de Equipo Ferroviario:</label>
        <select id="tipo_equipo_ferroviario" v-model="tipo_equipo_ferroviario" required>
          <option v-for="equipo in tipo_equipo_ferroviario_options" :value="equipo.id" :key="equipo.id">
            {{ equipo.tipo_equipo_name }} - {{ equipo.descripcion }}
          </option>
        </select>
      </div>

      <!-- Estado -->
      <div class="form-group">
        <label for="estado">Estado:</label>
        <select id="estado" v-model="estado" @change="handleEstadoChange" required>
          <option v-for="estado in estado_options" :value="estado.value" :key="estado.value">
            {{ estado.text }}
          </option>
        </select>
      </div>

      <!-- Operación -->
      <div class="form-group">
        <label for="operacion">Operación:</label>
        <select id="operacion" v-model="operacion" required :disabled="true">
          <option>{{ operacion }}</option>
        </select>
      </div>

      <!-- Plan Diario de Carga/Descarga -->
      <div class="form-group">
        <label for="plan_diario_carga_descarga">Plan Diario:</label>
        <input id="plan_diario_carga_descarga" type="number" v-model="plan_diario_carga_descarga" required />
      </div>

      <!-- Tipo de Destino -->
      <div class="form-group">
        <label for="tipo_destino">Tipo de destino:</label>
        <select id="tipo_destino" v-model="tipo_destino" @change="handleTipoDestinoChange" required>
          <option v-for="tipo in tipo_destino_options" :value="tipo.value" :key="tipo.value">
            {{ tipo.text }}
          </option>
        </select>
      </div>

      <!-- Destino -->
      <div class="form-group">
        <label for="destino">Destino:</label>
        <select id="destino" v-model="destino" required>
          <option v-for="item in destino_options" :value="item.nombre" :key="item.id">
            {{ item.nombre }}
          </option>
        </select>
      </div>

      <!-- Causas de Incumplimiento -->
      <div class="form-group">
        <label for="causas_incumplimiento">Causas de Incumplimiento:</label>
        <textarea id="causas_incumplimiento" v-model="causas_incumplimiento"></textarea>
      </div>

      <!-- Producto -->
      <div class="form-group">
        <label for="producto">Producto:</label>
        <select id="producto" v-model="producto" :disabled="estado !== 'cargado'" required>
          <option v-for="producto in producto_options" :value="producto.id" :key="producto.id">
            {{ producto.producto_name }}
          </option>
        </select>
      </div>

      <!-- Botones -->
      <div class="form-buttons">
        <button type="button">
          <router-link style="color:white;text-decoration:none" to="/vagones_cargados_descargados">Cancelar</router-link>
        </button>
        <button type="submit">Aceptar</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
  name: 'AdicionarVagonCargadoDescargadoView',
  data() {
    return {
      tipo_origen: '',
      origen: '',
      origen_options: [], // Opciones dinámicas para el campo "origen" 
      destino_options: [], // Opciones dinámicas para el campo "destino"
      tipo_equipo_ferroviario: '',
      estado: '',
      operacion: 'Carga', // Valor inicial de operación
      plan_diario_carga_descarga: '',
      tipo_destino: '',
      destino: '',
      causas_incumplimiento: '',
      producto: '',
      tipo_origen_options: [
        { value: 'puerto', text: 'Puerto' },
        { value: 'ac_ccd', text: 'Acceso comercial/CCD' },
      ],
      tipo_equipo_ferroviario_options: [], // Se llenará con datos de la API
      estado_options: [
        { value: 'vacio', text: 'Vacío' },
        { value: 'cargado', text: 'Cargado' },
      ],
      operacion_options: [
        { value: 'carga', text: 'Carga' },
        { value: 'descarga', text: 'Descarga' },
      ],
      tipo_destino_options: [
        { value: 'puerto', text: 'Puerto' },
        { value: 'ac_ccd', text: 'Acceso comercial/CCD' },
      ],
      producto_options: [], // Se llenará con datos de la API
    };
  },
  mounted() {
    this.getTipoEquipoFerroviarioOptions();
    this.getProductoOptions();
  },
  methods: {
    // Obtener opciones de tipo de equipo ferroviario
    async getTipoEquipoFerroviarioOptions() {
      try {
        const response = await axios.get('/api/tipo-e-f-no-locomotora/');
        this.tipo_equipo_ferroviario_options = response.data;
      } catch (error) {
        console.error('Error al obtener tipos de equipo ferroviario:', error);
        Swal.fire('Error', 'Hubo un error al obtener los tipos de equipo ferroviario.', 'error');
      }
    },

    validateForm() {           
            const causas_incumplimiento_regex = /^[A-Z][\w\d\W]{2,398}$/
            let valid = true;
            let errorMessage = '';
            
            if (!causas_incumplimiento_regex.test(this.causas_incumplimiento)) {
              errorMessage += 'El campo causas del incumplimiento comienza con mayúscula,. Tamaño mínimo 3 caracteres y tamaño máximo 399 caracteres.<br>';
              valid = false;
            }

            // Validar que no sea el mismo origen y destino
            if (this.origen === this.destino) {
              errorMessage += 'Los campos origen y destino no pueden tener el mismo valor.<br>';
              valid = false;             
              
            }

            // Validar el campo producto si el estado es "cargado"
            if (this.estado === 'cargado' && !this.producto) {
              errorMessage += 'El campo producto es obligatorio cuando el estado es "cargado".<br>';
              valid = false;
            }

            if (errorMessage) {
              Swal.fire({
                icon: 'error',
                title: 'Error de validación',
                html: errorMessage,
              });
              return false; // Detener el envío del formulario
            }


            return valid;
          },

    // Obtener opciones de productos
    async getProductoOptions() {
      try {
        const response = await axios.get('/ufc/productos-vagones-cargados-descargados/');
        this.producto_options = response.data;
      } catch (error) {
        console.error('Error al obtener los productos de vagones:', error);
        Swal.fire('Error', 'Hubo un error al obtener los productos.', 'error');
      }
    },

    // Manejar el cambio en el campo "tipo_origen"
    async handleTipoOrigenChange() {
      if (this.tipo_origen === 'puerto') {
        // Obtener la lista de puertos
        try {
          const response = await axios.get('/api/puertos/');
          this.origen_options = response.data.map(puerto => ({
            id: puerto.id,
            nombre: puerto.nombre_puerto,
          }));
        } catch (error) {
          console.error('Error al obtener los puertos:', error);
          Swal.fire('Error', 'Hubo un error al obtener los puertos.', 'error');
        }
      } else if (this.tipo_origen === 'ac_ccd') {
        // Obtener la lista de entidades con tipo "Acceso comercial" o "CCD"
        try {
          const response = await axios.get('/api/entidades-acceso-ccd/');
          this.origen_options = response.data.map(entidad => ({
            id: entidad.id,
            nombre: entidad.nombre,
          }));
        } catch (error) {
          console.error('Error al obtener las entidades:', error);
          Swal.fire('Error', 'Hubo un error al obtener las entidades.', 'error');
        }
      } else {
        this.origen_options = []; // Limpiar opciones si no se selecciona un tipo válido
      }
    },

    // Manejar el cambio en el campo "tipo_destino"
    async handleTipoDestinoChange() {
      if (this.tipo_destino === 'puerto') {
        // Obtener la lista de puertos
        try {
          const response = await axios.get('/api/puertos/');
          this.destino_options = response.data.map(puerto => ({
            id: puerto.id,
            nombre: puerto.nombre_puerto,
          }));
        } catch (error) {
          console.error('Error al obtener los puertos:', error);
          Swal.fire('Error', 'Hubo un error al obtener los puertos.', 'error');
        }
      } else if (this.tipo_destino === 'ac_ccd') {
        // Obtener la lista de entidades con tipo "Acceso comercial" o "CCD"
        try {
          const response = await axios.get('/api/entidades-acceso-ccd/');
          this.destino_options = response.data.map(entidad => ({
            id: entidad.id,
            nombre: entidad.nombre,
          }));
        } catch (error) {
          console.error('Error al obtener las entidades:', error);
          Swal.fire('Error', 'Hubo un error al obtener las entidades.', 'error');
        }
      } else {
        this.origen_destino_options = []; // Limpiar opciones si no se selecciona un tipo válido
      }
    },
    

    // Manejar el cambio en el campo "estado"
    handleEstadoChange() {
      if (this.estado === 'vacio') {
        this.operacion = 'Carga'; // Si el estado es "vacio", la operación es "Carga"
      } else if (this.estado === 'cargado') {
        this.operacion = 'Descarga'; // Si el estado es "cargado", la operación es "Descarga"
      }
    },

    // Guardar el vagón
    async saveVagon() {
  if (!this.validateForm()) {
    return; // Detener el envío si la validación falla
  }

  // Asegúrate de que `operacion` tenga un valor
  if (!this.operacion) {
    Swal.fire('Error', 'El campo operación es obligatorio.', 'error');
    return;
  }
  console.log('Operación antes de enviar:', this.operacion); // Depuración

  const data = {
    tipo_origen: this.tipo_origen,
    origen: this.origen,
    tipo_equipo_ferroviario: this.tipo_equipo_ferroviario,
    estado: this.estado,
    operacion: this.operacion,
    plan_diario_carga_descarga: this.plan_diario_carga_descarga,
    tipo_destino: this.tipo_destino,
    destino: this.destino,
    causas_incumplimiento: this.causas_incumplimiento,
    producto: this.producto || null, // Enviar null si el producto está vacío
  };

  try {
    const response = await axios.post('/ufc/vagones-cargados-descargados/', data);
    Swal.fire('Agregado!', 'El vagón ha sido añadido exitosamente.', 'success');
    this.$router.push('/vagones_cargados_descargados');
  } catch (error) {
    console.error('Error al agregar el vagón:', error);

    // Mostrar el mensaje de error del backend
    let errorMessage = 'Hubo un error al agregar el vagón.';
    if (error.response && error.response.data) {
      errorMessage += ` Detalles: ${JSON.stringify(error.response.data)}`;
    }

    Swal.fire('Error', errorMessage, 'error');
  }
}
  },
};
</script>


<style scoped>
/* Estilos similares al componente anterior */
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
select,
textarea {
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