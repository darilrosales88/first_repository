<template>
    <div>
      <!-- Botón para ocultar/mostrar el panel izquierdo -->
      <button @click="toggleSidebar" class="toggle-sidebar-btn">
        <i :class="isSidebarVisible ? 'bi bi-arrow-left' : 'bi bi-arrow-right'"></i>
      </button>
  
      <!-- Panel izquierdo -->
      <nav class="navbar" :style="{ width: isSidebarVisible ? '200px' : '0', overflow: isSidebarVisible ? 'visible' : 'hidden' }">
        <!-- Lista de elementos del menú -->
        <ul class="navbar-nav" style="margin-bottom:10em">
          <!-- Enlaces del menú -->
          <li class="nav-item dropdown" v-if="hasGroup('Admin')">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownSeguridad" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <i class="bi bi-shield-lock"></i> <span>Seguridad</span>
            </a>
            <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="navbarDropdownSeguridad">
              <li><router-link class="dropdown-item" to="/Usuarios">Usuarios</router-link></li>
              <li><hr class="dropdown-divider"></li>
              <li><router-link class="dropdown-item" to="/groups">Grupos</router-link></li>
              <li><hr class="dropdown-divider"></li>
              <li><router-link class="dropdown-item" to="/Trazas">Trazas</router-link></li>
            </ul>
          </li>
  
          <!-- Más enlaces -->
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownNomencladores" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <i class="bi bi-list-task"></i> <span>Nomencladores</span>
            </a>
            <ul class="dropdown-menu dropdown-menu-dark scrollable-menu" aria-labelledby="navbarDropdownNomencladores">
                <li><router-link class="dropdown-item" to="/Atraques">Atraques</router-link></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><a class="dropdown-item" href="/Cargos">Cargos</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><router-link class="dropdown-item" to="/contenedor">Contenedores</router-link></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><router-link class="dropdown-item" to="Destino">Destinos</router-link></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><router-link class="dropdown-item" to="Embarcaciones">Embarcaciones</router-link></li>
            <li>
              <li>
              <hr class="dropdown-divider">
            </li>
            <li><router-link class="dropdown-item" to="AdicionarEmbarcacion1">Prueba de modal</router-link></li>
            <li></li>
              <hr class="dropdown-divider">
            </li>
            <li><a class="dropdown-item" href="/Entidades">Entidades</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><router-link class="dropdown-item" to="/EquipoFerro">Equipos ferroviarios</router-link></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><router-link class="dropdown-item" to="EstadoTecnico">Estados técnicos</router-link></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li>
              <li><router-link class="dropdown-item" to="EstructuraUbicacion">Estructuras de ubicación</router-link></li>
              <hr class="dropdown-divider">
            </li>
            <li><router-link class="dropdown-item" to="/Incidencias">Incidencias</router-link></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><a class="dropdown-item" href="Organismos">OSDE/OACE u organismo</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><a class="dropdown-item" href="/Paises">Países</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            
            <li>
            <router-link class="dropdown-item" to="Producto">Productos</router-link>
            </li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><a class="dropdown-item" href="/Provincia">Provincias</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><router-link class="dropdown-item" to="Puertos">Puertos</router-link></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><router-link class="dropdown-item" to="Terminal">Terminales</router-link></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><router-link class="dropdown-item" to="/Territorio">Territorios</router-link></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><a class="dropdown-item" href="/TipoEmbalaje">Tipos de embalajes</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><router-link class="dropdown-item" to="/TipoEquipoFerro">Tipos de equipos ferroviarios</router-link></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><router-link class="dropdown-item" to="TipoEstructuraUbicacion">Tipos de estructuras de ubicacion</router-link></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><router-link class="dropdown-item" to="TipoManiobra">Tipos de maniobras</router-link></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><router-link class="dropdown-item" to="/UM">Unidades de medida</router-link></li>
            </ul>
          </li>
  
          <!-- Más enlaces -->
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <i class="bi bi-file-earmark-text"></i> <span class="d-lg-inline d-none">Partes</span>
            </a>
            <ul class="dropdown-menu dropdown-menu-dark w-100 scrollable-menu" aria-labelledby="navbarDropdown">
              <!-- ... (tus enlaces actuales) ... -->
              <li><a class="dropdown-item" href="#">GEMAR</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><a class="dropdown-item" href="#">EMCARGA</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><a class="dropdown-item" href="#">ETAG</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><a class="dropdown-item" href="#">ENOC</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><a class="dropdown-item" href="#">UFC</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><a class="dropdown-item" href="#">GEA</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><a class="dropdown-item" href="#">MINCIN</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><a class="dropdown-item" href="#">GEIA</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><a class="dropdown-item" href="#">AZCUBA</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><a class="dropdown-item" href="#">GECEM</a></li>
            </ul>
          </li>
  
          <li class="nav-item">
            <a class="nav-link">
              <i class="bi bi-file-earmark-bar-graph"></i> <span>Reportes</span>
            </a>
          </li>
        </ul>
  
        <!-- Botón de cerrar sesión -->
        <div class="logout-link">
          <a class="nav-link" @click="logout">
            <i class="bi bi-box-arrow-right"></i> <span class="logout-text">Cerrar sesión</span>
          </a>
        </div>
      </nav>
  
      <!-- Panel derecho (contenido principal) -->
      <div class="content" :style="{ marginLeft: isSidebarVisible ? '200px' : '0' }">
        <!-- Aquí va el contenido principal de tu aplicación -->
        <router-view></router-view>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'NavbarComponent',
    data() {
      return {
        userPermissions: [],
        userGroups: [],
        isSidebarVisible: true, // Controla la visibilidad del panel izquierdo
      };
    },
    async created() {
      await this.fetchUserPermissionsAndGroups();
    },
    methods: {
      hasPermission(permission) {
        return this.userPermissions.some(p => p.name === permission);
      },
      hasGroup(group) {
        return this.userGroups.some(g => g.name === group);
      },
      async fetchUserPermissionsAndGroups() {
        try {
          const userId = localStorage.getItem('userid');
          if (userId) {
            const response = await axios.get(`/apiAdmin/user/${userId}/permissions-and-groups/`);
            this.userPermissions = response.data.permissions;
            this.userGroups = response.data.groups;
          }
        } catch (error) {
          console.error('Error al obtener permisos y grupos:', error);
        }
      },
      async logout() {
        try {
          await axios.post('/api/v1/token/logout/');
          console.log('Logged out');
          axios.defaults.headers.common['Authorization'] = '';
          localStorage.removeItem('token');
          localStorage.removeItem('username');
          localStorage.removeItem('userid');
          this.$store.commit('removeToken');
          this.$router.push("/");
        } catch (error) {
          console.log(JSON.stringify(error));
        }
      },
      toggleSidebar() {
        this.isSidebarVisible = !this.isSidebarVisible; // Alternar visibilidad del panel izquierdo
      },
    },
  };
  </script>
  
  <style scoped>
  /* Estilos para el botón de alternar */
  .toggle-sidebar-btn {
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 1000;
    background-color: #003366;
    color: white;
    border: none;
    padding: 10px;
    border-radius: 50%;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .toggle-sidebar-btn:hover {
    background-color: #002244;
  }
  
  /* Estilos para el panel izquierdo */
  .navbar {
    width: 200px;
    height: 100vh;
    position: fixed;
    top: 0;
    left: 0;
    padding: 0;
    background-color: #003366;
    transition: width 0.3s ease, overflow 0.3s ease;
  }
  
  /* Estilos para el contenido principal */
  .content {
    margin-left: 200px; /* Ajusta el margen según el ancho del panel izquierdo */
    transition: margin-left 0.3s ease;
  }
  
  /* Ajustes para pantallas pequeñas */
  @media (max-width: 992px) {
    .navbar {
      width: 0; /* Ocultar el panel izquierdo por defecto en pantallas pequeñas */
    }
  
    .content {
      margin-left: 0; /* Redimensionar el contenido principal */
    }
  
    .toggle-sidebar-btn {
      left: 10px; /* Ajustar posición del botón */
    }
  }
  
  /* Estilos adicionales */
  .navbar-nav .nav-item {
    margin: 0.5rem 0; /* Separación entre elementos */
    margin-left: 1em;
    text-align: center; /* Centrar texto */
    position: relative; /* Necesario para posicionar los submenús */
  }
  
  .navbar-nav .nav-link:hover,
  .dropdown-item:hover {
    color: #fff !important; /* Efecto hover blanco */
  }
  
  .dropdown-menu {
    position: absolute; /* Mostrar fuera de la barra */
    margin-left: 23px;
    left: 100%; /* Posicionar al lado del elemento padre */
    top: 0;
    background-color: #003366; /* Azul oscuro */
    border: 1px solid #555; /* Borde gris */
    max-height: 200px; /* Altura máxima antes de mostrar el scroll */
    overflow-y: auto; /* Habilitar scroll vertical */
    min-width: 200px; /* Ancho mínimo para los submenús */
  }
  
  .dropdown-menu::-webkit-scrollbar {
    width: 8px; /* Ancho del scroll */
  }
  
  .dropdown-menu::-webkit-scrollbar-thumb {
    background-color: #fff; /* Color del scroll */
    border-radius: 4px; /* Redondear el scroll */
  }
  
  .dropdown-menu::-webkit-scrollbar-track {
    background-color: #444; /* Color de fondo del scroll */
  }
  
  .logout-text {
    display: none;
  }
  
  .logout-link .nav-link i {
    font-size: 1.5rem; /* Tamaño del ícono */
  }
  
  .logout-link {
    cursor: pointer;
    color: #fff !important;
    transition: color 0.3s ease;
    position: fixed;
    bottom: 1rem;
    left: 1rem;
  }
  
  .logout-link:hover {
    color: #ff8c42 !important;
  }
  </style>