<template>
  <div style="background-color: #002a68; color: white; text-align: right">
    <h6>Bienvenido:</h6>
  </div>
  <Navbar-Component />

  <div class="container mt-2 px-6" style="padding-left: 10%">
    <div class="row mb-4">
      <h2 class="mb-4">Editar registro de vagón cargado/descargado</h2>

      <div v-if="loading" class="text-center">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Cargando...</span>
        </div>
      </div>

      <form @submit.prevent="submitForm" v-else>
        <div class="row">
          <!-- Columna 1 -->
          <div class="col-md-6">
            <!-- Campo: TEF -->
            <div class="mb-3">
              <label for="tipo_equipo_ferroviario" class="form-label">
                Tipo de equipo ferroviario <span style="color: red">*</span>
              </label>
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
              <label for="tipo_origen" class="form-label">
                Tipo de Origen <span style="color: red">*</span>
              </label>
              <select
                class="form-select"
                v-model="formData.tipo_origen"
                id="tipo_origen"
                name="tipo_origen"
                required
              >
                <option value="ac_ccd">Acceso Comercial</option>
                <option value="puerto">Puerto</option>
              </select>
            </div>

            <!-- Campo: origen -->
            <div class="mb-3">
              <label for="origen" class="form-label">
                Origen <span style="color: red">*</span>
              </label>
              <select
                v-if="formData.tipo_origen !== 'puerto'"
                class="form-select"
                v-model="formData.origen"
                id="origen"
                name="origen"
                required
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
                required
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
              <label for="tipo_destino" class="form-label">
                Tipo de Destino <span style="color: red">*</span>
              </label>
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
              <label for="destino" class="form-label">
                Destino <span style="color: red">*</span>
              </label>
              <select
                v-if="formData.tipo_destino !== 'puerto'"
                class="form-select"
                v-model="formData.destino"
                id="tipo_destino"
                name="tipo_destino"
                required
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
                required
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
              <label for="estado" class="form-label">
                Estado <span style="color: red">*</span>
              </label>
              <select
                class="form-select"
                v-model="formData.estado"
                id="estado"
                name="estado"
                required
              >
                <option value="cargado">Cargado</option>
                <option value="vacio">Vacío</option>
              </select>
            </div>
          </div>

          <!-- Columna 2 -->
          <div class="col-md-6">
            <!-- Campo: operacion -->
            <div class="mb-3">
              <label for="operacion" class="form-label">
                Operación <span style="color: red">*</span>
              </label>
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
              <label for="plan_diario_carga" class="form-label">
                Plan diario de carga/descarga <span style="color: red">*</span>
              </label>
              <input
                type="number"
                class="form-control"
                v-model="formData.plan_diario_carga_descarga"
                id="plan_diario_carga_descarga"
                name="plan_diario_carga_descarga"
                required
              />
            </div>

            <!-- Campo: real_carga_descarga -->
            <div class="mb-3">
              <label for="real_carga_descarga" class="form-label">
                Real de carga/descarga <span style="color: red">*</span>
              </label>
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
                  type="button"
                  class="btn btn-sm btn-success ms-2"
                  @click="abrirModalAgregarProducto"
                >
                  <i class="bi bi-plus-circle"></i> Agregar
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

              <!-- Mostrar productos actuales -->
              <div v-if="formData.original_productos.length > 0" class="mt-3">
                <h6>Productos actualmente asociados:</h6>
                <ul>
                  <li
                    v-for="(prod, index) in formData.original_productos"
                    :key="index"
                  >
                    {{ prod.id }} -
                    {{
                      prod.producto_name ||
                      prod.nombre_producto ||
                      "Producto sin nombre"
                    }}
                  </li>
                </ul>
              </div>
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
              <label for="causas_incumplimiento" class="form-label">
                Causas del incumplimiento
              </label>
              <textarea
                class="form-control"
                v-model="formData.causas_incumplimiento"
                id="causas_incumplimiento"
                name="causas_incumplimiento"
                rows="3"
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Botón de envío -->
        <div class="text-center">
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="loading || registros_vagones_cargados.length === 0"
          >
            <span
              v-if="loading"
              class="spinner-border spinner-border-sm"
              role="status"
              aria-hidden="true"
            ></span>
            Guardar cambios
          </button>
          <button type="button" @click="goBack" class="btn btn-secondary">
            Volver
          </button>
        </div>
      </form>
    </div>
    <br />

    <!-- Segunda fila: Lista de vagones -->
    <div class="row">
      <div class="col-md-12">
        <h4 v-if="registros_vagones_cargados.length > 0">
          Cargados/descargados
        </h4>
        <h4 v-else style="color: red">* Debe agregar al menos un vagón</h4>
        <button
          type="button"
          class="btn btn-sm btn-success ms-2"
          @click="abrirModalAgregarVagon"
        >
          <i class="bi bi-plus-circle"></i> Agregar vagón
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
              v-for="(item, index) in registros_vagones_cargados"
              :key="index"
            >
              <td>{{ item.no_id || "Sin ID" }}</td>
              <td>{{ item.fecha_despacho || "No especificada" }}</td>
              <td>{{ item.origen || "No especificado" }}</td>
              <td>{{ item.fecha_llegada || "No especificada" }}</td>
              <td>{{ item.observaciones || "Sin observaciones" }}</td>
              <td v-if="hasGroup('AdminUFC')">
                <button
                  @click.prevent="confirmDeleteVagonAsignado(item)"
                  class="btn btn-danger btn-sm"
                  :disabled="!item"
                >
                  <i class="bi bi-trash"></i> Eliminar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
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
/* Estilos del componente AdicionarCargadoDescargado */
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
