<template>
  <div>
    <div class="card border" style="margin-left: 15.8em; width: 79%">
      <Navbar-Component />
      <div class="card-header bg-light border-bottom">
        <h6 class="mb-0 text-dark fw-semibold">
          Sistema de Partes Controlados
        </h6>
        <button class="btn btn-sm btn-outline-secondary" style="margin-top: 10px;" 
          @click="$router.push({ name: 'GEMAR' })" >
          <i class="bi bi-arrow-left me-1"></i> Volver a GEMAR
        </button>
      </div>
      <div class="card-body p-3">
        <!-- Formulario de Existencias -->
        <div class="form-section mb-4">
          <h6 class="text-dark fw-semibold mb-3">Existencia de mercancías importación-exportación</h6>
          
          <div class="row mb-3">
            <label class="col-sm-2 col-form-label">Fecha operación:</label>
            <div class="col-sm-4">
              <input 
                type="date" 
                v-model="fechaOperacion" 
                class="form-control form-control-sm"
                @change="cargarExistencias"
              >
            </div>
            <label class="col-sm-2 col-form-label">Fecha actual:</label>
            <div class="col-sm-4">
              <input 
                type="datetime-local" 
                v-model="fechaActual" 
                class="form-control form-control-sm"
                readonly
              >
            </div>
          </div>
        </div>

        <!-- Tabla de Existencias -->
        <div class="table-section">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h6 class="text-dark fw-semibold mb-0">Mercancia</h6>
            <button @click="navigateToAddMercancia" class="btn btn-sm btn-primary">
              <i class="bi bi-plus-circle me-1"></i> Agregar Mercancia
            </button>
          </div>
          
          <!-- Filtros de Productos -->
          <div class="p-3 mb-3 bg-light rounded">
            <h6 class="text-dark fw-semibold mb-2">Filtrar por tipo:</h6>
            <div class="btn-group" role="group">
              <button 
                @click="setTipoProducto('importacion')" 
                :class="['btn btn-sm', tipoProducto === 'importacion' ? 'btn-primary' : 'btn-outline-primary']"
              >
                Importación
              </button>
              <button 
                @click="setTipoProducto('exportacion')" 
                :class="['btn btn-sm', tipoProducto === 'exportacion' ? 'btn-primary' : 'btn-outline-primary']"
              >
                Exportación
              </button>
            </div>
          </div>

          <div class="table-responsive">
            <table class="table table-sm table-bordered table-hover">
              <thead class="table-light">
                <tr>
                  <th scope="col">No.</th>
                  <th scope="col">Terminal</th>
                  <th scope="col">Tipo Producto</th>
                  <th scope="col">Producto</th>
                  <th scope="col">Unidad Medida</th>
                  <th scope="col">Existencia</th>
                  <th scope="col">Estado</th>
                  <th scope="col">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(existencia, index) in existenciasFiltradas" :key="existencia.id">
                  <td>{{ index + 1 }}</td>
                  <td>{{ existencia.terminal.nombre_terminal }}</td>
                  <td>{{ existencia.tipo_producto_display }}</td>
                  <td>{{ existencia.producto.nombre_producto }}</td>
                  <td>{{ existencia.unidad_medida.unidad_medida }} ({{ existencia.unidad_medida.simbolo }})</td>
                  <td>{{ existencia.existencia }}</td>
                  <td>{{ existencia.estado_display || '-' }}</td>
                  <td>
                    <div class="d-flex gap-1">
                      <button 
                        @click="editarMercancia(existencia.id)" 
                        class="btn btn-sm btn-outline-primary"
                      >
                        <i class="bi bi-pencil"></i> 
                      </button>
                      <button 
                        @click="eliminarExistencia(existencia.id)" 
                        class="btn btn-sm btn-outline-danger"
                      >
                        <i class="bi bi-trash"></i> 
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="existenciasFiltradas.length === 0">
                  <td colspan="8" class="text-center">No hay registros para mostrar</td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <!-- Paginación -->
          <div class="io-pagination d-flex justify-content-between align-items-center mt-3">
            <div class="text-muted small">
              Mostrando {{ existenciasFiltradas.length }} de {{ existencias.length }} registros
            </div>
            <nav aria-label="Page navigation">
              <ul class="pagination pagination-sm mb-0">
                <li class="page-item disabled">
                  <button class="page-link">
                    <i class="bi bi-chevron-left"></i>
                  </button>
                </li>
                <li class="page-item disabled">
                  <span class="page-link">
                    Página 1 de 1
                  </span>
                </li>
                <li class="page-item">
                  <button class="page-link">
                    <i class="bi bi-chevron-right"></i>
                  </button>
                </li>
              </ul>
            </nav>
          </div>
        </div>

        <!-- Botones de acción -->
        <div class="d-flex justify-content-center gap-3 mt-4">
          <button @click="guardar" class="btn btn-sm btn-primary">
            <i class="bi bi-save me-1"></i> Guardar Todo
          </button>
          <button @click="cancelar" class="btn btn-sm btn-outline-secondary">
            <i class="bi bi-x me-1"></i> Cancelar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: 'ExistenciasMercancia',
  components: {
    NavbarComponent
  },
  data() {
    return {
      fechaOperacion: new Date().toISOString().split('T')[0],
      fechaActual: new Date().toISOString().slice(0, 16),
      existencias: [],
      tipoProducto: 'importacion', // 'importacion' o 'exportacion'
      loading: false
    }
  },
  computed: {
    isAdmin() {
      const userData = JSON.parse(localStorage.getItem('userData') || '{}');
      return userData.is_superuser;
    },
    isGemarUser() {
      const userData = JSON.parse(localStorage.getItem('userData') || '{}');
      return userData.rol === 'GEMAR' || userData.is_superuser;
    },
    existenciasFiltradas() {
      const tipo = this.tipoProducto === 'importacion' ? 1 : 2;
      return this.existencias.filter(e => e.tipo === tipo);
    }
  },
  async created() {
    await this.cargarExistencias();
  },
  methods: {
    async cargarExistencias() {
      try {
        this.loading = true;
        const token = localStorage.getItem('token');
        
        if (!token) {
          this.mostrarError('No se encontró el token de autenticación');
          return;
        }
        
        const response = await axios.get('/api/gemar/registros-existencia-mercancia/', {
          params: {
            fecha_operacion: this.fechaOperacion
          },
          headers: { 
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        this.existencias = response.data.results || [];
      } catch (error) {
        console.error('Error al cargar existencias:', error);
        this.mostrarError('Error al cargar las existencias de mercancía');
      } finally {
        this.loading = false;
      }
    },
    
    setTipoProducto(tipo) {
      this.tipoProducto = tipo;
    },
    
    navigateToAddMercancia() {
      this.$router.push({ name: 'AgregarExistenciaMercancia' });
    },
    
    editarMercancia(id) {
      this.$router.push({ 
        name: 'Editar-Existencias-Mercancia', 
        params: { id: id } 
      });
    },
    
    async eliminarExistencia(id) {
      try {
        const result = await Swal.fire({
          title: '¿Está seguro?',
          text: "Esta acción no se puede deshacer",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#d33',
          cancelButtonColor: '#3085d6',
          confirmButtonText: 'Sí, eliminar',
          cancelButtonText: 'Cancelar'
        });
        
        if (result.isConfirmed) {
          const token = localStorage.getItem('token');
          await axios.delete(`/gemar/existencias-mercancia/${id}/`, {
            headers: { 'Authorization': `Token ${token}` }
          });
          
          this.mostrarExito('Existencia eliminada correctamente');
          await this.cargarExistencias();
        }
      } catch (error) {
        console.error('Error al eliminar existencia:', error);
        this.mostrarError('Error al eliminar la existencia');
      }
    },
    
    async guardar() {
      if (!this.isGemarUser) {
        this.mostrarError('No tiene permisos para realizar esta acción');
        return;
      }
      
      try {
        if (!this.fechaOperacion) {
          this.mostrarError('La fecha de operación es requerida');
          return;
        }
        
        this.mostrarExito('Datos guardados correctamente');
        await this.cargarExistencias();
      } catch (error) {
        console.error('Error al guardar:', error);
        this.mostrarError('Error al guardar los datos');
      }
    },
    
    cancelar() {
      this.fechaOperacion = new Date().toISOString().split('T')[0];
      this.cargarExistencias();
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
.card {
  border-radius: 0.25rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 2px solid #e0e0e0 !important;
  padding: 0.75rem 1.25rem;
}

.form-section {
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 0.25rem;
  margin-bottom: 1rem;
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

/* Estilos para los botones */
.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  color: white;
}

.btn-outline-success {
  margin-left: 10px ;
  color: #28a745;
  border-color: #28a745;
}

.btn-outline-success:hover {
  background-color: #28a745;
  color: white;
}

.btn-outline-secondary {
  color: #6c757d;
  border-color: #6c757d;
}

.btn-outline-secondary:hover {
  background-color: #6c757d;
  color: white;
}

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
}

/* Estilos para los selects e inputs */
.form-control, .form-select {
  font-size: 0.875rem;
  padding: 0.25rem 0.5rem;
}

.form-control:focus, .form-select:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

/* Ajustes para la tabla con muchas columnas */
.table-sm th, .table-sm td {
  padding: 0.3rem 0.5rem;
  white-space: nowrap;
}

/* Hacer que las columnas numéricas sean más estrechas */
.table-sm td:nth-child(6) {
  width: 1%;
  white-space: nowrap;
}

/* Estilos para los badges de terminales */
.badge {
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.35em 0.65em;
}
</style>