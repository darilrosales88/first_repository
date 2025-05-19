<template>
  <nav class="navbar">
    <!-- Burbujas animadas de fondo -->
    <div class="bubbles">
      <div class="bubble bubble-1"></div>
      <div class="bubble bubble-2"></div>
      <div class="bubble bubble-3"></div>
      <div class="bubble bubble-4"></div>
      <div class="bubble bubble-5"></div>
    </div>
    
    <!-- Logo/Texto de la empresa -->
    <div class="logo-container">
      <h1 class="company-name">MITRANS</h1>
      <p class="company-slogan">Transporte y Logística</p>
    </div>
    
    <!-- Lista de elementos del menú -->
    <ul class="navbar-nav">
      <li class="nav-item home-item">
        <router-link to="/home" class="nav-link">
          <i class="bi bi-houses-fill"></i>
          <span>Inicio</span>
        </router-link>
      </li>
      
      <!-- Elemento Seguridad -->
      <li class="nav-item dropdown" v-if="hasGroup('Admin')">
        <div class="nav-link" @click="toggleDropdown('Seguridad')">
          <i class="bi bi-shield-lock"></i>
          <span>Seguridad</span>
          <i class="bi bi-chevron-right dropdown-arrow"></i>
        </div>
        <div class="submenu" v-if="activeDropdown === 'Seguridad'">
          <h3 class="submenu-title">Seguridad</h3>
          <ul class="submenu-items">
            <li>
              <router-link to="/Usuarios" class="submenu-link">Usuarios</router-link>
            </li>
            <li>
              <router-link to="/groups" class="submenu-link">Grupos</router-link>
            </li>
            <li>
              <router-link to="/Trazas" class="submenu-link">Trazas</router-link>
            </li>
          </ul>
        </div>
      </li>
      
      <!-- Elemento Nomencladores -->
      <li class="nav-item dropdown">
        <div class="nav-link" @click="toggleDropdown('Nomencladores')">
          <i class="bi bi-list-task"></i>
          <span>Nomencladores</span>
          <i class="bi bi-chevron-right dropdown-arrow"></i>
        </div>
        <div class="submenu" v-if="activeDropdown === 'Nomencladores'">
          <h3 class="submenu-title">Nomencladores</h3>
          <ul class="submenu-items scrollable-menu">
            <li>
              <router-link to="/Atraques" class="submenu-link">Atraques</router-link>
            </li>
            <li>
              <router-link to="/Cargos" class="submenu-link">Cargos</router-link>
            </li>
            <li>
              <router-link to="/contenedor" class="submenu-link">Contenedores</router-link>
            </li>
            <li>
              <router-link to="/Destino" class="submenu-link">Destinos</router-link>
            </li>
            <li>
              <router-link to="/Embarcaciones" class="submenu-link">Embarcaciones</router-link>
            </li>
            <li>
              <router-link to="/Entidades" class="submenu-link">Entidades</router-link>
            </li>
            <li>
              <router-link to="/EquipoFerro" class="submenu-link">Equipos ferroviarios</router-link>
            </li>
            <li>
              <router-link to="/EstadoTecnico" class="submenu-link">Estados técnicos</router-link>
            </li>
            <li>
              <router-link to="/EstructuraUbicacion" class="submenu-link">Estructuras de ubicación</router-link>
            </li>
            <li>
              <router-link to="/Incidencias" class="submenu-link">Incidencias</router-link>
            </li>
            <li>
              <router-link to="/Organismos" class="submenu-link">OSDE/OACE u organismo</router-link>
            </li>
            <li>
              <router-link to="/Paises" class="submenu-link">Países</router-link>
            </li>
            <li>
              <router-link to="/Producto" class="submenu-link">Productos</router-link>
            </li>
            <li>
              <router-link to="/Provincia" class="submenu-link">Provincias</router-link>
            </li>
            <li>
              <router-link to="/Puertos" class="submenu-link">Puertos</router-link>
            </li>
            <li>
              <router-link to="/Terminal" class="submenu-link">Terminales</router-link>
            </li>
            <li>
              <router-link to="/Territorio" class="submenu-link">Territorios</router-link>
            </li>
            <li>
              <router-link to="/TipoEmbalaje" class="submenu-link">Tipos de embalajes</router-link>
            </li>
            <li>
              <router-link to="/TipoEquipoFerro" class="submenu-link">Tipos de equipos ferroviarios</router-link>
            </li>
            <li>
              <router-link to="/TipoEstructuraUbicacion" class="submenu-link">Tipos de estructuras de ubicacion</router-link>
            </li>
            <li>
              <router-link to="/TipoManiobra" class="submenu-link">Tipos de maniobras</router-link>
            </li>
            <li>
              <router-link to="/UM" class="submenu-link">Unidades de medida</router-link>
            </li>
          </ul>
        </div>
      </li>
      
      <!-- Elemento Partes -->
      <li class="nav-item dropdown">
        <div class="nav-link" @click="toggleDropdown('Partes')">
          <i class="bi bi-file-earmark-text"></i>
          <span>Partes</span>
          <i class="bi bi-chevron-right dropdown-arrow"></i>
        </div>
        <div class="submenu" v-if="activeDropdown === 'Partes'">
          <h3 class="submenu-title">Partes</h3>
          <ul class="submenu-items scrollable-menu">
            <li><a class="submenu-link" href="#">GEMAR</a></li>
            <li><a class="submenu-link" href="#">EMCARGA</a></li>
            <li><a class="submenu-link" href="#">ETAG</a></li>
            <li><a class="submenu-link" href="#">ENOC</a></li>
            <li><router-link to="/ufc" class="submenu-link">UFC</router-link></li>
            <li><a class="submenu-link" href="#">GEA</a></li>
            <li><a class="submenu-link" href="#">MINCIN</a></li>
            <li><a class="submenu-link" href="#">GEIA</a></li>
            <li><a class="submenu-link" href="#">AZCUBA</a></li>
            <li><a class="submenu-link" href="#">GECEM</a></li>
          </ul>
        </div>
      </li>
      
      <!-- Elemento Reportes -->
      <li class="nav-item">
        <a class="nav-link">
          <i class="bi bi-file-earmark-bar-graph"></i>
          <span>Reportes</span>
        </a>
      </li>
    </ul>
    
    <!-- Botón de cerrar sesión -->
    <div class="logout-container" @click="logout">
      <div class="logout-content">
        <i class="bi bi-box-arrow-right"></i>
        <span class="logout-text">Cerrar sesión</span>
      </div>
      
    </div>
  </nav>
</template>

<script>
import axios from "axios";

export default {
  name: "NavbarComponent",
  data() {
    return {
      userPermissions: [],
      userGroups: [],
      activeDropdown: null,
      username: localStorage.getItem("username") || "Usuario"
    };
  },
  async created() {
    await this.fetchUserPermissionsAndGroups();
  },
  methods: {
    hasPermission(permission) {
      return this.userPermissions.some((p) => p.name === permission);
    },
    hasGroup(group) {
      return this.userGroups.some((g) => g.name === group);
    },
    async fetchUserPermissionsAndGroups() {
      try {
        const userId = localStorage.getItem("userid");
        if (userId) {
          const response = await axios.get(
            `/apiAdmin/user/${userId}/permissions-and-groups/`
          );
          this.userPermissions = response.data.permissions;
          this.userGroups = response.data.groups;
        }
      } catch (error) {
        console.error("Error al obtener permisos y grupos:", error);
      }
    },
    toggleDropdown(menu) {
      this.activeDropdown = this.activeDropdown === menu ? null : menu;
    },
    async logout() {
      try {
        await axios.post("/api/v1/token/logout/");
        console.log("Logged out");
        axios.defaults.headers.common["Authorization"] = "";
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        localStorage.removeItem("userid");
        this.$store.commit("removeToken");
        this.$router.push("/");
      } catch (error) {
        console.log(JSON.stringify(error));
      }
    },
  },
};
</script>

<style scoped>
/* Estilos base */
:root {
  --primary-color: #002a69;       /* Azul oscuro principal */
  --primary-light: #003580;       /* Azul un poco más claro para hover */
  --primary-dark: #001f54;        /* Azul más oscuro para submenús */
  --accent-color: #ff8c42;        /* Naranja para acentos */
  --text-color: #ffffff;          /* Texto blanco */
  --text-secondary: #eeeeee;      /* Texto secundario gris claro */
  --hover-color: #ff6b1a;         /* Naranja más intenso para hover */
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Estilos para la barra de navegación */
.navbar {
  width: 250px;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  background-color: #002a68;
  color: var(--text-color);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 1000;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.3);
}

/* Animación de burbujas */
.bubbles {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
}

.bubble {
  position: absolute;
  bottom: -100px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  animation: rise 15s infinite ease-in;
}

.bubble-1 {
  width: 40px;
  height: 40px;
  left: 10%;
  animation-duration: 15s;
}

.bubble-2 {
  width: 20px;
  height: 20px;
  left: 20%;
  animation-duration: 12s;
  animation-delay: 2s;
}

.bubble-3 {
  width: 50px;
  height: 50px;
  left: 35%;
  animation-duration: 18s;
  animation-delay: 1s;
}

.bubble-4 {
  width: 30px;
  height: 30px;
  left: 70%;
  animation-duration: 14s;
  animation-delay: 3s;
}

.bubble-5 {
  width: 25px;
  height: 25px;
  left: 85%;
  animation-duration: 16s;
  animation-delay: 4s;
}

@keyframes rise {
  0% {
    bottom: -100px;
    transform: translateX(0);
    opacity: 1;
  }
  50% {
    transform: translateX(20px);
  }
  100% {
    bottom: 100vh;
    transform: translateX(0);
    opacity: 0;
  }
}

/* Logo y nombre de la empresa */
.logo-container {
  padding: 20px;
  text-align: center;
  position: relative;
  z-index: 1;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.company-name {
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: 2px;
  margin-bottom: 5px;
  text-transform: uppercase;
  color: white;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}

.company-slogan {
  font-size: 0.8rem;
  color: white;
  letter-spacing: 1px;
}

/* Lista de navegación */
.navbar-nav {
  list-style: none;
  padding: 20px 0;
  flex-grow: 1;
  overflow-y: auto;
  position: relative;
  z-index: 1;
}

.nav-item {
  position: relative;
  margin-bottom: 5px;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: white;
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
}

.nav-link:hover {
  background-color: var(--primary-light);
  color: var(--accent-color);
}

.nav-link i {
  margin-right: 15px;
  font-size: 1.1rem;
}

.nav-link .dropdown-arrow {
  margin-left: auto;
  transition: transform 0.3s ease;
}

.nav-item.dropdown.active .dropdown-arrow {
  transform: rotate(90deg);
}

.home-item {
  margin-top: 10px;
}

/* Submenús */
.submenu {
  position: fixed;
  left: 250px;
  top: 0;
  width: 250px;
  height: 100vh;
  background-color: #002a68;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.3);
  z-index: 999;
  transform: translateX(0);
  transition: transform 0.3s ease;
}

.submenu-title {
  padding: 20px;
  font-size: 1.2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: black;
}

.submenu-items {
  list-style: none;
  padding: 10px 0;
  height: calc(100vh - 70px);
  overflow-y: auto;
}

.submenu-link {
  display: block;
  padding: 12px 20px;
  color: white;
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  background-color: var(--primary-dark);
}

.submenu-link:hover {
  background-color: var(--primary-light);
  color: var(--accent-color);
  padding-left: 25px;
}

/* Scroll personalizado */
.scrollable-menu::-webkit-scrollbar {
  width: 6px;
}

.scrollable-menu::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.scrollable-menu::-webkit-scrollbar-track {
  background-color: rgba(0, 0, 0, 0.1);
}

/* Cerrar sesión */
.logout-container {
  position: relative;
  padding: 15px 20px;
  background-color: rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 1;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.logout-container:hover {
  background-color: rgba(0, 0, 0, 0.3);
}

.logout-content {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.logout-content i {
  margin-right: 15px;
  font-size: 1.2rem;
  color: white;
}

.logout-text {
  font-weight: 500;
  font-size: 0.95rem;
  color: white;
}

.logout-user {
  display: flex;
  align-items: center;
  font-size: 0.85rem;
  color: white;
}

.logout-user i {
  margin-right: 10px;
}

/* Responsive */
@media (max-width: 992px) {
  .navbar {
    width: 70px;
  }
  
  .company-name, .company-slogan, .nav-link span, .logout-text, .logout-user {
    display: none;
  }
  
  .nav-link {
    justify-content: center;
    padding: 15px 0;
  }
  
  .nav-link i {
    margin-right: 0;
    font-size: 1.3rem;
  }
  
  .submenu {
    left: 70px;
  }
  
  .logo-container {
    padding: 15px 0;
  }
}
</style>