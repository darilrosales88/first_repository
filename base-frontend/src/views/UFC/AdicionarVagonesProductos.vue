<template>
  <Navbar-Component />
  <div class="container py-3" style="margin-left: 25em; width: 60%">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-clipboard-data me-2"></i>Nuevo registro de vagón con
          productos
        </h5>
      </div>
      <div class="card-body p-3">
        <form @submit.prevent="submitForm">
          <div class="row mb-3 g-2">
            <!-- Columna 1 -->
            <div class="col-md-6">
              <!-- Campo:Fecha de registro -->
              <div class="mb-3">
                <label
                  for="fecha_registro"
                  class="form-label small fw-semibold text-secondary"
                  >Fecha de registro</label
                >
                <input
                  type="text"
                  style="padding: 8px 12px"
                  class="form-control form-control-sm border-secondary"
                  :value="formattedFechaRegistro"
                  id="fecha_registro"
                  name="fecha_registro"
                  readonly
                />
              </div>
              <!-- Campo: tipo_origen -->
              <div class="mb-3">
                <label
                  for="tipo_origen"
                  class="form-label small fw-semibold text-secondary"
                  >Tipo de Origen</label
                >
                <select
                  class="form-select form-select-sm border-secondary"
                  style="padding: 8px 12px"
                  v-model="formData.tipo_origen"
                  id="tipo_origen"
                  name="tipo_origen"
                  required
                >
                  <option value="" disabled>Seleccione un tipo</option>
                  <option value="ac_ccd">Acceso Comercial</option>
                  <option value="puerto">Puerto</option>
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
                    formData.tipo_origen && formData.tipo_origen !== 'puerto'
                  "
                  style="padding: 8px 12px"
                  class="form-select form-select-sm border-secondary"
                  v-model="formData.origen"
                  id="origen"
                  name="origen"
                  required
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
                  style="padding: 8px 12px"
                  v-else-if="formData.tipo_origen === 'puerto'"
                  class="form-select form-select-sm border-secondary"
                  v-model="formData.origen"
                  id="origen"
                  name="origen"
                  required
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
                  style="padding: 8px 12px"
                  disabled
                >
                  <option value="">Seleccione primero el tipo de origen</option>
                </select>
              </div>

              <!-- Campo: tipo_producto -->
              <div class="mb-3">
                <label
                  for="tipo_producto"
                  
                  class="form-label small fw-semibold text-secondary"
                  >Tipo de Producto</label
                >
                <select
                  style="padding: 8px 12px"
                  class="form-select form-select-sm border-secondary"
                  v-model="formData.tipo_producto"
                  id="tipo_producto"
                  name="tipo_producto"
                >
                  <option value="producto">Producto</option>
                  <option value="contenedor">Contenedor</option>
                  <option value="combustible">Combustible</option>
                </select>
              </div>

              <!-- Campo: producto -->
              <div class="mb-3" v-if="mostrarCampoProducto">
                <label
                  for="producto"
                  class="form-label small fw-semibold text-secondary"
                >
                  Productos
                  <button
                    class="create-button ms-2"
                    @click="abrirModalAgregarProducto"
                  >
                    <i class="bi bi-plus-circle large-icon"></i>
                  </button>
                </label>
                <select
                  class="form-select"
                  v-model="formData.producto"
                  id="producto"
                  name="producto"
                  multiple
                  size="4"
                >
                  <option
                    v-for="producto in productos"
                    :key="producto.id"
                    :value="producto.id"
                  >
                    {{ producto.id }}-{{ producto.producto_name }} -
                    {{ producto.producto_codigo }}-{{
                      producto.tipo_embalaje_name
                    }}
                  </option>
                </select>                
              </div>

              <!-- Campo: tipo_combustible -->
              <div class="mb-3" v-if="mostrarCampoCombustible">
                <label
                  for="tipo_combustible"
                  class="form-label small fw-semibold text-secondary"
                  >Tipo de Combustible</label
                >
                <select
                  style="padding: 8px 12px"
                  class="form-select form-select-sm border-secondary"
                  v-model="formData.tipo_combustible"
                  id="tipo_combustible"
                  name="tipo_combustible"
                >
                  <option value="combustible_blanco">Combustible blanco</option>
                  <option value="combustible_negro">Combustible negro</option>
                  <option value="combustible_turbo">Combustible turbo</option>
                </select>
              </div>

              <!-- Campo: TEF -->
              <div class="mb-3" v-if="mostrarCampoCombustible && tipo_combustible">
                <label
                  for="tipo_equipo_ferroviario"
                  class="form-label small fw-semibold text-secondary"
                  >Tipo de equipo ferroviario</label
                >
                <select
                  style="padding: 8px 12px"
                  class="form-select form-select-sm border-secondary"
                  v-model="formData.tipo_equipo_ferroviario"
                  id="tipo_equipo_ferroviario"
                  name="tipo_equipo_ferroviario"
                  required
                >
                  <option
                    v-for="tipo_equipo_ferroviario in tipos_equipos_ferroviarios"
                    :key="tipo_equipo_ferroviario.id"
                    :value="tipo_equipo_ferroviario.id"
                  >
                    {{ tipo_equipo_ferroviario.id }}-{{
                      tipo_equipo_ferroviario.tipo_equipo_name
                    }}-{{ tipo_equipo_ferroviario.descripcion }}
                  </option>
                </select>
              </div>
            </div>

            <!-- Columna 2 -->
            <div class="col-md-6">
              <!-- Campo: plan_mensual -->
              <div class="mb-3">
                <label
                  for="plan_mensual"
                  class="form-label small fw-semibold text-secondary"
                  >Plan mensual</label
                >
                <input
                  type="number"
                  style="padding: 8px 12px"
                  class="form-control form-control-sm border-secondary"
                  v-model="formData.plan_mensual"
                  id="plan_mensual"
                  name="plan_mensual"
                  required
                />
              </div>

              <!-- Campo: plan_anual -->
              <div class="mb-3">
                <label
                  for="plan_anual"
                  class="form-label small fw-semibold text-secondary" 
                  >Plan anual></label
                >
                <input
                  type="number"
                  disabled
                  style="padding: 8px 12px"
                  class="form-control form-control-sm border-secondary"
                  v-model="formData.plan_anual"
                  id="plan_anual"
                  name="plan_anual"
                  :readonly="!esPlanAnualEditable"
                  :required="esPlanAnualEditable"
                />
              </div>

              <!-- Campo: plan_dia -->
              <div class="mb-3">
                <label
                  for="plan_dia"
                  class="form-label small fw-semibold text-secondary"
                  >Plan del día</label
                >
                <input
                  type="number"
                  class="form-control form-control-sm border-secondary"
                  v-model="formData.plan_dia"
                  id="plan_dia"
                  name="plan_dia"
                  readonly
                />
              </div>

              <!-- Campo: plan_acumulado_dia_anterior -->
              <div class="mb-3" v-if="mostrarCamposAcumulados">
                <label
                  for="plan_acumulado_dia_anterior"
                  class="form-label small fw-semibold text-secondary" 
                  >Plan acumulado día anterior</label
                >
                <input
                  type="number"
                  disabled
                  style="padding: 8px 12px"
                  class="form-control form-control-sm border-secondary"
                  v-model="formData.plan_acumulado_dia_anterior"
                  id="plan_acumulado_dia_anterior"
                  name="plan_acumulado_dia_anterior"
                  readonly
                />
              </div>

              <!-- Campo: real_acumulado_dia_anterior -->
              <div class="mb-3" v-if="mostrarCamposAcumulados">
                <label
                  for="real_acumulado_dia_anterior"
                  class="form-label small fw-semibold text-secondary" 
                  >Real acumulado día anterior</label
                >
                <input
                  type="number"
                  disabled
                  style="padding: 8px 12px"
                  class="form-control form-control-sm border-secondary" 
                  v-model="formData.real_acumulado_dia_anterior"
                  id="real_acumulado_dia_anterior"
                  name="real_acumulado_dia_anterior"
                  readonly
                />
              </div>

              <!-- Campo: vagones_situados -->
              <div class="mb-3">
                <label
                  for="plan_dia"
                  class="form-label small fw-semibold text-secondary"
                  >Vagones situados</label
                >
                <input
                  type="number"
                  class="form-control form-control-sm border-secondary"
                  v-model="formData.vagones_situados"
                  id="vagones_situados"
                  name="vagones_situados"
                  readonly
                />
              </div>

              <!-- Campo: vagones_cargados -->
              <div class="mb-3">
                <label
                  for="plan_dia"
                  class="form-label small fw-semibold text-secondary"
                  >Vagones cargados</label
                >
                <input
                  type="number"
                  class="form-control form-control-sm border-secondary"
                  v-model="formData.vagones_cargados"
                  id="vagones_cargados"
                  name="vagones_cargados"
                  readonly
                />
              </div>
              <!-- Campo: plan_aseguramiento_proximos_dias -->
              <div class="mb-3">
                <label
                  for="plan_dia"
                  class="form-label small fw-semibold text-secondary"
                  >Plan de aseguramiento de los próximos días</label
                >
                <input
                  type="number"
                  class="form-control form-control-sm border-secondary"
                  v-model="formData.plan_aseguramiento_proximos_dias"
                  id="plan_aseguramiento_proximos_dias"
                  name="plan_aseguramiento_proximos_dias"
                  readonly
                />
              </div>

              
            </div>
            <!-- Campo: observaciones -->
            <div class="mb-3">
              <label for="observaciones" class="form-label small text-secondary"
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
          <div class="modal-footer">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <button class="ufc-button secondary" @click="volver_principal">
                <i class="bi bi-x-circle" me-1></i>Cancelar
              </button>
              <button type="submit" class="ufc-button primary">
                <i class="bi bi-check-circle" me-1></i>Agregar
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
  <br />
  <!-- Modal para agregar producto -->
  <ModalAgregarProductoVagonesProductos
    v-if="mostrarModalProducto"
    :visible="mostrarModalProducto"
    @cerrar-modal="cerrarModalAddProducto"
  />
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import NavbarComponent from "@/components/NavbarComponent.vue";
import ModalAgregarProductoVagonesProductos from "@/components/ModalAgregarProductoVagonesyProductos.vue";

export default {
  name: "AdicionarVagonProducto",
  components: {
    NavbarComponent,
    ModalAgregarProductoVagonesProductos,
  },

  data() {
    return {
      informeOperativoId: null,
      mostrarModalProducto: false,
      formData: {
        tipo_equipo_ferroviario: "",
        tipo_origen: "",
        origen: "",
        tipo_combustible: "",
        tipo_producto: "",
        plan_mensual: "",
        plan_anual: 0,
        plan_dia:0,
        vagones_situados:0,
        vagones_cargados:0,
        plan_aseguramiento_proximos_dias:0,
        plan_acumulado_dia_anterior: 0,
        real_acumulado_dia_anterior: 0,
        producto: [],
        observaciones: "",
      },
      // Nuevas propiedades de estado
      userGroups: [],
      userPermissions: [],
      productos: [],
      tipos_equipos_ferroviarios: [],
      puertos: [],
      entidades: [],
      esPrimerDiaMes: false,
      esUnicoInformeAnual: false,
      informeOperativoAnterior: null,
    };
  },
  computed: {
    formattedFechaRegistro() {
      if (this.formData.fecha) {
        return new Date(this.formData.fecha).toLocaleString();
      }
      return new Date().toLocaleString();
    },
    mostrarCampoProducto() {
      return this.formData.tipo_producto === "producto";
    },
    mostrarCampoCombustible() {
      return this.formData.tipo_producto === "combustible";
    },
    mostrarCamposAcumulados() {
      // Casos 4 y 6: Mostrar campos acumulados cuando no es primer día del mes
      return !this.esPrimerDiaMes;
    },
    esPlanAnualEditable() {
      // Casos 3 y 4: Editable cuando es único informe en el año
      // Cuando no es editable, forzar el valor a 0
      if (!this.esUnicoInformeAnual) {
        this.formData.plan_anual = 0;
      }
      return this.esUnicoInformeAnual;
    },
  },

  async mounted() {
    await this.getProductos();
    this.getNoLocomotoras();
    this.getEntidades();
    this.getPuertos();
    this.verificarInformeOperativo();
  },
  async created() {
    await this.fetchUserPermissionsAndGroups();
  },
  watch: {
    "formData.tipo_combustible": {
      handler(newVal) {
        if (newVal) {
          this.getNoLocomotoras();
        }
      },
      immediate: true,
    },
  },
  methods: {
    // Métodos de autenticación y permisos
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

    // Métodos para manejar modales
    abrirModalAgregarProducto() {
      this.mostrarModalProducto = true;
    },
    cerrarModalAddProducto() {
      this.mostrarModalProducto = false;
      this.getProductos();
    },

    // Envío del formulario
    async submitForm() {
      try {
        // Verificar informe operativo
        const today = new Date();
        const fechaFormateada = `${today.getFullYear()}-${String(
          today.getMonth() + 1
        ).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;

        const informeResponse = await axios.get(
          "/ufc/verificar-informe-existente/",
          {
            params: { fecha_operacion: fechaFormateada },
          }
        );

        if (!informeResponse.data.existe) {
          Swal.fire(
            "Error",
            "No existe un informe operativo creado para la fecha actual. Debe crear uno primero.",
            "error"
          );
          this.$router.push({ name: "InfoOperativo" });
          return;
        }

        if (informeResponse.data.estado_parte === "Aprobado") {
          Swal.fire(
            "Error",
            "No se puede agregar registros a un informe operativo que ya ha sido aprobado.",
            "error"
          );
          return;
        }

        // Preparar datos para enviar
        const datosEnvio = {
          ...this.formData,
          informe_operativo: informeResponse.data.id,
          // Si necesitas enviar solo un producto, toma el primero
          producto: this.formData.producto.length > 0 ? this.formData.producto[0] : null,
          // Convertir valores a números
          plan_mensual: parseInt(this.formData.plan_mensual) || 0,
          plan_anual: parseInt(this.formData.plan_anual) || 0,
          plan_dia: this.formData.plan_dia,
          vagones_situados: this.formData.vagones_situados,
          vagones_cargados: this.formData.vagones_cargados,
          plan_aseguramiento_proximos_dias: this.formData.plan_aseguramiento_proximos_dias,

        };

        const response = await axios.post(
          "/ufc/vagones-productos/",
          datosEnvio
        );
        
        Swal.fire("Éxito", "Registro agregado correctamente", "success");
        this.$router.push({ name: "InfoOperativo" });
      } catch (error) {
        console.error("Error al guardar:", error);
        let errorMsg = "No se pudo guardar el registro";
        
        if (error.response?.data) {
          // Mejorar el manejo de errores del backend
          if (typeof error.response.data === 'object') {
            errorMsg += `: ${JSON.stringify(error.response.data)}`;
          } else {
            errorMsg += `: ${error.response.data}`;
          }
        } else if (error.message) {
          errorMsg += `: ${error.message}`;
        }
        
        Swal.fire("Error", errorMsg, "error");
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
          await this.DameCamposAutomaticos(response.data.id);
          return true;
        }
        return false;
      } catch (error) {
        console.error("Error al verificar informe:", error);
        return false;
      }
    },
    async DameCamposAutomaticos(informeId) {
      try {
        const response = await axios.get("/ufc/vagones-productos/calcular-campos-automaticos/", {
          params: { informe_id: informeId }
        });
        this.formData.plan_dia = response.data.plan_dia || 0;
        this.formData.plan_anual = response.data.plan_anual || 0;
        this.formData.vagones_situados = response.data.vagones_situados || 0;
        this.formData.vagones_cargados = response.data.vagones_cargados || 0;
        this.formData.plan_aseguramiento_proximos_dias = response.data.plan_aseguramiento_proximos_dias || 0;    
        this.formData.plan_acumulado_dia_anterior = response.data.plan_acumulado_dia_anterior || 0; 
        this.formData.real_acumulado_dia_anterior = response.data.real_acumulado_dia_anterior || 0;     
      } catch (error) {
        console.error("Error al obtener el plan del día:", error);
        this.formData.plan_dia = 0;
      }
    },

    // Métodos auxiliares
    resetForm() {
      this.formData = {
        tipo_equipo_ferroviario: "",
        tipo_origen: "ac_ccd",
        origen: "",
        tipo_combustible: "",
        tipo_producto: "",
        plan_mensual: "",
        plan_anual: "",
        plan_acumulado_dia_anterior: 0,
        real_acumulado_dia_anterior: 0,
        producto: [],
        plan_dia:0,
        vagones_situados:0,
        vagones_cargados:0,
        plan_aseguramiento_proximos_dias:0,
        observaciones: "",
      };
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

    // Métodos para obtener datos
    async getNoLocomotoras() {
      try {
        let url = "/api/tipo-e-f-no-locomotora/";

        // Si hay un tipo de combustible seleccionado, añadirlo como parámetro
        if (this.formData.tipo_combustible) {
          url += `?tipo_combustible=${this.formData.tipo_combustible}`;
        }

        const response = await axios.get(url);
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

    async getProductos() {
      try {
        const response = await axios.get("/ufc/producto-vagon/");
        this.productos = response.data.results.map((p) => ({
          ...p,
          id: parseInt(p.id), // Asegurar que los IDs son números
        }));
      } catch (error) {
        console.error("Error al obtener productos:", error);
        Swal.fire(
          "Error",
          "No se pudieron cargar los productos disponibles",
          "error"
        );
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
/* Estilos para el grid dentro del modal */

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
  background: #f1513f;
  color: white;
}

.ufc-button.secondary:hover {
  background: rgb(228, 56, 37);
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

.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
}

.btn-outline-danger:hover {
  color: #fff;
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

