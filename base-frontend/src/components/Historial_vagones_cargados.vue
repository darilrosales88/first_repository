<template>
    <div class="historial-vagones-container">
      <!-- Header con título y acciones -->
      <div class="hv-header">
        <h1 class="hv-title">
          <i class="bi bi-clock-history hv-title-icon"></i>
          Historial de Vagones
        </h1>
  
        <div class="hv-actions">
          <!-- Buscador moderno -->
          <div class="hv-search-container">
            <i class="bi bi-search hv-search-icon"></i>
            <input
              type="search"
              class="hv-search-input"
              placeholder="Buscar registros..."
              v-model="searchQuery"
              @input="handleSearchInput"
            />
            <div class="hv-search-border"></div>
          </div>
        </div>
      </div>
  
      <!-- Tarjeta contenedora de la tabla -->
      <div class="hv-card">
        <!-- Tabla con diseño moderno -->
        <div class="hv-table-container">
          <table class="hv-table">
            <thead>
              <tr>
                <th class="hv-th">Origen</th>
                <th class="hv-th">Estado</th>
                <th class="hv-th">Plan diario de carga descarga</th>
                <th class="hv-th">Real carga descarga</th>
                <th class="hv-th">Cantidad</th>
                <th class="hv-th">Fecha</th>
                <th class="hv-th">Ubicación</th>
                <th class="hv-th hv-th-actions">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <!-- Estado de carga -->
              <tr v-if="loading">
                <td colspan="9" class="hv-loading-td">
                  <div class="hv-loading">
                    <div class="hv-spinner"></div>
                    <span>Cargando registros...</span>
                  </div>
                </td>
              </tr>
  
              <!-- Filas de datos -->
              <tr
                v-for="(item, index) in filteredRecords"
                :key="item.id"
                class="hv-tr"
              >               
                <td class="hv-td">{{ item.origen }}</td>
                <td class="hv-td">
                  <span
                    :class="`hv-status hv-status-${getStatusClass(item.estado)}`"
                  >
                    {{ item.estado }}
                  </span>
                </td>
                <td class="hv-td">{{ item.plan_diario_carga_descarga }}</td>
                <td class="hv-td">
                  {{ item.real_carga_descarga || '-' }}
                </td>
                <td class="hv-td">
                  <span class="hv-badge hv-badge-primary">{{ item.cantidad }}</span>
                </td>
                <td class="hv-td">{{ formatDate(item.fecha_operacion) }}</td>
                <td class="hv-td">{{ item.ubicacion || 'N/A' }}</td>
  
                <!-- En la parte de las acciones de la tabla (dentro del <td>) -->
                <td class="hv-td hv-td-actions">
                  <div class="d-flex">
                    <button
                      @click="viewDetails(item)"
                      class="btn btn-sm btn-outline-info me-2"
                      title="Ver detalles"
                    >
                      <i class="bi bi-eye-fill"></i>
                    </button>
                    <button
                      @click="confirmDelete(item.id)"
                      class="btn btn-sm btn-outline-danger"
                      title="Eliminar"
                      :disabled="loading"
                    >
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
  
              <!-- Estado vacío -->
              <tr v-if="!loading && filteredRecords.length === 0">
                <td colspan="9" class="hv-empty-td">
                  <div class="hv-empty-state">
                    <i class="bi bi-database-exclamation"></i>
                    <h3>
                      {{
                        searchQuery ? "No hay coincidencias" : "No hay registros"
                      }}
                    </h3>
                    <p>
                      {{
                        searchQuery
                          ? `No encontramos resultados para "${searchQuery}"`
                          : "No hay registros de vagones en este momento"
                      }}
                    </p>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
  
      <!-- Paginación mejorada -->
      <div
        class="hv-pagination d-flex justify-content-between align-items-center"
      >
        <div class="hv-pagination-info">
          Mostrando {{ Math.min(currentPage * itemsPerPage, totalItems) }} de
          {{ totalItems }} registros
        </div>
        <nav aria-label="Navegación de páginas">
          <ul class="pagination pagination-sm mb-0">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <button class="page-link hv-pagination-btn" @click="previousPage">
                <i class="bi bi-chevron-left"></i>
              </button>
            </li>
            <li class="page-item disabled">
              <span class="page-link">
                Página {{ currentPage }} de
                {{ Math.ceil(totalItems / itemsPerPage) }}
              </span>
            </li>
            <li
              class="page-item"
              :class="{ disabled: currentPage * itemsPerPage >= totalItems }"
            >
              <button class="page-link hv-pagination-btn" @click="nextPage">
                <i class="bi bi-chevron-right"></i>
              </button>
            </li>
          </ul>
        </nav>
      </div>
  
      <!-- Modal de detalles - Versión mejorada con más color -->
      <div
        v-if="showDetailsModal"
        class="hv-modal-overlay"
        @click.self="closeModal"
      >
        <div class="hv-modal">
          <div class="hv-modal-header">
            <div class="hv-modal-header-content">
              <div class="hv-modal-icon-container">
                <i class="bi bi-info-circle-fill hv-modal-icon"></i>
              </div>
              <div>
                <h2>Detalles del Registro</h2>
                <p class="hv-modal-subtitle">
                  Información completa del historial del vagón
                </p>
              </div>
            </div>
            <button class="hv-modal-close" @click="closeModal">
              <i class="bi bi-x-lg"></i>
            </button>
          </div>
  
          <div class="hv-modal-body">
            <div class="hv-detail-grid">
                <!-- Información del Vagón -->
                <div class="hv-detail-card">
                <div class="hv-detail-card-header">
                    <i class="bi bi-train-freight-front"></i>
                    <h4>Información del Vagón</h4>
                </div>
                <div class="hv-detail-card-body">
                    <div class="hv-detail-item">
                    <span class="hv-detail-label">Número de Vagón:</span>
                    <span class="hv-detail-value">{{ currentRecord.vagon_no_id || "N/A" }}</span>
                    </div>
                    <div class="hv-detail-item">
                    <span class="hv-detail-label">Tipo de Vagón:</span>
                    <span class="hv-detail-value">{{ currentRecord.tipo_vagon || "N/A" }}</span>
                    </div>
                    <div class="hv-detail-item">
                    <span class="hv-detail-label">Capacidad:</span>
                    <span class="hv-detail-value">{{ currentRecord.capacidad || "N/A" }}</span>
                    </div>
                </div>
                </div>

                <!-- Operación -->
                <div class="hv-detail-card">
                <div class="hv-detail-card-header">
                    <i class="bi bi-clipboard2-data-fill"></i>
                    <h4>Operación</h4>
                </div>
                <div class="hv-detail-card-body">
                    <div class="hv-detail-item">
                    <span class="hv-detail-label">Estado:</span>
                    <span class="hv-detail-value">
                        <span :class="`hv-status hv-status-${getStatusClass(currentRecord.estado)}`">
                        {{ currentRecord.estado || "N/A" }}
                        </span>
                    </span>
                    </div>
                    <div class="hv-detail-item">
                    <span class="hv-detail-label">Operación:</span>
                    <span class="hv-detail-value">{{ currentRecord.operacion || "N/A" }}</span>
                    </div>
                    <div class="hv-detail-item">
                    <span class="hv-detail-label">Fecha Operación:</span>
                    <span class="hv-detail-value">{{ formatDateTime(currentRecord.fecha_operacion) || "N/A" }}</span>
                    </div>
                </div>
                </div>

                <!-- Carga/Descarga -->
                <div class="hv-detail-card hv-detail-card-highlight">
                <div class="hv-detail-card-header">
                    <i class="bi bi-box-seam-fill"></i>
                    <h4>Carga/Descarga</h4>
                </div>
                <div class="hv-detail-card-body">
                    <div class="hv-detail-item">
                    <span class="hv-detail-label">Producto:</span>
                    <span class="hv-detail-value">{{ currentRecord.producto_nombre || "N/A" }}</span>
                    </div>
                    <div class="hv-detail-item">
                    <span class="hv-detail-label">Cantidad:</span>
                    <span class="hv-detail-value hv-highlight-value hv-badge-primary">
                        {{ currentRecord.cantidad || "0" }}
                    </span>
                    </div>
                    <div class="hv-detail-item">
                    <span class="hv-detail-label">Unidad de Medida:</span>
                    <span class="hv-detail-value">{{ currentRecord.unidad_medida || "N/A" }}</span>
                    </div>
                </div>
                </div>

                <!-- Ubicación -->
                <div class="hv-detail-card">
                <div class="hv-detail-card-header">
                    <i class="bi bi-geo-alt-fill"></i>
                    <h4>Ubicación</h4>
                </div>
                <div class="hv-detail-card-body">
                    <div class="hv-detail-item">
                    <span class="hv-detail-label">Origen:</span>
                    <span class="hv-detail-value">{{ currentRecord.origen || "N/A" }}</span>
                    </div>
                    <div class="hv-detail-item">
                    <span class="hv-detail-label">Destino:</span>
                    <span class="hv-detail-value">{{ currentRecord.destino || "N/A" }}</span>
                    </div>
                    <div class="hv-detail-item">
                    <span class="hv-detail-label">Origen:</span>
                    <span class="hv-detail-value">{{ currentRecord.origen || "N/A" }}</span>
                    </div>
                </div>
                </div>

                <!-- Registros de Vagones -->
                <div class="hv-detail-card hv-detail-card-full" v-if="currentRecord.registros_vagones && currentRecord.registros_vagones.length">
                <div class="hv-detail-card-header">
                    <i class="bi bi-list-check"></i>
                    <h4>Registros de Vagones</h4>
                </div>
                <div class="hv-detail-card-body">
                    <div class="hv-registros-container">
                    <div class="hv-registro-item" v-for="(registro, index) in currentRecord.registros_vagones" :key="index">
                        <div class="hv-registro-header">
                        <span class="hv-registro-id">#{{ registro.no_id || registro.id }}</span>
                        <span class="hv-registro-fechas">
                            Despacho: {{ registro.fecha_despacho || "N/A" }} | 
                            Llegada: {{ registro.fecha_llegada || "N/A" }}
                        </span>
                        </div>
                        <div class="hv-registro-details">
                        <span class="hv-registro-origen">{{ registro.origen || "N/A" }}</span>
                        <span class="hv-registro-observaciones">{{ registro.observaciones || "Sin observaciones" }}</span>
                        </div>
                    </div>
                    </div>
                </div>
                </div>

                <!-- Observaciones -->
                <div class="hv-detail-card hv-detail-card-full">
                <div class="hv-detail-card-header">
                    <i class="bi bi-chat-square-text-fill"></i>
                    <h4>Observaciones</h4>
                </div>
                <div class="hv-detail-card-body">
                    <div class="hv-detail-item">
                    <span class="hv-detail-value">{{ currentRecord.observaciones || "Ninguna observación registrada" }}</span>
                    </div>
                </div>
                </div>
            </div>
            </div>
  
          <div class="hv-modal-footer">
            <button
              class="hv-modal-btn hv-modal-btn-secondary"
              @click="closeModal"
            >
              <i class="bi bi-x-circle"></i> Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Swal from "sweetalert2";
  import axios from "axios";
  
  export default {
    data() {
      return {
        allRecords: [],
        searchQuery: "",
        historialVagones: [],
        loading: false,
        showDetailsModal: false,
        errorLoading: false,
        currentRecord: {},
        debounceTimeout: null,
        currentPage: 1,
        itemsPerPage: 10,
        totalItems: 0,
      };
    },
  
    computed: {
      filteredRecords() {
        if (!this.searchQuery) return this.historialVagones;
        const query = this.searchQuery.toLowerCase();
        return this.historialVagones.filter((item) => {
          const fieldsToSearch = [
            item.vagon_no_id,
            item.origen,
            item.estado,
            item.operacion,
            item.producto_nombre,
            item.cantidad?.toString(),
            item.ubicacion,
            item.observaciones,
            item.plan_diario_carga_descarga,
            item.real_carga_descarga
          ];
  
          return fieldsToSearch.some(
            (field) => field && field.toString().toLowerCase().includes(query)
          );
        });
      },
    },
  
    mounted() {
      this.getHistorialVagones();
    },
  
    methods: {
        /*Retorna los registros de historial de vagones cargados */
        async getHistorialVagones() {
            this.loading = true;
            try {
                const response = await axios.get("/ufc/historial-vagones-cargados/", {
                params: {
                    page: this.currentPage,
                    page_size: this.itemsPerPage,
                    informe_id: this.informeId
                }
                });
                
                this.totalItems = response.data.count || response.data.length;

                if (response.data && Array.isArray(response.data.results || response.data)) {
                const data = response.data.results || response.data;
                this.allRecords = data.map((item) => {
                    // Parsear los datos JSON si es necesario
                    const datosVagon = typeof item.datos_vagon === 'string' ? 
                    JSON.parse(item.datos_vagon) : item.datos_vagon;
                    const datosRegistros = typeof item.datos_registros_vagones === 'string' ? 
                    JSON.parse(item.datos_registros_vagones) : item.datos_registros_vagones;
                    const datosProducto = typeof item.datos_productos === 'string' ? 
                    JSON.parse(item.datos_productos) : item.datos_productos;
                    console.log("manininiiiii> ", datosProducto);
                    
                    
                    // Obtener el primer registro de vagon
                    const primerRegistro = datosRegistros.length > 0 ? datosRegistros[0] : {};
                    
                    return {
                    id: item.id,
                    vagon_no_id: primerRegistro.no_id || "N/A",
                    tipo_vagon: datosVagon.tipo_equipo_ferroviario_name || "N/A",
                    estado: datosVagon.estado_name || datosVagon.estado || "N/A",
                    operacion: datosVagon.operacion_name || datosVagon.operacion || "N/A",
                    producto_nombre: datosProducto.cantidad || "N/A",
                    cantidad: datosRegistros.length || 0,
                    fecha_operacion: item.fecha_creacion,
                    ubicacion: datosVagon.origen || datosVagon.destino || "N/A",
                    origen: datosVagon.origen || "N/A",
                    observaciones: datosVagon.causas_incumplimiento || "",
                    capacidad: datosVagon.capacidad || "N/A",
                    unidad_medida: datosVagon.unidad_medida || "N/A",
                    plan_diario_carga_descarga:datosVagon.plan_diario_carga_descarga || '-',
                    real_carga_descarga:datosVagon.real_carga_descarga || '-'
                    };
                });

                this.historialVagones = [...this.allRecords];
                }
            } catch (error) {
                this.handleApiError(error, "cargar historial de vagones");
                this.historialVagones = [];
            } finally {
                this.loading = false;
            }
            },
  
      getStatusClass(status) {
        if (!status) return "default";
        const statusLower = status.toLowerCase();
  
        if (statusLower.includes("cargado")) return "success";
        if (statusLower.includes("descargado")) return "info";
        if (statusLower.includes("pendiente")) return "warning";
        if (statusLower.includes("vacio") || statusLower.includes("inactivo"))
          return "danger";
  
        return "primary";
      },
  
      async viewDetails(item) {
        try {
            this.loading = true;
            
            // Obtener los detalles completos del historial
            const response = await axios.get(`/ufc/historial-vagones-cargados/${item.id}/`);
            const historialData = response.data;
            
            // Parsear los datos JSON si son strings/*/*/*/*/*/*/*/*//*//////*/*/*/*/*/*/*/*/*/*/*/*/*/*/*//*//*/*/*/*/*/*/
            const datosVagon = typeof historialData.datos_vagon === 'string' ? 
            JSON.parse(historialData.datos_vagon) : historialData.datos_vagon;
            const datosRegistros = typeof historialData.datos_registros_vagones === 'string' ? 
            JSON.parse(historialData.datos_registros_vagones) : historialData.datos_registros_vagones;
            const datosProductos = typeof historialData.datos_productos === 'string' ? 
            JSON.parse(historialData.datos_productos) : historialData.datos_productos;
            
            // Extraer el primer registro de vagon (asumiendo que hay al menos uno)
            const primerRegistroVagon = datosRegistros.length > 0 ? datosRegistros[0] : {};
            const primerProducto = datosProductos.length > 0 ? datosProductos[0] : {};
            
            // Construir el objeto currentRecord con los datos mapeados
            this.currentRecord = {
            id: historialData.id,
            vagon_no_id: primerRegistroVagon.no_id || "N/A",
            tipo_vagon: datosVagon.tipo_equipo_ferroviario_name || 
                        (datosVagon.tipo_equipo_ferroviario && datosVagon.tipo_equipo_ferroviario.tipo_equipo) || 
                        "N/A",
            capacidad: datosVagon.capacidad || "N/A",
            estado: datosVagon.estado_name || datosVagon.estado || "N/A",
            operacion: datosVagon.operacion_name || datosVagon.operacion || "N/A",
            fecha_operacion: historialData.fecha_creacion || "N/A",
            producto_nombre: primerProducto.nombre_producto || "N/A",
            cantidad: datosRegistros.length || 0,
            unidad_medida: primerProducto.unidad_medida || "N/A",
            ubicacion: datosVagon.origen || datosVagon.destino || "N/A",
            origen: datosVagon.origen || "N/A",
            observaciones: datosVagon.observaciones || "Ninguna observación registrada",
            
            // Datos adicionales para mostrar en el modal
            tipo_origen: datosVagon.tipo_origen_name || datosVagon.tipo_origen || "N/A",
            tipo_destino: datosVagon.tipo_destino_name || datosVagon.tipo_destino || "N/A",
            origen: datosVagon.origen || "N/A",
            destino: datosVagon.destino || "N/A",
            registros_vagones: datosRegistros, // Todos los registros de vagones
            productos: datosProductos // Todos los productos
            };
            
            this.showDetailsModal = true;
        } catch (error) {
            console.error("Error al cargar detalles:", error);
            this.showErrorToast("No se pudieron cargar los detalles completos");
            
            // Mostrar al menos los datos básicos que ya teníamos
            this.currentRecord = { ...item };
            this.showDetailsModal = true;
        } finally {
            this.loading = false;
        }
        },
  
      formatDate(dateString) {
        if (!dateString) return "N/A";
        try {
          const date = new Date(dateString);
          return date.toLocaleDateString("es-ES", {
            year: "numeric",
            month: "short",
            day: "numeric"
          });
        } catch (e) {
          console.error("Error formateando fecha:", e);
          return dateString;
        }
      },
  
      formatDateTime(dateString) {
        if (!dateString) return "N/A";
        try {
          const date = new Date(dateString);
          const options = {
            year: "numeric",
            month: "long",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: true,
          };
          return date.toLocaleDateString("es-ES", options);
        } catch (e) {
          console.error("Error formateando fecha:", e);
          return dateString;
        }
      },
  
      closeModal() {
        this.showDetailsModal = false;
        this.currentRecord = {};
      },
  
      handleSearchInput() {
        clearTimeout(this.debounceTimeout);
        this.debounceTimeout = setTimeout(() => {
          if (!this.searchQuery.trim()) {
            this.historialVagones = [...this.allRecords];
            return;
          }
  
          const query = this.searchQuery.toLowerCase();
          this.historialVagones = this.allRecords.filter((item) => {
            const fieldsToSearch = [
              item.vagon_no_id,
              item.origen,
              item.estado,
              item.operacion,
              item.producto_nombre,
              item.cantidad?.toString(),
              item.ubicacion,
              item.observaciones,
            ];
  
            return fieldsToSearch.some(
              (field) => field && field.toString().toLowerCase().includes(query)
            );
          });
        }, 300);
      },
  
      async confirmDelete(id) {
        const result = await Swal.fire({
          title: "¿Eliminar registro?",
          text: "Esta acción no se puede deshacer",
          icon: "question",
          showCancelButton: true,
          confirmButtonColor: "#ff4444",
          cancelButtonColor: "#33b5e5",
          confirmButtonText: "Sí, eliminar",
          cancelButtonText: "Cancelar",
          customClass: {
            popup: "hv-swal-popup",
            confirmButton: "hv-swal-confirm",
            cancelButton: "hv-swal-cancel",
          },
        });
  
        if (result.isConfirmed) {
          try {
            this.loading = true;
            await axios.delete(`/ufc/historial-vagones-cargados/${id}/`);
            this.showSuccessToast("Registro eliminado");
            await this.getHistorialVagones();
          } catch (error) {
            this.handleApiError(error, "eliminar registro");
          } finally {
            this.loading = false;
          }
        }
      },
  
      previousPage() {
        if (this.currentPage > 1) {
          this.currentPage--;
          this.getHistorialVagones();
        }
      },
  
      nextPage() {
        if (this.currentPage * this.itemsPerPage < this.totalItems) {
          this.currentPage++;
          this.getHistorialVagones();
        }
      },
  
      showSuccessToast(message) {
        const Toast = Swal.mixin({
          toast: true,
          position: "top-end",
          showConfirmButton: false,
          timer: 3000,
          timerProgressBar: true,
          background: "#4BB543",
          color: "#fff",
          iconColor: "#fff",
          didOpen: (toast) => {
            toast.addEventListener("mouseenter", Swal.stopTimer);
            toast.addEventListener("mouseleave", Swal.resumeTimer);
          },
        });
  
        Toast.fire({
          icon: "success",
          title: message,
        });
      },
  
      showErrorToast(message) {
        const Toast = Swal.mixin({
          toast: true,
          position: "top-end",
          showConfirmButton: false,
          timer: 4000,
          timerProgressBar: true,
          background: "#ff4444",
          color: "#fff",
          iconColor: "#fff",
          didOpen: (toast) => {
            toast.addEventListener("mouseenter", Swal.stopTimer);
            toast.addEventListener("mouseleave", Swal.resumeTimer);
          },
        });
  
        Toast.fire({
          icon: "error",
          title: message,
        });
      },
  
      handleApiError(error, action) {
        let errorMsg = `Error al ${action}`;
        if (error.response) {
          errorMsg += ` (${error.response.status})`;
          if (error.response.data) {
            errorMsg += `: ${JSON.stringify(error.response.data)}`;
          }
        } else {
          errorMsg += `: ${error.message}`;
        }
        console.error(errorMsg, error);
        this.showErrorToast(errorMsg);
      },
    },
  };
  </script>
  
  <style scoped>
  /* Variables de color */
  :root {
    --hv-primary: #4361ee;
    --hv-primary-hover: #3a56d4;
    --hv-secondary: #3f37c9;
    --hv-accent: #4895ef;
    --hv-danger: #f72585;
    --hv-success: #4cc9f0;
    --hv-warning: #f8961e;
    --hv-info: #4895ef;
    --hv-light: #f8f9fa;
    --hv-dark: #212529;
    --hv-gray: #6c757d;
    --hv-light-gray: #e9ecef;
    --hv-border-radius: 12px;
    --hv-box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
    --hv-transition: all 0.3s ease;
  }
  
  /* Estilos base */
  .historial-vagones-container {
    padding: 2rem;
    max-width: 1400px;
    margin: 0 auto;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  }
  
  /* Header */
  .hv-header {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    gap: 1.5rem;
  }
  
  .hv-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--hv-dark);
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  
  .hv-title-icon {
    color: var(--hv-primary);
  }
  
  .hv-actions {
    display: flex;
    align-items: center;
    gap: 1.5rem;
  }
  
  /* Buscador */
  .hv-search-container {
    position: relative;
    width: 280px;
  }
  
  .hv-search-icon {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--hv-gray);
    font-size: 1rem;
  }
  
  .hv-search-input {
    width: 100%;
    padding: 0.6rem 1rem 0.6rem 2.5rem;
    border: 1px solid var(--hv-light-gray);
    border-radius: var(--hv-border-radius);
    font-size: 0.95rem;
    transition: var(--hv-transition);
    background-color: white;
  }
  
  .hv-search-input:focus {
    outline: none;
    border-color: var(--hv-primary);
    box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.15);
  }
  
  .hv-search-border {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background: var(--hv-primary);
    transition: var(--hv-transition);
  }
  
  .hv-search-input:focus ~ .hv-search-border {
    width: 100%;
  }
  
  /* Tarjeta contenedora */
  .hv-card {
    background: white;
    border-radius: var(--hv-border-radius);
    box-shadow: var(--hv-box-shadow);
    overflow: hidden;
    transition: var(--hv-transition);
  }
  
  .hv-card:hover {
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.12);
  }
  
  /* Tabla */
  .hv-table-container {
    overflow-x: auto;
    padding: 0.5rem;
  }
  
  .hv-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    min-width: 1000px;
  }
  
  .hv-th {
    padding: 1rem 1.2rem;
    text-align: left;
    font-weight: 600;
    color: var(--hv-dark);
    background-color: #f9fafb;
    border-bottom: 2px solid var(--hv-light-gray);
    position: sticky;
    top: 0;
  }
  
  .hv-th-actions {
    text-align: center;
  }
  
  .hv-tr {
    transition: var(--hv-transition);
  }
  
  .hv-tr:hover {
    background-color: rgba(67, 97, 238, 0.03);
  }
  
  .hv-td {
    padding: 1rem 1.2rem;
    border-bottom: 1px solid var(--hv-light-gray);
    color: var(--hv-dark);
  }
  
  .hv-td-actions {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
  }
  
  /* Badges y estados */
  .hv-badge {
    display: inline-block;
    padding: 0.25rem 0.6rem;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.8rem;
  }
  
  .hv-badge-primary {
    background: rgba(67, 97, 238, 0.1);
    color: var(--hv-primary);
    border: 1px solid rgba(67, 97, 238, 0.2);
  }
  
  .hv-status {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 500;
  }
  
  .hv-status-success {
    background: rgba(76, 201, 240, 0.1);
    color: #06d6a0;
    border: 1px solid rgba(6, 214, 160, 0.2);
  }
  
  .hv-status-warning {
    background: rgba(248, 150, 30, 0.1);
    color: #f8961e;
    border: 1px solid rgba(248, 150, 30, 0.2);
  }
  
  .hv-status-danger {
    background: rgba(247, 37, 133, 0.1);
    color: #ff7403;
    border: 1px solid rgba(247, 37, 133, 0.2);
  }
  
  .hv-status-info {
    background: rgba(72, 149, 239, 0.1);
    color: #4895ef;
    border: 1px solid rgba(72, 149, 239, 0.2);
  }
  
  .hv-status-primary {
    background: rgba(67, 97, 238, 0.1);
    color: var(--hv-primary);
    border: 1px solid rgba(67, 97, 238, 0.2);
  }
  
  .hv-status-default {
    background: rgba(108, 117, 125, 0.1);
    color: var(--hv-gray);
    border: 1px solid rgba(108, 117, 125, 0.2);
  }
  
  /* Estados de carga y vacío */
  .hv-loading-td,
  .hv-empty-td {
    padding: 3rem !important;
  }
  
  .hv-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    color: var(--hv-gray);
  }
  
  .hv-spinner {
    width: 3rem;
    height: 3rem;
    border: 4px solid rgba(67, 97, 238, 0.1);
    border-top-color: var(--hv-primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  .hv-empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 0.75rem;
    color: var(--hv-gray);
  }
  
  .hv-empty-state i {
    font-size: 2.5rem;
    color: var(--hv-accent);
  }
  
  .hv-empty-state h3 {
    color: var(--hv-dark);
    margin: 0;
    font-size: 1.2rem;
  }
  
  .hv-empty-state p {
    margin: 0;
    max-width: 400px;
  }
  
  /* Modal mejorado */
  .hv-modal-overlay {
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
  
  .hv-modal {
    background: white;
    border-radius: var(--hv-border-radius);
    width: 90%;
    max-width: 800px;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
    animation: slideUp 0.4s cubic-bezier(0.22, 1, 0.36, 1);
    overflow: hidden;
    border: 1px solid rgba(0, 0, 0, 0.1);
  }
  
  .hv-modal-header {
    padding: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(135deg, var(--hv-primary), var(--hv-secondary));
    color: white;
    position: relative;
  }
  
  .hv-modal-header::after {
    content: "";
    position: absolute;
    bottom: -10px;
    left: 0;
    width: 100%;
    height: 20px;
    background: linear-gradient(to bottom, rgba(67, 97, 238, 0.2), transparent);
  }
  
  .hv-modal-header-content {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .hv-modal-icon-container {
    background: rgba(255, 255, 255, 0.2);
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .hv-modal-icon {
    font-size: 1.5rem;
  }
  
  .hv-modal h2 {
    margin: 0;
    font-size: 1.4rem;
  }
  
  .hv-modal-subtitle {
    margin: 0.25rem 0 0;
    font-size: 0.9rem;
    opacity: 0.9;
    font-weight: 400;
  }
  
  .hv-modal-close {
    background: rgba(255, 255, 255, 0.2);
    border: none;
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 50%;
    transition: var(--hv-transition);
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
  }
  
  .hv-modal-close:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: rotate(90deg);
  }
  
  .hv-modal-body {
    padding: 1.5rem;
    overflow-y: auto;
    background: #f9fafb;
  }
  
  .hv-detail-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
  }
  
  .hv-detail-card {
    background: white;
    border-radius: var(--hv-border-radius);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    overflow: hidden;
    transition: var(--hv-transition);
    border: 1px solid var(--hv-light-gray);
  }
  
  .hv-detail-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  }
  
  .hv-detail-card-header {
    padding: 1rem;
    background: linear-gradient(to right, #f8f9fa, white);
    border-bottom: 1px solid var(--hv-light-gray);
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  
  .hv-detail-card-header i {
    font-size: 1.2rem;
    color: var(--hv-primary);
  }
  
  .hv-detail-card-header h4 {
    margin: 0;
    font-size: 1rem;
    color: var(--hv-dark);
  }
  
  .hv-detail-card-body {
    padding: 1rem;
  }
  
  .hv-detail-card-highlight {
    border: 1px solid rgba(67, 97, 238, 0.3);
  }
  
  .hv-detail-card-highlight .hv-detail-card-header {
    background: linear-gradient(to right, rgba(67, 97, 238, 0.05), white);
  }
  
  .hv-detail-card-highlight .hv-detail-card-header i {
    color: var(--hv-accent);
  }
  
  .hv-detail-card-full {
    grid-column: 1 / -1;
  }
  
  .hv-detail-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    margin-bottom: 0.75rem;
  }
  
  .hv-detail-item:last-child {
    margin-bottom: 0;
  }
  
  .hv-detail-label {
    font-size: 0.85rem;
    color: var(--hv-gray);
    font-weight: 500;
  }
  
  .hv-detail-value {
    font-size: 1rem;
    color: var(--hv-dark);
    font-weight: 500;
    word-break: break-word;
  }
  
  .hv-highlight-value {
    color: var(--hv-primary);
    font-weight: 600;
    font-size: 1.1rem;
  }
  
  .hv-modal-footer {
    padding: 1.25rem 1.5rem;
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    background: white;
    border-top: 1px solid var(--hv-light-gray);
  }
  
  .hv-modal-btn {
    padding: 0.6rem 1.2rem;
    border-radius: var(--hv-border-radius);
    font-weight: 500;
    cursor: pointer;
    transition: var(--hv-transition);
    border: none;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .hv-modal-btn-secondary {
    background: white;
    color: var(--hv-gray);
    border: 1px solid var(--hv-light-gray);
  }
  
  .hv-modal-btn-secondary:hover {
    background: #f1f3f5;
    color: var(--hv-dark);
  }
  
  .hv-modal-btn-primary {
    background: var(--hv-primary);
    color: white;
    box-shadow: 0 2px 6px rgba(67, 97, 238, 0.2);
  }
  
  .hv-modal-btn-primary:hover {
    background: var(--hv-primary-hover);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3);
  }
  
  /* Animaciones */
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }
  
  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  /* Responsive */
  @media (max-width: 992px) {
    .hv-header {
      flex-direction: column;
      align-items: flex-start;
    }
  
    .hv-actions {
      width: 100%;
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
  
    .hv-search-container {
      width: 100%;
    }
  
    .hv-detail-grid {
      grid-template-columns: 1fr;
    }
  }
  
  @media (max-width: 768px) {
    .historial-vagones-container {
      padding: 1.5rem 1rem;
    }
  
    .hv-title {
      font-size: 1.5rem;
    }
  
    .hv-modal {
      width: 95%;
    }
  
    .hv-modal-body {
      padding: 1.25rem 1rem;
    }
  
    .hv-modal-footer {
      padding: 1rem;
      flex-direction: column;
    }
  
    .hv-modal-btn {
      width: 100%;
      justify-content: center;
    }
  }
  
  /* Estilos para los botones */
  .btn-outline-info {
    color: #0dcaf0;
    border-color: #0dcaf0;
  }
  
  .btn-outline-danger {
    color: #dc3545;
    border-color: #dc3545;
  }
  
  .btn-sm {
    padding: 0.25rem 0.5rem;
    font-size: 0.875rem;
    border-radius: 0.2rem;
  }
  
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
  }
  
  .btn:hover {
    transform: translateY(-1px);
    opacity: 0.9;
  }
  
  .btn i {
    font-size: 1rem;
  }
  
  .me-2 {
    margin-right: 0.5rem !important;
  }
  
  .hv-td-actions {
    white-space: nowrap;
  }

  /* Estilos para los registros de vagones en el modal */
.hv-registros-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.hv-registro-item {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 0.75rem;
  border-left: 3px solid var(--hv-primary);
}

.hv-registro-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.hv-registro-id {
  font-weight: 600;
  color: var(--hv-primary);
}

.hv-registro-fechas {
  color: var(--hv-gray);
  font-size: 0.85rem;
}

.hv-registro-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.hv-registro-origen {
  font-weight: 500;
}

.hv-registro-observaciones {
  font-size: 0.85rem;
  color: var(--hv-gray);
}
  </style>