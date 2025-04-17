<template>
    <div class="form-container">
      <h2>Editar país</h2>
      <form @submit.prevent="saveItem">
        <div class="form-group">
          <label for="nacionalidad">Nacionalidad:</label>
          <input type="text" v-model="nacionalidad" required />
        </div>
  
        <div class="form-group">
          <label for="nombre_pais">País:</label>
          <input type="text" v-model="nombre_pais" required />
        </div>
  
        <div class="form-buttons">
          <button type="button">
            <router-link style="color: white; text-decoration: none;" to="/Paises">Cancelar</router-link>
          </button>
          <button type="submit">Aceptar</button>
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
  mounted() {
    this.getPais();
  },
  methods: {
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
