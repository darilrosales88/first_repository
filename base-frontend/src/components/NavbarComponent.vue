<template>
  <nav class="navbar" style="background-color: #002a69; height: 100vh">
    <div class="logo-container">
      <h1 class="company-name">MITRANS</h1>
      <p class="company-slogan">Transporte y Logística</p>
    </div>
    <!-- Lista de elementos del menú -->
    <ul class="navbar-nav">
      <div class="home">
        <router-link to="/home"
          ><i class="bi bi-houses-fill home-icon"></i
        ></router-link>
      </div>
      <!-- Enlaces del menú -->
      <li class="nav-item dropdown" v-if="hasGroup('Admin')">
        <a
          class="nav-link dropdown-toggle"
          href="#"
          id="navbarDropdownSeguridad"
          role="button"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          <i class="bi bi-shield-lock"></i> <span>Seguridad</span>
        </a>
        <ul
          class="dropdown-menu dropdown-menu-dark"
          aria-labelledby="navbarDropdownSeguridad"
        >
          <li>
            <router-link class="dropdown-item" to="/Usuarios"
              >Usuarios</router-link
            >
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/groups">Grupos</router-link>
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/Trazas">Trazas</router-link>
          </li>
        </ul>
      </li>

      <!-- Más enlaces -->
      <li class="nav-item dropdown">
        <a
          class="nav-link dropdown-toggle"
          href="#"
          id="navbarDropdownNomencladores"
          role="button"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          <i class="bi bi-list-task"></i> <span>Nomencladores</span>
        </a>
        <ul
          class="dropdown-menu dropdown-menu-dark scrollable-menu"
          aria-labelledby="navbarDropdownNomencladores"
        >
          <li>
            <router-link class="dropdown-item" to="/Atraques"
              >Atraques</router-link
            >
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li><a class="dropdown-item" href="/Cargos">Cargos</a></li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/contenedor"
              >Contenedores</router-link
            >
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/Destino"
              >Destinos</router-link
            >
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/Embarcaciones"
              >Embarcaciones</router-link
            >
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li><a class="dropdown-item" href="/Entidades">Entidades</a></li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/EquipoFerro"
              >Equipos ferroviarios</router-link
            >
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/EstadoTecnico"
              >Estados técnicos</router-link
            >
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/EstructuraUbicacion"
              >Estructuras de ubicación</router-link
            >
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/Incidencias"
              >Incidencias</router-link
            >
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <a class="dropdown-item" href="/Organismos"
              >OSDE/OACE u organismo</a
            >
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li><a class="dropdown-item" href="/Paises">Países</a></li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/Producto"
              >Productos</router-link
            >
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li><a class="dropdown-item" href="/Provincia">Provincias</a></li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/Puertos"
              >Puertos</router-link
            >
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/Terminal"
              >Terminales</router-link
            >
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/Territorio"
              >Territorios</router-link
            >
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <a class="dropdown-item" href="/TipoEmbalaje">Tipos de embalajes</a>
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/TipoEquipoFerro"
              >Tipos de equipos ferroviarios</router-link
            >
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/TipoEstructuraUbicacion"
              >Tipos de estructuras de ubicacion</router-link
            >
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/TipoManiobra"
              >Tipos de maniobras</router-link
            >
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/UM"
              >Unidades de medida</router-link
            >
          </li>
        </ul>
      </li>
      <li class="nav-item dropdown">
        <a
          class="nav-link dropdown-toggle"
          href="#"
          id="navbarDropdown"
          role="button"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          <i class="bi bi-file-earmark-text"></i>
          <span class="d-lg-inline d-none">Partes</span>
        </a>
        <ul
          class="dropdown-menu dropdown-menu-dark w-100 scrollable-menu"
          aria-labelledby="navbarDropdown"
        >
          <li>
            <a class="dropdown-item" style="width: 200px" href="#">GEMAR</a>
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li><a class="dropdown-item" href="#">EMCARGA</a></li>
          <li><hr class="dropdown-divider" /></li>
          <li><a class="dropdown-item" href="#">ETAG</a></li>
          <li><hr class="dropdown-divider" /></li>
          <li><a class="dropdown-item" href="#">ENOC</a></li>
          <li><hr class="dropdown-divider" /></li>
          <li>
            <router-link class="dropdown-item" to="/ufc">UFC</router-link>
          </li>
          <li><hr class="dropdown-divider" /></li>
          <li><a class="dropdown-item" href="#">GEA</a></li>
          <li><hr class="dropdown-divider" /></li>
          <li><a class="dropdown-item" href="#">MINCIN</a></li>
          <li><hr class="dropdown-divider" /></li>
          <li><a class="dropdown-item" href="#">GEIA</a></li>
          <li><hr class="dropdown-divider" /></li>
          <li><a class="dropdown-item" href="#">AZCUBA</a></li>
          <li><hr class="dropdown-divider" /></li>
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
        <i class="bi bi-box-arrow-right"></i>
        <span class="logout-text">Cerrar sesión</span>
      </a>
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
