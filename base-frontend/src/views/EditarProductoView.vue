<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container">
      <h3 style="color: #002A68;">Editar producto {{ producto.nombre_producto }}</h3>
      <form @submit.prevent="submitForm" class="form-grid">
        <!-- Campo Código del Producto -->
        <div class="mb-3">
          <label for="codigo_producto" class="form-label">Código:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="codigo_producto" v-model="producto.codigo_producto" required />
          <p v-if="codigo_producto_error" class="help is-danger">{{ codigo_producto_error }}</p>
        </div>

        <!-- Campo Nombre del Producto -->
        <div class="mb-3">
          <label for="nombre" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre" v-model="producto.nombre_producto" required />
          <p v-if="nombre_producto_error" class="help is-danger">{{ nombre_producto_error }}</p>
        </div>

        <!-- Campo Tipo de Producto -->
        <div class="mb-3">
          <label for="tipo_producto" class="form-label">Tipo de producto:<span style="color: red;">*</span></label>
          <select class="form-control" id="tipo_producto" v-model="producto.tipo_producto" required>
            <option v-for="t_producto in t_producto_options" :value="t_producto.value" :key="t_producto.value">
              {{ t_producto.text }}
            </option>
          </select>
        </div>

        <!-- Campo Descripción -->
        <div class="mb-3">
          <label for="descripcion" class="form-label">Descripción:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="descripcion" v-model="producto.descripcion" required />
          <p v-if="descripcion_error" class="help is-danger">{{ descripcion_error }}</p>
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
  max-width: 680px; /* Ancho reducido */
  margin: 20px; /* Centra el formulario */
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

.form-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 2 columnas de igual tamaño */
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
  color: #000; /* Asegura que el texto sea negro */
  background-color: #fff; /* Asegura que el fondo sea blanco */
}

select option {
  color: #000; /* Asegura que el texto de las opciones sea negro */
  background-color: #fff; /* Asegura que el fondo de las opciones sea blanco */
}

.form-buttons {
  grid-column: span 3; /* Los botones ocupan las 2 columnas */
  display: flex;
  justify-content: flex-end;
  font-size: 14px;
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

.help.is-danger {
  color: red;
  font-size: 12px;
  margin-top: 5px;
}
</style>

  <script>
  import axios from 'axios';
import Swal from 'sweetalert2';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'EditarProductoView',
  components: {
    NavbarComponent,
  },
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
        { value: 'contenedor', text: 'Contenedor' },
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
