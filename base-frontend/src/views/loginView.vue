<template>
  <div class="login-container">
    <!-- Pantalla de carga -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>Iniciando sesión...</p>
    </div>
    
    <!-- Fondo animado (original) -->
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

    <!-- Logo fuera del formulario -->
    <div class="logo-container">
      <img src="../assets/Imagenes/logo.png" alt="Logo de la empresa" class="logo">
    </div>

    <!-- Formulario profesional -->
    <div class="login-card">
      <div class="card-header">
        <h2>Bienvenido</h2>
        <p>Ingrese sus credenciales para continuar</p>
      </div>
      
      <form @submit.prevent="submitForm" class="login-form">
        <div class="form-group">
          <label for="username" class="form-label">
            <i class="bi bi-person-circle"></i> Usuario
          </label>
          <div class="input-container">
            <input
              type="text"
              id="username"
              class="form-input"
              placeholder="Ingrese su usuario"
              v-model="username"
              required
              :disabled="isLoading"
            >
            <div class="input-border"></div>
          </div>
        </div>
        
        <div class="form-group">
          <label for="password" class="form-label">
            <i class="bi bi-shield-lock"></i> Contraseña
          </label>
          <div class="input-container">
            <input
              type="password"
              id="password"
              class="form-input"
              placeholder="Ingrese su contraseña"
              v-model="password"
              required
              :disabled="isLoading"
            >
            <div class="input-border"></div>
          </div>
        </div>
        
        <button type="submit" class="login-btn" :disabled="isLoading">
          <span v-if="!isLoading">
            <i class="bi bi-box-arrow-in-right"></i> Iniciar Sesión
          </span>
          <span v-else>
            <i class="bi bi-arrow-repeat spinner"></i> Autenticando...
          </span>
          <span class="btn-pulse"></span>
        </button>
      </form>

      <div class="card-footer">
        <p>¿Olvidaste la contraseña? 
          <router-link 
            :to="{ name: 'RecuperarContrasena' }" 
            class="help-link"
            @click.native="testLink"
          >
            Haga click aquí
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

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
      isLoading: false,
    };
  },
  methods: {

    testLink() {
    console.log('Router link clicked');
    console.log('Current route:', this.$route);
    console.log('Router instance:', this.$router);
    this.$router.push({ name: 'RecuperarContrasena' }).catch(err => {
      console.error('Navigation error:', err);
    });
  },


    async submitForm() {
      this.isLoading = true;
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

        localStorage.setItem("token", token);
        localStorage.setItem("username", username);
        axios.defaults.headers.common["Authorization"] = "Token " + token;

        const userResponse = await axios.get("/api/v1/users/me/");
        localStorage.setItem("userid", userResponse.data.id);

        this.$router.push("/home");
      } catch (error) {
        if (error.response && error.response.status === 400) {
          Swal.fire({
            title: 'Acceso denegado',
            text: 'Usuario o contraseña incorrectos',
            icon: 'error',
            confirmButtonColor: '#4e73df',
            background: '#fff',
            backdrop: `
              rgba(0,0,123,0.4)
              url("/images/nyan-cat.gif")
              left top
              no-repeat
            `
          });
        } else {
          Swal.fire({
            title: 'Error de conexión',
            text: 'No se pudo conectar al servidor. Intente nuevamente.',
            icon: 'error',
            confirmButtonColor: '#4e73df'
          });
        }
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>

/* Variables */
:root {
  --primary-color: #002a68;
  --accent-color: #4e73df;
  --light-accent: #6699ff;
  --text-color: #2d3748;
  --light-text: #718096;
  --border-color: #e2e8f0;
  --card-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* Estructura principal */
.login-container {
  position: relative;
  width: 100%;
  min-height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* Fondo animado (conservado igual) */
svg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  display: block;
  background-color: rgb(0, 71, 163);
  z-index: 0;
}

/* Logo superior */
.logo-container {
  position: relative;
  z-index: 2;
  margin-bottom: 20px;
  text-align: center;
}

.logo {
  height: 80px;
  width: auto;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

/* Tarjeta de login */
.login-card {
  position: relative;
  width: 380px;
  background: white;
  border-radius: 12px;
  box-shadow: var(--card-shadow);
  overflow: hidden;
  z-index: 1;
  margin-bottom: 30px;
}

.card-header {
  padding: 25px 30px 15px;
  text-align: center;
  background: linear-gradient(135deg, #f6f9fc 0%, #eef2f6 100%);
  border-bottom: 1px solid var(--border-color);
}

.card-header h2 {
  color: var(--primary-color);
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 5px;
}

.card-header p {
  color: var(--light-text);
  font-size: 0.9rem;
  margin: 0;
}

/* Formulario */
.login-form {
  padding: 25px 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  color: var(--text-color);
  font-size: 0.85rem;
  font-weight: 500;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
}

.form-label i {
  margin-right: 8px;
  color: var(--accent-color);
  font-size: 1.1rem;
}

.input-container {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 12px 15px;
  font-size: 0.95rem;
  color: var(--text-color);
  background: #fff;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  transition: all 0.3s ease;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);
}

.form-input:focus {
  border-color: var(--accent-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(78, 115, 223, 0.15);
}

.input-border {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--accent-color);
  transition: width 0.3s ease;
}

.form-input:focus ~ .input-border {
  width: 100%;
}

/* Botón de login */

.login-btn {
  width: 100%;
  padding: 14px;
  margin-top: 15px;
  background: #002a68; /* Color azul oscuro */
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 42, 104, 0.3);
  z-index: 1;
}

.login-btn:hover {
  background: #0047a3; /* Color azul más claro al hover */
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 42, 104, 0.4);
}

.login-btn:active {
  transform: translateY(1px);
  box-shadow: 0 2px 4px rgba(0, 42, 104, 0.3);
}

.login-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    45deg,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0.3) 50%,
    rgba(255, 255, 255, 0.1) 100%
  );
  transform: translateX(-100%);
  transition: transform 0.6s ease;
  z-index: -1;
}

.login-btn:hover::before {
  transform: translateX(100%);
}

.btn-pulse {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background: rgba(255, 255, 255, 0.2);
  opacity: 0;
  border-radius: 8px;
}

.login-btn:focus:not(:active) .btn-pulse {
  animation: pulse 1s ease-out;
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    opacity: 0.7;
  }
  100% {
    transform: scale(1.05);
    opacity: 0;
  }
}

.login-btn:disabled {
  background: #a0aec0;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

.login-btn:disabled::before {
  display: none;
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}


/* Footer de la tarjeta */
.card-footer {
  padding: 15px 30px;
  text-align: center;
  background: #f8fafc;
  border-top: 1px solid var(--border-color);
  font-size: 0.85rem;
  color: var(--light-text);
}

.help-link {
  color: var(--accent-color);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.help-link:hover {
  color: var(--primary-color);
  text-decoration: underline;
}

/* Pantalla de carga */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.85);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-spinner {
  border: 4px solid rgba(78, 115, 223, 0.1);
  border-radius: 50%;
  border-top: 4px solid var(--accent-color);
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

.loading-overlay p {
  margin-top: 15px;
  color: var(--text-color);
  font-weight: 500;
}

/* Responsive */
@media (max-width: 480px) {
  .login-card {
    width: 90%;
    max-width: 380px;
  }
  
  .logo {
    height: 70px;
  }
  
  .card-header, .login-form, .card-footer {
    padding-left: 20px;
    padding-right: 20px;
  }
}
</style>