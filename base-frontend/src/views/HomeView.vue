<template>
  <nav class="navbar" style="background-color: #003366; height: 100vh;">
    
    
    <!-- Lista de elementos del menú -->
    <ul class="navbar-nav" style="margin-bottom:10em">
      <!-- Enlaces del menú -->
      <li class="nav-item dropdown" v-if="hasGroup('Admin')">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownSeguridad" role="button" data-bs-toggle="dropdown" aria-expanded="false">
          <i class="bi bi-shield-lock"></i> <span>Seguridad</span>
        </a>
        <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="navbarDropdownSeguridad">
          <li><router-link class="dropdown-item" to="/Usuarios">Usuarios</router-link></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><router-link class="dropdown-item" to="/groups">Grupos</router-link></li>
            <li>
              <hr class="dropdown-divider">
            </li>
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
            <li><a class="dropdown-item" href="#">GEMAR</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">EMCARGA</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">ETAG</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">ENOC</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">UFC</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">GEA</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">MINCIN</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">GEIA</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">AZCUBA</a></li>
            <li><hr class="dropdown-divider"></li>
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
</template>


<style scoped>
/* Estilos para la barra de navegación */
.navbar {
  width: 200px; /* Ancho fijo */
  height: 100vh; /* Ocupa toda la altura de la pantalla */
  position: fixed; /* Fija la barra en la pantalla */
  top: 0;
  left: 0;
  padding: 0;
  background-color: #003366; /* Azul oscuro */
  transition: width 0.3s ease; /* Transición suave para el ancho */
}

/* Barra de búsqueda */
.search-container {
  padding: 10px;
  margin: 10px;
}

.search-form .input-group {
  width: 100%;
}

.search-form {
  display: flex;
  align-items: center;
  background-color: white; /* Fondo blanco */
  border-radius: 50px; /* Forma ovalada */
  padding: 5px 10px;
  transition: box-shadow 0.3s ease; /* Transición suave para el efecto hover */
}

.search-form:hover {
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.8); /* Iluminación blanca */
}

.search-form .form-control {
  background-color: transparent;
  border: none;
  color: #000; /* Texto negro */
  box-shadow: none;
  flex-grow: 1; /* Ocupa el espacio disponible */
}

.search-form .form-control:focus {
  outline: none;
}

.search-icon {
  color: #000; /* Color negro para el ícono */
  transition: color 0.3s ease;
}

.search-icon:hover {
  color: gray; /* Color gris al pasar el cursor */
}



.navbar-nav .nav-item{
  margin-top:-6em;
}

/* Estilos para pantallas pequeñas */
@media (max-width: 992px) {
  .navbar {
    width: 80px; /* Ancho reducido para pantallas pequeñas */
  }

  .search-container {
    display: none; /* Ocultar barra de búsqueda */
  }

  .search-icon-mobile {
    display: block; /* Mostrar ícono de búsqueda */
  }

  .navbar-nav .nav-link span {
    display: none; /* Ocultar texto en pantallas pequeñas */
  }

  .navbar-nav .nav-link i {
    font-size: 1.5rem; /* Tamaño de los íconos */
  }

  /* Ajustes para los submenús en pantallas pequeñas */
  .dropdown-menu {
    position: absolute;
    left: 100%; /* Mostrar submenús al lado del elemento padre */
    top: 0;
    margin-left: 0;
    border-radius: 0;
    max-height: 200px; /* Altura máxima antes de mostrar el scroll */
    overflow-y: auto; /* Habilitar scroll vertical */
    background-color: #003366; /* Fondo azul oscuro */
    border: 1px solid #555; /* Borde gris */
    min-width: 200px; /* Ancho mínimo para los submenús */
  }

  

  .dropdown-menu li:hover {
    background-color: #555; /* Fondo gris al pasar el cursor */
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
  margin-left:23px;
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
 
<script>
import axios from 'axios';

export default {
  name: 'NavbarComponent',
  data() {
    return {
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [],      // Almacenará los grupos del usuario
      searchQuery: '', // Query de búsqueda
      showSearchPanel: false, // Estado para controlar si el panel de búsqueda está visible
    };
  },

  methods: {
    // Métodos relacionados con la barra de navegación
    handleSearch() {
      if (this.searchQuery.trim()) {
        // Normaliza la ruta: convierte a minúsculas y elimina espacios
        const routePath = this.searchQuery.trim().toLowerCase();

        // Redirige a la ruta
        this.$router.push(routePath);
      } else {
        alert('Por favor, ingresa una ruta válida.');
      }
    },
    focusSearch() {
      // Lógica al enfocar la búsqueda
    },
    blurSearch() {
      // Lógica al desenfocar la búsqueda
    },
    toggleSearchPanel() {
      this.showSearchPanel = !this.showSearchPanel; // Alternar visibilidad del panel de búsqueda
    },
    handleResize() {
      // Lógica para manejar el redimensionamiento de la pantalla
      console.log("La pantalla ha sido redimensionada");
      // Aquí puedes agregar lógica adicional si es necesario
    },

    // Métodos relacionados con permisos y grupos
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

          console.log('(Respuesta del servidorrr', this.userGroups)
        }
      } catch (error) {
        console.error('Error al obtener permisos y grupos:', error);
      }
    },
    async logout() {
      try {
        await axios.post('/api/v1/token/logout/');
        console.log('Logged out');
        // Eliminar los tokens y redirigir al inicio de sesión
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
  },

  mounted() {
    // Escuchar cambios en el tamaño de la pantalla
    window.addEventListener('resize', this.handleResize);
    this.handleResize(); // Verificar el tamaño inicial
  },
  beforeDestroy() {
    // Limpiar el listener al destruir el componente
    window.removeEventListener('resize', this.handleResize);
  },

  async created() {
    // Obtener los permisos y grupos del usuario al cargar el componente
    await this.fetchUserPermissionsAndGroups();
  },
};
</script>

