<template>
  <div class="form-container">
    <h2>Editar producto {{ producto.nombre_producto }}</h2>
    <form @submit.prevent="submitForm">

  <div class="form-group">
    <label for="codigo_producto">Código:</label>
    <input style="padding: 3px;" type="text" v-model="producto.codigo_producto" required />    
    <p v-if="codigo_producto_error" class="help is-danger">{{ codigo_producto_error }}</p>
  </div>

  <div class="form-group">
    <label for="nombre">Nombre:</label>
    <input style="padding: 3px;" type="text" v-model="producto.nombre_producto" required />    
    <p v-if="nombre_producto_error" class="help is-danger">{{ nombre_producto_error }}</p>
  </div>

  <div class="form-group">
    <label for="tipo_producto">Tipo de producto:</label>
    <select style="padding: 5px;" v-model="producto.tipo_producto" required>
      <option v-for="t_producto in t_producto_options" :value="t_producto.value" :key="t_producto.value">
        {{ t_producto.text }}
      </option>
    </select>
  </div>

  <div class="form-group">
    <label for="nombre_producto">Descripción:</label>
    <input style="padding: 3px;" type="text" v-model="producto.descripcion" required />    
    <p v-if="descripcion_error" class="help is-danger">{{ descripcion_error }}</p>
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
    max-width: 300px;
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
    text-align: left;
    display: flex;
    width: 260px;
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
    display: flex;
    justify-content: end;
    font-size: 15px;
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
  name: 'EditarProductoView',

  data() {
    return {      
      producto: {}, 
      
      nombre_producto_error: null, // Para la validación del campo
      codigo_producto_error: null, // Para la validación del campo
      descripcion_error: null, // Para la validación del campo
      t_producto_options: [
        { value: 'alimento', text: 'Alimento' },
        { value: 'combustible', text: 'Combustible'},
        { value: 'otros', text: 'Otros' },
      ],      
    };
  },

  mounted() {
    this.get_producto();
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
            const nombre_producto_regex = /^[\w\d\W ]{3,100}$/;
            const codigo_producto_regex = /^[\w\d\W ]{3,20}$/;
            const descripcion_regex = /^[A-Z][\w\d\W]{2,399}$/;
            
            let valid = true;
            
            if (!nombre_producto_regex.test(this.producto.nombre_producto)) {
              this.nombre_producto_error = 'Este campo acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y tamaño máximo 100 caracteres.';
              valid = false;
            } else {
              this.nombre_producto_error = null;
            }

            if (!codigo_producto_regex.test(this.producto.codigo_producto)) {
              this.codigo_producto_error = 'Este campo acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y tamaño máximo 20 caracteres.';
              valid = false;
            } else {
              this.codigo_producto_error = null;
            }

            if (!descripcion_regex.test(this.producto.descripcion)) {
              this.descripcion_error = 'Este campo comienza con 3 letras seguido de 7 dígitos.';
              valid = false;
            } else {
              this.descripcion_error = null;
            }

            return valid;
          },
    
    async get_producto() {
      this.$store.commit('setIsLoading', true);
      const producto_id = this.$route.params.id;
      try {
        const response = await axios.get(`/api/productos/${producto_id}/`);
        this.producto = response.data;        
        console.log('Datos del producto:', this.producto);
      } catch (error) {
        console.log(error);
      }
      this.$store.commit('setIsLoading', false);
    },

    /* Función para enviar los datos al servidor */
    async submitForm() {
          if (!this.validateForm()) {
            return;
          }

          this.$store.commit('setIsLoading', true);
          const producto_id = this.$route.params.id;

          try {
            // Envía this.producto en lugar de data
            await axios.patch(`/api/productos/${producto_id}/`, this.producto);
            this.$router.push('/Producto');
            Swal.fire('Actualizado!', 'El producto ha sido modificado exitosamente.', 'success');
          } catch (error) {
            console.error('Error al actualizar el producto:', error);
            Swal.fire('Error', 'Hubo un error al actualizar el producto.', 'error');
          } finally {
            this.$store.commit('setIsLoading', false);
          }
        }        
  }
};
  </script>
