<template>
  <div class="container">
    <!-- Fila para el icono y el buscador -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <!-- Icono de agregar (a la izquierda) -->
      <button class="btn btn-link p-0" @click="showModal = true">
        <i class="bi bi-plus-circle fs-3"></i> <!-- Icono grande -->
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
        <span class="position-absolute top-50 start-0 translate-middle-y ps-2">
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
          <th scope="row">{{ (index + 1) }}</th>
          <td>{{ item.tipo_origen }}</td>
          <td>{{ item.tipo_equipo }}</td>
          <td>{{ item.estado }}</td>
          <td>{{ item.operacion }}</td>
          <td>{{ item.producto }}</td>
          <td>{{ item.situados }}</td>
          <td>{{ item.pendiente_proximo_dia }}</td>
          
          <td>
            <button class="btn btn-warning btn-small" @click="openEditModal(item)">
              <i style="color: black" class="bi bi-pencil-square"></i>
            </button>
            <button 
              style="margin-left:1em" 
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
            <p class="mt-2">No se encontraron resultados para "{{ searchQuery }}"</p>
          </td>
        </tr>
      
      </tbody>
    </table>

    <!-- Modal para agregar nuevos datos -->
    <div v-if="showModal" class="modal-backdrop">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ isEditing ? 'Editar Registro' : 'Agregar nuevo registro' }}</h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="isEditing ? updateItem() : addNewItem()">
            <!-- Campos del formulario (igual que antes) -->
            <div class="mb-3">
              <label for="origen" class="form-label">Origen</label>
              <select class="form-select" id="origen" v-model="nuevoRegistro.tipo_origen" required>
                <option value="">Seleccione un origen</option>
                <option v-for="item in tipo_origen_options" :key="item.id" :value="item.id">{{ item.text }}</option>
              </select>
            </div>
      <div class="mb-3">
        <label for="tipoEquipo" class="form-label">Tipo de equipo</label>
        <select class="form-select" id="tipoEquipo" v-model="nuevoRegistro.tipo_equipo" required>
          <option value="">Seleccione un tipo</option>
          <option v-for="item in tipo_equipo_options" :key="item.id" :value="item.id">{{ item.text }}</option>
        </select>
      </div>
      <div class="mb-3">
        <label for="estado" class="form-label">Estado</label>
        <select class="form-select" id="estado" v-model="nuevoRegistro.estado" required>
          <option value="">Seleccione un estado</option>
          <option v-for="item in estado_options" :key="item.id" :value="item.id">{{ item.text }}</option>
        </select>
      </div>
      <div class="mb-3">
        <label for="operacion" class="form-label">Operacion</label>
        <select class="form-select" id="operacion" v-model="nuevoRegistro.operacion" required>
          <option value="">Seleccione una operación</option>
          <option v-for="item in t_operacion_options" :key="item.id" :value="item.id">{{ item.text }}</option>
        </select>
      </div>
      <div class="mb-3">
        <label for="producto" class="form-label">Producto</label>
        <select class="form-select" id="producto" v-model="nuevoRegistro.producto" required>
          <option value="">Seleccione un producto</option>
          <option v-for="item in producto_options" :key="item.id" :value="item.id">
            {{ item.producto }}
          </option>
        </select>
      </div>
      <div class="mb-3">
        <label for="situados" class="form-label">Situados</label>
        <input type="text" class="form-control" id="situados" v-model="nuevoRegistro.situados" required />
      </div>

      <div class="mb-3">
        <label for="situados" class="form-label">Pendientes al proximo dia</label>
        <input type="text" class="form-control" id="situados" v-model="nuevoRegistro.pendiente_proximo_dia" required />
      </div>
      
      <button 
    style="margin-right:1em" 
    type="submit" 
    class="btn btn-primary btn-sm"
    :disabled="loading"
  >
    <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    {{ isEditing ? (loading ? 'Actualizando...' : 'Actualizar') : (loading ? 'Procesando...' : 'Agregar') }}
  </button>
      <button 
        type="button" 
        class="btn btn-secondary btn-sm" 
        @click="showModal = false"
        :disabled="loading"
      >
        Cancelar
      </button>
    </form>
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
      registrosPorSituar: [], // Nombre consistente
      loading: false,
      busqueda_existente: true,
      showModal: false,
      
      // Opciones para los selects
      tipo_origen_options: [
        { id: 'puerto', text: 'Puerto' },
        { id: 'acceso comercial', text: 'Acceso Comercial' },
      ],
      tipo_equipo_options: [
        { id: 'casilla', text: 'Casilla' },
        { id: 'caj_gon', text: 'Cajon o Gondola' },
      ],
      estado_options: [
        { id: 'vacio', text: 'Vacio' },
        { id: 'cargado', text: 'Cargado' }
      ],
      t_operacion_options: [
        { id: 'carga', text: 'Carga' },
        { id: 'descarga', text: 'Descarga' }
      ],
      producto_options: [],

      nuevoRegistro: {
        tipo_origen: '',
        tipo_equipo: '',
        estado: '',
        operacion: '',
        producto: '',
        situados: '',
        pendiente_proximo_dia: '',
      }
    };
  },

  mounted() {
    this.getPorSituar();
    this.loadProductos();
  },

  methods: {
    async getPorSituar() {
      this.loading = true;
      try {
        const response = await axios.get('http://127.0.0.1:8000/ufc/situados/');
        console.log('Datos de situados:', response.data);
        
        // Validación más robusta
        if (!response.data || !Array.isArray(response.data)) {
          throw new Error("La API no devolvió un array de datos");
        }

        // Mapeo seguro de datos
        this.allRecords = response.data.results.map(item => ({
          id: item.id,
          tipo_origen: item.tipo_origen || '',
          tipo_equipo: item.tipo_equipo || '',
          estado: item.estado || '',
          operacion: item.operacion || '',
          producto: item.producto || '',
          situados: item.situados || 0,
          pendiente_proximo_dia: item.pendiente_proximo_dia || 0
        }));

        this.registrosPorSituar = [...this.allRecords];
        this.busqueda_existente = true;

      } catch (error) {
        console.error("Error en getPorSituar:", error);
        this.handleApiError(error, "cargar registros");
        this.registrosPorSituar = [];
      } finally {
        this.loading = false;
      }
    },

    async loadProductos() {
      try {
        this.loading = true;
        const response = await axios.get('http://127.0.0.1:8000/api/productos/');
        console.log('Datos de productos:', response.data);
        
        if (!response.data || !Array.isArray(response.data)) {
          throw new Error("La API no devolvió un array de productos");
        }

        this.producto_options = response.data.map(p => ({
          id: p.id,
          producto: p.nombre || p.producto || `Producto ${p.id}`
        }));

      } catch (error) {
        console.error("Error en loadProductos:", error);
        this.handleApiError(error, "cargar productos");
        this.producto_options = [];
      } finally {
        this.loading = false;
      }
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
      Swal.fire("Error", errorMsg, "error");
    },

    // ... (otros métodos se mantienen igual)
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