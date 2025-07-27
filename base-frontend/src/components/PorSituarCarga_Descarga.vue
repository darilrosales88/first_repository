<template>
  <div class="container py-3">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h6 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-inboxes-fill me-2"></i>Registros Por Situar
        </h6>
      </div>
      <div class="card-body p-3">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <router-link v-if="hasGroup('AdminUFC') && this.habilitado" to="/AdicionarPorSituar">
            <button class="btn btn-sm btn-primary">
              <i class="bi bi-plus-circle me-1"></i>Agregar nuevo registro por
              situar
            </button>
          </router-link>
          <form @submit.prevent="search_producto" class="search-container">
            <div class="input-group">
              <input
                type="search"
                class="form-control"
                placeholder="Buscar en registros"
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
                <th scope="col">Tipo Origen</th>
                <th scope="col">Origen</th>
                <th scope="col">Tipo Equipo</th>
                <th scope="col">Estado</th>
                <th scope="col">Operación</th>
                <th scope="col">Producto</th>
                <th scope="col">Por Situar</th>
                <th scope="col">Acciones</th>
              </tr>
              <tr v-if="!busqueda_existente && porSituarCarga_Descarga.length != 0">
                <td colspan="9" class="text-center text-muted py-4">
                  <i class="bi bi-exclamation-circle fs-4"></i>
                  <p class="mt-2">
                    No se encontraron resultados para "{{ searchQuery }}"
                  </p>
                </td>
              </tr>
              <tr v-if="porSituarCarga_Descarga.length == 0">
                <td colspan="10" class="text-center text-muted py-4">
                  <div class="ps-loading" v-if="loading">
                    <div class="ps-spinner"></div>
                    <span>Cargando registros...</span>
                  </div>
                  <div v-else>
                    <i class="bi bi-database-exclamation fs-4"></i>
                    <p class="mt-2">No hay registros</p>
                  </div>
                </td>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in porSituarCarga_Descarga" :key="item.id" class="align-middle">
                <th scope="row">{{ index + 1 }}</th>
                <td>{{ item.tipo_origen_name }}</td>
                <td>{{ item.origen }}</td>
                <td>{{ item.tipo_equipo_name }}</td>
                <td class="ps-td">
                  <span
                    :class="`ps-status ps-status-${getStatusClass(
                      item.estado
                    )}`">
                    {{ item.estado }}
                  </span>
                </td>
                <td>{{ item.operacion }}</td>
                <td class="ps-td">
                  <span v-if="item.producto">
                    {{ item.producto_detalle.producto_name
                    }}<!-- Aqui hay que actualizar tambien esto mismo en los demas estados @BZ-theFanG #-#-->
                  </span>
                  <span v-else>-</span>
                </td>
                <td>{{ item.por_situar }}</td>
                <td v-if="hasGroup('AdminUFC')">
                  <div class="d-flex">
                    <button 
                      @click="viewDetails(item)"
                      class="btn btn-sm btn-outline-info me-2"
                      title="Ver detalles">
                      <i class="bi bi-eye-fill"></i>
                    </button>

                    <button v-if="this.habilitado"
                      @click="editRegistroPorSituar(item)"
                      class="btn btn-sm btn-outline-warning me-2"
                      title="Editar">
                      <i class="bi bi-pencil-square"></i>
                    </button>

                    <button v-if="this.habilitado"
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
            Mostrando {{ porSituarCarga_Descarga.length }} de
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

          <!-- Modal Overlay - Fondo oscuro que se muestra cuando el modal está activo -->
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
                    <h2>Detalles del Registro</h2>
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
                      <!-- Item 1.1: Tipo Origen -->
                      <div class="ps-detail-item">
                        <span class="ps-detail-label">Tipo Origen:</span>
                        <span class="ps-detail-value">
                          {{
                            currentRecord.tipo_origen_name ||
                            currentRecord.tipo_origen ||
                            "N/A"
                          }}
                        </span>
                      </div>

                      <!-- Item 1.2: Origen -->
                      <div class="ps-detail-item">
                        <span class="ps-detail-label">Origen:</span>
                        <span class="ps-detail-value">
                          {{ currentRecord.origen || "N/A" }}
                        </span>
                      </div>

                      <!-- Item 1.3: Tipo de Equipo -->
                      <div class="ps-detail-item">
                        <span class="ps-detail-label">Tipo de Equipo:</span>
                        <span class="ps-detail-value">
                          {{ currentRecord.tipo_equipo_name || "N/A" }}
                        </span>
                      </div>
                    </div>
                  </div>

                  <!-- Tarjeta 2: Estado,Operación y Producto -->
                  <div class="ps-detail-card">
                    <div class="ps-detail-card-header">
                      <i class="bi bi-clipboard2-data-fill"></i>
                      <h4>Estado y Operación</h4>
                    </div>
                    <div class="ps-detail-card-body">
                      <!-- Item 2.1: Estado -->
                      <div class="ps-detail-item">
                        <span class="ps-detail-label">Estado:</span>
                        <span class="ps-detail-value">
                          <span :class="`ps-status ps-status-${getStatusClass(currentRecord.estado)}`">
                            {{ currentRecord.estado || "N/A" }}
                          </span>
                        </span>
                      </div>

                      <!-- Item 2.2: Operación -->
                      <div class="ps-detail-item">
                        <span class="ps-detail-label">Operación:</span>
                        <span class="ps-detail-value">
                          {{ currentRecord.operacion || "N/A" }}
                        </span>
                      </div>

                      <!-- Item 2.3: Producto -->
                      <div class="ps-detail-item">
                        <span class="ps-detail-label">Producto:</span>
                        <span class="ps-detail-value">
                          <span v-if="currentRecord.productos_info && currentRecord.productos_info.length > 0">
                            {{getNombresProductos(currentRecord.productos_info)}}
                          </span>
                          <span v-else>N/A</span>
                        </span>
                      </div>
                    </div>
                  </div>

                  <!-- Tarjeta 3: Cantidad (Destacada) -->
                  <div class="ps-detail-card">
                    <div class="ps-detail-card-header">
                      <i class="bi bi-exclamation-square-fill"></i>
                      <h4>Cantidad</h4>
                    </div>
                    <div class="ps-detail-card-body">
                      <!-- Item 3.1: Por Situar -->
                      <div class="ps-detail-item">
                        <span class="ps-detail-label">Por Situar:</span>
                        <span class="ps-detail-value ps-highlight-value">
                          {{ currentRecord.por_situar || "0" }}
                        </span>
                      </div>
                    </div>
                  </div>

                  <!-- Tarjeta 4: Observaciones (Ancho completo) -->
                  <div class="ps-detail-card ps-detail-card-full">
                    <div class="ps-detail-card-header">
                      <i class="bi bi-chat-square-text-fill"></i>
                      <h4>Observaciones</h4>
                    </div>
                    <div class="ps-detail-card-body">
                      <!-- Item 4.1: Observaciones -->
                      <div class="ps-detail-item">
                        <span class="ps-detail-value">
                          {{
                            currentRecord.observaciones ||
                            "Ninguna observación registrada"
                          }}
                        </span>
                      </div>
                    </div>
                  </div>

                  <!-- Tarjeta 5: Meta Información -->
                  <div class="ps-detail-card">
                    <div class="ps-detail-card-header">
                      <i class="bi bi-calendar-event-fill"></i>
                      <h4>Meta Información</h4>
                    </div>
                    <div class="ps-detail-card-body">
                      <!-- Item 5.1: Fecha Creación -->
                      <div class="ps-detail-item">
                        <span class="ps-detail-label">Fecha Creación:</span>
                        <span class="ps-detail-value">
                          {{ currentRecord.fecha_registro }}
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
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "PorSituarCargaDescarga",
  props: {
    informeID: {
      type: Number,
      required: false,
    },
  },
  data() {
    return {
      porSituarCarga_Descarga: [],
      allRecords: [], // Copia completa de todos los registros para filtrado local
      habilitado: true,
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 0,
      searchQuery: "",
      debounceTimeout: null,
      busqueda_existente: true,
      userPermissions: [],
      userGroups: [],
      loading: false,
      mostrarModalDetalles: false,
      currentRecord: {},
      registroPorSituarSeleccionado: null,
      showDetailsModal: false,
    };
  },

  async mounted() {
    await this.getPorSituar();
    console.log("Hola", this.porSituarCarga_Descarga);
    await this.fetchUserPermissionsAndGroups();
  },

  methods: {
    getStatusClass(status) {
      if (!status) return "default";
      const statusLower = status.toLowerCase();

      if (statusLower.includes("cargado")) return "success";
      if (statusLower.includes("vacio"))return "danger";

      return "info";
    },
    getNombresProductos(productos) {
      if (!productos || !Array.isArray(productos)) return "-";
      return productos
        .filter((p) => p && p.nombre_producto)
        .map((p) => p.nombre_producto)
        .join(", ");
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
        this.currentRecord = { ...item };
        this.showDetailsModal = true;

        const response = await axios.get(
          `http://127.0.0.1:8000/ufc/por-situar/${item.id}/`
        );
        this.currentRecord = {
          ...this.currentRecord,
          ...response.data,
        };

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

    /*     async getPorSituarCarga_Descargas() {
      this.loading = true;
      try {
        const response = await axios.get("ufc/por-situar-hoy/", {
          params: {
            page: this.currentPage,
            page_size: this.itemsPerPage,
          },
        });

        this.porSituarCarga_Descarga = response.data.results;
        this.allRecords = [...response.data.results]; // Guardar copia completa para filtrado
        this.totalItems = response.data.count;
        this.busqueda_existente = true;
      } catch (error) {
        console.error(
          "Error al obtener los registros por situar carga/deacarga",
          error
        );
        this.busqueda_existente = false;
      } finally {
        this.loading = false;
      }
    }, */

    async getPorSituar() {
      this.loading = true;
      const today = new Date();
      const fechaFormateada = `${today.getFullYear()}-${String(
        today.getMonth() + 1
      ).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;

      try {
        const infoID = await axios.get(
          `/ufc/verificar-informe-existente/?fecha_operacion=${fechaFormateada}`
        );
        this.estado_parte = infoID.data.estado;

        //Para la reutilizacion del componente se deberia usar el operador ternario en informe: props.informeId? props.informeId: infoID.data.id
        
        if (this.informeID || infoID.data.id) {
          const response = await axios.get("/ufc/por-situar/", {
            params: {
              page: this.currentPage,
              page_size: this.itemsPerPage,
              informe: this.informeID ? this.informeID : infoID.data.id,
            },
          });
          
          if(this.informeID){
            this.habilitado = false;
          }
          this.porSituarCarga_Descarga = response.data.results;
          this.totalItems = response.data.count;
        } else {
          this.showErrorToast("No hay ID para cargar");
        }
      } catch (error) {
        console.error("Error al obtener datos:", error);
      } finally {
        this.loading = false;
      }
    },

    // Nuevo método de búsqueda adaptado del componente que funciona
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        if (!this.searchQuery.trim()) {
          this.porSituarCarga_Descarga = [...this.allRecords];
          this.busqueda_existente = true;
          return;
        }

        const query = this.searchQuery.toLowerCase();
        this.porSituarCarga_Descarga = this.allRecords.filter((item) => {
          const tipoEquipo =
            item.tipo_equipo_ferroviario_name?.toLowerCase() || "";
          const productos = item.productos_list?.toLowerCase() || "";
          const estado = item.estado?.toLowerCase() || "";

          return (
            tipoEquipo.includes(query) ||
            productos.includes(query) ||
            estado.includes(query)
          );
        });

        this.busqueda_existente = this.porSituarCarga_Descarga.length > 0;
      }, 300);
    },

    // Métodos de paginación
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.getPorSituarCarga_Descargas();
      }
    },

    nextPage() {
      if (this.currentPage * this.itemsPerPage < this.totalItems) {
        this.currentPage++;
        this.getPorSituarCarga_Descargas();
      }
    },

    goToPage(page) {
      this.currentPage = page;
      this.getPorSituarCarga_Descargas();
    },

    async delete_tren(id) {
      try {
        await axios.delete(`/ufc/por-situar/${id}/`);
        this.porSituarCarga_Descarga = this.porSituarCarga_Descarga.filter(
          (objeto) => objeto.id !== id
        );
        this.showSuccessToast("El registro ha sido eliminado correctamente");
      } catch (error) {
        console.error("Error al eliminar el producto:", error);
        this.showErrorToast("Hubo un error al eliminar el producto.");
      }
    },

    editRegistroPorSituar(item) {
      console.log(item)
      // Aquí puedes implementar la navegación a la página de edición
      this.$router.push({
        name: "EditarPorSituar",
        params: { id: item.id },
      });
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
          this.delete_tren(id);
        }
      });
    },

    // Método para manejar errores (similar al del componente que funciona)
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
.card-header {
  background-color: #f8f9fa;
  border-bottom: 2px solid #e0e0e0 !important;
  padding: 0.75rem 1.25rem;
}

/* Estilos para el contenedor del buscador */
.search-container {
  position: relative;
  width: 100%;
  max-width: 300px; /* Ancho máximo del buscador */
}

/* Estilos para el input del buscador */
.search-container input {
  padding-right: 40px; /* Espacio para el icono de lupa */
  border-radius: 20px; /* Bordes redondeados */
}

/* Estilos para el icono de lupa */
.search-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #888; /* Color del icono */
  pointer-events: none; /* Evita que el icono interfiera con el input */
}

/* Estilos para la tabla responsive */
.table-responsive {
  overflow-x: auto; /* Permite desplazamiento horizontal en pantallas pequeñas */
}

/* Estilos para el icono de agregar */
.btn-link {
  color: #007bff; /* Color azul para el icono */
  text-decoration: none; /* Sin subrayado */
}

.btn-link:hover {
  color: #0056b3; /* Color azul más oscuro al pasar el mouse */
}

.search-container {
  position: relative;
  width: 100%;
  max-width: 300px;
}

.search-container input {
  padding-left: 2.5rem !important; /* Espacio para el icono */
  border-radius: 20px !important;
}

.search-container .bi-search {
  color: #6c757d; /* Color gris para el icono */
  z-index: 10;
}

/* Para asegurar que el input group conserve los estilos */
.input-group {
  width: 100%;
}

/* Tabla */
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
}

.ps-modal {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow: auto;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.pagination-container button {
  margin: 0 5px;
}

/* Estados de carga y vacío */
.ps-loading-td,
.ps-empty-td {
  padding: 3rem !important;
}

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

.ps-empty-action {
  margin-top: 1rem;
  color: var(--ps-primary);
  text-decoration: none;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: var(--ps-transition);
}

.ps-empty-action:hover {
  color: var(--ps-primary-hover);
  transform: translateY(-2px);
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
  border-radius: var(--ps-border-radius);
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  animation: slideUp 0.4s cubic-bezier(0.22, 1, 0.36, 1);
  overflow: hidden;
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
}

.ps-modal h2 {
  margin: 0;
  font-size: 1.4rem;
}

.ps-modal-subtitle {
  margin: 0.25rem 0 0;
  font-size: 0.9rem;
  opacity: 0.9;
  font-weight: 400;
}

.ps-modal-close {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: var(--ps-transition);
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
  border-radius: var(--ps-border-radius);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: var(--ps-transition);
  border: 1px solid var(--ps-light-gray);
}

.ps-detail-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.ps-detail-card-header {
  padding: 1rem;
  background-color: #0d6efd;
  color: white;
  border-bottom: 1px solid var(--ps-light-gray);
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.ps-detail-card-header i {
  font-size: 1.2rem;
  color: var(--ps-primary);
}

.ps-detail-card-header h4 {
  margin: 0;
  font-size: 1rem;
  color: var(--ps-dark);
}

.ps-detail-card-body {
  padding: 1rem;
}

.ps-detail-card-highlight {
  border: 1px solid rgba(67, 97, 238, 0.3);
}

.ps-detail-card-highlight .ps-detail-card-header {
  background: linear-gradient(to right, rgba(67, 97, 238, 0.05), white);
}

.ps-detail-card-highlight .ps-detail-card-header i {
  color: var(--ps-accent);
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
  color: var(--ps-gray);
  font-weight: 500;
}

.ps-detail-value {
  font-size: 1rem;
  color: var(--ps-dark);
  font-weight: 500;
  word-break: break-word;
}

.ps-highlight-value {
  color: var(--ps-primary);
  font-weight: 600;
  font-size: 1.1rem;
}

.ps-modal-footer {
  padding: 1.25rem 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  background: white;
  border-top: 1px solid var(--ps-light-gray);
}

.ps-modal-btn {
  padding: 0.6rem 1.2rem;
  border-radius: var(--ps-border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: var(--ps-transition);
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.ps-modal-btn-secondary {
  background: white;
  color: var(--ps-gray);
  border: 1px solid var(--ps-light-gray);
}

.ps-modal-btn-secondary:hover {
  background: #f1f3f5;
  color: var(--ps-dark);
}

.ps-modal-btn-primary {
  background: var(--ps-primary);
  color: white;
  box-shadow: 0 2px 6px rgba(67, 97, 238, 0.2);
}

.ps-modal-btn-primary:hover {
  background: var(--ps-primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3);
}

.ps-status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
}

.ps-status-success {
  background: rgba(76, 201, 240, 0.1);
  color: #06d6a0;
  border: 1px solid rgba(6, 214, 160, 0.2);
}


.ps-status-danger {
  background: rgba(247, 37, 133, 0.1);
  color: #f72585;
  border: 1px solid rgba(247, 37, 133, 0.2);
}

.ps-status-default {
  background: rgba(108, 117, 125, 0.1);
  color: var(--io-gray);
  border: 1px solid rgba(108, 117, 125, 0.2);
}
</style>
