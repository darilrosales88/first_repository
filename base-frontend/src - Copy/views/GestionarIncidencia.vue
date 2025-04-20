<template>
  <div class="form-container">
    <h2>Editar incidencia</h2>
    <form @submit.prevent="saveItem">
      <div class="form-group">
        <label for="latitud">Código:</label>
        <input type="text" id="latitud" v-model="codigo_incidencia" />
      </div>
      <div class="form-group">
        <label for="nombre">Nombre*:</label>
        <input type="text" id="nombre" v-model="nombre_incidencia" required />
      </div>
      <div class="form-group">
        <label for="pais">Imputable:</label>
        <select id="imputable" v-model="tipo_imputable" required>
          <option v-for="item in options" :key="item.value" :value="item.value">
            {{ item.text }}
          </option>
        </select>
      </div>
      <div class="form-buttons">
        <button type="button">
          <router-link style="color: white; text-decoration: none" to="/Incidencias"
            >Cancelar</router-link
          >
        </button>
        <button type="submit">Aceptar</button>
      </div>
    </form>
  </div>
</template>

<style>
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
import Swal from "sweetalert2";
import axios from "axios";

export default {
  data() {
    return {
      nombre_incidencia: "",
      codigo_incidencia: "",
      tipo_imputable: "",
      options: [
        { value: "imputables_buque", text: "Imputables al buque" },
        { value: "imputables_puerto", text: "Imputable al puerto" },
        { value: "imputables_receptor", text: "Imputable al receptor" },
        { value: "imputables_otras_causas", text: "Imputable a otras causas" },
        { value: "imputables_imp_exp", text: "Imputable a; importador / exportador" },
        {
          value: "imputables_aut_portuarias",
          text: "Imputables a las autoridades portuarias",
        },
      ],
    };
  },

  mounted() {
    this.getIncidencias();
    
  },

  methods: {

    getIncidencias() {
      const incidencia_id = this.$route.params.id;
      axios
        .get(`http://127.0.0.1:8000/api/incidencias/${incidencia_id}/`)
        .then((response) => {
          console.log('Datos de la incidencia:', response.data); // Verifica los datos
          this.nombre_incidencia = response.data.nombre_incidencia;
          this.codigo_incidencia = response.data.codigo_incidencia;
          this.tipo_imputable = response.data.tipo_imputable;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    async saveItem() {
      this.$store.commit("setIsLoading", true);
      const incidencia_id = this.$route.params.id; // Asegúrate de que estás obteniendo el ID correcto

      const payload = {
        nombre_incidencia: this.nombre_incidencia,
        codigo_incidencia: this.codigo_incidencia,
        tipo_imputable: this.tipo_imputable,
      };

      console.log('Payload enviado:', payload); // Verifica el payload

      axios
        .patch(`http://127.0.0.1:8000/api/incidencias/${incidencia_id}/`, payload)
        .then((response) => {
          Swal.fire(
            "Actualizado!",
            "La incidencia ha sido actualizada exitosamente.",
            "success"
          );
          this.$router.push("/Incidencias");
        })
        .catch((error) => {
          console.log(error);
        });
      this.$store.commit("setIsLoading", false);
    },
  },
};
</script>