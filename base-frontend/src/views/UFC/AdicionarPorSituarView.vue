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
                  @change="buscarEquipos"
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
        <!-- Agrega esto justo antes de la sección de vagones agregados -->
        <div class="ufc-form-actions" style="margin-bottom: 20px">
          <button
            type="button"
            class="ufc-button primary"
            @click="mostrarModalVagon = true"
          >
            <i class="bi bi-plus-circle"></i> Adicionar Vagón
          </button>
        </div>

        <!-- Modal para agregar vagón -->
        <div v-if="mostrarModalVagon" class="ufc-modal-overlay">
          <div class="ufc-modal-container">
            <div class="ufc-modal-header">
              <h3><i class="bi bi-train-freight-front"></i> Agregar Vagón</h3>
              <button @click="cerrarModalVagon" class="ufc-modal-close">
                <i class="bi bi-x"></i>
              </button>
            </div>
            <div class="ufc-modal-body">
              <div class="ufc-form-grid">
                <!-- Campo: Equipo Ferroviario -->
                <div class="ufc-input-group">
                  <label for="equipo_ferroviario"
                    >Equipo Ferroviario <span class="required">*</span></label
                  >
                  <select
                    class="ufc-select"
                    v-model="nuevoVagon.equipo_ferroviario"
                    required
                  >
                    <option value="" disabled>Seleccione un equipo</option>
                    <option
                      v-for="equipo in equipos_vagones"
                      :key="equipo.id"
                      :value="equipo.id"
                    >
                      {{ equipo.numero_identificacion }} -
                      {{ equipo.tipo_equipo_name }}
                    </option>
                  </select>
                </div>

                <!-- Campo: Cantidad de días -->
                <div class="ufc-input-group">
                  <label for="cant_dias"
                    >Cantidad de días <span class="required">*</span></label
                  >
                  <input
                    type="number"
                    class="ufc-input"
                    v-model.number="nuevoVagon.cant_dias"
                    min="1"
                    required
                  />
                </div>
              </div>

              <!-- Botones del modal -->
              <div class="ufc-form-actions">
                <button
                  type="button"
                  class="ufc-button secondary"
                  @click="cerrarModalVagon"
                >
                  <i class="bi bi-x-circle"></i> Cancelar
                </button>
                <button
                  type="button"
                  class="ufc-button primary"
                  @click="agregarNuevoVagon"
                  :disabled="
                    !nuevoVagon.equipo_ferroviario || !nuevoVagon.cant_dias
                  "
                >
                  <i class="bi bi-check-circle"></i> Agregar
                </button>
              </div>
            </div>
          </div>
        </div>

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
                  <th>Cant. días</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(vagon, index) in vagonesAgregados" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td>
                    {{
                      vagon.datos?.equipo_vagon ||
                      vagon.equipo_ferroviario.numero_identificacion
                    }}
                  </td>
                  <td>
                    {{ vagon.cant_dias }}
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
              warning: vagonesAgregados.length < formData.por_situar,
              success: vagonesAgregados.length === formData.por_situar,
              error: vagonesAgregados.length > formData.por_situar,
            }"
          >
            <p v-if="vagonesAgregados.length < formData.por_situar">
              Faltan
              {{ formData.por_situar - vagonesAgregados.length }}
              vagones por agregar.
            </p>
            <p v-else-if="vagonesAgregados.length === formData.por_situar">
              Todos los vagones han sido agregados.
            </p>
            <p v-else>
              Se han agregado más vagones de los permitidos. Por favor, elimina
              los excedentes.
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
        equipos_vagones: [],
      },
      productoSearch: "",
      filteredProductos: [],
      showProductosDropdown: false,
      entidades: [],
      puertos: [],
      productos: [],
      loading: false,
      mostrarModal: false,
      equipos: [],
      equipos_vagones: [],
      mostrarModalVagon: false,
      vagonesAgregados: [],
      nuevoVagon: {
        equipo_ferroviario: "",
        cant_dias: 1,
      },

      tipo_origen_options: [
        { id: "ac_ccd", text: "comercial/AccesoCCD" },
        { id: "puerto", text: "Puerto" },
      ],
      t_operacion_options: [
        { id: "carga", text: "Carga" },
        { id: "descarga", text: "Descarga" },
      ],
    };
  },
  mounted() {
    this.getProductos();
    this.getEntidades();
    this.getPuertos();
    this.getEquipos();
    this.filteredProductos = this.productos;
    this.closeDropdownsOnClickOutside();
  },
  computed: {
    formattedFechaRegistro() {
      if (this.formData.fecha) {
        return new Date(this.formData.fecha).toLocaleString();
      }
      return new Date().toLocaleString();
    },
  },
  methods: {
    async verificarInformeOperativo() {
      try {
        this.formData.fecha = new Date().toISOString();
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
    async abrirModalVagon() {
      this.mostrarModalVagon = true;
      console.log(this.vagonesAgregados);
      if (this.equiposFerroviarios.length === 0) {
        await this.buscarEquipos();
      }
    },
    cerrarModalVagon() {
      this.mostrarModalVagon = false;
      this.nuevoVagon = {
        equipo_ferroviario: "",
        cant_dias: 1,
      };
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
    agregarNuevoVagon() {
      if (!this.nuevoVagon.equipo_ferroviario || !this.nuevoVagon.cant_dias) {
        Swal.fire("Error", "Debe completar todos los campos", "error");
        return;
      }

      const equipoSeleccionado = this.equipos_vagones.find(
        (e) => e.id === this.nuevoVagon.equipo_ferroviario
      );

      const vagonAgregado = {
        equipo_ferroviario: equipoSeleccionado,
        cant_dias: this.nuevoVagon.cant_dias,
        // Agrega otros datos necesarios para mantener consistencia
        datos: {
          equipo_vagon: equipoSeleccionado.numero_identificacion,
        },
      };

      this.vagonesAgregados.push(vagonAgregado);
      this.cerrarModalVagon();

      Swal.fire("Éxito", "Vagón agregado correctamente", "success");
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
    async buscarEquipos() {
      try {
        let url = "/api/e-f-no-locomotora/";
        if (!this.formData.tipo_equipo) {
          return;
        }

        // al tipo de equipo específico lo añadimos como parámetro
        url += `?tipo_equipo=${this.formData.tipo_equipo}`;
        const response = await axios.get(url);

        // en caso de que no exista EF para el tipo seleccionado en el componente padre
        if (response.data.length === 0) {
          Swal.fire({
            title: "Error",
            text: "No existen equipos ferroviarios para el tipo seleccionado.",
            icon: "error",
            willClose: () => {
              this.cerrarModal();
            },
          });
          return;
        }

        this.equipos_vagones = response.data;
      } catch (error) {
        console.error("Error al obtener los equipos ferroviarios:", error);
        Swal.fire({
          title: "Error",
          text: "Hubo un error al obtener los equipos ferroviarios.",
          icon: "error",
          willClose: () => {
            this.cerrarModal();
          },
        });
      }
    },

    async getProductos() {
      this.loading = true;
      try {
        const response = await axios.get("/ufc/producto-vagon/", {
          params: {
            include_details: true, // Asegúrate que tu backend incluya los datos relacionados
          },
        });

        this.productos = response.data.results.map((p) => {
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
      } catch (error) {
        console.error("Error al obtener productos:", error);
        Swal.fire("Error", "No se pudieron cargar los productos", "error");
      } finally {
        this.loading = false;
      }
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

    abrirModalAgregarProducto() {
      this.mostrarModal = true;
    },

    cerrarModal() {
      this.mostrarModal = false;
      this.getProductos();
    },

    handleEstadoChange() {
      // Eliminamos la lógica que vaciaba los productos
      // Ahora este método no hace nada con los productos
    },

    async submitForm() {
      try {
        // 1. Verificar que exista un informe operativo
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

        // 2. Verificar que el informe no esté aprobado
        const informeNoAprobado = await this.verificarEstadoInforme();
        if (!informeNoAprobado) {
          Swal.fire(
            "Error",
            "No se puede agregar registros a un informe operativo que ya ha sido aprobado.",
            "error"
          );
          return;
        }

        // Validación de campos requeridos
        if (!this.formData.tipo_origen) {
          throw new Error("El campo Tipo de Origen es requerido");
        }

        if (!this.formData.origen) {
          throw new Error("El campo Origen es requerido");
        }

        if (!this.formData.tipo_equipo) {
          throw new Error("El campo Tipo de Equipo es requerido");
        }

        if (!this.formData.operacion) {
          throw new Error("El campo Operación es requerido");
        }

        if (
          this.formData.estado === "cargado" &&
          this.formData.productos.length === 0
        ) {
          throw new Error(
            "Debe seleccionar al menos un producto cuando el estado es Cargado"
          );
        }

        if (!this.formData.por_situar || this.formData.por_situar < 1) {
          throw new Error("La cantidad por situar debe ser al menos 1");
        }

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
          /*  equipo_vagon: this.vagonesAgregados.map((v) => ({
            cant_dias: v.cant_dias,
            equipo_ferroviario: v.equipo_ferroviario.id,
          })), */

          informe_operativo: this.informeOperativoId, // Incluir el ID del informe
        };

        // Enviar los datos al backend
        const response = await axios.post("/ufc/por-situar/", payload);

        // Mostrar mensaje de éxito
        Swal.fire({
          title: "¡Éxito!",
          text: "El registro ha sido creado correctamente",
          icon: "success",
          confirmButtonText: "Aceptar",
        }).then(() => {
          // Resetear el formulario después de enviar
          this.resetForm();
        });
      } catch (error) {
        console.error("Error al enviar el formulario:", error);

        let errorMessage = "Hubo un error al enviar el formulario";
        if (error.response) {
          // Error de respuesta del servidor
          if (error.response.data) {
            errorMessage = Object.values(error.response.data).join("\n");
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
        productos: [], // Cambiado a array vacío
        por_situar: 1,
        observaciones: "",
      };
    },

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
      if (this.formData.productos.length === 1) {
        const producto = this.productos.find(
          (p) => p.id === this.formData.productos[0]
        );
        return producto
          ? `${producto.id}-${producto.producto_name}`
          : "1 producto seleccionado";
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
    agregarVagon() {
      if (this.vagonesAgregados.length >= this.formData.por_situar) {
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
  },
};
</script>

<style scoped>
/* Estilos para el select con búsqueda */
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
/* Estilos para el grid dentro del modal */
.ufc-modal-body .ufc-form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
  margin-bottom: 20px;
}

/* Ajustes para los botones del modal */
.ufc-modal-body .ufc-form-actions {
  border-top: 1px solid #eee;
  padding-top: 15px;
  margin-top: 0;
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
</style>
