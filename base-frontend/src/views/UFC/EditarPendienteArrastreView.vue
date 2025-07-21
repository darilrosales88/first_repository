<template>
  <div class="ufc-header">
    <h6>Partes UFC</h6>
  </div>
  <Navbar-Component />
  <Producto-Vagones />

  <!-- Primer contenedor principal -->
  <div class="container py-3" style="margin-left: 20em; width: 70%">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-file-earmark-plus"></i> Editar registro pendiente a
          arrastre
        </h5>
      </div>
      <div class="card-body p-3">
        <form @submit.prevent="submitForm" class="ufc-form">
          <div class="row">
            <!-- Columna Izquierda -->
            <div class="col-md-6">
              <!-- Campo: Fecha de registro -->
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

              <!-- Grupo Origen -->
              <div class="ufc-form-group">
                <div class="ufc-form-row">
                  <!-- Campo: tipo_origen -->
                  <div class="mb-3">
                    <label
                      for="tipo_origen"
                      class="form-label small fw-semibold text-secondary"
                      >Tipo de Origen</label
                    >
                    <select
                      class="form-select form-select-sm border-secondary"
                      style="
                        width: 187px;
                        padding-top: 8px;
                        padding-bottom: 8px;
                      "
                      v-model="formData.tipo_origen"
                      required
                      oninvalid="this.setCustomValidity('Por favor, seleccione un tipo de origen')"
                      oninput="this.setCustomValidity('')"
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
                  <div class="mb-3">
                    <label
                      for="origen"
                      class="form-label small fw-semibold text-secondary"
                      >Origen</label
                    >
                    <select
                      v-if="
                        formData.tipo_origen &&
                        formData.tipo_origen !== 'puerto'
                      "
                      class="form-select form-select-sm border-secondary"
                      style="
                        width: 230px;
                        padding-top: 8px;
                        padding-bottom: 8px;
                      "
                      v-model="formData.origen"
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
                      style="
                        width: 230px;
                        padding-top: 8px;
                        padding-bottom: 8px;
                      "
                      v-model="formData.origen"
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
                        {{ puerto.id }}- {{ puerto.nombre_puerto }}
                      </option>
                    </select>

                    <select
                      v-else
                      class="form-select form-select-sm border-secondary"
                      style="
                        width: 230px;
                        padding-top: 8px;
                        padding-bottom: 8px;
                      "
                      disabled
                    >
                      <option value="">Seleccione un tipo de origen</option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- Grupo Destino -->
              <div class="ufc-form-group">
                <div class="ufc-form-row">
                  <!-- Campo: tipo_destino -->
                  <div class="mb-3">
                    <label
                      for="tipo_destino"
                      class="form-label small fw-semibold text-secondary"
                      >Tipo de Destino</label
                    >
                    <select
                      class="form-select form-select-sm border-secondary"
                      style="
                        width: 187px;
                        padding-top: 8px;
                        padding-bottom: 8px;
                      "
                      v-model="formData.tipo_destino"
                      required
                      oninvalid="this.setCustomValidity('Por favor, seleccione un tipo de destino')"
                      oninput="this.setCustomValidity('')"
                    >
                      <option value="" disabled>Seleccione un tipo</option>
                      <option
                        v-for="item in tipo_destino_options"
                        :key="item.id"
                        :value="item.id"
                      >
                        {{ item.text }}
                      </option>
                    </select>
                  </div>

                  <!-- Campo: destino -->
                  <div class="mb-3">
                    <label
                      for="destino"
                      class="form-label small fw-semibold text-secondary"
                      >Destino</label
                    >
                    <select
                      v-if="
                        formData.tipo_destino &&
                        formData.tipo_destino !== 'puerto'
                      "
                      class="form-select form-select-sm border-secondary"
                      style="
                        width: 230px;
                        padding-top: 8px;
                        padding-bottom: 8px;
                      "
                      v-model="formData.destino"
                      required
                      oninvalid="this.setCustomValidity('Por favor, seleccione un destino')"
                      oninput="this.setCustomValidity('')"
                    >
                      <option value="" disabled>Seleccione un destino</option>
                      <option
                        v-for="entidad in entidades"
                        :key="entidad.id"
                        :value="entidad.nombre"
                      >
                        {{ entidad.nombre }}
                      </option>
                    </select>

                    <select
                      v-else-if="formData.tipo_destino === 'puerto'"
                      class="form-select form-select-sm border-secondary"
                      style="
                        width: 230px;
                        padding-top: 8px;
                        padding-bottom: 8px;
                      "
                      v-model="formData.destino"
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
                        {{ puerto.id }}- {{ puerto.nombre_puerto }}
                      </option>
                    </select>

                    <select
                      v-else
                      class="form-select form-select-sm border-secondary"
                      style="
                        width: 230px;
                        padding-top: 8px;
                        padding-bottom: 8px;
                      "
                      disabled
                    >
                      <option value="">Seleccione un tipo de destino</option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- Campo: tipo_equipo -->
              <div class="mb-3">
                <label
                  for="tipo_equipo"
                  class="form-label small fw-semibold text-secondary"
                  >Tipo de Equipo Ferroviario</label
                >
                <select
                  class="form-select form-select-sm border-secondary"
                  style="padding: 8px 12px"
                  v-model="formData.tipo_equipo"
                  @change="buscarEquipos"
                  required
                  oninvalid="this.setCustomValidity('Por favor, seleccione un equipo ferroviario')"
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
              <!-- Campo: cantidad_vagones -->
              <div class="mb-3">
                <label
                  for="cantidad_vagones"
                  v-if="isDisable"
                  class="form-label small fw-semibold text-secondary"
                  >Deshabilitado - Seleccione un tipo de equipo
                  ferroviario</label
                >
                <label
                  for="cantidad_vagones"
                  v-else
                  class="form-label small fw-semibold text-secondary"
                  >Cantidad de Vagones - Cantidad Máxima
                  {{ this.equipos_vagones.length }}</label
                >
                <div class="ufc-por-situar-container">
                  <input
                    type="number"
                    class="ufc-por-situar-input"
                    v-model.number="formData.cantidad_vagones"
                    min="1"
                    :max="`${this.equipos_vagones.length}`"
                    :disabled="isDisable"
                    required
                  />
                  <span class="ufc-por-situar-suffix">unidades</span>
                </div>
              </div>
            </div>

            <!-- Columna Derecha -->
            <div class="col-md-6">
              <!-- Campo: estado -->
              <div class="mb-3">
                <label
                  for="estado"
                  class="form-label small fw-semibold text-secondary"
                  >Estado</label
                >
                <select
                  class="form-select form-select-sm border-secondary"
                  style="padding: 8px 12px"
                  v-model="formData.estado"
                  @change="handleEstadoChange"
                  required
                  oninvalid="this.setCustomValidity('Por favor, seleccione un estado')"
                  oninput="this.setCustomValidity('')"
                >
                  <option value="cargado">Cargado</option>
                  <option value="vacio">Vacío</option>
                </select>
              </div>

              <!-- Campo: operacion -->
              <div class="mb-3">
                <label
                  for="operacion"
                  class="form-label small fw-semibold text-secondary"
                  >Operación</label
                >
                <select
                  class="form-select form-select-sm border-secondary"
                  style="padding: 8px 12px"
                  v-model="formData.operacion"
                  required
                  oninvalid="this.setCustomValidity('Por favor, seleccione una operación')"
                  oninput="this.setCustomValidity('')"
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
              <div class="ufc-input-group" style="margin-top: 16px;">
                <label for="productos" class="form-label small fw-semibold text-secondary">
                  Productos
                </label>
                <div class="ufc-input-with-action">
                  <select
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="formData.producto"
                    @change="buscarTipoEquipo"
                    required
                    oninvalid="this.setCustomValidity('Por favor, seleccione un Producto')"
                    oninput="this.setCustomValidity('')"
                  >
                    <option value="" disabled>Seleccione un Producto</option>
                    <option
                      v-for="producto in productos"
                      :key="producto.id"
                      :value="producto.id"
                    >
                      {{ producto.producto_name }}-{{
                        producto.producto_codigo
                      }}-{{ producto.tipo_embalaje_name }}
                    </option>
                  </select>
                  <button
                    class="create-button ms-2"
                    @click.stop.prevent="abrirModalAgregarProducto"
                  >
                    <i class="bi bi-plus-circle large-icon"></i>
                  </button>
                </div>
              </div>

              <div class="mb-3">
                <label for="observaciones" class="form-label small fw-semibold text-secondary">Observaciones</label>
                <textarea
                  class="form-control form-control-sm border-secondary"
                  v-model="formData.observaciones"
                  rows="4"
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Botones de acción -->
          <div class="modal-footer">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <button class="ufc-button secondary" @click="volver_principal">
                <i class="bi bi-x-circle" me-1></i>Cancelar
              </button>
              <button type="submit" class="ufc-button primary">
                <i class="bi bi-check-circle" me-1></i>Actualizar
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Modal para agregar producto -->
  <ModalAgregarProducto
    v-if="mostrarModal"
    :visible="mostrarModal"
    @cerrar-modal="cerrarModal"
  />

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
              oninvalid="this.setCustomValidity('Por favor, seleccione un estado')"
              oninput="this.setCustomValidity('')"
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
            @click="cerrarModalVagon"
          >
            <i class="bi bi-x-circle"></i> Cancelar
          </button>
          <button
            type="button"
            class="ufc-button primary"
            @click="annadidoNuevoVagon"
            :disabled="!nuevoVagon.equipo_ferroviario || !nuevoVagon.cant_dias"
          >
            <i class="bi bi-check-circle"></i> Añadir
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Contenedor de vagones agregados -->
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
          <p v-if="vagonesAgregados.length > formData.cantidad_vagones">
            Existen
            {{ vagonesAgregados.length  - formData.cantidad_vagones}}
            vagones sobrantes.
          </p>
          <p v-else-if="vagonesAgregados.length === formData.cantidad_vagones">
            Todos los vagones han sido agregados.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios, { formToJSON } from "axios";
import Swal from "sweetalert2";
import NavbarComponent from "@/components/NavbarComponent.vue";
import ModalAgregarProducto from "@/components/ModalAgregarProducto.vue";

export default {
  name: "AdicionarPendienteArrastre",
  components: {
    NavbarComponent,
    ModalAgregarProducto,
  },
  data() {
    return {
      formData: {
        tipo_origen: "",
        origen: "",
        tipo_destino: "",
        destino: "",
        tipo_equipo: "",
        operacion: "",
        estado: "cargado",
        producto: "",
        cantidad_vagones: 1,
        observaciones: "",
        equipos_vagones: [],
      },
      userGroups: [], // Inicializa como array vacío
      userPermissions: [], // Inicializa como array vacío
      productoSearch: "",
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
      informeOperativoId: null,

      tipo_origen_options: [
        { id: "ac_ccd", text: "comercial/AccesoCCD" },
        { id: "puerto", text: "Puerto" },
      ],
      tipo_destino_options: [
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
    this.buscarEquipos();
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
  computed: {
    formattedFechaRegistro() {
      if (this.formData.fecha) {
        return new Date(this.formData.fecha).toLocaleString("es-ES");
      }
      return new Date().toLocaleString("es-ES");
    },
  },
  async created() {
    this.registroId = this.$route.params.id;
    if (this.registroId) {
      this.cargarRegistro();
    }
    this.getEntidades();
    this.getPuertos();
    this.getProductos();
    this.getEquipos();
  },
  methods: {
    // Verifica s
    // i el usuario pertenece a un grupo es
    // pecífico
    async cargarRegistro() {
      this.loading = true;
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/ufc/pendiente-arrastre/${this.registroId}/`
        );
        const registro = response.data;

        await this.getProductos();

        for(let i = 0; i < registro.equipo_vagon_detalle.length; i++) {
          let vagon = {
              equipo_ferroviario: registro.equipo_vagon_detalle[i].equipo_ferroviario_detalle,
              cant_dias: registro.equipo_vagon_detalle[i].cant_dias,
          };
          this.vagonesAgregados.push(vagon);
        }

        this.formData = {
          id: registro.id,
          tipo_origen: registro.tipo_origen,
          origen: registro.origen,
          tipo_destino: registro.tipo_destino,
          destino: registro.destino,
          tipo_equipo: registro.tipo_equipo,
          estado: registro.estado,
          operacion: registro.operacion,
          producto: registro.producto,
          cantidad_vagones: registro.cantidad_vagones,
          observaciones: registro.observaciones,
        };
        this.buscarEquipos();
      } catch (error) {
        throw new Error(error);
      } finally {
        this.loading = false;
        await this.buscarEquipos();
      }
    },

    hasGroup(group) {
      return this.userGroups.some((g) => g.name === group);
    },
    // Obtiene los permisos y grupos del usuario
    async fetchUserPermissionsAndGroups() {
      try {
        const userId = localStorage.getItem("userid");
        if (userId) {
          const response = await axios.get(
            `/apiAdmin/user/${userId}/permissions-and-groups/`
          );
          this.userPermissions = response.data.permissions;
          this.userGroups = response.data.groups;
        }
        console.log("Permisos: ", this.userPermissions);
        console.log("Grupos: ", this.userGroups);
      } catch (error) {
        console.error("Error al obtener permisos y grupos:", error);
      }
    },

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

    async abrirModalVagon() {
      this.mostrarModalVagon = true;
      console.log(this.vagonesAgregados);

      await this.buscarEquipos();
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
    annadidoNuevoVagon() {
      if (!this.nuevoVagon.equipo_ferroviario || !this.nuevoVagon.cant_dias) {
        Swal.fire("Error", "Complete todos los campos", "error");
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
      this.formData.cantidad_vagones = this.vagonesAgregados.length;
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
          const tipoEmbalaje = p.tipo_embalaje_name || {};
          return {
            ...p,
            tipo_embalaje: {
              nombre:
                tipoEmbalaje || tipoEmbalaje.nombre_embalaje || "Sin embalaje",
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
        this.loading = true;

        if (this.vagonesAgregados.length==0) {
          Swal.fire({
            title: "Error",
            text: "Añada al menos un vagón",
            icon: "error",
          });
          return;
        }

        if (this.formData.estado === "cargado" && this.formData.producto.length === 0) {
          this.showErrorToast("Seleccione al menos un producto");
          return;
        }

        if (this.vagonesAgregados.length != this.formData.cantidad_vagones) {
          Swal.fire({
            title: "Advertencia",
            text: `El número de vagones asociados (${this.vagonesAgregados.length}) no coincide con la cantidad de "Situados" (${this.formData.situados}). ¿Desea actualizar el campo "Situados" para que coincida?`,
            icon: "warning",
            showCancelButton: false,
            confirmButtonText: "Aceptar",
            confirmButtonColor: "#007bff"
          });
          return;
        }
        // Preparar los datos para enviar
        const payload = {
          tipo_origen: this.formData.tipo_origen,
          origen: this.formData.origen,
          tipo_destino: this.formData.tipo_destino,
          destino: this.formData.destino,
          tipo_equipo: this.formData.tipo_equipo,
          operacion: this.formData.operacion,
          estado: this.formData.estado,
          producto: this.formData.producto,
          cantidad_vagones: this.vagonesAgregados.length,
          observaciones: this.formData.observaciones,
          informe_operativo: this.informeOperativoId,

          // Datos de los vagones (estructura corregida)
          equipo_vagon: this.vagonesAgregados.map((vagon) => ({
            equipo_ferroviario: vagon.equipo_ferroviario.id, // ID del equipo
            cant_dias: vagon.cant_dias,
            // Otros campos necesarios para el vagon
          })),
        };
        console.log("Payload a enviar:", payload);
        // Enviar los datos al backend
        const response = await axios.patch(
          `/ufc/pendiente-arrastre/${this.registroId}/`,
          payload
        );

        this.showSuccessToast("Registro actualizado");
        this.$router.push({ name: "InfoOperativo" });
      } catch (error) {
        console.error("Error al enviar el formulario:", error);
        let errorMessage = "Hubo un error al enviar el formulario";
        if (error.response) {
          
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

    resetForm() {
      this.formData = {
        tipo_origen: "",
        origen: "",
        tipo_destino: "",
        destino: "",
        tipo_equipo: "",
        operacion: "",
        estado: "cargado",
        productos: [], // Cambiado a array vacío
        cantidad_vagones: 1,
        observaciones: "",
      };
      this.vagonesAgregados = [];
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
    eliminarVagon(index) {
      this.vagonesAgregados.splice(index, 1);
      this.formData.cantidad_vagones = this.vagonesAgregados.length;
      this.showSuccessToast("Vagón eliminado");
    },
  },
};
</script>

<style scoped>
/* Nuevos estilos para los campos apareados */
.ufc-form-row {
  display: flex;
  gap: 15px;
}

.ufc-input-group.paired {
  flex: 1;
  min-width: 0; /* Evita problemas de desbordamiento */
}

/* Ajustes para el grid principal */
.ufc-form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 15px;
}

@media (max-width: 768px) {
  .ufc-form-row {
    flex-direction: column;
    gap: 10px;
  }

  .ufc-form-grid {
    grid-template-columns: 1fr;
  }
}

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

.ufc-por-situar-container {
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 6px;
  overflow: hidden;
  border-color: rgba(var(--bs-secondary-rgb),var(--bs-border-opacity)) !important;
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

.ufc-validation-message {
  padding: 10px;
  border-radius: 6px;
  font-size: 0.85rem;
  margin-top: 10px;
}

.ufc-validation-message.warning {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeeba;
}

.ufc-validation-message.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.ufc-validation-message.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

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

.full-width {
  grid-column: 1 / -1;
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
