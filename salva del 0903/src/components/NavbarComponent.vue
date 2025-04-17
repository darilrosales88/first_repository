<template>
<br>
<br>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <router-link to="/home"><i class="bi bi-houses-fill"></i></router-link>
  
  <div class="container-fluid">
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">        
        <li class="nav-item dropdown" v-if="hasGroup('Admin')">
          
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Seguridad
          </a>
          <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
          
            <li><router-link class="dropdown-item" to="/Usuarios">Usuarios</router-link></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><router-link class="dropdown-item" to="/groups">Grupos</router-link></li>
            <li><router-link class="dropdown-item" to="/Trazas">Trazas</router-link></li>
          </ul>
        </li>
        <!-- Enlace a Nomencladores (solo para usuarios autenticados) -->
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Nomencladores
          </a>
          <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
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
            <li><router-link class="dropdown-item" to="/vagones_cargados_descargados">Vagones cargados/descargados</router-link></li>
            <li><router-link class="dropdown-item" to="/productos_vagones_cargados_descargados">Productos de agones cargados/descargados</router-link></li>
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Partes
          </a>
          <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
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
          <a class="nav-link ">Reportes</a>
        </li>
        <li class="nav-item">
          <a class="nav-link " @click="logout()">Cerrar sesión</a>
        </li>
      </ul>
      
    </div>
  </div>
</nav>
</template>
<script>
import axios from 'axios';

export default {
  name: 'NavbarComponent',
  data() {
    return {
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [],      // Almacenará los grupos del usuario
    };
  },  
  async created() {
    // Obtener los permisos y grupos del usuario al cargar el componente
    await this.fetchUserPermissionsAndGroups();
  },
  methods: {
    // Verifica si el usuario tiene un permiso específico
    hasPermission(permission) {
      return this.userPermissions.some(p => p.name === permission);
      },
    hasGroup(group) {
          return this.userGroups.some(g => g.name === group);
      },
    // Obtiene los permisos y grupos del usuario desde el backend
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
};
</script>