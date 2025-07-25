<template>
  <div class="ufc-header">
    <h6>Partes UFC</h6>
  </div>
  <Navbar-Component />
  <div class="container py-3" style="margin-left: 20em; width: 70%">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-clipboard-data me-2"></i>Nuevo registro de vagón cargado/descargado
        </h5>
      </div>
      <div class="card-body p-3">
        <form @submit.prevent="submitForm">
          <div class="row">
            <!-- Columna 1 -->
            <div class="col-md-6">
              <!-- Campo:Fecha de registro -->
              <div class="mb-3">
                <label for="fecha_registro" class="form-label small fw-semibold text-secondary">Fecha de registro</label>
                <input type="text" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" :value="formattedFechaRegistro" id="fecha_registro" name="fecha_registro" readonly/>
              </div>

              <div class="ufc-form-group">
                <div class="ufc-form-row">
                  <!-- Campo: tipo_origen -->
                  <div class="mb-3">
                    <label for="tipo_origen" class="form-label small fw-semibold text-secondary">Tipo de Origen</label>
                    <select class="form-select form-select-sm border-secondary" style="width:187px; padding-top:8px;padding-bottom:8px;" v-model="formData.tipo_origen" id="tipo_origen" name="tipo_origen" required
                      oninvalid="this.setCustomValidity('Por favor, seleccione un tipo de origen')"
                      oninput="this.setCustomValidity('')">
                      <option value="" disabled>Seleccione un tipo</option>
                      <option value="ac_ccd">Acceso Comercial</option>
                      <option value="puerto">Puerto</option>
                    </select>
                  </div>

                  <!-- Campo: origen -->
                  <div class="mb-3">
                    <label for="origen" class="form-label small fw-semibold text-secondary" >Origen</label>
                    <select v-if="formData.tipo_origen !== 'puerto' && formData.tipo_origen != ''" class="form-select form-select-sm border-secondary" style="width:230px; padding-top:8px;padding-bottom:8px;"  v-model="formData.origen" id="origen" name="origen" required
                      oninvalid="this.setCustomValidity('Por favor, seleccione un origen')"
                      oninput="this.setCustomValidity('')">
                      <option value="" disabled>Seleccione un destino</option>
                      <option v-for="entidad in entidades" :key="entidad.id" :value="entidad.nombre">
                        {{ entidad.id }}-{{ entidad.nombre }}
                      </option>
                    </select>

                    <select v-else-if ="formData.tipo_origen === 'puerto' && formData.tipo_origen != ''" class="form-select form-select-sm border-secondary" style="width:230px; padding-top:8px;padding-bottom:8px;" v-model="formData.origen" id="origen" name="origen" required
                      oninvalid="this.setCustomValidity('Por favor, seleccione un puerto')"
                      oninput="this.setCustomValidity('')">
                      <option value="" disabled>Seleccione un puerto</option>
                      <option v-for="puerto in puertos" :key="puerto.id" :value="puerto.nombre_puerto">
                        {{ puerto.id }}- {{ puerto.nombre_puerto }}
                      </option>
                    </select>
                    <select
                      v-if="formData.tipo_origen == '' "
                      class="form-select form-select-sm border-secondary" style="width:230px; padding-top:8px;padding-bottom:8px;"
                      disabled>
                      <option value="">Seleccione un tipo de destino</option>
                    </select>
                  </div>
                </div>
              </div>

              <div class="ufc-form-group">
                <div class="ufc-form-row">
                  <!-- Campo: tipo_destino -->
                  <div class="mb-3">
                    <label for="tipo_destino" class="form-label small fw-semibold text-secondary">Tipo de Destino</label>
                    <select class="form-select form-select-sm border-secondary" style="width:187px; padding-top:8px;padding-bottom:8px;" v-model="formData.tipo_destino" id="tipo_destino" name="tipo_destino" required
                      oninvalid="this.setCustomValidity('Por favor, seleccione un tipo de destino')"
                      oninput="this.setCustomValidity('')">
                      <option value="" disabled>Seleccione un destino</option>
                      <option value="ac_ccd">Acceso Comercial</option>
                      <option value="puerto">Puerto</option>
                    </select>
                  </div>

                  <!-- Campo: destino -->
                  <div class="mb-3">
                    <label for="destino" class="form-label small fw-semibold text-secondary">Destino</label>
                    <select v-if="formData.tipo_destino !== 'puerto' && formData.tipo_destino != ''" class="form-select form-select-sm border-secondary" style="width:230px; padding-top:8px;padding-bottom:8px;" v-model="formData.destino" id="tipo_destino" name="tipo_destino" required
                      oninvalid="this.setCustomValidity('Por favor, seleccione un destino')"
                      oninput="this.setCustomValidity('')">
                      <option value="" disabled>Seleccione un destino</option>
                      <option v-for="entidad in entidades" :key="entidad.id":value="entidad.nombre">
                        {{ entidad.id }}-{{ entidad.nombre }}
                      </option>
                    </select>

                    <select v-else-if ="formData.tipo_destino === 'puerto' && formData.tipo_destino != ''" class="form-select form-select-sm border-secondary" style="width:230px; padding-top:8px;padding-bottom:8px;" v-model="formData.destino" id="destino" name="destino" required
                      oninvalid="this.setCustomValidity('Por favor, seleccione un puerto')"
                      oninput="this.setCustomValidity('')">
                      <option value="" disabled>Seleccione un puerto</option>
                      <option v-for="puerto in puertos" :key="puerto.id" :value="puerto.nombre_puerto">
                        {{ puerto.id }}- {{ puerto.nombre_puerto }}
                      </option>
                    </select>
                    <select
                      v-if="formData.tipo_destino == '' "
                      class="form-select form-select-sm border-secondary" style="width:230px; padding-top:8px;padding-bottom:8px;"
                      disabled>
                      <option value="">Seleccione un tipo de destino</option>
                    </select>
                  </div>
                </div>
              </div>
              <!-- Campo: TEF -->
              <div class="mb-3">
                <label for="tipo_equipo_ferroviario" class="form-label small fw-semibold text-secondary">Tipo de Equipo Ferroviario</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" v-model="formData.tipo_equipo_ferroviario" id="tipo_equipo_ferroviario" name="tipo_equipo_ferroviario" required
                  oninvalid="this.setCustomValidity('Por favor, seleccione un tipo de equipo ferroviario')"
                  oninput="this.setCustomValidity('')">
                  <option v-for="tipo_equipo_ferroviario in tipos_equipos_ferroviarios" :key="tipo_equipo_ferroviario.id" :value="tipo_equipo_ferroviario.id">
                    {{ tipo_equipo_ferroviario.id }}-{{tipo_equipo_ferroviario.tipo_equipo_name}}-{{ tipo_equipo_ferroviario.descripcion }}
                  </option>
                </select>
              </div>
            </div>

            <!-- Columna 2 -->
            <div class="col-md-6">
              <!-- Campo: estado -->
              <div class="mb-3">
                <label for="estado" class="form-label small fw-semibold text-secondary">Estado</label>
                <select class="form-select form-select-sm border-secondary" style="padding: 8px 12px;" v-model="formData.estado" id="estado" name="estado" required>
                  <option value="cargado">Cargado</option>
                  <option value="vacio">Vacio</option>
                </select>
              </div>

              <!-- Campo: operacion -->
              <div class="mb-3">
                <label for="operacion" class="form-label small fw-semibold text-secondary">Operación</label>
                <input type="text" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" v-model="formData.operacion" id="operacion" name="operacion" readonly/>
              </div>

              <!-- Campo: plan_diario_carga -->
              <div class="mb-3">
                <label for="plan_diario_carga" class="form-label small fw-semibold text-secondary">Plan diario de carga/descarga</label>
                <input type="number" class="form-control form-control-sm border-secondary" style="padding: 8px 12px;" v-model="formData.plan_diario_carga_descarga" id="plan_diario_carga_descarga" min="0" name="plan_diario_carga_descarga"/>
              </div>

               <div class="mb-3">
                <!-- Campo: Productos-->
                <div class="mb-3">
                  
                  <label
                    for="productos"
                    class="form-label small fw-semibold text-secondary"
                    >Productos</label
                  >
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
                        <!-- Esto tambien hay que modificarlo en los demas y quitar las funciones basuras ademas de agregar esto mismo en los editar de cada uno @BZ-theFanG #-# -->
                        {{ producto.producto_name }}-{{
                          producto.producto_codigo
                        }}-{{ producto.tipo_embalaje_name }}
                      </option>
                    </select>
                    <button class="create-button ms-2" @click.stop.prevent="abrirModalAgregarProducto">
                      <i class="bi bi-plus-circle large-icon"></i>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Modal para agregar producto cargado/descargado -->
              <ModalAgregarProducto v-if="mostrarModalProducto" :visible="mostrarModalProducto" @cerrar-modal="cerrarModalAddProductoCargado"/>

              <!-- Modal para agregar vagon a estado cargado/descargado -->
              <ModalAgregarVagonCargado v-if="mostrarModalVagon" :visible="mostrarModalVagon" :tipo-equipo="formData.tipo_equipo_ferroviario" @cerrar-modal="cerrarModalAddVagonCargado" @vagon-agregado="handleVagonAgregado"/>

            </div>
          </div>
          <!-- Campo: causas_incumplimiento -->
          <div class="full-width">
            <label for="causas_incumplimiento" class="form-label small fw-semibold text-secondary">Causas del incumplimiento
            </label>
            <textarea class="form-control form-control-sm border-secondary" v-model="formData.causas_incumplimiento" id="causas_incumplimiento" name="causas_incumplimiento" rows="4" required
            oninvalid="this.setCustomValidity('Por favor, escriba las causas del imcumplimiento')"
            oninput="this.setCustomValidity('')"></textarea>
          </div>

          <div class="modal-footer mt-3">
            <div class=" d-flex justify-content-between align-items-center mb-4">
              <button class="ufc-button secondary" @click="volver_principal">
                <i class="bi bi-x-circle" me-1></i>Cancelar
              </button>
              <button type="submit" class=" ufc-button primary" >
                <i class="bi bi-check-circle" me-1></i>Agregar
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
import ModalAgregarVagonCargado from "@/components/ModaAgregarVagonCargado.vue";
import ModalAgregarProducto from "@/components/ModalAgregarProducto.vue";
export default {
  name: "AdicionarVagonCargadoDescargado",
  components: {
    NavbarComponent,
    ModalAgregarVagonCargado,
    ModalAgregarProducto,
  },
  data() {
    return {
      /*para que cuando se abra el modal de adicionar vagon se oculte el formulario padre */
      mostrarModalVagon: false,

      formData: {
        fecha:"",
        tipo_equipo_ferroviario: "",
        tipo_origen: "",
        origen: "",
        tipo_destino: "",
        destino: "",
        estado: "cargado",
        producto: [],
        plan_diario_carga_descarga: "",
        real_carga_descarga: "",
        operacion: "",
        causas_incumplimiento: "", // Asegúrate de incluir este campo
      },
      showProductosDropdown: false,
      filteredProductos: [],
      registros_vagones_temporales: [], // Asegúrate de inicializarlo como array vacío
      //vagonPrincipalId: null, // Para almacenar el ID del vagon principal
      userGroups: [], // Inicializa como array vacío
      userPermissions: [], // Inicializa como array vacío
      registros_vagones_cargados: [], // Lista filtrada de resitros de vagones en el estado cargado/descargado
      mostrarModalProducto: false,
      productos: [],
      equipos: [],
      equipos_vagones: [],
      tipos_equipos_ferroviarios: [],
      puertos: [],
      entidades: [],
      informeOperativoId: null,
      fechaActual: new Date().toISOString().split('T')[0],
      allRecords: [], // Copia completa de todos los registros para filtrado local
    };
  },

  computed: {
    formattedFechaRegistro() {
      if (this.formData.fecha) {
        return new Date(this.formData.fecha).toLocaleString();
      }
      return new Date().toLocaleString();
    }
  },

  mounted() {
    // Llama al método para obtener los puertos
    this.getProductos();
    this.getNoLocomotoras();
    this.getEntidades();
    this.filteredProductos = this.producto;
    this.closeDropdownsOnClickOutside();
    this.getPuertos();
  },

  /*actualizando automaticamente el valor del campo operacion a partir del campo estado */
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

    "formData.producto": {
      handler(newVal, oldVal) {
        if (JSON.stringify(newVal) !== JSON.stringify(oldVal)) {
          this.calcularRealCargaDescarga();
        }
      },
      deep: true
    }
  },
  async created() {
    await this.fetchUserPermissionsAndGroups(); // Espera a que se carguen los permisos
    //await this.GetRegistroVagonesCargadosDescargados(); // Luego carga los registros
  },

  methods: {
    async verificarInformeOperativo() {
      try {
        this.formData.fecha = new Date().toISOString();
        const today = new Date();
        const fechaFormateada = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;

        const response = await axios.get('/ufc/verificar-informe-existente/', {
          params: { fecha_operacion: fechaFormateada }
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
    
    async verificarInformeOperativo() {
      try {
        this.formData.fecha = new Date().toISOString();
        const today = new Date();
        const fechaFormateada = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;

        const response = await axios.get('/ufc/verificar-informe-existente/', {
          params: { fecha_operacion: fechaFormateada }
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
    
    async submitForm() {
      try {
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

        const informeNoAprobado = await this.verificarEstadoInforme();
        if (!informeNoAprobado) {
          Swal.fire(
            "Error",
            "No se puede agregar registros a un informe operativo que ya ha sido aprobado.",
            "error"
          );
          return;
        }

        if (this.registros_vagones_temporales.length === 0) {
          Swal.fire("Error", "Debe agregar al menos un vagón", "error");
          return;
        }

        if (this.formData.estado === "cargado" && this.formData.producto.length === 0) {
          this.showErrorToast("Debe seleccionar al menos un producto cuando el estado es Cargado");
          return;
        }

        if (this.formData.origen === this.formData.destino) {
          Swal.fire("Error", "No puede tener el mismo Origen y Destino", "error");
          return;
        }

        // Preparar datos para enviar
        const datosEnvio = {
          tipo_equipo_ferroviario: this.formData.tipo_equipo_ferroviario,
          tipo_origen: this.formData.tipo_origen,
          origen: this.formData.origen,
          tipo_destino: this.formData.tipo_destino,
          destino: this.formData.destino,
          estado: this.formData.estado,
          operacion: this.formData.operacion,
          plan_diario_carga_descarga: Number(this.formData.plan_diario_carga_descarga),
          causas_incumplimiento: this.formData.causas_incumplimiento || 'Sin causas especificadas',
          producto_ids: this.formData.producto,
          registros_vagones_data: this.registros_vagones_temporales.map(v => ({
            no_id: v.no_id,
            fecha_despacho: v.fecha_despacho,
            tipo_origen: v.tipo_origen || this.formData.tipo_origen,
            origen: v.origen || this.formData.origen,
            fecha_llegada: v.fecha_llegada || null,
            observaciones: v.observaciones || ''
          })),
          informe_operativo: this.informeOperativoId
        };

        // Enviar datos
        const response = await axios.post("/ufc/vagones-cargados-descargados/", datosEnvio);
        
        // Mostrar mensaje de éxito
        this.showSuccessToast("El registro ha sido creado correctamente");
        this.resetForm();
        this.$router.push({ name: "InfoOperativo" });
        
      } catch (error) {
        console.error("Error detallado:", error.response?.data);
        let errorMsg = "Error al guardar el registro";
        this.showErrorToast("Error al guardar el registro");
        if (error.response?.data) {
          if (typeof error.response.data === 'object') {
            errorMsg += ": " + JSON.stringify(error.response.data);
          } else {
            errorMsg += ": " + error.response.data;
          }
        }
        
        Swal.fire("Error", errorMsg, "error");
      }
    },
    async calcularRealCargaDescarga() {
      if (!this.formData.producto?.length) {
        this.formData.real_carga_descarga = 0;
        return;
      }

      try {
        const response = await axios.post(
          "/ufc/vagones-cargados-descargados/calcular_total_vagones_por_productos/",
          { producto_ids: [...this.formData.producto] } // Enviar copia
        );
        this.formData.real_carga_descarga = response.data.total;
      } catch (error) {
        console.error("Error al calcular:", error);
        this.formData.real_carga_descarga = 0;
      }
    },

    resetForm() {
      this.formData = {
        tipo_equipo_ferroviario: "",
        tipo_origen: "",
        origen: "",
        tipo_destino: "",
        destino: "",
        estado: "cargado",
        producto: [],
        plan_diario_carga_descarga: "",
        real_carga_descarga: "",
        operacion: "",
        causas_incumplimiento: "",
      };
    },
    // Al abrir/cerrar el modal hijo
    abrirModalAgregarVagon() {
      this.mostrarModalVagon = true;
    },

    cerrarModalAddVagonCargado() {
      this.mostrarModalVagon = false;
    },
    // Verifica si el usuario tiene un permiso específico
    hasPermission(permission) {
      return this.userPermissions.some((p) => p.name === permission);
    },
    // Verifica si el usuario pertenece a un grupo específico
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
        console.log("Permisos: ",this.userPermissions );
        console.log("Grupos: ",this.userGroups );
        console.log("Permisos: ",this.userPermissions );
        console.log("Grupos: ",this.userGroups );
      } catch (error) {
        console.error("Error al obtener permisos y grupos:", error);
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

    handleVagonAgregado(nuevoVagon) {
      // Verificar si el vagón ya está en la lista temporal
      const existe = this.registros_vagones_temporales.some(
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

      // Agregar a la lista temporal
      this.registros_vagones_temporales.push({
        ...nuevoVagon,
        id: null,
      });

      // Actualizar lista de visualización (creando nuevo array)
      this.registros_vagones_cargados = [...this.registros_vagones_temporales];
    },

    // Método para agregar registros temporales desde el modal
    agregarRegistroTemporal(registro) {
      this.registros_vagones_temporales.push(registro);
    },

    /*        // Obtiene los registros de los vagones del estado cargado/descargado
    async GetRegistroVagonesCargadosDescargados() {

      try {
        this.loading = true;
        const response = await axios.get("/ufc/registro-vagones-cargados/");
        
        // Actualizar ambas listas
        this.registros_vagones_cargados = response.data.results || [];
        this.registros_vagones_temporales = [...this.registros_vagones_cargados];

      } catch (error) {
        console.error("Error al cargar registros:", error);
        this.registros_vagones_cargados = [];
        this.registros_vagones_temporales = [];
        this.busqueda_existente = false;
        Swal.fire("Error", "No se pudieron cargar los vagones", "error");
      }
    }, */

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        if (!this.searchQuery.trim()) {
          this.vagones_productos = [...this.allRecords];
          this.busqueda_existente = true;
          return;
        }

        const query = this.searchQuery.toLowerCase();
        this.vagones_productos = this.allRecords.filter((item) => {
          const tipoEquipo = item.tipo_equipo_ferroviario_name?.toLowerCase() || "";
          const tipoOrigen = item.origen?.toLowerCase() || "";
          const productos = item.productos_list?.toLowerCase() || "";
          
          return (
            tipoEquipo.includes(query) ||
            tipoOrigen.includes(query) ||
            productos.includes(query)
          );
        });

        this.busqueda_existente = this.vagones_productos.length > 0;
      }, 300);
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

    confirmDeleteVagonAsignado(item) {
      // Verificación adicional de seguridad
      if (!item) {
        console.error("Item a eliminar es null/undefined");
        Swal.fire("Error", "No se puede eliminar: elemento no válido", "error");
        return;
      }

      // Si es un vagon temporal (sin ID)
      if (item.id === null || item.id === undefined) {
        Swal.fire({
          title: "¿Estás seguro?",
          text: "¿Quieres eliminar este vagón de la lista temporal?",
          icon: "warning",
          showCancelButton: true,
          confirmButtonText: "Sí, eliminar",
          cancelButtonText: "Cancelar",
        }).then((result) => {
          if (result.isConfirmed) {
            this.deleteVagonTemporal(item);
          }
        });
      } else {
        // Si es un vagon persistente (con ID)
        Swal.fire({
          title: "¿Estás seguro?",
          text: "¡Esta acción eliminará el registro principal y todos los vagones asociados!",
          icon: "warning",
          showCancelButton: true,
          confirmButtonText: "Sí, eliminar todo",
          cancelButtonText: "Cancelar",
          reverseButtons: true,
        }).then((result) => {
          if (result.isConfirmed) {
            this.delete_vagon_asignado(item.id);
          }
        });
      }
    },
    deleteVagonTemporal(item) {
      try {
        // Validación exhaustiva del item
        if (!item || typeof item !== "object" || item === null) {
          throw new Error("El elemento a eliminar no es válido");
        }

        // Validación de propiedades requeridas
        if (
          !item.hasOwnProperty("no_id") ||
          !item.hasOwnProperty("fecha_despacho")
        ) {
          throw new Error("El elemento no tiene las propiedades requeridas");
        }

        // Encontrar el índice usando propiedades seguras
        const index = this.registros_vagones_temporales.findIndex(
          (vagon) =>
            vagon &&
            vagon.no_id === item.no_id &&
            vagon.fecha_despacho === item.fecha_despacho
        );

        if (index === -1) {
          Swal.fire(
            "Error",
            "No se encontró el vagón en la lista temporal",
            "error"
          );
          return;
        }

        // Eliminar el elemento
        this.registros_vagones_temporales.splice(index, 1);

        // Actualizar lista de visualización (creando nuevo array para reactividad)
        this.registros_vagones_cargados = [
          ...this.registros_vagones_temporales,
        ];

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
    async getNoLocomotoras() {
      try {
        // Hacemos la petición al nuevo endpoint que ya filtra las locomotoras
        const response = await axios.get("/api/tipo-e-f-no-locomotora/");

        // La respuesta ya contiene todos los datos filtrados (no es paginada)
        this.tipos_equipos_ferroviarios = response.data;
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
        let nextPage = "/api/entidades/"; // URL inicial

        while (nextPage) {
          const response = await axios.get(nextPage);
          allEntidades = [...allEntidades, ...response.data.results];

          // Actualizamos nextPage con la URL de la siguiente página (o null si no hay más)
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
        let nextPage = "/api/puertos/"; // URL inicial

        while (nextPage) {
          const response = await axios.get(nextPage);
          allPuertos = [...allPuertos, ...response.data.results];

          // Actualizamos nextPage con la URL de la siguiente página (o null si no hay más)
          nextPage = response.data.next;
        }

        this.puertos = allPuertos;
      } catch (error) {
        console.error("Error al obtener los puertos:", error);
        Swal.fire("Error", "Hubo un error al obtener los puertos.", "error");
      }
    },

    async getProductos() {
      try {
        let allProductos = [];
        let nextPage = "/ufc/producto-vagon/"; // URL inicial

        while (nextPage) {
          const response = await axios.get(nextPage);
          allProductos = [...allProductos, ...response.data.results];

          // Actualiza nextPage con la URL de la siguiente página (null si no hay más)
          nextPage = response.data.next;
        }

        this.productos = allProductos;
      } catch (error) {
        console.error("Error al obtener los productos:", error);
        Swal.fire("Error", "Hubo un error al obtener los productos.", "error");
      }
    },

    /* abrir y cerrar modal de agregar producto en estado de vagones cargados */
    abrirModalAgregarProducto() {
      this.mostrarModalProducto = true;
    },
    cerrarModalAddProductoCargado() {
      this.mostrarModalProducto = false;
      this.getProductos();
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

    openVagonesCargadosDetailsModal(vagon) {
      Swal.fire({
        title: "Detalles del Vagón",
        html: `
            <div style="text-align: left;">
                <p><strong>Nombre:</strong> ${vagon.cliente_name}</p>
                <p><strong>Puerto:</strong> ${vagon.destino}</p>
                
            </div>
        `,
        width: "600px",
        customClass: {
          popup: "custom-swal-popup",
          title: "custom-swal-title",
          htmlContainer: "custom-swal-html",
        },
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

.ufc-form-row {
  display: flex;
  gap: 15px;
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
