<template>
  <div class="content">
    <Navbar-Component />

    <!-- Barra de búsqueda -->
    <form class="d-flex" @submit.prevent="handleSearch" style="padding: 10px">
      <label for="searchQuery" style="padding-right: 10px"
        >Buscar por usuario:</label
      >
      <input
        id="searchQuery"
        class="form-control form-control-sm me-2"
        type="search"
        placeholder="Buscar por usuario..."
        aria-label="Search"
        v-model="searchQuery"
        @input="handleSearchInput"
        style="width: 200px"
      />

      <!-- Campos de filtrado por rango de fechas -->
      <label for="filterFechaInicio" style="padding-right: 10px"
        >Fecha inicio:</label
      >
      <input
        id="filterFechaInicio"
        type="date"
        class="form-control form-control-sm me-2"
        v-model="filterFechaInicio"
        @input="handleSearchInput"
        placeholder="Fecha inicio"
      />

      <label for="filterFechaFin" style="padding-right: 10px">Fecha fin:</label>
      <input
        id="filterFechaFin"
        type="date"
        class="form-control form-control-sm me-2"
        v-model="filterFechaFin"
        @input="handleSearchInput"
        placeholder="Fecha fin"
      />

      <!-- Campo de filtrado por acción -->
      <label for="filterAccion" style="padding-right: 10px">Acción:</label>
      <input
        id="filterAccion"
        type="text"
        class="form-control form-control-sm me-2"
        v-model="filterAccion"
        @input="handleSearchInput"
        placeholder="Acción"
      />
    </form>

    <!-- Tabla de auditorías -->
    <div class="table-responsive">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">No</th>
            <th scope="col">Usuario</th>
            <th scope="col">Acción</th>
            <th scope="col">Dirección IP</th>
            <th scope="col">Navegador</th>
            <th scope="col">Fecha</th>
            <th scope="col">Hora</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in auditorias" :key="item.id">
            <th scope="row" style="background-color: white">
              {{ (currentPage - 1) * itemsPerPage + index + 1 }}
            </th>
            <td>{{ item.usuario ? item.usuario : "Anónimo" }}</td>
            <td>{{ item.accion }}</td>
            <td>{{ item.direccion_ip }}</td>
            <td>{{ item.navegador }}</td>
            <td>{{ formatDate(item.fecha) }}</td>
            <td>{{ formatTime(item.fecha) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <h1 v-if="!busqueda_existente">
      No existe ningún registro asociado a ese parámetro de búsqueda
    </h1>

    <!-- Paginación -->
    <nav aria-label="Page navigation" v-if="totalPages > 1">
      <ul class="pagination justify-content-center">
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
          v-for="page in totalPagesArray"
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
.content {
  padding-left: 15%;
  align-content: center;
}
.search-container {
  padding: 10px;
}

.search-form {
  display: flex;
  justify-content: flex-end;
  margin-left: auto;
}

@media (max-width: 768px) {
  .search-form {
    margin-left: auto;
    margin-right: 10px;
  }
}
</style>

<script>
import axios from "axios";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  components: {
    NavbarComponent,
  },
  data() {
    return {
      auditorias: [], // Lista de auditorías
      searchQuery: "", // Término de búsqueda por usuario
      filterFechaInicio: "", // Filtro por fecha de inicio
      filterFechaFin: "", // Filtro por fecha de fin
      filterAccion: "", // Filtro por acción
      debounceTimeout: null, // Timeout para la búsqueda automática
      currentPage: 1, // Página actual
      itemsPerPage: 10, // Elementos por página
      totalItems: 0, // Total de elementos
      totalPages: 1, // Total de páginas
      busqueda_existente: true, // Variable para controlar la visibilidad del <h1> de la busqueda
    };
  },
  computed: {
    totalPagesArray() {
      const range = 2; // Número de páginas a mostrar a cada lado de la página actual
      const start = Math.max(1, this.currentPage - range);
      const end = Math.min(this.totalPages, this.currentPage + range);

      const pages = [];
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    },
  },
  created() {
    this.fetchAuditorias();
  },
  methods: {
    // Obtener las auditorías desde el backend
    async fetchAuditorias() {
      try {
        const fechaInicio = this.filterFechaInicio
          ? `${this.filterFechaInicio}T00:00:00`
          : null;
        const fechaFin = this.filterFechaFin
          ? `${this.filterFechaFin}T23:59:59`
          : null;

        const params = {
          usuario: this.searchQuery,
          fecha_after: fechaInicio,
          fecha_before: fechaFin,
          accion: this.filterAccion,
          page: this.currentPage,
          page_size: this.itemsPerPage,
        };
        const response = await axios.get("apiAdmin/auditoria/", { params });
        this.auditorias = response.data.results;
        this.totalItems = response.data.count;
        this.totalPages = Math.ceil(this.totalItems / this.itemsPerPage);
        this.busqueda_existente = this.auditorias.length > 0;
      } catch (error) {
        console.error("Error al obtener los datos de auditoría:", error);
        this.busqueda_existente = false;
      }
    },

    // Manejar la búsqueda
    handleSearch() {
      this.currentPage = 1; // Reiniciar a la primera página al buscar
      this.fetchAuditorias();
    },

    // Búsqueda automática con debounce
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.handleSearch();
      }, 300); // Ajusta el tiempo de espera según sea necesario
    },

    // Cambiar de página
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        this.fetchAuditorias();
      }
    },

    // Formatear la fecha
    formatDate(date) {
      if (!date) return "";
      return new Date(date).toLocaleDateString();
    },

    // Formatear la hora
    formatTime(date) {
      if (!date) return "";
      return new Date(date).toLocaleTimeString();
    },
  },
};
</script>
