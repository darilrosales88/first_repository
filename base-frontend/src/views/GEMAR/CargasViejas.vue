<template>
  <div>
    <div class="card border" style="margin-left: 15.8em; width: 79%">
      <Navbar-Component />
      <div class="card-header bg-light border-bottom">
        <h6 class="mb-0 text-dark fw-semibold">
          Sistema de Partes Controlados - Cargas Viejas
        </h6>
        <button
          class="btn btn-sm btn-outline-secondary"
          style="margin-top: 10px"
          @click="$router.push({ name: 'GEMAR' })"
        >
          <i class="bi bi-arrow-left me-1"></i> Volver a GEMAR
        </button>
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
                :max="maxDate"
                @change="cargarPartes"
              />
            </div>
            <label class="col-sm-2 col-form-label">Fecha actual:</label>
            <div class="col-sm-4">
              <input
                type="datetime-local"
                v-model="fechaActual"
                class="form-control form-control-sm"
                readonly
              />
            </div>
          </div>
        </div>

        <!-- Tabla de Cargas Viejas -->
        <div class="table-section">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h6 class="text-dark fw-semibold mb-0">
              Registro de Cargas Viejas
            </h6>
            <button @click="navigateToAddCarga" class="btn btn-sm btn-primary">
              <i class="bi bi-plus-circle me-1"></i> Agregar Carga
            </button>
          </div>

          <div class="table-responsive">
            <table class="table table-sm table-bordered table-hover">
              <thead class="table-light">
                <tr>
                  <th scope="col">No.</th>
                  <th scope="col">Puerto</th>
                  <th scope="col">Terminal</th>
                  <th scope="col">Producto</th>
                  <th scope="col">Manifiesto</th>
                  <th scope="col">Tons. Ayer</th>
                  <th scope="col">Tons. Hoy</th>
                  <th scope="col">Organismo</th>
                  <th scope="col">Días almacén</th>
                  <th scope="col">Plan</th>
                  <th scope="col">Real</th>
                  <th scope="col">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(carga, index) in cargas" :key="carga.id">
                  <td>{{ index + 1 }}</td>
                  <td>{{ getPuertoNombre(carga.puerto_id) }}</td>
                  <td>{{ getTerminalNombre(carga.terminal_id) }}</td>
                  <td>{{ getProductoNombre(carga.producto_id) }}</td>
                  <td>{{ carga.manifiesto }}</td>
                  <td>{{ carga.toneladas_ayer }}</td>
                  <td>{{ carga.toneladas_hoy }}</td>
                  <td>{{ getOrganismoNombre(carga.organismo_id) }}</td>
                  <td>{{ carga.dias_almacen }}</td>
                  <td>{{ carga.plan }}</td>
                  <td>{{ carga.real }}</td>
                  <td>
                    <div class="d-flex gap-1">
                      <button 
                        @click="editarCarga(carga.id)" 
                        class="btn btn-sm btn-outline-primary"
                      >
                        <i class="bi bi-pencil"></i> 
                      </button>
                      <button 
                        @click="eliminarCarga(carga.id)" 
                        class="btn btn-sm btn-outline-danger"
                      >
                        <i class="bi bi-trash"></i> 
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="cargas.length === 0">
                  <td colspan="12" class="text-center">No hay registros para mostrar</td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <!-- Paginación -->
          <div class="io-pagination d-flex justify-content-between align-items-center mt-3">
            <div class="text-muted small">
              Mostrando {{ cargas.length }} de {{ totalRegistros }} registros
            </div>
            <nav aria-label="Page navigation">
              <ul class="pagination pagination-sm mb-0">
                <li class="page-item" :class="{ disabled: !pagination.previous }">
                  <button class="page-link" @click="cambiarPagina(pagination.previous)">
                    <i class="bi bi-chevron-left"></i>
                  </button>
                </li>
                <li class="page-item disabled">
                  <span class="page-link">
                    Página {{ paginaActual }} de {{ totalPaginas }}
                  </span>
                </li>
                <li class="page-item" :class="{ disabled: !pagination.next }">
                  <button class="page-link" @click="cambiarPagina(pagination.next)">
                    <i class="bi bi-chevron-right"></i>
                  </button>
                </li>
              </ul>
            </nav>
          </div>
        </div>

        <!-- Botones de acción -->
        <div class="d-flex justify-content-center gap-3 mt-4">
          <button @click="guardarParte" class="btn btn-sm btn-success" :disabled="loading">
            <i class="bi bi-floppy me-1"></i> Guardar
          </button>
          <button @click="cancelar" class="btn btn-sm btn-outline-secondary" :disabled="loading">
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
  name: "CargasViejas",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      fechaOperacion: new Date().toISOString().split('T')[0],
      fechaActual: new Date().toISOString().slice(0, 16),
      cargas: [],
      puertos: [],
      terminales: [],
      productos: [],
      organismos: [],
      loading: false,
      parteId: null,
      pagination: {
        next: null,
        previous: null,
        count: 0
      },
      paginaActual: 1,
      totalPaginas: 1,
      totalRegistros: 0
    };
  },
  computed: {
    maxDate() {
      return new Date().toISOString().split('T')[0];
    },
    isAdmin() {
      const userData = JSON.parse(localStorage.getItem("userData") || "{}");
      return userData.is_superuser;
    },
    isGemarUser() {
      const userData = JSON.parse(localStorage.getItem("userData") || "{}");
      return userData.rol === "GEMAR" || userData.is_superuser;
    },
  },
  async created() {
    await this.cargarDatosIniciales();
    await this.cargarPartes();
  },
  methods: {
    getPuertoNombre(puertoId) {
      const puerto = this.puertos.find(p => p.id === puertoId);
      return puerto ? puerto.nombre_puerto : 'N/A';
    },
    
    getTerminalNombre(terminalId) {
      const terminal = this.terminales.find(t => t.id === terminalId);
      return terminal ? terminal.nombre_terminal : 'N/A';
    },
    
    getProductoNombre(productoId) {
      const producto = this.productos.find(p => p.id === productoId);
      return producto ? producto.nombre_producto : 'N/A';
    },
    
    getOrganismoNombre(organismoId) {
      const organismo = this.organismos.find(o => o.id === organismoId);
      return organismo ? organismo.nombre : 'N/A';
    },
    
    navigateToAddCarga() {
      this.$router.push({ name: 'AgregarCarga' });
    },
    
    editarCarga(id) {
      this.$router.push({ 
        name: 'EditarCarga', 
        params: { id: id } 
      });
    },
    
    async eliminarCarga(id) {
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
          await axios.delete(`/api/gemar/registros-carga-vieja/${id}/`, {
            headers: { 'Authorization': `Token ${token}` }
          });
          
          this.mostrarExito('Carga eliminada correctamente');
          await this.cargarPartes();
        }
      } catch (error) {
        console.error('Error al eliminar carga:', error);
        this.mostrarError('Error al eliminar la carga');
      }
    },
    
    cambiarPagina(url) {
      if (!url) return;
      
      // Extraer el número de página de la URL
      const pageMatch = url.match(/page=(\d+)/);
      if (pageMatch) {
        this.paginaActual = parseInt(pageMatch[1]);
        this.cargarPartes(url);
      }
    },
    
    async cargarPartes(url = null) {
      try {
        this.loading = true;
        const token = localStorage.getItem("token");

        if (!token) {
          this.mostrarError("No se encontró el token de autenticación");
          return;
        }

        const headers = {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        };

        const params = {
          fecha_operacion: this.fechaOperacion,
          page: this.paginaActual
        };
        
        // CORRECCIÓN: Usar la URL correcta según urls.py
        const apiUrl = url || "/api/gemar/registros-carga-vieja/";
        
        const response = await axios.get(apiUrl, {
          params: url ? null : params, // No enviar params si usamos URL completa
          headers: headers
        });

        this.cargas = response.data.results || [];
        this.totalRegistros = response.data.count || this.cargas.length;
        
        // Configurar paginación
        this.pagination = {
          next: response.data.next,
          previous: response.data.previous,
          count: response.data.count || 0
        };
        
        // Calcular total de páginas
        this.totalPaginas = Math.ceil(this.totalRegistros / (response.data.results?.length || 1));
        
      } catch (error) {
        console.error("Error al cargar partes:", error);
        let errorMessage = "Error al cargar los partes de carga vieja";
        if (error.response) {
          if (error.response.status === 403) {
            errorMessage = "No tiene permisos para acceder a estos datos";
          } else if (error.response.data?.detail) {
            errorMessage = error.response.data.detail;
          }
        }
        this.mostrarError(errorMessage);
      } finally {
        this.loading = false;
      }
    },

    async cargarDatosIniciales() {
      try {
        this.loading = true;
        const token = localStorage.getItem("token");

        if (!token) {
          this.mostrarError("No se encontró el token de autenticación");
          return;
        }

        const headers = {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        };

        // CORRECCIÓN: Usar las URLs correctas según el archivo urls.py
        const [puertosRes, productosRes, organismosRes, terminalesRes] = await Promise.all([
          axios.get("/api/puertos/", { headers }),
          axios.get("/api/productos/", { headers }),
          axios.get("/api/osde/", { headers }),
          axios.get("/api/terminales/", { headers }),
        ]);

        this.puertos = puertosRes.data.results || puertosRes.data || [];
        this.productos = productosRes.data.results || productosRes.data || [];
        this.organismos = organismosRes.data.results || organismosRes.data || [];
        this.terminales = terminalesRes.data.results || terminalesRes.data || [];

        // Normalizar datos
        this.puertos = this.puertos.map((p) => ({
          id: p.id,
          nombre_puerto: p.nombre_puerto || p.nombre || "",
        }));

        this.productos = this.productos.map((p) => ({
          id: p.id,
          nombre_producto: p.nombre_producto || p.nombre || "",
        }));

        this.organismos = this.organismos.map((o) => ({
          id: o.id,
          nombre: o.nombre || o.nombre_organismo || "",
          abreviatura: o.abreviatura || "",
        }));

        this.terminales = this.terminales.map((t) => ({
          id: t.id,
          nombre_terminal: t.nombre_terminal || t.nombre || "",
          puerto_id: t.puerto?.id || t.puerto_id || null,
        }));

      } catch (error) {
        console.error("Error al cargar datos:", error);
        let errorMessage = "Error al cargar datos iniciales";
        if (error.response) {
          console.error("Detalles del error:", error.response.data);
          if (error.response.status === 403) {
            errorMessage = "No tiene permisos para acceder a estos datos";
          } else if (error.response.data?.detail) {
            errorMessage = error.response.data.detail;
          }
        }
        this.mostrarError(errorMessage);
      } finally {
        this.loading = false;
      }
    },

    async guardarParte() {
      try {
        this.loading = true;
        
        if (this.cargas.length === 0) {
          this.mostrarError("No hay cargas para guardar");
          return;
        }

        const token = localStorage.getItem("token");
        const headers = {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        };

        // Crear el parte principal
        const parteData = {
          fecha_operacion: this.fechaOperacion,
          registros: this.cargas.map(carga => ({
            puerto_id: carga.puerto_id,
            terminal_id: carga.terminal_id,
            producto_id: carga.producto_id,
            manifiesto: carga.manifiesto,
            toneladas_ayer: carga.toneladas_ayer,
            toneladas_hoy: carga.toneladas_hoy,
            organismo_id: carga.organismo_id,
            dias_almacen: carga.dias_almacen,
            plan: carga.plan,
            real: carga.real
          }))
        };

        // Verificar si ya existe un parte para esta fecha
        let parteExistente = null;
        try {
          const response = await axios.get(`/gemar/partes-carga-vieja/?fecha_operacion=${this.fechaOperacion}`, { headers });
          if (response.data.results && response.data.results.length > 0) {
            parteExistente = response.data.results[0];
          }
        } catch (error) {
          console.log("No se encontró parte existente para esta fecha");
        }

        let response;
        if (parteExistente) {
          // Actualizar parte existente
          response = await axios.put(`/gemar/partes-carga-vieja/${parteExistente.id}/`, parteData, { headers });
        } else {
          // Crear nuevo parte
          response = await axios.post("/gemar/partes-carga-vieja/", parteData, { headers });
        }

        this.mostrarExito("Parte guardado correctamente");
        await this.cargarPartes();
        
      } catch (error) {
        console.error("Error al guardar parte:", error);
        let errorMessage = "Error al guardar el parte";
        if (error.response) {
          if (error.response.status === 403) {
            errorMessage = "No tiene permisos para realizar esta acción";
          } else if (error.response.data?.detail) {
            errorMessage = error.response.data.detail;
          } else if (error.response.data) {
            errorMessage = JSON.stringify(error.response.data);
          }
        }
        this.mostrarError(errorMessage);
      } finally {
        this.loading = false;
      }
    },

    cancelar() {
      this.fechaOperacion = new Date().toISOString().split('T')[0];
      this.cargarPartes();
    },

    mostrarError(mensaje) {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: mensaje,
        confirmButtonText: "Aceptar",
      });
    },

    mostrarExito(mensaje) {
      Swal.fire({
        icon: "success",
        title: "Éxito",
        text: mensaje,
        confirmButtonText: "Aceptar",
      });
    },
  },
};
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

.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  color: white;
}

.btn-outline-primary {
  color: #0d6efd;
  border-color: #0d6efd;
}

.btn-outside-primary:hover {
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

.btn-success {
  background-color: #198754;
  border-color: #198754;
}

.btn-success:hover {
  background-color: #157347;
  border-color: #146c43;
}

.form-control,
.form-select {
  font-size: 0.875rem;
  padding: 0.25rem 0.5rem;
}

.form-control:focus,
.form-select:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.table-sm th,
.table-sm td {
  padding: 0.3rem 0.5rem;
  white-space: nowrap;
}

.table-sm td:nth-child(5),
.table-sm td:nth-child(6),
.table-sm td:nth-child(8),
.table-sm td:nth-child(10),
.table-sm td:nth-child(11) {
  width: 1%;
  white-space: nowrap;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
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
</style>