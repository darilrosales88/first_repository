<template>
  <div class="container py-3">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h6 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-inboxes-fill me-2"></i>Registros de hechos extraordinarios
        </h6>
      </div>
      <div class="card-body p-3">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <router-link 
            v-if="hasGroup('AdminGEMAR')" 
            to="/gemar_hecho_extraordinario/add"
            custom
            v-slot="{ navigate }"
          >
            <button 
              class="btn btn-sm btn-primary"
              @click="navigate"
              :disabled="ActivarDesactivarBotonAgregar"
            >
              <i class="bi bi-plus-circle me-1"></i>Agregar nuevo HE
            </button>
            
          </router-link>
          <form @submit.prevent="searchHechos" class="search-container">
            <div class="input-group">
              <input
                type="search"
                class="form-control"
                placeholder="Buscar por informado o garante"
                v-model="searchQuery"
                @input="handleSearchInput"/>
              <span
                class="position-absolute top-50 start-0 translate-middle-y ps-2">
                <i class="bi bi-search"></i>
              </span>
            </div>
          </form>
        </div>
        <!-- Tabla responsive con mejoras -->
        <div class="table table-responsive">
          <table class="table table-sm table-bordered table-hover">
            <thead class="table-light">
              <tr>
                <th scope="col" style="width: 50px">No</th>
                <th scope="col">Fecha Operación</th>
                <th scope="col">Informado</th>
                <th scope="col">Garante</th>
                <th scope="col">Producto</th>
                <th scope="col">Tipo Diferencia</th>
                <th scope="col">Incidencia</th>
                <th scope="col">Acciones</th>
              </tr>
              <tr v-if="!busqueda_existente && hechosExtraordinarios.length != 0">
                <td colspan="8" class="text-center text-muted py-4">
                  <i class="bi bi-exclamation-circle fs-4"></i>
                  <p class="mt-2">
                    No se encontraron resultados para "{{ searchQuery }}"
                  </p>
                </td>
              </tr>
              <tr v-if="hechosExtraordinarios.length == 0">
                <td colspan="8" class="text-center text-muted py-4">
                  <div class="ps-loading" v-if="loading">
                    <div class="ps-spinner"></div>
                    <span>Cargando registros...</span>
                  </div>
                  <div v-else>
                    <i class="bi bi-database-exclamation fs-4"></i>
                    <p class="mt-2">No hay registros de hechos extraordinarios</p>
                  </div>
                </td>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in hechosExtraordinarios" :key="item.id" class="align-middle">
                <th scope="row">{{ index + 1 }}</th>
                <td>{{ formatDate(item.fecha_operacion) }}</td>
                <td>{{ item.informado }}</td>
                <td>{{ item.garante_name || 'N/A' }}</td>
                <td>{{ item.producto_name || 'N/A' }}</td>
                <td class="ps-td">
                  <span :class="`ps-status ps-status-${getStatusClass(item.tipo_diferencia)}`">
                    {{ item.tipo_diferencia || 'N/A' }}
                  </span>
                </td>
                <td>{{ item.incidencia_name || 'N/A' }}</td>
                <td>
                  <div class="d-flex">
                    <button 
                      @click="viewDetails(item)"
                      class="btn btn-sm btn-outline-info me-2"
                      title="Ver detalles">
                      <i class="bi bi-eye-fill"></i>
                    </button>

                    <button v-if="hasGroup('AdminGEMAR')"
                      :disabled="estadoParte === 'Aprobado'"
                      :title="estadoParte === 'Aprobado' ? 'No se puede  HE a un parte aprobado' : ''"
                      @click="editHecho(item)"
                      class="btn btn-sm btn-outline-warning me-2"
                      title="Editar">
                      <i class="bi bi-pencil-square"></i>
                    </button>

                    <button v-if="hasGroup('AdminGEMAR')"
                      @click="confirmDelete(item.id)"
                      class="btn btn-sm btn-outline-danger"
                      title="Eliminar">
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Paginación mejorada -->
        <div class="d-flex justify-content-between align-items-center">
          <div class="text-muted small">
            Mostrando {{ hechosExtraordinarios.length }} de
            {{ totalItems }} registros
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
                  Página {{ currentPage }} de
                  {{ Math.ceil(totalItems / itemsPerPage) }}
                </span>
              </li>
              <li
                class="page-item"
                :class="{ disabled: currentPage * itemsPerPage >= totalItems }"
              >
                <button class="page-link" @click="nextPage">
                  <i class="bi bi-chevron-right"></i>
                </button>
              </li>
            </ul>
          </nav>
        </div>

        <!-- Modal de Detalles -->
        <div
          v-if="showDetailsModal"
          class="ps-modal-overlay"
          @click.self="closeModal"
        >
          <!-- Contenedor principal del modal -->
          <div class="ps-modal">
            <!-- Encabezado del modal -->
            <div class="ps-modal-header">
              <div class="ps-modal-header-content">
                <div class="ps-modal-icon-container">
                  <i class="bi bi-info-circle-fill ps-modal-icon"></i>
                </div>
                <div>
                  <h2>Detalles del Hecho Extraordinario</h2>
                  <p class="ps-modal-subtitle">
                    Información completa del registro seleccionado
                  </p>
                </div>
              </div>
              <button class="ps-modal-close" @click="closeModal">
                <i class="bi bi-x-lg"></i>
              </button>
            </div>

            <!-- Cuerpo del modal -->
            <div class="ps-modal-body">
              <!-- Grid de tarjetas de detalles -->
              <div class="ps-detail-grid">
                <!-- Tarjeta 1: Información Básica -->
                <div class="ps-detail-card">
                  <div class="ps-detail-card-header">
                    <i class="bi bi-tag-fill"></i>
                    <h4>Información Básica</h4>
                  </div>
                  <div class="ps-detail-card-body">
                    <!-- Fecha Operación -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Fecha Operación:</span>
                      <span class="ps-detail-value">
                        {{ formatDate(currentRecord.fecha_operacion) || "N/A" }}
                      </span>
                    </div>

                    <!-- Informado -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Informado:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.informado || "N/A" }}
                      </span>
                    </div>

                    <!-- Garante -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Garante:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.garante_name || "N/A" }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Tarjeta 2: Involucrados -->
                <div class="ps-detail-card">
                  <div class="ps-detail-card-header">
                    <i class="bi bi-people-fill"></i>
                    <h4>Involucrados</h4>
                  </div>
                  <div class="ps-detail-card-body">
                    <!-- Tipo Involucrado -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Tipo Involucrado:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.tipo_involucrado || "N/A" }}
                      </span>
                    </div>

                    <!-- Involucrado -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Involucrado:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.involucrado || "N/A" }}
                      </span>
                    </div>

                    <!-- Tipo Origen -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Tipo Origen:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.tipo_origen || "N/A" }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Tarjeta 3: Ubicaciones -->
                <div class="ps-detail-card">
                  <div class="ps-detail-card-header">
                    <i class="bi bi-geo-alt-fill"></i>
                    <h4>Ubicaciones</h4>
                  </div>
                  <div class="ps-detail-card-body">
                    <!-- Origen -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Origen:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.origen || "N/A" }}
                      </span>
                    </div>

                    <!-- Destino -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Destino:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.destino || "N/A" }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Tarjeta 4: Producto -->
                <div class="ps-detail-card">
                  <div class="ps-detail-card-header">
                    <i class="bi bi-box-seam-fill"></i>
                    <h4>Producto</h4>
                  </div>
                  <div class="ps-detail-card-body">
                    <!-- Producto Involucrado -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Producto:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.producto_name || "N/A" }}
                      </span>
                    </div>

                    <!-- Embalaje -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Embalaje:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.embalaje_name || "N/A" }}
                      </span>
                    </div>

                    <!-- Unidad Medida -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Unidad Medida:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.unidad_medida_name || "N/A" }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Tarjeta 5: Diferencias -->
                <div class="ps-detail-card ps-detail-card-highlight">
                  <div class="ps-detail-card-header">
                    <i class="bi bi-exclamation-triangle-fill"></i>
                    <h4>Diferencias</h4>
                  </div>
                  <div class="ps-detail-card-body">
                    <!-- Tipo Diferencia -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Tipo Diferencia:</span>
                      <span class="ps-detail-value ps-highlight-value">
                        {{ currentRecord.tipo_diferencia || "N/A" }}
                      </span>
                    </div>

                    <!-- Cantidad Diferencia -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Cantidad:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.cantidad_diferencia || "0" }}
                      </span>
                    </div>

                    <!-- KG Diferencia -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">KG Diferencia:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.kg_diferencia || "0" }}
                      </span>
                    </div>

                    <!-- Valor Diferencia -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Valor Diferencia:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.valor_diferencia || "0" }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Tarjeta 6: Averías -->
                <div class="ps-detail-card">
                  <div class="ps-detail-card-header">
                    <i class="bi bi-tools"></i>
                    <h4>Averías</h4>
                  </div>
                  <div class="ps-detail-card-body">
                    <!-- Avería -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Avería:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.averia === 'si' ? 'Sí' : 'No' }}
                      </span>
                    </div>

                    <!-- Cantidad Avería -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Cantidad Avería:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.cantidad_averia || "0" }}
                      </span>
                    </div>

                    <!-- KG Avería -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">KG Avería:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.kg_averia || "0" }}
                      </span>
                    </div>

                    <!-- Valor Avería -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Valor Avería:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.valor_averia || "0" }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Tarjeta 7: Incidencia y Descripción -->
                <div class="ps-detail-card ps-detail-card-full">
                  <div class="ps-detail-card-header">
                    <i class="bi bi-chat-square-text-fill"></i>
                    <h4>Incidencia y Descripción</h4>
                  </div>
                  <div class="ps-detail-card-body">
                    <!-- Incidencia -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Incidencia:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.incidencia_involucrada_name || "N/A" }}
                      </span>
                    </div>

                    <!-- Descripción -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Descripción:</span>
                      <span class="ps-detail-value">
                        {{ currentRecord.descripcion_hecho || "Ninguna descripción registrada" }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Tarjeta 8: Meta Información -->
                <div class="ps-detail-card">
                  <div class="ps-detail-card-header">
                    <i class="bi bi-calendar-event-fill"></i>
                    <h4>Meta Información</h4>
                  </div>
                  <div class="ps-detail-card-body">
                    <!-- Fecha Creación -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Fecha Registro:</span>
                      <span class="ps-detail-value">
                        {{ formatDate(currentRecord.fecha_actual) || "N/A" }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Pie del modal -->
            <div class="ps-modal-footer">
              <button
                class="ps-modal-btn ps-modal-btn-secondary"
                @click="closeModal"
              >
                <i class="bi bi-x-circle"></i> Cerrar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "HechosExtraordinariosList",
  props: {
        estadoParte: {
          type: String,
          default: '',
          required: true
        }
      },
  data() {
    return {      
      hechosExtraordinarios: [],
      allRecords: [], // Copia completa de todos los registros para filtrado local
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 0,
      searchQuery: "",
      debounceTimeout: null,
      busqueda_existente: true,
      userPermissions: [],
      userGroups: [],
      loading: false,
      showDetailsModal: false,
      currentRecord: {},
      existe_parte_mio:""
      };
  },
  // 3. Agregar un watcher para el estado
    watch: {
      estadoParte(newVal) {
        console.log('Estado del parte actualizado:', newVal);
        // Puedes forzar una actualización aquí si es necesario
        this.fetchHechosExtraordinarios();
      }
    },

  async mounted() {
    await this.ExisteParteMio();
    await this.fetchHechosExtraordinarios();
    await this.fetchUserPermissionsAndGroups();
  },

  computed: {
      ActivarDesactivarBotonAgregar() {
        return this.estadoParte === 'Aprobado' || this.loading || !this.existe_parte_mio;
      },
      
    },

  methods: {
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      const date = new Date(dateString);
      return date.toLocaleString();
    },

    getStatusClass(status) {
      if (!status) return "default";
      const statusLower = status.toLowerCase();

      if (statusLower.includes("sobrante")) return "success";
      if (statusLower.includes("faltante")) return "danger";

      return "info";
    },

    hasGroup(group) {
      return this.userGroups.some((g) => g.name === group);
    },

    closeModal() {
      this.showDetailsModal = false;
      this.currentRecord = {};
    },

    async viewDetails(item) {
      this.loading = true;
      try {
        // Hacer una solicitud para obtener detalles completos si es necesario
        const response = await axios.get(`/gemar/gemar-hechos-extraordinarios/${item.id}/`);
        this.currentRecord = response.data;
        this.showDetailsModal = true;
      } catch (error) {
        console.error("Error al cargar detalles:", error);
        this.showErrorToast("No se pudieron cargar los detalles completos");
      } finally {
        this.loading = false;
      }
    },

    async fetchUserPermissionsAndGroups() {
      try {
        const userId = localStorage.getItem("userid");
        if (userId) {
          const response = await axios.get(
            `/apiAdmin/user/${userId}/permissions-and-groups/`
          );
          this.userPermissions = response.data.permissions;
          this.userGroups = response.data.groups;
        }
      } catch (error) {
        console.error("Error al obtener permisos y grupos:", error);
      }
    },

    async ExisteParteMio() {
      this.loading = true;
      try {
        const fechaHoy = new Date().toISOString().split('T')[0];
        const response = await axios.get("/gemar/gemar-hechos-extraordinarios/mis_hechos_extraordinarios/", {
          params: {
            fecha_operacion: fechaHoy,
            page: this.currentPage,
            page_size: this.itemsPerPage,
            search: this.searchQuery
          },
        });     
        this.existe_parte_mio = response.data.existe_parte;
      } catch (error) {
        console.error("Error al obtener datos:", error);
        this.showErrorToast("No existe aún el parte correspondiente a la fecha actual.");
      } finally {
        this.loading = false;
      }
    },
    
    async fetchHechosExtraordinarios() {
      this.loading = true;
      try {
        const fechaHoy = new Date().toISOString().split('T')[0];
        const response = await axios.get("/gemar/gemar-hechos-extraordinarios/mis_hechos_extraordinarios/", {
          params: {
            fecha_operacion: fechaHoy,
            page: this.currentPage,
            page_size: this.itemsPerPage,
            search: this.searchQuery
          },
        });
        if (response.data.existe_parte) {
          this.hechosExtraordinarios = response.data.hechos;
          this.allRecords = [...response.data.hechos];
          this.totalItems = response.data.hechos.length;
        } else {
          this.hechosExtraordinarios = [];
          this.allRecords = [];
          this.totalItems = 0;
        }
      } catch (error) {
        console.error("Error al obtener datos:", error);
        this.showErrorToast("No existe aún el parte correspondiente a la fecha actual.");
      } finally {
        this.loading = false;
      }
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        if (!this.searchQuery.trim()) {
          this.hechosExtraordinarios = [...this.allRecords];
          this.busqueda_existente = true;
          return;
        }

        const query = this.searchQuery.toLowerCase();
        this.hechosExtraordinarios = this.allRecords.filter((item) => {
          const informado = item.informado?.toLowerCase() || "";
          const garante = item.garante?.nombre_entidad?.toLowerCase() || "";
          const producto = item.producto_involucrado?.nombre_producto?.toLowerCase() || "";

          return (
            informado.includes(query) ||
            garante.includes(query) ||
            producto.includes(query)
          );
        });

        this.busqueda_existente = this.hechosExtraordinarios.length > 0;
      }, 300);
    },

    async searchHechos() {
      await this.fetchHechosExtraordinarios();
    },

    // Métodos de paginación
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.fetchHechosExtraordinarios();
      }
    },

    nextPage() {
      if (this.currentPage * this.itemsPerPage < this.totalItems) {
        this.currentPage++;
        this.fetchHechosExtraordinarios();
      }
    },

    goToPage(page) {
      this.currentPage = page;
      this.fetchHechosExtraordinarios();
    },

    editHecho(item) {
      this.$router.push({
        name: "editar_gemar_hecho_extraordinario",
        params: { id: item.id },
      });
    },

    async deleteHecho(id) {
      try {
        await axios.delete(`/gemar/gemar-hechos-extraordinarios/${id}/`);
        this.hechosExtraordinarios = this.hechosExtraordinarios.filter(
          (objeto) => objeto.id !== id
        );
        this.showSuccessToast("El registro ha sido eliminado correctamente");
      } catch (error) {
        console.error("Error al eliminar el hecho extraordinario:", error);
        this.showErrorToast("Hubo un error al eliminar el registro.");
      }
    },

    confirmDelete(id) {
      Swal.fire({
        title: "¿Estás seguro?",
        text: "¡No podrás revertir esta acción!",
        icon: "warning",
        showCancelButton: true,
        cancelButtonText: '<i class="bi bi-x-circle me-1"></i>Cancelar',
        cancelButtonColor: "#f1513f",
        confirmButtonText: '<i class="bi bi-trash me-1"></i>Eliminar',
        confirmButtonColor: "#007bff",
        reverseButtons: true,
      }).then((result) => {
        if (result.isConfirmed) {
          this.deleteHecho(id);
        }
      });
    },

    // Método para manejar errores
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
      Swal.fire("Error", errorMsg, "error");
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
  },
};
</script>

<style scoped>
/* Estilos generales */
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

/* Estilos para la tabla responsive */
.table-responsive {
  overflow-x: auto;
}

/* Estilos para el icono de agregar */
.btn-link {
  color: #007bff;
  text-decoration: none;
}

.btn-link:hover {
  color: #0056b3;
}

/* Estados de carga y vacío */
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
  border-radius: 10px;
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  animation: slideUp 0.4s cubic-bezier(0.22, 1, 0.36, 1);
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
  color: white;
}

.ps-modal h2 {
  margin: 0;
  font-size: 1.4rem;
  color: white;
}

.ps-modal-subtitle {
  margin: 0.25rem 0 0;
  font-size: 0.9rem;
  opacity: 0.9;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.8);
}

.ps-modal-close {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
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
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid #e9ecef;
}

.ps-detail-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.ps-detail-card-header {
  padding: 1rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.ps-detail-card-header i {
  font-size: 1.2rem;
  color: #0d6efd;
}

.ps-detail-card-header h4 {
  margin: 0;
  font-size: 1rem;
  color: #212529;
}

.ps-detail-card-body {
  padding: 1rem;
}

.ps-detail-card-highlight {
  border: 1px solid rgba(13, 110, 253, 0.3);
}

.ps-detail-card-highlight .ps-detail-card-header {
  background: linear-gradient(to right, rgba(13, 110, 253, 0.05), white);
}

.ps-detail-card-highlight .ps-detail-card-header i {
  color: #fd7e14;
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
  color: #6c757d;
  font-weight: 500;
}

.ps-detail-value {
  font-size: 1rem;
  color: #212529;
  font-weight: 500;
  word-break: break-word;
}

.ps-highlight-value {
  color: #0d6efd;
  font-weight: 600;
  font-size: 1.1rem;
}

.ps-modal-footer {
  padding: 1.25rem 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  background: white;
  border-top: 1px solid #e9ecef;
}

.ps-modal-btn {
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.ps-modal-btn-secondary {
  background: white;
  color: #6c757d;
  border: 1px solid #e9ecef;
}

.ps-modal-btn-secondary:hover {
  background: #f1f3f5;
  color: #212529;
}

.ps-status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
}

.ps-status-success {
  background: rgba(6, 214, 160, 0.1);
  color: #06d6a0;
  border: 1px solid rgba(6, 214, 160, 0.2);
}

.ps-status-danger {
  background: rgba(247, 37, 133, 0.1);
  color: #f72585;
  border: 1px solid rgba(247, 37, 133, 0.2);
}

.ps-status-info {
  background: rgba(13, 110, 253, 0.1);
  color: #0d6efd;
  border: 1px solid rgba(13, 110, 253, 0.2);
}

.ps-status-default {
  background: rgba(108, 117, 125, 0.1);
  color: #6c757d;
  border: 1px solid rgba(108, 117, 125, 0.2);
}

/* Animaciones */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .ps-detail-grid {
    grid-template-columns: 1fr;
  }
  
  .ps-modal {
    width: 95%;
  }
}
</style>