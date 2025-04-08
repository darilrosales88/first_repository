<template>
  <div class="form-container">
    <h2>Editar Tipo de Estructura de Ubicación</h2>
    <form @submit.prevent="updateTipoEstructuraUbicacion">
      <div class="form-group">
        <label for="nombre">Nombre*:</label>
        <input type="text" id="nombre" v-model="nombre_tipo_estructura_ubicacion" required />
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
  font-family: "Franklin Gothic Medium", "Arial Narrow", Arial, sans-serif;
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
  name: "EditarTipoEstructuraUbicacionView",

  data() {
    return {
      nombre_tipo_estructura_ubicacion: "", // Campo para el nombre del tipo de estructura de ubicación
    };
  },

  mounted() {
    this.getTipoEstructuraUbicacion(); // Obtener el registro al cargar el componente
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
    // Obtener el tipo de estructura de ubicación por su ID
    async getTipoEstructuraUbicacion() {
      const tipoEstructuraId = this.$route.params.id; // Obtener el ID de la URL
      try {
        const response = await axios.get(`/api/tipos_estructuras_ubicacion/${tipoEstructuraId}/`);
        this.nombre_tipo_estructura_ubicacion = response.data.nombre_tipo_estructura_ubicacion; // Rellenar el campo
      } catch (error) {
        console.error("Error al obtener el tipo de estructura de ubicación:", error);
        Swal.fire("Error", "No se pudo cargar el tipo de estructura de ubicación.", "error");
      }
    },

    // Validar el formulario
    validateForm() {
      const nombre_tipo_estructura_ubicacion_regex = /^[A-Z][a-zA-ZáéíóúÁÉÍÓÚñÑ ]{4,99}$/; // Ajustado para mínimo 5 caracteres

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

    // Actualizar un tipo de estructura de ubicación
    async updateTipoEstructuraUbicacion() {
      // Validar el formulario antes de enviarlo
      if (!this.validateForm()) {
        return; // Si la validación falla, no enviar el formulario
      }

      const tipoEstructuraId = this.$route.params.id; // Obtener el ID de la URL
      const payload = {
        nombre_tipo_estructura_ubicacion: this.nombre_tipo_estructura_ubicacion,
      };

      try {
        await axios.patch(`/api/tipos_estructuras_ubicacion/${tipoEstructuraId}/`, payload);
        Swal.fire("Actualizado!", "El tipo de estructura de ubicación ha sido actualizado exitosamente.", "success");
        this.$router.push("/TipoEstructuraUbicacion"); // Redirigir a la lista de tipos de estructura de ubicación
      } catch (error) {
        console.error("Error al actualizar el tipo de estructura de ubicación:", error);
        Swal.fire("Error", "Hubo un error al actualizar el tipo de estructura de ubicación.", "error");
      }
    },
  },
};
</script>