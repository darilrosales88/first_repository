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
          <i class="bi bi-pencil-square"></i> Editar registro por situar
        </h2>

        <form @submit.prevent="submitForm" class="ufc-form">
          <div class="ufc-form-grid">
            <!-- Columna Izquierda -->
            <div class="ufc-form-column">
              <!-- Campo: tipo_origen -->
              <div class="ufc-input-group">
                <label for="tipo_origen"
                  >Tipo de Origen <span class="required">*</span></label
                >
                <select
                  class="ufc-select"
                  v-model="formData.tipo_origen"
                  :disabled="loading"
                  required
                  @change="handleTipoOrigenChange"
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
                  :disabled="loading || !formData.tipo_origen"
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
                  :disabled="loading || !formData.tipo_origen"
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
                  :disabled="loading"
                  required
                >
                  <option value="" disabled>Seleccione un tipo</option>
                  <option
                    v-for="option in equipos"
                    :key="option.id"
                    :value="option.id"
                  >
                    {{ option.id }}-{{ option.tipo_equipo_name }}
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
                  :disabled="loading"
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
                  :disabled="loading"
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

              <!-- Campo: producto -->
              <div class="ufc-input-group">
                <label for="productos"
                  >Productos
                  <span v-if="formData.estado === 'cargado'" class="required"
                    >*</span
                  ></label
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
                            (Embalaje: {{ producto.tipo_embalaje || "N/A" }})
                          </template>
                        </div>
                      </div>
                    </div>
                  </div>
                  <button
                    class="ufc-add-button"
                    @click.prevent="abrirModalAgregarProducto"
                    :disabled="loading"
                  >
                    <i class="bi bi-plus-circle"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <ModalAgregarProducto
            v-if="mostrarModal"
            :visible="mostrarModal"
            @cerrar-modal="cerrarModal"
          />

          <!-- Campos de cantidades (full width) -->
          <div class="ufc-quantity-grid">
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
                  :disabled="loading"
                  required
                  @input="validatePorSituar"
                />
                <span class="ufc-por-situar-suffix">unidades</span>
              </div>
            </div>
          </div>

          <!-- Vagones asociados -->
          <div class="ufc-vagones-container">
            <div class="ufc-vagones-header">
              <h3>
                <i class="bi bi-train-freight-front"></i> Vagones Asociados
              </h3>
              <button
                class="ufc-button small primary"
                @click.prevent="abrirModalAgregarVagon"
                :disabled="loading"
              >
                <i class="bi bi-plus"></i> Agregar Vagón
              </button>
            </div>

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
                        class="ufc-icon-button warning"
                        @click.prevent="editarVagon(index)"
                      >
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button
                        class="ufc-icon-button danger"
                        @click.prevent="eliminarVagon(index)"
                      >
                        <i class="bi bi-trash"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-else class="ufc-vagones-empty">
              <div class="ufc-empty-state">
                <i class="bi bi-train"></i>
                <p>No hay vagones asociados a este registro</p>
              </div>
            </div>
          </div>

          <!-- Observaciones (full width) -->
          <div class="ufc-input-group full-width">
            <label for="observaciones">Observaciones</label>
            <textarea
              class="ufc-textarea"
              v-model="formData.observaciones"
              :disabled="loading"
              rows="2"
              maxlength="500"
              placeholder="Máximo 500 caracteres"
            ></textarea>
            <div class="ufc-char-counter">
              {{ formData.observaciones.length }}/500
            </div>
          </div>

          <!-- Botones de acción -->
          <div class="ufc-form-actions">
            <button
              type="button"
              class="ufc-button secondary"
              @click="confirmCancel"
              :disabled="loading"
            >
              <i class="bi bi-x-circle"></i> Cancelar
            </button>
            <button
              type="submit"
              class="ufc-button primary"
              :disabled="loading || isFormInvalid"
            >
              <i class="bi bi-check-circle"></i>
              <span v-if="loading">Guardando...</span>
              <span v-else>Guardar Cambios</span>
            </button>

            <button
              type="button"
              class="ufc-button primary"
              @click="abrirModalVagon"
            >
              <i class="bi bi-plus-circle"></i> Adicionar Vagón
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal para agregar equipos -->
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
          Se han agregado más vagones de los permitidos. Por favor, elimina los
          excedentes.
        </p>
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
            @producto-agregado="handleProductoAgregado"
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
          <button @click="cerrarModalVagon" class="ufc-modal-close">
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
                @click="cerrarModalVagon"
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
  name: "EditarPorSituar",
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
      userGroups: [], // Inicializa como array vacío
      userPermissions: [], // Inicializa como array vacío
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
      vagonesAsociados: [],
      mostrarModalVagon: false,
      modoEdicionVagon: false,
      vagonEditIndex: null,
      vagonForm: {
        equipo_ferroviario: "",
        dias: 1,
      },
      equiposFerroviarios: [],
      formErrors: {},
    };
  },
  computed: {
    isFormInvalid() {
      return (
        !this.formData.tipo_origen ||
        !this.formData.origen ||
        !this.formData.tipo_equipo ||
        !this.formData.estado ||
        !this.formData.operacion ||
        (this.formData.estado === "cargado" &&
          this.formData.productos.length === 0)
      );
    },
  },
  created() {
    this.registroId = this.$route.params.id;
    if (this.registroId) {
      this.cargarRegistro();
    }
    this.getEntidades();
    this.getPuertos();
    this.getProductos();
    this.getEquipos();
  },
  mounted() {
    this.filteredProductos = this.productos;
    this.closeDropdownsOnClickOutside();
  },

  methods: {
    async cargarRegistro() {
      this.loading = true;
      try {
        const response = await axios.get(`/ufc/por-situar/${this.registroId}/`);
        const registro = response.data;

        this.formData = {
          id: registro.id,
          tipo_origen: registro.tipo_origen,
          origen: registro.origen,
          tipo_equipo: registro.tipo_equipo,
          estado: registro.estado,
          operacion: registro.operacion,
          productos: registro.productos_info?.map((p) => p.id) || [],
          por_situar: registro.por_situar,
          observaciones: registro.observaciones || "",
        };

        if (registro.vagones) {
          this.vagonesAsociados = registro.vagones.map((v) => ({
            id: v.id,
            equipo_ferroviario: v.equipo_ferroviario,
            equipo_ferroviario_nombre:
              v.equipo_ferroviario_numero_identificacion,
            dias: v.dias,
          }));
        }
      } catch (error) {
        console.error("Error al cargar el registro:", error);
        Swal.fire("Error", "No se pudo cargar el registro", "error");
        this.$router.push({ name: "InfoOperativo" });
      } finally {
        this.loading = false;
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
    async abrirModalVagon() {
      this.mostrarModalVagon = true;

      await this.buscarEquipos();
    },
    cerrarModalVagon() {
      this.mostrarModalVagon = false;
      this.nuevoVagon = {
        equipo_ferroviario: "",
        cant_dias: 1,
      };
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

    async getProductos() {
      try {
        const response = await axios.get("/ufc/producto-vagon/", {
          params: {
            include_details: true,
          },
        });

        this.productos = response.data.results.map((p) => ({
          id: p.id,
          producto_name: p.producto_name || `Producto ${p.id}`,
          producto_codigo: p.producto_codigo || "N/A",
          tipo_embalaje: p.tipo_embalaje_name || "N/A",
        }));
        this.filteredProductos = [...this.productos];
      } catch (error) {
        console.error("Error al obtener productos:", error);
        Swal.fire("Error", "No se pudieron cargar los productos", "error");
      }
    },
    async getPuertos() {
      try {
        const response = await axios.get("/api/puertos/");
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
      this.mostrarModal = false;
      this.getProductos();
    },

    handleEstadoChange() {
      if (this.formData.estado !== "cargado") {
        this.formData.productos = []; // Limpiar array de productos
      }
    },

    async submitForm() {
      try {
        this.loading = true;

        // Validación
        const errors = [];

        if (!this.formData.origen) {
          errors.push("El campo Origen es requerido");
        }

        if (!this.formData.tipo_equipo) {
          errors.push("El campo Tipo de Equipo es requerido");
        }

        if (!this.formData.operacion) {
          errors.push("El campo Operación es requerido");
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
          errors.push("La cantidad por situar debe ser al menos 1");
        }

        if (!["ac_ccd", "puerto"].includes(this.formData.tipo_origen)) {
          errors.push("Tipo de origen no válido");
        }

        if (errors.length > 0) {
          throw new Error(errors.join("\n"));
        }

        // Preparar datos para enviar
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

          // Datos de los vagones (estructura corregida)
          equipo_vagon: this.vagonesAgregados.map((vagon) => ({
            equipo_ferroviario: vagon.equipo_ferroviario.id, // ID del equipo
            cant_dias: vagon.cant_dias,
            // Otros campos necesarios para el vagon
          })),
        };

        // Enviar datos para actualizar (PUT)
        const response = await axios.put(
          `http://127.0.0.1:8000/ufc/por-situar/${this.registroId}/`,
          payload
        );

        Swal.fire({
          title: "Éxito",
          text: "Registro actualizado correctamente",
          icon: "success",
        }).then(() => {
          this.$router.push({ name: "InfoOperativo" });
        });
      } catch (error) {
        let errorMessage = "Error al actualizar el registro";

        if (error.message) {
          errorMessage = error.message;
        } else if (error.response?.data) {
          errorMessage = Object.values(error.response.data).join("\n");
        }

        Swal.fire("Error", errorMessage, "error");
        console.error("Error al enviar el formulario:", error);
      } finally {
        this.loading = false;
      }
    },
    getNombresProductos(productos) {
      if (!productos || !Array.isArray(productos)) return "-";
      return productos
        .filter((p) => p && p.nombre_producto)
        .map((p) => p.nombre_producto)
        .join(", ");
    },
    handleTipoOrigenChange() {
      this.formData.origen = ""; // Resetear origen cuando cambia el tipo
    },
    handleEstadoChange() {
      if (this.formData.estado !== "cargado") {
        this.formData.productos = [];
      }
    },
    validatePorSituar() {
      if (this.formData.por_situar < 1) {
        this.formData.por_situar = 1;
      }
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

      // Si el estado es vacío, mostramos solo el conteo
      if (this.formData.estado === "vacio") {
        return `${this.formData.productos.length} producto(s) seleccionado(s)`;
      }

      // Para estado cargado, mostramos más detalles
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

    handleEstadoChange() {
      // Eliminamos la lógica que limpiaba los productos
      // Ahora los productos permanecen sin importar el estado
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
/* Estilos para el select personalizado de productos */
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

.ufc-selected-products {
  font-size: 0.8rem;
  color: #666;
  margin-top: 5px;
}

/* Estilos anteriores... */

.ufc-quantity-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-bottom: 15px;
}

@media (max-width: 768px) {
  .ufc-quantity-grid {
    grid-template-columns: 1fr;
  }
}

/* Mantener todos los demás estilos igual que en el formulario anterior */
</style>

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
  position: relative;
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

.ufc-char-counter {
  text-align: right;
  font-size: 0.75rem;
  color: #666;
  margin-top: 5px;
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
  flex-shrink: 0;
}

.ufc-add-button:hover {
  background: #e9ecef;
  color: #001a3d;
}

.ufc-add-button i {
  font-size: 1.2rem;
}

.ufc-loading,
.ufc-disabled {
  font-size: 0.8rem;
  color: #777;
  padding: 8px 0;
}

.ufc-loading i {
  margin-right: 5px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Estilo para el campo por situar */
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
  margin-top: 25px;
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

.ufc-button.primary:hover:not(:disabled) {
  background: #003d8f;
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.ufc-button.secondary {
  background: white;
  color: #555;
  border: 1px solid #ddd;
}

.ufc-button.secondary:hover:not(:disabled) {
  background: #f8f9fa;
  border-color: #ccc;
}

.ufc-button.small {
  padding: 8px 12px;
  font-size: 0.85rem;
}

.ufc-button[disabled] {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none !important;
}

/* Estilos para selects */
.ufc-select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 14px;
}

/* Estilos para el select personalizado de productos */
.ufc-custom-select {
  position: relative;
  width: 100%;
  cursor: pointer;
  flex: 1;
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
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ufc-select-arrow {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  transition: transform 0.2s;
  pointer-events: none;
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
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 100;
  margin-top: 2px;
}

.ufc-productos-search-container {
  padding: 10px;
  border-bottom: 1px solid #eee;
  background: #f8f9fa;
  position: sticky;
  top: 0;
  z-index: 10;
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

.ufc-no-results {
  padding: 15px;
  text-align: center;
  color: #666;
  font-size: 0.9rem;
}

.ufc-selected-count {
  font-size: 0.8rem;
  color: #666;
  margin-top: 5px;
  text-align: right;
}

/* Estilos para la sección de vagones */
.ufc-vagones-container {
  margin-top: 30px;
  border-top: 1px solid #eee;
  padding-top: 20px;
}

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
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.ufc-vagones-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.ufc-vagones-table th {
  background-color: #002a68;
  color: white;
  padding: 12px 15px;
  text-align: left;
  font-weight: 500;
}

.ufc-vagones-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
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
  font-size: 0.9rem;
}

.ufc-icon-button.warning {
  background-color: rgba(255, 193, 7, 0.1);
  color: #ffc107;
}

.ufc-icon-button.warning:hover {
  background-color: rgba(255, 193, 7, 0.2);
}

.ufc-icon-button.danger {
  background-color: rgba(220, 53, 69, 0.1);
  color: #dc3545;
}

.ufc-icon-button.danger:hover {
  background-color: rgba(220, 53, 69, 0.2);
}

.ufc-vagones-empty {
  margin-top: 20px;
  text-align: center;
  padding: 30px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px dashed #ddd;
}

.ufc-empty-state {
  color: #6c757d;
}

.ufc-empty-state i {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #adb5bd;
}

.ufc-empty-state p {
  margin: 10px 0 0;
  font-size: 0.95rem;
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
  backdrop-filter: blur(2px);
}

.ufc-modal-container {
  background: white;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow: auto;
  box-shadow: 0 5px 25px rgba(0, 0, 0, 0.2);
  animation: modalFadeIn 0.3s ease-out;
}

.ufc-modal-header {
  padding: 18px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #002a68;
  color: white;
  border-radius: 10px 10px 0 0;
  position: sticky;
  top: 0;
  z-index: 10;
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
  line-height: 1;
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

/* Responsive */
@media (max-width: 768px) {
  .ufc-form-card {
    padding: 15px;
  }

  .ufc-vagones-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .ufc-form-actions {
    flex-direction: column;
    gap: 10px;
  }

  .ufc-button {
    width: 100%;
    justify-content: center;
  }
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

/* Clase full-width para elementos que deben ocupar todo el ancho */
.full-width {
  grid-column: 1 / -1;
}

/* Estilos para la cuadrícula de cantidades */
.ufc-quantity-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}
</style>
