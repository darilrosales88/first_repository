<template>
  <!-- El template permanece exactamente igual -->
  <div class="cargado-container">
    <!-- Header con título y acciones -->
    <div class="ps-header">
      <h1 class="ps-title">
        <i class="bi bi-train-freight-front ps-title-icon"></i>
        Vagones Cargados/Descargados
      </h1>

      <div class="ps-actions">
        <button class="btn btn-link p-0" v-if="this.estado_parte === 'Creado'">
          <router-link
            to="AdicionarVagonCargadoDescargado"
            title="Agregar nuevo vagón cargado/descargado"
          >
            <i class="bi bi-plus-circle fs-3"></i>
          </router-link>
        </button>

        <!-- Buscador moderno -->
        <div class="ps-search-container">
          <i class="bi bi-search ps-search-icon"></i>
          <input
            type="search"
            class="ps-search-input"
            placeholder="Origen, Destino, Producto, Locomotora"
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
              <th class="ps-th" style="width: 50px">No</th>
              <th class="ps-th">TEF</th>
              <th class="ps-th">Origen</th>
              <th class="ps-th">Destino</th>
              <th class="ps-th">Estado</th>
              <th class="ps-th">Productos</th>
              <th class="ps-th ps-th-actions">Acciones</th>
            </tr>
            <tr v-if="!busqueda_existente">
              <td colspan="7" class="ps-empty-td">
                <div class="ps-empty-state">
                  <i class="bi bi-exclamation-circle"></i>
                  <h3>No se encontraron resultados</h3>
                  <p>No encontramos coincidencias para "{{ searchQuery }}"</p>
                </div>
              </td>
            </tr>
          </thead>
          <tbody>
            <!-- Estado de carga -->
            <tr v-if="loading">
              <td colspan="7" class="ps-loading-td">
                <div class="ps-loading">
                  <div class="ps-spinner"></div>
                  <span>Cargando registros...</span>
                </div>
              </td>
            </tr>

            <!-- Filas de datos -->
            <tr
              v-for="(vagon, index) in cargados_descargados"
              :key="vagon.id"
              class="ps-tr"
            >
              <td class="ps-td">{{ index + 1 }}</td>
              <td class="ps-td">{{ vagon.tipo_equipo_ferroviario_name }}</td>
              <td class="ps-td">{{ vagon.origen }}</td>
              <td class="ps-td">{{ vagon.destino }}</td>
              <td class="ps-td">
                <span
                  :class="`ps-status ps-status-${getStatusClass(vagon.estado)}`"
                >
                  {{ vagon.estado }}
                </span>
              </td>
              <td class="ps-td">{{ vagon.productos_list }}</td>

              <!-- Acciones -->
              <td v-if="hasGroup('AdminUFC')" class="ps-td">
                <div class="d-flex">
                  <button
                    @click="viewDetails(vagon)"
                    class="btn btn-sm btn-outline-info me-2"
                    title="Ver detalles"
                  >
                    <i class="bi bi-eye-fill"></i>
                  </button>

                  <button
                    @click="editVagon(vagon)"
                    class="btn btn-sm btn-outline-warning me-2"
                    title="Editar"
                  >
                    <i class="bi bi-pencil-square"></i>
                  </button>
                  <button
                    @click="confirmDelete(vagon.id)"
                    class="btn btn-sm btn-outline-danger"
                    title="Eliminar"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </td>
            </tr>

            <!-- Estado vacío -->
            <tr
              v-if="
                !loading &&
                cargados_descargados.length === 0 &&
                busqueda_existente
              "
            >
              <td colspan="7" class="ps-empty-td">
                <div class="ps-empty-state">
                  <i class="bi bi-database-exclamation"></i>
                  <h3>No hay registros</h3>
                  <p>
                    No hay vagones cargados/descargados registrados actualmente
                  </p>
                  <router-link
                    to="/AdicionarVagonCargadoDescargado"
                    class="ps-empty-action"
                    v-if="!searchQuery && this.estado_parte === 'Creado'"
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

    <!-- Modal de detalles - Versión mejorada -->
    <div
      v-if="mostrarModalDetalles"
      class="ps-modal-overlay"
      @click.self="cerrarModalDetalles"
    >
      <div class="ps-modal">
        <div class="ps-modal-header">
          <div class="ps-modal-header-content">
            <div class="ps-modal-icon-container">
              <i class="bi bi-info-circle-fill ps-modal-icon"></i>
            </div>
            <div>
              <h2>Detalles del Vagón</h2>
              <p class="ps-modal-subtitle">
                Información completa del vagón cargado/descargado
              </p>
            </div>
          </div>
          <button class="ps-modal-close" @click="cerrarModalDetalles">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>

        <div class="ps-modal-body" v-if="vagonSeleccionado">
          <div class="ps-detail-grid">
            <div class="ps-detail-card">
              <div class="ps-detail-card-header">
                <i class="bi bi-tag-fill"></i>
                <h4>Información Básica</h4>
              </div>
              <div class="ps-detail-card-body">
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Tipo de Equipo:</span>
                  <span class="ps-detail-value">{{
                    vagonSeleccionado.tipo_equipo_ferroviario_name || "N/A"
                  }}</span>
                </div>

                <div class="ps-detail-item">
                  <span class="ps-detail-label">Origen:</span>
                  <span class="ps-detail-value">{{
                    vagonSeleccionado.origen || "N/A"
                  }}</span>
                </div>

                <div class="ps-detail-item">
                  <span class="ps-detail-label">Destino:</span>
                  <span class="ps-detail-value">{{
                    vagonSeleccionado.destino || "N/A"
                  }}</span>
                </div>
              </div>
            </div>

            <div class="ps-detail-card">
              <div class="ps-detail-card-header">
                <i class="bi bi-clipboard2-data-fill"></i>
                <h4>Estado y Fecha</h4>
              </div>
              <div class="ps-detail-card-body">
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Estado:</span>
                  <span class="ps-detail-value">
                    <span
                      :class="`ps-status ps-status-${getStatusClass(
                        vagonSeleccionado.estado
                      )}`"
                    >
                      {{ vagonSeleccionado.estado || "N/A" }}
                    </span>
                  </span>
                </div>

                <div class="ps-detail-item">
                  <span class="ps-detail-label">Fecha:</span>
                  <span class="ps-detail-value">{{
                    vagonSeleccionado.fecha || "N/A"
                  }}</span>
                </div>
              </div>
            </div>

            <div class="ps-detail-card ps-detail-card-highlight">
              <div class="ps-detail-card-header">
                <i class="bi bi-box-seam-fill"></i>
                <h4>Productos</h4>
              </div>
              <div class="ps-detail-card-body">
                <div class="ps-detail-item">
                  <span class="ps-detail-value">
                    <span v-if="vagonSeleccionado.productos_list">
                      {{ vagonSeleccionado.productos_list }}
                    </span>
                    <span v-else>N/A</span>
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
                    vagonSeleccionado.observaciones ||
                    "Ninguna observación registrada"
                  }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="ps-modal-footer">
          <button
            class="ps-modal-btn ps-modal-btn-secondary"
            @click="cerrarModalDetalles"
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
  name: "CargadosDescargados",

  data() {
    return {
      cargados_descargados: [], // Lista de vagones
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
      mostrarModalDetalles: false,
      vagonSeleccionado: null,
      estado_parte: "",
    };
  },

  props: {
    informeId: {
      type: [String, Number],
      required: true,
    },
  },

  async mounted() {
    await this.getVagonesCargadosDescargados();
    await this.fetchUserPermissionsAndGroups();
  },

  methods: {
    hasGroup(group) {
      return this.userGroups.some((g) => g.name === group);
    },

    viewDetails(vagon) {
      this.vagonSeleccionado = vagon;
      this.mostrarModalDetalles = true;
    },

    cerrarModalDetalles() {
      this.mostrarModalDetalles = false;
      this.vagonSeleccionado = null;
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

    async getVagonesCargadosDescargados() {
      this.loading = true;
      try {
        const today = new Date();
        const fechaFormateada = `${today.getFullYear()}-${String(
          today.getMonth() + 1
        ).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;
        const infoID = await axios.get(
          `/ufc/verificar-informe-existente/?fecha_operacion=${fechaFormateada}`
        );
        this.estado_parte = infoID.data.estado;
        if (infoID.data.existe) {
          //Para la reutilizacion del componente se deberia usar el operador ternario en informe: props.informeId? props.informeId: infoID.data.id
          const response = await axios.get(
            "/ufc/vagones-cargados-descargados/",
            {
              params: {
                page: this.currentPage,
                page_size: this.itemsPerPage,
                informe: infoID.data.id,
              },
            }
          );

          this.cargados_descargados = response.data.results;
          this.allRecords = [...response.data.results]; // Guardar copia completa para filtrado
          this.totalItems = response.data.count;
          this.busqueda_existente = true;
        }
      } catch (error) {
        console.error(
          "Error al obtener los vagones cargados/descargados:",
          error
        );
        this.busqueda_existente = false;
      } finally {
        this.loading = false;
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

    // Nuevo método de búsqueda adaptado del componente que funciona
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        if (!this.searchQuery.trim()) {
          this.cargados_descargados = [...this.allRecords];
          this.busqueda_existente = true;
          return;
        }

        const query = this.searchQuery.toLowerCase();
        this.cargados_descargados = this.allRecords.filter((item) => {
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

        this.busqueda_existente = this.cargados_descargados.length > 0;
      }, 300);
    },

    // Métodos de paginación
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.getVagonesCargadosDescargados();
      }
    },

    nextPage() {
      if (this.currentPage * this.itemsPerPage < this.totalItems) {
        this.currentPage++;
        this.getVagonesCargadosDescargados();
      }
    },

    goToPage(page) {
      this.currentPage = page;
      this.getVagonesCargadosDescargados();
    },

    async delete_vagon(id) {
      try {
        console.log("muestrae el id: ", id);
        const response = await axios.delete(
          `/ufc/vagones-cargados-descargados/${id}/`
        );

        if (response.status === 204) {
          // Normalmente DELETE devuelve 204 No Content
          this.cargados_descargados = this.cargados_descargados.filter(
            (objeto) => objeto.id !== id
          );
          Swal.fire("Eliminado!", "El vagón ha sido eliminado.", "success");
        } else {
          throw new Error(`Respuesta inesperada: ${response.status}`);
        }
      } catch (error) {
        console.error("Error completo:", error);
        console.error("Respuesta del servidor:", error.response?.data);

        Swal.fire(
          "Error",
          error.response?.data?.message || "Error al eliminar el vagón",
          "error"
        );
      }
      window.location.reload();
    },

    cerrarModal() {
      this.mostrarModal = false;
    },

    editVagon(vagon) {
      // Aquí puedes implementar la navegación a la página de edición
      this.$router.push({
        name: "EditarCargadoDescargado",
        params: { id: vagon.id },
      });
    },

    confirmDelete(id) {
      Swal.fire({
        title: "¿Estás seguro?",
        text: "¡No podrás revertir esta acción!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
        reverseButtons: true,
      }).then((result) => {
        if (result.isConfirmed) {
          this.delete_vagon(id);
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
  },
};
</script>

<style scoped>
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
.cargado-container {
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

/* Botones de acción */
.btn-small {
  font-size: 22px;
  color: black;
  margin-right: 5px;
  outline: none;
  border: none;
  background: none;
  padding: 0;
}

.btn-eye {
  font-size: 22px;
  margin-right: 5px;
  outline: none;
  border: none;
  background: none;
  padding: 0;
}

.btn:hover {
  scale: 1.1;
}

.btn:focus {
  outline: none;
  box-shadow: none;
}

/* Badges y estados */
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

/* Paginación */
.ps-pagination {
  margin-top: 1.5rem;
  padding: 0.5rem;
}

.ps-pagination-info {
  font-size: 0.9rem;
  color: var(--ps-gray);
}

.ps-pagination-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px !important;
  transition: var(--ps-transition);
}

.ps-pagination-btn:hover {
  background: var(--ps-light-gray);
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
  .cargado-container {
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
