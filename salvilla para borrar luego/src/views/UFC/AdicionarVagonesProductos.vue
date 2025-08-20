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
                    {{ entidad.id }}-{{ entidad.nombre }}
                  </option>
                </select>

                <select
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
                    {{ puerto.id }}- {{ puerto.nombre_puerto }}
                  </option>
                </select>

                <select
                  v-else
                  class="form-select form-select-sm border-secondary"
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
                  class="form-select"
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
              <div class="mb-3" v-if="mostrarCampoCombustible">
                <label
                  for="tipo_equipo_ferroviario"
                  class="form-label small fw-semibold text-secondary"
                  >Tipo de equipo ferroviario</label
                >
                <select
                  class="form-select"
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
                  >Plan anual
                  <span style="color: red" v-if="esPlanAnualEditable"
                    >*</span
                  ></label
                >
                <input
                  type="number"
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

.create-button {
  text-decoration: none;
  color: green;
  margin-left: 940px;
}

.form-container {
  max-width: 300px;
  margin: 50px;
  padding: 20px;
  background-color: f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  font-family: "Franklin Gothic Medium", "Arial Narrow", Arial, sans-serif;
  text-align: left;
  margin-bottom: 20px;
  font-size: 20px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  text-align: left;
  display: flex;
  width: 260px;
  flex-direction: column;
  gap: 5px;
  font-size: 14px;
}

label {
  font-weight: bold;
}

input,
select {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.form-buttons {
  display: flex;
  justify-content: end;
  font-size: 15px;
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
</style>
