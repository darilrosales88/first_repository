<template>
  <div class="container py-3">
    <h4>Vagones Cargados/descargados</h4>
    <!-- Encabezado con acciones -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <!-- Botón de agregar - más destacado -->
      <button class="btn btn-link p-0" @click="showModal = true">
        <router-link
          v-if="hasGroup('AdminUFC')"
          to="AdicionarVagonCargadoDescargado"
          title="Agregar nuevo vagón cargado/descargado"
        >
          <i class="bi bi-plus-circle fs-3"></i>
        </router-link>
        <!-- Icono grande -->
      </button>

      <form @submit.prevent="search_producto" class="search-container">
        <div class="input-group">
          <input
            type="search"
            class="form-control"
            placeholder="Origen, Destino, Producto, Locomotora"
            v-model="searchQuery"
            @input="handleSearchInput"
          />
          <span
            class="position-absolute top-50 start-0 translate-middle-y ps-2"
          >
            <i class="bi bi-search"></i>
          </span>
        </div>
      </form>
    </div>

    <!-- Tabla responsive con mejoras -->
    <div class="table table-responsive">
      <table class="table table-hover mb-0">
        <thead>
          <tr>
            <th scope="col" style="width: 50px">No</th>
            <th scope="col">TEF</th>
            <th scope="col">Origen</th>
            <th scope="col">Destino</th>
            <th scope="col">Estado</th>
            <th scope="col">Productos</th>
            <th scope="col">Acciones</th>
          </tr>
          <tr v-if="!busqueda_existente">
            <td colspan="8" class="text-center text-muted py-4">
              <i class="bi bi-exclamation-circle fs-4"></i>
              <p class="mt-2">
                No se encontraron resultados para "{{ searchQuery }}"
              </p>
            </td>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(vagon, index) in cargados_descargados"
            :key="vagon.id"
            class="align-middle"
          >
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ vagon.tipo_equipo_ferroviario_name }}</td>
            <td>{{ vagon.origen }}</td>
            <td>
              <span>
                {{ vagon.destino }}
              </span>
            </td>
            <td>{{ vagon.estado }}</td>
            <td>{{ vagon.productos_list }}</td>
            <td v-if="hasGroup('AdminUFC')">
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
        </tbody>
      </table>
    </div>
    <!-- Modal de detalles -->
    <div v-if="mostrarModalDetalles" class="modal-backdrop">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Detalles del Vagón Cargado/Descargado</h5>
          <button @click="cerrarModalDetalles" class="btn-close">
            <i class="bi bi-x"></i>
          </button>
        </div>
        <div class="modal-body" v-if="vagonSeleccionado">
          <!-- Información básica -->
          <div class="row mb-3">
            <div class="col-md-6">
              <p>
                <strong>Tipo de equipo ferroviario:</strong>
                {{ vagonSeleccionado.tipo_equipo_ferroviario_name || "N/A" }}
              </p>
              <p>
                <strong>Origen:</strong> {{ vagonSeleccionado.origen || "N/A" }}
              </p>
              <p>
                <strong>Destino:</strong>
                {{ vagonSeleccionado.destino || "N/A" }}
              </p>
            </div>
            <div class="col-md-6">
              <p>
                <strong>Estado:</strong> {{ vagonSeleccionado.estado || "N/A" }}
              </p>
              <p>
                <strong>Fecha:</strong> {{ vagonSeleccionado.fecha || "N/A" }}
              </p>
            </div>
          </div>

          <!-- Productos asociados -->
          <div class="mb-3">
            <h6 class="border-bottom pb-2">Productos asociados</h6>
            <div
              v-if="
                vagonSeleccionado.productos_list &&
                vagonSeleccionado.productos_list.length > 0
              "
            >
              <p>{{ vagonSeleccionado.productos_list }}</p>
            </div>
            <div v-else>
              <p class="text-muted">No hay productos asociados</p>
            </div>
          </div>

          <!-- Observaciones -->
          <div class="mb-3">
            <h6 class="border-bottom pb-2">Observaciones</h6>
            <p v-if="vagonSeleccionado.observaciones">
              {{ vagonSeleccionado.observaciones }}
            </p>
            <p v-else class="text-muted">No hay observaciones registradas</p>
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
    <!-- Termina la paginacion -->
  </div>
</template>

<style scoped>
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
</style>
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
    };
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
        const response = await axios.get("/ufc/vagones-cargados-descargados/", {
          params: {
            page: this.currentPage,
            page_size: this.itemsPerPage,
          },
        });

        this.cargados_descargados = response.data.results;
        this.allRecords = [...response.data.results]; // Guardar copia completa para filtrado
        this.totalItems = response.data.count;
        this.busqueda_existente = true;
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
  },
};
</script>

<style scoped>
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

/* Estilos para el modal */
.modal-backdrop {
  top: 0;
  left: 0;
  width: 100%;
  height: 90%;
  background-color: transparent; /* Fondo semitransparente */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* Asegura que el modal esté por encima de todo */
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  width: 90%;
  max-width: 500px; /* Ancho máximo del modal */
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.modal-title {
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
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
</style>
