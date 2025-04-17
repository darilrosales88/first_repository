<template>
    <div class="form-container">
      <h2>Editar Incidencia</h2>
      <form @submit.prevent="update_incidencia">
        <div class="form-group">
          <label for="codigo_incidencia">Código de Incidencia</label>
          <input type="text" v-model="codigo_incidencia" required />
        </div>
  
        <div class="form-group">
          <label for="nombre_incidencia">Nombre</label>
          <input type="text" v-model="nombre_incidencia" required />
        </div>
  
        <div class="form-group">
          <label for="tipo_imputable">Tipo Imputable</label>
          <select v-model="tipo_imputable" required>
            <option value="-">-</option>
            <option value="imputables_buque">Imputables al buque</option>
            <option value="imputables_puerto">Imputables al puerto</option>
            <option value="imputables_receptor">Imputables al receptor</option>
            <option value="imputables_otras_causas">Imputables a otras causas</option>
            <option value="imputables_imp_exp">Imputables al importador / exportador</option>
            <option value="imputables_aut_portuarias">Imputables a las autoridades portuarias</option>
          </select>
        </div>
  
        <div class="form-buttons">
          <button type="button">
            <router-link style="color:white;text-decoration:none" to="/Incidencias">Cancelar</router-link>
          </button>
          <button type="submit">Actualizar</button>
        </div>
      </form>
    </div>
  </template>
  
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
  select {
    flex: 2;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    color: #000;
    background-color: #fff;
  }
  
  select option {
    color: #000;
    background-color: #fff;
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
    background-color: #28a745;
    color: white;
  }
  </style>
  
  <script>
  import axios from 'axios';
  import Swal from 'sweetalert2';
  
  export default {
    name: 'EditarIncidencia',
    data() {
      return {
        codigo_incidencia: '',
        nombre_incidencia: '',
        tipo_imputable: '-',
      };
    },
    mounted() {
      this.getIncidencia();
    },
    methods: {
      // Obtener el registro existente por su ID
      async getIncidencia() {
        const id = this.$route.params.id; // Obtener el ID de la URL
        try {
          const response = await axios.get(`/api/incidencias/${id}/`);
          const data = response.data;
          this.codigo_incidencia = data.codigo_incidencia;
          this.nombre_incidencia = data.nombre_incidencia;
          this.tipo_imputable = data.tipo_imputable;
        } catch (error) {
          console.error('Error al obtener la incidencia:', error);
          Swal.fire('Error', 'No se pudo cargar el registro para editar.', 'error');
        }
      },
  
      // Validar el formulario
      validateForm() {
        const codigo_incidencia_regex = /^[\w\d\W ]{2,5}$/;
        const nombre_incidencia_regex = /^[\w\d\W ]{3,100}$/;
  
        if (!codigo_incidencia_regex.test(this.codigo_incidencia)) {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'El código de incidencia acepta letras, números y caracteres especiales. Tamaño mínimo 2 caracteres y máximo 5 caracteres.',
          });
          return false;
        }
  
        if (!nombre_incidencia_regex.test(this.nombre_incidencia)) {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'El nombre acepta letras, números y caracteres especiales. Tamaño mínimo 3 caracteres y máximo 100 caracteres.',
          });
          return false;
        }
  
        return true;
      },
  
      // Actualizar el registro
      async update_incidencia() {
        // Validar el formulario antes de enviarlo
        if (!this.validateForm()) {
          return; // Si la validación falla, no enviar el formulario
        }
  
        const id = this.$route.params.id; // Obtener el ID de la URL
        const data = {
          codigo_incidencia: this.codigo_incidencia,
          nombre_incidencia: this.nombre_incidencia,
          tipo_imputable: this.tipo_imputable,
        };
  
        try {
          await axios.put(`/api/incidencias/${id}/`, data);
          Swal.fire('Actualizado!', 'La incidencia ha sido actualizada exitosamente.', 'success');
          this.$router.push('/Incidencias');
        } catch (error) {
          console.log(error);
          Swal.fire('Error', 'Hubo un error al actualizar la incidencia.', 'error');
        }
      },
    },
  };
  </script>