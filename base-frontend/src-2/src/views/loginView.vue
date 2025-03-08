<template>
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
        style="position: relative; padding-top: 3em; margin-right: 44em"
        src="../assets/Imagenes/logo.png"
      />
  
      <form
        @submit.prevent="submitForm"
        style="margin-top: 2em; position: absolute"
        class="row row-cols-lg-auto g-3 align-items-center"
      >
        <div style="margin-left: 2em;" class="col-12">
          <label class="visually-hidden" for="inlineFormInputGroupUsername">Nombre de usuario</label>
          <div class="input-group">
            <div class="input-group-text">
              <i class="bi bi-person"></i> <!-- Ícono de persona de Bootstrap Icons (person.svg) -->
            </div>
            <input
              type="text"
              class="form-control"
              id="inlineFormInputGroupUsername"
              placeholder="Usuario"
              v-model="username"
              required
            />
          </div>
        </div>
  
        <div style="margin-left: 2.69em; font-size: 12px;" class="col-12">
          <label class="visually-hidden" for="inlineFormInputGroupPassword">Contraseña</label>
          <div class="input-group">
            <div class="input-group-text">
              <i class="bi bi-lock"></i> <!-- Ícono de candado de Bootstrap Icons (lock.svg) -->
            </div>
            <input
              type="password"
              class="form-control"
              id="inlineFormInputGroupPassword"
              style="font-size: 14px;"
              placeholder="Por favor, escriba su contraseña"
              v-model="password"
              required
            />
          </div>
        </div>
  
        <div style="margin-left: 5em;" class="justify-content-end">
          <button
            style="margin-left: 3.7em; width: 80%; font-size: 14px; margin-top: 1em"
            class="btn btn-primary me-md-2 justify-content-end"
            type="submit"
          >
          Iniciar Sesi&oacute;n  <i class="bi bi-shield-lock"></i>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

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
    };
  },

  methods: {
    async submitForm() {
      this.$store.commit("setIsLoading", true);
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
        this.$store.commit("setToken", token);
        axios.defaults.headers.common["Authorization"] = "Token " + token;
        localStorage.setItem("token", token);
        localStorage.setItem("username", username);

        // Obtener el ID del usuario desde el backend
        const userResponse = await axios.get("/api/v1/users/me/");
        localStorage.setItem("userid", userResponse.data.id);

        console.log('ID del usuario:', userResponse.data.id); // Verificar el ID
        this.$router.push("/home");
      } catch (error) {
        this.$store.commit("setIsLoading", false);
        if (error.response && error.response.status === 400) {
          Swal.fire('Error', 'Usuario o contraseña incorrectos.', 'error');
        } else if (error.message) {
          Swal.fire('Error', 'Algo salió mal. Inténtelo de nuevo.', 'error');
        }
      } finally {
        this.$store.commit("setIsLoading", false);
      }
    },
  },
};
</script>
  