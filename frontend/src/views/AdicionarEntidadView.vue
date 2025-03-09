<template>
  <div class="form-container">
    <h2>Crear Entidad</h2>
    <form @submit.prevent="saveItem" class="form-grid">
      <div class="form-group">
        <label for="nombre">Nombre:<span style="color: red;">*</span></label>
        <input type="text" style="padding: 3px;" v-model="nombre" required />
      </div>
      <div class="form-group">
        <label for="abreviatura">Abreviatura:<span style="color: red;">*</span></label>
        <input type="text" style="padding: 3px;" v-model="abreviatura" required />
      </div>
      <div class="form-group">
        <label for="codigo_reeup">Codigo REEUP:</label>
        <input type="text" style="padding: 3px;" v-model="codigo_reeup" />
      </div>
      <div class="form-group">
        <label for="osde_oace_organismo">OSDE/OACE u organismo:<span style="color: red;">*</span></label>
        <select id="osde_oace_organismo" style="padding: 5px;" v-model="osde_oace_organismo" required>
          <option v-for="item in osdeOaceOrganismoOptions" :key="item.id" :value="item.id">{{ item.nombre }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="provincia">Provincia:<span style="color: red;">*</span></label>
        <select id="provincia" style="padding: 5px;" v-model="provincia" required>
          <option v-for="item in provinciaOptions" :key="item.id" :value="item.id">{{ item.nombre_provincia }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="tipo_entidad">Tipo de entidad:<span style="color: red;">*</span></label>
        <select id="tipo_entidad" style="padding: 5px;" v-model="tipo_entidad" required>
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
      territoriosOptions: [],
      tipoEntidadOptions: [
        { value: 'importador', text: 'Importador' },
        { value: 'exportador', text: 'Exportador' },
        { value: 'transportista', text: 'Transportista' },
        { value: 'acceso_comercial', text: 'Acceso comercial' },
        { value: 'compania_naviera', text: 'Compañía naviera' },
        { value: 'mitrans', text: 'Mitrans' },
        { value: 'otros', text: 'Otros' }
      ],
      nombre: '',
      abreviatura: '',
      codigo_reeup:'',
      osde_oace_organismo: '',
      provincia: '',
      territorio: '',
      tipo_entidad: '',
      errores: null,
    };
  },

  mounted() {
    this.getOsdeOaceOrganismos();
    this.getProvincias();
    this.getTerritorios();
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
          this.errores = '';
          const nombre_regex = /^[A-Z][A-Za-zÁÉÍÓÚáéíóú ]{2,99}$/;
          const codigo_reeup_regex = /^[1-9][0-9]{4,10}$/;
          const abreviatura_regex = /^[A-ZÁÉÍÓÚ]{1}[A-Za-zÁÉÍÓÚáéíóú\s]{2,19}$/;

          let valid = true;

          // Validación del campo nombre
          if (!nombre_regex.test(this.nombre)) {
            this.errores += 'El campo nombre comienza con mayúscula, acepta letras y espacios. Tamaño mínimo 2 caracteres y tamaño máximo 100 caracteres.<br>';
            valid = false;
          }

          // Validación del campo abreviatura
          if (!abreviatura_regex.test(this.abreviatura)) {
            this.errores += 'El campo abreviatura comienza con mayúscula seguido de espacio o caracteres alfabéticos. Tamaño mínimo 3 caracteres y tamaño máximo 20 caracteres.<br>';
            valid = false;
          }

          // Validación del campo codigo_reeup (solo si no está vacío)
          if (this.codigo_reeup && !codigo_reeup_regex.test(this.codigo_reeup)) {
            this.errores += 'El campo código REEUP acepta entre 5 y 11 dígitos.<br>';
            valid = false;
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

    // Verificar si el codigo reeup ya existe
    async doesCodigoReeupExist() {
      try {
        const response = await axios.get("/api/entidades/verificar-existencia-reeup/", {
          params: {
            codigo_reeup: this.codigo_reeup,            
          },
        });
        return response.data.exists; // ese exists es la variable declarada en la funcion verificar_destino en el views.py
      } catch (error) {
        return false; // En caso de error, asumimos que no existe
        console.error("Error al verificar el código reeup:", error);
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

    async getTerritorios() {
      try {
        const response = await axios.get('/api/territorios/');
        this.territoriosOptions = response.data;
      } catch (error) {
        console.error('Error al obtener los territorios:', error);
      }
    },

    async saveItem() {
      if (!this.validateForm()) {
        Swal.fire('Errores en la entrada de datos', this.errores, 'error');
        return;
      }

      // Verificar si el destino ya existe
      if (await this.doesCodigoReeupExist()) {
        Swal.fire("Error", "El código REEUP proporcionado ya existe.", "error");
        return;
      }

      const data = {
        nombre: this.nombre,
        abreviatura: this.abreviatura,
        codigo_reeup:this.codigo_reeup,
        osde_oace_organismo: this.osde_oace_organismo,
        provincia: this.provincia,
        tipo_entidad: this.tipo_entidad,
        territorio:this.territorio
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
  max-width: 600px; /* Ajusta el ancho máximo del contenedor */
  margin: 50px; /* Centra el contenedor */
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

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 4 columnas de igual tamaño */
  gap: 15px; /* Espacio entre los elementos */
}

.form-group {
  text-align: left;
  width: 260px;
  display: flex;
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
  grid-column: span 2; /* Los botones ocupan las 4 columnas */
  display: flex;
  justify-content: end;
  font-size: 15px;
  margin-top: 20px;
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