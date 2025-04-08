<template>
    <div class="form-container">
      <h2>Adicionar pais</h2>
      <form @submit.prevent="saveItem">
        <div class="form-group">
          <label for="nombre"> Nacionalidad:</label>
          <input type="text" v-model="nacionalidad" required />
        </div>
  
        <div class="form-group">
          <label for="nombre"> Pais:</label>
          <input type="text" v-model="nombre_pais" required />
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
  select {
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
  
<script>
  import Swal from 'sweetalert2';
  import axios from 'axios';
  
  export default {
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