<template>
    <div class="container py-3">
      <div class="card border">
        <div class="card-header bg-light border-bottom">
          <h5 class="mb-0 text-dark fw-semibold">
            <i class="bi bi-clipboard-data me-2"></i>Informes Operativos UFC
          </h5>
        </div>
        
        <div class="card-body p-3">
          <!-- Filtro por fecha -->
          <div class="row mb-3">
            <div class="col-md-4">
              <input 
                type="date" 
                class="form-control form-control-sm"
                v-model="fechaFiltro"
                @change="cargarInformes"
              >
            </div>
          </div>
  
          <!-- Tabla de informes -->
          <div class="table-responsive">
            <table class="table table-sm table-hover">
              <thead>
                <tr>
                  <th>Fecha Operación</th>
                  <th>Plan Mensual</th>
                  <th>Plan Diario</th>
                  <th>Vagones Cargados</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="informe in informes" :key="informe.id">
                  <td>{{ formatDate(informe.fecha_operacion) }}</td>
                  <td>{{ informe.plan_mensual_total }}</td>
                  <td>{{ informe.plan_diario_total_vagones_cargados }}</td>
                  <td>{{ informe.real_total_vagones_cargados }}</td>
                  <td>
                    <button 
                      class="btn btn-sm btn-outline-primary"
                      @click="verDetalle(informe.id)"
                    >
                      <i class="bi bi-eye"></i> Ver
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
  
      <!-- Modal de detalle -->
      <div v-if="informeSeleccionado" class="modal fade show" style="display: block; background: rgba(0,0,0,0.5)">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Detalle del Informe</h5>
              <button type="button" class="btn-close" @click="informeSeleccionado = null"></button>
            </div>
            <div class="modal-body">
              <!-- Mostrar datos principales -->
              <div class="row mb-3">
                <div class="col-md-6">
                  <strong>Fecha Operación:</strong> {{ formatDate(informeSeleccionado.fecha_operacion) }}
                </div>
                <div class="col-md-6">
                  <strong>Plan Mensual:</strong> {{ informeSeleccionado.plan_mensual_total }}
                </div>
              </div>
              
              <!-- Mostrar relaciones -->
              <div class="accordion" id="accordionDetalle">
                <!-- Vagones y Productos -->
                <div class="accordion-item">
                  <h2 class="accordion-header">
                    <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseVagones">
                      Vagones y Productos ({{ informeSeleccionado.vagones_y_productos.length }})
                    </button>
                  </h2>
                  <div id="collapseVagones" class="accordion-collapse collapse show">
                    <div class="accordion-body">
                      <table class="table table-sm">
                        <thead>
                          <tr>
                            <th>Vagón</th>
                            <th>Producto</th>
                            <th>Cantidad</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="item in informeSeleccionado.vagones_y_productos" :key="item.id">
                            <td>{{ item.vagon }}</td>
                            <td>{{ item.producto }}</td>
                            <td>{{ item.cantidad }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
                
                <!-- Otras relaciones (similar al anterior) -->
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="informeSeleccionado = null">Cerrar</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import Swal from 'sweetalert2';
  
  export default {
    name: 'PartesUFC',
    data() {
      return {
        informes: [],
        informeSeleccionado: null,
        fechaFiltro: null,
        isLoading: false,
        itemsPerPage: 10, // Cantidad de items por página
        pagination: {
        current_page: 1,
        total_pages: 1,
        total_items: 0
       }
      }
    },
    mounted() {
      this.cargarInformes();
    },
    methods: {
        async cargarInformes(page = 1) {
  this.isLoading = true;
  try {
    // Construir parámetros de consulta
    const params = {
      page: page,
      page_size: this.itemsPerPage // Definido en data() como 10 por ejemplo
    };

    // Agregar filtro por fecha si existe
    if (this.fechaFiltro) {
      params.fecha_operacion = this.fechaFiltro;
    }

    // Realizar la petición
    const response = await axios.get('/ufc/informe-operativo/', { params });

    // Asignar los resultados
    this.informes = response.data.results;
    
    // Configurar la paginación
    this.pagination = {
      current_page: page,
      total_pages: Math.ceil(response.data.count / this.itemsPerPage),
      total_items: response.data.count
    };
    console.log("Datos que se deben mostrar: ",this.informes);

  } catch (error) {
    console.error('Error cargando informes:', error);
    
    let errorMessage = 'No se pudieron cargar los informes';
    if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail;
    } else if (error.response?.status === 403) {
      errorMessage = 'No tiene permisos para ver estos datos';
    }

    await Swal.fire({
      title: 'Error',
      text: errorMessage,
      icon: 'error',
      confirmButtonText: 'Entendido'
    });
    
    // Reiniciar estado en caso de error
    this.informes = [];
    this.pagination = {
      current_page: 1,
      total_pages: 1,
      total_items: 0
    };
  } finally {
    this.isLoading = false;
  }
},
      
      async verDetalle(id) {
        try {
          const response = await axios.get(`/ufc/informe-operativo/${id}/`);
          this.informeSeleccionado = response.data;
        } catch (error) {
          console.error('Error cargando detalle:', error);
          Swal.fire({
            title: 'Error',
            text: 'No se pudo cargar el detalle del informe',
            icon: 'error'
          });
        }
      },
      
      formatDate(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleDateString('es-ES');
      }
    }
  }
  </script>
  
  <style scoped>
  /* Estilos personalizados si los necesitas */
  </style>