<template>
  <div class="container py-3">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h6 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-clipboard-data me-2"></i>Vagones Cargados/descargados
        </h6>
      </div>
      <div class="card-body p-3">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <router-link
            v-if="hasGroup('AdminUFC') && this.habilitado"
            to="AdicionarVagonCargadoDescargado">
            <button class="btn btn-sm btn-primary">
              <i class="bi bi-plus-circle me-1"></i>Agregar nuevo vagón
              cargado/descargado
            </button>
          </router-link>
          <form @submit.prevent="search_producto" class="search-container">
            <div class="input-group">
              <input
                type="search"
                class="form-control"
                placeholder="Buscar en registros"
                v-model="searchQuery"
                @input="handleSearchInput"
              />
              <span class="position-absolute top-50 start-0 translate-middle-y ps-2">
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
                <th scope="col">TEF</th>
                <th scope="col">Origen</th>
                <th scope="col">Destino</th>
                <th scope="col">Estado</th>
                <th scope="col">Productos</th>
                <th scope="col">Acciones</th>
              </tr>
              <tr v-if="!busqueda_existente && cargados_descargados.length != 0">
                <td colspan="8" class="text-center text-muted py-4">
                  <i class="bi bi-exclamation-circle fs-4"></i>
                  <p class="mt-2">
                    No se encontraron resultados para "{{ searchQuery }}"
                  </p>
                </td>
              </tr>
              <tr v-if="cargados_descargados.length == 0">
                <td colspan="8" class="text-center text-muted py-4">
                  <div class="ps-loading" v-if="loading">
                    <div class="ps-spinner"></div>
                    <span>Cargando registros...</span>
                  </div>
                  <div v-else>
                    <i class="bi bi-database-exclamation fs-4"></i>
                    <p class="mt-2">
                      No hay registros
                    </p>
                  </div>
                </td>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(vagon, index) in cargados_descargados" :key="vagon.id" class="align-middle">
                <th scope="row">{{ index + 1 }}</th>
                <td>{{ vagon.tipo_equipo_ferroviario_name }}</td>
                <td>{{ vagon.origen }}</td>
                <td>
                  <span>
                    {{ vagon.destino }}
                  </span>
                </td>
                <td>
                  <span
                    :class="`ps-status ps-status-${getStatusClass(
                      vagon.estado
                    )}`">
                    {{ vagon.estado }}
                  </span>
                </td>
                <td>{{ vagon.productos_list }}</td>
                <td v-if="hasGroup('AdminUFC')">
                  <div class="d-flex">
                    <button
                      @click="viewDetails(vagon)"
                      class="btn btn-sm btn-outline-info me-2"
                      title="Ver detalles">
                      <i class="bi bi-eye-fill"></i>
                    </button>

                    <button v-if="this.habilitado"
                      @click="editVagon(vagon)"
                      class="btn btn-sm btn-outline-warning me-2"
                      title="Editar">
                      <i class="bi bi-pencil-square"></i>
                    </button>

                    <button v-if="this.habilitado"
                      @click="confirmDelete(vagon.id)"
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

        <!-- Modal de detalles -->
        <div
          v-if="mostrarModalDetalles"
          class="ps-modal-overlay"
          @click.self="cerrarModalDetalles()"
        >
          <!-- Modal -->
          <div class="ps-modal">
            <!-- 1. Encabezado del Modal -->
            <div class="ps-modal-header">
              <div class="ps-modal-header-content">
                <div class="ps-modal-icon-container">
                  <i class="bi bi-info-circle-fill ps-modal-icon"></i>
                </div>
                <div>
                  <h2>Detalles del Registro</h2>
                  <p class="ps-modal-subtitle">
                    Información completa del registro situado
                  </p>
                </div>
              </div>
              <button class="ps-modal-close" @click="cerrarModalDetalles()">
                <i class="bi bi-x-lg"></i>
              </button>
            </div>

            <!-- 2. Cuerpo del Modal -->
            <div class="ps-modal-body">
              <div class="ps-detail-grid">
                <!-- 2.1 Tarjeta - Información Básica -->
                <div class="ps-detail-card">
                  <div class="ps-detail-card-header">
                    <i class="bi bi-tag-fill"></i>
                    <h4>Información Básica</h4>
                  </div>
                  <div class="ps-detail-card-body">
                    <!-- 2.1.2 Item - Origen -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Tipo Origen:</span>
                      <span class="ps-detail-value">
                        {{ vagonSeleccionado.tipo_origen_name || "N/A" }}
                      </span>
                    </div>

                    <!-- 2.1.2 Item - Origen -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Origen:</span>
                      <span class="ps-detail-value">
                        {{ vagonSeleccionado.origen || "N/A" }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- 2.2 Tarjeta - Estado,Operación y Producto -->
                <div class="ps-detail-card">
                  <div class="ps-detail-card-header">
                    <i class="bi bi-clipboard2-data-fill"></i>
                    <h4>Estado,Operación y Producto</h4>
                  </div>
                  <div class="ps-detail-card-body">
                    <!-- 2.2.1 Item - Estado -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Estado:</span>
                      <span class="ps-detail-value">
                        <span
                          :class="`ps-status ps-status-${getStatusClass(
                            vagonSeleccionado.estado
                          )}`">
                          {{ vagonSeleccionado.estado || "N/A" }}
                        </span>
                      </span>
                    </div>

                    <!-- 2.2.2 Item - Operación -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Operación:</span>
                      <span class="ps-detail-value">
                        {{ vagonSeleccionado.operacion || "N/A" }}
                      </span>
                    </div>

                    <!-- 2.2.3 Item - Productos (lista) -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Productos:</span>
                      <span class="ps-detail-value">
                        <template v-if="stringArray && stringArray.length > 0">
                          <div
                            v-for="producto in stringArray"
                            class="producto-item"
                          >
                            • {{ producto }}
                          </div>
                        </template>
                        <span v-else>N/A</span>
                      </span>
                    </div>
                  </div>
                </div>

                <!-- 2.3 Tarjeta - Cantidades (destacada) -->
                <div class="ps-detail-card">
                  <div class="ps-detail-card-header">
                    <i class="bi bi-check-circle-fill"></i>
                    <h4>Cantidades</h4>
                  </div>
                  <div class="ps-detail-card-body">
                    <!-- 2.3.1 Item - Vagones -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Real Carga/Descarga:</span>
                      <span
                        class="ps-detail-value ps-highlight-value ps-badge-success"
                      >
                        {{ vagonSeleccionado.real_carga_descarga || "0" }}
                      </span>
                    </div>
                  </div>
                </div>
                <div class="ps-detail-card">
                  <div class="ps-detail-card-header">
                    <i class="bi bi-geo-alt-fill"></i>
                    <h4>Destinos</h4>
                  </div>
                  <div class="ps-detail-card-body">
                    <!-- 2.4.1 Item - Tipo Destino -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Tipo Destino:</span>
                      <span class="ps-detail-value">
                        {{
                          getTipoOrigenText(vagonSeleccionado.tipo_destino) ||
                          "N/A"
                        }}
                      </span>
                    </div>
                  </div>

                  <!-- 2.4.2 Item - Destino -->
                  <div class="ps-detail-item">
                    <span class="ps-detail-label">Destino:</span>
                    <span class="ps-detail-value">
                      {{ vagonSeleccionado.destino || "N/A" }}
                    </span>
                  </div>
                </div>

                <!-- 2.4 Tarjeta - Causas del Incumplimiento (ancho completo) -->
                <div class="ps-detail-card ps-detail-card-full">
                  <div class="ps-detail-card-header">
                    <i class="bi bi-chat-square-text-fill"></i>
                    <h4>Causas de Incumplimiento</h4>
                  </div>
                  <div class="ps-detail-card-body">
                    <!-- 2.4.1 Item - Observaciones -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-value">
                        {{
                          vagonSeleccionado.causas_incumplimiento ||
                          "Ninguna causa de incumplimiento registrada"
                        }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- 2.5 Tarjeta - Fecha de Creación -->
                <div class="ps-detail-card">
                  <div class="ps-detail-card-header">
                    <i class="bi bi-calendar-event-fill"></i>
                    <h4>Fecha de Creación</h4>
                  </div>
                  <div class="ps-detail-card-body">
                    <!-- 2.5.1 Item - Fecha y Hora -->
                    <div class="ps-detail-item">
                      <span class="ps-detail-label">Fecha y Hora:</span>
                      <span class="ps-detail-value">
                        {{ vagonSeleccionado.fecha_registro }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Paginación mejorada -->
        <div class="d-flex justify-content-between align-items-center">
          <div class="text-muted small">
            Mostrando {{ cargados_descargados.length }} de
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
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "CargadosDescargados",
  props: {
    informeID: {
      type: Number,
      required: false,
    },
  },
  data() {
    return {
      cargados_descargados: [], // Lista de vagones
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
      stringArray: [],
      charArray: [],
      vagonSeleccionado: null,
      tipo_origen_options: [
        { id: "puerto", text: "Puerto" },
        { id: "ac_ccd", text: "Acceso Comercial/CCD" },
      ],
    };
  },

  async mounted() {
    await this.getVagonesCargadosDescargados();
    await this.fetchUserPermissionsAndGroups();
  },

  methods: {
    getTipoOrigenText(id) {
      const option = this.tipo_origen_options.find((o) => o.id === id);
      return option ? option.text : id;
    },

    getStatusClass(status) {
      if (!status) return "default";
      const statusLower = status.toLowerCase();
      if (statusLower.includes("cargado")) return "success";
      if (statusLower.includes("vacio")) return "danger";
      return "info";
    },

    hasGroup(group) {
      return this.userGroups.some((g) => g.name === group);
    },

    viewDetails(vagon) {
      this.vagonSeleccionado = vagon;
      console.log(this.vagonSeleccionado);
      this.convertCharsToStrings(this.vagonSeleccionado);
      this.mostrarModalDetalles = true;
    },

    cerrarModalDetalles() {
      this.mostrarModalDetalles = false;
      this.vagonSeleccionado = null;
    },

    convertCharsToStrings(item) {
      // Convertir el string en arreglo de caracteres, manteniendo espacios
      this.charArray = item.productos_list.split("");

      let currentWord = "";
      this.stringArray = [];

      for (const char of this.charArray) {
        if (char === ",") {
          // Al encontrar coma, guardar la palabra actual (incluso si está vacía)
          this.stringArray.push(currentWord);
          currentWord = "";
        } else {
          // Agregar el carácter a la palabra actual (incluyendo espacios)
          currentWord += char;
        }
      }

      // Añadir la última palabra si existe (puede ser vacía)
      if (
        currentWord !== "" ||
        this.charArray[this.charArray.length - 1] === ","
      ) {
        this.stringArray.push(currentWord);
      }

      // Opcional: eliminar espacios en blanco al inicio/final de cada palabra
      this.stringArray = this.stringArray.map((word) => word.trim());

      // Opcional: filtrar palabras vacías si no se desean
      // this.stringArray = this.stringArray.filter(word => word !== '');
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

        //Para la reutilizacion del componente se deberia usar el operador ternario en informe: props.informeId? props.informeId: infoID.data.id
        if (this.informeID || infoID.data.id) {
          const response = await axios.get(
            "/ufc/vagones-cargados-descargados/",
            {
              params: {
                page: this.currentPage,
                page_size: this.itemsPerPage,
                informe: this.informeID ? this.informeID : infoID.data.id,
              },
            }
          );

          if(this.informeID){
            this.habilitado = false;
          }

          this.cargados_descargados = response.data.results;
          this.allRecords = [...response.data.results]; // Guardar copia completa para filtrado
          this.totalItems = response.data.count;
          this.busqueda_existente = true;
        } else {
          this.showErrorToast("No hay ID para cargar");
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

    async delete_tren(id) {
      try {
        await axios.delete(`/ufc/vagones-cargados-descargados/${id}/`);
        this.cargados_descargados = this.cargados_descargados.filter(
          (objeto) => objeto.id !== id
        );
        Swal.fire(
          "Eliminado!",
          "El producto ha sido eliminado exitosamente.",
          "success"
        );
      } catch (error) {
        console.error("Error al eliminar el producto:", error);
        Swal.fire("Error", "Hubo un error al eliminar el producto.", "error");
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
          this.delete_tren(id); // 'this' se mantiene correctamente
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

.modal-body {
  margin-bottom: 20px;
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

.btn-outline-info {
  color: #17a2b8;
  border-color: #17a2b8;
}

.btn-outline-warning {
  color: #ffc107;
  border-color: #ffc107;
}

.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
}

.btn-outline-info:hover,
.btn-outline-warning:hover,
.btn-outline-danger:hover {
  color: #fff;
}

/* Responsive */
@media (max-width: 768px) {
  .card-body {
    padding: 1rem;
  }

  .btn {
    width: 100%;
  }

  .d-flex {
    flex-direction: column;
    gap: 0.5rem !important;
  }
}
</style>
