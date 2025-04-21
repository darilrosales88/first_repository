<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container">
      <h3 style="color: #002A68;">Editar Entidad</h3>
      <form @submit.prevent="updateItem" class="form-grid">
        <!-- Campo Nombre -->
        <div class="mb-3">
          <label for="nombre" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre" v-model="nombre" required />
        </div>

        <!-- Campo Abreviatura -->
        <div class="mb-3">
          <label for="abreviatura" class="form-label">Abreviatura:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="abreviatura" v-model="abreviatura" required />
        </div>

        <!-- Campo Código REEUP -->
        <div class="mb-3">
          <label for="codigo_reeup" class="form-label">Código REEUP:</label>
          <input type="text" class="form-control" id="codigo_reeup" v-model="codigo_reeup" />
        </div>

        <!-- Campo OSDE/OACE u organismo -->
        <div class="mb-3">
          <label for="osde_oace_organismo" class="form-label">OSDE/OACE u organismo:<span style="color: red;">*</span></label>
          <select class="form-control" id="osde_oace_organismo" v-model="osde_oace_organismo" required>
            <option v-for="item in osdeOaceOrganismoOptions" :key="item.id" :value="item.id">{{ item.nombre }}</option>
          </select>
        </div>

        <!-- Campo Provincia -->
        <div class="mb-3">
          <label for="provincia" class="form-label">Provincia:<span style="color: red;">*</span></label>
          <select class="form-control" id="provincia" v-model="provincia" required>
            <option v-for="item in provinciaOptions" :key="item.id" :value="item.id">{{ item.nombre_provincia }}</option>
          </select>
        </div>

        <!-- Campo Tipo de entidad -->
        <div class="mb-3">
          <label for="tipo_entidad" class="form-label">Tipo de entidad:<span style="color: red;">*</span></label>
          <select class="form-control" id="tipo_entidad" v-model="tipo_entidad" required>
            <option v-for="option in tipoEntidadOptions" :key="option.value" :value="option.value">{{ option.text }}</option>
          </select>
        </div>

        <!-- Campo Territorio -->
        <div class="mb-3">
          <label for="territorio" class="form-label">Territorio:</label>
          <select class="form-control" id="territorio" v-model="territorio">
            <option v-for="item in territoriosOptions" :key="item.id" :value="item.id">{{ item.nombre_territorio }}</option>
          </select>
        </div>

        <!-- Botones -->
        <div class="form-buttons">
          <button type="button" @click="confirmCancel" style="color:white;text-decoration:none">Cancelar</button>
          <button type="submit">Actualizar</button>
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
  grid-template-columns: repeat(3, 1fr); /* 3 columnas de igual tamaño */
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
  margin-top: 20px;
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
import axios from 'axios';
import Swal from 'sweetalert2';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'EditarEntidadView',
  components: {
    NavbarComponent,
  },

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
      codigo_reeup: '',
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
    this.loadEntidadData();
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
        this.osdeOaceOrganismoOptions = response.data.results;
      } catch (error) {
        console.error('Error al obtener los OSDE/OACE organismos:', error);
      }
    },

    async getProvincias() {
      try {
        const response = await axios.get('/api/provincias/');
        this.provinciaOptions = response.data.results;
      } catch (error) {
        console.error('Error al obtener las provincias:', error);
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

    async getTerritorios() {
      try {
        const response = await axios.get('/api/territorios/');
        this.territoriosOptions = response.data.results;
      } catch (error) {
        console.error('Error al obtener los territorios:', error);
      }
    },

    async loadEntidadData() {
      const entidadId = this.$route.params.id;
      try {
        const response = await axios.get(`/api/entidades/${entidadId}/`);
        const entidad = response.data;
        this.nombre = entidad.nombre;
        this.abreviatura = entidad.abreviatura;
        this.codigo_reeup = entidad.codigo_reeup;
        this.osde_oace_organismo = entidad.osde_oace_organismo;
        this.provincia = entidad.provincia;
        this.territorio = entidad.territorio;
        this.tipo_entidad = entidad.tipo_entidad;
      } catch (error) {
        console.error('Error al cargar los datos de la entidad:', error);
        Swal.fire('Error', 'No se pudieron cargar los datos de la entidad.', 'error');
      }
    },

    async updateItem() {
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
        codigo_reeup: this.codigo_reeup,
        osde_oace_organismo: this.osde_oace_organismo,
        provincia: this.provincia,
        tipo_entidad: this.tipo_entidad,
        territorio: this.territorio,
      };

      const entidadId = this.$route.params.id;

      try {
        await axios.put(`/api/entidades/${entidadId}/`, data);
        Swal.fire('Actualizado!', 'La entidad ha sido actualizada exitosamente.', 'success');
        this.$router.push('/Entidades');
      } catch (error) {
        console.log(error);
        Swal.fire('Error', 'Hubo un error al actualizar la entidad.', 'error');
      }
    }
  }
};
</script>

