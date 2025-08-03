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

        <!-- Tabla de Terminales -->
        <div class="table-section">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h6 class="text-dark fw-semibold mb-0">Mercancia</h6>
            <button @click="navigateToAddMercancia" class="btn btn-sm btn-primary">
      <i class="bi bi-plus-circle me-1"></i> Agregar Mercancia
    </button>
          </div>
          
          <div class="table-responsive">
            <table class="table table-sm table-bordered table-hover">
              <thead class="table-light">
                <tr>
                  <th scope="col">No.</th>
                  <th scope="col">Terminal</th>
                  <th scope="col">Capacidad Importación</th>
                  <th scope="col">Capacidad Exportación</th>
                  <th scope="col">Existencia Importación</th>
                  <th scope="col">Existencia Exportación</th>
                  <th scope="col">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(terminal, index) in terminales" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td>
                    <select v-model="terminal.terminal_id" class="form-select form-select-sm">
                      <option value="">Seleccione...</option>
                      <option 
                        v-for="term in listaTerminales" 
                        :value="term.id"
                        :key="term.id"
                      >
                        {{ term.nombre }}
                      </option>
                    </select>
                  </td>
                  <td>
                    <input 
                      type="number" 
                      v-model="terminal.capacidad_importacion" 
                      class="form-control form-control-sm"
                      step="0.01"
                      min="0"
                    >
                  </td>
                  <td>
                    <input 
                      type="number" 
                      v-model="terminal.capacidad_exportacion" 
                      class="form-control form-control-sm"
                      step="0.01"
                      min="0"
                    >
                  </td>
                  <td>
                    <input 
                      type="number" 
                      v-model="terminal.existencia_importacion" 
                      class="form-control form-control-sm"
                      step="0.01"
                      min="0"
                    >
                  </td>
                  <td>
                    <input 
                      type="number" 
                      v-model="terminal.existencia_exportacion" 
                      class="form-control form-control-sm"
                      step="0.01"
                      min="0"
                    >
                  </td>
                  <td>
  <div class="d-flex gap-1">
    <button 
      @click="editarMercancia(terminal.terminal_id || index)" 
      class="btn btn-sm btn-outline-primary"
    >
      <i class="bi bi-pencil"></i> 
    </button>
    <button 
      @click="saveTerminal(index)" 
      class="btn btn-sm btn-outline-success me-2"
    >
      <i class="bi bi-check-circle"></i> Guardar
    </button>
    <button 
      @click="removeTerminal(index)" 
      class="btn btn-sm btn-outline-danger"
    >
      <i class="bi bi-trash"></i> 
    </button>
  </div>
</td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <!-- Lista de Mercancias disponibles -->
          <div class="mt-3 p-3 bg-light rounded">
            <h6 class="text-dark fw-semibold mb-2">Mercancias disponibles:</h6>
            <div class="d-flex flex-wrap gap-2">
              <span v-for="term in listaMercansias" :key="term.id" class="badge bg-secondary">
                {{ term.nombre }}
              </span>
            </div>
          </div>
          
          <!-- Paginación -->
          <div class="io-pagination d-flex justify-content-between align-items-center mt-3">
            <div class="text-muted small">
              Mostrando 1-15 de 30 registros
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
                    Página 1 de 2
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

        <!-- Filtros de Productos -->
        <div class="p-3 mb-4 bg-light rounded">
          <h6 class="text-dark fw-semibold mb-3">Productos</h6>
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
      fechaOperacion: '',
      fechaActual: new Date().toISOString().slice(0, 16),
      terminales: [],
      listaMercansias: [],
      tipoProducto: 'importacion',
      loading: false,
      debugInfo: {
        terminalesResponse: null
      }
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
    }
  },
  async created() {
    await this.cargarDatosIniciales();
    console.log('Datos cargados:', {
      terminales: this.listaTerminales,
      debugInfo: this.debugInfo
    });
  },
  methods: {
    editarMercancia(id) {
    // Navegar a la página de edición con el ID de la terminal
    if (!id) {
      this.mostrarError('No se puede editar una terminal sin ID');
      return;
    }
    
    this.$router.push({ 
      name: 'EditarExistenciaMercancia', 
      params: { id: id } 
    });
  },
    navigateToAddMercancia() {
      this.$router.push({ name: 'AgregarExistenciaMercancia' });
    },
    async cargarDatosIniciales() {
      try {
        this.loading = true;
        const token = localStorage.getItem('token');
        
        if (!token) {
          this.mostrarError('No se encontró el token de autenticación');
          return;
        }
        
        const headers = { 
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        };
        
        const instance = axios.create({
          baseURL: 'http://127.0.0.1:8000',
          headers: headers,
          withCredentials: true
        });
        
        const response = await instance.get('/api/terminales/');
        this.debugInfo.terminalesResponse = response.data;
        this.listaTerminales = response.data.results || [];
        
        this.listaTerminales = this.listaTerminales.map(t => ({
          id: t.id,
          nombre: t.nombre || t.nombre_terminal || '',
        }));
        
      } catch (error) {
        console.error('Error al cargar terminales:', error);
        let errorMessage = 'Error al cargar terminales';
        if (error.response) {
          console.error('Detalles del error:', error.response.data);
          if (error.response.status === 403) {
            errorMessage = 'No tiene permisos para acceder a estos datos';
          } else if (error.response.data?.detail) {
            errorMessage = error.response.data.detail;
          }
        }
        this.mostrarError(errorMessage);
      } finally {
        this.loading = false;
      }
    },

    addTerminal() {
      this.terminales.push({
        terminal_id: null,
        capacidad_importacion: 0,
        capacidad_exportacion: 0,
        existencia_importacion: 0,
        existencia_exportacion: 0
      });
    },
    
    removeTerminal(index) {
      if (this.terminales.length > 1) {
        this.terminales.splice(index, 1);
      } else {
        this.mostrarError('Debe haber al menos una terminal');
      }
    },
    
    async saveTerminal(index) {
      try {
        const terminal = this.terminales[index];
        
        if (!terminal.terminal_id) {
          this.mostrarError('Debe seleccionar una terminal');
          return;
        }
        
        // Validar que los valores numéricos no sean negativos
        if (terminal.capacidad_importacion < 0 || 
            terminal.capacidad_exportacion < 0 || 
            terminal.existencia_importacion < 0 || 
            terminal.existencia_exportacion < 0) {
          this.mostrarError('Los valores no pueden ser negativos');
          return;
        }
        
        // Aquí podrías implementar lógica adicional para validar
        // que las existencias no superen las capacidades, etc.
        
        this.mostrarExito('Datos de la terminal validados correctamente');
        
      } catch (error) {
        console.error('Error al validar terminal:', error);
        this.mostrarError('Error al validar los datos de la terminal');
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
        
        // Primero validamos todas las terminales
        for (const terminal of this.terminales) {
          if (!terminal.terminal_id) {
            this.mostrarError('Todas las terminales deben estar seleccionadas');
            return;
          }
        }
        
        const token = localStorage.getItem('token');
        const headers = { 
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        };
        
        const payload = {
          fecha_operacion: this.fechaOperacion,
          terminales: this.terminales.filter(t => t.terminal_id).map(t => ({
            terminal_id: t.terminal_id,
            capacidad_importacion: t.capacidad_importacion,
            capacidad_exportacion: t.capacidad_exportacion,
            existencia_importacion: t.existencia_importacion,
            existencia_exportacion: t.existencia_exportacion,
            tipo: this.tipoProducto === 'importacion' ? 1 : 2
          }))
        };
        
        if (payload.terminales.length === 0) {
          this.mostrarError('Debe agregar al menos una terminal válida');
          return;
        }
        
        const instance = axios.create({
          baseURL: 'http://127.0.0.1:8000',
          headers: headers,
          withCredentials: true
        });
        
        const response = await instance.post('/api/gemar/existencias-mercancia/', payload);
        
        if (response.status === 201) {
          this.mostrarExito('Existencias de mercancía guardadas correctamente');
          this.terminales = [{
            terminal_id: null,
            capacidad_importacion: 0,
            capacidad_exportacion: 0,
            existencia_importacion: 0,
            existencia_exportacion: 0
          }];
          this.$emit('parte-creado');
        } else {
          this.mostrarError('Error inesperado al guardar las existencias');
        }
      } catch (error) {
        console.error('Error al guardar:', error);
        let errorMessage = 'Error al guardar las existencias de mercancía';
        if (error.response) {
          if (error.response.status === 400) {
            errorMessage = error.response.data.detail || 'Datos inválidos';
          } else if (error.response.status === 403) {
            errorMessage = 'No tiene permisos para realizar esta acción';
          }
        }
        this.mostrarError(errorMessage);
      }
    },
    
    //cancelar() {
      //this.terminales = [{
        //terminal_id: null,
        //capacidad_importacion: 0,
        //capacidad_exportacion: 0,
        //existencia_importacion: 0,
        //existencia_exportacion: 0
      //}];
    //},
    
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
.table-sm td:nth-child(3),
.table-sm td:nth-child(4),
.table-sm td:nth-child(5),
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