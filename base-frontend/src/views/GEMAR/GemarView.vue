<template>
  <div>
    <NavbarComponent />
    <div class="container py-3" style="margin-left: 15.8em; width: 79%">
      <div class="card border">
        <div class="card-header bg-light border-bottom">
          <h6 class="mb-0 text-dark fw-semibold">
            <i class="bi bi-clipboard-data me-2"></i>
            Sistema de Partes Controlados - GEMAR
          </h6>
        </div>
        <div class="card-body p-3">
          <div v-if="showMainTable">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <div class="parts-menu" style="position: relative;">
                <button class="btn btn-sm btn-primary" @click="showMenu = !showMenu">
                  <i class="bi bi-plus-circle me-1"></i>Tipos de Partes
                </button>
                <div v-if="showMenu" class="menu-options" style="position: absolute; top: 100%; left: 0; z-index: 1000;">
                  <a href="/CargasViejas" class="dropdown-item">Cargas Viejas</a>
                  <a href="/ExistenciasMercancia" class="dropdown-item">Existencias Mercancía</a>
                  <a href="/PartesPBIP" class="dropdown-item">Partes PBIP</a>
                </div>
              </div>
              <form @submit.prevent="handleSearch" class="search-container">
                <div class="input-group">
                  <input
                    type="search"
                    class="form-control"
                    placeholder="Buscar por tipo, entidad o estado"
                    v-model="searchQuery"
                    @input="handleSearchInput"
                  />
                  <span class="position-absolute top-50 start-0 translate-middle-y ps-2">
                    <i class="bi bi-search"></i>
                  </span>
                </div>
              </form>
            </div>
            
            <div v-if="loading" class="text-center my-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
              <p class="mt-2">Cargando partes...</p>
            </div>
            
            <div v-else class="table-responsive">
              <table class="table table-sm table-bordered table-hover">
                <thead class="table-light">
                  <tr>
                    <th scope="col">No.</th>
                    <th scope="col">Fecha</th>
                    <th scope="col">Hora</th>
                    <th scope="col">Tipo parte</th>
                    <th scope="col">Entidad</th>
                    <th scope="col">Organismo</th>
                    <th scope="col">Estado</th>
                    <th scope="col">Creado por</th>
                    <th scope="col">Aprobado por</th>
                    <th scope="col">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(parte, index) in paginatedPartes" :key="parte.id">
                    <td>{{ (currentPage - 1) * itemsPerPage + index + 1 }}</td>
                    <td>{{ formatDate(parte.fecha_operacion) || '-' }}</td>
                    <td>{{ formatTime(parte.fecha_creacion) || '-' }}</td>
                    <td>{{ getTipoParte(parte) }}</td>
                    <td>{{ getEntidad(parte) }}</td>
                    <td>{{ parte.organismo?.nombre || '-' }}</td>
                    <td>
                      <span :class="'status-' + getStatusClass(parte.estado || parte.estado_registro || '')">
                        {{ parte.estado || parte.estado_registro || '-' }}
                      </span>
                    </td>
                    <td>{{ parte.creado_por?.username || '-' }}</td>
                    <td>{{ parte.aprobado_por?.username || '-' }}</td>
                    <td>
                      <div class="d-flex">
                        <button 
                          @click="verParte(parte)"
                          class="btn btn-sm btn-outline-info me-2"
                          title="Ver detalles">
                          <i class="bi bi-eye-fill"></i>
                        </button>
                        <button 
                          v-if="(parte.estado === 'CREADO' || parte.estado_registro === 'CREADO') && tienePermiso('approve')"
                          @click="confirmarParte(parte)"
                          class="btn btn-sm btn-outline-success me-2"
                          title="Confirmar">
                          <i class="bi bi-check-circle"></i>
                        </button>
                        <button
                          @click="confirmDelete(parte)"
                          class="btn btn-sm btn-outline-danger"
                          title="Eliminar"
                          :disabled="loading || (parte.estado === 'APROBADO' || parte.estado_registro === 'APROBADO')">
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="filteredPartes.length === 0 && !loading">
                    <td colspan="10" class="text-center text-muted py-4">
                      <i class="bi bi-database-exclamation fs-4"></i>
                      <p class="mt-2">
                        {{ searchQuery ? 'No hay coincidencias' : 'No hay informes' }}
                      </p>
                      <p>
                        {{
                          searchQuery
                            ? `No encontramos resultados para "${searchQuery}"`
                            : 'No hay informes operativos registrados'
                        }}
                      </p>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <!-- Paginación -->
            <div class="io-pagination d-flex justify-content-between align-items-center mt-3">
              <div class="text-muted small">
                Mostrando {{ (currentPage - 1) * itemsPerPage + 1 }}-{{ Math.min(currentPage * itemsPerPage, filteredPartes.length) }} de {{ filteredPartes.length }} registros
              </div>
              <nav aria-label="Page navigation">
                <ul class="pagination pagination-sm mb-0">
                  <li class="page-item" :class="{ disabled: currentPage === 1 }">
                    <button class="page-link" @click="changePage(currentPage - 1)">
                      <i class="bi bi-chevron-left"></i>
                    </button>
                  </li>
                  <li class="page-item disabled">
                    <span class="page-link">
                      Página {{ currentPage }} de {{ totalPages }}
                    </span>
                  </li>
                  <li class="page-item" :class="{ disabled: currentPage >= totalPages }">
                    <button class="page-link" @click="changePage(currentPage + 1)">
                      <i class="bi bi-chevron-right"></i>
                    </button>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
          
          <!-- Contenedor para el parte seleccionado -->
          <div v-if="!showMainTable" class="selected-part-container">
            <button @click="backToMainTable" class="btn btn-sm btn-outline-secondary mb-3">
              <i class="bi bi-arrow-left"></i> Volver al registro
            </button>
            <component 
              :is="currentComponent" 
              :key="componentKey"
              @parte-creado="handleParteCreado"
              @cancelar="backToMainTable"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de confirmación de eliminación -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="closeDeleteModal">
      <div class="modal">
        <div class="modal-header">
          <h5>Confirmar eliminación</h5>
          <button class="modal-close" @click="closeDeleteModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        <div class="modal-body">
          <p>¿Está seguro que desea eliminar este registro? Esta acción no se puede deshacer.</p>
        </div>
        <div class="modal-footer">
          <button @click="closeDeleteModal" class="btn btn-sm btn-outline-secondary">
            Cancelar
          </button>
          <button @click="deleteParte" class="btn btn-sm btn-danger">
            Eliminar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavbarComponent from "@/components/NavbarComponent.vue";
import CargasViejas from "@/views/GEMAR/CargasViejas.vue";
import ExistenciasMercancia from "@/views/GEMAR/ExistenciasMercancia.vue";
import PartesPBIP from "@/views/GEMAR/PartesPBIP.vue";
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "GemarView",
  components: {
    NavbarComponent,
    CargasViejas,
    ExistenciasMercancia,
    PartesPBIP,
  },
  data() {
    return {
      showMainTable: true,
      currentComponent: null,
      showMenu: false,
      searchQuery: '',
      partes: [],
      filteredPartes: [],
      currentPage: 1,
      itemsPerPage: 15,
      loading: false,
      componentKey: 0,
      showDeleteModal: false,
      parteToDelete: null,
      debounceTimeout: null
    }
  },
  created() {
    this.cargarPartes();
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredPartes.length / this.itemsPerPage);
    },
    paginatedPartes() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredPartes.slice(start, end);
    }
  },
  methods: {
    async cargarPartes() {
      try {
        this.loading = true;
        const today = new Date().toISOString().split('T')[0];
        
        const resumenRes = await axios.get(`/api/gemar/resumen-diario/?fecha=${today}`);
        
        this.partes = [
          ...resumenRes.data.partes_pbip.map(p => ({ ...p, tipo: 'PBIP' })),
          ...resumenRes.data.cargas_viejas.map(c => ({ ...c, tipo: 'Carga Vieja' })),
          ...resumenRes.data.existencias.map(e => ({ ...e, tipo: 'Existencia' }))
        ];
        
        this.filteredPartes = [...this.partes];
      } catch (error) {
        console.error("Error al cargar partes:", error);
        this.mostrarError("No se pudieron cargar los partes. Intente nuevamente.");
      } finally {
        this.loading = false;
      }
    },
    
    async aprobarParte(parte) {
      try {
        const token = localStorage.getItem('token');
        const headers = { Authorization: `Bearer ${token}` };
        
        let endpoint = '';
        if (parte.tipo === 'PBIP') {
          endpoint = `/api/gemar/partes-pbip/${parte.id}/aprobar/`;
        } else if (parte.tipo === 'Carga Vieja') {
          endpoint = `/api/gemar/cargas-viejas/${parte.id}/aprobar/`;
        } else {
          endpoint = `/api/gemar/existencias-mercancia/${parte.id}/aprobar/`;
        }
        
        await axios.post(endpoint, {}, { headers });
        this.mostrarExito("Parte aprobado correctamente");
        this.cargarPartes(); // Recargar los datos
      } catch (error) {
        this.mostrarError("Error al aprobar el parte");
      }
    },
    
    selectPart(componentName) {
      this.showMenu = false;
      this.showMainTable = false;
      this.currentComponent = componentName;
      this.componentKey++; // Forzar recarga del componente
    },
    
    backToMainTable() {
      this.showMainTable = true;
      this.currentComponent = null;
      this.cargarPartes();
    },
    
    handleParteCreado() {
      this.backToMainTable();
      this.mostrarExito("Parte creado exitosamente");
    },
    
    handleSearch() {
      if (!this.searchQuery) {
        this.filteredPartes = [...this.partes];
        return;
      }
      
      const query = this.searchQuery.toLowerCase();
      this.filteredPartes = this.partes.filter(parte => {
        return (
          (parte.tipo && parte.tipo.toLowerCase().includes(query)) ||
          (parte.buque?.nombre && parte.buque.nombre.toLowerCase().includes(query)) ||
          (parte.puerto?.nombre && parte.puerto.nombre.toLowerCase().includes(query)) ||
          (parte.producto?.nombre && parte.producto.nombre.toLowerCase().includes(query)) ||
          (parte.estado && typeof parte.estado === 'string' && parte.estado.toLowerCase().includes(query)) ||
          (parte.estado_registro && typeof parte.estado_registro === 'string' && parte.estado_registro.toLowerCase().includes(query))
        );
      });
      this.currentPage = 1;
    },
    
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.handleSearch();
      }, 300);
    },
    
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    
    async verParte(parte) {
      try {
        const token = localStorage.getItem('token');
        const headers = { Authorization: `Bearer ${token}` };
        
        let endpoint = '';
        if (parte.tipo === 'PBIP') endpoint = `/api/gemar/partes-pbip/${parte.id}/`;
        else if (parte.tipo === 'Carga Vieja') endpoint = `/api/gemar/cargas-viejas/${parte.id}/`;
        else endpoint = `/api/gemar/existencias-mercancia/${parte.id}/`;
        
        const response = await axios.get(endpoint, { headers });
        
        Swal.fire({
          title: `Detalles del parte ${parte.tipo}`,
          html: this.generateDetailsHtml(response.data),
          confirmButtonText: 'Cerrar',
          width: '800px'
        });
      } catch (error) {
        this.mostrarError("No se pudieron cargar los detalles del parte");
      }
    },
    
    async deleteParte() {
      if (!this.parteToDelete) return;
      
      try {
        const token = localStorage.getItem('token');
        const headers = { Authorization: `Bearer ${token}` };
        
        let endpoint = '';
        if (this.parteToDelete.tipo === 'PBIP') endpoint = `/api/gemar/partes-pbip/${this.parteToDelete.id}/`;
        else if (this.parteToDelete.tipo === 'Carga Vieja') endpoint = `/api/gemar/cargas-viejas/${this.parteToDelete.id}/`;
        else endpoint = `/api/gemar/existencias-mercancia/${this.parteToDelete.id}/`;
        
        await axios.delete(endpoint, { headers });
        this.mostrarExito("Parte eliminado correctamente");
        this.cargarPartes();
        this.closeDeleteModal();
      } catch (error) {
        this.mostrarError("Error al eliminar el parte");
      }
    },
    
    generateDetailsHtml(parte) {
      let html = '<div class="text-start">';
      
      if (parte.tipo === 'PBIP') {
        html += `
          <p><strong>Buque:</strong> ${parte.buque?.nombre || 'N/A'}</p>
          <p><strong>Puerto:</strong> ${parte.puerto?.nombre || 'N/A'}</p>
          <p><strong>Fecha Operación:</strong> ${this.formatFullDate(parte.fecha_operacion)}</p>
          <p><strong>Nivel:</strong> ${parte.nivel_display || 'N/A'}</p>
          <p><strong>Estado:</strong> <span class="badge bg-${parte.estado === 'APROBADO' ? 'success' : 'warning'}">${parte.estado || 'N/A'}</span></p>
        `;
      } else if (parte.tipo === 'Carga Vieja') {
        html += `
          <p><strong>Producto:</strong> ${parte.producto?.nombre || 'N/A'}</p>
          <p><strong>Puerto:</strong> ${parte.puerto?.nombre || 'N/A'}</p>
          <p><strong>Terminal:</strong> ${parte.terminal?.nombre || 'N/A'}</p>
          <p><strong>Manifiesto:</strong> ${parte.manifiesto || 'N/A'}</p>
          <p><strong>Toneladas Hoy:</strong> ${parte.toneladas_hoy || '0'}</p>
          <p><strong>Días en Almacén:</strong> ${parte.dias_almacen || '0'}</p>
        `;
      } else if (parte.tipo === 'Existencia') {
        html += `
          <p><strong>Terminal:</strong> ${parte.terminal?.nombre || 'N/A'}</p>
          <p><strong>Tipo:</strong> ${parte.tipo_display || 'N/A'}</p>
          <p><strong>Producto:</strong> ${parte.producto?.nombre || 'N/A'}</p>
          <p><strong>Existencia:</strong> ${parte.existencia || '0'}</p>
          <p><strong>Estado:</strong> <span class="badge bg-${parte.estado_registro === 'APROBADO' ? 'success' : 'warning'}">${parte.estado_registro || 'N/A'}</span></p>
        `;
      }
      
      html += '</div>';
      return html;
    },
    
    confirmarParte(parte) {
      Swal.fire({
        title: 'Confirmar aprobación',
        text: `¿Está seguro que desea aprobar este parte de ${parte.tipo}?`,
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, aprobar',
        cancelButtonText: 'Cancelar'
      }).then((result) => {
        if (result.isConfirmed) {
          this.aprobarParte(parte);
        }
      });
    },
    
    confirmDelete(parte) {
      this.parteToDelete = parte;
      this.showDeleteModal = true;
    },
    
    closeDeleteModal() {
      this.showDeleteModal = false;
      this.parteToDelete = null;
    },
    
    tienePermiso(accion) {
      // Implementa lógica de permisos según tu sistema
      const userRoles = localStorage.getItem('userRoles') || '';
      if (accion === 'approve') {
        return userRoles.includes('admin') || userRoles.includes('supervisor');
      }
      return true;
    },
    
    getStatusClass(status) {
      if (!status) return 'default';
      
      // Asegurarnos de que status sea una cadena
      const statusStr = typeof status === 'string' ? status : String(status);
      const statusLower = statusStr.toLowerCase();

      if (statusLower.includes('aprobado')) return 'success';
      if (statusLower.includes('pendiente') || statusLower.includes('creado'))
        return 'warning';
      if (statusLower.includes('rechazado') || statusLower.includes('cancelado')) return 'danger';

      return 'info';
    },
    
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('es-ES');
    },
    
    formatTime(datetimeString) {
      if (!datetimeString) return '';
      const date = new Date(datetimeString);
      return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
    },
    
    formatFullDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    
    getTipoParte(parte) {
      return parte.tipo || '-';
    },
    
    getEntidad(parte) {
      if (parte.buque) return parte.buque.nombre;
      if (parte.terminal) return parte.terminal.nombre;
      if (parte.producto) return parte.producto.nombre;
      return '-';
    },
    
    mostrarError(mensaje) {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: mensaje,
        confirmButtonText: 'Aceptar'
      });
    },
    
    mostrarExito(mensaje) {
      Swal.fire({
        icon: 'success',
        title: 'Éxito',
        text: mensaje,
        confirmButtonText: 'Aceptar'
      });
    }
  }
}
</script>

<style scoped>
/* Estilos heredados de RegistrosPartesUFC */
.card-header {
  background-color: #f8f9fa;
  border-bottom: 2px solid #e0e0e0 !important;
  padding: 0.75rem 1.25rem;
}

.search-container {
  position: relative;
  width: 100%;
  max-width: 300px;
}

.search-container input {
  padding-left: 2.5rem !important;
  border-radius: 20px !important;
}

.search-container .bi-search {
  color: #6c757d;
  z-index: 10;
}

.input-group {
  width: 100%;
}

.table-responsive {
  overflow-x: auto;
}

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

/* Estilos para los estados */
.status-success {
  background-color: rgba(40, 167, 69, 0.1);
  color: #28a745;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-warning {
  background-color: rgba(255, 193, 7, 0.1);
  color: #ffc107;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-danger {
  background-color: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-info {
  background-color: rgba(23, 162, 184, 0.1);
  color: #17a2b8;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-default {
  background-color: rgba(108, 117, 125, 0.1);
  color: #6c757d;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.menu-options {
  background-color: white;
  border: 1px solid #dee2e6;
  border-radius: 0.25rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  min-width: 200px;
}

.menu-options a {
  display: block;
  padding: 0.5rem 1rem;
  color: #212529;
  text-decoration: none;
}

.menu-options a:hover {
  background-color: #f8f9fa;
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 0.25rem 1rem;
  clear: both;
  font-weight: 400;
  color: #212529;
  text-align: inherit;
  text-decoration: none;
  white-space: nowrap;
  background-color: transparent;
  border: 0;
}

.dropdown-item:hover {
  color: #16181b;
  background-color: #f8f9fa;
}

.selected-part-container {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #dee2e6;
  border-radius: 0.25rem;
  background-color: #f8f9fa;
}

/* Estilos para la paginación */
.io-pagination {
  padding: 0.75rem 1.25rem;
  background-color: #f8f9fa;
  border-top: 1px solid #dee2e6;
  border-radius: 0 0 0.25rem 0.25rem;
}

.page-link {
  min-width: 32px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-item.active .page-link {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.page-link {
  color: #0d6efd;
  text-decoration: none;
}

.page-item.disabled .page-link {
  color: #6c757d;
  pointer-events: none;
  height: 30px;
}

.page-item:not(.disabled):not(.active) .page-link:hover {
  background-color: #e9ecef;
  color: #0a58ca;
}

.page-item .page-link i {
  font-size: 0.9rem;
}

/* Estilos para el mensaje de no resultados */
.text-muted {
  color: #6c757d !important;
}

.bi-database-exclamation {
  color: #adb5bd;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

/* Modal de confirmación */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.modal {
  background: white;
  border-radius: 0.5rem;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.modal-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h5 {
  margin: 0;
  font-size: 1.25rem;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6c757d;
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #dee2e6;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
</style>