<template>
  <div class="form-container">
    <h2>Crear Entidad</h2>
    <form @submit.prevent="saveItem">
      <div class="form-group">
        <label for="nombre">Nombre*:</label>
        <input type="text" v-model="nombre" required />
      </div>
      <div class="form-group">
        <label for="abreviatura">Abreviatura*:</label>
        <input type="text" v-model="abreviatura" required />
      </div>
      <div class="form-group">
        <label for="osde_oace_organismo">OSDE/OACE u organismo*:</label>
        <select id="osde_oace_organismo" v-model="osde_oace_organismo" required>
          <option v-for="item in osdeOaceOrganismoOptions" :key="item.id" :value="item.id">{{ item.nombre }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="provincia">Provincia*:</label>
        <select id="provincia" v-model="provincia" required>
          <option v-for="item in provinciaOptions" :key="item.id" :value="item.id">{{ item.nombre_provincia }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="tipo_entidad">Tipo de entidad*:</label>
        <select id="tipo_entidad" v-model="tipo_entidad" required>
          <option v-for="option in tipoEntidadOptions" :key="option.value" :value="option.value">{{ option.text }}</option>
        </select>
      </div>
      <div class="form-buttons">
        <button type="button" @click="confirmCancel" style="color:white;text-decoration:none">Cancelar</button>
        <button>Aceptar</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
  name: 'AdicionarEntidadView',

  data() {
    return {
      osdeOaceOrganismoOptions: [],
      provinciaOptions: [],
      tipoEntidadOptions: [
        { value: 'I', text: 'Importador' },
        { value: 'E', text: 'Exportador' },
        { value: 'T', text: 'Transportista' },
        { value: 'AC', text: 'Acceso comercial' },
        { value: 'CN', text: 'Compañía naviera' },
        { value: 'M', text: 'Mitrans' },
        { value: 'O', text: 'Otros' }
      ],
      nombre: '',
      abreviatura: '',
      osde_oace_organismo: '',
      provincia: '',
      tipo_entidad: '',
      nombre_error: null,
      abreviatura_error: null,
    };
  },

  mounted() {
    this.getOsdeOaceOrganismos();
    this.getProvincias();
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
      const nombre_regex = /^[A-Z][\w\d\W]{2,99}$/;
      const abreviatura_regex = /^[A-ZÁÉÍÓÚ]{1}[A-Za-zÁÉÍÓÚáéíóú\s]{2,19}$/;

      let valid = true;

      if (!nombre_regex.test(this.nombre)) {
        this.nombre_error = 'Este campo comienza con mayúscula, acepta letras, números y caracteres especiales. Tamaño mínimo 2 caracteres y tamaño máximo 100 caracteres.';
        Swal.fire({
          icon: 'error',
          title: 'Error en el nombre',
          text: this.nombre_error,
        });
        valid = false;
      } else {
        this.nombre_error = null;
      }

      if (!abreviatura_regex.test(this.abreviatura)) {
        this.abreviatura_error = 'Este campo comienza con mayúscula seguido de espacio o caracteres alfabéticos. Tamaño mínimo 3 caracteres y tamaño máximo 20 caracteres.';
        Swal.fire({
          icon: 'error',
          title: 'Error en la abreviatura',
          text: this.abreviatura_error,
        });
        valid = false;
      } else {
        this.abreviatura_error = null;
      }

      return valid;
    },

    async getOsdeOaceOrganismos() {
      try {
        const response = await axios.get('/api/osde/');
        this.osdeOaceOrganismoOptions = response.data;
      } catch (error) {
        console.error('Error al obtener los OSDE/OACE organismos:', error);
      }
    },

    async getProvincias() {
      try {
        const response = await axios.get('/api/provincias/');
        this.provinciaOptions = response.data;
      } catch (error) {
        console.error('Error al obtener las provincias:', error);
      }
    },

    async saveItem() {
      if (!this.validateForm()) {
        return;
      }

      const data = {
        nombre: this.nombre,
        abreviatura: this.abreviatura,
        osde_oace_organismo: this.osde_oace_organismo,
        provincia: this.provincia,
        tipo_entidad: this.tipo_entidad,
      };

      try {
        await axios.post('/api/entidades/', data);
        Swal.fire('Agregado!', 'La entidad ha sido añadida exitosamente.', 'success');
        this.$router.push('/Entidades');
      } catch (error) {
        console.log(error);
        Swal.fire('Error', 'Hubo un error al agregar la entidad.', 'error');
      }
    }
  }
};
</script>
  
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
    font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
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
  
  input,select {
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