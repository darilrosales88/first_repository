<template>
  <div>
    <div style="background-color: #002a68; color: white; text-align: right">
      <h6>Bienvenido:</h6>
    </div>
    <Navbar-Component />
    <div class="container py-3" style="margin-left: 17em; width: 79%">
      <div class="card border">
        <div class="card-header bg-light border-bottom">
          <h6 class="mb-0 text-dark fw-semibold">
            Listado de Embarcaciones
          </h6>
        </div>
        <div class="card-body p-3">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <router-link v-if="hasGroup('Admin')" to="/AdicionarEmbarcacion">
              <button class="btn btn-sm btn-primary">
                <i class="bi bi-plus-circle me-1"></i>Agregar nueva embarcación
              </button>
            </router-link>
            <form @submit.prevent="SearchAtraque" class="search-container">
              <div class="input-group">
                <input
                  type="search"
                  class="form-control"
                  placeholder="Buscar por nombre, tipo o nacionalidad"
                  v-model="searchQuery"
                  @input="handleSearchInput"/>
                <span class="position-absolute top-50 start-0 translate-middle-y ps-2">
                  <i class="bi bi-search"></i>
                </span>
              </div>
            </form>
          </div>
          <div class="table table-responsive">
            <table class="table table-sm table-bordered table-hover" >
              <thead class="table-light">
                <tr>
                  <th scope="col">Nombre</th>
                  <th scope="col">Nacionalidad</th>
                  <th scope="col">Eslora</th>
                  <th scope="col">Manga</th>
                  <th scope="col">Calado máximo</th>
                  <th scope="col">Desplazamiento máximo</th>
                  <th scope="col">Tipo de embarcación</th>
                  <th scope="col">Tipo de buque</th>
                  <th scope="col">Tipo de patana</th>
                  <th scope="col">IMO</th>
                  <th scope="col">Potencia</th>
                  <th scope="col">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in embarcaciones" :key="item.id">
                  <td>{{ item.nombre_embarcacion }}</td>
                  <td>{{ item.nacionalidad_name }}</td>
                  <td>{{ item.eslora }}</td>
                  <td>{{ item.manga }}</td>
                  <td>{{ item.calado_maximo }}</td>
                  <td>{{ item.desplazamiento_maximo }}</td>
                  <td>{{ getTipoEmbarcacionText(item.tipo_embarcacion) }}</td>
                  <td>{{ getTipoBuqueText(item.tipo_buque) }}</td>
                  <td>{{ getTipoPatanaText(item.tipo_patana) }}</td>
                  <td>{{ item.imo }}</td>
                  <td>{{ item.potencia }}</td>
                  <td>
                    <div class="d-flex">
                      <button 
                        @click="openatraqueDetailsModal(item)"
                        class="btn btn-sm btn-outline-info me-2"
                        title="Ver detalles">
                        <i class="bi bi-eye-fill"></i>
                      </button>
                      <button v-if="hasGroup('Admin')"
                        @click="edit(item)"
                        class="btn btn-sm btn-outline-warning me-2"
                        title="Editar"> 
                        <i class="bi bi-pencil-square"></i>
                      </button>

                      <button v-if="hasGroup('Admin')"
                        @click.prevent="confirmDelete(item.id)"
                        class="btn btn-sm btn-outline-danger"
                        title="Eliminar">
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            <!-- Mensaje cuando no hay resultados -->
            <h1 v-if="!busqueda_existente">
              No existe ningún registro asociado a ese parámetro de búsqueda.
            </h1>
          </div>
          <!-- Paginación -->
          <nav aria-label="Page navigation example" style="margin-left: 30%;">
            <ul class="pagination">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">Anterior</a>
              </li>
              <li class="page-item" v-for="page in pages" :key="page":class="{ active: page === currentPage }">
                <a class="page-link" href="#" @click.prevent="changePage(page)">{{page}}</a>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">Siguiente</a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "EmbarcacionView",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      embarcaciones: [], // Lista de embarcaciones paginadas
      searchQuery: "", // Término de búsqueda
      debounceTimeout: null, // Timeout para el debounce
      userPermissions: [], // Permisos del usuario
      userGroups: [], // Grupos del usuario
      currentPage: 1, // Página actual
      totalPages: 1, // Total de páginas
      pages: [], // Lista de páginas visibles
      busqueda_existente: true, // Controla si hay resultados de búsqueda
    };
  },
  async created() {
    await this.fetchUserPermissionsAndGroups();
    await this.getEmbarcaciones();
  },
  methods: {
    toggleNoIdVisibility() {
      this.showNoId = !this.showNoId;
    },
    // Verifica si el usuario tiene un permiso específico
    hasPermission(permission) {
      return this.userPermissions.some((p) => p.name === permission);
    },
    // Verifica si el usuario pertenece a un grupo específico
    hasGroup(group) {
      return this.userGroups.some((g) => g.name === group);
    },
    // Obtiene los permisos y grupos del usuario
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
    // Obtiene las embarcaciones con paginación
    async getEmbarcaciones() {
      try {
        this.$store.commit("setIsLoading", true);
        const response = await axios.get("/api/embarcaciones/", {
          params: {
            page: this.currentPage,
            search: this.searchQuery,
          },
        });
        this.embarcaciones = response.data.results;
        this.totalPages = Math.ceil(response.data.count / 15);
        this.updatePages();
        this.busqueda_existente = true;
      } catch (error) {
        console.error("Error al obtener las embarcaciones:", error);
        Swal.fire("Error", "No se pudieron cargar las embarcaciones.", "error");
      } finally {
        this.$store.commit("setIsLoading", false);
      }
    },
    // Busca embarcaciones con paginación
    async searchEmbarcacion() {
      try {
        this.$store.commit("setIsLoading", true);
        this.currentPage = 1; // Reiniciar a la primera página al realizar una búsqueda
        const response = await axios.get("/api/embarcaciones/", {
          params: {
            page: this.currentPage,
            search: this.searchQuery,
          },
        });
        this.embarcaciones = response.data.results;
        this.totalPages = Math.ceil(response.data.count / 15);
        this.updatePages();
        this.busqueda_existente = this.embarcaciones.length > 0;
      } catch (error) {
        console.error("Error al buscar embarcaciones:", error);
        this.busqueda_existente = false;
      } finally {
        this.$store.commit("setIsLoading", false);
      }
    },
    // Debounce para evitar múltiples llamadas durante la escritura
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchEmbarcacion();
      }, 300);
    },
    // Confirma la eliminación de una embarcación
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
          this.deleteEmbarcacion(id);
        }
      });
    },
    // Elimina una embarcación
    async deleteEmbarcacion(id) {
      try {
        await axios.delete(`/api/embarcaciones/${id}/`);
        // Actualizar la lista sin recargar toda la página
        if (this.embarcaciones.length === 1 && this.currentPage > 1) {
          this.currentPage -= 1;
        }
        await this.getEmbarcaciones();
        Swal.fire(
          "Eliminado!",
          "La embarcación ha sido eliminada exitosamente.",
          "success"
        );
      } catch (error) {
        console.error("Error al eliminar la embarcación:", error);
        Swal.fire(
          "Error",
          "Hubo un error al eliminar la embarcación.",
          "error"
        );
      }
    },
    // Cambia de página
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        this.getEmbarcaciones();
      }
    },
    // Actualiza la lista de páginas visibles
    updatePages() {
      const startPage = Math.max(1, this.currentPage - 2);
      const endPage = Math.min(this.totalPages, this.currentPage + 2);
      this.pages = [];
      for (let i = startPage; i <= endPage; i++) {
        this.pages.push(i);
      }
    },
    // Obtiene el texto asociado al valor del tipo de embarcación
    getTipoEmbarcacionText(value) {
      const tipos_embarcaciones = {
        buque: "Buque",
        remolcador: "Remolcador",
        patana: "Patana",
        otros: "Otros",
      };
      return tipos_embarcaciones[value] || "Desconocido";
    },
    // Obtiene el texto asociado al valor del tipo de buque
    getTipoBuqueText(value) {
      const tipos_buques = {
        buque_carga_gral: "Buque de carga general",
        buque_granelero: "Buque granelero",
        buque_ro_ro: "Buque Ro Ro",
        buque_frig: "Buque frigorífico",
        buque_tanque: "Buque tanque",
        buque_gases: "Buque de gases",
      };
      return tipos_buques[value] || "Desconocido";
    },
    // Obtiene el texto asociado al valor del tipo de patana
    getTipoPatanaText(value) {
      const tipos_patanas = {
        pat_carga_seca: "Patana de carga seca",
        pat_carga_liquida: "Patana de carga líquida",
        patana_comb: "Patana de combustible",
        patana_ro_ro: "Patana Ro Ro",
      };
      return tipos_patanas[value] || "Desconocido";
    },

    edit(item) {
      console.log(item)
      // Aquí puedes implementar la navegación a la página de edición
      this.$router.push({
        name: "EditarEmbarcacion",
        params: { id: item.id },
      });
    },
    openEmbarcacionDetailsModal(Embarcacion) {
      Swal.fire({
        title: "Detalles de la Embarcacion",
        html: `
          <div style="text-align: left;">
            <p><strong>Nombre:</strong> ${Embarcacion.nombre_embarcacion}</p>
            <p><strong>Nacionalidad:</strong> ${
              Embarcacion.nacionalidad_name
            }</p>
            <p><strong>Eslora:</strong> ${Embarcacion.eslora}</p>
            <p><strong>Manga:</strong> ${Embarcacion.manga}</p>
            <p><strong>Calado máximo:</strong> ${Embarcacion.calado_maximo}</p>
            <p><strong>Desplazamiento maximo:</strong> ${
              Embarcacion.desplazamiento_maximo
            }</p>
            <p><strong>Tipo de Embarcacion:</strong> ${this.getTipoEmbarcacionText(
              Embarcacion.tipo_embarcacion
            )}</p>
            <p><strong>Tipo de buque:</strong> ${this.getTipoBuqueText(
              Embarcacion.tipo_buque
            )}</p>
            <p><strong>Tipo de Patana:</strong> ${this.getTipoPatanaText(
              Embarcacion.tipo_patana
            )}</p>
            <p><strong>IMO:</strong> ${Embarcacion.imo}</p>
            <p><strong>Potencia:</strong> ${Embarcacion.potencia}</p>
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

<style scoped>
.card-header {
  background-color: #f8f9fa;
  border-bottom: 2px solid #e0e0e0 !important;
  padding: 0.75rem 1.25rem;
}

/* Estilos para el contenedor del buscador */
.search-container {
  position: relative;
  width: 100%;
  max-width: 300px; /* Ancho máximo del buscador */
}

/* Estilos para el input del buscador */
.search-container input {
  padding-right: 40px; /* Espacio para el icono de lupa */
  border-radius: 20px; /* Bordes redondeados */
}

/* Estilos para el icono de lupa */
.search-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #888; /* Color del icono */
  pointer-events: none; /* Evita que el icono interfiera con el input */
}

/* Estilos para la tabla responsive */
.table-responsive {
  overflow-x: auto; /* Permite desplazamiento horizontal en pantallas pequeñas */
}

/* Estilos para el icono de agregar */
.btn-link {
  color: #007bff; /* Color azul para el icono */
  text-decoration: none; /* Sin subrayado */
}

.btn-link:hover {
  color: #0056b3; /* Color azul más oscuro al pasar el mouse */
}

.search-container {
  position: relative;
  width: 100%;
  max-width: 360px;
}

.search-container input {
  padding-left: 2.5rem !important; /* Espacio para el icono */
  border-radius: 20px !important;
}

.search-container .bi-search {
  color: #6c757d; /* Color gris para el icono */
  z-index: 10;
}

/* Para asegurar que el input group conserve los estilos */
.input-group {
  width: 100%;
}

/* Tabla */
.table {
  font-size: 0.875rem;
}

.table thead th {
  background-color: #f8f9fa;
  border-color: #dee2e6;
  color: #495057;
  font-weight: 500;
}

.table tbody tr:hover {
  background-color: #f8f9fa;
}

.ps-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.ps-modal {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow: auto;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.pagination-container button {
  margin: 0 5px;
}

/* Estados de carga y vacío */
.ps-loading-td,
.ps-empty-td {
  padding: 3rem !important;
}

.ps-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: var(--ps-gray);
}

.ps-spinner {
  width: 3rem;
  height: 3rem;
  border: 4px solid rgba(67, 97, 238, 0.1);
  border-top-color: var(--ps-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.ps-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.75rem;
  color: var(--ps-gray);
}

.ps-empty-state i {
  font-size: 2.5rem;
  color: var(--ps-accent);
}

.ps-empty-state h3 {
  color: var(--ps-dark);
  margin: 0;
  font-size: 1.2rem;
}

.ps-empty-state p {
  margin: 0;
  max-width: 400px;
}

.ps-empty-action {
  margin-top: 1rem;
  color: var(--ps-primary);
  text-decoration: none;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: var(--ps-transition);
}

.ps-empty-action:hover {
  color: var(--ps-primary-hover);
  transform: translateY(-2px);
}

/* Modal mejorado */
.ps-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
  animation: fadeIn 0.3s ease-out;
}

.ps-modal {
  background: white;
  border-radius: var(--ps-border-radius);
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  animation: slideUp 0.4s cubic-bezier(0.22, 1, 0.36, 1);
  overflow: hidden;
}

.ps-modal-header {
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #0d6efd;
  color: white;
  position: relative;
}

.ps-modal-header::after {
  content: "";
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 100%;
  height: 20px;
  background: linear-gradient(to bottom, rgba(67, 97, 238, 0.2), transparent);
}

.ps-modal-header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.ps-modal-icon-container {
  background: rgba(23, 25, 184, 0.2);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ps-modal-icon {
  font-size: 1.5rem;
}

.ps-modal h2 {
  margin: 0;
  font-size: 1.4rem;
}

.ps-modal-subtitle {
  margin: 0.25rem 0 0;
  font-size: 0.9rem;
  opacity: 0.9;
  font-weight: 400;
}

.ps-modal-close {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: var(--ps-transition);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
}

.ps-modal-close:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: rotate(90deg);
}

.ps-modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  background: #f9fafb;
}

.ps-detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.ps-detail-card {
  background: white;
  border-radius: var(--ps-border-radius);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: var(--ps-transition);
  border: 1px solid var(--ps-light-gray);
}

.ps-detail-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.ps-detail-card-header {
  padding: 1rem;
  background-color: #0d6efd;
  color: white;
  border-bottom: 1px solid var(--ps-light-gray);
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.ps-detail-card-header i {
  font-size: 1.2rem;
  color: var(--ps-primary);
}

.ps-detail-card-header h4 {
  margin: 0;
  font-size: 1rem;
  color: var(--ps-dark);
}

.ps-detail-card-body {
  padding: 1rem;
}

.ps-detail-card-highlight {
  border: 1px solid rgba(67, 97, 238, 0.3);
}

.ps-detail-card-highlight .ps-detail-card-header {
  background: linear-gradient(to right, rgba(67, 97, 238, 0.05), white);
}

.ps-detail-card-highlight .ps-detail-card-header i {
  color: var(--ps-accent);
}

.ps-detail-card-full {
  grid-column: 1 / -1;
}

.ps-detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 0.75rem;
}

.ps-detail-item:last-child {
  margin-bottom: 0;
}

.ps-detail-label {
  font-size: 0.85rem;
  color: var(--ps-gray);
  font-weight: 500;
}

.ps-detail-value {
  font-size: 1rem;
  color: var(--ps-dark);
  font-weight: 500;
  word-break: break-word;
}

.ps-highlight-value {
  color: var(--ps-primary);
  font-weight: 600;
  font-size: 1.1rem;
}

.ps-modal-footer {
  padding: 1.25rem 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  background: white;
  border-top: 1px solid var(--ps-light-gray);
}

.ps-modal-btn {
  padding: 0.6rem 1.2rem;
  border-radius: var(--ps-border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: var(--ps-transition);
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.ps-modal-btn-secondary {
  background: white;
  color: var(--ps-gray);
  border: 1px solid var(--ps-light-gray);
}

.ps-modal-btn-secondary:hover {
  background: #f1f3f5;
  color: var(--ps-dark);
}

.ps-modal-btn-primary {
  background: var(--ps-primary);
  color: white;
  box-shadow: 0 2px 6px rgba(67, 97, 238, 0.2);
}

.ps-modal-btn-primary:hover {
  background: var(--ps-primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3);
}

.ps-status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
}

.ps-status-success {
  background: rgba(76, 201, 240, 0.1);
  color: #06d6a0;
  border: 1px solid rgba(6, 214, 160, 0.2);
}


.ps-status-danger {
  background: rgba(247, 37, 133, 0.1);
  color: #f72585;
  border: 1px solid rgba(247, 37, 133, 0.2);
}

.ps-status-default {
  background: rgba(108, 117, 125, 0.1);
  color: var(--io-gray);
  border: 1px solid rgba(108, 117, 125, 0.2);
}
</style>
