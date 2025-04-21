<template>
  <div class="container py-3">
    <!-- Encabezado con acciones -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <router-link
        v-if="hasPermission"
        to="/AgregarArrastre"
        class="btn btn-link"
        title="Agregar nuevo vagón"
      >
        <i class="bi bi-plus-circle fs-3"></i>
      </router-link>

      <form @submit.prevent="searchTrenes" class="search-container">
        <div class="input-group">
          <span class="input-group-text">
            <i class="bi bi-search"></i>
          </span>
          <input
            type="search"
            class="form-control"
            placeholder="Origen, Destino, Producto, Locomotora"
            v-model="searchQuery"
            @input="handleSearchInput"
          />
        </div>
      </form>
    </div>

    <!-- Tabla responsive -->
    <div class="table-responsive">
      <table class="table table-hover mb-0">
        <thead>
          <tr>
            <th scope="col" style="width: 50px">#</th>
            <th scope="col">Origen</th>
            <th scope="col">Tipo de origen</th>
            <th scope="col">Estado</th>
            <th scope="col">Producto</th>
            <th scope="col" class="text-end">Cant. Vagones</th>
            <th scope="col">Destino</th>
            <th scope="col" v-if="hasPermission" style="width: 120px">
              Acciones
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(tren, index) in paginatedTrenes"
            :key="tren.id"
            class="align-middle"
          >
            <th scope="row">
              {{ (currentPage - 1) * itemsPerPage + index + 1 }}
            </th>
            <td>{{ tren.origen || "-" }}</td>
            <td>{{ getTipoOrigenText(tren.tipo_origen) || "-" }}</td>
            <td>
              <span :class="`badge bg-${getEstadoBadge(tren.estado)}`">
                {{ getEstadoText(tren.estado) || "-" }}
              </span>
            </td>
            <td>{{ getProductoText(tren.producto) || "-" }}</td>
            <td class="text-end">{{ tren.cantidad_vagones || "0" }}</td>
            <td>{{ tren.destino || "-" }}</td>
            <td v-if="hasPermission">
              <div class="d-flex">
                <router-link
                  :to="`/editar/${tren.id}`"
                  class="btn btn-sm btn-outline-warning me-2"
                  title="Editar"
                >
                  <i class="bi bi-pencil-square"></i>
                </router-link>
                <button
                  @click="confirmDelete(tren.id)"
                  class="btn btn-sm btn-outline-danger"
                  title="Eliminar"
                >
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="filteredTrenes.length === 0">
            <td colspan="8" class="text-center text-muted py-4">
              No se encontraron resultados
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Paginación -->
    <div class="d-flex justify-content-between align-items-center mt-3">
      <div class="text-muted small">
        Mostrando {{ paginatedTrenes.length }} de
        {{ filteredTrenes.length }} registros
      </div>
      <nav aria-label="Page navigation">
        <ul class="pagination pagination-sm mb-0">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link" @click="previousPage">
              <i class="bi bi-chevron-left"></i>
            </button>
          </li>
          <li class="page-item disabled">
            <span class="page-link">
              Página {{ currentPage }} de {{ totalPages }}
            </span>
          </li>
          <li
            class="page-item"
            :class="{ disabled: currentPage >= totalPages }"
          >
            <button class="page-link" @click="nextPage">
              <i class="bi bi-chevron-right"></i>
            </button>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Swal from 'sweetalert2'

export default {
  name: "PendientesArrastre",
  data() {
    return {
      en_trenes: [],
      searchQuery: "",
      currentPage: 1,
      itemsPerPage: 10,
      hasPermission: true,
      loading: false,

      tipo_origen_options: [
        { id: "puerto", text: "Puerto" },
        { id: "acceso_comercial", text: "Acceso Comercial" },
      ],
      tipo_equipo_options: [
        { id: "casilla", text: "Casilla" },
        { id: "cajon_gondola", text: "Cajón o Góndola" },
      ],
      estado_options: [
        { id: "vacio", text: "Vacío" },
        { id: "cargado", text: "Cargado" },
      ],
      producto_options: [
        { id: "granos", text: "Granos" },
        { id: "minerales", text: "Minerales" },
        { id: "combustible", text: "Combustible" },
      ],
    }
  },
  computed: {
    filteredTrenes() {
      if (!this.searchQuery) {
        return this.en_trenes;
      }

      const query = this.searchQuery.toLowerCase();
      return this.en_trenes.filter(
        (tren) =>
          (tren.origen && tren.origen.toLowerCase().includes(query)) ||
          (tren.destino && tren.destino.toLowerCase().includes(query)) ||
          (this.getProductoText(tren.producto) &&
            this.getProductoText(tren.producto)
              .toLowerCase()
              .includes(query)) ||
          (tren.cantidad_vagones &&
            tren.cantidad_vagones.toString().includes(query))
      );
    },
    paginatedTrenes() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredTrenes.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredTrenes.length / this.itemsPerPage);
    },
  },
  created() {
    this.fetchTrenes();
  },
  methods: {
    async fetchTrenes() {
      this.loading = true;
      try {
        const response = await axios.get("/ufc/pendiente-arrastre/");
        this.en_trenes = response.data.results;
      } catch (error) {
        console.error("Error al obtener los trenes:", error);
        Swal.fire("Error", "No se pudieron cargar los trenes", "error");
      } finally {
        this.loading = false;
      }
    },

    getTipoOrigenText(id) {
      const option = this.tipo_origen_options.find((o) => o.id === id);
      return option ? option.text : id;
    },

    getEstadoText(id) {
      const option = this.estado_options.find((o) => o.id === id);
      return option ? option.text : id;
    },

    getEstadoBadge(id) {
      return id === "cargado" ? "success" : "secondary";
    },

    getProductoText(id) {
      const option = this.producto_options.find((o) => o.id === id);
      return option ? option.text : id;
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchTrenes();
      }, 500);
    },

    searchTrenes() {
      this.currentPage = 1;
    },

    confirmDelete(id) {
      Swal.fire({
        title: "¿Estás seguro?",
        text: "No podrás revertir esta acción",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
      }).then((result) => {
        if (result.isConfirmed) {
          this.deleteTren(id);
        }
      });
    },

    async deleteTren(id) {
      try {
        await axios.delete(`/ufc/pendiente-arrastre/${id}/`);
        this.en_trenes = this.en_trenes.filter((t) => t.id !== id);
        Swal.fire("Eliminado", "El tren ha sido eliminado", "success");
      } catch (error) {
        console.error("Error al eliminar el tren:", error);
        Swal.fire("Error", "No se pudo eliminar el tren", "error");
      }
    },

    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },

    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
  }
}
</script>

<style scoped>
.search-container {
  position: relative;
  width: 100%;
  max-width: 400px;
}

.table-responsive {
  overflow-x: auto;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.table th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.btn-link {
  color: #007bff;
  text-decoration: none;
}

.btn-link:hover {
  color: #0056b3;
}

.badge {
  font-weight: 500;
  padding: 5px 10px;
  border-radius: 4px;
}

.bg-success {
  background-color: #28a745 !important;
}

.bg-secondary {
  background-color: #6c757d !important;
}

.pagination .page-link {
  border-radius: 4px;
  margin: 0 3px;
}

.pagination .page-item.disabled .page-link {
  opacity: 0.6;
}

.pagination .page-item:not(.disabled) .page-link:hover {
  background-color: #f8f9fa;
}
</style>