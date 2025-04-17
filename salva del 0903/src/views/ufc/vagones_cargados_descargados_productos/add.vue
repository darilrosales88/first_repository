<template>
  <div class="form-container">
    <h2>Adicionar Producto de Vagón Cargado/Descargado</h2>
    <form @submit.prevent="saveProductoVagon">
      <!-- Tipo de Producto -->
      <div class="form-group">
        <label for="tipo_producto">Tipo de Producto:</label>
        <select v-model="tipo_producto" @change="handleTipoProductoChange" required>
          <option v-for="tipo in tipo_producto_options" :value="tipo.value" :key="tipo.value">
            {{ tipo.text }}
          </option>
        </select>
      </div>

      <!-- Producto -->
      <div class="form-group">
        <label for="producto">Producto:</label>
        <select v-model="producto" required>
          <option v-for="prod in producto_options" :value="prod.id" :key="prod.id">
            {{ prod.nombre_producto }}
          </option>
        </select>
      </div>

      <!-- Tipo de Embalaje -->
      <div class="form-group">
        <label for="tipo_embalaje">Tipo de Embalaje:</label>
        <select v-model="tipo_embalaje" required>
          <option v-for="embalaje in tipo_embalaje_options" :value="embalaje.id" :key="embalaje.id">
            {{ embalaje.nombre_tipo_embalaje }}
          </option>
        </select>
      </div>

      <!-- Unidad de Medida -->
      <div class="form-group">
        <label for="unidad_medida">Unidad de Medida:</label>
        <select v-model="unidad_medida" required>
          <option v-for="unidad in unidad_medida_options" :value="unidad.id" :key="unidad.id">
            {{ unidad.unidad_medida }}
          </option>
        </select>
      </div>

      <!-- Cantidad -->
      <div class="form-group">
        <label for="cantidad">Cantidad:</label>
        <input type="number" v-model="cantidad" min="0" step="1" required />
      </div>

      <!-- Estado -->
      <div class="form-group">
        <label for="estado">Estado:</label>
        <select v-model="estado" :disabled="tipo_producto !== 'contenedor'" @change="handleEstadoChange">
          <option v-for="estado in estado_options" :value="estado.value" :key="estado.value">
            {{ estado.text }}
          </option>
        </select>
      </div>

      <!-- Contiene -->
      <div class="form-group">
        <label for="contiene">Contiene:</label>
        <select v-model="contiene" :disabled="estado !== 'lleno'">
          <option v-for="cont in contiene_options" :value="cont.value" :key="cont.value">
            {{ cont.text }}
          </option>
        </select>
      </div>

      <!-- Botones -->
      <div class="form-buttons">
        <button type="button">
          <router-link style="color:white;text-decoration:none" to="/productos_vagones_cargados_descargados">Cancelar</router-link>
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
  name: 'AdicionarProductoVagonView',
  data() {
    return {
      tipo_producto: '',
      producto: '',
      tipo_embalaje: '',
      unidad_medida: '',
      cantidad: '',
      estado: '',
      contiene: '',
      tipo_producto_options: [
        { value: 'producto', text: 'Producto' },
        { value: 'contenedor', text: 'Contenedor' },
      ],
      producto_options: [], // Se llenará con datos de la API
      tipo_embalaje_options: [], // Se llenará con datos de la API
      unidad_medida_options: [], // Se llenará con datos de la API
      estado_options: [
        { value: 'vacio', text: 'Vacío' },
        { value: 'lleno', text: 'Lleno' },
      ],
      contiene_options: [
        { value: 'alimentos', text: 'Alimentos' },
        { value: 'productos_varios', text: 'Productos varios' },
      ],
    };
  },
  mounted() {
    this.getProductoOptions();
    this.getTipoEmbalajeOptions();
    this.getUnidadMedidaOptions();
  },
  methods: {
    // Obtener opciones de productos
    async getProductoOptions() {
      try {
        const response = await axios.get('/api/productos/');
        this.producto_options = response.data;
      } catch (error) {
        console.error('Error al obtener los productos:', error);
        Swal.fire('Error', 'Hubo un error al obtener los productos.', 'error');
      }
    },

    // Obtener opciones de tipo de embalaje
    async getTipoEmbalajeOptions() {
      try {
        const response = await axios.get('/api/embalajes/');
        this.tipo_embalaje_options = response.data;
      } catch (error) {
        console.error('Error al obtener los tipos de embalaje:', error);
        Swal.fire('Error', 'Hubo un error al obtener los tipos de embalaje.', 'error');
      }
    },

    // Obtener opciones de unidad de medida
    async getUnidadMedidaOptions() {
      try {
        const response = await axios.get('/api/unidades_medida/');
        this.unidad_medida_options = response.data;
      } catch (error) {
        console.error('Error al obtener las unidades de medida:', error);
        Swal.fire('Error', 'Hubo un error al obtener las unidades de medida.', 'error');
      }
    },

    // Manejar el cambio en el campo "tipo_producto"
    handleTipoProductoChange() {
      if (this.tipo_producto !== 'contenedor') {
        this.estado = ''; // Limpiar el campo estado si no es un contenedor
      }
    },

    // Manejar el cambio en el campo "estado"
    handleEstadoChange() {
      if (this.estado !== 'lleno') {
        this.contiene = ''; // Limpiar el campo contiene si el estado no es "lleno"
      }
    },

    // Guardar el producto de vagón
    async saveProductoVagon() {
      const data = {
        tipo_producto: this.tipo_producto,
        producto: this.producto,
        tipo_embalaje: this.tipo_embalaje,
        unidad_medida: this.unidad_medida,
        cantidad: this.cantidad,
        estado: this.estado,
        contiene: this.contiene,
      };

      try {
        await axios.post('/ufc/productos-vagones-cargados-descargados/', data);
        Swal.fire('Agregado!', 'El producto de vagón ha sido añadido exitosamente.', 'success');
        this.$router.push('/productos_vagones_cargados_descargados');
      } catch (error) {
        console.error('Error al agregar el producto:', error);
        Swal.fire('Error', 'Hubo un error al agregar el producto.', 'error');
      }
    },
  },
};
</script>
  
  <style scoped>
  /* Estilos sin cambios */
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