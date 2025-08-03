<template>
  <div>
    <div style="background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido: </h6>
    </div>  
    <Navbar-Component />
    <div class="container py-3" style="margin-left: 18em; width: 75%">
      <div class="card border">
        <div class="card-header bg-light border-bottom">
          <h6 class="mb-0 text-dark fw-semibold">
            Listado de organismos
          </h6>
        </div>
        <div class="card-body p-3">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <router-link v-if="hasGroup('Admin')" class="btn btn-sm btn-primary" to="/AdicionarOrganismos">
              <i class="bi bi-plus-circle me-1"></i>Adicionar organismo
            </router-link>
            <form @submit.prevent="searchOrganismos" class="search-container">
              <div class="input-group">
                <input
                  type="search"
                  class="form-control"
                  placeholder="Buscar por nombre, abreviatura o código"
                  v-model="searchQuery"
                  @input="handleSearchInput"
                />
                <span class="position-absolute top-50 start-0 translate-middle-y ps-2">
                  <i class="bi bi-search"></i>
                </span>
              </div>
            </form>
          </div>
          <div class="table table-responsive">
            <table class="table table-sm table-bordered table-hover">
              <thead class="table-light">
                <tr>
                  <th scope="col">Nombre</th>
                  <th scope="col">Abreviatura</th>
                  <th scope="col">Código REEUP</th>
                  <th scope="col">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item) in organismos" :key="item.id">
                  <td>{{ item.nombre }}</td>
                  <td>{{ item.abreviatura }}</td>
                  <td>{{ item.codigo_reeup }}</td>
                  <td>
                    <div class="d-flex" style="margin-left: 30%;">
                      <button 
                        @click="openOrganismosDetailsModal(item)" 
                        class="btn btn-sm btn-outline-info me-2"
                        title="Ver detalles"
                        v-html="showNoId ? '<i class=\'bi bi-eye-slash-fill\'></i>' : '<i class=\'bi bi-eye-fill\'></i>'">
                      </button>
                      
                        <router-link v-if="hasGroup('Admin')"
                          :to="{name: 'EditarOrganismos', params: {id:item.id}}" 
                          class="btn btn-sm btn-outline-warning me-2"
                          title="Editar">
                          <i class="bi bi-pencil-square"></i>
                        </router-link>
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
            <h1 v-if="!busqueda_existente && searchQuery">
              No existe ningún registro asociado a ese parámetro de búsqueda
            </h1>
            <h1 v-if="organismos.length === 0 && !loading && !searchQuery">
              No hay organismos registrados
            </h1>
          </div>
          <!-- Paginación -->
          <nav aria-label="Page navigation example" style="margin-left: 30%;">
            <ul class="pagination">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">Anterior</a>
              </li>
              <li class="page-item" v-for="page in pages" :key="page" :class="{ active: page === currentPage }">
                <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
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
import axios from 'axios';
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: 'OrganismosView',
  components: {
    NavbarComponent,
  },
  data() {
    return {
      organismos: [],
      searchQuery: '',
      debounceTimeout: null,
      busqueda_existente: true,
      userPermissions: [],
      userGroups: [],
      loading: false,
      error: null,
      currentPage: 1,      // Página actual
      totalPages: 1,       // Total de páginas
      pages: [],           // Lista de páginas visibles
      itemsPerPage: 15      // Número de elementos por página
    };
  },
  async created() {
    await this.fetchUserPermissionsAndGroups();
    await this.get_organismos();
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
          this.userPermissions = response.data.permissions || [];
          this.userGroups = response.data.groups || [];
        }
      } catch (error) {
        console.error('Error al obtener permisos y grupos:', error);
      }
    },
    async get_organismos() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get("/api/osde/", {
          params: {
            page: this.currentPage,
            search: this.searchQuery
          },
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`
          }
        });

        // Asumiendo que el backend devuelve una respuesta paginada
        this.organismos = Array.isArray(response.data.results) ? response.data.results : response.data;
        this.totalPages = Math.ceil(response.data.count / this.itemsPerPage);
        this.updatePages();
        this.busqueda_existente = this.organismos.length > 0 || !this.searchQuery;
      } catch (error) {
        console.error("Error al obtener organismos:", error);
        this.error = error;
        if (error.response && error.response.status === 401) {
          Swal.fire("Sesión expirada", "Por favor inicie sesión nuevamente", "error");
          this.$router.push('/login');
        } else {
          Swal.fire("Error", "No se pudieron cargar los organismos", "error");
        }
        this.organismos = [];
        this.busqueda_existente = false;
      } finally {
        this.loading = false;
      }
    },
    async searchOrganismos() {
      try {
        this.loading = true;
        this.currentPage = 1; // Reiniciar a la primera página al realizar una búsqueda
        const response = await axios.get("/api/osde/", {
          params: {
            search: this.searchQuery,
            page: this.currentPage
          },
          headers: {
            'Authorization': `Token ${localStorage.getItem('token')}`
          }
        });
        this.organismos = Array.isArray(response.data.results) ? response.data.results : response.data;
        this.totalPages = Math.ceil(response.data.count / this.itemsPerPage);
        this.updatePages();
        this.busqueda_existente = this.organismos.length > 0;
      } catch (error) {
        console.error("Error en búsqueda:", error);
        this.busqueda_existente = false;
      } finally {
        this.loading = false;
      }
    },
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchOrganismos();
      }, 500);
    },
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
          this.deleteOrganismo(id);
        }
      });
    },
    async deleteOrganismo(id) {
      try {
        await axios.delete(`/api/osde/${id}/`, {
          headers: {
            'Authorization': `Token ${localStorage.getItem('token')}`
          }
        });
        
        await this.get_organismos();
        Swal.fire(
          "Eliminado!",
          "El organismo ha sido eliminado exitosamente.",
          "success"
        );
      } catch (error) {
        console.error("Error al eliminar el organismo:", error);
        Swal.fire(
          "Error",
          error.response?.data?.message || "Hubo un error al eliminar el organismo.",
          "error"
        );
      }
    },
    openOrganismosDetailsModal(organismo) {
      Swal.fire({
        title: 'Detalles del Organismo',
        html: `
          <div style="text-align: left;">
            <p><strong>Nombre:</strong> ${organismo.nombre}</p>
            <p><strong>Abreviatura:</strong> ${organismo.abreviatura}</p>
            <p><strong>Código REEUP:</strong> ${organismo.codigo_reeup}</p>
          </div>
        `,
        width: '600px',
        customClass: {
          popup: 'custom-swal-popup',
          title: 'custom-swal-title',
          htmlContainer: 'custom-swal-html',
        },
      });
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        this.get_organismos();
      }
    },
    updatePages() {
      const startPage = Math.max(1, this.currentPage - 2);
      const endPage = Math.min(this.totalPages, this.currentPage + 2);
      this.pages = [];
      for (let i = startPage; i <= endPage; i++) {
        this.pages.push(i);
      }
    }
  }
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
  max-width: 300px;
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
