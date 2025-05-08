<template>
  <div class="por-situar-container">
    <!-- Header con título y acciones -->
    <div class="ps-header">
      <h1 class="ps-title">
        <i class="bi bi-inboxes-fill ps-title-icon"></i>
        Registros Por Situar
      </h1>

      <div class="ps-actions">
        <button class="btn btn-link p-0">
          <router-link to="/AdicionarPorSituar"
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
              <th class="ps-th">Tipo Origen</th>
              <th class="ps-th">Origen</th>
              <th class="ps-th">Tipo Equipo</th>
              <th class="ps-th">Estado</th>
              <th class="ps-th">Operación</th>
              <th class="ps-th">Producto</th>
              <th class="ps-th">Por Situar</th>
              <th class="ps-th ps-th-actions">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <!-- Estado de carga -->
            <tr v-if="loading">
              <td colspan="9" class="ps-loading-td">
                <div class="ps-loading">
                  <div class="ps-spinner"></div>
                  <span>Cargando registros...</span>
                </div>
              </td>
            </tr>

            <!-- Filas de datos -->
            <tr
              v-for="(item, index) in filteredRecords"
              :key="item.id"
              class="ps-tr"
            >
              <td class="ps-td">{{ item.tipo_origen_name }}</td>
              <td class="ps-td">{{ item.origen }}</td>
              <td class="ps-td">{{ item.tipo_equipo_name }}</td>
              <td class="ps-td">
                <span
                  :class="`ps-status ps-status-${getStatusClass(item.estado)}`"
                >
                  {{ item.estado }}
                </span>
              </td>
              <td class="ps-td">{{ item.operacion }}</td>
              <td class="ps-td">
                <span
                  v-if="item.productos_info && item.productos_info.length > 0"
                >
                  {{ getNombresProductos(item.productos_info) }}
                </span>
                <span v-else>-</span>
              </td>
              <td class="ps-td">{{ item.por_situar }}</td>

              <!-- Acciones -->
              <td v-if="hasGroup('AdminUFC')" class="ps-td">
                <div class="d-flex">
                  <button
                    @click="viewDetails(item)"
                    class="btn btn-sm btn-outline-info me-2"
                    title="Ver detalles"
                  >
                    <i class="bi bi-eye-fill"></i>
                  </button>

                  <router-link
                    :to="{
                      name: 'EditarPorSituar',
                      params: { id: item.id || 'default-id' },
                    }"
                    class="btn btn-sm btn-outline-warning me-2"
                    title="Editar"
                  >
                    <i class="bi bi-pencil-square"></i>
                  </router-link>

                  <button
                    @click="confirmDelete(item.id)"
                    class="btn btn-sm btn-outline-danger"
                    title="Eliminar"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </td>
            </tr>

            <!-- Estado vacío -->
            <tr v-if="!loading && filteredRecords.length === 0">
              <td colspan="9" class="ps-empty-td">
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
                        : "No hay registros por situar en este momento"
                    }}
                  </p>
                  <router-link
                    to="/AdicionarPorSituar"
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
    <div
      class="ps-pagination d-flex justify-content-between align-items-center"
    >
      <div class="ps-pagination-info">
        Mostrando {{ Math.min(currentPage * itemsPerPage, totalItems) }} de
        {{ totalItems }} registros
      </div>
      <nav aria-label="Navegación de páginas">
        <ul class="pagination pagination-sm mb-0">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link ps-pagination-btn" @click="previousPage">
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
            <button class="page-link ps-pagination-btn" @click="nextPage">
              <i class="bi bi-chevron-right"></i>
            </button>
          </li>
        </ul>
      </nav>
    </div>
    <!-- Modal de detalles - Versión mejorada con más color -->
    <div
      v-if="showDetailsModal"
      class="ps-modal-overlay"
      @click.self="closeModal"
    >
      <div class="ps-modal">
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

        <div class="ps-modal-body">
          <div class="ps-detail-grid">
            <div class="ps-detail-card">
              <div class="ps-detail-card-header">
                <i class="bi bi-tag-fill"></i>
                <h4>Información Básica</h4>
              </div>
              <div class="ps-detail-card-body">
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Tipo Origen:</span>
                  <span class="ps-detail-value">{{
                    currentRecord.tipo_origen_name ||
                    currentRecord.tipo_origen ||
                    "N/A"
                  }}</span>
                </div>

                <div class="ps-detail-item">
                  <span class="ps-detail-label">Origen:</span>
                  <span class="ps-detail-value">{{
                    currentRecord.origen || "N/A"
                  }}</span>
                </div>

                <div class="ps-detail-item">
                  <span class="ps-detail-label">Tipo de Equipo:</span>
                  <span class="ps-detail-value">{{
                    currentRecord.tipo_equipo_name || "N/A"
                  }}</span>
                </div>
              </div>
            </div>

            <div class="ps-detail-card">
              <div class="ps-detail-card-header">
                <i class="bi bi-clipboard2-data-fill"></i>
                <h4>Estado y Operación</h4>
              </div>
              <div class="ps-detail-card-body">
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Estado:</span>
                  <span class="ps-detail-value">
                    <span
                      :class="`ps-status ps-status-${getStatusClass(
                        currentRecord.estado
                      )}`"
                    >
                      {{ currentRecord.estado || "N/A" }}
                    </span>
                  </span>
                </div>

                <div class="ps-detail-item">
                  <span class="ps-detail-label">Operación:</span>
                  <span class="ps-detail-value">{{
                    currentRecord.operacion || "N/A"
                  }}</span>
                </div>

                <div class="ps-detail-item">
                  <span class="ps-detail-label">Producto:</span>
                  <span class="ps-detail-value">
                    <span
                      v-if="
                        currentRecord.productos_info &&
                        currentRecord.productos_info.length > 0
                      "
                    >
                      {{ getNombresProductos(currentRecord.productos_info) }}
                    </span>
                    <span v-else>N/A</span>
                  </span>
                </div>
              </div>
            </div>

            <div class="ps-detail-card ps-detail-card-highlight">
              <div class="ps-detail-card-header">
                <i class="bi bi-exclamation-square-fill"></i>
                <h4>Cantidad</h4>
              </div>
              <div class="ps-detail-card-body">
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Por Situar:</span>
                  <span class="ps-detail-value ps-highlight-value">
                    {{ currentRecord.por_situar || "0" }}
                  </span>
                </div>
              </div>
            </div>

            <div class="ps-detail-card ps-detail-card-full">
              <div class="ps-detail-card-header">
                <i class="bi bi-chat-square-text-fill"></i>
                <h4>Observaciones</h4>
              </div>
              <div class="ps-detail-card-body">
                <div class="ps-detail-item">
                  <span class="ps-detail-value">{{
                    currentRecord.observaciones ||
                    "Ninguna observación registrada"
                  }}</span>
                </div>
              </div>
            </div>

            <div class="ps-detail-card">
              <div class="ps-detail-card-header">
                <i class="bi bi-calendar-event-fill"></i>
                <h4>Meta Información</h4>
              </div>
              <div class="ps-detail-card-body">
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Fecha Creación:</span>
                  <span class="ps-detail-value">
                    {{
                      currentRecord.created_at
                        ? formatDateTime(currentRecord.created_at)
                        : "N/A"
                    }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

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
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";

export default {
  data() {
    return {
      allRecords: [],
      debounceTimeout: null,
      isEditing: false,
      currentItemId: null,
      searchQuery: "",
      registrosPorSituar: [],
      loading: false,
      busqueda_existente: true,
      showModal: false,
      showDetailsModal: false,
      currentRecord: {},
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 0,
      userGroups: [],
      userPermissions: [],
    };
  },

  computed: {
    filteredRecords() {
      if (!this.searchQuery) return this.registrosPorSituar;
      const query = this.searchQuery.toLowerCase();
      return this.registrosPorSituar.filter((item) => {
        const fieldsToSearch = [
          item.tipo_origen_name,
          item.origen,
          item.tipo_equipo_name,
          item.estado,
          item.operacion,
          item.productos_info
            ? this.getNombresProductos(item.productos_info)
            : "",
          item.por_situar,
          item.observaciones,
        ];
        return fieldsToSearch.some(
          (field) => field && field.toString().toLowerCase().includes(query)
        );
      });
    },
  },

  mounted() {
    this.getPorSituar();
    this.fetchUserPermissionsAndGroups();
  },

  methods: {
    hasGroup(group) {
      return this.userGroups.some((g) => g.name === group);
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

    getPorSituar() {
      this.loading = true;
      axios
        .get("http://127.0.0.1:8000/ufc/por-situar-hoy/")
        .then((response) => {
          this.registrosPorSituar = response.data.results;
          this.totalItems = response.data.count;
          this.loading = false;
        })

        .catch((error) => {
          console.error("Error al obtener datos:", error);
          this.errorLoading = true;
          this.loading = false;
          this.showErrorToast("No se pudieron cargar los registros");
        });
      console.log("que lasodsjkbvbksdjfksd: ", this.registrosPorSituar);
    },

    getNombresProductos(productos) {
      if (!productos || !Array.isArray(productos)) return "-";
      return productos
        .filter((p) => p && p.nombre_producto)
        .map((p) => p.nombre_producto)
        .join(", ");
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

    editRecord(item) {
      // Implementa la lógica de edición aquí
      console.log("Editar registro:", item);
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

    getStatusClass(status) {
      if (!status) return "default";
      const statusLower = status.toLowerCase();

      if (statusLower.includes("activo")) return "success";
      if (statusLower.includes("pendiente")) return "warning";
      if (statusLower.includes("inactivo") || statusLower.includes("cancelado"))
        return "danger";

      return "info";
    },

    closeModal() {
      this.showDetailsModal = false;
      this.currentRecord = {};
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
      });

      if (result.isConfirmed) {
        try {
          this.loading = true;
          await axios.delete(`/ufc/por-situar-hoy/${id}/`);
          this.showSuccessToast("Registro eliminado");
          await this.getPorSituar();
        } catch (error) {
          this.handleApiError(error, "eliminar registro");
        } finally {
          this.loading = false;
        }
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

    handleSearchInput() {
      if (this.debounceTimeout) {
        clearTimeout(this.debounceTimeout);
      }
      this.debounceTimeout = setTimeout(() => {
        // Lógica de búsqueda si es necesaria
      }, 300);
    },
  },
};
</script>

<style scoped>
/* Estilos CSS de los botones (de la primera tabla) */
.btn-small {
  font-size: 22px; /* Aumenta el tamaño del ícono */
  color: black;
  margin-right: 5px;
  outline: none; /* Elimina el borde de foco */
  border: none;
  background: none; /* Elimina el fondo */
  padding: 0; /* Elimina el padding para que solo se vea el ícono */
}

.btn-eye {
  font-size: 22px; /* Aumenta el tamaño del ícono */
  margin-right: 5px;
  outline: none; /* Elimina el borde de foco */
  border: none;
  background: none; /* Elimina el fondo */
  padding: 0; /* Elimina el padding para que solo se vea el ícono */
}

.btn:hover {
  scale: 1.1; /* Asegura que no haya fondo al hacer hover */
}

.btn:focus {
  outline: none; /* Elimina el borde de foco al hacer clic */
  box-shadow: none; /* Elimina cualquier sombra de foco en algunos navegadores */
}

.producto-item {
  padding: 0.5rem 0;
  border-bottom: 1px dashed #eee;
}
.producto-item:last-child {
  border-bottom: none;
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

.ps-search-input:focus {
  outline: none;
  border-color: var(--ps-primary);
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.15);
}

.ps-search-border {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--ps-primary);
  transition: var(--ps-transition);
}

.ps-search-input:focus ~ .ps-search-border {
  width: 100%;
}

/* Tarjeta contenedora */
.ps-card {
  background: white;
  border-radius: var(--ps-border-radius);
  box-shadow: var(--ps-box-shadow);
  overflow: hidden;
  transition: var(--ps-transition);
}

.ps-card:hover {
  box-shadow: 0 10px 35px rgba(0, 0, 0, 0.12);
}

/* Tabla */
.ps-table-container {
  overflow-x: auto;
  padding: 0.5rem;
}

.ps-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  min-width: 1000px;
}

.ps-th {
  padding: 1rem 1.2rem;
  text-align: left;
  font-weight: 600;
  color: var(--ps-dark);
  background-color: #f9fafb;
  border-bottom: 2px solid var(--ps-light-gray);
  position: sticky;
  top: 0;
}

.ps-th-actions {
  text-align: center;
}

.ps-tr {
  transition: var(--ps-transition);
}

.ps-tr:hover {
  background-color: rgba(67, 97, 238, 0.03);
}

.ps-td {
  padding: 1rem 1.2rem;
  border-bottom: 1px solid var(--ps-light-gray);
  color: var(--ps-dark);
}

.ps-td-index {
  font-weight: 600;
  color: var(--ps-gray);
}

.ps-td-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

/* Botones de acción con efecto transparente al hover */
.ps-action-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: var(--ps-transition);
  background: transparent;
  color: var(--ps-gray);
  position: relative;
  overflow: hidden;
}

.ps-action-btn::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: currentColor;
  opacity: 0.1;
  transition: var(--ps-transition);
}

.ps-action-btn:hover {
  transform: translateY(-2px);
  opacity: 0.8;
}

.ps-action-btn:hover::before {
  opacity: 0.2;
}

.ps-action-view {
  color: var(--ps-info);
}

.ps-action-edit {
  color: var(--ps-warning);
}

.ps-action-delete {
  color: var(--ps-danger);
}

.ps-action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.ps-action-btn i {
  position: relative;
  z-index: 1;
}

/* Badges y estados */
.ps-badge {
  display: inline-block;
  padding: 0.25rem 0.6rem;
  border-radius: 50px;
  font-weight: 600;
  font-size: 0.8rem;
  background: var(--ps-primary);
  color: white;
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

.ps-status-warning {
  background: rgba(248, 150, 30, 0.1);
  color: #f8961e;
  border: 1px solid rgba(248, 150, 30, 0.2);
}

.ps-status-danger {
  background: rgba(247, 37, 133, 0.1);
  color: #f72585;
  border: 1px solid rgba(247, 37, 133, 0.2);
}

.ps-status-info {
  background: rgba(72, 149, 239, 0.1);
  color: #4895ef;
  border: 1px solid rgba(72, 149, 239, 0.2);
}

.ps-status-default {
  background: rgba(108, 117, 125, 0.1);
  color: var(--ps-gray);
  border: 1px solid rgba(108, 117, 125, 0.2);
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
  animation: slideUp 0.4s cubic-bezier(0.22, 1, 0.36, 1);
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.1);
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
  background: rgba(255, 255, 255, 0.2);
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
  .ps-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .ps-actions {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .ps-search-container {
    width: 100%;
  }

  .ps-detail-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .por-situar-container {
    padding: 1.5rem 1rem;
  }

  .ps-title {
    font-size: 1.5rem;
  }

  .ps-modal {
    width: 95%;
  }

  .ps-modal-body {
    padding: 1.25rem 1rem;
  }

  .ps-modal-footer {
    padding: 1rem;
    flex-direction: column;
  }

  .ps-modal-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
