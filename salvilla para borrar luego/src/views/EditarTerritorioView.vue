<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container" style="margin-left: 18em; width: 75%">
      <h3 style="color: #002A68;">Editar territorio</h3>
      <form @submit.prevent="updateItem" class="form-grid">
        <!-- Campo Nombre -->
        <div class="mb-3">
          <label for="nombre" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre" v-model="nombre_territorio" required />
        </div>

        <!-- Campo Abreviatura -->
        <div class="mb-3">
          <label for="abreviatura" class="form-label">Abreviatura:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="abreviatura" v-model="abreviatura" required />
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
  max-width: 600px; /* Ancho reducido */
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
</style>

<script>
import Swal from 'sweetalert2';
import axios from 'axios';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  components: {
    NavbarComponent,
  },
  data() {
    return {
      id: this.$route.params.id, // ID del territorio a editar
      nombre_territorio: '',
      abreviatura: '',
      errores:''
    };
  },

  mounted() {
    this.fetchItem();
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
    async fetchItem() {
      try {
        const response = await axios.get(`/api/territorios/${this.id}/`);
        this.nombre_territorio = response.data.nombre_territorio;
        this.abreviatura = response.data.abreviatura;
      } catch (error) {
        console.error('Error al obtener los datos del territorio:', error);
        Swal.fire('Error', 'Hubo un error al obtener los datos del territorio.', 'error');
      }
    },

    validateForm() {
      const nombre_territorio_regex = /^[A-Z][\w\d\W]{2,99}$/;
      const abreviatura_regex = /^[\d\w\W\s]{3,20}$/;
      let valid = true;
      this.errores='';

      if (!nombre_territorio_regex.test(this.nombre_territorio)) {
        this.errores += 'El campo Nombre comienza con mayúscula, acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y tamaño máximo 100 caracteres.<br>';
        valid = false;
      }

      if (!abreviatura_regex.test(this.abreviatura)) {
        this.errores += 'El campo Abreviatura acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y tamaño máximo 20 caracteres.<br>';
        valid = false;
      }
      

      return valid;
    },

    async updateItem() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        Swal.fire('Errores en la entrada de datos', this.errores, 'error');
        return; // Si la validación falla, no enviar el formulario
      }

      this.$store.commit('setIsLoading', true);

      const territorio = {
        nombre_territorio: this.nombre_territorio,
        abreviatura: this.abreviatura
      };

      try {
        await axios.put(`/api/territorios/${this.id}/`, territorio);
        this.$router.push('/Territorio');
        Swal.fire('Actualizado!', 'El territorio ha sido actualizado exitosamente.', 'success');
      } catch (error) {
        console.error('Error al actualizar el territorio:', error);
        Swal.fire('Error', 'Hubo un error al actualizar el territorio.', 'error');
      }

      this.$store.commit('setIsLoading', false);
    }
  }
};
</script>