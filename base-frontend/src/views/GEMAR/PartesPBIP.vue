<template>
  <div>
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h6 class="mb-0 text-dark fw-semibold">
          Sistema de Partes Controlados
        </h6>
      </div>
      <div class="card-body p-3">
        <!-- Formulario de PBIP -->
        <div class="form-section mb-4">
          <h6 class="text-dark fw-semibold mb-3">Parte de PBIP</h6>
          
          <div class="row mb-3">
            <label class="col-sm-2 col-form-label">Fecha operación:*</label>
            <div class="col-sm-4">
              <input 
                type="date" 
                v-model="parte.fecha_operacion" 
                class="form-control form-control-sm"
                required
              >
            </div>
          </div>
          
          <div class="row mb-3">
            <label class="col-sm-2 col-form-label">Fecha actual:*</label>
            <div class="col-sm-4">
              <input 
                type="datetime-local" 
                v-model="parte.fecha_actual" 
                class="form-control form-control-sm"
                readonly
              >
            </div>
          </div>
        </div>

        <!-- Tabla de Protección de Buques -->
        <div class="table-section">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h6 class="text-dark fw-semibold mb-0">Protección de Buques en Instalaciones Portuarias</h6>
            <button @click="addBuque" class="btn btn-sm btn-primary">
              <i class="bi bi-plus-circle me-1"></i> Agregar Buque
            </button>
          </div>
          
          <div class="table-responsive">
            <table class="table table-sm table-bordered table-hover">
              <thead class="table-light">
                <tr>
                  <th scope="col">No.</th>
                  <th scope="col">Buque</th>
                  <th scope="col">Puerto de Arribo</th>
                  <th scope="col">Fecha y Hora</th>
                  <th scope="col">Nivel</th>
                  <th scope="col">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in buques" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td>
                    <select v-model="item.buque_id" class="form-select form-select-sm">
                      <option value="">Seleccione...</option>
                      <option 
                        v-for="buque in listaBuques" 
                        :value="buque.id"
                        :key="buque.id"
                      >
                        {{ buque.nombre }}
                      </option>
                    </select>
                  </td>
                  <td>
                    <select v-model="item.puerto_id" class="form-select form-select-sm">
                      <option value="">Seleccione...</option>
                      <option 
                        v-for="puerto in listaPuertos" 
                        :value="puerto.id"
                        :key="puerto.id"
                      >
                        {{ puerto.nombre }}
                      </option>
                    </select>
                  </td>
                  <td>
                    <input 
                      type="datetime-local" 
                      v-model="item.fecha_hora" 
                      class="form-control form-control-sm"
                    >
                  </td>
                  <td>
                    <select v-model="item.nivel" class="form-select form-select-sm">
                      <option value="1">Nivel 1</option>
                      <option value="2">Nivel 2</option>
                      <option value="3">Nivel 3</option>
                    </select>
                  </td>
                  <td>
                    <button @click="removeBuque(index)" class="btn btn-sm btn-outline-danger">
                      <i class="bi bi-trash"></i> Eliminar
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
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

        <!-- Botones de acción -->
        <div class="d-flex justify-content-center gap-3 mt-4">
          <button @click="rechazar" class="btn btn-sm btn-outline-danger">
            <i class="bi bi-x-circle me-1"></i> Rechazar
          </button>
          <button @click="aprobar" class="btn btn-sm btn-outline-success">
            <i class="bi bi-check-circle me-1"></i> Aprobar
          </button>
          <button @click="listo" class="btn btn-sm btn-outline-primary">
            <i class="bi bi-check-all me-1"></i> Listo
          </button>
          <button @click="cancelar" class="btn btn-sm btn-outline-secondary">
            <i class="bi bi-x me-1"></i> Cancelar
          </button>
          <button @click="aceptar" class="btn btn-sm btn-primary">
            <i class="bi bi-save me-1"></i> Aceptar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: 'PartesPBIP',
  data() {
    return {
      parte: {
        fecha_operacion: '',
        fecha_actual: new Date().toISOString().slice(0, 16),
      },
      buques: [],
      listaBuques: [],
      listaPuertos: [],
      loading: false,
      error: null
    }
  },
  async created() {
    await this.cargarDatosIniciales();
  },
  computed: {
    isAdmin() {
      const userData = JSON.parse(localStorage.getItem('userData') || '{}');
      return userData.is_superuser || false;
    },
    isGemarUser() {
      const userData = JSON.parse(localStorage.getItem('userData') || '{}');
      return !userData.is_superuser; // O la lógica específica para GEMAR
    }
},
  methods: {
    async cargarDatosIniciales() {
      try {
        this.loading = true;
        const token = localStorage.getItem('token');
        const headers = { Authorization: `Bearer ${token}` };
        
        const [buquesRes, puertosRes] = await Promise.all([
          axios.get('/api/embarcaciones/', { headers }),
          axios.get('/api/puertos/', { headers })
        ]);
        
        this.listaBuques = buquesRes.data;
        this.listaPuertos = puertosRes.data;
      } catch (error) {
        this.error = 'Error al cargar datos iniciales';
        this.mostrarError(this.error);
      } finally {
        this.loading = false;
      }
    },
    
    addBuque() {
      this.buques.push({
        buque_id: null,
        puerto_id: null,
        fecha_hora: new Date().toISOString().slice(0, 16),
        nivel: 1
      });
    },
    
    removeBuque(index) {
      this.buques.splice(index, 1);
    },
    
    async aceptar() {
      if (!this.validarFormulario()) return;
      
      try {
        this.loading = true;
        const token = localStorage.getItem('token');
        const headers = { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        };
        
        const payload = {
          fecha_operacion: this.parte.fecha_operacion,
          buques: this.buques.map(b => ({
            buque_id: b.buque_id,
            puerto_id: b.puerto_id,
            fecha_hora: b.fecha_hora,
            nivel: b.nivel
          }))
        };
        
        await axios.post('/api/gemar/partes-pbip/', payload, { headers });
        this.mostrarExito('Parte PBIP creado correctamente');
        this.resetFormulario();
        this.$emit('parte-creado'); // Emitir evento para actualizar la vista principal
      } catch (error) {
        this.error = this.obtenerMensajeError(error);
        this.mostrarError(this.error);
      } finally {
        this.loading = false;
      }
    },
    
    validarFormulario() {
      if (!this.parte.fecha_operacion) {
        this.error = 'La fecha de operación es requerida';
        return false;
      }
      
      if (this.buques.length === 0) {
        this.error = 'Debe agregar al menos un buque';
        return false;
      }
      
      for (const buque of this.buques) {
        if (!buque.buque_id || !buque.puerto_id || !buque.fecha_hora) {
          this.error = 'Todos los campos son requeridos para cada buque';
          return false;
        }
      }
      
      this.error = null;
      return true;
    },
    
    obtenerMensajeError(error) {
      if (error.response) {
        if (error.response.data) {
          if (typeof error.response.data === 'object') {
            return Object.values(error.response.data).join(' ');
          }
          return error.response.data;
        }
        return error.response.statusText;
      }
      return 'Error de conexión con el servidor';
    },
    
    resetFormulario() {
      this.parte = {
        fecha_operacion: '',
        fecha_actual: new Date().toISOString().slice(0, 16)
      };
      this.buques = [];
      this.error = null;
    },
    
    cancelar() {
      this.resetFormulario();
    },
    
    async rechazar() {
      // Implementar lógica para rechazar si es necesario
    },
    
    async aprobar() {
      // Implementar lógica para aprobar
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
  color: #28a745;
  border-color: #28a745;
}

.btn-outline-success:hover {
  background-color: #28a745;
  color: white;
}

.btn-outline-primary {
  color: #0d6efd;
  border-color: #0d6efd;
}

.btn-outline-primary:hover {
  background-color: #0d6efd;
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
</style>