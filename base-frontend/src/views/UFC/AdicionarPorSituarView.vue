<template>
  <div class="ufc-form-container">
    <!-- Encabezado corporativo -->
    <div class="ufc-header">
      <h6>Partes UFC</h6>
    </div>

    <Navbar-Component />
    <Producto-Vagones />

    <div class="ufc-form-wrapper">
      <div class="ufc-form-card">
        <h2 class="ufc-form-title">
          <i class="bi bi-file-earmark-plus"></i> Nuevo registro por situar
        </h2>

        <form @submit.prevent="submitForm" class="ufc-form">
          <div class="ufc-form-grid">
            <!-- Columna Izquierda -->
            <div class="ufc-form-column">
              <!-- Campo:Fecha de registro -->
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
                  <option value="" disabled>Seleccione un tipo</option>
                  <option
                    v-for="item in tipo_origen_options"
                    :key="item.id"
                    :value="item.id"
                  >
                    {{ item.text }}
                  </option>
                </select>
              </div>

              <!-- Campo: origen -->
              <div class="ufc-input-group">
                <label for="origen"
                  >Origen <span class="required">*</span></label
                >
                <select
                  v-if="
                    formData.tipo_origen && formData.tipo_origen !== 'puerto'
                  "
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
                  v-else-if="formData.tipo_origen === 'puerto'"
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

                <select v-else class="ufc-select" disabled>
                  <option value="">Seleccione primero el tipo de origen</option>
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
                  required
                >
                  <option value="" disabled>Seleccione un tipo</option>
                  <option
                    v-for="option in tipo_equipo_options"
                    :key="option.id"
                    :value="option.id"
                  >
                    {{ option.text }}
                  </option>
                </select>
              </div>
            </div>

            <!-- Columna Derecha -->
            <div class="ufc-form-column">
              <!-- Campo: estado -->
              <div class="ufc-input-group">
                <label for="estado"
                  >Estado <span class="required">*</span></label
                >
                <select
                  class="ufc-select"
                  v-model="formData.estado"
                  @change="handleEstadoChange"
                  required
                >
                  <option value="cargado">Cargado</option>
                  <option value="vacio">Vacío</option>
                </select>
              </div>

              <!-- Campo: operacion -->
              <div class="ufc-input-group">
                <label for="operacion"
                  >Operación <span class="required">*</span></label
                >
                <select
                  class="ufc-select"
                  v-model="formData.operacion"
                  required
                >
                  <option value="" disabled>Seleccione una operación</option>
                  <option
                    v-for="option in t_operacion_options"
                    :key="option.id"
                    :value="option.id"
                  >
                    {{ option.text }}
                  </option>
                </select>
              </div>

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
                        getSelectedProductosText() || "Seleccione productos..."
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
                            selected: formData.productos.includes(producto.id),
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

              <ModalAgregarProducto
                v-if="mostrarModal"
                :visible="mostrarModal"
                @cerrar-modal="cerrarModal"
              />

              <!-- Campo: por_situar -->
              <div class="ufc-input-group">
                <label for="por_situar"
                  >Por Situar <span class="required">*</span></label
                >
                <div class="ufc-por-situar-container">
                  <input
                    type="number"
                    class="ufc-por-situar-input"
                    v-model.number="formData.por_situar"
                    min="1"
                    required
                    readonly
                  />
                  <span class="ufc-por-situar-suffix">unidades</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Observaciones (full width) -->
          <div class="ufc-input-group full-width">
            <label for="observaciones">Observaciones</label>
            <textarea
              class="ufc-textarea"
              v-model="formData.observaciones"
              rows="2"
            ></textarea>
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
            <button type="submit" class="ufc-button primary">
              <i class="bi bi-check-circle"></i> Agregar
            </button>
          </div>
        </form>
      </div>

      <!-- Tabla de Vagones Asociados (FUERA del formulario) -->
      <div class="ufc-vagones-card">
        <div class="ufc-vagones-header">
          <h3><i class="bi bi-train-freight-front"></i> Vagones Asociados</h3>
          <div>
            <span class="ufc-vagones-count">
              {{ vagonesAsociados.length }} / {{ formData.por_situar }}
            </span>
            <button
              class="ufc-button primary small"
              @click="abrirModalAgregarVagon"
              :disabled="vagonesAsociados.length >= formData.por_situar"
            >
              <i class="bi bi-plus-circle"></i> Agregar Vagón
            </button>
          </div>
        </div>

        <!-- Tabla cuando hay datos -->
        <div
          v-if="vagonesAsociados.length > 0"
          class="ufc-vagones-table-container"
        >
          <table class="ufc-vagones-table">
            <thead>
              <tr>
                <th>Equipo Ferroviario</th>
                <th>Días</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(vagon, index) in vagonesAsociados" :key="index">
                <td>{{ vagon.equipo_ferroviario_nombre }}</td>
                <td>{{ vagon.dias }}</td>
                <td class="ufc-actions-cell">
                  <button
                    class="ufc-icon-button danger"
                    @click="eliminarVagon(index)"
                    title="Eliminar"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Mensaje cuando no hay datos -->
        <div v-else class="ufc-vagones-empty">
          <div class="ufc-empty-state">
            <i class="bi bi-train-freight-front"></i>
            <p>No hay vagones asociados</p>
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

    <!-- Modal para agregar/editar vagón -->
    <div v-if="mostrarModalVagon" class="ufc-modal-overlay">
      <div class="ufc-modal-container">
        <div class="ufc-modal-header">
          <h3>
            <i class="bi bi-train-freight-front"></i>
            {{ modoEdicionVagon ? "Editar Vagón" : "Agregar Vagón" }}
          </h3>
          <button @click="cerrarModal" class="ufc-modal-close">
            <i class="bi bi-x"></i>
          </button>
        </div>
        <div class="ufc-modal-body">
          <form @submit.prevent="guardarVagon" class="ufc-modal-form">
            <div class="ufc-input-group">
              <label for="equipo_ferroviario"
                >Equipo Ferroviario <span class="required">*</span></label
              >
              <select
                class="ufc-select"
                v-model="vagonForm.equipo_ferroviario"
                required
              >
                <option value="" disabled>Seleccione un equipo</option>
                <option
                  v-for="equipo in equiposFerroviarios"
                  :key="equipo.id"
                  :value="equipo.id"
                >
                  {{ equipo.numero_identificacion }} -
                  {{ equipo.tipo_equipo.tipo_equipo }}
                </option>
              </select>
            </div>

            <div class="ufc-input-group">
              <label for="dias">Días <span class="required">*</span></label>
              <input
                type="number"
                class="ufc-input"
                v-model.number="vagonForm.dias"
                min="1"
                required
              />
            </div>

            <div class="ufc-modal-actions">
              <button
                type="button"
                class="ufc-button secondary"
                @click="cerrarModal"
              >
                Cancelar
              </button>
              <button type="submit" class="ufc-button primary">
                {{ modoEdicionVagon ? "Guardar Cambios" : "Agregar" }}
              </button>
            </div>
          </form>
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
  name: "AdicionarPorSituar",
  components: {
    NavbarComponent,
    ModalAgregarProducto,
  },
  data() {
    return {
      formData: {
        tipo_origen: "",
        origen: "",
        tipo_equipo: "",
        operacion: "",
        estado: "cargado",
        productos: [],
        por_situar: 1,
        observaciones: "",
      },
      productoSearch: "",
      filteredProductos: [],
      showProductosDropdown: false,
      entidades: [],
      puertos: [],
      productos: [],
      loading: false,
      mostrarModal: false,
      tipo_origen_options: [
        { id: "ac_ccd", text: "comercial/AccesoCCD" },
        { id: "puerto", text: "Puerto" },
      ],
      tipo_equipo_options: [
        { id: "casilla", text: "Casilla" },
        { id: "caj_gon", text: "Cajon o Gondola" },
      ],
      t_operacion_options: [
        { id: "carga", text: "Carga" },
        { id: "descarga", text: "Descarga" },
      ],
      vagonesAsociados: [], // Aquí se almacenarán los vagones antes de enviar
      equiposFerroviarios: [], // Lista de equipos disponibles
      mostrarModalVagon: false,
      vagonForm: {
        equipo_ferroviario: "",
        dias: 1,
      },
      vagonEditIndex: null,
      modoEdicionVagon: false,
    };
  },
  mounted() {
    this.getProductos();
    this.getEntidades();
    this.getPuertos();
    this.filteredProductos = this.productos;
    this.closeDropdownsOnClickOutside();
  },
  computed: {
    formattedFechaRegistro() {
      return new Date().toLocaleString("es-ES", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },
  },
  methods: {
    async abrirModalAgregarVagon() {
      try {
        // Cargar equipos ferroviarios disponibles
        const response = await axios.get("/api/e-f-no-locomotora/");

        // Filtrar equipos que no estén ya en la lista de vagones asociados
        const equiposDisponibles = response.data;

        this.equiposFerroviarios = equiposDisponibles;

        if (this.equiposFerroviarios.length === 0) {
          Swal.fire({
            title: "No hay equipos disponibles",
            text: "Todos los equipos ferroviarios ya están asociados o no hay equipos activos",
            icon: "info",
          });
          return;
        }

        this.modoEdicionVagon = false;
        this.vagonForm = {
          equipo_ferroviario: this.equiposFerroviarios[0]?.id || "",
          dias: 1,
        };
        this.mostrarModalVagon = true;
      } catch (error) {
        console.error("Error al cargar equipos:", error);
        Swal.fire(
          "Error",
          "No se pudieron cargar los equipos ferroviarios",
          "error"
        );
      }
    },

    guardarVagon() {
      // Validación
      if (
        !this.vagonForm.equipo_ferroviario ||
        !this.vagonForm.dias ||
        this.vagonForm.dias < 1
      ) {
        Swal.fire("Error", "Complete todos los campos correctamente", "error");
        return;
      }

      // Buscar el equipo seleccionado para obtener su nombre
      const equipoSeleccionado = this.equiposFerroviarios.find(
        (e) => e.id === this.vagonForm.equipo_ferroviario
      );

      if (!equipoSeleccionado) {
        Swal.fire("Error", "No se encontró el equipo seleccionado", "error");
        return;
      }

      const vagonData = {
        equipo_ferroviario: this.vagonForm.equipo_ferroviario,
        equipo_ferroviario_nombre: `${equipoSeleccionado.numero_identificacion} - ${equipoSeleccionado.tipo_equipo.tipo_equipo}`,
        dias: this.vagonForm.dias,
      };

      if (this.modoEdicionVagon) {
        // Editar existente
        this.vagonesAsociados[this.vagonEditIndex] = vagonData;
        Swal.fire("Actualizado", "El vagón ha sido actualizado", "success");
      } else {
        // Agregar nuevo
        this.vagonesAsociados.push(vagonData);
        Swal.fire("Agregado", "El vagón ha sido agregado", "success");
      }

      // Actualizar el campo por_situar automáticamente
      this.formData.por_situar = this.vagonesAsociados.length;

      this.cerrarModal();
    },

    eliminarVagon(index) {
      Swal.fire({
        title: "¿Eliminar vagón?",
        text: "Esta acción no se puede deshacer",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#002a68",
        cancelButtonColor: "#6c757d",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
      }).then((result) => {
        if (result.isConfirmed) {
          this.vagonesAsociados.splice(index, 1);
          // Actualizar el campo por_situar automáticamente
          this.formData.por_situar = this.vagonesAsociados.length;
          Swal.fire("Eliminado", "El vagón ha sido eliminado", "success");
        }
      });
    },

    async verificarInformeOperativo() {
      try {
        const today = new Date();
        const fechaFormateada = `${today.getFullYear()}-${String(
          today.getMonth() + 1
        ).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;

        const response = await axios.get("/ufc/verificar-informe-existente/", {
          params: { fecha_operacion: fechaFormateada },
        });

        if (response.data.existe) {
          this.informeOperativoId = response.data.id;
          return true;
        }
        return false;
      } catch (error) {
        console.error("Error al verificar informe:", error);
        return false;
      }
    },

    async getEntidades() {
      try {
        const response = await axios.get("/api/entidades/");
        this.entidades = response.data.results;
      } catch (error) {
        console.error("Error al obtener entidades:", error);
        Swal.fire("Error", "No se pudieron obtener las entidades", "error");
      }
    },

    async getProductos() {
      this.loading = true;
      try {
        const response = await axios.get("/ufc/producto-vagon/", {
          params: {
            include_details: true,
            estado: "activo", // Solo productos activos
          },
        });

        this.productos = response.data.results.map((p) => {
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
        this.filteredProductos = this.productos;
      } catch (error) {
        console.error("Error al obtener productos:", error);
        Swal.fire("Error", "No se pudieron cargar los productos", "error");
      } finally {
        this.loading = false;
      }
    },

    async getPuertos() {
      try {
        const response = await axios.get("/api/puertos/", {
          params: {
            estado: "activo", // Solo puertos activos
          },
        });
        this.puertos = response.data.results;
      } catch (error) {
        console.error("Error al obtener los puertos:", error);
        Swal.fire("Error", "Hubo un error al obtener los puertos.", "error");
      }
    },

    abrirModalAgregarProducto() {
      this.mostrarModal = true;
    },

    cerrarModal() {
      this.mostrarModalVagon = false;
      this.getProductos(); // Refrescar la lista de productos
    },

    handleEstadoChange() {
      // Si el estado cambia a vacío, limpiar los productos seleccionados
      if (this.formData.estado === "vacio") {
        this.formData.productos = [];
      }
    },

    async submitForm() {
      // Validación básica del formulario
      if (!this.formData.tipo_origen) {
        Swal.fire("Error", "El campo Tipo de Origen es requerido", "error");
        return;
      }

      if (!this.formData.origen) {
        Swal.fire("Error", "El campo Origen es requerido", "error");
        return;
      }

      if (!this.formData.tipo_equipo) {
        Swal.fire("Error", "El campo Tipo de Equipo es requerido", "error");
        return;
      }

      if (!this.formData.operacion) {
        Swal.fire("Error", "El campo Operación es requerido", "error");
        return;
      }

      if (
        this.formData.estado === "cargado" &&
        this.formData.productos.length === 0
      ) {
        Swal.fire(
          "Error",
          "Debe seleccionar al menos un producto cuando el estado es Cargado",
          "error"
        );
        return;
      }

      if (!this.formData.por_situar || this.formData.por_situar < 1) {
        Swal.fire(
          "Error",
          "La cantidad por situar debe ser al menos 1",
          "error"
        );
        return;
      }

      // Verificar informe operativo
      const existeInforme = await this.verificarInformeOperativo();
      if (!existeInforme) {
        Swal.fire(
          "Error",
          "No existe un informe operativo creado para la fecha actual. Debe crear uno primero.",
          "error"
        );
        this.$router.push({ name: "InfoOperativo" });
        return;
      }

      if (this.vagonesAsociados.length !== this.formData.por_situar) {
        Swal.fire({
          title: "Advertencia",
          text: `El número de vagones asociados (${this.vagonesAsociados.length}) no coincide con la cantidad "Por Situar" (${this.formData.por_situar}). ¿Desea actualizar el campo "Por Situar" para que coincida?`,
          icon: "warning",
          showCancelButton: true,
          confirmButtonText: "Sí, actualizar",
          cancelButtonText: "No, corregir manualmente",
        }).then((result) => {
          if (result.isConfirmed) {
            this.formData.por_situar = this.vagonesAsociados.length;
          }
        });
        return;
      }

      try {
        // Preparar los datos para enviar
        const payload = {
          tipo_origen: this.formData.tipo_origen,
          origen: this.formData.origen,
          tipo_equipo: this.formData.tipo_equipo,
          operacion: this.formData.operacion,
          estado: this.formData.estado,
          producto: this.formData.productos,
          por_situar: this.formData.por_situar,
          observaciones: this.formData.observaciones,
          informe_operativo: this.informeOperativoId,
          vagones: this.vagonesAsociados.map((v) => ({
            equipo_ferroviario: v.equipo_ferroviario,
            dias: v.dias,
          })),
        };

        // Enviar los datos al backend
        const response = await axios.post("/ufc/por-situar/", payload);

        // Mostrar mensaje de éxito
        await Swal.fire({
          title: "¡Éxito!",
          text: "El registro ha sido creado correctamente",
          icon: "success",
          confirmButtonText: "Aceptar",
        });

        // Resetear el formulario después de enviar
        this.resetForm();
        this.$router.push({ name: "InfoOperativo" });
      } catch (error) {
        console.error("Error al enviar el formulario:", error);

        let errorMessage = "Hubo un error al enviar el formulario";
        if (error.response) {
          // Error de respuesta del servidor
          if (error.response.data) {
            if (typeof error.response.data === "object") {
              errorMessage = Object.values(error.response.data).join("\n");
            } else {
              errorMessage = error.response.data;
            }
          }
        } else if (error.message) {
          // Error de validación
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
    async verificarEstadoInforme() {
      try {
        if (!this.informeOperativoId) return false;

        const response = await axios.get(
          `/ufc/informe-operativo/${this.informeOperativoId}/`
        );
        return response.data.estado_parte !== "Aprobado";
      } catch (error) {
        console.error("Error al verificar estado del informe:", error);
        return false;
      }
    },

    resetForm() {
      this.formData = {
        tipo_origen: "",
        origen: "",
        tipo_equipo: "",
        operacion: "",
        estado: "cargado",
        productos: [],
        por_situar: 1,
        observaciones: "",
      };
      this.vagonesAsociados = [];
    },

    confirmCancel() {
      Swal.fire({
        title: "¿Cancelar operación?",
        text: "Los datos no guardados se perderán",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, cancelar",
        cancelButtonText: "No, continuar",
        confirmButtonColor: "#002a68",
        cancelButtonColor: "#6c757d",
      }).then((result) => {
        if (result.isConfirmed) {
          this.resetForm();
          this.$router.push({ name: "InfoOperativo" });
        }
      });
    },

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
      const index = this.formData.productos.indexOf(productoId);
      if (index === -1) {
        this.formData.productos.push(productoId);
      } else {
        this.formData.productos.splice(index, 1);
      }
    },

    getSelectedProductosText() {
      if (this.formData.productos.length === 0) return "";

      const selectedProducts = this.productos.filter((p) =>
        this.formData.productos.includes(p.id)
      );

      if (selectedProducts.length === 1) {
        return `${selectedProducts[0].id}-${selectedProducts[0].producto_name}`;
      }

      return `${this.formData.productos.length} productos seleccionados`;
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
/* Estilos base */
.ufc-form-container {
  font-family: "Segoe UI", Roboto, -apple-system, sans-serif;
  color: #333;
  padding-bottom: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
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
  padding: 25px;
  margin-bottom: 20px;
}

.ufc-vagones-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 25px;
  margin-bottom: 30px;
}

.ufc-form-title {
  color: #002a68;
  font-size: 1.3rem;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.ufc-form-title i {
  font-size: 1.4rem;
}

.ufc-form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

@media (max-width: 768px) {
  .ufc-form-grid {
    grid-template-columns: 1fr;
  }
}

.ufc-input-group {
  margin-bottom: 20px;
}

.ufc-input-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #444;
}

.ufc-input-group .required {
  color: #e74c3c;
}

.ufc-select,
.ufc-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
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
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
  font-size: 0.9rem;
}

.ufc-textarea:focus {
  border-color: #002a68;
  box-shadow: 0 0 0 3px rgba(0, 42, 104, 0.1);
  outline: none;
}

.ufc-input-with-action {
  display: flex;
  gap: 10px;
}

.ufc-add-button {
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  width: 42px;
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
  font-size: 1.2rem;
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
  padding: 10px 12px;
  font-size: 0.9rem;
  min-width: 0;
}

.ufc-por-situar-suffix {
  background: #f8f9fa;
  padding: 10px 12px;
  font-size: 0.85rem;
  color: #666;
  border-left: 1px solid #ddd;
}

/* Botones de acción */
.ufc-form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.ufc-button {
  padding: 10px 20px;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  display: flex;
  align-items: center;
  gap: 8px;
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

.ufc-button.small {
  padding: 8px 15px;
  font-size: 0.85rem;
}

/* Estilos para el select con búsqueda */
.ufc-custom-select {
  position: relative;
  width: 100%;
  cursor: pointer;
}

.ufc-select-display {
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
  background-color: white;
  min-height: 42px;
  display: flex;
  align-items: center;
}

.ufc-select-arrow {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  transition: transform 0.2s;
  color: #666;
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
  padding: 10px;
  border-bottom: 1px solid #eee;
  background: #f8f9fa;
}

.ufc-productos-search {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
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
  padding: 10px 12px;
  font-size: 0.9rem;
  border-bottom: 1px solid #f0f0f0;
  transition: all 0.1s;
}

.ufc-producto-option:hover {
  background-color: #f5f5f5;
}

.ufc-producto-option.selected {
  background-color: #002a68;
  color: white;
}

/* Estilos para la sección de vagones asociados */
.ufc-vagones-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.ufc-vagones-header h3 {
  color: #002a68;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

.ufc-vagones-table-container {
  overflow-x: auto;
  margin-bottom: 20px;
  border: 1px solid #eee;
  border-radius: 8px;
}

.ufc-vagones-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.ufc-vagones-table th {
  background-color: #002a68;
  color: white;
  padding: 12px 15px;
  text-align: left;
  font-weight: 500;
  font-size: 0.9rem;
}

.ufc-vagones-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
  font-size: 0.9rem;
}

.ufc-vagones-table tr:last-child td {
  border-bottom: none;
}

.ufc-vagones-table tr:hover {
  background-color: #f8f9fa;
}

.ufc-actions-cell {
  display: flex;
  gap: 10px;
}

.ufc-icon-button {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.ufc-icon-button i {
  font-size: 1rem;
}

.ufc-icon-button.danger {
  background-color: #dc3545;
  color: white;
}

.ufc-icon-button.danger:hover {
  background-color: #c82333;
}

/* Estilo para estado vacío */
.ufc-vagones-empty {
  margin-top: 20px;
  text-align: center;
  padding: 40px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px dashed #ddd;
}

.ufc-empty-state {
  color: #6c757d;
}

.ufc-empty-state i {
  font-size: 2.5rem;
  margin-bottom: 15px;
  color: #adb5bd;
}

.ufc-empty-state p {
  margin: 0;
  font-size: 1rem;
  color: #6c757d;
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
  font-size: 1.5rem;
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

.ufc-modal-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.ufc-modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

/* Animaciones */
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

/* Estilos responsivos */
@media (max-width: 576px) {
  .ufc-form-card,
  .ufc-vagones-card {
    padding: 15px;
  }

  .ufc-form-actions {
    flex-direction: column;
  }

  .ufc-button {
    width: 100%;
    justify-content: center;
  }

  .ufc-vagones-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .ufc-vagones-header h3 {
    margin-bottom: 10px;
  }
}
</style>
