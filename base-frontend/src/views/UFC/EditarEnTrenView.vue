<template>
  <div class="ufc-header">
    <h6>Bienvenido:</h6>
  </div>
  <Navbar-Component />
  <Producto-Vagones />
  <div class="container py-3" style="margin-left: 20em; width: 70%">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-file-earmark-plus me-2"></i> Editar registro de vagón</h5>
      </div>
      <div class="card-body p-3">
        <form @submit.prevent="submitForm" class="ufc-form">
          <div class="ufc-form-grid">
            <!-- Columna Izquierda -->
            <!-- Campo: Fecha de registro -->
            <div class="ufc-form-column">
              <!-- Campo: locomotora -->
              <div class="ufc-input-group">
                <label for="locomotora" class="form-label small fw-semibold text-secondary"
                  >Locomotora </label
                >
                <select
                  class="form-select form-select-sm border-secondary"
                  v-model="formData.locomotora"
                  required
                >
                  <option value="" disabled>Seleccione una locomotora</option>
                  <option
                    v-for="locomotora in locomotoras"
                    :key="locomotora.id"
                    :value="locomotora.id"
                  >
                    {{ locomotora.id }}-{{
                      locomotora.numero_identificacion
                    }}
                    - {{ locomotora.tipo_equipo_name }}
                  </option>
                </select>
              </div>

              <!-- Campo: tipo_origen -->
              <div class="ufc-input-group">
                <label for="tipo_origen" class="form-label small fw-semibold text-secondary"
                  >Tipo de Origen</label
                >
                <select
                  class="form-select form-select-sm border-secondary"
                  v-model="formData.tipo_origen"
                  required
                >
                  <option value="ac_ccd">Acceso Comercial</option>
                  <option value="puerto">Puerto</option>
                </select>
              </div>

              <!-- Campo: origen -->
              <div class="ufc-input-group">
                <label for="origen" class="form-label small fw-semibold text-secondary"
                  >Origen</label
                >
                <select
                  v-if="formData.tipo_origen !== 'puerto'"
                  class="form-select form-select-sm border-secondary"
                  v-model="formData.origen"
                  required
                >
                  <option value="" disabled>Seleccione un origen</option>
                  <option
                    v-for="entidad in entidades"
                    :key="entidad.id"
                    :value="entidad.nombre"
                  >
                    {{ entidad.id }}-{{ entidad.nombre }}
                  </option>
                </select>

                <select
                  v-else
                  class="form-select form-select-sm border-secondary"
                  v-model="formData.origen"
                  required
                >
                  <option value="" disabled>Seleccione un puerto</option>
                  <option
                    v-for="puerto in puertos"
                    :key="puerto.id"
                    :value="puerto.nombre_puerto"
                  >
                    {{ puerto.id }}- {{ puerto.nombre_puerto }}
                  </option>
                </select>
              </div>

              <!-- Campo: tipo_equipo -->
              <div class="ufc-input-group">
                <label for="tipo_equipo" class="form-label small fw-semibold text-secondary">Tipo de Equipo</label>
                <select
                  class="form-select form-select-sm border-secondary"
                  v-model="formData.tipo_equipo"
                  @click="buscarEquipos"
                  required>
                  <option value="" disabled>Seleccione un tipo</option>
                  <option
                    v-for="equipo in equipos"
                    :key="equipo.id"
                    :value="equipo.id">
                    {{ equipo.id }}-{{ equipo.tipo_equipo_name }}-{{
                      equipo.tipo_carga_name
                    }}
                  </option>
                </select>
              </div>

              <!-- Campo: estado -->
              <div class="ufc-input-group">
                <label for="estado" class="form-label small fw-semibold text-secondary"
                  >Estado</label
                >
                <select class="form-select form-select-sm border-secondary" v-model="formData.estado" required>
                  <option value="cargado">Cargado</option>
                  <option value="vacio">Vacio</option>
                </select>
              </div>

              <!-- Campo: Vagon No ID -->
              <div class="ufc-input-group">
                <label for="equipo_vagon" class="form-label small fw-semibold text-secondary"
                  >Vagon No ID</label
                >
                <select
                  class="form-select form-select-sm border-secondary"
                  v-model="formData.equipo_vagon"
                  required
                  @click="onVagonChange"
                >
                  <option value="" disabled>Seleccione un vagón</option>
                  <option v-for="item in equipos_vagones" :value="item.id">
                    {{ item.id }}-{{ item.numero_identificacion }}
                  </option>
                </select>
              </div>
            </div>

            <!-- Columna Derecha -->
            <div class="ufc-form-column">
              <!-- Campo: tipo_destino -->
              <div class="ufc-input-group">
                <label for="tipo_destino" class="form-label small fw-semibold text-secondary"
                  >Tipo de Destino</label
                >
                <select
                  class="form-select form-select-sm border-secondary"
                  v-model="formData.tipo_destino"
                  required
                >
                  <option value="ac_ccd">Acceso Comercial</option>
                  <option value="puerto">Puerto</option>
                </select>
              </div>

              <!-- Campo: destino -->
              <div class="ufc-input-group">
                <label for="destino" class="form-label small fw-semibold text-secondary"
                  >Destino</label
                >
                <select
                  v-if="formData.tipo_destino !== 'puerto'"
                  class="form-select form-select-sm border-secondary"
                  v-model="formData.destino"
                  required
                >
                  <option value="" disabled>Seleccione un destino</option>
                  <option
                    v-for="entidad in entidades"
                    :key="entidad.id"
                    :value="entidad.nombre"
                  >
                    {{ entidad.id }}-{{ entidad.nombre }}
                  </option>
                </select>

                <select
                  v-else
                  class="ufc-select"
                  v-model="formData.destino"
                  required
                >
                  <option value="" disabled>Seleccione un puerto</option>
                  <option
                    v-for="puerto in puertos"
                    :key="puerto.id"
                    :value="puerto.nombre_puerto"
                  >
                    {{ puerto.id }}- {{ puerto.nombre_puerto }}
                  </option>
                </select>
              </div>

              <!-- Campo: producto -->
              <div class="ufc-input-group">
                <label for="producto" class="form-label small fw-semibold text-secondary"
                  >Productos</label
                >
                <div class="ufc-input-with-action">
                  <div
                    class="ufc-custom-select"
                    @click="toggleProductosDropdown"
                  >
                    <div class="ufc-select-display">
                      {{
                        getSelectedProductosText() ||
                        "Seleccione productos..."
                      }}
                    </div>
                    <i class="bi bi-chevron-down ufc-select-arrow"></i>

                    <div
                      class="ufc-productos-dropdown"
                      v-if="showProductosDropdown"
                    >
                      <div class="ufc-productos-search-container">
                        <input
                          type="text"
                          class="ufc-productos-search"
                          placeholder="Buscar productos..."
                          v-model="productoSearch"
                          @input="filterProductos"
                          @click.stop
                        />
                      </div>
                      <div class="ufc-productos-options">
                        <div
                          v-for="producto in filteredProductos"
                          :key="producto.id"
                          class="ufc-producto-option"
                          :class="{
                            selected: formData.producto.includes(producto.id),
                          }"
                          @click.stop="toggleProductoSelection(producto.id)"
                        >
                          {{ producto.id }}-{{ producto.producto_name }} -
                          {{ producto.producto_codigo }}
                          <template v-if="producto.tipo_embalaje">
                            (Embalaje:
                            {{
                              producto.tipo_embalaje_name ||
                              producto.tipo_embalaje.nombre_embalaje ||
                              "N/A"
                            }})
                          </template>
                        </div>
                      </div>
                    </div>
                  </div>
                  <button class="create-button ms-2" @click.stop.prevent="abrirModalAgregarProducto">
                    <i class="bi bi-plus-circle large-icon"></i>
                  </button>
                </div>
              </div>

              <ModalAgregarProducto v-if="mostrarModal" :visible="mostrarModal" @cerrar-modal="cerrarModal"/>

              <!-- Campo: cantidad_vagones -->
              <div class="ufc-input-group">
                <label for="cantidad_vagones" class="form-label small fw-semibold text-secondary"
                  >Cantidad de Vagones</label
                >
                <input
                  type="number"
                  class="form-control form-control-sm border-secondary"
                  v-model="formData.cantidad_vagones"
                  min="0"
                  required
                />
              </div>

              <!-- Campo: observaciones -->
              <div class="ufc-input-group full-width">
                <label for="observaciones" class="form-label small fw-semibold text-secondary">Observaciones</label>
                <textarea
                  class="form-control form-control-sm border-secondary"
                  v-model="formData.observaciones"
                  rows="3"
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Botones de acción -->
          <div class="modal-footer">
            <div class=" d-flex justify-content-between align-items-center mb-4">
              <button class="ufc-button secondary" @click="volver_principal">
                <i class="bi bi-x-circle" me-1></i>Cancelar
              </button>
              <button type="submit" class=" ufc-button primary" >
                <i class="bi bi-check-circle" me-1></i>Actualizar
              </button>
            </div>
          </div>
        </form>      
      </div>
    </div>
  </div>
  <div class="container py-3" style="margin-left: 20em; width: 70%">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-train-freight-front"></i> Vagones agregados
        </h5>
      </div>
      <div class="card-body p-3">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <button class="btn btn-primary" @click="agregarVagon">
            <i class="bi bi-plus-circle"></i> Agregar Vagon
          </button>
        </div>
        <!-- Tabla responsive con mejoras -->
        <div class="table table-responsive">
          <table class="table table-sm table-bordered table-hover">
            <thead class="table-light">
              <tr>
                <th scope="col">No.</th>
                <th scope="col">No. ID en trenes</th>
                <th scope="col">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="9" class="ps-loading-td">
                  <div class="ps-loading">
                    <div class="ps-spinner"></div>
                    <span>Cargando registros...</span>
                  </div>
                </td>
              </tr>
              <tr v-for="(vagon, index) in vagonesAgregados" :key="index">
                <td>{{ index + 1 }}</td>
                <td>
                  {{ vagon["datos"]["equipo_vagon"] }}
                </td>
                <td>
                  <button class="ufc-button danger ufc-button-sm" @click="eliminarVagon(index)">
                    <i class="bi bi-trash"></i> Eliminar
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- Validación de cantidad de vagones -->
        <div class="ufc-validation-message" :class="{ warning: vagonesAgregados.length < formData.cantidad_vagones, success: vagonesAgregados.length === formData.cantidad_vagones, error: vagonesAgregados.length > formData.cantidad_vagones,}">
          <p v-if="vagonesAgregados.length < formData.cantidad_vagones">
            Faltan
            {{ formData.cantidad_vagones - vagonesAgregados.length }}
            vagones por agregar.
          </p>
          <p v-else-if="vagonesAgregados.length === formData.cantidad_vagones">
            Todos los vagones han sido agregados.
          </p>
          <p v-else>
            Se han agregado más vagones de los permitidos. Por favor,
            elimina los excedentes.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import NavbarComponent from "@/components/NavbarComponent.vue";
import ModalAgregarProducto from "@/components/ModalAgregarProducto.vue";
export default {
  name: "EditarEnTren",
  components: {
    NavbarComponent,
    ModalAgregarProducto,
  },
  data() {
    return {
      formData: {
        locomotora: "",
        tipo_origen: "ac_ccd",
        origen: "",
        tipo_equipo: "",
        estado: "cargado",
        tipo_destino: "ac_ccd",
        destino: "",
        producto: [],
        observaciones: "",
        equipo_vagon: [],
        cantidad_vagones: 0,
      },
      productoSearch: "",
      filteredProductos: [],
      showProductosDropdown: false,
      mostrarModal: false,
      productos: [],
      equipos: [],
      equipos_vagones: [],
      locomotoras: [],
      puertos: [],
      entidades: [],
      vagon: [],
      vagonesAgregados: [],
      numeroIdentificacionSeleccionado: null,
    };
  },
  computed: {
    formattedFechaRegistro() {
      if (this.formData.fecha) {
        return new Date(this.formData.fecha).toLocaleString();
      }
      return new Date().toLocaleString();
    },
  },

  async mounted() {
    this.getProductos();
    this.getLocomotoras();
    this.getEntidades();
    this.getPuertos();
    this.filteredProductos = this.productos;
    this.closeDropdownsOnClickOutside();
    this.getEquipos();
    await this.getTren();
    await this.buscarEquipos();
  },

  methods: {
    confirmCancel() {
      Swal.fire({
        title: "¿Está seguro de que quiere cancelar la operación?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        cancelmButtonText: "Cancelar",
        confirmButtonText: "Aceptar",
      }).then((result) => {
        if (result.isConfirmed) {
          window.history.back();
        }
      });
    },

    resetForm() {
      // Restablece los valores del formulario
      this.formData = {
        locomotora: "puerto",
        tipo_origen: "acc_d",
        origen: "",
        tipo_equipo: "",
        estado: "cargado",
        tipo_destino: "ac_ccd",
        destino: "",
        producto: "",
        observaciones: "",
        equipo_vagon: "",
      };

      // Restablecer el número de identificación seleccionado

      // Opcional: Limpiar el localStorage si es necesario
    },
    async getTren() {
      const vagon_id = this.$route.params.id;
      try {
        const response = await axios.get(`/ufc/en-trenes/${vagon_id}/`);
        this.vagon = response.data;
        this.formData = {
          ...this.vagon,
          producto: this.vagon.producto ? [this.vagon.producto] : [],
        };
        this.formData.producto = [];
      } catch (error) {
        console.error("Error al obtener el vagon:", error);
      }
    },

    async submitForm() {
      try {
        console.log(this.formData.producto);
        const vagonesJson = localStorage.getItem("vagonesAgregados");
        const vagones = JSON.parse(vagonesJson);
        const vagon_id = this.$route.params.id;
        this.formData.equipo_vagon = vagones.map((vagon) => vagon.vagon_id);
        console.log("Este es el Form", this.formData);
        await axios.post(`/ufc/en-trenes/${vagon_id}/`, this.formData);

        Swal.fire({
          title: "¡Éxito!",
          text: "El formulario ha sido actualizado correctamente",
          icon: "success",
          confirmButtonText: "Aceptar",
        });
        this.$router.push({ name: "InfoOperativo" });
      } catch (error) {
        console.error("Error al actualizar:", error);
        Swal.fire({
          title: "Error",
          text: error.response?.data?.detail || "Error al actualizar",
          icon: "error",
          confirmButtonText: "Entendido",
        });
      }
    },

    onVagonChange(event) {
      const selectedId = this.formData.equipo_vagon;
      const selectedVagon = this.equipos_vagones.find(
        (vagon) => vagon.id === selectedId
      );
      if (selectedVagon) {
        this.numeroIdentificacionSeleccionado =
          selectedVagon.numero_identificacion;
        console.log(
          "Número de identificación seleccionado:",
          this.numeroIdentificacionSeleccionado
        );
      } else {
        this.numeroIdentificacionSeleccionado = null;
      }
    },

    async getLocomotoras() {
      try {
        let allLocomotoras = [];
        let nextPage ="/api/equipos_ferroviarios/?id_tipo_equipo_territorio=locomo";
        while (nextPage) {
          const response = await axios.get(nextPage);
          allLocomotoras = [...allLocomotoras, ...response.data.results];
          nextPage = response.data.next;
        }
        this.locomotoras = allLocomotoras;
      } catch (error) {
        console.error("Error al obtener las Locomotoras:", error);
        Swal.fire(
          "Error",
          "Hubo un error al obtener las Locomotoras.",
          "error"
        );
      }
    },
    async buscarEquipos() {
      const tipo_equipo_buscar = this.formData.tipo_equipo;
      try {
        let peticion = await axios.get(
          `/api/e-f-no-locomotora/?tipo_equipo=${tipo_equipo_buscar}`
        );
        this.equipos_vagones = peticion.data;
      } catch (error) {
        console.error("Error al obtener los equipos:", error);
        Swal.fire("Error", "Hubo un error al obtener los equipos.", "error");
      }
    },
    async getEntidades() {
      try {
        let allEntidades = [];
        let nextPage = "/api/entidades/";
        while (nextPage) {
          const response = await axios.get(nextPage);
          allEntidades = [...allEntidades, ...response.data.results];
          nextPage = response.data.next;
        }
        this.entidades = allEntidades;
      } catch (error) {
        console.error("Error al obtener las entidades:", error);
        Swal.fire("Error", "Hubo un error al obtener las entidades.", "error");
      }
    },
    volverEnTren() {
      this.$router.push({ name: "InfoOperativo" });
    },
    async getPuertos() {
      try {
        let allPuertos = [];
        let nextPage = "/api/puertos/";
        while (nextPage) {
          const response = await axios.get(nextPage);
          allPuertos = [...allPuertos, ...response.data.results];
          nextPage = response.data.next;
        }
        this.puertos = allPuertos;
      } catch (error) {
        console.error("Error al obtener los puertos:", error);
        Swal.fire("Error", "Hubo un error al obtener los puertos.", "error");
      }
    },
    async getEquipos() {
      try {
        const response = await axios.get("/api/tipo-e-f-no-locomotora/");
        this.equipos = response.data;
      } catch (error) {
        console.error("Error al obtener los equipos:", error);
        Swal.fire("Error", "Hubo un error al obtener los equipos.", "error");
      }
    },
    async getProductos() {
      try {
        let allProductos = [];
        let nextPage = "/ufc/producto-vagon/";
        while (nextPage) {
          const response = await axios.get(nextPage);
          allProductos = [...allProductos, ...response.data.results];
          nextPage = response.data.next;
        }

        this.productos = allProductos.map((p) => {
          // Asegurar que tipo_embalaje esté definido
          const tipoEmbalaje = p.tipo_embalaje || {};
          return {
            ...p,
            tipo_embalaje: {
              nombre:
                tipoEmbalaje.nombre ||
                tipoEmbalaje.nombre_embalaje ||
                "Sin embalaje",
            },
          };
        });
        console.log(this.productos);
      } catch (error) {
        console.error("Error al obtener los productos:", error);
        Swal.fire("Error", "Hubo un error al obtener los productos.", "error");
      }
    },
    abrirModalAgregarProducto() {
      this.mostrarModal = true;
    },
    cerrarModal() {
      this.mostrarModal = false;
      this.getProductos();
    },
    agregarVagon() {
      if (this.vagonesAgregados.length >= this.formData.cantidad_vagones) {
        Swal.fire({
          title: "Error",
          text: "Ya has agregado la cantidad máxima de vagones permitida.",
          icon: "error",
          confirmButtonText: "Entendido",
        });
        return;
      }

      const datosVagon = JSON.parse(JSON.stringify(this.formData));
      const nuevoVagon = {
        vagon_id: this.formData.equipo_vagon,
        datos: datosVagon,
      };

      this.vagonesAgregados.push(nuevoVagon);
      Swal.fire({
        title: "Éxito",
        text: "Vagón agregado correctamente.",
        icon: "success",
        confirmButtonText: "Aceptar",
      });
      localStorage.setItem(
        "vagonesAgregados",
        JSON.stringify(this.vagonesAgregados)
      );
    },
    eliminarVagon(index) {
      this.vagonesAgregados.splice(index, 1);
      localStorage.setItem(
        "vagonesAgregados",
        JSON.stringify(this.vagonesAgregados)
      );
      Swal.fire({
        title: "Éxito",
        text: "Vagón eliminado correctamente.",
        icon: "success",
        confirmButtonText: "Aceptar",
      });
    },
    /* Acciones del producto */
    toggleProductosDropdown() {
      this.showProductosDropdown = !this.showProductosDropdown;
      if (this.showProductosDropdown) {
        this.productoSearch = "";
        this.filterProductos();
      }
    },

    filterProductos() {
      if (!this.productoSearch) {
        this.filteredProductos = this.productos;
        return;
      }
      const searchTerm = this.productoSearch.toLowerCase();
      this.filteredProductos = this.productos.filter(
        (producto) =>
          producto.producto_name.toLowerCase().includes(searchTerm) ||
          producto.producto_codigo.toLowerCase().includes(searchTerm) ||
          producto.id.toString().includes(searchTerm)
      );
    },

    toggleProductoSelection(productoId) {
      const index = this.formData.producto.indexOf(productoId);
      if (index === -1) {
        this.formData.producto.push(productoId);
      } else {
        this.formData.producto.splice(index, 1);
      }
    },

    getSelectedProductosText() {
      if (this.formData.producto.length === 0) return "";
      if (this.formData.producto.length === 1) {
        const producto = this.productos.find(
          (p) => p.id === this.formData.producto[0]
        );
        return producto
          ? `${producto.id}-${producto.producto_name}`
          : "1 producto seleccionado";
      }
      return `${this.formData.producto.length} productos seleccionados`;
    },

    closeDropdownsOnClickOutside() {
      document.addEventListener("click", (e) => {
        if (!e.target.closest(".ufc-custom-select")) {
          this.showProductosDropdown = false;
        }
      });
    },
    validateForm() {
      const nombre_atraque_regex = /^[A-Z][A-Za-z ]{2,99}$/;
      let errorMessage = "";

      if (!nombre_atraque_regex.test(this.nombre_atraque)) {
        errorMessage +=
          'El campo "Nombre" debe comenzar con mayúscula, seguir con letras y espacios, y tener entre 3 y 100 caracteres.\n';
      }

      if (errorMessage) {
        Swal.fire({
          icon: "error",
          title: "Error de validación",
          text: errorMessage,
        });
        return false; // Detener el envío del formulario
      }

      return true; // El formulario es válido
    },
  },
};
</script>
<style scoped>

/* Todos los estilos del primer formulario ya están incluidos */
/* Se añaden estilos adicionales específicos para este componente */
.ufc-custom-select {
  position: relative;
  width: 100%;
  cursor: pointer;
}

.ufc-select-display {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.85rem;
  background-color: white;
  min-height: 36px;
  display: flex;
  align-items: center;
   border-color: rgba(var(--bs-secondary-rgb),var(--bs-border-opacity)) !important;
}

.ufc-select-arrow {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  transition: transform 0.2s;
}

.ufc-custom-select.open .ufc-select-arrow {
  transform: translateY(-50%) rotate(180deg);
}

.ufc-productos-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  max-height: 300px;
  overflow-y: auto;
  background: white;
  border: 1px solid #ddd;
  border-radius: 0 0 6px 6px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 10;
  margin-top: 2px;
}

.ufc-productos-search-container {
  padding: 8px;
  border-bottom: 1px solid #eee;
  background: #f8f9fa;
}

.ufc-productos-search {
  width: 100%;
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.85rem;
}

.ufc-productos-search:focus {
  outline: none;
  border-color: #002a68;
}

.ufc-productos-options {
  max-height: 250px;
  overflow-y: auto;
}

.ufc-producto-option {
  padding: 8px 12px;
  font-size: 0.85rem;
  border-bottom: 1px solid #f0f0f0;
}

.ufc-producto-option:hover {
  background-color: #f5f5f5;
}

.ufc-producto-option.selected {
  background-color: #002a68;
  color: white;
}

/* Estilo para el botón de agregar */
.ufc-add-button {
  margin-left: 8px;
}

/* Para navegadores que soportan datalist */
input[list] {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.85rem;
}

.ufc-select[multiple] {
  height: auto;
  min-height: 100px;
  padding: 8px;
}

.ufc-select[multiple] option {
  padding: 6px 8px;
  margin: 2px 0;
  border-radius: 4px;
}

.ufc-select[multiple] option:checked {
  background-color: #002a68;
  color: white;
}

.ufc-form-container {
  font-family: "Segoe UI", Roboto, -apple-system, sans-serif;
  color: #333;
  padding-bottom: 20px;
}

.ufc-header {
  background-color: #002a68;
  color: white;
  text-align: right;
  padding: 10px 15px;
  margin-bottom: 20px;
}

.ufc-header h6 {
  margin: 0;
  font-size: 1rem;
  font-weight: 500;
}

.ufc-form-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 15px;
}

.ufc-form-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.ufc-form-title {
  color: #002a68;
  font-size: 1.3rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}

.ufc-form-title i {
  font-size: 1.4rem;
}

.ufc-form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

@media (max-width: 768px) {
  .ufc-form-grid {
    grid-template-columns: 1fr;
  }
}

.ufc-input-group {
  margin-bottom: 15px;
}

.ufc-input-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 0.85rem;
  font-weight: 500;
  color: #444;
}

.ufc-input-group .required {
  color: #e74c3c;
}

.ufc-select,
.ufc-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.85rem;
  transition: all 0.2s;
  background-color: white;
}

.ufc-select:focus,
.ufc-input:focus {
  border-color: #002a68;
  box-shadow: 0 0 0 3px rgba(0, 42, 104, 0.1);
  outline: none;
}

.ufc-textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  resize: vertical;
  min-height: 70px;
  font-family: inherit;
  font-size: 0.85rem;
}

.ufc-textarea:focus {
  border-color: #002a68;
  box-shadow: 0 0 0 3px rgba(0, 42, 104, 0.1);
  outline: none;
}

.ufc-input-with-action {
  display: flex;
  gap: 8px;
}

.ufc-add-button {
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  width: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #002a68;
  transition: all 0.2s;
}

.ufc-add-button:hover {
  background: #e9ecef;
  color: #001a3d;
}

.ufc-add-button i {
  font-size: 1.1rem;
}

.ufc-disabled {
  font-size: 0.8rem;
  color: #777;
  padding: 8px 0;
}

/* Estilo especial para el campo por situar */
.ufc-por-situar-container {
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 6px;
  overflow: hidden;
}

.ufc-por-situar-input {
  flex: 1;
  border: none;
  padding: 8px 12px;
  font-size: 0.85rem;
  min-width: 0;
}

.ufc-por-situar-suffix {
  background: #f8f9fa;
  padding: 8px 12px;
  font-size: 0.8rem;
  color: #666;
  border-left: 1px solid #ddd;
}

/* Botones de acción */
.ufc-form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.ufc-button {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 1 rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  display: flex;
  align-items: center;
  gap: 6px;
}

.ufc-button.primary:hover {
  background: #003d8f;
}

.ufc-button.secondary {
    background:rgb(241, 81, 63);
    color: white;
}

.ufc-button.secondary:hover {
    background:rgb(228, 56, 37);
}

.create-button {
  text-decoration: none;
  color: green;
  margin-left: 940px;
}

button {
  margin-left: 10px;
  padding: 5px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

button[type="button"] {
  background-color: #007bff;
  color: white;
}

button[type="submit"] {
  margin-left: 15px;
  background-color: #007bff;
  color: white;
}

/* Estilos para selects */
.ufc-select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 12px;
}

/* Estilos para el modal */
.ufc-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.ufc-modal-container {
  background: white;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow: auto;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
  animation: modalFadeIn 0.3s ease-out;
}

.ufc-modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #002a68;
  color: white;
  border-radius: 10px 10px 0 0;
}

.ufc-modal-header h3 {
  margin: 0;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.ufc-modal-close {
  background: transparent;
  border: none;
  color: white;
  font-size: 1.3rem;
  cursor: pointer;
  padding: 5px;
  transition: all 0.2s;
}

.ufc-modal-close:hover {
  color: #ccc;
}

.ufc-modal-body {
  padding: 20px;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.ufc-vagones-agregados {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.ufc-subtitle {
  color: #002a68;
  font-size: 1.1rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.ufc-table-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

.ufc-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

.ufc-table th {
  background-color: #f8f9fa;
  padding: 10px;
  text-align: left;
  border-bottom: 2px solid #ddd;
  color: #555;
}

.ufc-table td {
  padding: 10px;
  border-bottom: 1px solid #eee;
  vertical-align: middle;
}

.ufc-table tr:hover {
  background-color: #f5f5f5;
}

.ufc-button-sm {
  padding: 5px 10px;
  font-size: 0.8rem;
}

.ufc-button.danger {
  background-color: #e74c3c;
  color: white;
}

.ufc-button.danger:hover {
  background-color: #c0392b;
}

.ufc-validation-message {
  padding: 10px;
  border-radius: 6px;
  font-size: 0.85rem;
  margin-top: 10px;
}

.ufc-validation-message.warning {
  background-color: #fff3cd;
  color: #856404;
  border-left: 4px solid #ffeeba;
}

.ufc-validation-message.success {
  background-color: #d4edda;
  color: #155724;
  border-left: 4px solid #c3e6cb;
}

.ufc-validation-message.error {
  background-color: #f8d7da;
  color: #721c24;
  border-left: 4px solid #f5c6cb;
}

/* Se mantienen todos los estilos del primer formulario */
.ufc-form-container {
  font-family: "Segoe UI", Roboto, -apple-system, sans-serif;
  color: #333;
  padding-bottom: 20px;
}

.ufc-header {
  background-color: #002a68;
  color: white;
  text-align: right;
  padding: 10px 15px;
  margin-bottom: 20px;
}

.ufc-header h6 {
  margin: 0;
  font-size: 1rem;
  font-weight: 500;
}

.ufc-form-wrapper {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 15px;
}

.ufc-form-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.ufc-form-title {
  color: #002a68;
  font-size: 1.3rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}

.ufc-form-title i {
  font-size: 1.4rem;
}

.ufc-form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

@media (max-width: 768px) {
  .ufc-form-grid {
    grid-template-columns: 1fr;
  }
}

.ufc-input-group {
  margin-bottom: 15px;
}

.ufc-input-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 0.85rem;
  font-weight: 500;
  color: #444;
}

.ufc-input-group .required {
  color: #e74c3c;
}

.ufc-select,
.ufc-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.85rem;
  transition: all 0.2s;
  background-color: white;
}

.ufc-select:focus,
.ufc-input:focus {
  border-color: #002a68;
  box-shadow: 0 0 0 3px rgba(0, 42, 104, 0.1);
  outline: none;
}

.ufc-textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  resize: vertical;
  min-height: 70px;
  font-family: inherit;
  font-size: 0.85rem;
}

.ufc-textarea:focus {
  border-color: #002a68;
  box-shadow: 0 0 0 3px rgba(0, 42, 104, 0.1);
  outline: none;
}

.ufc-input-with-action {
  display: flex;
  gap: 8px;
}

.ufc-add-button {
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  width: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #002a68;
  transition: all 0.2s;
}

.ufc-add-button:hover {
  background: #e9ecef;
  color: #001a3d;
}

.ufc-add-button i {
  font-size: 1.1rem;
}

.ufc-disabled {
  font-size: 0.8rem;
  color: #777;
  padding: 8px 0;
}

/* Estilos para selects */
.ufc-select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 12px;
}

/* Estilos para el modal */
.ufc-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.ufc-modal-container {
  background: white;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow: auto;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
  animation: modalFadeIn 0.3s ease-out;
}

.ufc-modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #002a68;
  color: white;
  border-radius: 10px 10px 0 0;
}

.ufc-modal-header h3 {
  margin: 0;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.ufc-modal-close {
  background: transparent;
  border: none;
  color: white;
  font-size: 1.3rem;
  cursor: pointer;
  padding: 5px;
  transition: all 0.2s;
}

.ufc-modal-close:hover {
  color: #ccc;
}

.ufc-modal-body {
  padding: 20px;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.full-width {
  grid-column: 1 / -1;
}
</style>

