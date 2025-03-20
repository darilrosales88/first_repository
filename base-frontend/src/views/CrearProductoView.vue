<template>
  <div class="form-container">
    <h2>Adicionar producto</h2>
    <form @submit.prevent="save_producto">
      <!-- Campo Código -->
      <div class="form-group">
        <label for="codigo_producto">Código:</label>
        <input
          style="padding: 3px"
          type="text"
          v-model="codigo_producto"
          step="0.01"
          required
        />
      </div>

      <!-- Campo Nombre -->
      <div class="form-group">
        <label for="nombre_producto"
          >Nombre:<span style="color: red">*</span></label
        >
        <input
          style="padding: 3px"
          type="text"
          v-model="nombre_producto"
          step="0.01"
          required
        />
      </div>

      <!-- Campo Tipo de Producto -->
      <div class="form-group">
        <label for="tipo_producto"
          >Tipo de producto:<span style="color: red">*</span></label
        >
        <select style="padding: 5px" v-model="tipo_producto" required>
          <option
            v-for="t_producto in t_producto_options"
            :value="t_producto.value"
            :key="t_producto.value"
          >
            {{ t_producto.text }}
          </option>
        </select>
      </div>

      <!-- Campo Descripción -->
      <div class="form-group">
        <label for="descripcion">Descripción:</label>
        <input
          style="padding: 3px"
          type="textarea"
          v-model="descripcion"
          step="0.01"
          required
        />
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
        <button>Aceptar</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
body {
  background-color: #f2f2f2;
}

.form-container {
  max-width: 680px; /* Ajusta el ancho máximo del contenedor */
  margin: 20px; /* Centra el formulario */
  padding: 20px;
  margin-left: 220px;
  border-radius: 8px;
  background-color: rgb(245, 245, 245);
}

h2 {
  font-family: "Franklin Gothic Medium", "Arial Narrow", Arial, sans-serif;
  text-align: left;
  margin-bottom: 20px;
  font-size: 18px;
}

.form-label {
  font-size: 14px;
  text-align: left;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 2 columnas de igual tamaño */
  gap: 15px; /* Espacio entre los elementos */
}

.mb-3 {
  width: 200px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 14px;
}

label {
  font-weight: bold;
}

input,
select {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 2px;
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
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "CrearProductoView",
  data() {
    return {
      codigo_producto: "",
      nombre_producto: "",
      descripcion: "",
      tipo_producto: "",
      t_producto_options: [
        { value: "alimento", text: "Alimento" },
        { value: "combustible", text: "Combustible" },
        { value: "otros", text: "Otros" },
      ],
    };
  },
  methods: {
    confirmCancel() {
      Swal.fire({
        title: "¿Está seguro de que quiere cancelar la operación?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        cancelmButtonText: "Cancelar",
        confirmButtonText: "Aceptar",
      }).then((result) => {
        if (result.isConfirmed) {
          window.history.back();
        }
      });
    },
    validateForm() {
      const codigo_producto_regex = /^[\w\d\W ]{3,20}$/;
      const nombre_producto_regex = /^[A-Z][\w\d\W ]{3,100}$/;
      const descripcion_regex = /^[A-Z][\w\d\W]{2,399}$/;

      if (!codigo_producto_regex.test(this.codigo_producto)) {
        Swal.fire(
          "Error",
          "El código debe tener entre 3 y 20 caracteres y puede incluir letras, números y caracteres especiales.",
          "error"
        );
        return false;
      }

      if (!nombre_producto_regex.test(this.nombre_producto)) {
        Swal.fire(
          "Error",
          "El nombre debe comenzar con mayúscula, tener entre 3 y 100 caracteres y puede incluir letras, números y caracteres especiales.",
          "error"
        );
        return false;
      }

      if (!descripcion_regex.test(this.descripcion)) {
        Swal.fire(
          "Error",
          "La descripción debe comenzar con mayúscula, tener entre 2 y 399 caracteres y puede incluir letras, números y caracteres especiales.",
          "error"
        );
        return false;
      }

      return true;
    },
    async save_producto() {
      this.$store.commit("setIsLoading", true);

      const producto = {
        codigo_producto: this.codigo_producto,
        nombre_producto: this.nombre_producto,
        tipo_producto: this.tipo_producto,
        descripcion: this.descripcion,
      };

      try {
        await axios.post("/api/productos/", producto);
        this.$router.go(-1);
        Swal.fire(
          "Agregado!",
          "El producto ha sido insertado exitosamente.",
          "success"
        );
      } catch (error) {
        console.error("Error al insertar el producto:", error);
        Swal.fire("Error", "Hubo un error al insertar el producto.", "error");
      }

      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>
