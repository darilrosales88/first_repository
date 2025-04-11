<template>
  <div class="container">
    <!-- Fila para el icono y el buscador -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <!-- Icono de agregar (a la izquierda) -->
      <button class="btn btn-link p-0" >
        <router-link to="/AdicionarPorSituar"><i class="bi bi-plus-circle fs-3"></i></router-link>
        
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
            <th scope="col">Tipo Origen</th>
            <th scope="col">Origen</th>
            <th scope="col">Tipo de equipo</th>
            <th scope="col">Estado</th>
            <th scope="col">Operacion</th>
            <th scope="col">Producto</th>
            <th scope="col">Por Situar</th>
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
          <td>{{ item.por_situar }}</td>

          <td>
            <button class="btn btn-warning btn-small">
              <router-link 
                :to="{ 
                  name: 'EditarPorSituar', 
                  params: { 
                    id: item.id || 'default-id' 
                  } 
                }"
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
        <tr v-if="!loading && registrosPorSituar.length === 0 && !errorLoading">
  <td colspan="8" class="text-center text-muted py-4">
    <i class="bi bi-database fs-4"></i>
    <p class="mt-2">No hay registros disponibles</p>
  </td>
</tr>
      </tbody>
    </table>

   
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
      errorLoading: false,
      
      // Opciones para los selects
      tipo_origen_options: [
        { id: "puerto", text: "Puerto" },
        { id: "acceso comercial", text: "Acceso Comercial" },
      ],
      tipo_equipo_options: [
        { id: "casilla", text: "Casilla" },
        { id: "caj_gon", text: "Cajon o Gondola" },
      ],
      estado_options: [
        { id: "vacio", text: "Vacio" },
        { id: "cargado", text: "Cargado" },
      ],
      t_operacion_options: [
        { id: "carga", text: "Carga" },
        { id: "descarga", text: "Descarga" },
      ],
      producto_options: [],
      origen: '',
    };
  },

  mounted() {
    this.getPorSituar();
  },

  methods: {
    async getPorSituar() {
      this.loading = true;
      this.errorLoading = false;
      try {
        const response = await axios.get("http://127.0.0.1:8000/ufc/por-situar/");
        
        // Manejo correcto de la respuesta
        this.allRecords = Array.isArray(response.data) ? response.data : response.data.results || [];
        this.registrosPorSituar = [...this.allRecords];
        this.busqueda_existente = this.registrosPorSituar.length > 0;
      } catch (error) {
        console.error("Error al cargar datos:", error);
        this.errorLoading = true;
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'No se pudieron cargar los datos. Por favor, intente nuevamente.',
        });
      } finally {
        this.loading = false;
      }
    },

    // ... (otros métodos permanecen iguales)
  }
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
