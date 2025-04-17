<template>
<div>
    <!-- Pantalla de carga -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>Iniciando sesión...</p>
    </div>
  <div>
    <svg
      version="1.1"
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      x="0px"
      y="0px"
      width="100%"
      height="100%"
      viewBox="0 0 1600 900"
      preserveAspectRatio="xMidYMax slice"
    >
      <defs>
        <linearGradient id="bg">
          <stop offset="0%" style="stop-color: rgba(130, 158, 249, 0.06)"></stop>
          <stop offset="50%" style="stop-color: rgba(76, 190, 255, 0.6)"></stop>
          <stop offset="100%" style="stop-color: rgba(115, 209, 72, 0.2)"></stop>
        </linearGradient>
        <path
          id="wave"
          fill="url(#bg)"
          d="M-363.852,502.589c0,0,236.988-41.997,505.475,0
  s371.981,38.998,575.971,0s293.985-39.278,505.474,5.859s493.475,48.368,716.963-4.995v560.106H-363.852V502.589z"
        />
      </defs>
      <g>
        <use xlink:href="#wave" opacity=".3">
          <animateTransform
            attributeName="transform"
            attributeType="XML"
            type="translate"
            dur="10s"
            calcMode="spline"
            values="270 230; -334 180; 270 230"
            keyTimes="0; .5; 1"
            keySplines="0.42, 0, 0.58, 1.0;0.42, 0, 0.58, 1.0"
            repeatCount="indefinite"
          />
        </use>
        <use xlink:href="#wave" opacity=".6">
          <animateTransform
            attributeName="transform"
            attributeType="XML"
            type="translate"
            dur="8s"
            calcMode="spline"
            values="-270 230;243 220;-270 230"
            keyTimes="0; .6; 1"
            keySplines="0.42, 0, 0.58, 1.0;0.42, 0, 0.58, 1.0"
            repeatCount="indefinite"
          />
        </use>
        <use xlink:href="#wave" opacty=".9">
          <animateTransform
            attributeName="transform"
            attributeType="XML"
            type="translate"
            dur="6s"
            calcMode="spline"
            values="0 230;-140 200;0 230"
            keyTimes="0; .4; 1"
            keySplines="0.42, 0, 0.58, 1.0;0.42, 0, 0.58, 1.0"
            repeatCount="indefinite"
          />
        </use>
      </g>
    </svg>
    <div class="container">
      <img
        style="position: relative; padding-top: 3em; margin-right: 35em"
        src="../assets/Imagenes/logo.png"
      />
  
      <form
        @submit.prevent="submitForm"
        style="margin-top: 2em; position: absolute"
        class="row row-cols-lg-auto g-3 align-items-center"
      >
        <div style="margin-left: 5em; " class="responsive col-12">
          <label class="visually-hidden" for="inlineFormInputGroupUsername">Nombre de usuario</label>
          <div class="input-group">
            <div class="input-group-text">
              <i class="bi bi-person"></i>
            </div>
            <input
              type="text"
              class="form-control"
              id="inlineFormInputGroupUsername"
              style="width: 230px;"
              placeholder="Usuario"
              v-model="username"
              required
            />
          </div>
        </div>
  
        <div style="margin-left: 6.5em; font-size: 12px;" class="col-12">
          <label class="visually-hidden" for="inlineFormInputGroupPassword">Contraseña</label>
          <div class="input-group">
            <div class="input-group-text">
              <i class="bi bi-lock"></i>
            </div>
            <input
              type="password"
              class="form-control"
              id="inlineFormInputGroupPassword"
              style="font-size: 14px; width: 230px; "
              placeholder="Por favor, escriba su contraseña"
              v-model="password"
              required
            />
          </div>
        </div>
  
        <div style="margin-left: 7em;" class="justify-content-end">
          <button
            style="margin-left: 5.7em; width: 80%; font-size: 14px; margin-top: 1em"
            class="btn btn-primary me-md-2 justify-content-end"
            type="submit"
            :disabled="isLoading"
          >
            <span v-if="!isLoading">Iniciar Sesi&oacute;n  <i class="bi bi-shield-lock"></i></span>
            <span v-else>
              <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              Cargando...
            </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</div>
</template>

<style scoped>
/* Ajustes adicionales para pantallas pequeñas */
@media (max-width: 768px) {
  .container {
    padding: 0 15px;
  }

  .img-fluid {
    padding-top: 1em !important;
  }

  .input-group {
    margin-bottom: 1em;
   
  }

  

  .btn {
    width: 100%;
  }
}
</style>

<style scoped>
svg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  display: block;
  background-color: rgb(0, 71, 163);
}

.container {
  margin-top: 1em;
  margin-left: 25em;
}

.container form {
  width: 30%;
}


</style>
  
<script>
import axios from "axios";
import Swal from 'sweetalert2';

export default {
  name: "LoginView",
  data() {
    return {
      username: "",
      password: "",
      errors: [],
      isLoading: false, // Estado de carga local
    };
  },

  methods: {
    async submitForm() {
      this.isLoading = true; // Activar pantalla de carga
      axios.defaults.headers.common["Authorization"] = "";
      localStorage.removeItem("token");

      const formData = {
        username: this.username,
        password: this.password,
      };

      try {
        const response = await axios.post("/api/v1/token/login/", formData);
        const token = response.data.auth_token;
        const username = this.username;

        // Guardar el token y el nombre de usuario en localStorage
        localStorage.setItem("token", token);
        localStorage.setItem("username", username);
        axios.defaults.headers.common["Authorization"] = "Token " + token;

        // Obtener el ID del usuario desde el backend
        const userResponse = await axios.get("/api/v1/users/me/");
        localStorage.setItem("userid", userResponse.data.id);

        console.log('ID del usuario:', userResponse.data.id); // Verificar el ID
        this.$router.push("/home");
      } catch (error) {
        if (error.response && error.response.status === 400) {
          Swal.fire('Error', 'Usuario o contraseña incorrectos.', 'error');
        } else if (error.message) {
          Swal.fire('Error', 'Algo salió mal. Inténtelo de nuevo.', 'error');
        }
      } finally {
        this.isLoading = false; // Desactivar pantalla de carga
      }
    },
  },
};
</script>

  