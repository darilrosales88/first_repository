<template>
  <div class="container">
    <!-- Fila para el icono y el buscador -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <!-- Icono de agregar (a la izquierda) -->
      <button class="btn btn-link p-0" @click="showModal = true">
        <i class="bi bi-plus-circle fs-3"></i>
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
          <td>{{ item.tipo_equipo }}</td>
          <td>{{ item.estado }}</td>
          <td>{{ item.operacion }}</td>
          <td>{{ item.producto_name }}</td>
          <td>{{ item.por_situar }}</td>

          <td>
            <button
              class="btn btn-warning btn-small"
              @click="openEditModal(item)"
            >
              <i style="color: black" class="bi bi-pencil-square"></i>
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

    <!-- Modal para agregar nuevos datos -->
    <div v-if="showModal" class="modal-backdrop">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            {{ isEditing ? "Editar Registro" : "Agregar nuevo registro" }}
          </h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="isEditing ? updateItem() : addNewItem()">
            <!-- Campos del formulario (igual que antes) -->
            <div class="mb-3">
              <label for="origen" class="form-label">Origen</label>
              <select
                class="form-select"
                id="origen"
                v-model="nuevoRegistro.tipo_origen"
                required
              >
                <option value="">Seleccione un origen</option>
                <option
                  v-for="item in tipo_origen_options"
                  :key="item.id"
                  :value="item.id"
                >
                  {{ item.text }}
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label for="tipoEquipo" class="form-label">Tipo de equipo</label>
              <select
                class="form-select"
                id="tipoEquipo"
                v-model="nuevoRegistro.tipo_equipo"
                required
              >
                <option value="">Seleccione un tipo</option>
                <option
                  v-for="item in tipo_equipo_options"
                  :key="item.id"
                  :value="item.id"
                >
                  {{ item.text }}
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label for="estado" class="form-label">Estado</label>
              <select
                class="form-select"
                id="estado"
                v-model="nuevoRegistro.estado"
                required
              >
                <option value="">Seleccione un estado</option>
                <option
                  v-for="item in estado_options"
                  :key="item.id"
                  :value="item.id"
                >
                  {{ item.text }}
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label for="operacion" class="form-label">Operacion</label>
              <select
                class="form-select"
                id="operacion"
                v-model="nuevoRegistro.operacion"
                required
              >
                <option value="">Seleccione una operación</option>
                <option
                  v-for="item in t_operacion_options"
                  :key="item.id"
                  :value="item.id"
                >
                  {{ item.text }}
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label for="producto" class="form-label">Producto</label>
              <select
                class="form-select"
                id="producto"
                v-model="nuevoRegistro.producto"
                required
              >
                <option value="">Seleccione un producto</option>
                <option
                  v-for="item in producto_options"
                  :key="item.id"
                  :value="item.id"
                >
                  {{ item.producto }}
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label for="situados" class="form-label">Por Situar</label>
              <input
                type="text"
                class="form-control"
                id="situados"
                v-model="nuevoRegistro.cantidad_por_situar"
                required
              />
            </div>

            <button
              style="margin-right: 1em"
              type="submit"
              class="btn btn-primary btn-sm"
              :disabled="loading"
            >
              <span
                v-if="loading"
                class="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
              ></span>
              {{
                isEditing
                  ? loading
                    ? "Actualizando..."
                    : "Actualizar"
                  : loading
                  ? "Procesando..."
                  : "Agregar"
              }}
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
      allRecords: [], // Para guardar todos los registros sin filtrar
      debounceTimeout: null, // Para el debounce del buscador
      isEditing: false,
      currentItemId: null,
      searchQuery: "",
      registrosPorSituar: [], // Cambiado de por_situar a registrosPorSituar para evitar conflicto
      loading: false,
      busqueda_existente: true,
      showModal: false,

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

      // Datos del nuevo registro
      nuevoRegistro: {
        tipo_origen: "",
        tipo_equipo: "",
        estado: "",
        operacion: "",
        producto: "",
        cantidad_por_situar: "",
      },
    };
  },

  mounted() {
    this.getPorSituar();
    this.loadProductos();
  },

  methods: {
    openEditModal(item) {
      this.isEditing = true;
      this.currentItemId = item.id;
      this.nuevoRegistro = {
        tipo_origen: item.tipo_origen,
        tipo_equipo: item.tipo_equipo,
        estado: item.estado,
        operacion: item.operacion,
        producto: item.producto,
        cantidad_por_situar: item.por_situar,
      };
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
      this.isEditing = false;
      this.currentItemId = null;
      this.resetForm();
    },

    async updateItem() {
      try {
        this.loading = true;

        const datosParaEnviar = {
          tipo_origen: this.nuevoRegistro.tipo_origen,
          tipo_equipo: this.nuevoRegistro.tipo_equipo,
          estado: this.nuevoRegistro.estado,
          operacion: this.nuevoRegistro.operacion,
          producto: this.nuevoRegistro.producto,
          por_situar: this.nuevoRegistro.cantidad_por_situar,
        };

        const response = await axios.put(
          `http://127.0.0.1:8000/ufc/por-situar/${this.currentItemId}/`,
          datosParaEnviar
        );

        if (response.status === 200) {
          Swal.fire("Éxito", "Registro actualizado correctamente", "success");
          this.showModal = false;
          this.resetForm();
          this.getPorSituar();
        } else {
          throw new Error(`Respuesta inesperada: ${response.status}`);
        }
      } catch (error) {
        console.error("Error al actualizar:", error);
        let errorMessage = "Error al actualizar el registro";

        if (error.response?.data) {
          errorMessage += ": " + JSON.stringify(error.response.data);
        }

        Swal.fire("Error", errorMessage, "error");
      } finally {
        this.loading = false;
      }
    },

    async updateItem() {
      try {
        this.loading = true;

        const datosParaEnviar = {
          tipo_origen: this.nuevoRegistro.tipo_origen,
          tipo_equipo: this.nuevoRegistro.tipo_equipo,
          estado: this.nuevoRegistro.estado,
          operacion: this.nuevoRegistro.operacion,
          producto: this.nuevoRegistro.producto,
          por_situar: this.nuevoRegistro.cantidad_por_situar,
        };

        const response = await axios.put(
          `http://127.0.0.1:8000/ufc/por-situar/${this.currentItemId}/`,
          datosParaEnviar
        );

        if (response.status === 200) {
          Swal.fire("Éxito", "Registro actualizado correctamente", "success");
          this.showModal = false;
          this.resetForm();
          this.getPorSituar();
        } else {
          throw new Error(`Respuesta inesperada: ${response.status}`);
        }
      } catch (error) {
        console.error("Error al actualizar:", error);
        let errorMessage = "Error al actualizar el registro";

        if (error.response?.data) {
          errorMessage += ": " + JSON.stringify(error.response.data);
        }

        Swal.fire("Error", errorMessage, "error");
      } finally {
        this.loading = false;
      }
    },

    getPorSituar() {
      this.loading = true;
      axios
        .get("http://127.0.0.1:8000/ufc/por-situar/")
        .then((response) => {
          this.allRecords = response.data.results; // Guarda todos los registros
          this.registrosPorSituar = [...this.allRecords]; // Copia para mostrar
          this.busqueda_existente = true;
        })
        .catch((error) => {
          console.error(error);
          Swal.fire("Error", "No se pudieron cargar los datos", "error");
        })
        .finally(() => {
          this.loading = false;
        });
    },

    async addNewItem() {
      try {
        // Validación mejorada
        const camposRequeridos = [
          { nombre: "tipo_origen", valor: this.nuevoRegistro.tipo_origen },
          { nombre: "tipo_equipo", valor: this.nuevoRegistro.tipo_equipo },
          { nombre: "estado", valor: this.nuevoRegistro.estado },
          { nombre: "operacion", valor: this.nuevoRegistro.operacion },
          { nombre: "producto", valor: this.nuevoRegistro.producto },
          {
            nombre: "cantidad_por_situar",
            valor: this.nuevoRegistro.cantidad_por_situar,
          },
        ];

        const camposFaltantes = camposRequeridos.filter(
          (campo) => !campo.valor
        );

        if (camposFaltantes.length > 0) {
          const campos = camposFaltantes.map((c) => c.nombre).join(", ");
          Swal.fire(
            "Error",
            `Faltan los siguientes campos: ${campos}`,
            "error"
          );
          return;
        }

        this.loading = true;

        // Preparamos los datos para enviar
        const datosParaEnviar = {
          tipo_origen: this.nuevoRegistro.tipo_origen,
          tipo_equipo: this.nuevoRegistro.tipo_equipo,
          estado: this.nuevoRegistro.estado,
          operacion: this.nuevoRegistro.operacion, // Cambiado a t_operacion para coincidir con el backend
          producto: this.nuevoRegistro.producto,
          por_situar: this.nuevoRegistro.cantidad_por_situar,
        };

        console.log("Datos a enviar al backend:", datosParaEnviar);

        const response = await axios.post(
          "http://127.0.0.1:8000/ufc/por-situar/",
          datosParaEnviar
        );

        if (response.status === 201) {
          Swal.fire("Éxito", "Registro creado correctamente", "success");
          this.showModal = false;
          this.resetForm();
          this.getPorSituar();
        } else {
          throw new Error(`Respuesta inesperada: ${response.status}`);
        }
      } catch (error) {
        console.error("Error completo:", error);
        console.error("Respuesta del error:", error.response);

        let errorMessage = "Error al crear el registro";
        if (error.response) {
          errorMessage += ` (${error.response.status}): `;
          if (error.response.data) {
            // Mostrar errores específicos del backend
            if (typeof error.response.data === "object") {
              errorMessage += Object.entries(error.response.data)
                .map(([key, value]) => `${key}: ${value}`)
                .join(", ");
            } else {
              errorMessage += JSON.stringify(error.response.data);
            }
          }
        } else {
          errorMessage += `: ${error.message}`;
        }

        Swal.fire("Error", errorMessage, "error");
      } finally {
        this.loading = false;
      }
    },

    resetForm() {
      this.nuevoRegistro = {
        tipo_origen: "",
        tipo_equipo: "",
        estado: "",
        operacion: "",
        producto: "",
        cantidad_por_situar: "",
      };
    },

    async loadProductos() {
      try {
        this.loading = true;
        const response = await axios.get("/api/productos/", {
          params: { limit: 100 },
        });

        if (response.status === 200) {
          this.producto_options = response.data.results.map((p) => ({
            id: p.id,
            producto: p.nombre_producto || p.descripcion || `Producto ${p.id}`,
          }));
        }
      } catch (error) {
        console.error("Error detallado:", error);
        let errorMsg = "Error al cargar productos";

        if (error.response?.data?.detail) {
          errorMsg += `: ${error.response.data.detail}`;
        }

        Swal.fire("Error", errorMsg, "error");
      } finally {
        this.loading = false;
      }
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        if (this.searchQuery.trim() === "") {
          this.getPorSituar();
        } else {
          this.filterRecords();
        }
      }, 300);
    },

    filterRecords() {
      const query = this.searchQuery.toLowerCase();
      if (!query) {
        this.registrosPorSituar = [...this.allRecords];
        this.busqueda_existente = true;
        return;
      }

      this.registrosPorSituar = this.allRecords.filter((item) => {
        // Convertir todos los valores a string antes de comparar
        const tipoEquipo = item.tipo_equipo
          ? String(item.tipo_equipo).toLowerCase()
          : "";
        const producto = item.producto
          ? String(item.producto).toLowerCase()
          : "";
        const operacion = item.operacion
          ? String(item.operacion).toLowerCase()
          : "";

        return (
          tipoEquipo.includes(query) ||
          producto.includes(query) ||
          operacion.includes(query)
        );
      });

      this.busqueda_existente = this.registrosPorSituar.length > 0;
    },

    search_por_situar() {
      this.loading = true;
      axios
        .get(
          `http://127.0.0.1:8000/ufc/por-situar/?tipo_equipo=${this.searchQuery}`
        )
        .then((response) => {
          this.registrosPorSituar = response.data;
          this.busqueda_existente = this.registrosPorSituar.length > 0;
        })
        .catch((error) => {
          console.error(error);
          this.busqueda_existente = false;
          this.registrosPorSituar = [];
        })
        .finally(() => {
          this.loading = false;
        });
    },

    async confirmDelete(id) {
      try {
        const result = await Swal.fire({
          title: "¿Estás seguro?",
          text: "¡No podrás revertir esto!",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#d33",
          cancelButtonColor: "#3085d6",
          confirmButtonText: "Sí, eliminar",
          cancelButtonText: "Cancelar",
        });

        if (result.isConfirmed) {
          await this.deleteItem(id);
          Swal.fire("¡Eliminado!", "El registro ha sido eliminado.", "success");
          // Recargar los datos después de eliminar
          this.getPorSituar();
        }
      } catch (error) {
        console.error("Error al eliminar:", error);
        Swal.fire("Error", "No se pudo eliminar el registro", "error");
      }
    },

    async deleteItem(id) {
      this.loading = true;
      try {
        const response = await axios.delete(
          `http://127.0.0.1:8000/ufc/por-situar/${id}/`
        );

        if (response.status !== 204) {
          throw new Error(`Respuesta inesperada: ${response.status}`);
        }
      } finally {
        this.loading = false;
      }
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
