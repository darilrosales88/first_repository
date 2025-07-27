<template>
  <div>
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h6 class="mb-0 text-dark fw-semibold">
          Sistema de Partes Controlados
        </h6>
      </div>
      <div class="card-body p-3">
        <!-- Formulario de Cargas Viejas -->
        <div class="form-section mb-4">
          <h6 class="text-dark fw-semibold mb-3">Cargas viejas GEMAR</h6>
          
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

        <!-- Tabla de Cargas Viejas -->
        <div class="table-section">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h6 class="text-dark fw-semibold mb-0">Registro de Cargas Viejas</h6>
            <button @click="addCarga" class="btn btn-sm btn-primary">
              <i class="bi bi-plus-circle me-1"></i> Agregar Carga
            </button>
          </div>
          
          <div class="table-responsive">
            <table class="table table-sm table-bordered table-hover">
              <thead class="table-light">
                <tr>
                  <th scope="col">No.</th>
                  <th scope="col">Puerto</th>
                  <th scope="col">Producto</th>
                  <th scope="col">Manifiesto</th>
                  <th scope="col">Tons. Ayer</th>
                  <th scope="col">Tons. Hoy</th>
                  <th scope="col">Organismo</th>
                  <th scope="col">Días almacén</th>
                  <th scope="col">Operación</th>
                  <th scope="col">Plan</th>
                  <th scope="col">Real</th>
                  <th scope="col">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(carga, index) in cargas" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td>
                    <select v-model="carga.puerto_id" class="form-select form-select-sm">
                      <option value="">Seleccione...</option>
                      <option 
                        v-for="puerto in puertos" 
                        :value="puerto.id"
                        :key="puerto.id"
                      >
                        {{ puerto.nombre }}
                      </option>
                    </select>
                    <span v-if="carga.puerto_id && !puertos.find(p => p.id === carga.puerto_id)" class="text-danger small">
                      Puerto no encontrado
                    </span>
                  </td>
                  
                  <td>
                    <select v-model="carga.producto_id" class="form-select form-select-sm">
                      <option value="">Seleccione...</option>
                      <option 
                        v-for="producto in productos" 
                        :value="producto.id"
                        :key="producto.id"
                      >
                        {{ producto.nombre }}
                      </option>
                    </select>
                    <span v-if="carga.producto_id && !productos.find(p => p.id === carga.producto_id)" class="text-danger small">
                      Producto no encontrado
                    </span>
                  </td>

                  <td>
                    <input 
                      type="text" 
                      v-model="carga.manifiesto" 
                      class="form-control form-control-sm"
                    >
                  </td>
                  <td>
                    <input 
                      type="number" 
                      v-model="carga.toneladas_ayer" 
                      class="form-control form-control-sm"
                      step="0.01"
                      min="0"
                    >
                  </td>
                  <td>
                    <input 
                      type="number" 
                      v-model="carga.toneladas_hoy" 
                      class="form-control form-control-sm"
                      step="0.01"
                      min="0"
                    >
                  </td>

                  <td>
                    <select v-model="carga.organismo_id" class="form-select form-select-sm">
                      <option value="">Seleccione...</option>
                      <option 
                        v-for="organismo in organismos" 
                        :value="organismo.id"
                        :key="organismo.id"
                      >
                        {{ organismo.nombre }}
                      </option>
                    </select>
                    <span v-if="carga.organismo_id && !organismos.find(o => o.id === carga.organismo_id)" class="text-danger small">
                      Organismo no encontrado
                    </span>
                  </td>

                  <td>
                    <input 
                      type="number" 
                      v-model="carga.dias_almacen" 
                      class="form-control form-control-sm"
                      min="0"
                    >
                  </td>
                  <td>
                    <select v-model="carga.operacion" class="form-select form-select-sm">
                      <option value="carga">Carga</option>
                      <option value="descarga">Descarga</option>
                    </select>
                  </td>
                  <td>
                    <input 
                      type="number" 
                      v-model="carga.plan" 
                      class="form-control form-control-sm"
                      step="0.01"
                      min="0"
                    >
                  </td>
                  <td>
                    <input 
                      type="number" 
                      v-model="carga.real" 
                      class="form-control form-control-sm"
                      step="0.01"
                      min="0"
                    >
                  </td>
                  <td>
                    <button @click="removeCarga(index)" class="btn btn-sm btn-outline-danger">
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
          <button @click="guardar" class="btn btn-sm btn-primary">
            <i class="bi bi-save me-1"></i> Guardar
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

export default {
  name: 'CargasViejas',
  data() {
    return {
      fechaOperacion: '',
      fechaActual: new Date().toISOString().slice(0, 16),
      cargas: [{
        puerto_id: '',
        producto_id: '',
        manifiesto: '',
        toneladas_ayer: 0,
        toneladas_hoy: 0,
        organismo_id: '',
        dias_almacen: 0,
        operacion: 'carga',
        plan: 0,
        real: 0
      }],
      puertos: [],
      productos: [],
      organismos: [],
      loading: false
    }
  },
  async created() {
    await this.cargarDatosIniciales();
    console.log('Puertos cargados:', this.puertos);
    console.log('Productos cargados:', this.productos);
    console.log('Organismos cargados:', this.organismos);
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
  methods: {
    async cargarCargasViejas() {
      try {
        const token = localStorage.getItem('token');
        const headers = { 
          Authorization: `Token ${token}`,
          'Content-Type': 'application/json'
        };
        
        const response = await axios.get('/api/gemar/cargas-viejas/', { 
          headers,
          params: {
            fecha_operacion: this.fechaOperacion
          }
        });
        
        if (response.data && Array.isArray(response.data)) {
          this.cargas = response.data.map(item => ({
            id: item.id,
            puerto_id: item.puerto?.id || '',
            terminal_id: item.terminal?.id || '',
            producto_id: item.producto?.id || '',
            manifiesto: item.manifiesto,
            toneladas_ayer: item.toneladas_ayer,
            toneladas_hoy: item.toneladas_hoy,
            organismo_id: item.organismo?.id || '',
            dias_almacen: item.dias_almacen,
            operacion: item.operacion || 'carga',
            plan: item.plan,
            real: item.real
          }));
        }
      } catch (error) {
        console.error('Error al cargar cargas viejas:', error);
      }
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
          Authorization: `Token ${token}`,
          'Content-Type': 'application/json'
        };
        
        // Configura Axios para usar credenciales
        axios.defaults.withCredentials = true;
        
        // Usar la misma URL base para todas las peticiones
        const baseURL = 'http://127.0.0.1:8000';
        
        const [puertosRes, productosRes, organismosRes] = await Promise.all([
          axios.get(`${baseURL}/api/puertos`, { headers }),
          axios.get(`${baseURL}/api/productos`, { headers }),
          axios.get(`${baseURL}/api/osde`, { headers })
        ]);
        
        // Verificar que los datos sean arrays válidos
        this.puertos = Array.isArray(puertosRes.data) ? puertosRes.data : [];
        this.productos = Array.isArray(productosRes.data) ? productosRes.data : [];
        this.organismos = Array.isArray(organismosRes.data) ? organismosRes.data : [];
        
        // Si los arrays están vacíos, mostrar advertencia
        if (this.puertos.length === 0) console.warn('No se cargaron puertos');
        if (this.productos.length === 0) console.warn('No se cargaron productos');
        if (this.organismos.length === 0) console.warn('No se cargaron organismos');
        
      } catch (error) {
        console.error('Error al cargar datos:', error);
        let errorMessage = 'Error al cargar datos iniciales';
        if (error.response) {
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

    
    addCarga() {
      this.cargas.push({
        puerto_id: null,
        producto_id: null,
        manifiesto: '',
        toneladas_ayer: 0,
        toneladas_hoy: 0,
        organismo_id: null,
        dias_almacen: 0,
        operacion: 'carga',
        plan: 0,
        real: 0
      });
    },
    
    removeCarga(index) {
      this.cargas.splice(index, 1);
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
        
        const token = localStorage.getItem('token');
        const headers = { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        };
        
        const payload = {
          fecha_operacion: this.fechaOperacion,
          cargas: this.cargas.filter(c => 
            c.puerto_id && c.producto_id && c.organismo_id
          ).map(c => ({
            puerto_id: c.puerto_id,
            producto_id: c.producto_id,
            manifiesto: c.manifiesto,
            toneladas_ayer: c.toneladas_ayer,
            toneladas_hoy: c.toneladas_hoy,
            organismo_id: c.organismo_id,
            dias_almacen: c.dias_almacen,
            plan: c.plan,
            real: c.real
          }))
        };
        
        const response = await axios.post('/api/gemar/cargas-viejas/', payload, { headers });
        if (response.status === 403) {
          this.mostrarError('No tiene permisos para realizar esta acción');
          return;
        }
        this.mostrarExito('Cargas viejas guardadas correctamente');
        this.cargas = [{
          puerto_id: null,
          producto_id: null,
          manifiesto: '',
          toneladas_ayer: 0,
          toneladas_hoy: 0,
          organismo_id: null,
          dias_almacen: 0,
          operacion: 'carga',
          plan: 0,
          real: 0
        }];
        this.$emit('parte-creado'); // Emitir evento para actualizar la vista principal
      } catch (error) {
        console.error('Error al guardar:', error);
        this.mostrarError('Error al guardar las cargas viejas');
      }
    },
    
    cancelar() {
      this.cargas = [{
        puerto_id: null,
        producto_id: null,
        manifiesto: '',
        toneladas_ayer: 0,
        toneladas_hoy: 0,
        organismo_id: null,
        dias_almacen: 0,
        operacion: 'carga',
        plan: 0,
        real: 0
      }];
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
.table-sm td:nth-child(5),
.table-sm td:nth-child(6),
.table-sm td:nth-child(8),
.table-sm td:nth-child(10),
.table-sm td:nth-child(11) {
  width: 1%;
  white-space: nowrap;
}
</style>