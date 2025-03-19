<template>
  <div>
    <Navbar-Component />
    
    <div class="form-container">
      <h3 style="color: #002A68;">Editar Cargo <strong>{{ cargo.nombre_cargo }}</strong></h3>
      <form @submit.prevent="submitForm">
        <!-- Campo Nombre del Cargo -->
        <div class="mb-3">
          <label for="nombre_cargo" class="form-label">Nombre:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="nombre_cargo" v-model="cargo.nombre_cargo" required />
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
  components: {
    NavbarComponent,
  },
  name: "EditarCargoView",
  data() {
    return {
      cargo: {
        nombre_cargo: "",
      },
    };
  },
  mounted() {
    this.get_cargo();
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
    async get_cargo() {
      this.$store.commit("setIsLoading", true);
      const cargo_id = this.$route.params.id;
      try {
        const response = await axios.get(`/api/cargos/${cargo_id}/`);
        this.cargo = response.data;
      } catch (error) {
        console.error("Error al obtener el cargo:", error);
      }
      this.$store.commit("setIsLoading", false);
    },

    async submitForm() {
      this.$store.commit("setIsLoading", true);
      const cargo_id = this.$route.params.id;
      try {
        const response = await axios.patch(`/api/cargos/${cargo_id}/`, this.cargo);
        this.cargo = response.data;
        this.$router.push("/Cargos");
        Swal.fire(
          "Actualizado!",
          "El cargo ha sido modificado exitosamente.",
          "success"
        );
      } catch (error) {
        console.error("Error al actualizar el cargo:", error);
      }
      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>

