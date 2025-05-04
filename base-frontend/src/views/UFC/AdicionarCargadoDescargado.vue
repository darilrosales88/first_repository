<template>
  <div style="background-color: #002a68; color: white; text-align: right">
    <h6>Bienvenido:</h6>
  </div>
  <Navbar-Component />
  <div class="container mt-2 px-6" style="padding-left: 10%">
    <div class="row mb-4">
      <h2 class="mb-4">Nuevo registro de vagón cargado/descargado</h2>
      <form @submit.prevent="submitForm">
        <div class="row">
          <!-- Columna 1 -->
          <div class="col-md-6">
            <!-- Campo: TEF -->
            <div class="mb-3">
              <label for="tipo_equipo_ferroviario" class="form-label"
                >Tipo de equipo ferroviario
                <span style="color: red">*</span></label
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
                  }}
                  -
                  {{ tipo_equipo_ferroviario.descripcion }}
                </option>
              </select>
            </div>

            <!-- Campo: tipo_origen -->
            <div class="mb-3">
              <label for="tipo_origen" class="form-label"
                >Tipo de Origen <span style="color: red">*</span></label
              >
              <select
                class="form-select"
                v-model="formData.tipo_origen"
                id="tipo_origen"
                name="tipo_origen"
              >
                <option value="ac_ccd">Acceso Comercial</option>
                <option value="puerto">Puerto</option>
              </select>
            </div>

            <!-- Campo: origen -->
            <div class="mb-3">
              <label for="origen" class="form-label"
                >Origen <span style="color: red">*</span></label
              >
              <select
                v-if="formData.tipo_origen !== 'puerto'"
                class="form-select"
                v-model="formData.origen"
                id="origen"
                name="origen"
              >
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
                class="form-select"
                v-model="formData.origen"
                id="origen"
                name="origen"
              >
                <option
                  v-for="puerto in puertos"
                  :key="puerto.id"
                  :value="puerto.nombre_puerto"
                >
                  {{ puerto.id }}- {{ puerto.nombre_puerto }}
                </option>
              </select>
            </div>

            <!-- Campo: tipo_destino -->
            <div class="mb-3">
              <label for="tipo_destino" class="form-label"
                >Tipo de Destino <span style="color: red">*</span></label
              >
              <select
                class="form-select"
                v-model="formData.tipo_destino"
                id="tipo_destino"
                name="tipo_destino"
                required
              >
                <option value="ac_ccd">Acceso Comercial</option>
                <option value="puerto">Puerto</option>
              </select>
            </div>

            <!-- Campo: destino -->
            <div class="mb-3">
              <label for="destino" class="form-label"
                >Destino <span style="color: red">*</span></label
              >
              <select
                v-if="formData.tipo_destino !== 'puerto'"
                class="form-select"
                v-model="formData.destino"
                id="tipo_destino"
                name="tipo_destino"
              >
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
                class="form-select"
                v-model="formData.destino"
                id="destino"
                name="destino"
              >
                <option
                  v-for="puerto in puertos"
                  :key="puerto.id"
                  :value="puerto.nombre_puerto"
                >
                  {{ puerto.id }}- {{ puerto.nombre_puerto }}
                </option>
              </select>
            </div>

            <!-- Campo: estado -->
            <div class="mb-3">
              <label for="estado" class="form-label"
                >Estado <span style="color: red">*</span></label
              >
              <select
                class="form-select"
                v-model="formData.estado"
                id="estado"
                name="estado"
                required
              >
                <option value="cargado">Cargado</option>
                <option value="vacio">Vacio</option>
              </select>
            </div>
          </div>

          <!-- Columna 2 -->
          <div class="col-md-6">
            <!-- Campo: operacion -->
            <div class="mb-3">
              <label for="operacion" class="form-label"
                >Operación <span style="color: red">*</span></label
              >
              <input
                type="text"
                class="form-control"
                v-model="formData.operacion"
                id="operacion"
                name="operacion"
                readonly
              />
            </div>
            <!-- Campo: plan_diario_carga -->
            <div class="mb-3">
              <label for="plan_diario_carga" class="form-label"
                >Plan diario de carga/descarga
                <span style="color: red">*</span></label
              >
              <input
                type="number"
                class="form-control"
                v-model="formData.plan_diario_carga_descarga"
                id="plan_diario_carga_descarga"
                name="plan_diario_carga_descarga"
              />
            </div>

            <!-- Campo: plan_diario_carga -->
            <div class="mb-3">
              <label for="real_carga_descarga" class="form-label"
                >Real de carga/descarga <span style="color: red">*</span></label
              >
              <input
                type="number"
                class="form-control"
                v-model="formData.real_carga_descarga"
                id="real_carga_descarga"
                name="real_carga_descarga"
                readonly
              />
            </div>
            <!-- Campo: producto -->
            <div class="mb-3">
              <label for="producto" class="form-label">
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
                v-model="formData.lista_productos"
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
              <small class="text-muted"
                >Mantén presionado Ctrl o Shift para seleccionar múltiples
                productos</small
              >
            </div>

            <!-- Modal para agregar producto cargado/descargado -->
            <ModalAgregarProducto
              v-if="mostrarModalProducto"
              :visible="mostrarModalProducto"
              @cerrar-modal="cerrarModalAddProductoCargado"
            />

            <!-- Modal para agregar vagon a estado cargado/descargado -->
            <ModalAgregarVagonCargado
              v-if="mostrarModalVagon"
              :visible="mostrarModalVagon"
              @cerrar-modal="cerrarModalAddVagonCargado"
              @vagon-agregado="handleVagonAgregado"
            />

            <!-- Campo: causas_incumplimiento -->
            <div class="mb-3">
              <label for="causas_incumplimiento" class="form-label"
                >Causas del incumplimiento
              </label>
              <textarea
                class="form-control"
                v-model="formData.causas_incumplimiento"
                id="causas_incumplimiento"
                name="causas_incumplimiento"
                rows="3"
                required
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Botón de envío -->
        <div class="text-center">
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="registros_vagones_temporales.length === 0"
          >
            Guardar
          </button>
          <button @click="volver_principal" class="btn btn-secondary">
            Volver
          </button>
        </div>
      </form>
    </div>
    <br />
    <!-- Segunda fila: Lista de vagones -->
    <div class="row">
      <div class="col-md-12">
        <h4 v-if="registros_vagones_temporales.length > 0">
          Cargados/descargados
        </h4>
        <h4 v-else style="color: red">* Debe agregar al menos un vagón</h4>
        <button class="create-button ms-2" @click="abrirModalAgregarVagon">
          <i class="bi bi-plus-circle large-icon"></i>
        </button>
        <table class="table table-hover mb-0">
          <thead>
            <tr>
              <th>No ID</th>
              <th>Fecha de despacho</th>
              <th>Origen</th>
              <th>Fecha de llegada</th>
              <th>Observaciones</th>
              <th v-if="hasGroup('AdminUFC')">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-if="hasGroup('AdminUFC')"
              v-for="(item, index) in registros_vagones_cargados"
              :key="index"
            >
              <!-- usar id como llave -->
              <td>{{ item.no_id || "Sin ID" }}</td>
              <!-- Manejo de null -->
              <td>{{ item.fecha_despacho }}</td>
              <td>{{ item.origen }}</td>
              <td>{{ item.fecha_llegada }}</td>
              <td>{{ item.observaciones }}</td>
              <td>
                <span v-if="hasGroup('AdminUFC')">
                  <button
                    @click.prevent="confirmDeleteVagonAsignado(item)"
                    class="btn btn-danger btn-small"
                    :disabled="!item"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
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
        tipo_equipo_ferroviario: "",
        tipo_origen: "ac_ccd",
        origen: "",
        tipo_destino: "ac_ccd",
        destino: "",
        estado: "cargado",
        lista_productos: [],
        plan_diario_carga_descarga: "",
        real_carga_descarga: "",
        operacion: "",
        causas_incumplimiento: "", // Asegúrate de incluir este campo
      },
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
      fechaActual: new Date().toISOString().split('T')[0] // Fecha actual en formato YYYY-MM-DD
    };
  },

  mounted() {
    // Llama al método para obtener los puertos
    this.getProductos();
    this.getNoLocomotoras();
    this.getEntidades();
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

    "formData.lista_productos": {
      handler() {
        this.calcularRealCargaDescarga();
      },
      deep: true,
    },
  },
  async created() {
    await this.fetchUserPermissionsAndGroups(); // Espera a que se carguen los permisos
    //await this.GetRegistroVagonesCargadosDescargados(); // Luego carga los registros
  },

  methods: {
    async verificarInformeOperativo() {
      try {
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
    // 0. First check if there are any wagons added
    if (this.registros_vagones_temporales.length === 0) {
      Swal.fire("Error", "Debe agregar al menos un vagón", "error");
      return;
    }

    // 1. Verify if operational report exists for current date
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

    // 2. Basic validations
    if (!this.formData.tipo_equipo_ferroviario || 
        !this.formData.tipo_origen ||
        !this.formData.origen || 
        !this.formData.tipo_destino ||
        !this.formData.destino) {
      Swal.fire("Error", "Por favor complete todos los campos obligatorios", "error");
      return;
    }

    // 3. Product validation for loaded wagons
    if (this.formData.estado === "cargado" && 
        (!this.formData.lista_productos || this.formData.lista_productos.length === 0)) {
      Swal.fire("Error", "Debe seleccionar al menos un producto.", "error");
      return;
    }

    // 4. Calculate real value
    await this.calcularRealCargaDescarga();

    // 5. Prepare data
    const datosEnvio = {
      ...this.formData,
      informe_operativo: this.informeOperativoId,
      real_carga_descarga: this.formData.real_carga_descarga || 0,
      causas_incumplimiento: this.formData.causas_incumplimiento || '',
      producto_ids: Array.isArray(this.formData.lista_productos) 
        ? this.formData.lista_productos 
        : [this.formData.lista_productos],
      registros_vagones_data: this.registros_vagones_temporales.map(v => ({
        no_id: v.no_id,
        fecha_despacho: v.fecha_despacho,
        tipo_origen: v.tipo_origen,
        origen: v.origen,
        fecha_llegada: v.fecha_llegada,
        observaciones: v.observaciones
      }))
    };

    // 6. Send data
    const response = await axios.post("/ufc/vagones-cargados-descargados/", datosEnvio);

    // 7. Reset and show success
    this.registros_vagones_temporales = [];
    this.formData.lista_productos = [];
    this.resetForm();

    await Swal.fire({
      title: "Éxito",
      text: "Registro creado correctamente",
      icon: "success",
      confirmButtonText: "Aceptar"
    });

    this.$router.push({ name: "InfoOperativo" });

  } catch (error) {
    console.error("Error al guardar:", error.response);
    let errorMsg = "No se pudo guardar el registro";
    if (error.response?.data) {
      errorMsg += `: ${JSON.stringify(error.response.data)}`;
    }
    Swal.fire("Error", errorMsg, "error");
  }
},

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

    resetForm() {
      this.formData = {
        tipo_equipo_ferroviario: "",
        tipo_origen: "ac_ccd",
        origen: "",
        tipo_destino: "ac_ccd",
        destino: "",
        estado: "cargado",
        lista_productos: [],
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
      } catch (error) {
        console.error("Error al obtener permisos y grupos:", error);
      }
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
    const response = await axios.get("/ufc/registro-vagones-cargados/");
    
    // Actualizar ambas listas
    this.registros_vagones_cargados = response.data.results || [];
    this.registros_vagones_temporales = [...this.registros_vagones_cargados];
    
  } catch (error) {
    console.error("Error al cargar registros:", error);
    this.registros_vagones_cargados = [];
    this.registros_vagones_temporales = [];
    Swal.fire("Error", "No se pudieron cargar los vagones", "error");
  }
}, */

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
    volver_principal() {
      this.$router.push({ name: "InfoOperativo" });
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
  },
};
</script>
