<template>
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
  <div class="container d-flex flex-column align-items-center justify-content-center">
    <img
      style="position: relative; margin-top: 3em"
      class="img-fluid mb-4"
      src="../assets/Imagenes/logo.png"
      alt="Logo"
    />

    <form
      @submit.prevent="submitForm"
      class="row row-cols-lg-auto g-3 align-items-center w-100"
    >
      <div class="col-12">
        <label class="visually-hidden" for="inlineFormInputGroupUsername">Username</label>
        <div class="input-group">
          <div class="input-group-text">@</div>
          <input
            type="text"
            class="form-control"
            id="inlineFormInputGroupUsername"
            placeholder="Username"
            v-model="username"
            required
          />
        </div>
      </div>

      <div class="col-12">
        <label class="visually-hidden" for="inlineFormInputGroupPassword">Password</label>
        <div class="input-group">
          <input
            type="password"
            class="form-control"
            id="inlineFormInputGroupPassword"
            placeholder="Please write your password"
            v-model="password"
            required
          />
        </div>
      </div>

      <div class="col-12 d-flex justify-content-center">
        <button
          style="position: absolute; width: 15%; margin-top: 2em"
          class="btn btn-primary me-md-2"
          type="submit"
        >
          Loguearse <i class="bi bi-shield-lock"></i>
        </button>
      </div>
    </form>
    <br />
    <br />
    <br />
    <br />
    <div v-if="loginError" class="alert alert-danger mt-3" role="alert">
      {{ loginError }}
    </div>

    <!-- Pantalla de carga -->
    <div v-if="isLoading" class="loading-screen">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
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
  margin-left: auto;
  margin-right: auto;
  max-width: 600px;
  padding: 0 15px;
  text-align: center;
}

.container form {
  width: 100%;
}

.loading-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.8);
  z-index: 9999;
}

@media (max-width: 768px) {
  .container img {
    margin-right: 0;
    margin-bottom: 1em;
  }

  .container form {
    position: relative;
  }
}
</style>

<script>
import axios from "axios";
export default {
  name: "LoginView",
  data() {
    return {
      username: "",
      password: "",
      errors: [],
      loginError: "",
      isLoading: false, // Añade esta propiedad
    };
  },

  methods: {
    async submitForm() {
      this.isLoading = true; // Muestra la pantalla de carga
      axios.defaults.headers.common["Authorization"] = "";
      localStorage.removeItem("token");

      const formData = {
        username: this.username,
        password: this.password,
      };

      await axios
        .post("/api/v1/token/login/", formData)
        .then((response) => {
          const token = response.data.auth_token;
          const role = response.data.role;

          this.$store.commit("setToken", token);

          axios.defaults.headers.common["Authorization"] = "Token " + token;

          localStorage.setItem("token", token);
          console.log(role);

          this.$router.push("/home");
        })
        .catch((error) => {
          if (error.response) {
            this.loginError = "Usuario o contraseña incorrectos."; // Actualiza el mensaje de error
            for (const property in error.response.data) {
              this.errors.push(`${property}: ${error.response.data[property]}`);
            }
          } else if (error.message) {
            this.loginError = "Algo salió mal. Inténtelo de nuevo."; // Actualiza el mensaje de error
            this.errors.push("Algo salió mal. Inténtelo de nuevo.");
          }
        });
      this.isLoading = false; // Oculta la pantalla de carga
    },
  },
};
</script>
