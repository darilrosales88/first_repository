<template>
  <Navbar-Component />
  <div class="container py-3" style="margin-left: 20em; width: 70%">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-clipboard-data me-2"></i>Editar registro de vagón cargado/descargado
        </h5>
      </div>
      <div class="card-body p-3">
        <form @submit.prevent="submitForm">
          <div class="row">
            <!-- Columna 1 -->
            <div class="col-md-6">
              <!-- Campo: TEF -->
              <div class="mb-3">
                <label for="tipo_equipo_ferroviario" class="form-label small fw-semibold text-secondary">Tipo de equipo ferroviario</label>
                <select class="form-select form-select-sm border-secondary" v-model="formData.tipo_equipo_ferroviario" id="tipo_equipo_ferroviario" name="tipo_equipo_ferroviario" required>
                  <option v-for="tipo_equipo_ferroviario in tipos_equipos_ferroviarios" :key="tipo_equipo_ferroviario.id" :value="tipo_equipo_ferroviario.id">
                    {{ tipo_equipo_ferroviario.id }}-{{tipo_equipo_ferroviario.tipo_equipo_name}}-{{ tipo_equipo_ferroviario.descripcion }}
                  </option>
                </select>
              </div>

              <!-- Campo: tipo_origen -->
              <div class="mb-3">
                <label for="tipo_origen" class="form-label small fw-semibold text-secondary">Tipo de Origen</label>
                <select class="form-select form-select-sm border-secondary" v-model="formData.tipo_origen" id="tipo_origen" name="tipo_origen">
                  <option value="ac_ccd">Acceso Comercial</option>
                  <option value="puerto">Puerto</option>
                </select>
              </div>

              <!-- Campo: origen -->
              <div class="mb-3">
                <label for="origen" class="form-label small fw-semibold text-secondary">Origen</label>
                <select v-if="formData.tipo_origen !== 'puerto'" class="form-select form-select-sm border-secondary" v-model="formData.origen" id="origen" name="origen">
                  <option v-for="entidad in entidades" :key="entidad.id" :value="entidad.nombre">
                    {{ entidad.id }}-{{ entidad.nombre }}
                  </option>
                </select>

                <select v-else class="form-select form-select-sm border-secondary" v-model="formData.origen" id="origen" name="origen">
                  <option v-for="puerto in puertos" :key="puerto.id" :value="puerto.nombre_puerto">
                    {{ puerto.id }}- {{ puerto.nombre_puerto }}
                  </option>
                </select>
              </div>

              <!-- Campo: tipo_destino -->
              <div class="mb-3">
                <label for="tipo_destino" class="form-label small fw-semibold text-secondary">Tipo de Destino</label>
                <select class="form-select form-select-sm border-secondary" v-model="formData.tipo_destino" id="tipo_destino" name="tipo_destino" required>
                  <option value="ac_ccd">Acceso Comercial</option>
                  <option value="puerto">Puerto</option>
                </select>
              </div>

              <!-- Campo: destino -->
              <div class="mb-3">
                <label for="destino" class="form-label small fw-semibold text-secondary">Destino</label>
                <select v-if="formData.tipo_destino !== 'puerto'" class="form-select form-select-sm border-secondary" v-model="formData.destino" id="tipo_destino" name="tipo_destino">
                  <option v-for="entidad in entidades" :key="entidad.id":value="entidad.nombre">
                    {{ entidad.id }}-{{ entidad.nombre }}
                  </option>
                </select>

                <select v-else class="form-select form-select-sm border-secondary" v-model="formData.destino" id="destino" name="destino">
                  <option v-for="puerto in puertos" :key="puerto.id" :value="puerto.nombre_puerto">
                    {{ puerto.id }}- {{ puerto.nombre_puerto }}
                  </option>
                </select>
              </div>

              <!-- Campo: estado -->
              <div class="mb-3">
                <label for="estado" class="form-label small fw-semibold text-secondary">Estado</label>
                <select class="form-select form-select-sm border-secondary" v-model="formData.estado" id="estado" name="estado" required>
                  <option value="cargado">Cargado</option>
                  <option value="vacio">Vacio</option>
                </select>
              </div>
            </div>

            <!-- Columna 2 -->
            <div class="col-md-6">
              <!-- Campo: operacion -->
              <div class="mb-3">
                <label for="operacion" class="form-label small fw-semibold text-secondary">Operación</label>
                <input type="text" class="form-control form-control-sm border-secondary" v-model="formData.operacion" id="operacion" name="operacion" readonly/>
              </div>

              
              <!-- Campo: plan_diario_carga -->
              <div class="mb-3">
                <label for="plan_diario_carga" class="form-label small fw-semibold text-secondary">Plan diario de carga/descarga</label>
                <input type="number" class="form-control form-control-sm border-secondary" v-model="formData.plan_diario_carga_descarga" id="plan_diario_carga_descarga" name="plan_diario_carga_descarga"/>
              </div>

              <!-- Campo: plan_diario_carga -->
              <div class="mb-3">
                <label for="real_carga_descarga" class="form-label small fw-semibold text-secondary">Real de carga/descarga</label>
                <input type="number" class="form-control form-control-sm border-secondary" v-model="formData.real_carga_descarga" id="real_carga_descarga" name="real_carga_descarga" readonly/>
              </div>

              <!-- Campo: producto -->
              <div class="mb-3">
                <label for="producto" class="form-label small fw-semibold text-secondary">Productos <span v-if="formData.estado === 'cargado'" class="required"></span></label>
                <div class="ufc-input-with-action">
                  <div class="ufc-custom-select" @click="toggleProductosDropdown">
                    <div class="ufc-select-display">
                      {{ getSelectedProductosText() || 'Seleccione productos...' }}
                    </div>
                    <i class="bi bi-chevron-down ufc-select-arrow"></i>
                    
                    <div class="ufc-productos-dropdown" v-if="showProductosDropdown">
                      <div class="ufc-productos-search-container">
                        <input
                          type="text"
                          class="ufc-productos-search"
                          placeholder="Buscar productos..."
                          v-model="productoSearch"
                          @input="filterProductos"
                          @click.stop>
                      </div>
                      <div class="ufc-productos-options">
                        <div
                          v-for="producto in filteredProductos"
                          :key="producto.id"
                          class="ufc-producto-option"
                          :class="{ 'selected': formData.lista_productos.includes(producto.id) }"
                          @click.stop="toggleProductoSelection(producto.id)">
                          {{ producto.id }}-{{ producto.producto_name }} - {{ producto.producto_codigo }}
                          <template v-if="producto.tipo_embalaje">
                            (Embalaje: {{ producto.tipo_embalaje.nombre || producto.tipo_embalaje.nombre_embalaje || 'N/A' }})
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

              <!-- Modal para agregar producto cargado/descargado -->
              <ModalAgregarProducto v-if="mostrarModalProducto" :visible="mostrarModalProducto" @cerrar-modal="cerrarModalAddProductoCargado"/>

              <!-- Modal para agregar vagon a estado cargado/descargado -->
              <ModalAgregarVagonCargado v-if="mostrarModalVagon" :visible="mostrarModalVagon" :tipo-equipo="formData.tipo_equipo_ferroviario" @cerrar-modal="cerrarModalAddVagonCargado" @vagon-agregado="handleVagonAgregado"/>

              <!-- Campo: causas_incumplimiento -->
              <div class="mb-3">
                <label for="causas_incumplimiento" class="form-label small fw-semibold text-secondary">Causas del incumplimiento
                </label>
                <textarea class="form-control form-control-sm border-secondary" v-model="formData.causas_incumplimiento" id="causas_incumplimiento" name="causas_incumplimiento" rows="3" required></textarea>
              </div>
            </div>
          </div>

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
          *Debe existir al menos un vagón
        </h5>
      </div>
      <div class="card-body p-3">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <button class="btn btn-primary" @click="abrirModalAgregarVagon">
            <i class="bi bi-plus-circle me-1"></i>Agregar vagón
          </button>
        </div>
        <!-- Tabla responsive con mejoras -->
        <div class="table table-responsive">
          <table class="table table-sm table-bordered table-hover">
            <thead class="table-light">
              <tr>
                <th scope="col">No ID</th>
                <th scope="col">Fecha de despacho</th>
                <th scope="col">Origen</th>
                <th scope="col">Fecha de llegada</th>
                <th scope="col">Observaciones</th>
                <th scope="col">Acciones</th>
              </tr>
              <tr v-if="registros_vagones_cargados.length == 0">
                <td colspan="8" class="text-center text-muted py-4">
                  <div class="ps-loading" v-if="loading">
                    <div class="ps-spinner"></div>
                    <span>Cargando registros...</span>
                  </div>
                  <div v-else>
                    <i class="bi bi-database-exclamation fs-4"></i>
                    <p class="mt-2">
                      No hay registros
                    </p>
                  </div>
                </td>
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
              <tr v-for="(item, index) in registros_vagones_cargados" :key="item.id" class="align-middle">
                <td>{{ item.no_id || "Sin ID" }}</td>
                <td>{{ item.fecha_despacho }}</td>
                <td>{{ item.origen }}</td>
                <td>{{ item.fecha_llegada }}</td>
                <td>{{ item.observaciones }}</td>
                <td v-if="hasGroup('AdminUFC')">
                  <div class="d-flex">
                    <button @click.prevent="confirmDeleteVagonAsignado(item)" class="btn btn-sm btn-outline-danger" title="Eliminar">
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
    
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import NavbarComponent from "@/components/NavbarComponent.vue";
import ModalAgregarProductoCargadoDescargado from "@/components/ModaAgregarProductoCargadoDescargado.vue";
import ModalAgregarVagonCargado from "@/components/ModaAgregarVagonCargado.vue";
import ModalAgregarProducto from "@/components/ModalAgregarProducto.vue";
export default {
  name: "EditarCargadoDescargado",
  components: {
    NavbarComponent,
    ModalAgregarProductoCargadoDescargado,
    ModalAgregarProducto,
    ModalAgregarVagonCargado,
  },
  props: {
    id: {
      type: [String, Number],
      required: true,
    },
  },
  data() {
    return {
      loading: false,
      mostrarModalVagon: false,
      mostrarModalProducto: false,
      formData: {
        tipo_equipo_ferroviario: "",
        tipo_origen: "ac_ccd",
        origen: "",
        tipo_destino: "ac_ccd",
        destino: "",
        estado: "cargado",
        lista_productos: [],
        original_productos: [],
        plan_diario_carga_descarga: "",
        real_carga_descarga: "",
        operacion: "",
        causas_incumplimiento: "",
        original_equipo: null,
      },
      showProductosDropdown: false,
      filteredProductos: [],
      registros_vagones_temporales: [],
      registros_vagones_cargados: [],
      userGroups: [],
      userPermissions: [],
      productos: [],
      tipos_equipos_ferroviarios: [],
      puertos: [],
      entidades: [],
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
    "formData.lista_productos": {
      handler() {
        this.calcularRealCargaDescarga();
      },
      deep: true,
    },
  },
  async created() {
    await this.fetchUserPermissionsAndGroups();
    await this.getProductos();
    await this.getNoLocomotoras();
    await this.getEntidades();
    this.filteredProductos = this.lista_productos;
    this.closeDropdownsOnClickOutside();
    await this.getPuertos();
    await this.loadVagonData();
  },
  methods: {
    async loadVagonData() {
      /* this.loading = true; */
      try {
        // 1. Obtener datos principales
        const mainResponse = await axios.get(
          `/ufc/vagones-cargados-descargados/${this.id}/`
        );
        const vagonData = mainResponse.data;

        // 2. Obtener registros asociados - manejar posibles errores
        let registrosVagones = [];
        try {
          const registrosResponse = await axios.get(
            `/ufc/vagones-cargados-descargados/${this.id}/registros-completos/`
          );
          registrosVagones = registrosResponse.data || [];
        } catch (error) {
          console.error("Error al obtener registros asociados:", error);
          registrosVagones = [];
        }

        // 3. Asignar datos principales
        this.formData = {
          tipo_equipo_ferroviario:
            vagonData.tipo_equipo_ferroviario?.id ||
            vagonData.tipo_equipo_ferroviario ||
            "",
          tipo_origen: vagonData.tipo_origen || "ac_ccd",
          origen: vagonData.origen || "",
          tipo_destino: vagonData.tipo_destino || "ac_ccd",
          destino: vagonData.destino || "",
          estado: vagonData.estado || "cargado",
          lista_productos: Array.isArray(vagonData.producto)
            ? vagonData.producto.map((p) => p.id || p)
            : vagonData.producto_ids || [],
          original_productos: Array.isArray(vagonData.producto)
            ? vagonData.producto.filter((p) => p && p.id)
            : [],
          plan_diario_carga_descarga:
            vagonData.plan_diario_carga_descarga || "",
          real_carga_descarga: vagonData.real_carga_descarga || "",
          operacion:
            vagonData.operacion ||
            (vagonData.estado === "cargado" ? "descarga" : "carga"),
          causas_incumplimiento: vagonData.causas_incumplimiento || "",
          original_equipo:
            vagonData.tipo_equipo_ferroviario?.tipo_equipo_name ||
            vagonData.tipo_equipo_ferroviario_name ||
            "",
        };

        // 4. Asignar registros de vagones con verificación
        if (!Array.isArray(registrosVagones)) {
          console.warn("registrosVagones no es un array:", registrosVagones);
          registrosVagones = [];
        }

        // Asignación segura a la propiedad reactiva
        this.registros_vagones_cargados = registrosVagones.map((vagon) => ({
          id: vagon.id,
          no_id: vagon.no_id || "Sin ID",
          fecha_despacho: vagon.fecha_despacho || "",
          tipo_origen: vagon.tipo_origen || "ac_ccd",
          origen: vagon.origen || "",
          fecha_llegada: vagon.fecha_llegada || "",
          observaciones: vagon.observaciones || "",
        }));

        // Depuración: verificar asignación
        console.log(
          "Después de loadVagonData, registros_vagones_cargados:",
          this.registros_vagones_cargados
        );
      } catch (error) {
        console.error("Error al cargar datos del vagón:", error);
        Swal.fire("Error", "No se pudo cargar los datos del vagón", "error");
        this.goBack();
      } finally {
        this.loading = false;
      }
    },

    // Métodos para manejar modales
    abrirModalAgregarProducto() {
      this.mostrarModalProducto = true;
    },
    cerrarModalAddProductoCargado() {
      this.mostrarModalProducto = false;
      this.getProductos();
    },
    abrirModalAgregarVagon() {
      this.mostrarModalVagon = true;
    },
    cerrarModalAddVagonCargado() {
      this.mostrarModalVagon = false;
    },

    // Métodos para permisos
    hasPermission(permission) {
      return this.userPermissions.some((p) => p.name === permission);
    },
    hasGroup(group) {
      return this.userGroups.some((g) => g.name === group);
    },
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
      } catch (error) {
        console.error("Error al obtener permisos y grupos:", error);
      }
    },

    // Métodos para cálculos
    async calcularRealCargaDescarga() {
      if (
        !this.formData.lista_productos ||
        this.formData.lista_productos.length === 0
      ) {
        this.formData.real_carga_descarga = 0;
        return;
      }

      try {
        const response = await axios.post(
          "/ufc/vagones-cargados-descargados/calcular_total_vagones_por_productos/",
          { producto_ids: this.formData.lista_productos }
        );
        this.formData.real_carga_descarga = response.data.total;
      } catch (error) {
        console.error("Error al calcular el total de vagones:", error);
        this.formData.real_carga_descarga = 0;
      }
    },

    // Métodos para CRUD
    async submitForm() {
      if (!this.registros_vagones_cargados) {
        console.error("registros_vagones_cargados es undefined!");
        this.registros_vagones_cargados = [];
      }

      this.loading = true;
      try {
        const payload = {
          tipo_equipo_ferroviario: this.formData.tipo_equipo_ferroviario,
          tipo_origen: this.formData.tipo_origen,
          origen: this.formData.origen,
          tipo_destino: this.formData.tipo_destino,
          destino: this.formData.destino,
          estado: this.formData.estado,
          producto_ids: Array.isArray(this.formData.lista_productos)
            ? this.formData.lista_productos
            : [this.formData.lista_productos],
          plan_diario_carga_descarga: this.formData.plan_diario_carga_descarga,
          real_carga_descarga: this.formData.real_carga_descarga,
          operacion: this.formData.operacion,
          causas_incumplimiento: this.formData.causas_incumplimiento,
          registros_vagones_data: this.registros_vagones_cargados.map((v) => ({
            id: v.id || null, // Incluir el ID si existe para actualización
            no_id: v.no_id,
            fecha_despacho: v.fecha_despacho,
            tipo_origen: v.tipo_origen || "ac_ccd",
            origen: v.origen,
            fecha_llegada: v.fecha_llegada || null,
            observaciones: v.observaciones || "",
          })),
        };

        console.log("Payload a enviar:", payload); // Para depuración

        const response = await axios.put(
          `/ufc/vagones-cargados-descargados/${this.id}/`,
          payload,
          {
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": this.getCookie("csrftoken"),
            },
          }
        );

        await Swal.fire({
          title: "Éxito",
          text: "Vagón actualizado correctamente",
          icon: "success",
        });

        this.$router.push({ name: "InfoOperativo" });
      } catch (error) {
        console.error("Error al actualizar:", error);

        let errorMsg = "Error al actualizar el vagón";
        if (error.response?.data) {
          errorMsg += `: ${JSON.stringify(error.response.data)}`;
        }

        Swal.fire({
          title: "Error",
          text: errorMsg,
          icon: "error",
        });
      } finally {
        this.loading = false;
      }
    },

    // Método auxiliar para obtener cookies
    getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    },

    confirmDeleteVagonAsignado(item) {
      if (!item) {
        console.error("Item a eliminar es null/undefined");
        Swal.fire("Error", "No se puede eliminar: elemento no válido", "error");
        return;
      }

      Swal.fire({
        title: "¿Estás seguro?",
        text: "¿Quieres eliminar este vagón de la lista?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
      }).then((result) => {
        if (result.isConfirmed) {
          this.deleteVagonTemporal(item);
        }
      });
    },

    handleVagonAgregado(nuevoVagon) {
      // Validar campos obligatorios
      if (
        !nuevoVagon.no_id ||
        !nuevoVagon.fecha_despacho ||
        !nuevoVagon.origen
      ) {
        Swal.fire(
          "Error",
          "Debe completar todos los campos obligatorios del vagón",
          "error"
        );
        return;
      }

      const existe = this.registros_vagones_cargados.some(
        (v) =>
          v.no_id === nuevoVagon.no_id &&
          v.fecha_despacho === nuevoVagon.fecha_despacho
      );

      if (existe) {
        Swal.fire(
          "Advertencia",
          "Este vagón ya fue agregado a la lista",
          "warning"
        );
        return;
      }

      this.registros_vagones_cargados.push({
        no_id: nuevoVagon.no_id,
        fecha_despacho: nuevoVagon.fecha_despacho,
        tipo_origen: nuevoVagon.tipo_origen || "ac_ccd",
        origen: nuevoVagon.origen,
        fecha_llegada: nuevoVagon.fecha_llegada || "",
        observaciones: nuevoVagon.observaciones || "",
      });
    },

    deleteVagonTemporal(item) {
      try {
        if (!item || typeof item !== "object" || item === null) {
          throw new Error("El elemento a eliminar no es válido");
        }

        const index = this.registros_vagones_cargados.findIndex(
          (vagon) =>
            vagon &&
            vagon.no_id === item.no_id &&
            vagon.fecha_despacho === item.fecha_despacho
        );

        if (index === -1) {
          Swal.fire("Error", "No se encontró el vagón en la lista", "error");
          return;
        }

        this.registros_vagones_cargados.splice(index, 1);
        Swal.fire("Éxito", "Vagón eliminado correctamente", "success");
      } catch (error) {
        console.error("Error al eliminar vagón temporal:", error);
        Swal.fire(
          "Error",
          `No se pudo eliminar el vagón: ${error.message}`,
          "error"
        );
      }
    },

    // Métodos para obtener datos
    async getNoLocomotoras() {
      try {
        const response = await axios.get("/api/tipo-e-f-no-locomotora/");
        this.tipos_equipos_ferroviarios = response.data.map((item) => ({
          ...item,
          id: item.id.toString(),
        }));
      } catch (error) {
        console.error("Error al obtener los equipos ferroviarios:", error);
        Swal.fire(
          "Error",
          "Hubo un error al obtener los equipos ferroviarios.",
          "error"
        );
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
      const index = this.formData.lista_productos.indexOf(productoId);
      if (index === -1) {
        this.formData.lista_productos.push(productoId);
      } else {
        this.formData.lista_productos.splice(index, 1);
      }
    },

    getSelectedProductosText() {
      if (this.formData.lista_productos.length === 0) return "";
      if (this.formData.lista_productos.length === 1) {
        const producto = this.productos.find(
          (p) => p.id === this.formData.lista_productos[0]
        );
        return producto
          ? `${producto.id}-${producto.producto_name}`
          : "1 producto seleccionado";
      }
      return `${this.formData.lista_productos.length} productos seleccionados`;
    },

    closeDropdownsOnClickOutside() {
      document.addEventListener("click", (e) => {
        if (!e.target.closest(".ufc-custom-select")) {
          this.showProductosDropdown = false;
        }
      });
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

        this.productos = allProductos.map((p) => ({
          ...p,
          id: p.id?.toString() || "",
        }));
      } catch (error) {
        console.error("Error al obtener los productos:", error);
        Swal.fire("Error", "Hubo un error al obtener los productos.", "error");
      }
    },

    // Navegación
    goBack() {
      this.$router.go(-1);
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
</style>
