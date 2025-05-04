<template>
  <div>
    <div style="background-color: #002a68; color: white; text-align: right">
      <h6>Bienvenido:</h6>
    </div>
    <br />
    <Navbar-Component />
    <br />
    <br />
    <div class="search-container">
      <form class="d-flex search-form" @submit.prevent="search_tipo_equipo">
        <div class="input-container">
          <i class="bi bi-search"></i>
          <input
            class="form-control form-control-sm me-2"
            type="search"
            placeholder=" tipo de carga"
            aria-label="Buscar"
            v-model="searchQuery"
            @input="handleSearchInput"
            style="width: 200px; padding-left: 5px; margin-top: -70px"
          />
        </div>
      </form>
    </div>
    <div class="create-button-container">
      <router-link
        v-if="hasGroup('Admin')"
        class="create-button"
        to="AdicionarTipoEquipo"
      >
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h3
      style="
        margin-top: -33px;
        font-size: 18px;
        margin-right: 440px;
        color: #002a68;
      "
    >
      Listado de tipos de equipos ferroviarios
    </h3>
    <br />
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Tipo de equipo</th>
            <th scope="col">Tipo de carga</th>
            <th scope="col">Tipo de combustible</th>
            <th scope="col">Longitud</th>
            <th scope="col">Peso neto sin carga</th>
            <th scope="col">Peso máximo con carga</th>
            <th scope="col">Capacidad cúbica máxima</th>
            <th scope="col">Descripción</th>
            <th scope="col">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in tipos_equipos" :key="item.id">
            <td>{{ getTipoEquipoText(item.tipo_equipo) }}</td>
            <td>{{ getTipoCargaText(item.tipo_carga) }}</td>
            <td>{{ getTipoCombustibleText(item.tipo_combustible) }}</td>
            <td>{{ item.longitud }}</td>
            <td>{{ item.peso_neto_sin_carga }}</td>
            <td>{{ item.peso_maximo_con_carga }}</td>
            <td>{{ item.capacidad_cubica_maxima }}</td>
            <td>{{ item.descripcion }}</td>
            <td>
              <button
                @click="openTipoEquipoFerroDetailsModal(item)"
                class="btn btn-info btn-small btn-eye"
                v-html="
                  showNoId
                    ? '<i class=\'bi bi-eye-slash-fill\'></i>'
                    : '<i class=\'bi bi-eye-fill\'></i>'
                "
              ></button>
              <span v-if="hasGroup('Admin')">
                <button class="btn btn-warning btn-small">
                  <router-link
                    :to="{
                      name: 'EditarTipoEquipoFerro',
                      params: { id: item.id },
                    }"
                  >
                    <i style="color: black" class="bi bi-pencil-square"></i>
                  </router-link>
                </button>
                <button
                  @click.prevent="confirmDelete(item.id)"
                  class="btn btn-danger btn-small"
                >
                  <i class="bi bi-trash"></i>
                </button>
              </span>
            </td>
          </tr>
        </tbody>
      </table>
      <h1 v-if="!busqueda_existente">
        No existe ningún registro asociado a ese parámetro de búsqueda.
      </h1>
    </div>
    <!-- Paginación -->
    <nav aria-label="Page navigation example">
      <ul class="pagination">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <a
            class="page-link"
            href="#"
            @click.prevent="changePage(currentPage - 1)"
            >Anterior</a
          >
        </li>
        <li
          class="page-item"
          v-for="page in pages"
          :key="page"
          :class="{ active: page === currentPage }"
        >
          <a class="page-link" href="#" @click.prevent="changePage(page)">{{
            page
          }}</a>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <a
            class="page-link"
            href="#"
            @click.prevent="changePage(currentPage + 1)"
            >Siguiente</a
          >
        </li>
      </ul>
    </nav>
  </div>
</template>

<style scoped>
.search-container input::placeholder {
  font-size: 14px;
  color: #999;
}

body {
  overflow: scroll;
}

.search-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 5px;
}

.table-container {
  overflow-x: auto;
  max-width: 100%;
}
.input-container {
  position: relative;
  display: inline-block;
}

.input-container .bi {
  position: absolute;
  left: 180px;
  color: #999;
  margin-top: -55px;
  transform: translateY(-50%);
  pointer-events: none; /* Para que el ícono no interfiera con el clic en el input */
}
.large-icon {
  font-size: 1.7rem; /* Tamaño del ícono */
}
table {
  width: 84%;
  border-collapse: collapse;
  margin-left: 190px;
  margin-bottom: 10px;
  font-size: 0.875rem;
}
nav .pagination {
  display: flex;
  justify-content: center;
  align-items: center;
}
th,
td {
  padding: 0.15rem; /* Reducir el padding */
  white-space: nowrap;
}

th {
  background-color: #f2f2f2;
}

.btn {
  cursor: pointer;
}

.btn-small {
  font-size: 22px; /* Aumenta el tamaño del ícono */
  color: black;
  margin-right: 5px;
  outline: none; /* Elimina el borde de foco */
  border: none;
  background: none; /* Elimina el fondo */
  padding: 0; /* Elimina el padding para que solo se vea el ícono */
}
.btn-eye {
  font-size: 22px; /* Aumenta el tamaño del ícono */
  margin-right: 5px;
  outline: none; /* Elimina el borde de foco */
  border: none;
  background: none; /* Elimina el fondo */
  padding: 0; /* Elimina el padding para que solo se vea el ícono */
}
.btn:hover {
  background: none; /* Asegura que no haya fondo al hacer hover */
}

.btn:focus {
  outline: none; /* Elimina el borde de foco al hacer clic */
  box-shadow: none; /* Elimina cualquier sombra de foco en algunos navegadores */
}

.create-button-container {
  margin-top: -80px;
  text-align: left;
}

.create-button {
  text-decoration: none;
  color: green;
  margin-left: 940px;
}

@media (max-width: 768px) {
  .create-button-container {
    text-align: left;
    margin-right: 0;
  }
}
</style>

<script>
import Swal from "sweetalert2";
import axios from "axios";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "TipoEquipoFerro",

  components: {
    NavbarComponent,
  },

  data() {
    return {
      tipos_equipos: [],
      searchQuery: "", // Término de búsqueda
      debounceTimeout: null, // Timeout para el debounce
      busqueda_existente: true, // Variable para controlar la visibilidad del mensaje de búsqueda
      userPermissions: [], // Permisos del usuario
      userGroups: [], // Grupos del usuario
      showNoId: false,
      currentPage: 1, // Página actual
      totalPages: 1, // Total de páginas
      pages: [], // Lista de páginas visibles
    };
  },

  mounted() {
    this.get_tipos_equipos();
  },

  async created() {
    // Obtener los permisos y grupos del usuario al cargar el componente
    await this.fetchUserPermissionsAndGroups();
  },

  methods: {
    toggleNoIdVisibility() {
      this.showNoId = !this.showNoId; // Alternar la visibilidad de las columnas No e Id
    },
    // Verifica si el usuario tiene un permiso específico
    hasPermission(permission) {
      if (!this.userPermissions) return false; // Verificación adicional
      return this.userPermissions.some((p) => p.name === permission);
    },
    hasGroup(group) {
      if (!this.userGroups) return false; // Verificación adicional
      return this.userGroups.some((g) => g.name === group);
    },
    // Obtiene los permisos y grupos del usuario desde el backend
    async fetchUserPermissionsAndGroups() {
      try {
        const userId = localStorage.getItem("userid");
        if (userId) {
          const response = await axios.get(
            `/apiAdmin/user/${userId}/permissions-and-groups/`
          );
          this.userPermissions = response.data.permissions || []; // Inicializa como array vacío si es undefined
          this.userGroups = response.data.groups || []; // Inicializa como array vacío si es undefined
        }
      } catch (error) {
        console.error("Error al obtener permisos y grupos:", error);
      }
    },
    async get_tipos_equipos() {
      this.$store.commit("setIsLoading", true);
      try {
        const response = await axios.get("/api/tipos_equipos/", {
          params: {
            page: this.currentPage,
            search: this.searchQuery,
          },
        });
        this.tipos_equipos = response.data.results; // Obtener los registros de la página actual
        this.totalPages = Math.ceil(response.data.count / 15); // Calcular el número total de páginas
        this.updatePages(); // Actualizar la lista de páginas visibles
        this.busqueda_existente = true; // Reinicia la variable al cargar todos los tipos de equipos
      } catch (error) {
        console.error("Error al obtener los tipos de equipos:", error);
        Swal.fire(
          "Error",
          "No se pudieron cargar los tipos de equipos.",
          "error"
        );
      }
      this.$store.commit("setIsLoading", false);
    },
    // Método para buscar registros en base al parámetro de búsqueda
    async search_tipo_equipo() {
      this.$store.commit("setIsLoading", true);

      axios
        .get(
          `/api/tipos_equipos/?busqueda_tipo_equipo__tipo_carga=${this.searchQuery}`
        )
        .then((response) => {
          this.tipos_equipos = response.data.results;
          // Actualiza busqueda_existente basado en el resultado
          this.busqueda_existente = this.tipos_equipos.length > 0;
        })
        .catch((error) => {
          console.log(error);
          this.busqueda_existente = false; // Asegura que busqueda_existente sea false en caso de error
        });

      this.$store.commit("setIsLoading", false);
    },
    updatePages() {
      const startPage = Math.max(1, this.currentPage - 2); // Mostrar 2 páginas antes de la actual
      const endPage = Math.min(this.totalPages, this.currentPage + 2); // Mostrar 2 páginas después de la actual
      this.pages = [];
      for (let i = startPage; i <= endPage; i++) {
        this.pages.push(i);
      }
    },

    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        this.get_tipos_equipos();
      }
    },
    // Usar SweetAlert2 para confirmar la eliminación
    confirmDelete(id) {
      Swal.fire({
        title: "¿Estás seguro?",
        text: "¡No podrás revertir esta acción!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
        reverseButtons: true,
      }).then((result) => {
        if (result.isConfirmed) {
          this.delete_tipo_equipo(id);
        }
      });
    },
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.search_tipo_equipo();
      }, 300); // Ajusta el tiempo de espera según sea necesario
    },
    // Eliminar tipo de equipo
    async delete_tipo_equipo(id) {
      try {
        await axios.delete(`/api/tipos_equipos/${id}/`);
        // Actualizar la lista de tipos de equipo eliminando el que se ha borrado
        this.tipos_equipos = this.tipos_equipos.filter(
          (tipo_equipo) => tipo_equipo.id !== id
        );
        Swal.fire(
          "Eliminado!",
          "El tipo de equipo ferroviario ha sido eliminado exitosamente.",
          "success"
        );
      } catch (error) {
        console.error(
          "Error al eliminar el tipo de equipo ferroviario:",
          error
        );
        Swal.fire(
          "Error",
          "Hubo un error al eliminar el tipo de equipo ferroviario.",
          "error"
        );
      }
    },
    // Función para que sea mostrado el texto asociado al valor del select
    getTipoEquipoText(value) {
      const tiposEquipos = {
        casilla: "Casilla",
        caj_gon: "Cajones o Góndola",
        planc_plat: "Plancha o Plataforma",
        Plan_porta_cont: "Plancha porta contenedores",
        cist_liquidos: "Cisterna para líquidos",
        cist_solidos: "Cisterna para sólidos",
        tolva_g_mineral: "Tolva granelera(mineral)",
        tolva_g_agric: "Tolva granelera(agrícola)",
        tolva_g_cemento: "Tolva para cemento",
        volqueta: "Volqueta",
        Vagon_ref: "Vagón refrigerado",
        jaula: "Jaula",
        locomotora: "Locomotora",
        tren: "Tren",
        // Añade aquí todos los tipos de equipo que necesites
      };
      return tiposEquipos[value] || "Desconocido";
    },
    getTipoCargaText(value) {
      const tiposCarga = {
        combustible: "Combustible",
        aceite: "Aceite",
        miel: "Miel",
        alcohol: "Alcohol",
        quimicos: "Químicos",
        contenedores: "Contenedores",
        otros: "Otros",
        // Añade aquí todos los tipos de carga que necesites
      };
      return tiposCarga[value] || "Desconocido";
    },
    getTipoCombustibleText(value) {
      const tiposCombustible = {
        combust_blanco: "Combustible blanco",
        combustible_negro: "Combustible negro",
        combustible_turbo: "Combustible turbo",
        // Añade aquí todos los tipos de combustible que necesites
      };
      return tiposCombustible[value] || "Desconocido";
    },
    openTipoEquipoFerroDetailsModal(TipoEquipoFerro) {
      // Mapear IDs de grupos a nombres
      const gruposAsignados =
        TipoEquipoFerro.groups && TipoEquipoFerro.groups.length > 0
          ? TipoEquipoFerro.groups
              .map((groupId) => {
                const grupo = this.gruposDisponibles.find(
                  (g) => g.id === groupId
                );
                return grupo ? grupo.name : "Desconocido";
              })
              .join(", ")
          : "Ninguno";

      // Mapear IDs de permisos a nombres
      const permisosAsignados =
        TipoEquipoFerro.TipoEquipoFerro_permissions &&
        TipoEquipoFerro.TipoEquipoFerro_permissions.length > 0
          ? TipoEquipoFerro.TipoEquipoFerro_permissions.map((permisoId) => {
              const permiso = this.permisosDisponibles.find(
                (p) => p.id === permisoId
              );
              return permiso ? permiso.name : "Desconocido";
            }).join(", ")
          : "Ninguno";

      Swal.fire({
        title: "Detalles del Atraque",
        html: `
            <div style="text-align: left;">
                <p><strong>Tipo de equipo:</strong> ${TipoEquipoFerro.tipo_equipo}</p>
                <p><strong>Tipo de carga:</strong> ${TipoEquipoFerro.tipo_carga}</p>
                <p><strong>Tipo de combustible:</strong> ${TipoEquipoFerro.tipo_combustible}</p>
                 <p><strong>Logitud:</strong> ${TipoEquipoFerro.longitud}</p>
                <p><strong>Peso neto sin carga:</strong> ${TipoEquipoFerro.peso_neto_sin_carga}</p>
                <p><strong>Peso máximo con carga:</strong> ${TipoEquipoFerro.peso_maximo_con_carga}</p>
                 <p><strong>Capacidad cúbica máxima:</strong> ${TipoEquipoFerro.capacidad_cubica_maxima}</p>
                <p><strong>Descripción:</strong> ${TipoEquipoFerro.descripcion}</p>
            </div>
        `,
        width: "600px",
        customClass: {
          popup: "custom-swal-popup",
          title: "custom-swal-title",
          htmlContainer: "custom-swal-html",
        },
      });
    },
  },
};
</script>
