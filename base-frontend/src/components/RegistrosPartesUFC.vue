<template>
  <div class="informes-operativos-container">
    <!-- Header con título y acciones -->
    <div class="io-header">
      <h1 class="io-title">
        <i class="bi bi-clipboard-data io-title-icon"></i>
        Partes de Informes Operativos
      </h1>

      <div class="io-actions">
        <!-- Buscador moderno -->
        <div class="io-search-container">
          <i class="bi bi-search io-search-icon"></i>
          <input
            type="search"
            class="io-search-input"
            placeholder="Buscar informes..."
            v-model="searchQuery"
            @input="handleSearchInput"
          />
          <div class="io-search-border"></div>
        </div>
      </div>
    </div>

    <!-- Tarjeta contenedora de la tabla -->
    <div class="io-card">
      <!-- Tabla con diseño moderno -->
      <div class="io-table-container">
        <table class="io-table">
          <thead>
            <tr>
              <th class="io-th">Fecha</th>
              <th class="io-th">Hora</th>
              <th class="io-th">Tipo de Parte</th>
              <th class="io-th">Provincia</th>
              <th class="io-th">Estado</th>
              <th class="io-th">Creado por</th>
              <th class="io-th">Aprobado por</th>
              <th class="io-th io-th-actions">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <!-- Estado de carga -->
            <tr v-if="loading">
              <td colspan="8" class="io-loading-td">
                <div class="io-loading">
                  <div class="io-spinner"></div>
                  <span>Cargando informes...</span>
                </div>
              </td>
            </tr>

            <!-- Filas de datos -->
            <tr
              v-for="(informe, index) in filteredRecords"
              :key="informe.id"
              class="io-tr"
            >
              <td class="io-td">
                {{ formatDate(informe.fecha_operacion) || "-" }}
              </td>
              <td class="io-td">
                {{ formatTime(informe.fecha_operacion) || "-" }}
              </td>
              <td class="io-td">Informe operativo</td>
              <td class="io-td">
                {{
                  informe.creado_por_detalle?.provincia.nombre_provincia || "-"
                }}
              </td>
              <td class="io-td">
                <span
                  :class="`io-status io-status-${getStatusClass(
                    informe.estado_parte
                  )}`"
                >
                  {{ informe.estado_parte || "-" }}
                </span>
              </td>
              <td class="io-td">
                {{ informe.creado_por_detalle?.first_name || "-" }}
              </td>
              <td class="io-td">
                {{
                  informe.aprobado_por_detalle
                    ? informe.aprobado_por_detalle.first_name
                    : "-"
                }}<!-- Uso de operador ternario una talla -->
              </td>

              <!-- Acciones -->
              <td class="io-td io-td-actions">
                <div class="d-flex">
                  <button
                    @click="viewDetails(informe)"
                    class="btn btn-sm btn-outline-info me-2"
                    title="Ver detalles"
                  >
                    <i class="bi bi-eye-fill"></i>
                  </button>
                  <!-- <router-link
                    :to="{
                      name: 'EditarInformeOperativo',
                      params: { id: informe.id },
                    }"
                    class="btn btn-sm btn-outline-warning me-2"
                    title="Editar"
                    v-if="informe.estado_parte !== 'Aprobado'"
                  >
                    <i class="bi bi-pencil-square"></i>
                  </router-link> -->
                  <button
                    @click="confirmDelete(informe.id)"
                    class="btn btn-sm btn-outline-danger"
                    title="Eliminar"
                    :disabled="loading || informe.estado_parte === 'Aprobado'"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </td>
            </tr>

            <!-- Estado vacío -->
            <tr v-if="!loading && filteredRecords.length === 0">
              <td colspan="8" class="io-empty-td">
                <div class="io-empty-state">
                  <i class="bi bi-database-exclamation"></i>
                  <h3>
                    {{
                      searchQuery ? "No hay coincidencias" : "No hay informes"
                    }}
                  </h3>
                  <p>
                    {{
                      searchQuery
                        ? `No encontramos resultados para "${searchQuery}"`
                        : "No hay informes operativos registrados"
                    }}
                  </p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Paginación -->
    <div class="io-pagination">
      <div class="text-muted small">
        Mostrando {{ filteredRecords.length }} de {{ totalItems }} registros
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

    <!-- Modal de detalles -->
    <div
      v-if="showDetailsModal"
      class="io-modal-overlay"
      @click.self="closeDetailsModal"
    >
      <div class="io-modal">
        <div class="io-modal-header">
          <div class="io-modal-header-content">
            <div class="io-modal-icon-container">
              <i class="bi bi-clipboard-data io-modal-icon"></i>
            </div>
            <div>
              <h2>Detalles del Informe Operativo</h2>
              <p class="io-modal-subtitle">
                Información completa del parte seleccionado
              </p>
            </div>
          </div>
          <button class="io-modal-close" @click="closeDetailsModal">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>

        <div class="io-modal-body">
          <div class="io-detail-grid">
            <div class="io-detail-card">
              <div class="io-detail-card-header">
                <i class="bi bi-calendar-date"></i>
                <h4>Información General</h4>
              </div>
              <div class="io-detail-card-body">
                <div class="io-detail-item">
                  <span class="io-detail-label">Fecha:</span>
                  <span class="io-detail-value">{{
                    formatFullDate(currentInforme.fecha_operacion) || "N/A"
                  }}</span>
                </div>

                <div class="io-detail-item">
                  <span class="io-detail-label">Tipo de parte:</span>
                  <span class="io-detail-value">Informe Operativo Diario</span>
                </div>

                <div class="io-detail-item">
                  <span class="io-detail-label">Estado:</span>
                  <span class="io-detail-value">
                    <span
                      :class="`io-status io-status-${getStatusClass(
                        currentInforme.estado_parte
                      )}`"
                    >
                      {{ currentInforme.estado_parte || "N/A" }}
                    </span>
                  </span>
                </div>
              </div>
            </div>

            <div class="io-detail-card">
              <div class="io-detail-card-header">
                <i class="bi bi-person-lines-fill"></i>
                <h4>Responsables</h4>
              </div>
              <div class="io-detail-card-body">
                <div class="io-detail-item">
                  <span class="io-detail-label">Creado por:</span>
                  <span class="io-detail-value">{{
                    currentInforme.creado_por_detalle?.first_name || "N/A"
                  }}</span>
                </div>

                <div class="io-detail-item">
                  <span class="io-detail-label">Aprobado por:</span>
                  <span class="io-detail-value">{{
                    currentInforme.aprobado_por_detalle?.first_name || "N/A"
                  }}</span>
                </div>
              </div>
            </div>

            <div class="io-detail-card">
              <div class="io-detail-card-header">
                <i class="bi bi-geo-alt-fill"></i>
                <h4>Ubicación</h4>
              </div>
              <div class="io-detail-card-body">
                <div class="io-detail-item">
                  <span class="io-detail-label">Provincia:</span>
                  <span class="io-detail-value">{{
                    currentInforme?.creado_por_detalle?.provincia
                      .nombre_provincia || "N/A"
                  }}</span>
                </div>
              </div>
            </div>

            <div class="io-detail-card io-detail-card-full">
              <div class="io-detail-card-header">
                <i class="bi bi-bar-chart-line-fill"></i>
                <h4>Métricas</h4>
              </div>
              <div class="io-detail-card-body">
                <div class="io-detail-item">
                  <span class="io-detail-label">Plan Mensual Total:</span>
                  <span class="io-detail-value">{{
                    currentInforme.plan_mensual_total || "0"
                  }}</span>
                </div>
                <div class="io-detail-item">
                  <span class="io-detail-label">Vagones Cargados (Plan):</span>
                  <span class="io-detail-value">{{
                    currentInforme.plan_diario_total_vagones_cargados || "0"
                  }}</span>
                </div>
                <div class="io-detail-item">
                  <span class="io-detail-label">Vagones Cargados (Real):</span>
                  <span class="io-detail-value">{{
                    currentInforme.real_total_vagones_cargados || "0"
                  }}</span>
                </div>
                <div class="io-detail-item">
                  <span class="io-detail-label">Vagones Situados:</span>
                  <span class="io-detail-value">{{
                    currentInforme.total_vagones_situados || "0"
                  }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="io-modal-footer">
          <button
            class="io-modal-btn io-modal-btn-secondary"
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
  name: "RegistrosPartes",
  data() {
    return {
      informes: [],
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 0,
      searchQuery: "",
      debounceTimeout: null,
      loading: false,
      showDetailsModal: false,
      currentInforme: {},
    };
  },

  computed: {
    filteredRecords() {
      if (!this.searchQuery) return this.informes;

      const query = this.searchQuery.toLowerCase();
      return this.informes.filter((informe) => {
        const fieldsToSearch = [
          this.formatDate(informe.fecha_operacion),
          this.formatTime(informe.fecha_operacion),
          informe.estado_parte,
          informe.provincia?.nombre,
          informe.creado_por?.username,
          informe.aprobado_por?.username,
        ];

        return fieldsToSearch.some(
          (field) => field && field.toString().toLowerCase().includes(query)
        );
      });
    },
  },

  async mounted() {
    await this.getInformes();
  },

  methods: {
    formatDate(dateString) {
      if (!dateString) return "";
      const date = new Date(dateString);
      return date.toLocaleDateString("es-ES");
    },

    formatTime(dateString) {
      if (!dateString) return "";
      const date = new Date(dateString);
      return date.toLocaleTimeString("es-ES", {
        hour: "2-digit",
        minute: "2-digit",
      });
    },

    formatFullDate(dateString) {
      if (!dateString) return "";
      const date = new Date(dateString);
      return date.toLocaleString("es-ES", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },

    getStatusClass(status) {
      if (!status) return "default";
      const statusLower = status.toLowerCase();

      if (statusLower.includes("aprobado")) return "success";
      if (statusLower.includes("pendiente") || statusLower.includes("creado"))
        return "warning";
      if (statusLower.includes("rechazado")) return "danger";

      return "info";
    },

    async getInformes() {
      this.loading = true;
      try {
        const response = await axios.get("/ufc/informe-operativo/", {
          params: {
            page: this.currentPage,
            page_size: this.itemsPerPage,
          },
        });
        this.informes = response.data.results;
        this.totalItems = response.data.count;
      } catch (error) {
        console.error("Error al obtener los informes:", error);
        this.showErrorToast("No se pudieron cargar los informes");
      } finally {
        this.loading = false;
      }
    },

    async searchInformes() {
      this.loading = true;
      try {
        const response = await axios.get("/ufc/informe-operativo/", {
          params: {
            search: this.searchQuery,
          },
        });
        this.informes = response.data.results;
        this.totalItems = response.data.count;
      } catch (error) {
        console.error("Error al buscar informes", error);
        this.showErrorToast("Error al buscar informes");
      } finally {
        this.loading = false;
      }
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchInformes();
      }, 300);
    },

    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.getInformes();
      }
    },

    nextPage() {
      if (this.currentPage * this.itemsPerPage < this.totalItems) {
        this.currentPage++;
        this.getInformes();
      }
    },

    async viewDetails(informe) {
      this.loading = true;
      try {
        const response = await axios.get(
          `/ufc/informe-operativo/${informe.id}/`
        );
        this.currentInforme = response.data;
        this.showDetailsModal = true;
      } catch (error) {
        console.error("Error al cargar detalles:", error);
        this.showErrorToast("No se pudieron cargar los detalles completos");
      } finally {
        this.loading = false;
      }
    },

    closeDetailsModal() {
      this.showDetailsModal = false;
      this.currentInforme = {};
    },

    confirmDelete(id) {
      Swal.fire({
        title: "¿Eliminar informe?",
        text: "Esta acción no se puede deshacer",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#ff4444",
        cancelButtonColor: "#33b5e5",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
      }).then((result) => {
        if (result.isConfirmed) {
          this.deleteInforme(id);
        }
      });
    },

    async deleteInforme(id) {
      try {
        await axios.delete(`/ufc/informe-operativo/${id}/`);
        this.informes = this.informes.filter((informe) => informe.id !== id);
        this.showSuccessToast("Informe eliminado correctamente");
      } catch (error) {
        console.error("Error al eliminar el informe:", error);
        this.showErrorToast("Error al eliminar el informe");
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
  },
};
</script>

<style scoped>
/* Variables de color */
:root {
  --io-primary: #4361ee;
  --io-primary-hover: #3a56d4;
  --io-secondary: #3f37c9;
  --io-accent: #4895ef;
  --io-danger: #f72585;
  --io-success: #4cc9f0;
  --io-warning: #f8961e;
  --io-info: #4895ef;
  --io-light: #f8f9fa;
  --io-dark: #212529;
  --io-gray: #6c757d;
  --io-light-gray: #e9ecef;
  --io-border-radius: 12px;
  --io-box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  --io-transition: all 0.3s ease;
}

/* Estilos base */
.informes-operativos-container {
  padding: 2rem;
  padding-left: 10%;
  max-width: 1400px;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

/* Header */
.io-header {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  gap: 1.5rem;
}

.io-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--io-dark);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.io-title-icon {
  color: var(--io-primary);
}

.io-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

/* Buscador */
.io-search-container {
  position: relative;
  width: 280px;
}

.io-search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--io-gray);
  font-size: 1rem;
}

.io-search-input {
  width: 100%;
  padding: 0.6rem 1rem 0.6rem 2.5rem;
  border: 1px solid var(--io-light-gray);
  border-radius: var(--io-border-radius);
  font-size: 0.95rem;
  transition: var(--io-transition);
  background-color: white;
}

.io-search-input:focus {
  outline: none;
  border-color: var(--io-primary);
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.15);
}

.io-search-border {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--io-primary);
  transition: var(--io-transition);
}

.io-search-input:focus ~ .io-search-border {
  width: 100%;
}

/* Tarjeta contenedora */
.io-card {
  background: white;
  border-radius: var(--io-border-radius);
  box-shadow: var(--io-box-shadow);
  overflow: hidden;
  transition: var(--io-transition);
}

.io-card:hover {
  box-shadow: 0 10px 35px rgba(0, 0, 0, 0.12);
}

/* Tabla */
.io-table-container {
  overflow-x: auto;
  padding: 0.5rem;
}

.io-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  min-width: 1000px;
}

.io-th {
  padding: 1rem 1.2rem;
  text-align: left;
  font-weight: 600;
  color: var(--io-dark);
  background-color: #f9fafb;
  border-bottom: 2px solid var(--io-light-gray);
  position: sticky;
  top: 0;
}

.io-th-actions {
  text-align: center;
}

.io-tr {
  transition: var(--io-transition);
}

.io-tr:hover {
  background-color: rgba(67, 97, 238, 0.03);
}

.io-td {
  padding: 1rem 1.2rem;
  border-bottom: 1px solid var(--io-light-gray);
  color: var(--io-dark);
}

.io-td-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

/* Botones de acción */
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

/* Badges y estados */
.io-status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
}

.io-status-success {
  background: rgba(76, 201, 240, 0.1);
  color: #06d6a0;
  border: 1px solid rgba(6, 214, 160, 0.2);
}

.io-status-warning {
  background: rgba(248, 150, 30, 0.1);
  color: #f8961e;
  border: 1px solid rgba(248, 150, 30, 0.2);
}

.io-status-danger {
  background: rgba(247, 37, 133, 0.1);
  color: #f72585;
  border: 1px solid rgba(247, 37, 133, 0.2);
}

.io-status-info {
  background: rgba(72, 149, 239, 0.1);
  color: #4895ef;
  border: 1px solid rgba(72, 149, 239, 0.2);
}

.io-status-default {
  background: rgba(108, 117, 125, 0.1);
  color: var(--io-gray);
  border: 1px solid rgba(108, 117, 125, 0.2);
}

/* Estados de carga y vacío */
.io-loading-td,
.io-empty-td {
  padding: 3rem !important;
}

.io-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: var(--io-gray);
}

.io-spinner {
  width: 3rem;
  height: 3rem;
  border: 4px solid rgba(67, 97, 238, 0.1);
  border-top-color: var(--io-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.io-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.75rem;
  color: var(--io-gray);
}

.io-empty-state i {
  font-size: 2.5rem;
  color: var(--io-accent);
}

.io-empty-state h3 {
  color: var(--io-dark);
  margin: 0;
  font-size: 1.2rem;
}

.io-empty-state p {
  margin: 0;
  max-width: 400px;
}

/* Paginación */
.io-pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1.5rem;
  padding: 0 0.5rem;
}

.page-link {
  border-radius: var(--io-border-radius) !important;
  margin: 0 2px;
  transition: var(--io-transition);
}

.page-link:hover {
  background-color: var(--io-light-gray);
}

/* Modal mejorado */
.io-modal-overlay {
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

.io-modal {
  background: white;
  border-radius: var(--io-border-radius);
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

.io-modal-header {
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, var(--io-primary), var(--io-secondary));
  color: white;
  position: relative;
}

.io-modal-header::after {
  content: "";
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 100%;
  height: 20px;
  background: linear-gradient(to bottom, rgba(67, 97, 238, 0.2), transparent);
}

.io-modal-header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.io-modal-icon-container {
  background: rgba(255, 255, 255, 0.2);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.io-modal-icon {
  font-size: 1.5rem;
}

.io-modal h2 {
  margin: 0;
  font-size: 1.4rem;
}

.io-modal-subtitle {
  margin: 0.25rem 0 0;
  font-size: 0.9rem;
  opacity: 0.9;
  font-weight: 400;
}

.io-modal-close {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: var(--io-transition);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
}

.io-modal-close:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: rotate(90deg);
}

.io-modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  background: #f9fafb;
}

.io-detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.io-detail-card {
  background: white;
  border-radius: var(--io-border-radius);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: var(--io-transition);
  border: 1px solid var(--io-light-gray);
}

.io-detail-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.io-detail-card-header {
  padding: 1rem;
  background: linear-gradient(to right, #f8f9fa, white);
  border-bottom: 1px solid var(--io-light-gray);
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.io-detail-card-header i {
  color: var(--io-primary);
  font-size: 1.2rem;
}

.io-detail-card-header h4 {
  margin: 0;
  font-size: 1.1rem;
}

.io-detail-card-body {
  padding: 1rem;
}

.io-detail-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.io-detail-item:last-child {
  margin-bottom: 0;
}

.io-detail-label {
  font-weight: 500;
  color: var(--io-gray);
}

.io-detail-value {
  font-weight: 400;
  color: var(--io-dark);
  text-align: right;
  max-width: 60%;
  word-break: break-word;
}

.io-detail-card-full {
  grid-column: 1 / -1;
}

.io-detail-card-highlight .io-detail-value {
  color: var(--io-primary);
  font-weight: 500;
}

.io-modal-footer {
  padding: 1.25rem 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  background: white;
  border-top: 1px solid var(--io-light-gray);
}

.io-modal-btn {
  padding: 0.6rem 1.2rem;
  border-radius: var(--io-border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: var(--io-transition);
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.io-modal-btn-secondary {
  background: white;
  color: var(--io-gray);
  border: 1px solid var(--io-light-gray);
}

.io-modal-btn-secondary:hover {
  background: #f1f3f5;
  color: var(--io-dark);
}

/* Animaciones */
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
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
