<template>
  <div class="container py-3">
    <!-- Encabezado con acciones -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <!-- Botón de agregar - más destacado -->

      <button class="btn btn-link p-0" @click="showModal = true">
        <router-link
          v-if="hasPermission"
          to="AdicionarVagon"
          title="Agregar nuevo vagón"
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
            <th scope="col" style="width: 50px">#</th>
            <th scope="col">Código Locomotora</th>
            <th scope="col">Tipo</th>
            <th scope="col">Estado</th>
            <th scope="col">Producto</th>
            <th scope="col" class="text-end">Cant. Vagones</th>
            <th scope="col">Origen</th>
            <th scope="col">Destino</th>
            <th scope="col" v-if="showNoId">Descripción</th>
            <th scope="col" v-if="hasPermission" style="width: 120px">
              Acciones
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(tren, index) in en_trenes"
            :key="tren.id"
            class="align-middle"
          >
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ tren.numero_identificacion_locomotora || "-" }}</td>
            <td>{{ tren.tipo_equipo || "-" }}</td>
            <td>
              <span>
                {{ tren.estado || "-" }}
              </span>
            </td>
            <td>{{ tren.producto_name || "-" }}</td>
            <td class="text-end">{{ tren.cantidad_vagones || "0" }}</td>
            <td>{{ tren.origen || "-" }}</td>
            <td>{{ tren.destino || "-" }}</td>
            <td v-if="showNoId">{{ tren.descripcion || "-" }}</td>
            <td v-if="hasPermission">
              <div class="d-flex">
                <button
                  @click="openVagonDetailsModal(tren)"
                  class="btn btn-sm btn-outline-info me-2"
                  :title="showNoId ? 'Ocultar detalles' : 'Ver detalles'"
                >
                  <i
                    :class="
                      showNoId ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill'
                    "
                  ></i>
                </button>
                <router-link
                  :to="{ name: 'EditarEnTren', params: { id: tren.id } }"
                  class="btn btn-sm btn-outline-warning me-2"
                  title="Editar"
                >
                  <i class="bi bi-pencil-square"></i>
                </router-link>
                <button
                  @click.prevent="confirmDelete(tren.id)"
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

    <!-- Paginación mejorada -->
    <div class="d-flex justify-content-between align-items-center">
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

    <!-- Modal para detalles -->
    <ModalEnTrenes
      v-if="mostrarModal"
      :visible="mostrarModal"
      @cerrar-modal="cerrarModal"
    />
  </div>
</template>

<style scoped>
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
import ModalEnTrenes from "@/components/ModalViewEnTrenes.vue";

export default {
  name: "EnTrenes",

  data() {
    return {
      en_trenes: [], // Lista de trenes
      currentPage: 1, // Página actual
      itemsPerPage: 10, // Elementos por página
      totalItems: 0, // Total de elementos
      searchQuery: "", // Búsqueda
      debounceTimeout: null,
      busqueda_existente: true,
      userPermissions: [],
      userGroups: [],
      showContent: false,
      mostrarModal: false,
      mostrarModal: false,
    };
  },

  async mounted() {
    // Cuando el componente se monta, llamamos a las funciones necesarias// Obtener el rol del usuario
    await this.getTrenes();
    await this.hasGroup(); // Obtener la lista de trenes
    await this.fetchUserPermissionsAndGroups();
    console.log(this.user_role);
  },

  methods: {
    // Verifica si el usuario tiene un permiso específico

    hasPermission() {
      if (this.user_role === "role") {
        return true;
      } else {
        return this.user_role === "admin";
      }
    },
    toggleContentVisibility() {
      this.showContent = !this.showContent; // Alternar la visibilidad de las columnas No e Id
    },
    hasGroup(group) {
      return this.userGroups.some((g) => g.name === group);
    },
    // Obtiene los permisos y grupos del usuario desde el backend
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

    async getTrenes() {
      try {
        const response = await axios.get("/ufc/en-trenes/", {
          params: {
            page: this.currentPage, // Página actual
            page_size: this.itemsPerPage, // Elementos por página
          },
        });
        this.en_trenes = response.data.results; // Datos de la página actual
        this.totalItems = response.data.count; // Total de elementos
        console.log("Trenes obtenidos:", this.en_trenes);
      } catch (error) {
        console.error("Error al obtener los trenes:", error);
      }
    },

    async searchTrenes() {
      this.$store.commit("setIsLoading", true);
      try {
        const response = await axios.get("/ufc/en-trenes/", {
          params: {
            origen_destino: this.searchQuery, // Término de búsqueda
            page: this.currentPage, // Página actual
            page_size: this.itemsPerPage, // Elementos por página
          },
        });
        this.en_trenes = response.data.results; // Datos de la página actual
        this.totalItems = response.data.count; // Total de elementos
        this.busqueda_existente = this.en_trenes.length > 0;
      } catch (error) {
        console.error("Error al buscar trenes", error);
        this.busqueda_existente = false;
      }
      this.$store.commit("setIsLoading", false);
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

    // Cambiar a la página siguiente
    nextPage() {
      if (this.currentPage * this.itemsPerPage < this.totalItems) {
        this.currentPage++;
        this.getTrenes();
      }
    },

    // Cambiar a una página específica
    goToPage(page) {
      this.currentPage = page;
      this.getTrenes();
    },
    async delete_tren(id) {
      try {
        await axios.delete(`/ufc/en-trenes/${id}/`);
        // Actualizar la lista de productos eliminando el que se ha borrado
        this.en_trenes = this.en_trenes.filter((tren) => tren.id !== id);

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

    openVagonDetailsModal(tren) {
      // Mapear IDs de grupos a nombres
      /* const gruposAsignados = user.groups && user.groups.length > 0
        ? user.groups
            .map(groupId => {
                const grupo = this.gruposDisponibles.find(g => g.id === groupId);
                return grupo ? grupo.name : 'Desconocido';
            })
            .join(', ')
        : 'Ninguno'; */

      // Mapear IDs de permisos a nombres
      /*  const permisosAsignados = user.user_permissions && user.user_permissions.length > 0
        ? user.user_permissions
            .map(permisoId => {
                const permiso = this.permisosDisponibles.find(p => p.id === permisoId);
                return permiso ? permiso.name : 'Desconocido';
            })
            .join(', ')
        : 'Ninguno'; */

      Swal.fire({
        title: "Detalles del Vagon",
        html: `
            <div style="text-align: left;">
                <p><strong>No Id Locomotora:</strong> ${tren.numero_identificacion_locomotora}</p>
                <p><strong>Tipo de equipo:</strong> ${tren.tipo_equipo}</p>
                <p><strong>Estado:</strong> ${tren.estado}</p>
                <p><strong>Producto Id:</strong> ${tren.producto}</p>
                <p><strong>Producto nombre:</strong> ${tren.producto_name}</p>
                <p><strong>Tipo de origen:</strong> ${tren.tipo_origen}</p>
                <p><strong>Origen:</strong> ${tren.origen}</p>
                <p><strong>Tipo de destino:</strong> ${tren.tipo_destino}</p>
                <p><strong>Destino:</strong> ${tren.destino}</p> 
                <p><strong>Nombre del equipo de carga:</strong> ${tren.equipo_carga_name}</p>
                <p><strong>Observaciones:</strong> ${tren.observaciones}</p>
                
            </div>
        `,
        width: "600px",
        customClass: {
          popup: "custom-swal-popup",
          title: "custom-swal-title",
          htmlContainer: "custom-swal-html",
        },
      });
    },
    abrirModalEnTren() {
      this.mostrarModal = true;
      console.log("Abriendo Modal....");
    },
    cerrarModal() {
      this.mostrarModal = false;
    },
    abrirModalEnTren() {
      this.mostrarModal = true;
      console.log("Abriendo Modal....");
    },
    cerrarModal() {
      this.mostrarModal = false;
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
