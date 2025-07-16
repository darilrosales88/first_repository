<template>
  <div class="por-situar-container">
    <!-- Header con título y acciones -->
    <div class="ps-header">
      <h1 class="ps-title">
        <i class="bi bi-train-front-fill ps-title-icon"></i>
        Vagones en Tren
      </h1>

      <div class="ps-actions">
        <button class="btn btn-link p-0">
          <router-link to="/AdicionarVagon"
            ><i class="bi bi-plus-circle fs-3"></i
          ></router-link>
        </button>

        <!-- Buscador moderno -->
        <div class="ps-search-container">
          <i class="bi bi-search ps-search-icon"></i>
          <input
            type="search"
            class="ps-search-input"
            placeholder="Buscar registros..."
            v-model="searchQuery"
            @input="handleSearchInput"
          />
          <div class="ps-search-border"></div>
        </div>
      </div>
    </div>

    <!-- Tarjeta contenedora de la tabla -->
    <div class="ps-card">
      <!-- Tabla con diseño moderno -->
      <div class="ps-table-container">
        <table class="ps-table">
          <thead>
            <tr>
              <th class="ps-th">Código Locomotora</th>
              <th class="ps-th">Tipo de Equipo</th>
              <th class="ps-th">Estado</th>
              <th class="ps-th">Producto</th>
              <th class="ps-th">Cant. Vagones</th>
              <th class="ps-th">Origen</th>
              <th class="ps-th">Destino</th>
              <th class="ps-th" v-if="showNoId">Descripción</th>
              <th class="ps-th ps-th-actions">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <!-- Estado de carga -->
            <tr v-if="loading">
              <td :colspan="showNoId ? 10 : 9" class="ps-loading-td">
                <div class="ps-loading">
                  <div class="ps-spinner"></div>
                  <span>Cargando registros...</span>
                </div>
              </td>
            </tr>

            <!-- Filas de datos -->
            <tr
              v-for="(tren, index) in filteredRecords"
              :key="tren.id"
              class="ps-tr"
            >
              <td class="ps-td">
                {{ tren.numero_identificacion_locomotora || "-" }}
              </td>
              <td class="ps-td">{{ tren.tipo_equipo_name || "-" }}</td>
              <td class="ps-td">
                <span
                  :class="`ps-status ps-status-${getStatusClass(tren.estado)}`"
                >
                  {{ tren.estado || "-" }}
                </span>
              </td>
              <td class="ps-td">
                <span
                  v-if="tren.productos_info && tren.productos_info.length > 0"
                >
                  {{ getNombresProductos(tren.productos_info) }}
                </span>
                <span v-else>-</span>
              </td>
              <td class="ps-td">
                <span class="ps-badge">{{ tren.cantidad_vagones || "0" }}</span>
              </td>
              <td class="ps-td">{{ tren.origen || "-" }}</td>
              <td class="ps-td">{{ tren.destino || "-" }}</td>
              <td class="ps-td" v-if="showNoId">
                {{ tren.descripcion || "-" }}
              </td>

              <!-- En el td de acciones de la tabla -->
              <td class="ps-td ps-td-actions">
                <div class="d-flex">
                  <button
                    @click="viewDetails(tren)"
                    class="btn btn-sm btn-outline-info me-2"
                    title="Ver detalles"
                  >
                    <i class="bi bi-eye-fill"></i>
                  </button>
                  <router-link
                    :to="{
                      name: 'EditarEnTren',
                      params: { id: tren.id },
                    }"
                    class="btn btn-sm btn-outline-warning me-2"
                    title="Editar"
                  >
                    <i class="bi bi-pencil-square"></i>
                  </router-link>
                  <button
                    @click="confirmDelete(tren.id)"
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
              <td :colspan="showNoId ? 10 : 9" class="ps-empty-td">
                <div class="ps-empty-state">
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
                        : "No hay vagones registrados en este momento"
                    }}
                  </p>
                  <router-link
                    to="/AdicionarVagon"
                    class="ps-empty-action"
                    v-if="!searchQuery"
                  >
                    <i class="bi bi-plus-circle"></i> Crear primer registro
                  </router-link>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Paginación mejorada -->
    <div class="ps-pagination">
      <div class="text-muted small">
        Mostrando {{ en_trenes.length }} de {{ totalItems }} registros
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
    <!-- Fin Paginacion -->

    <!-- Modal de detalles - Versión mejorada con más color -->
    <div
      v-if="showDetailsModal"
      class="ps-modal-overlay"
      @click.self="closeDetailsModal"
    >
      <div class="ps-modal">
        <div class="ps-modal-header">
          <div class="ps-modal-header-content">
            <div class="ps-modal-icon-container">
              <i class="bi bi-info-circle-fill ps-modal-icon"></i>
            </div>
            <div>
              <h2>Detalles del Vagon</h2>
              <p class="ps-modal-subtitle">
                Información completa del registro seleccionado
              </p>
            </div>
          </div>
          <button class="ps-modal-close" @click="closeDetailsModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>

        <div class="ps-modal-body">
          <div class="ps-detail-grid">
            <div class="ps-detail-card">
              <div class="ps-detail-card-header">
                <i class="bi bi-tag-fill"></i>
                <h4>Información Básica</h4>
              </div>
              <div class="ps-detail-card-body">
                <div class="ps-detail-item">
                  <span class="ps-detail-label">No Id Locomotora:</span>
                  <span class="ps-detail-value">{{
                    currentTren.numero_identificacion_locomotora || "N/A"
                  }}</span>
                </div>

                <div class="ps-detail-item">
                  <span class="ps-detail-label">Tipo de equipo:</span>
                  <span class="ps-detail-value">{{
                    currentTren.tipo_equipo_name || "N/A"
                  }}</span>
                </div>

                <div class="ps-detail-item">
                  <span class="ps-detail-label">Estado:</span>
                  <span class="ps-detail-value">
                    <span
                      :class="`ps-status ps-status-${getStatusClass(
                        currentTren.estado
                      )}`"
                    >
                      {{ currentTren.estado || "N/A" }}
                    </span>
                  </span>
                </div>
              </div>
            </div>

            <div class="ps-detail-card">
              <div class="ps-detail-card-header">
                <i class="bi bi-clipboard2-data-fill"></i>
                <h4>Producto y Cantidad</h4>
              </div>
              <div class="ps-detail-card-body">
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Producto Id:</span>
                  <span class="ps-detail-value">{{
                    currentTren.producto || "N/A"
                  }}</span>
                </div>

                <div class="ps-detail-item">
                  <span class="ps-detail-label">Producto nombre:</span>
                  <span class="ps-detail-value">{{
                    getNombresProductos(currentTren.productos_info)
                  }}</span>
                </div>

                <div class="ps-detail-item">
                  <span class="ps-detail-label">Cantidad de vagones:</span>
                  <span class="ps-detail-value">{{
                    currentTren.cantidad_vagones || "0"
                  }}</span>
                </div>
              </div>
            </div>

            <div class="ps-detail-card">
              <div class="ps-detail-card-header">
                <i class="bi bi-geo-alt-fill"></i>
                <h4>Origen y Destino</h4>
              </div>
              <div class="ps-detail-card-body">
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Tipo de origen:</span>
                  <span class="ps-detail-value">{{
                    currentTren.tipo_origen || "N/A"
                  }}</span>
                </div>

                <div class="ps-detail-item">
                  <span class="ps-detail-label">Origen:</span>
                  <span class="ps-detail-value">{{
                    currentTren.origen || "N/A"
                  }}</span>
                </div>

                <div class="ps-detail-item">
                  <span class="ps-detail-label">Tipo de destino:</span>
                  <span class="ps-detail-value">{{
                    currentTren.tipo_destino || "N/A"
                  }}</span>
                </div>

                <div class="ps-detail-item">
                  <span class="ps-detail-label">Destino:</span>
                  <span class="ps-detail-value">{{
                    currentTren.destino || "N/A"
                  }}</span>
                </div>
              </div>
            </div>

            <div class="ps-detail-card ps-detail-card-highlight">
              <div class="ps-detail-card-header">
                <i class="bi bi-gear-fill"></i>
                <h4>Equipo</h4>
              </div>
              <div class="ps-detail-card-body">
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Equipo de carga:</span>
                  <span class="ps-detail-value ps-highlight-value">
                    {{ currentTren.equipo_carga_name || "N/A" }}
                  </span>
                </div>
              </div>
            </div>

            <div class="ps-detail-card ps-detail-card-full">
              <div class="ps-detail-card-header">
                <i class="bi bi-chat-square-text-fill"></i>
                <h4>Descripción y Observaciones</h4>
              </div>
              <div class="ps-detail-card-body">
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Descripción:</span>
                  <span class="ps-detail-value">{{
                    currentTren.descripcion || "Ninguna"
                  }}</span>
                </div>
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Observaciones:</span>
                  <span class="ps-detail-value">{{
                    currentTren.observaciones || "Ninguna"
                  }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="ps-modal-footer">
          <button
            class="ps-modal-btn ps-modal-btn-secondary"
            @click="closeDetailsModal"
          >
            <i class="bi bi-x-circle"></i> Cerrar
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
  name: "EnTrenes",
  data() {
    return {
      en_trenes: [],
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 0,
      searchQuery: "",
      debounceTimeout: null,
      busqueda_existente: true,
      userPermissions: [],
      userGroups: [],
      showContent: false,
      mostrarModal: false,
      loading: false,
      user_role: "",
      showNoId: false,
      showDetailsModal: false,
      currentTren: {},
      allRecords: [],
    };
  },

  computed: {
    filteredRecords() {
      if (!this.searchQuery) return this.en_trenes;

      const query = this.searchQuery.toLowerCase();
      return this.en_trenes.filter((item) => {
        const fieldsToSearch = [
          item.numero_identificacion_locomotora,
          item.tipo_equipo,
          item.estado,
          item.producto_name,
          item.cantidad_vagones?.toString(),
          item.origen,
          item.destino,
          item.descripcion,
          item.observaciones,
        ];

        return fieldsToSearch.some(
          (field) => field && field.toString().toLowerCase().includes(query)
        );
      });
    },
    hasPermission() {
      if (this.user_role === "role") {
        return true;
      } else {
        return this.user_role === "admin";
      }
    },
  },

  async mounted() {
    await this.getTrenes();
    await this.fetchUserPermissionsAndGroups();
  },

  methods: {
    toggleContentVisibility() {
      this.showNoId = !this.showNoId;
    },
    getNombresProductos(productos) {
      if (!productos || !Array.isArray(productos)) return "-";
      return productos
        .filter((p) => p && p.nombre_producto && p.codigo_producto)
        .map((p) => `${p.nombre_producto} (${p.codigo_producto})`)
        .join(", ");
    },

    hasGroup(group) {
      return this.userGroups.some((g) => g.name === group);
    },

    async fetchUserPermissionsAndGroups() {
      try {
        const userId = localStorage.getItem("userid");
        if (userId) {
          const response = await axios.get(`/apiAdmin/users/${userId}/`);
          this.userPermissions = response.data.permissions;
          this.userGroups = response.data.groups;
          this.user_role = response.data.role;
        }
      } catch (error) {
        console.error("Error al obtener permisos y grupos:", error);
      }
    },
    async viewDetails(item) {
      this.loading = true;
      try {
        this.currentTren = { ...item };
        const response = await axios.get(
          `http://127.0.0.1:8000/ufc/en-trenes/${item.id}/`
        );
        this.currentTren = response.data;
        this.showDetailsModal = true;
      } catch (error) {
        console.error("Error al cargar detalles:", error);
        this.showErrorToast("No se pudieron cargar los detalles completos");
      } finally {
        this.loading = false;
      }
    },

    async getTrenes() {
      this.loading = true;
      try {
        const response = await axios.get("/ufc/en-trenes/", {
          params: {
            page: this.currentPage,
            page_size: this.itemsPerPage,
          },
        });
        this.en_trenes = response.data.results;
        this.allRecords = response.data.results;
        this.totalItems = response.data.count;
      } catch (error) {
        console.error("Error al obtener los trenes:", error);
        this.showErrorToast("No se pudieron cargar los registros");
      } finally {
        this.loading = false;
      }
    },

    async searchTrenes() {
      this.loading = true;
      try {
        const response = await axios.get("/ufc/en-trenes/", {
          params: {
            search: this.searchQuery,
          },
        });
        this.en_trenes = response.data.results;
        this.totalItems = response.data.count;
        this.busqueda_existente = this.en_trenes.length > 0;
      } catch (error) {
        console.error("Error al buscar trenes", error);
        this.busqueda_existente = false;
        this.showErrorToast("Error al buscar registros");
      } finally {
        this.loading = false;
      }
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchTrenes();
      }, 300);
    },

    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.getTrenes();
      }
    },

    nextPage() {
      if (this.currentPage * this.itemsPerPage < this.totalItems) {
        this.currentPage++;
        this.getTrenes();
      }
    },

    goToPage(page) {
      this.currentPage = page;
      this.getTrenes();
    },

    async delete_tren(id) {
      try {
        await axios.delete(`/ufc/en-trenes/${id}/`);
        this.en_trenes = this.en_trenes.filter((tren) => tren.id !== id);
        this.showSuccessToast("Registro eliminado");
      } catch (error) {
        console.error("Error al eliminar el producto:", error);
        this.showErrorToast("Error al eliminar el registro");
      }
    },

    openVagonDetailsModal(tren) {
      this.currentTren = { ...tren };
      this.showDetailsModal = true;
    },

    closeDetailsModal() {
      this.showDetailsModal = false;
      this.currentTren = {};
    },

    getStatusClass(status) {
      if (!status) return "default";
      const statusLower = status.toLowerCase();

      if (statusLower.includes("activo")) return "success";
      if (statusLower.includes("pendiente")) return "warning";
      if (statusLower.includes("inactivo") || statusLower.includes("cancelado"))
        return "danger";

      return "info";
    },

    confirmDelete(id) {
      Swal.fire({
        title: "¿Eliminar registro?",
        text: "Esta acción no se puede deshacer",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#ff4444",
        cancelButtonColor: "#33b5e5",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
        customClass: {
          popup: "ps-swal-popup",
          confirmButton: "ps-swal-confirm",
          cancelButton: "ps-swal-cancel",
        },
      }).then((result) => {
        if (result.isConfirmed) {
          this.delete_tren(id);
        }
      });
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
/* Estilos para los botones */
.btn-outline-info {
  color: #0dcaf0;
  border-color: #0dcaf0;
}

.btn-outline-warning {
  color: #ffc107;
  border-color: #ffc107;
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

.ps-td-actions {
  white-space: nowrap;
}
/* Variables de color */
:root {
  --ps-primary: #4361ee;
  --ps-primary-hover: #3a56d4;
  --ps-secondary: #3f37c9;
  --ps-accent: #4895ef;
  --ps-danger: #f72585;
  --ps-success: #4cc9f0;
  --ps-warning: #f8961e;
  --ps-info: #4895ef;
  --ps-light: #f8f9fa;
  --ps-dark: #212529;
  --ps-gray: #6c757d;
  --ps-light-gray: #e9ecef;
  --ps-border-radius: 12px;
  --ps-box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  --ps-transition: all 0.3s ease;
}

/* Estilos base */
.por-situar-container {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

/* Header */
.ps-header {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  gap: 1.5rem;
}

.ps-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--ps-dark);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.ps-title-icon {
  color: var(--ps-primary);
}

.ps-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

/* Botón de agregar como icono */
.ps-add-icon {
  background: var(--ps-primary);
  color: white;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  transition: var(--ps-transition);
  box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3);
  position: relative;
  overflow: hidden;
  border: none;
}

.ps-add-icon::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.3) 0%,
    rgba(255, 255, 255, 0) 70%
  );
  opacity: 0;
  transition: var(--ps-transition);
}

.ps-add-icon:hover {
  transform: translateY(-3px) scale(1.1);
  box-shadow: 0 6px 16px rgba(67, 97, 238, 0.4);
}

.ps-add-icon:hover::after {
  opacity: 1;
}

/* Buscador */
.ps-search-container {
  position: relative;
  width: 280px;
}

.ps-search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--ps-gray);
  font-size: 1rem;
}

.ps-search-input {
  width: 100%;
  padding: 0.6rem 1rem 0.6rem 2.5rem;
  border: 1px solid var(--ps-light-gray);
  border-radius: var(--ps-border-radius);
  font-size: 0.95rem;
  transition: var(--ps-transition);
  background-color: white;
}

.form-label {
  margin-bottom: 0.3rem;
  letter-spacing: 0.02rem;
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

.ps-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.75rem;
  color: var(--ps-gray);
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

/* Estilos para los botones de acción */
.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
  line-height: 1.5;
  border-radius: 0.2rem;
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
  animation: slideUp 0.4s cubic-bezier(0.22, 1, 0.36, 1);
  overflow: hidden;
}

.ps-modal-header {
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, var(--ps-primary), var(--ps-secondary));
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
  background: linear-gradient(to right, #f8f9fa, white);
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
</style>