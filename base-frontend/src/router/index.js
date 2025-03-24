import { createRouter, createWebHistory } from "vue-router";
import Vue from "vue";
import Router from "vue-router";
import HomeView from "../views/HomeView.vue";
import loginView from "../views/loginView.vue";
import store from "@/store";
import Usuarios from "@/views/Usuarios.vue";
import AdicionarUsuario from "@/views/AdicionarUsuario.vue";
import GroupsView from "@/views/GroupsView.vue";
import EditGroup from "@/views/EditGroup.vue";
import CreateGroup from "@/views/CreateGroup.vue";
import TrazasAuditoria from "@/views/TrazasAuditoria.vue";

const routes = [
  //para la gestion de los usuarios
  {
    path: "/Usuarios",
    name: "Usuarios",
    component: Usuarios,
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/AdicionarUsuario",
    name: "AdicionarUsuario",
    component: AdicionarUsuario,
    meta: {
      requireLogin: true,
    },
  },

  {
    path: "/editar-usuario/:id/edit",
    name: "EditarUsuario",
    component: () => import("../views/EditarUsuario.vue"),
    meta: {
      requireLogin: true,
    },
  },
  //para la gestion de los grupos de los usuarios
  {
    path: "/groups",
    name: "GroupsView",
    component: GroupsView,
  },
  {
    path: "/create-group",
    name: "CreateGroup",
    component: CreateGroup,
  },
  {
    path: "/edit-group/:id",
    name: "EditGroup",
    component: EditGroup,
  },

  {
    path: "/Trazas",
    name: "Trazas",
    component: TrazasAuditoria,
    meta: {
      requireLogin: true,
    },
  },

  {
    path: "/",
    name: "login",
    component: loginView,
  },

  {
    path: "/home",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/contenedor",
    name: "contenedor",
    component: () => import("../views/ContenedorView.vue"),
    meta: {
      requireLogin: true,
    },
  },

  {
    path: "/Cargos",
    name: "Cargos",
    component: () => import("../views/CargosView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/AdicionarCargo",
    name: "AdicionarCargo",
    component: () => import("../views/AdicionarCargoView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarCargo/:id",
    name: "EditarCargo",
    component: () => import("../views/EditarCargoView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/Paises",
    name: "paises",
    component: () => import("../views/PaisesView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/AdicionarPais",
    name: "AdicionarPais",
    component: () => import("../views/AdicionarPaisView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarPais/:id",
    name: "EditarPais",
    component: () => import("../views/EditarPaisView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/Provincia",
    name: "provincia",
    component: () => import("../views/ProvinciasView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/AdicionarProvincia",
    name: "AdicionarProvincia",
    component: () => import("../views/AdicionarProvinciaView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarProvincia/:id",
    name: "EditarProvincia",
    component: () => import("../views/EditarProvinciaView.vue"),
    meta: {
      requireLogin: true,
    },
  },

  {
    path: "/Entidades",
    name: "Entidades",
    component: () => import("../views/EntidadesView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/AdicionarEntidades",
    name: "AdicionarEntidades",
    component: () => import("../views/AdicionarEntidadView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarEntidades/:id/edit",
    name: "EditarEntidades",
    component: () => import("../views/EditarEntidadView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/Organismos",
    name: "Organismos",
    component: () => import("../views/OrganismosView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/AdicionarOrganismos",
    name: "AdicionarOrganismos",
    component: () => import("../views/AdicionarOrganismoView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarOrganismos/:id",
    name: "EditarOrganismos",
    component: () => import("../views/EditarOrganismoView.vue"),
    meta: {
      requireLogin: true,
    },
  },

  {
    path: "/CrearContenedor",
    name: "CrearContenedor",
    component: () => import("../views/CrearContenedorView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarContenedor/:id/",
    name: "EditarContenedor",
    component: () => import("../views/EditarContenedorView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/Destino",
    name: "Destino",
    component: () => import("../views/DestinoView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/AdicionarDestino",
    name: "AdicionarDestino",
    component: () => import("../views/AdicionarDestinoView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarDestino/:id/edit",
    name: "EditarDestino",
    component: () => import("../views/EditarDestinoView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/Embarcaciones",
    name: "Embarcaciones",
    component: () => import("../views/EmbarcacionView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/AdicionarEmbarcacion",
    name: "AdicionarEmbarcacion",
    component: () => import("../views/AdicionarEmbarcacionView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  //esto es de pruebaaaaa
  {
    path: "/AdicionarEmbarcacion1",
    name: "AdicionarEmbarcacion1",
    component: () => import("../views/Prueba.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarEmbarcacion/:id/edit",
    name: "EditarEmbarcacion",
    component: () => import("../views/EditarEmbarcacionView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/TipoManiobra",
    name: "TipoManiobra",
    component: () => import("../views/TipoManiobraView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/AdicionarManiobra",
    name: "AdicionarManiobra",
    component: () => import("../views/AdicionarManiobraView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarManiobra/:id/edit",
    name: "EditarManiobra",
    component: () => import("../views/EditarManiobraView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/Producto",
    name: "Producto",
    component: () => import("../views/ProductoView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/CrearProducto",
    name: "CrearProducto",
    component: () => import("../views/CrearProductoView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarProducto/:id",
    name: "EditarProducto",
    component: () => import("../views/EditarProductoView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/Territorio",
    name: "Territorio",
    component: () => import("../views/TerritorioView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/AdicionarTerritorio",
    name: "AdicionarTerritorio",
    component: () => import("../views/AdicionarTerritorioView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarTerritorio/:id/edit",
    name: "EditarTerritorio",
    component: () => import("../views/EditarTerritorioView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EquipoFerro",
    name: "EquipoFerro",
    component: () => import("../views/EquipoFerroView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/AdicionarEquipo",
    name: "AdicionarEquipo",
    component: () => import("../views/AdicionarEquipoView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarEquipo/:id/edit",
    name: "EditarEquipo",
    component: () => import("../views/EditarEquipoView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EstadoTecnico",
    name: "EstadoTecnico",
    component: () => import("../views/EstadoTecnicoView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/AdicionarEstadoTecnico",
    name: "AdicionarEstadoTecnico",
    component: () => import("../views/AdicionarEstadoTecnico.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarEstadoTecnico/:id",
    name: "EditarEstadoTecnico",
    component: () => import("../views/EditarEstadoTecnico.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/TipoEquipoFerro",
    name: "TipoEquipoFerro",
    component: () => import("../views/TipoEquipoFerroView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/AdicionarTipoEquipo",
    name: "AdicionarTipoEquipo",
    component: () => import("../views/AdicionarTipoEquipoView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarTipoEquipoFerro/:id/edit",
    name: "EditarTipoEquipoFerro",
    component: () => import("../views/EditarTipoEquipoFerroView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/UM",
    name: "UM",
    component: () => import("../views/UMView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/AdicionarUM",
    name: "AdicionarUM",
    component: () => import("../views/AdicionarUMView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarUM/:id/edit",
    name: "EditarUM",
    component: () => import("../views/EditarUMView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/Atraques",
    name: "Atraques",
    component: () => import("../views/AtraquesView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/AdicionarAtraque",
    name: "AdicionarAtraque",
    component: () => import("../views/AdicionarAtraqueView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarAtraque/:id/",
    name: "EditarAtraque",
    component: () => import("../views/EditarAtraqueView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EstructuraUbicacion",
    name: "EstructuraUbicacion",
    component: () => import("../views/EstructuradeUbicacion.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/AdicionarEstructura",
    name: "AdicionarEstructura",
    component: () => import("../views/CrearEstructuradeUbicacion.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarEstructura/:id",
    name: "EditarEstructura",
    component: () => import("../views/EditarEstructuradeUbicacion.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/Incidencias",
    name: "Incidencias",
    component: () => import("../views/Incidencias.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/CrearIncidencia",
    name: "CrearIncidencia",
    component: () => import("../views/CrearIncidencia.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarIncidencia/:id/edit",
    name: "EditarIncidencia",
    component: () => import("../views/EditarIncidencia.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/Puertos",
    name: "Puertos",
    component: () => import("../views/PuertoView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/CrearPuerto",
    name: "CrearPuerto",
    component: () => import("../views/CrearPuertoView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarPuerto/:id/edit",
    name: "EditarPuerto",
    component: () => import("../views/EditarPuertoView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/Terminal",
    name: "Terminal",
    component: () => import("../views/TerminalView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/CrearTerminal",
    name: "CrearTerminal",
    component: () => import("../views/CrearTerminalView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarTerminal/:id/edit",
    name: "EditarTerminal",
    component: () => import("../views/EditarTerminalView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/TipoEstructuraUbicacion",
    name: "TipoEstructuraUbicacion",
    component: () => import("../views/TipoEstructuraUbicacionView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/CrearTipoUbicacion",
    name: "CrearTipoUbicacion",
    component: () => import("../views/CrearTipoUbicacionView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarTipoUbicacion/:id/edit",
    name: "EditarTipoUbicacion",
    component: () => import("../views/EditarTipoUbicacionView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/TipoEmbalaje",
    name: "TipoEmbalaje",
    component: () => import("../views/TipoEmbalajeView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/EditarTipoEmbalaje/:id/edit",
    name: "EditarTipoEmbalaje",
    component: () => import("../views/EditarTipoEmbalajeView.vue"),
    meta: {
      requireLogin: true,
    },
  },
  {
    path: "/AdicionarTipoEmbalaje",
    name: "AdicionarTipoEmbalaje",
    component: () => import("../views/AdicionarTipoEmbalajeView.vue"),
    meta: {
      requireLogin: true,
    },
  },

  {
    path: "/ufc",
    name: "ufc",
    component: () => import("../views/UFCView.vue"),
    meta: {
      requireLogin: true,
    },
  },

  {
    path: "/InfoOperativo",
    name: "InfoOperativo",
    component: () => import("../views/InformeOperativoView.vue"),
    meta: {
      requireLogin: true,
    },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

/*el siguiente codigo es para que en caso de que no este autenticado redireccione a la pagina del login, en caso contrario 
redirecciona a donde se desea ir */
router.beforeEach((to, from, next) => {
  if (
    to.matched.some((record) => record.meta.requireLogin) &&
    !store.state.isAuthenticated
  ) {
    next("/");
  } else {
    next();
  }
});

export default router;
