<template>
  <div>
    <div style="background-color: #002a68; color: white; text-align: right">
      <h6>Bienvenido:</h6>
    </div>
    <br />
    <Navbar-Component />
    <div class="form-container" style="margin-left: 18em; width: 75%">
      <h3 style="color: #002a68">Adicionar Tipo de Estructura de Ubicación</h3>
      <form @submit.prevent="createTipoEstructuraUbicacion">
        <div class="form-row">
          <div class="mb-3">
            <label for="nombre_tipo_estructura_ubicacion" class="form-label"
              >Nombre:<span style="color: red">*</span></label
            >
            <input
              type="text"
              class="form-control"
              id="nombre_tipo_estructura_ubicacion"
              v-model="nombre_tipo_estructura_ubicacion"
              required
            />
          </div>
        </div>

        <div class="form-buttons">
          <button
            type="button"
            @click="confirmCancel"
            style="color: white; text-decoration: none"
          >
            Cancelar
          </button>
          <button type="submit">Aceptar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
body {
  background-color: #f2f2f2;
}

.form-container {
  max-width: 600px;
  margin: 20px;
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
  padding: 1px 0px;
  height: 25px;
  font-size: 14px;
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
  padding: 6px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  font-size: 14px;
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
  name: "CrearTipoEstructuraUbicacionView",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      nombre_tipo_estructura_ubicacion: "", // Campo para el nombre del tipo de estructura de ubicación
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
    // Validar el formulario
    validateForm() {
      const nombre_tipo_estructura_ubicacion_regex = /^[A-Z][a-zA-Záéíóe ]{4,99}$/; // Ajustado para mínimo 5 caracteres

      if (!nombre_tipo_estructura_ubicacion_regex.test(this.nombre_tipo_estructura_ubicacion)) {
        Swal.fire({
          icon: "error",
          title: "Error en el nombre",
          text: "El nombre debe comenzar con mayúscula, aceptar letras minúsculas y espacios. Tamaño mínimo: 5 caracteres. Tamaño máximo: 100 caracteres.",
        });
        return false;
      }

      return true;
    },

    // Crear un tipo de estructura de ubicación
    async createTipoEstructuraUbicacion() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      const payload = {
        nombre_tipo_estructura_ubicacion: this.nombre_tipo_estructura_ubicacion,
      };

      try {
        await axios.post("/api/tipos_estructuras_ubicacion/", payload);
        Swal.fire("Creado!", "El tipo de estructura de ubicación ha sido creado exitosamente.", "success");
        this.$router.push("/TipoEstructuraUbicacion"); // Redirigir a la lista de tipos de estructura de ubicación
      } catch (error) {
        console.error("Error al crear el tipo de estructura de ubicación:", error);
        Swal.fire("Error", "Hubo un error al crear el tipo de estructura de ubicación.", "error");
      }
    },
  },
};
</script>