<template>
  <div class="container">
    <!-- Fila para el icono y el buscador -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <!-- Icono de agregar (a la izquierda) -->
      <button class="btn btn-link p-0">
        <router-link to="/AdicionarSituados"><i class="bi bi-plus-circle fs-3"></i></router-link>
        
        <!-- Icono grande -->
      </button>

      <!-- Buscador (a la derecha) -->
      <form @submit.prevent="search_por_situar" class="search-container">
        <div class="input-group">
          <input
            type="search"
            class="form-control"
            placeholder="Buscar por tipo de equipo..."
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

    <!-- Tabla -->
    <table class="table table-responsive">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Tipo de origen</th>
          <th scope="col">Origen</th>
          <th scope="col">Tipo de equipo</th>
          <th scope="col">Estado</th>
          <th scope="col">Operacion</th>
          <th scope="col">Producto</th>
          <th scope="col">Situados</th>
          <th scope="col">Pendientes por situar</th>

          <th scope="col">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="loading">
          <td colspan="8" class="text-center">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Cargando...</span>
            </div>
          </td>
        </tr>

        <tr v-for="(item, index) in registrosPorSituar" :key="item.id">
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ item.tipo_origen }}</td>
          <td>{{ item.origen }}</td>
          <td>{{ item.tipo_equipo }}</td>
          <td>{{ item.estado }}</td>
          <td>{{ item.operacion }}</td>
          <td>{{ item.producto_name }}</td>
          <td>{{ item.situados }}</td>
          <td>{{ item.pendiente_proximo_dia }}</td>

          <td>
            <button class="btn btn-warning btn-small">
              <router-link
                    :to="{ name: 'EditarSituados', params: { id: item.id } }"
                  >
                    <i style="color: black" class="bi bi-pencil-square"></i>
                  </router-link>
            </button>
            <button
              style="margin-left: 1em"
              class="btn btn-danger btn-small"
              @click="confirmDelete(item.id)"
              :disabled="loading"
            >
              <i class="bi bi-trash"></i>
            </button>
          </td>
        </tr>
        <tr v-if="!busqueda_existente && registrosPorSituar.length === 0">
          <td colspan="8" class="text-center text-muted py-4">
            <i class="bi bi-exclamation-circle fs-4"></i>
            <p class="mt-2">
              No se encontraron resultados para "{{ searchQuery }}"
            </p>
          </td>
        </tr>
      </tbody>
    </table>

    
    
    <!-- Paginación mejorada -->
    <div class="d-flex justify-content-between align-items-center">
      <div class="text-muted small">
        Mostrando {{ allRecords.length }} de {{ totalItems }} registros
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
      totalItems: 0,
      currentPage: 1, // Página actual
      itemsPerPage: 10,

      // Opciones para los selects
      

      nuevoRegistro: {
        tipo_origen: "",
        tipo_equipo: "",
        estado: "",
        operacion: "",
        producto: "",
        situados: "",
        pendiente_proximo_dia: "",
        origen: '',
      },
    };
  },

  mounted() {
    this.getPorSituar();
    
  },

  methods: {
    // Obtener todos los registros
    async getPorSituar() {
      this.loading = true;
      try {
        const response = await axios.get("http://127.0.0.1:8000/ufc/situados/");
        this.totalItems = response.data.count;
        if (
          response.data &&
          Array.isArray(response.data.results || response.data)
        ) {
          const data = response.data.results || response.data;
          this.allRecords = data.map((item) => ({
            id: item.id,
            tipo_origen: item.tipo_origen || "",
            tipo_equipo: item.tipo_equipo || "",
            estado: item.estado || "",
            operacion: item.operacion || "",
            producto: item.producto_name || "",
            situados: item.situados || 0,
            pendiente_proximo_dia: item.pendiente_proximo_dia || 0,
          }));

          this.registrosPorSituar = [...this.allRecords];
          this.busqueda_existente = true;
        }
      } catch (error) {
        this.handleApiError(error, "cargar registros");
        this.registrosPorSituar = [];
      } finally {
        this.loading = false;
      }
    },

    // Cargar productos para el select
    

    // Buscar por tipo de equipo
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        if (!this.searchQuery.trim()) {
          this.registrosPorSituar = [...this.allRecords];
          this.busqueda_existente = true;
          return;
        }

        const query = this.searchQuery.toLowerCase();
        this.registrosPorSituar = this.allRecords.filter((item) => {
          const tipoEquipo = item.tipo_equipo?.toLowerCase() || "";
          return tipoEquipo.includes(query);
        });

        this.busqueda_existente = this.registrosPorSituar.length > 0;
      }, 300);
    },

    

    // Agregar nuevo registro
    

    

    // Confirmar eliminación
    async confirmDelete(id) {
      const result = await Swal.fire({
        title: "¿Estás seguro?",
        text: "¡No podrás revertir esta acción!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
      });

      if (result.isConfirmed) {
        await this.deleteItem(id);
      }
    },

    // Eliminar registro
    async deleteItem(id) {
      try {
        this.loading = true;
        const response = await axios.delete(
          `http://127.0.0.1:8000/ufc/situados/${id}/`
        );

        if (response.status === 204) {
          Swal.fire("Eliminado", "El registro ha sido eliminado", "success");
          await this.getPorSituar();
        }
      } catch (error) {
        this.handleApiError(error, "eliminar registro");
      } finally {
        this.loading = false;
      }
    },

    // Manejo de errores
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
