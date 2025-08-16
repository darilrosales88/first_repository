<template>
  <!-- Encabezado corporativo -->
  <div class="ufc-header">
    <h6>Partes UFC</h6>
  </div>
  <Navbar-Component />
  <Producto-Vagones />
  <div class="container py-3" style="margin-left: 20em; width: 70%">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-file-earmark-plus me-2"></i> Nuevo registro de
          situados
        </h5>
      </div>
      <div class="card-body p-3">
        <form @submit.prevent="submitForm">
          <div class="ufc-form-grid">
            <!-- Columna 1 -->
            <div>
              <!-- Campo:Fecha de registro -->
              <div class="mb-3">
                <label
                  for="fecha_registro"
                  class="form-label small fw-semibold text-secondary"
                  >Fecha de registro</label
                >
                <input
                  type="text"
                  class="form-control form-control-sm border-secondary"
                  style="padding: 8px 12px"
                  :value="formattedFechaRegistro"
                  id="fecha_registro"
                  name="fecha_registro"
                  readonly
                />
              </div>
              <!-- Campo: tipo_origen -->
              <div class="ufc-input-group">
                <label
                  for="tipo_origen"
                  class="form-label small fw-semibold text-secondary"
                >
                  Tipo de Origen
                </label>
                <select
                  class="form-select form-select-sm border-secondary"
                  style="padding: 8px 12px"
                  v-model="formData.tipo_origen"
                  id="tipo_origen"
                  name="tipo_origen"
                  required
                  oninvalid="this.setCustomValidity('Por favor, seleccione un tipo de origen')"
                  oninput="this.setCustomValidity('')"
                >
                  @change="handleTipoOrigenChange" >
                  <option value="" disabled>Seleccione un tipo</option>
                  <option
                    v-for="option in tipo_origen_options"
                    :key="option.id"
                    :value="option.id"
                  >
                    {{ option.text }}
                  </option>
                </select>
              </div>

              <!-- Campo: origen -->
              <div class="ufc-input-group">
                <label
                  for="origen"
                  class="form-label small fw-semibold text-secondary"
                  style="margin-top: 17px"
                >
                  Origen
                </label>
                <select
                  v-if="formData.tipo_origen === 'ac_ccd'"
                  class="form-select form-select-sm border-secondary"
                  style="padding: 8px 12px; margin-top: 9px"
                  v-model="formData.origen"
                  id="origen"
                  name="origen"
                  required
                  oninvalid="this.setCustomValidity('Por favor, seleccione un origen')"
                  oninput="this.setCustomValidity('')"
                >
                  
                  <option value="" disabled>Seleccione un origen</option>
                  <option
                    v-for="entidad in entidades"
                    :key="entidad.id"
                    :value="entidad.nombre"
                  >
                    {{ entidad.nombre }}
                  </option>
                </select>

                <select
                  v-else-if="formData.tipo_origen === 'puerto'"
                  class="form-select form-select-sm border-secondary"
                  style="padding: 8px 12px; margin-top: 9px"
                  v-model="formData.origen"
                  id="origen"
                  name="origen"
                  required
                  oninvalid="this.setCustomValidity('Por favor, seleccione un puerto')"
                  oninput="this.setCustomValidity('')"
                >
                  <option value="" disabled>Seleccione un puerto</option>
                  <option
                    v-for="puerto in puertos"
                    :key="puerto.id"
                    :value="puerto.nombre_puerto"
                  >
                    {{ puerto.nombre_puerto }}
                  </option>
                </select>

                <select
                  v-else
                  class="form-select form-select-sm border-secondary"
                  style="padding: 8px 12px; margin-top: 9px"
                  disabled
                >
                  <option value="">Seleccione primero el tipo de origen</option>
                </select>
              </div>

              <!-- Campo: tipo_equipo -->
              <div class="ufc-input-group">
                <label
                  for="tipo_equipo"
                  class="form-label small fw-semibold text-secondary"
                >
                  Tipo de Equipo Ferroviario
                </label>
                <select
                  class="form-select form-select-sm border-secondary"
                  style="padding: 8px 12px"
                  v-model="formData.tipo_equipo"
                  id="tipo_equipo"
                  name="tipo_equipo"
                  @change="buscarEquipos"
                  required
                  oninvalid="this.setCustomValidity('Por favor, seleccione un tipo de equipo ferroviario')"
                  oninput="this.setCustomValidity('')"
                >
                  <option value="" disabled>Seleccione un tipo</option>
                  <option
                    v-for="equipo in equipos"
                    :key="equipo.id"
                    :value="equipo.id"
                  >
                    {{ equipo.tipo_equipo_name }}-{{
                      equipo.tipo_carga_name
                    }}
                  </option>
                </select>
              </div>

              <!-- Campo: situados -->
              <div class="ufc-input-group">
                <label
                  for="situados"
                  v-if="isDisable"
                  class="form-label small fw-semibold text-secondary"
                  >Deshabilitado - Seleccione un tipo de equipo
                  ferroviario</label
                >
                <label
                  for="situados"
                  v-else
                  class="form-label small fw-semibold text-secondary"
                  >Vagones Situados - Cantidad Máxima
                  {{ this.equipos_vagones.length }}</label
                >
                <div class="ufc-por-situar-container">
                  <input
                    type="number"
                    class="ufc-por-situar-input"
                    v-model.number="formData.situados"
                    id="situados"
                    name="situados"
                    min="1"
                    :max="`${this.equipos_vagones.length}`"
                    :disabled="isDisable"
                    required
                  />
                  <span class="ufc-por-situar-suffix">unidades</span>
                </div>
              </div>
            </div>

            <!-- Columna 2 -->

            <div>
              <!-- Campo: estado -->
              <div class="ufc-input-group">
                <label
                  for="estado"
                  class="form-label small fw-semibold text-secondary"
                  style="margin-top: 4px"
                >
                  Estado
                </label>
                <select
                  class="form-select form-select-sm border-secondary"
                  style="padding: 8px 12px"
                  v-model="formData.estado">
                  <option value="cargado">Cargado</option>
                  <option value="vacio">Vacio</option>
                </select>
              </div>

              <!-- Campo: operacion -->
              <div  style="margin-bottom: 12px;">
                <label for="operacion" class="form-label small fw-semibold text-secondary">Operación</label>
                <input type="text" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" v-model="formData.operacion" id="operacion" name="operacion" readonly/>
              </div>

              <div class="mb-3">
                <!-- Campo: Productos-->
                <div class="mb-3">
                  
                  <label
                    for="productos"
                    class="form-label small fw-semibold text-secondary"
                    >Productos</label>
                  <div class="ufc-input-with-action">
                    <select v-if="formData.tipo_equipo"
                      class="form-select form-select-sm border-secondary"
                      style="padding: 8px 12px"
                      v-model="formData.producto"
                      @change="buscarTipoEquipo"
                      required
                      oninvalid="this.setCustomValidity('Por favor, seleccione un Producto')"
                      oninput="this.setCustomValidity('')">
                      <option value="" disabled>Seleccione un Producto</option>
                      <option
                        v-for="producto in productos"
                        :key="producto.id"
                        :value="producto.id">
                        {{ producto.producto_name }}-{{
                          producto.producto_codigo
                        }}-{{ producto.tipo_embalaje_name }}
                      </option>
                    </select>
                    <select
                      v-else
                      class="form-select form-select-sm border-secondary"
                      style="padding: 8px 12px"
                      disabled>
                      <option value="">Seleccione primero el tipo de equipo</option>
                    </select>
                    <button class="create-button ms-2" @click.stop.prevent="abrirModalAgregarProducto">
                      <i class="bi bi-plus-circle large-icon"></i>
                    </button>
                  </div>
                </div>
              </div>

              <ModalAgregarProducto
                v-if="mostrarModal"
                :visible="mostrarModal"
                @cerrar-modal="cerrarModal"
              />

              <!-- Campo: situados -->

              <!-- Campo: pendiente_proximo_dia -->
              <div class="ufc-input-group">
                <label
                  for="pendiente_proximo_dia"
                  class="form-label small fw-semibold text-secondary"
                >
                  Pendientes al próximo día
                </label>
                <div class="ufc-por-situar-container">
                  <input
                    type="number"
                    class="ufc-por-situar-input"
                    v-model.number="formData.pendiente_proximo_dia"
                    id="pendiente_proximo_dia"
                    name="pendiente_proximo_dia"
                    min="0"
                  />
                </div>
              </div>

              <!-- Campo: observaciones -->
              <div class="ufc-input-group">
                <label
                  for="observaciones"
                  class="form-label small fw-semibold text-secondary"
                  >Observaciones</label
                >
                <textarea
                  class="form-control form-control-sm border-secondary"
                  v-model="formData.observaciones"
                  id="observaciones"
                  name="observaciones"
                  rows="3"
                ></textarea>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <button class="ufc-button secondary" @click="volver_principal">
                <i class="bi bi-x-circle" me-1></i>Cancelar
              </button>
              <button type="submit" class="ufc-button primary">
                <i class="bi bi-check-circle" me-1></i>Añadir
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Modal para agregar vagón -->
  <div v-if="mostrarModalVagon" class="ufc-modal-overlay">
    <div class="ufc-modal-container">
      <div class="ufc-modal-header">
        <h3><i class="bi bi-train-freight-front"></i> Añadir Vagón</h3>
        <button @click="cerrarModalVagon" class="ufc-modal-close">
          <i class="bi bi-x"></i>
        </button>
      </div>
      <div class="ufc-modal-body">
        <div class="ufc-form-grid">
          <!-- Campo: Equipo Ferroviario -->
          <div class="ufc-input-group">
            <label for="equipo_ferroviario">Equipo Ferroviario</label>
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
            <label for="cant_dias">Cantidad de días</label>
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
            @click="cerrarModalVagon">
            <i class="bi bi-x-circle"></i> Cancelar
          </button>
          <button
            type="button"
            class="ufc-button primary"
            @click="agregarNuevoVagon()">
            <i class="bi bi-check-circle"></i> Agregar
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="container py-3" style="margin-left: 20em; width: 70%">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-train-freight-front"></i> Vagones 
        </h5>
      </div>
      <div class="card-body p-3">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <button class="btn btn-primary" @click="abrirModalVagon()">
            <i class="bi bi-plus-circle"></i> Añadir
          </button>
        </div>
        <!-- Tabla responsive con mejoras -->
        <div class="table table-responsive">
          <table class="table table-sm table-bordered table-hover">
            <thead class="table-light">
              <tr>
                <th scope="col">No.</th>
                <th scope="col">No. ID en trenes</th>
                <th>Cant. días</th>
                <th scope="col">Acciones</th>
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
                    class="btn btn-sm btn-outline-danger"
                    @click="eliminarVagon(index)"
                  >
                    <i class="bi bi-trash"></i>
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
            warning: vagonesAgregados.length < formData.situados,
            success: vagonesAgregados.length === formData.situados,
            error: vagonesAgregados.length > formData.situados,
          }"
        >
          <p v-if="vagonesAgregados.length < formData.situados">
            Faltan
            {{ formData.situados - vagonesAgregados.length }}
            vagones por añadir.
          </p>
          <p v-if="vagonesAgregados.length > formData.situados">
            Existen
            {{ vagonesAgregados.length  - formData.situados}}
            vagones sobrantes.
          </p>
          <p v-else-if="vagonesAgregados.length === formData.situados">
            Todos los vagones han sido agregados.
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
  name: "AdicionarSituados",
  components: {
    NavbarComponent,
    ModalAgregarProducto,
  },
  data() {
    return {
      informeOperativoId: null,
      formData: {
        tipo_origen: "",
        origen: "",
        tipo_equipo: "",
        estado: "cargado",
        operacion: "",
        productos: "",
        situados: 1,
        pendiente_proximo_dia: 0,
        observaciones: "",
        equipos_vagones: [],
      },
      isDisable: true,
      userGroups: [], 
      userPermissions: [], // Inicializa como array vacío
      productoSearch: "",
      showProductosDropdown: false,
      entidades: [],
      puertos: [],
      productos: [],
      loading: false,
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
    };
  },

  watch: {
    "formData.estado": {
      immediate: true,
      handler(newVal) {
        if (newVal === "vacio") {
          this.formData.operacion = "carga";
        } else if (newVal === "cargado") {
          this.formData.operacion = "descarga";
        }
      },
    },
  },

  mounted() {
    this.verificarInformeOperativo();
    this.getProductos();
    this.getEntidades();
    this.getPuertos();
    this.getEquipos();
  },

  computed: {
    formattedFechaRegistro() {
      if (this.formData.fecha) {
        return new Date(this.formData.fecha).toLocaleString("es-ES");
        return new Date(this.formData.fecha).toLocaleString("es-ES");
      }
      return new Date().toLocaleString("es-ES");
      return new Date().toLocaleString("es-ES");
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
      if (this.equipos_vagones.length == 0) {
        Swal.fire({
          title: "Error",
          text: "Seleccione el tipo de equipo",
          icon: "error",
          showCancelButton: false,
          confirmButtonText: "Aceptar",
          confirmButtonColor: "#ff4444"
        });
        return;
      }
      if (this.vagonesAgregados.length == this.formData.situados) {
        Swal.fire({
          title: "Error",
          text: "Ya añadió todos los vagones según la cantidad de vagones situados definida",
          icon: "error",
          showCancelButton: false,
          confirmButtonText: "Aceptar",
          confirmButtonColor: "#ff4444"
        });
        return;
      }
      this.mostrarModalVagon = true;
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
      
      if (this.nuevoVagon.equipo_ferroviario == '') {
        this.showErrorToast("Debe completar todos los campos");
        return;
      }
      const equipoSeleccionado = this.equipos_vagones.find((e) => e.id === this.nuevoVagon.equipo_ferroviario);
      const yaExistente = this.vagonesAgregados.some(
        (vagon) => vagon.equipo_ferroviario.id === this.nuevoVagon.equipo_ferroviario
      );

      if (yaExistente) {
        this.showErrorToast("Este vagón ya ha sido agregado a la lista");
        return;
      }

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
      this.showSuccessToast("Vagón añadido");
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

    async getProductoXEquipo() {
      this.loading = true;
      
      try {
        const response = await axios.get(`/ufc/producto-vagon/?tipo_equipo=${this.formData.tipo_equipo}`);

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
        this.isDisable = false;
        this.getProductoXEquipo();
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

    eliminarVagon(index) {
      this.vagonesAgregados.splice(index, 1);
      localStorage.setItem(
        "vagonesAgregados",
        JSON.stringify(this.vagonesAgregados)
      );
      this.showSuccessToast("Vagón eliminado");
    },


    cerrarModalVagon() {
      this.mostrarModalVagon = false;
      this.vagonEditIndex = null;
      this.modoEdicionVagon = false;
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

    async getPuertos() {
      try {
        const response = await axios.get("/api/puertos/");
        this.puertos = response.data.results;
      } catch (error) {
        console.error("Error al obtener los puertos:", error);
        Swal.fire("Error", "Hubo un error al obtener los puertos.", "error");
      }
    },

    handleTipoOrigenChange() {
      this.formData.origen = "";
      if (this.formData.tipo_origen === "ac_ccd") {
        this.formData.tipo_origen = "ac_ccd";
      } else if (this.formData.tipo_origen === "puerto") {
        this.formData.tipo_origen = "puerto";
      }
    },

    abrirModalAgregarProducto() {
      this.mostrarModal = true;
    },

    cerrarModal() {
      this.mostrarModal = false;
      this.getProductoXEquipo();
    },

    increment(field) {
      this.formData[field] += 1;
    },

    decrement(field) {
      if (this.formData[field] > (field === "situados" ? 1 : 0)) {
        this.formData[field] -= 1;
      }
    },
    async submitForm() {
      try {

        const informeNoAprobado = await this.verificarEstadoInforme();
        if (!informeNoAprobado) {
          Swal.fire(
            "Error",
            "No se puede agregar registros a un informe operativo que ya ha sido aprobado.",
            "error"
          );
          return;
        }

        const existeInforme = await this.verificarInformeOperativo();
        if (!existeInforme) {
          Swal.fire(
            "Error",
            "No existe un informe operativo creado para la fecha actual. Cree uno primero.",
            "error"
          );
          return;
        }

        if (this.vagonesAgregados.length==0) {
          Swal.fire({
            title: "Error",
            text: "Añada al menos un vagón",
            icon: "error",
          });
          return;
        }

        if (this.formData.estado === "cargado" && this.formData.producto.length === 0) {
          this.showErrorToast("Debe seleccionar al menos un producto cuando el estado es Cargado");
          return;
        }


        if (this.vagonesAgregados.length !== this.formData.situados) {
          Swal.fire({
            title: "Advertencia",
            text: `El número de vagones asociados (${this.vagonesAgregados.length}) no coincide con la cantidad de "Situados" (${this.formData.situados}).`,
            icon: "warning",
            showCancelButton: false,
            confirmButtonText: "Aceptar",
            confirmButtonColor: "#007bff"
          });
          return;
        }

        // Preparar datos para enviar
        const payload = {
          tipo_origen: this.formData.tipo_origen,
          origen: this.formData.origen,
          tipo_equipo: this.formData.tipo_equipo,
          estado: this.formData.estado,
          operacion: this.formData.operacion,
          producto: this.formData.producto,
          situados: this.formData.situados,
          pendiente_proximo_dia: this.formData.pendiente_proximo_dia,
          observaciones: this.formData.observaciones,
          informe_operativo: this.informeOperativoId,

          equipo_vagon: this.vagonesAgregados.map((vagon) => ({
            equipo_ferroviario: vagon.equipo_ferroviario.id,
            cant_dias: vagon.cant_dias,
          })),
        };
        console.log("Datos a enviar", payload);

        const response = await axios.post("/ufc/situados/", payload);
        this.$router.push({ name: "InfoOperativo" });
        this.showSuccessToast("El registro ha sido creado");
        this.resetForm();
        
      } catch (error) {
        console.error("Error al enviar el formulario:", error);
        this.showErrorToast(error.message);
      } 
    },
    resetForm() {
      this.formData = {
        tipo_origen: "",
        origen: "",
        tipo_equipo: "",
        estado: "cargado",
        operacion: "",
        productos: [],
        situados: 1,
        pendiente_proximo_dia: 0,
        observaciones: "",
      };
      this.vagonesAgregados = [];
      this.vagonesAgregados = [];
    },

    async confirmCancel() {
      const result = await Swal.fire({
        title: "¿Cancelar operación?",
        text: "Los datos no guardados se perderán",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, cancelar",
        cancelButtonText: "No, continuar",
        reverseButtons: true,
      });

      if (result.isConfirmed) {
        this.resetForm();
        this.$router.push({ name: "InfoOperativo" });
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
          (p) => p.id === this.formData.producto
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

    volver_principal() {
      event.preventDefault();
      event.stopPropagation();
      Swal.fire({
        title: "¿Volver a la página principal?",
        text: "Los datos no guardados se perderán",
        icon: "warning",
        showCancelButton: true,
        cancelButtonText: '<i class="bi bi-x-circle me-1"></i>Continuar',
        cancelButtonColor: "#f1513f",
        confirmButtonText: '<i class="bi bi-box-arrow-right me-1"></i>Volver',
        confirmButtonColor: "#007bff",
        reverseButtons: true,
      }).then((result) => {
        if (result.isConfirmed) {
          this.resetForm();
          this.$router.push({ name: "InfoOperativo" });
        }
      });
    },
    showSuccessToast(message) {
      const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        background: "#4BB543",
        color: "#fff",
        iconColor: "#fff",
        didOpen: (toast) => {
          toast.addEventListener("mouseenter", Swal.stopTimer);
          toast.addEventListener("mouseleave", Swal.resumeTimer);
        },
      });

      Toast.fire({
        icon: "success",
        title: message,
      });
    },

    showErrorToast(message) {
      const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 4000,
        timerProgressBar: true,
        background: "#ff4444",
        color: "#fff",
        iconColor: "#fff",
        didOpen: (toast) => {
          toast.addEventListener("mouseenter", Swal.stopTimer);
          toast.addEventListener("mouseleave", Swal.resumeTimer);
        },
      });

      Toast.fire({
        icon: "error",
        title: message,
      });
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
  },
};
</script>

<style scoped>
/* Estilos para la sección de vagones asociados */
.ufc-vagones-container {
  margin-top: 30px;
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.ufc-vagones-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.ufc-vagones-header h3 {
  color: #002a68;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
}

.ufc-button.small {
  padding: 6px 12px;
  font-size: 0.8rem;
}

.ufc-vagones-table-container {
  overflow-x: auto;
}

.ufc-vagones-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.ufc-vagones-table th {
  background-color: #002a68;
  color: white;
  padding: 10px 12px;
  text-align: left;
  font-weight: 500;
  font-size: 0.85rem;
}

.ufc-vagones-table td {
  padding: 12px;
  border-bottom: 1px solid #eee;
  font-size: 0.85rem;
}

.ufc-vagones-table tr:hover {
  background-color: #f8f9fa;
}

.ufc-actions-cell {
  display: flex;
  gap: 8px;
}

.ufc-icon-button {
  width: 30px;
  height: 30px;
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
  background-color: #ffc107;
  color: #212529;
}

.ufc-icon-button.warning:hover {
  background-color: #e0a800;
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
  padding: 30px;
  background-color: #f8f9fa;
  border-radius: 8px;
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
  margin: 0;
  font-size: 0.9rem;
}

/* Estilos para el modal de vagón */
.ufc-modal-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.ufc-modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

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
  border-color: rgba(
    var(--bs-secondary-rgb),
    var(--bs-border-opacity)
  ) !important;
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
  border-color: rgba(
    var(--bs-secondary-rgb),
    var(--bs-border-opacity)
  ) !important;
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
  background: rgb(241, 81, 63);
  color: white;
}

.ufc-button.secondary:hover {
  background: rgb(228, 56, 37);
}

.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
}

.btn-outline-danger:hover {
  color: #fff;
}

.create-button {
  text-decoration: none;
  border: none;
  color: green;
  margin-left: 940px;
}

button {
  margin-left: 10px;
  padding: 5px 15px;
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
.form-select:focus {
  border-color: #dc3545;
  box-shadow: 0 0 0 0.25rem rgba(220, 53, 69, 0.25);
  outline: 0;
}
.form-control:focus {
  border-color: #dc3545;
  box-shadow: 0 0 0 0.25rem rgba(220, 53, 69, 0.25);
  outline: 0;
}
</style>
