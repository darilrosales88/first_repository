<template>
  <div>
    <div style="background-color: #002a68; color: white; text-align: right">
      <h6>Bienvenido:</h6>
    </div>
    <br />
    <Navbar-Component />

    <div class="form-container" style="margin-left: 18em; width: 75%">
      <h3 style="color: #002a68">Editar Tipo de Estructura de Ubicación</h3>
      <form @submit.prevent="updateTipoEstructuraUbicacion">
        <div class="form-row">
          <!-- Campo Nombre -->
          <div class="mb-3">
            <label for="nombre" class="form-label"
              >Nombre:<span style="color: red">*</span></label
            >
            <input
              type="text"
              class="form-control"
              id="nombre"
              v-model="nombre_tipo_estructura_ubicacion"
              required
            />
          </div>
        </div>

        <!-- Botones -->
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
  name: "EditarTipoEstructuraUbicacionView",
  components: {
    NavbarComponent,
  },
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