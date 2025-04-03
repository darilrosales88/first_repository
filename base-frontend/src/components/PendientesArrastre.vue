<template>
   
    <div class="container py-3">
      <!-- Encabezado con acciones -->
      <div class="d-flex justify-content-between align-items-center mb-4">
        <!-- Botón de agregar - más destacado -->
        <button 
          v-if="hasPermission"
          @click="showAddModal = true"
          class="btn btn-primary"
          title="Agregar nuevo vagón"
        >
          <i class="bi bi-plus-circle me-1"></i> Agregar
        </button>

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

      <!-- Tabla responsive con mejoras -->
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
              <th scope="row">{{ (currentPage - 1) * itemsPerPage + index + 1 }}</th>
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
                  <button
                    @click="viewDetails(tren)"
                    class="btn btn-sm btn-outline-info me-2"
                    title="Ver detalles"
                  >
                    <i class="bi bi-eye-fill"></i>
                  </button>
                  <button
                    @click="editTren(tren)"
                    class="btn btn-sm btn-outline-warning me-2"
                    title="Editar"
                  >
                    <i class="bi bi-pencil-square"></i>
                  </button>
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

      <!-- Paginación mejorada -->
      <div class="d-flex justify-content-between align-items-center mt-3">
        <div class="text-muted small">
          Mostrando {{ paginatedTrenes.length }} de {{ filteredTrenes.length }} registros
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

      <!-- Modal para agregar/editar -->
      <div v-if="showAddModal || showEditModal" class="modal-backdrop">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEditing ? 'Editar' : 'Agregar' }} Tren</h5>
            <button @click="closeModal" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="isEditing ? updateTren() : createTren()">
              <div class="mb-3">
                <label class="form-label">Origen</label>
                <input v-model="currentTren.origen" type="text" class="form-control" required>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Tipo de Origen</label>
                <select v-model="currentTren.tipo_origen" class="form-select" required>
                  <option v-for="option in tipo_origen_options" :value="option.id" :key="option.id">
                    {{ option.text }}
                  </option>
                </select>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Tipo de Equipo</label>
                <select v-model="currentTren.tipo_equipo" class="form-select" required>
                  <option v-for="option in tipo_equipo_options" :value="option.id" :key="option.id">
                    {{ option.text }}
                  </option>
                </select>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Estado</label>
                <select v-model="currentTren.estado" class="form-select" required>
                  <option v-for="option in estado_options" :value="option.id" :key="option.id">
                    {{ option.text }}
                  </option>
                </select>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Cantidad de Vagones</label>
                <input v-model="currentTren.cantidad_vagones" type="number" class="form-control" required>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Producto</label>
                <select v-model="currentTren.producto" class="form-select" required>
                  <option v-for="option in producto_options" :value="option.id" :key="option.id">
                    {{ option.text }}
                  </option>
                </select>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Destino</label>
                <input v-model="currentTren.destino" type="text" class="form-control" required>
              </div>
              
              <div class="d-flex justify-content-end">
                <button type="button" @click="closeModal" class="btn btn-outline-secondary me-2">
                  Cancelar
                </button>
                <button type="submit" class="btn btn-primary" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  {{ isEditing ? 'Actualizar' : 'Guardar' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Modal para detalles -->
      <div v-if="showDetailModal" class="modal-backdrop">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Detalles del Tren</h5>
            <button @click="showDetailModal = false" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label fw-bold">Origen:</label>
              <p>{{ currentTren.origen }}</p>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Tipo de Origen:</label>
              <p>{{ getTipoOrigenText(currentTren.tipo_origen) }}</p>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Estado:</label>
              <p>{{ getEstadoText(currentTren.estado) }}</p>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Producto:</label>
              <p>{{ getProductoText(currentTren.producto) }}</p>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Cantidad de Vagones:</label>
              <p>{{ currentTren.cantidad_vagones }}</p>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Destino:</label>
              <p>{{ currentTren.destino }}</p>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="showDetailModal = false" class="btn btn-primary">
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';

const API_URL = 'http://127.0.0.1:8000/ufc/pendiente_arrastre';

export default {
  name: 'GestionTrenes',
  data() {
    return {
      en_trenes: [],
      searchQuery: '',
      currentPage: 1,
      itemsPerPage: 10,
      hasPermission: true,
      loading: false,

      // Modales
      showAddModal: false,
      showEditModal: false,
      showDetailModal: false,
      isEditing: false,

      // Datos del tren actual
      currentTren: {
        id: null,
        origen: '',
        tipo_origen: '',
        tipo_equipo: '',
        estado: '',
        cantidad_vagones: '',
        producto: '',
        destino: ''
      },

      // Opciones para los selects
      tipo_origen_options: [
        { id: 'puerto', text: 'Puerto' },
        { id: 'acceso_comercial', text: 'Acceso Comercial' }
      ],
      tipo_equipo_options: [
        { id: 'casilla', text: 'Casilla' },
        { id: 'cajon_gondola', text: 'Cajón o Góndola' }
      ],
      estado_options: [
        { id: 'vacio', text: 'Vacío' },
        { id: 'cargado', text: 'Cargado' }
      ],
      producto_options: [
        { id: 'granos', text: 'Granos' },
        { id: 'minerales', text: 'Minerales' },
        { id: 'combustible', text: 'Combustible' }
      ]
    };
  },
  computed: {
    filteredTrenes() {
      if (!this.searchQuery) {
        return this.en_trenes;
      }
      
      const query = this.searchQuery.toLowerCase();
      return this.en_trenes.filter(tren => 
        (tren.origen && tren.origen.toLowerCase().includes(query)) ||
        (tren.destino && tren.destino.toLowerCase().includes(query)) ||
        (this.getProductoText(tren.producto) && this.getProductoText(tren.producto).toLowerCase().includes(query)) ||
        (tren.cantidad_vagones && tren.cantidad_vagones.toString().includes(query))
      );
    },
    paginatedTrenes() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredTrenes.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredTrenes.length / this.itemsPerPage);
    }
  },
  created() {
    this.fetchTrenes();
  },
  methods: {
    async fetchTrenes() {
      this.loading = true;
      try {
        const response = await axios.get(API_URL);
        this.en_trenes = response.data;
      } catch (error) {
        console.error('Error al obtener los trenes:', error);
        Swal.fire('Error', 'No se pudieron cargar los trenes', 'error');
      } finally {
        this.loading = false;
      }
    },
    
    getTipoOrigenText(id) {
      const option = this.tipo_origen_options.find(o => o.id === id);
      return option ? option.text : id;
    },
    
    getEstadoText(id) {
      const option = this.estado_options.find(o => o.id === id);
      return option ? option.text : id;
    },
    
    getEstadoBadge(id) {
      return id === 'cargado' ? 'success' : 'secondary';
    },
    
    getProductoText(id) {
      const option = this.producto_options.find(o => o.id === id);
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
    
    async createTren() {
      this.loading = true;
      try {
        const response = await axios.post(API_URL, this.currentTren);
        this.en_trenes.unshift(response.data);
        this.closeModal();
        Swal.fire('Éxito', 'Tren creado correctamente', 'success');
      } catch (error) {
        console.error('Error al crear el tren:', error);
        Swal.fire('Error', 'No se pudo crear el tren', 'error');
      } finally {
        this.loading = false;
      }
    },
    
    editTren(tren) {
      this.currentTren = { ...tren };
      this.isEditing = true;
      this.showEditModal = true;
    },
    
    async updateTren() {
      this.loading = true;
      try {
        const response = await axios.put(`${API_URL}/${this.currentTren.id}`, this.currentTren);
        const index = this.en_trenes.findIndex(t => t.id === this.currentTren.id);
        if (index !== -1) {
          this.en_trenes.splice(index, 1, response.data);
        }
        this.closeModal();
        Swal.fire('Éxito', 'Tren actualizado correctamente', 'success');
      } catch (error) {
        console.error('Error al actualizar el tren:', error);
        Swal.fire('Error', 'No se pudo actualizar el tren', 'error');
      } finally {
        this.loading = false;
      }
    },
    
    confirmDelete(id) {
      Swal.fire({
        title: '¿Estás seguro?',
        text: 'No podrás revertir esta acción',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
      }).then((result) => {
        if (result.isConfirmed) {
          this.deleteTren(id);
        }
      });
    },
    
    async deleteTren(id) {
      try {
        await axios.delete(`${API_URL}/${id}`);
        this.en_trenes = this.en_trenes.filter(t => t.id !== id);
        Swal.fire('Eliminado', 'El tren ha sido eliminado', 'success');
      } catch (error) {
        console.error('Error al eliminar el tren:', error);
        Swal.fire('Error', 'No se pudo eliminar el tren', 'error');
      }
    },
    
    viewDetails(tren) {
      this.currentTren = { ...tren };
      this.showDetailModal = true;
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
    
    closeModal() {
      this.showAddModal = false;
      this.showEditModal = false;
      this.currentTren = {
        id: null,
        origen: '',
        tipo_origen: '',
        tipo_equipo: '',
        estado: '',
        cantidad_vagones: '',
        producto: '',
        destino: ''
      };
      this.isEditing = false;
    }
  }
};
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

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content {
  background-color: #fff;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  opacity: 0.7;
}

.btn-close:hover {
  opacity: 1;
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

.spinner-border {
  margin-right: 5px;
}
</style>