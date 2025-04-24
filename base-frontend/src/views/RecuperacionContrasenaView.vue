<template>
  <div class="password-reset-container">
    <!-- Pantalla de carga -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>Actualizando contraseña...</p>
    </div>
    
    <!-- Fondo animado (idéntico al login) -->
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

    <!-- Logo superior -->
    <div class="logo-container">
      <img src="../assets/Imagenes/logo.png" alt="Logo de la empresa" class="logo">
    </div>

    <!-- Tarjeta de creación de nueva contraseña -->
    <div class="reset-card">
      <div class="card-header">
        <h2><i class="bi bi-shield-lock"></i> Crear Nueva Contraseña</h2>
        <p>Ingrese y confirme su nueva contraseña</p>
      </div>
      
      <form @submit.prevent="submitNewPassword" class="reset-form">
        <div class="form-group">
          <label for="newPassword" class="form-label">
            <i class="bi bi-key"></i> Nueva Contraseña
          </label>
          <div class="input-container">
            <input
              type="password"
              id="newPassword"
              class="form-input"
              placeholder="Ingrese su nueva contraseña"
              v-model="newPassword"
              required
              :disabled="isLoading"
            >
            <div class="input-border"></div>
          </div>
          <div class="password-strength">
            <div class="strength-bar" :class="{'weak': passwordStrength === 1, 'medium': passwordStrength === 2, 'strong': passwordStrength === 3}"></div>
            <span class="strength-text">{{ passwordStrengthText }}</span>
          </div>
          <ul class="password-requirements">
            <li :class="{'valid': hasMinLength}"><i class="bi" :class="hasMinLength ? 'bi-check-circle-fill' : 'bi-circle'"></i> Mínimo 8 caracteres</li>
            <li :class="{'valid': hasUpperCase}"><i class="bi" :class="hasUpperCase ? 'bi-check-circle-fill' : 'bi-circle'"></i> Al menos una mayúscula</li>
            <li :class="{'valid': hasNumber}"><i class="bi" :class="hasNumber ? 'bi-check-circle-fill' : 'bi-circle'"></i> Al menos un número</li>
          </ul>
        </div>
        
        <div class="form-group">
          <label for="confirmPassword" class="form-label">
            <i class="bi bi-key-fill"></i> Confirmar Contraseña
          </label>
          <div class="input-container">
            <input
              type="password"
              id="confirmPassword"
              class="form-input"
              placeholder="Confirme su nueva contraseña"
              v-model="confirmPassword"
              required
              :disabled="isLoading"
            >
            <div class="input-border"></div>
          </div>
          <div class="password-match" :class="{'match': passwordsMatch, 'mismatch': !passwordsMatch && confirmPassword.length > 0}">
            <i class="bi" :class="passwordsMatch ? 'bi-check-circle-fill' : 'bi-exclamation-circle-fill'"></i>
            {{ passwordsMatch ? 'Las contraseñas coinciden' : 'Las contraseñas no coinciden' }}
          </div>
        </div>
        
        <button type="submit" class="reset-btn" :disabled="isLoading || !formIsValid">
          <span v-if="!isLoading">
            <i class="bi bi-check-circle"></i> Actualizar Contraseña
          </span>
          <span v-else>
            <i class="bi bi-arrow-repeat spinner"></i> Procesando...
          </span>
          <span class="btn-pulse"></span>
        </button>
      </form>

      <div class="card-footer">
        <router-link to="/" class="back-link">
          <i class="bi bi-arrow-left"></i> Volver al inicio de sesión
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from 'sweetalert2';

export default {
  name: "PasswordResetView",
  data() {
    return {
      newPassword: "",
      confirmPassword: "",
      isLoading: false,
      token: "" // Token de recuperación que vendría por URL
    };
  },
  computed: {
    hasMinLength() {
      return this.newPassword.length >= 8;
    },
    hasUpperCase() {
      return /[A-Z]/.test(this.newPassword);
    },
    hasNumber() {
      return /[0-9]/.test(this.newPassword);
    },
    passwordStrength() {
      let strength = 0;
      if (this.newPassword.length > 0) strength++;
      if (this.hasMinLength) strength++;
      if (this.hasUpperCase && this.hasNumber) strength++;
      return strength;
    },
    passwordStrengthText() {
      const texts = ["", "Débil", "Moderada", "Fuerte"];
      return texts[this.passwordStrength];
    },
    passwordsMatch() {
      return this.newPassword === this.confirmPassword && this.newPassword.length > 0;
    },
    formIsValid() {
      return (
        this.hasMinLength &&
        this.hasUpperCase &&
        this.hasNumber &&
        this.passwordsMatch
      );
    }
  },
  methods: {
    async submitNewPassword() {
  if (!this.formIsValid) return;
  
  this.isLoading = true;
  
  try {
    const response = await axios.post("http://127.0.0.1:8000/api/v1/users/", {
      token: this.token,
      new_password: this.newPassword,  // Asegúrate que coincida con lo que espera tu backend
      confirm_password: this.confirmPassword
    });

    if (response.status === 200) {
      await Swal.fire({
        title: '¡Éxito!',
        text: 'Tu contraseña ha sido actualizada correctamente',
        icon: 'success',
        confirmButtonColor: '#002a68'
      });
      this.$router.push('/login'); // Redirige al login
    }
  } catch (error) {
    let errorMessage = 'Ocurrió un error al actualizar la contraseña';
    
    // Manejo específico de errores
    if (error.response) {
      if (error.response.status === 400) {
        errorMessage = error.response.data.message || 'Token inválido o expirado';
      } else if (error.response.status === 401) {
        errorMessage = 'No autorizado - verifica tus credenciales';
      }
    }
    
    await Swal.fire({
      title: 'Error',
      text: errorMessage,
      icon: 'error',
      confirmButtonColor: '#002a68'
    });
  } finally {
    this.isLoading = false;
  }
},

  mounted() {
  // Obtener el token de la URL
  this.token = this.$route.query.token || '';
  
  // Si usas parámetros en la ruta (ej: /reset-password/:token)
  // this.token = this.$route.params.token;
}
}
}
</script>

<style scoped>
/* Variables consistentes con el login */
:root {
  --primary-color: #002a68;
  --accent-color: #4e73df;
  --light-accent: #6699ff;
  --success-color: #28a745;
  --error-color: #e53e3e;
  --warning-color: #dd6b20;
  --text-color: #2d3748;
  --light-text: #718096;
  --border-color: #e2e8f0;
  --card-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* Estructura principal (igual al login) */
.password-reset-container {
  position: relative;
  width: 100%;
  min-height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* Fondo animado (igual al login) */
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

/* Logo superior (igual al login) */
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

/* Tarjeta de reset con algunos ajustes */
.reset-card {
  position: relative;
  width: 420px; /* Un poco más ancho que el login */
  background: white;
  border-radius: 12px;
  box-shadow: var(--card-shadow);
  overflow: hidden;
  z-index: 1;
  margin-bottom: 30px;
  animation: fadeInUp 0.5s ease-out;
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
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.card-header p {
  color: var(--light-text);
  font-size: 0.9rem;
  margin: 0;
}

/* Formulario con mejoras específicas para password */
.reset-form {
  padding: 25px 30px;
}

.form-group {
  margin-bottom: 25px;
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

/* Indicador de fortaleza de contraseña */
.password-strength {
  display: flex;
  align-items: center;
  margin-top: 8px;
  height: 20px;
}

.strength-bar {
  height: 4px;
  border-radius: 2px;
  background: #e2e8f0;
  flex-grow: 1;
  margin-right: 10px;
  overflow: hidden;
  position: relative;
}

.strength-bar::after {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 0;
  transition: width 0.3s ease, background 0.3s ease;
}

.strength-bar.weak::after {
  width: 33%;
  background: var(--error-color);
}

.strength-bar.medium::after {
  width: 66%;
  background: var(--warning-color);
}

.strength-bar.strong::after {
  width: 100%;
  background: var(--success-color);
}

.strength-text {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--light-text);
}

.strength-bar.weak ~ .strength-text {
  color: var(--error-color);
}

.strength-bar.medium ~ .strength-text {
  color: var(--warning-color);
}

.strength-bar.strong ~ .strength-text {
  color: var(--success-color);
}

/* Requisitos de contraseña */
.password-requirements {
  list-style: none;
  padding: 0;
  margin: 8px 0 0;
}

.password-requirements li {
  font-size: 0.75rem;
  color: var(--light-text);
  margin-bottom: 4px;
  display: flex;
  align-items: center;
}

.password-requirements li i {
  margin-right: 6px;
  font-size: 0.9rem;
}

.password-requirements li.valid {
  color: var(--success-color);
}

.password-requirements li.valid i {
  color: var(--success-color);
}

/* Indicador de coincidencia de contraseñas */
.password-match {
  font-size: 0.75rem;
  margin-top: 8px;
  display: flex;
  align-items: center;
}

.password-match i {
  margin-right: 6px;
  font-size: 0.9rem;
}

.password-match.match {
  color: var(--success-color);
}

.password-match.mismatch {
  color: var(--error-color);
}

/* Botón de reset (similar al login con mejoras) */
.reset-btn {
  width: 100%;
  padding: 14px;
  margin-top: 10px;
  background: var(--primary-color);
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

.reset-btn:hover:not(:disabled) {
  background: #0047a3;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 42, 104, 0.4);
}

.reset-btn:active:not(:disabled) {
  transform: translateY(1px);
  box-shadow: 0 2px 4px rgba(0, 42, 104, 0.3);
}

.reset-btn::before {
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

.reset-btn:hover:not(:disabled)::before {
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

.reset-btn:focus:not(:active) .btn-pulse {
  animation: pulse 1s ease-out;
}

.reset-btn:disabled {
  background: #a0aec0;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
  opacity: 0.7;
}

.reset-btn:disabled::before {
  display: none;
}

/* Footer de la tarjeta */
.card-footer {
  padding: 15px 30px;
  text-align: center;
  background: #f8fafc;
  border-top: 1px solid var(--border-color);
  font-size: 0.85rem;
}

.back-link {
  color: var(--accent-color);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.back-link:hover {
  color: var(--primary-color);
  text-decoration: underline;
}

.back-link i {
  font-size: 0.9rem;
}

/* Pantalla de carga (igual al login) */
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

/* Animaciones */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 480px) {
  .reset-card {
    width: 90%;
    max-width: 420px;
  }
  
  .logo {
    height: 70px;
  }
  
  .card-header, .reset-form, .card-footer {
    padding-left: 20px;
    padding-right: 20px;
  }
}
</style>