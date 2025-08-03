<template>
  <nav
    class="navbar navbar-expand d-flex flex-column align-items-start navbar-dark p-0"
    style="width: 250px; height: 100vh;"
    role="navigation"
    aria-label="Main navigation"
  >
    <!-- Logo/Texto de la empresa -->
    <div class="logo-container">
      <h1 class="company-name">MITRANS</h1>
      <p class="company-slogan">Transporte y Logística</p>
    </div>

    <!-- Contenedor principal del menú con scroll -->
    <div>
      <ul class="navbar-nav w-100 flex-column">
        <li
          v-for="(item, index) in menuItems"
          :key="index"
          class="nav-item"
          @click="insertRouteMain(item.title)"
        >
          <a
            class="nav-link px-3 py-3 d-flex align-items-center"
            role="button"
            @click="toggleDropdown(index)"
            :aria-expanded="isOpen(index)"
            :aria-controls="'submenu-' + index"
          >
            <span
              ><i
                style="margin-right: 10px"
                :class="`bi bi-${item.icon} me-1 fs-5`"
              ></i
              >{{ item.title }}
              <span
                v-if="
                  item.title != 'Home' &&
                  item.title != 'Reportes' &&
                  item.title != 'Cerrar sesión'
                "
                class="dropdown-indicator"
                aria-hidden="true"
              >
                {{ isOpen(index) ? "↑" : "↓" }}
              </span>
            </span>
          </a>
          <ul
            :id="'submenu-' + index"
            class="submenu w-100 flex-column"
            v-show="isOpen(index)"
            role="menu"
          >
            <li
              v-for="(subitem, subindex) in item.submenu"
              :key="subindex"
              class="submenu-item"
              role="menuitem"
            >
              <a
                class="submenu-link px-2 py-2 d-flex align-items-center"
                role="button"
                @click="insertRoute(subitem.route)"
                ><i
                  style="margin-right: 10px"
                  :class="`bi bi-${subitem.icon} me-2 fs-5`"
                ></i>
                {{ subitem.title }}
              </a>
            </li>
          </ul>
        </li>
      </ul>
      <div class="bubbles-container">
        <div class="bubble bubble-1"></div>
        <div class="bubble bubble-2"></div>
        <div class="bubble bubble-3"></div>
        <div class="bubble bubble-4"></div>
        <div class="bubble bubble-5"></div>
      </div>
    </div>

    <!-- Contenedor de burbujas (fijo al final) -->
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
      openIndexes: -1,
      iconName: "house",
      menuItems: [
        {
          title: "Home",
          icon: "houses-fill",
        },
        {
          title: "Seguridad",
          icon: "shield-lock",
          submenu: [
            { title: "Usuarios", route: "/Usuarios", icon: "person" },
            { title: "Grupos", route: "/groups", icon: "people" },
            { title: "Trazas", route: "/Trazas", icon: "list-check" },
          ],
        },
        {
          title: "Nomencladores",
          icon: "list-task",
          submenu: [
            { title: "Atraques", route: "/Atraques", icon: "bounding-box" },
            { title: "Cargos", route: "/Cargos", icon: "person-badge" },
            { title: "Contenedores", route: "/contenedor", icon: "box-seam" },
            { title: "Destinos", route: "/Destino", icon: "geo-alt" },
            { title: "Embarcaciones", route: "/Embarcaciones", icon: "water" },
            { title: "Entidades", route: "/Entidades", icon: "building" },
            {
              title: "Equipos ferroviarios",
              route: "/EquipoFerro",
              icon: "train-freight-front",
            },
            {
              title: "Estados técnicos",
              route: "/EstadoTecnico",
              icon: "tools",
            },
            {
              title: "Estruct. de ubicación",
              route: "/EstructuraUbicacion",
              icon: "layers",
            },
            {
              title: "Incidencias",
              route: "/Incidencias",
              icon: "exclamation-triangle",
            },
            {
              title: "OSDE/OACE",
              route: "/Organismos",
              icon: "building-gear",
            },
            { title: "Países", route: "/Paises", icon: "globe-americas" },
            { title: "Productos", route: "/Producto", icon: "box-seam" },
            { title: "Provincias", route: "/Provincia", icon: "map" },
            { title: "Puertos", route: "/Puertos", icon: "geo" },
            { title: "Terminales", route: "/Terminal", icon: "terminal" },
            { title: "Territorios", route: "/Territorio", icon: "pin-map" },
            {
              title: "Tipos de embalajes",
              route: "/TipoEmbalaje",
              icon: "box-seam",
            },
            {
              title: "Tipos de equipos",
              route: "/TipoEquipoFerro",
              icon: "train-lightrail-front",
            },
            {
              title: "Tipos de estructuras",
              route: "/TipoEstructuraUbicacion",
              icon: "layer-forward",
            },
            {
              title: "Tipos de maniobras",
              route: "/TipoManiobra",
              icon: "arrow-left-right",
            },
            { title: "Unidades de medida", route: "/UM", icon: "rulers" },
          ],
        },
        {
          title: "Partes",
          icon: "file-earmark-text",
          submenu: [
            { title: "Registro de Informes", route: "/ufc", icon: "table" },
            { title: "Informe Operativo", route: "/InfoOperativo", icon: "file-earmark-text" },
            { title: "CCD Producto", route: "/ccdxproducto", icon: "file-earmark-spreadsheet" },
          ],
        },
        {
          title: "Reportes",
          icon: "file-earmark-bar-graph",
        },
        {
          title: "Cerrar sesión",
          icon: "box-arrow-right",
        },
      ],
    };
  },
  async created() {
    await this.fetchUserPermissionsAndGroups();
  },
  methods: {
    toggleDropdown(index) {
      if (this.isOpen(index)) {
        this.openIndexes = -1;
      } else {
        this.openIndexes = index;
      }
    },
    isOpen(index) {
      return this.openIndexes == index;
    },
    insertRouteMain(title) {
      if (title == "Home") {
        this.$router.push("/home");
      } else if (title == "Reportes") {
        this.$router.push("/reportes");
      } else if (title == "Cerrar sesión") {
        this.logout();
      }
    },
    insertRoute(route) {
      console.log(route);
      this.$router.push(route);
    },
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
        this.$store.commit("setAuthentication", false);
        this.$router.push("/");
      } catch (error) {
        console.log(JSON.stringify(error));
      }
    },
  },
};
</script>

<style scoped>
/* Estructura principal */
.navbar {
  max-height: 100%;
  overflow-y: auto;
  position: fixed;
  top: 0;
  left: 0%;
  padding: 0;
  background-color: #002d69;
  transition: width 0.3s ease;

  /* Firefox */
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.5) transparent;

  /* Safari/Chrome/Edge (WebKit) */
  &::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
    border-radius: 10px;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.5);
    border-radius: 10px;
    border: 2px solid transparent;
    background-clip: content-box;
    transition: background-color 0.3s ease;
  }

  &::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.7);
  }
}

/* Logo */
.logo-container {
  padding: 20px;
  text-align: center;
  flex-shrink: 0;
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

/* Contenedor de burbujas (fijo al final) */
.bubbles-container {
  height: 150px;
  width: 240px;
  position: relative;
  flex-shrink: 0;
  overflow: hidden;
  z-index: 0;
}

.bubble {
  position: absolute;
  bottom: -100px;
  background-color: rgba(255, 255, 255, 0.46);
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
    bottom: 150px;
    transform: translateX(0);
    opacity: 0;
  }
}

/* Estilos del menú */
.nav-item {
  position: relative;
  text-decoration: none !important;
}

.navbar-nav .nav-link {
  color: #eeeded;
  font-weight: bold;
  transition: all 0.3s ease;
  text-decoration: none !important;
}

.navbar-nav .nav-link:hover {
  background-color: #eeeded;
  color: #002d69 !important;
  border-radius: 5px;
  text-decoration: none !important;
}

.navbar-nav .nav-link:hover .bi {
  color: #002d69 !important;
}

.submenu {
  padding-left: 20px;
  text-decoration: none !important;
}

.submenu .submenu-link {
  color: #eeeded;
  font-weight: bold;
  transition: all 0.3s ease;
  text-decoration: none !important;
}

.submenu .submenu-link:hover {
  background-color: #eeeded;
  color: #002d69 !important;
  border-radius: 5px;
  text-decoration: none !important;
}
</style>
