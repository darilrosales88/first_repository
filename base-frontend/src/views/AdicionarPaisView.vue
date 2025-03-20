<template>
  <div>
    <Navbar-Component />
    
    <div class="form-container">
      <h3>Adicionar país:</h3>
      <form @submit.prevent="saveItem">
        <!-- Campo Nacionalidad -->
        <div class="form-row">
        <div class="mb-3">
          <label for="nacionalidad" class="form-label">Nacionalidad:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nacionalidad" v-model="nacionalidad" required />
        </div>

        <!-- Campo Nombre del País -->
        <div class="mb-3">
          <label for="nombre_pais" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre_pais" v-model="nombre_pais" required />
        </div>
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
  margin: 20px ; /* Centra el formulario */
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
.form-label{
  font-size: 14px;
  text-align: left;
}
form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-row {
  display: flex;
  flex-direction: row;
  gap: 15px;
}

.mb-3 {
  width: 200px;
  display: flex;
  flex-direction: column;
}

.form-control {
  padding: 1px 0px; /* Padding reducido */
  height: 25px; /* Altura reducida */
  font-size: 14px; /* Tamaño de fuente reducido */
  border: 1px solid #ccc;
  border-radius: 2px;
}

.form-buttons {
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
  
      async saveItem() {
        
        this.$store.commit('setIsLoading', true);
  
        const pais = {
            nacionalidad: this.nacionalidad,
            nombre_pais: this.nombre_pais
        };
  
        try {
          await axios.post('/api/paises/', pais);
          this.$router.push('/Paises');
          Swal.fire('Agregado!', 'El pais ha sido insertado exitosamente.', 'success');
        } catch (error) {
          console.error('Error al insertar el pais:', error);
          Swal.fire('Error', 'Hubo un error al insertar el pais.', 'error');
        }
  
        this.$store.commit('setIsLoading', false);
      }
    }
  };
</script>