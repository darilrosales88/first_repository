<template>
  <div class="ufc-form-container">
    <!-- Encabezado corporativo -->
    <div class="ufc-header">
      <h6>Bienvenido:</h6>
    </div>

    <Navbar-Component />
    <Producto-Vagones />
    <div class="content px-5">
      <div class="ufc-form-wrapper container px-5">
        <div class="ufc-form-card">
          <h2 class="ufc-form-title">
            <i class="bi bi-train-freight-front"></i> Nuevo registro de vagón
          </h2>

          <form @submit.prevent="submitForm" class="ufc-form">
            <div class="ufc-form-grid">
              <!-- Columna Izquierda -->
              <!-- Campo: Fecha de registro -->
              <div class="ufc-form-column">
                <div class="mb-3">
                  <label for="fecha_registro" class="form-label"
                    >Fecha de registro</label
                  >
                  <input
                    type="text"
                    class="form-control"
                    :value="formattedFechaRegistro"
                    id="fecha_registro"
                    name="fecha_registro"
                    readonly
                  />
                </div>
                <!-- Campo: locomotora -->
                <div class="ufc-input-group">
                  <label for="locomotora"
                    >Locomotora <span class="required">*</span></label
                  >
                  <select
                    class="ufc-select"
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
                  <label for="tipo_origen"
                    >Tipo de Origen <span class="required">*</span></label
                  >
                  <select
                    class="ufc-select"
                    v-model="formData.tipo_origen"
                    required
                  >
                    <option value="ac_ccd">Acceso Comercial</option>
                    <option value="puerto">Puerto</option>
                  </select>
                </div>

                <!-- Campo: origen -->
                <div class="ufc-input-group">
                  <label for="origen"
                    >Origen <span class="required">*</span></label
                  >
                  <select
                    v-if="formData.tipo_origen !== 'puerto'"
                    class="ufc-select"
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
                    class="ufc-select"
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
                  <label for="tipo_equipo"
                    >Tipo de Equipo <span class="required">*</span></label
                  >
                  <select
                    class="ufc-select"
                    v-model="formData.tipo_equipo"
                    @click="buscarEquipos"
                    required
                  >
                    <option value="" disabled>Seleccione un tipo</option>
                    <option
                      v-for="equipo in equipos"
                      :key="equipo.id"
                      :value="equipo.id"
                    >
                      {{ equipo.id }}-{{ equipo.tipo_equipo_name }}-{{
                        equipo.tipo_carga_name
                      }}
                    </option>
                  </select>
                </div>

                <!-- Campo: estado -->
                <div class="ufc-input-group">
                  <label for="estado"
                    >Estado <span class="required">*</span></label
                  >
                  <select class="ufc-select" v-model="formData.estado" required>
                    <option value="cargado">Cargado</option>
                    <option value="vacio">Vacio</option>
                  </select>
                </div>

                <!-- Campo: Vagon No ID -->
                <div class="ufc-input-group">
                  <label for="equipo_vagon"
                    >Vagon No ID <span class="required">*</span></label
                  >
                  <select
                    class="ufc-select"
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
                  <label for="tipo_destino"
                    >Tipo de Destino <span class="required">*</span></label
                  >
                  <select
                    class="ufc-select"
                    v-model="formData.tipo_destino"
                    required
                  >
                    <option value="ac_ccd">Acceso Comercial</option>
                    <option value="puerto">Puerto</option>
                  </select>
                </div>

                <!-- Campo: destino -->
                <div class="ufc-input-group">
                  <label for="destino"
                    >Destino <span class="required">*</span></label
                  >
                  <select
                    v-if="formData.tipo_destino !== 'puerto'"
                    class="ufc-select"
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
                  <label for="producto"
                    >Productos <span class="required">*</span></label
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
                    <button
                      class="ufc-add-button"
                      @click.prevent="abrirModalAgregarProducto"
                    >
                      <i class="bi bi-plus-circle"></i>
                    </button>
                  </div>
                </div>

                <!-- Modal Agregar Producto -->
                <div v-if="mostrarModal" class="ufc-modal-overlay">
                  <div class="ufc-modal-container">
                    <div class="ufc-modal-header">
                      <h3><i class="bi bi-box-seam"></i> Nuevo Producto</h3>
                      <button @click="cerrarModal" class="ufc-modal-close">
                        <i class="bi bi-x"></i>
                      </button>
                    </div>
                    <div class="ufc-modal-body">
                      <ModalAgregarProducto
                        :visible="mostrarModal"
                        @cerrar-modal="cerrarModal"
                      />
                    </div>
                  </div>
                </div>

                <!-- Campo: cantidad_vagones -->
                <div class="ufc-input-group">
                  <label for="cantidad_vagones"
                    >Cantidad de Vagones <span class="required">*</span></label
                  >
                  <input
                    type="number"
                    class="ufc-input"
                    v-model="formData.cantidad_vagones"
                    min="0"
                    required
                  />
                </div>

                <!-- Campo: observaciones -->
                <div class="ufc-input-group full-width">
                  <label for="observaciones">Observaciones</label>
                  <textarea
                    class="ufc-textarea"
                    v-model="formData.observaciones"
                    rows="3"
                  ></textarea>
                </div>
              </div>
            </div>

            <!-- Botones de acción -->
            <div class="ufc-form-actions">
              <button
                type="button"
                class="ufc-button secondary"
                @click="confirmCancel"
              >
                <i class="bi bi-x-circle"></i> Cancelar
              </button>
              <button
                type="button"
                class="ufc-button primary"
                @click="agregarVagon"
              >
                <i class="bi bi-plus-circle"></i> Agregar Vagon
              </button>
              <button
                type="button"
                class="ufc-button primary"
                @click="submitForm"
              >
                <i class="bi bi-check-circle"></i> Guardar
              </button>
            </div>
          </form>

          <!-- Sección de vagones agregados -->
          <div class="ufc-vagones-agregados">
            <h3 class="ufc-subtitle">
              <i class="bi bi-list-check"></i> Vagones agregados
            </h3>

            <div class="ufc-table-container">
              <table class="ufc-table">
                <thead>
                  <tr>
                    <th>No.</th>
                    <th>No. ID en trenes</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(vagon, index) in vagonesAgregados" :key="index">
                    <td>{{ index + 1 }}</td>
                    <td>
                      {{ vagon["datos"]["equipo_vagon"] }}
                    </td>
                    <td>
                      <button
                        class="ufc-button danger ufc-button-sm"
                        @click="eliminarVagon(index)"
                      >
                        <i class="bi bi-trash"></i> Eliminar
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Validación de cantidad de vagones -->
            <div
              class="ufc-validation-message"
              :class="{
                warning: vagonesAgregados.length < formData.cantidad_vagones,
                success: vagonesAgregados.length === formData.cantidad_vagones,
                error: vagonesAgregados.length > formData.cantidad_vagones,
              }"
            >
              <p v-if="vagonesAgregados.length < formData.cantidad_vagones">
                Faltan
                {{ formData.cantidad_vagones - vagonesAgregados.length }}
                vagones por agregar.
              </p>
              <p
                v-else-if="
                  vagonesAgregados.length === formData.cantidad_vagones
                "
              >
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

      <!-- Modal para agregar producto -->
      <div v-if="mostrarModal" class="ufc-modal-overlay">
        <div class="ufc-modal-container">
          <div class="ufc-modal-header">
            <h3><i class="bi bi-box-seam"></i> Nuevo Producto</h3>
            <button @click="cerrarModal" class="ufc-modal-close">
              <i class="bi bi-x"></i>
            </button>
          </div>
          <div class="ufc-modal-body">
            <ModalAgregarProducto
              :visible="mostrarModal"
              @cerrar-modal="cerrarModal"
            />
          </div>
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
  name: "AdicionarEnTren",
  components: {
    NavbarComponent,
    ModalAgregarProducto,
  },
  data() {
    return {
      formData: {
        locomotora: "",
        tipo_origen: "acc_d",
        origen: "",
        tipo_equipo: "",
        estado: "cargado",
        tipo_destino: "ac_ccd",
        destino: "",
        producto: [],
        cantidad_vagones: 0,
        observaciones: "",
        equipo_vagon: [],
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
  mounted() {
    this.getProductos();
    this.getEquipos();
    this.getLocomotoras();
    this.getEntidades();
    this.getPuertos();
    this.filteredProductos = this.productos;
    this.closeDropdownsOnClickOutside();
  },
  methods: {
    confirmCancel() {
      Swal.fire({
        title: "¿Cancelar operación?",
        text: "Los datos no guardados se perderán",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, cancelar",
        cancelButtonText: "No, continuar",
      }).then((result) => {
        if (result.isConfirmed) {
          this.resetForm();
          this.$router.push({ name: "InfoOperativo" });
        }
      });
    },
    resetForm() {
      this.formData = {
        locomotora: "puerto",
        tipo_origen: "acc_d",
        origen: "",
        tipo_equipo: "",
        estado: "cargado",
        tipo_destino: "ac_ccd",
        destino: "",
        producto: [],
        cantidad_vagones: 0,
        equipo_vagon: [],
        observaciones: "",
      };
      this.vagonesAgregados = [];
      this.numeroIdentificacionSeleccionado = null;
      localStorage.removeItem("vagonesAgregados");
      localStorage.removeItem("formData");
    },
    async submitForm() {
      try {
        // 1. Verificar que hay vagones agregados
        const vagonesJson = localStorage.getItem("vagonesAgregados");
        if (!vagonesJson) {
          Swal.fire({
            title: "Error",
            text: "No hay vagones para agregar",
            icon: "error",
            confirmButtonText: "Entendido",
          });
          return;
        }

        // 2. Verificar si existe un informe operativo para la fecha actual
        const today = new Date();
        const fechaFormateada = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
        
        const informeResponse = await axios.get('/ufc/verificar-informe-existente/', {
          params: { fecha_operacion: fechaFormateada }
        });

        if (!informeResponse.data.existe) {
          Swal.fire(
            "Error",
            "No existe un informe operativo creado para la fecha actual. Debe crear uno primero.",
            "error"
          );
          this.$router.push({ name: "InfoOperativo" });
          return;
        }

        // 3. Verificar que el informe no esté en estado "Aprobado"
        const informeDetalleResponse = await axios.get(`/ufc/informe-operativo/${informeResponse.data.id}/`);
        if (informeDetalleResponse.data.estado_parte === "Aprobado") {
          Swal.fire(
            "Error",
            "No se puede agregar registros a un informe operativo que ya ha sido aprobado.",
            "error"
          );
          return;
        }

        // 4. Validaciones básicas del formulario
        if (!this.formData.tipo_origen) {
          throw new Error("El campo Tipo de Origen es requerido");
        }

        if (!this.formData.origen) {
          throw new Error("El campo Origen es requerido");
        }

        if (!this.formData.tipo_equipo) {
          throw new Error("El campo Tipo de Equipo es requerido");
        }

        if (this.formData.estado === "cargado" && this.formData.producto.length === 0) {
          throw new Error("Debe seleccionar al menos un producto cuando el estado es Cargado");
        }

        if (!this.formData.cantidad_vagones || this.formData.cantidad_vagones < 1) {
          throw new Error("La cantidad por situar debe ser al menos 1");
        }

        // 5. Preparar datos para enviar
        const vagones = JSON.parse(vagonesJson);
        this.formData.equipo_vagon = vagones.map((vagon) => vagon.vagon_id);
        this.formData.informe_operativo = informeResponse.data.id; // Añadir el ID del informe operativo

        console.log("Datos del formulario:", this.formData);
        
        // 6. Enviar datos al backend
        await axios.post("/ufc/en-trenes-hoy/", this.formData);
        
        // 7. Mostrar éxito y resetear formulario
        Swal.fire({
          title: "¡Éxito!",
          text: "El formulario ha sido procesado correctamente",
          icon: "success",
          confirmButtonText: "Aceptar",
        });
        
        this.resetForm();
        
      } catch (error) {
        console.error("Error al enviar el formulario:", error);

        let errorMessage = "Hubo un error al enviar el formulario";
        if (error.response) {
          if (error.response.data) {
            errorMessage = error.response.data.non_field_errors
              ? error.response.data.non_field_errors[0]
              : Object.values(error.response.data).join("\n");
          }
        } else if (error.message) {
          errorMessage = error.message;
        }

        Swal.fire({
          title: "Error",
          text: errorMessage,
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
        let nextPage =
          "/api/equipos_ferroviarios/?id_tipo_equipo_territorio=locomo";
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
      try {
        let peticion = `/api/equipos_ferroviarios/?id_tipo_equipo_territorio=${this.formData["tipo_equipo"]}`;
        let allEquipos = [];
        while (peticion) {
          const response = await axios.get(peticion);
          allEquipos = [...allEquipos, ...response.data.results];
          peticion = response.data.next;
        }
        this.equipos_vagones = allEquipos;
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
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  display: flex;
  align-items: center;
  gap: 6px;
}

.ufc-button.primary {
  background: #002a68;
  color: white;
}

.ufc-button.primary:hover {
  background: #003d8f;
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.ufc-button.secondary {
  background: white;
  color: #555;
  border: 1px solid #ddd;
}

.ufc-button.secondary:hover {
  background: #f8f9fa;
  border-color: #ccc;
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
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  display: flex;
  align-items: center;
  gap: 6px;
}

.ufc-button.primary {
  background: #002a68;
  color: white;
}

.ufc-button.primary:hover {
  background: #003d8f;
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.ufc-button.secondary {
  background: white;
  color: #555;
  border: 1px solid #ddd;
}

.ufc-button.secondary:hover {
  background: #f8f9fa;
  border-color: #ccc;
}

.ufc-button.danger {
  background: #e74c3c;
  color: white;
}

.ufc-button.danger:hover {
  background: #c0392b;
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
