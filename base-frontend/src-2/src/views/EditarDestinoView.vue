<template>
  <div class="form-container">
    <h2>Editar Destino</h2>
    <form @submit.prevent="updateDestino">
      <div class="form-group">
        <label for="cliente">Cliente*:</label>
        <select id="cliente" v-model="cliente" required>
          <option value="">-Seleccione-</option>
          <option v-for="item in clienteOptions" :key="item.id" :value="item.id">
            {{ item.nombre }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="destino">Destino*:</label>
        <input type="text" id="destino" v-model="destino" required />
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
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "EditarDestinoView",

  data() {
    return {
      destinoId: this.$route.params.id,
      cliente: "",
      clienteOptions: [],
      destino: "",
      errores:''
    };
  },

  mounted() {
    this.getClientes(); // Obtener la lista de clientes
    this.getDestino(); // Obtener los datos del destino a editar
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
        this.clienteOptions = response.data;
      } catch (error) {
        console.error('Error al obtener los clientes:', error);
      }
    },

    async getDestino() {
      try {
        const response = await axios.get(`/api/destinos/${this.destinoId}/`);
        const destino = response.data;
        this.cliente = destino.cliente;
        this.destino = destino.destino;
      } catch (error) {
        console.error('Error al obtener el destino:', error);
        Swal.fire('Error', 'No se pudo cargar el destino.', 'error');
        this.$router.push('/Destino'); // Redirigir si hay un error
      }
    },

    async updateDestino() {
      if (!this.validateForm()) {
        Swal.fire('Errores en la entrada de datos', this.errores, 'error');
        return; // Si la validación falla, no enviar el formulario
      }

      const payload = {
        cliente: this.cliente,
        destino: this.destino
      };

      try {
        await axios.put(`/api/destinos/${this.destinoId}/`, payload);
        Swal.fire("Actualizado!", "El destino ha sido actualizado exitosamente.", "success");
        this.$router.push("/Destino");
      } catch (error) {
        console.error("Error al actualizar el destino:", error);
        Swal.fire("Error", "Hubo un error al actualizar el destino.", "error");
      }
    }
  }
};
</script>