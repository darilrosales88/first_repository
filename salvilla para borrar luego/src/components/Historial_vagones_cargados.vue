<template>
  <div class="cargado-container">
    <!-- Header con título -->
    <div class="ps-header">
      <h1 class="ps-title">
        <i class="bi bi-clock-history ps-title-icon"></i>
        Historial Completo de Vagones Cargados/Descargados
      </h1>
    </div>

    <!-- Selector de parte operativo -->
    <div class="ps-card mb-3">
      <div class="ps-select-container">
        <label for="parte-operativo" class="ps-select-label">
          <i class="bi bi-card-checklist"></i> Seleccionar Parte Operativo
        </label>
        <select 
          id="parte-operativo" 
          class="ps-select" 
          v-model="parteSeleccionado"
          @change="cargarHistorial"
        >
          <option value="">-- Seleccione un parte --</option>
          <option 
            v-for="parte in partesOperativos" 
            :key="parte.id" 
            :value="parte.id"
          >
            {{ formatFecha(parte.fecha_operacion) }} - {{ parte.estado_parte }}
          </option>
        </select>
      </div>
    </div>

    <!-- Tarjeta contenedora de la tabla -->
    <div class="ps-card" v-if="parteSeleccionado">
      <div class="ps-table-container">
        <table class="ps-table">
          <thead>
            <tr>
              <th class="ps-th">No</th>
              <th class="ps-th">Fecha Creación</th>
              <th class="ps-th">Tipo Equipo</th>
              <th class="ps-th">Origen</th>
              <th class="ps-th">Destino</th>
              <th class="ps-th">Operación</th>
              <th class="ps-th">Estado</th>
              <th class="ps-th ps-th-actions">Acciones</th>
            </tr>
            <tr v-if="!loading && historialVagones.length === 0">
              <td colspan="8" class="ps-empty-td">
                <div class="ps-empty-state">
                  <i class="bi bi-database-exclamation"></i>
                  <h3>No hay registros de historial</h3>
                  <p>No se encontraron vagones para el parte operativo seleccionado</p>
                </div>
              </td>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="8" class="ps-loading-td">
                <div class="ps-loading">
                  <div class="ps-spinner"></div>
                  <span>Cargando historial...</span>
                </div>
              </td>
            </tr>

            <tr
              v-for="(historial, index) in historialVagones"
              :key="historial.id"
              class="ps-tr"
            >
              <td class="ps-td">{{ index + 1 }}</td>
              <td class="ps-td">{{ formatFecha(historial.fecha_creacion) }}</td>
              <td class="ps-td">{{ historial.datos_vagon.tipo_equipo_ferroviario_name }}</td>
              <td class="ps-td">{{ historial.datos_vagon.origen }}</td>
              <td class="ps-td">{{ historial.datos_vagon.destino }}</td>
              <td class="ps-td">{{ historial.datos_vagon.operacion }}</td>
              <td class="ps-td">
                <span :class="`ps-status ps-status-${getStatusClass(historial.datos_vagon.estado)}`">
                  {{ historial.datos_vagon.estado }}
                </span>
              </td>
              <td class="ps-td">
                <button
                  @click="verDetalles(historial)"
                  class="btn btn-sm btn-outline-info"
                  title="Ver detalles completos"
                >
                  <i class="bi bi-eye-fill"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Mensaje cuando no hay parte seleccionado -->
    <div class="ps-card" v-if="!parteSeleccionado">
      <div class="ps-empty-state">
        <i class="bi bi-card-checklist"></i>
        <h3>Seleccione un parte operativo</h3>
        <p>Por favor, seleccione un parte operativo de la lista para visualizar su historial de vagones</p>
      </div>
    </div>

    <!-- Modal de detalles completos -->
    <div
      v-if="mostrarModalDetalles && vagonSeleccionado"
      class="ps-modal-overlay"
      @click.self="cerrarModalDetalles"
    >
      <div class="ps-modal" style="max-width: 900px;">
        <div class="ps-modal-header">
          <div class="ps-modal-header-content">
            <div class="ps-modal-icon-container">
              <i class="bi bi-info-circle-fill ps-modal-icon"></i>
            </div>
            <div>
              <h2>Detalles Completos del Vagón</h2>
              <p class="ps-modal-subtitle">
                Información completa del vagón cargado/descargado
              </p>
            </div>
          </div>
          <button class="ps-modal-close" @click="cerrarModalDetalles">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>

        <div class="ps-modal-body">
          <div class="ps-detail-grid">
            <!-- Información básica -->
            <div class="ps-detail-card">
              <div class="ps-detail-card-header">
                <i class="bi bi-tag-fill"></i>
                <h4>Información Básica</h4>
              </div>
              <div class="ps-detail-card-body">
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Tipo de Equipo:</span>
                  <span class="ps-detail-value">{{ vagonSeleccionado.datos_vagon.tipo_equipo_ferroviario_name || "N/A" }}</span>
                </div>
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Origen:</span>
                  <span class="ps-detail-value">{{ vagonSeleccionado.datos_vagon.origen || "N/A" }}</span>
                </div>
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Destino:</span>
                  <span class="ps-detail-value">{{ vagonSeleccionado.datos_vagon.destino || "N/A" }}</span>
                </div>
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Operación:</span>
                  <span class="ps-detail-value">{{ vagonSeleccionado.datos_vagon.operacion || "N/A" }}</span>
                </div>
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Fecha:</span>
                  <span class="ps-detail-value">{{ formatFecha(vagonSeleccionado.datos_vagon.fecha) || "N/A" }}</span>
                </div>
              </div>
            </div>

            <!-- Estado y métricas -->
            <div class="ps-detail-card">
              <div class="ps-detail-card-header">
                <i class="bi bi-clipboard2-data-fill"></i>
                <h4>Estado y Métricas</h4>
              </div>
              <div class="ps-detail-card-body">
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Estado:</span>
                  <span class="ps-detail-value">
                    <span :class="`ps-status ps-status-${getStatusClass(vagonSeleccionado.datos_vagon.estado)}`">
                      {{ vagonSeleccionado.datos_vagon.estado || "N/A" }}
                    </span>
                  </span>
                </div>
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Plan Diario:</span>
                  <span class="ps-detail-value">{{ vagonSeleccionado.datos_vagon.plan_diario_carga_descarga || "N/A" }}</span>
                </div>
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Real:</span>
                  <span class="ps-detail-value">{{ vagonSeleccionado.datos_vagon.real_carga_descarga || "N/A" }}</span>
                </div>
                <div class="ps-detail-item">
                  <span class="ps-detail-label">Causas Incumplimiento:</span>
                  <span class="ps-detail-value">{{ vagonSeleccionado.datos_vagon.causas_incumplimiento || "Ninguna" }}</span>
                </div>
              </div>
            </div>

            <!-- Productos -->
            <div class="ps-detail-card ps-detail-card-full">
              <div class="ps-detail-card-header">
                <i class="bi bi-box-seam-fill"></i>
                <h4>Productos ({{ vagonSeleccionado.datos_productos.length }})</h4>
              </div>
              <div class="ps-detail-card-body">
                <div class="ps-table-container">
                  <table class="ps-table">
                    <thead>
                      <tr>
                        <th class="ps-th">Producto</th>
                        <th class="ps-th">Tipo Embalaje</th>
                        <th class="ps-th">Cantidad</th>
                        <th class="ps-th">Unidad</th>
                        <th class="ps-th">Estado</th>
                        <th class="ps-th">Contiene</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(producto, idx) in vagonSeleccionado.datos_productos" :key="idx" class="ps-tr">
                        <td class="ps-td">{{ producto.producto_name }}</td>
                        <td class="ps-td">{{ producto.tipo_embalaje_name || "N/A" }}</td>
                        <td class="ps-td">{{ producto.cantidad }}</td>
                        <td class="ps-td">{{ producto.unidad_medida_simbolo || "N/A" }}</td>
                        <td class="ps-td">{{ producto.estado }}</td>
                        <td class="ps-td">{{ producto.contiene || "N/A" }}</td>
                      </tr>
                      <tr v-if="vagonSeleccionado.datos_productos.length === 0" class="ps-tr">
                        <td colspan="6" class="ps-td text-center">No hay productos registrados</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <!-- Registros de Vagones -->
            <div class="ps-detail-card ps-detail-card-full" v-if="vagonSeleccionado.datos_registros_vagones.length > 0">
              <div class="ps-detail-card-header">
                <i class="bi bi-train-freight-front"></i>
                <h4>Registros de Vagones ({{ vagonSeleccionado.datos_registros_vagones.length }})</h4>
              </div>
              <div class="ps-detail-card-body">
                <div class="ps-table-container">
                  <table class="ps-table">
                    <thead>
                      <tr>
                        <th class="ps-th">No. Identificación</th>
                        <th class="ps-th">Fecha Despacho</th>
                        <th class="ps-th">Origen</th>
                        <th class="ps-th">Fecha Llegada</th>
                        <th class="ps-th">Observaciones</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(registro, idx) in vagonSeleccionado.datos_registros_vagones" :key="idx" class="ps-tr">
                        <td class="ps-td">{{ registro.no_id }}</td>
                        <td class="ps-td">{{ registro.fecha_despacho ? formatFecha(registro.fecha_despacho) : 'N/A' }}</td>
                        <td class="ps-td">{{ registro.origen }}</td>
                        <td class="ps-td">{{ registro.fecha_llegada ? formatFecha(registro.fecha_llegada) : 'N/A' }}</td>
                        <td class="ps-td">{{ registro.observaciones || 'Ninguna' }}</td>
                      </tr>
                    </tbody>
                  </table>
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
  name: "HistorialVagonesCompleto",

  data() {
    return {
      partesOperativos: [],
      historialVagones: [],
      parteSeleccionado: "",
      loading: false,
      mostrarModalDetalles: false,
      vagonSeleccionado: null,
    };
  },

  async mounted() {
    await this.cargarPartesOperativos();
  },

  methods: {
    formatFecha(fechaString) {
      if (!fechaString) return "N/A";
      const fecha = new Date(fechaString);
      return fecha.toLocaleDateString("es-ES", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },

    async cargarPartesOperativos() {
      this.loading = true;
      try {
        const response = await axios.get("/ufc/informe-operativo/");
        this.partesOperativos = response.data.results || response.data;
      } catch (error) {
        console.error("Error al cargar partes operativos:", error);
        Swal.fire(
          "Error",
          "No se pudieron cargar los partes operativos",
          "error"
        );
      } finally {
        this.loading = false;
      }
    },

    async cargarHistorial() {
      if (!this.parteSeleccionado) {
        this.historialVagones = [];
        return;
      }

      this.loading = true;
      try {
        const response = await axios.get("/ufc/historial-vagones-cargados/", {
          params: {
            informe_id: this.parteSeleccionado
          }
        });
        
        this.historialVagones = response.data.results || response.data;
      } catch (error) {
        console.error("Error al cargar el historial:", error);
        Swal.fire(
          "Error",
          "No se pudo cargar el historial de vagones",
          "error"
        );
      } finally {
        this.loading = false;
      }
    },

    verDetalles(historial) {
      this.vagonSeleccionado = historial;
      this.mostrarModalDetalles = true;
    },

    cerrarModalDetalles() {
      this.mostrarModalDetalles = false;
      this.vagonSeleccionado = null;
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

/* Selector */
.ps-select-container {
  padding: 1rem;
}

.ps-select-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--ps-dark);
}

.ps-select-label i {
  color: var(--ps-primary);
  font-size: 1.1rem;
}

.ps-select {
  width: 100%;
  padding: 0.6rem 1rem;
  border: 1px solid var(--ps-light-gray);
  border-radius: var(--ps-border-radius);
  font-size: 0.95rem;
  transition: var(--ps-transition);
  background-color: white;
}

.ps-select:focus {
  outline: none;
  border-color: var(--ps-primary);
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.15);
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