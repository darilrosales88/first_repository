<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container">
      <h3 style="color: #002A68;">Editar país</h3>
      <form @submit.prevent="saveItem" class="form-grid">
        <!-- Campo Nacionalidad -->
        <div class="mb-3">
          <label for="nacionalidad" class="form-label">Nacionalidad:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nacionalidad" v-model="nacionalidad" required />
        </div>

        <!-- Campo País -->
        <div class="mb-3">
          <label for="nombre_pais" class="form-label">País:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre_pais" v-model="nombre_pais" required />
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
      nacionalidad: '',
      nombre_pais: '',
    };
  },
  mounted() {
    this.getPais();
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
    async getPais() {
      const pais_id = this.$route.params.id;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/paises/${pais_id}/`);
        const pais = response.data;
        this.nacionalidad = pais.nacionalidad;
        this.nombre_pais = pais.nombre_pais;
      } catch (error) {
        console.error("Error al obtener el país:", error);
      }
    },
    async saveItem() {
      const pais_id = this.$route.params.id;
      const payload = {
        nacionalidad: this.nacionalidad,
        nombre_pais: this.nombre_pais,
      };
      try {
        await axios.patch(`http://127.0.0.1:8000/api/paises/${pais_id}/`, payload);
        Swal.fire("Actualizado!", "El país ha sido actualizado exitosamente.", "success");
        this.$router.push("/Paises");
      } catch (error) {
        console.error("Error al actualizar el país:", error);
        Swal.fire("Error", "Hubo un error al actualizar el país.", "error");
      }
    },
  }
};
</script>
