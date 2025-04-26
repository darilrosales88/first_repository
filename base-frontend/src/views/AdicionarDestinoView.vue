<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container">
      <h2>Adicionar Destino:</h2>
      <form @submit.prevent="createDestino">
        <div class="form-row">
          <div class="mb-3">
            <label for="cliente" class="form-label">Cliente:<span style="color: red;">*</span></label>
            <select class="form-control" id="cliente" v-model="cliente" required>
              <option value="">-Seleccione-</option>
              <option v-for="item in clienteOptions" :key="item.id" :value="item.id">
                {{ item.nombre }}
              </option>
            </select>
          </div>

          <div class="mb-3">
            <label for="destino" class="form-label">Destino:<span style="color: red;">*</span></label>
            <input type="text" class="form-control" id="destino" v-model="destino" required />
          </div>
        </div>

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

h2 {
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

.form-row {
  display: flex;
  flex-direction: row;
  gap: 15px;
}

.mb-3 {
  width: 200px; /* Ajuste para que ocupe el ancho completo */
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
import axios from "axios";
import Swal from "sweetalert2";
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: "CrearDestinoView",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      cliente: "",
      clienteOptions: [],
      destino: "",
      errores:''
    };
  },

  mounted() {
    this.getClientes(); // Obtener la lista de clientes
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
      this.errores='';
      const destino_regex = /^[A-Z]{1}[\d\w\W ]{2,99}$/;
      
      let valid = true;

      if (this.cliente === "") {
        this.errores += 'Debe seleccionar un cliente.<br>';
        valid = false;
      }

      if (!destino_regex.test(this.destino)) {
       this.errores += 'El destino debe comenzar con mayúscula seguido de letras, números y caracteres especiales. Tamaño mínimo: 3 caracteres. Tamaño máximo: 100 caracteres.';
        valid = false;
      }

      return valid;
    },

    async getClientes() {
      try {
        const response = await axios.get('/api/entidades/');
        this.clienteOptions = response.data.results;
      } catch (error) {
        console.error('Error al obtener los clientes:', error);
      }
    },

    async createDestino() {
      if (!this.validateForm()) {
        Swal.fire('Errores en la entrada de datos', this.errores, 'error');
        return; // Si la validación falla, no enviar el formulario
      }

      const payload = {
        cliente: this.cliente,
        destino: this.destino
      };

      try {
        await axios.post("/api/destinos/", payload);
        Swal.fire("Creado!", "El destino ha sido creado exitosamente.", "success");
        this.$router.push("/Destino");
      } catch (error) {
        console.error("Error al crear el destino:", error);
        Swal.fire("Error", "Hubo un error al crear el destino.", "error");
      }
    }
  }
};
</script>