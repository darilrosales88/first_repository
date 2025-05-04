<template>    
  <Navbar-Component />

  <div class="container mt-2 px-6" style="padding-left: 10%">
    <div class="row mb-4">
      <h2 class="mb-4">Editar registro de vagón con productos</h2>
      <form @submit.prevent="submitForm">
        <div class="row">
          <!-- Columna 1 -->
          <div class="col-md-6">
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
                required
                :class="{ 'is-invalid': errors.tipo_origen }"
              >
                <option value="ac_ccd">Acceso Comercial</option>
                <option value="puerto">Puerto</option>
              </select>
              <div class="invalid-feedback" v-if="errors.tipo_origen">
                {{ errors.tipo_origen }}
              </div>
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
                required
                :class="{ 'is-invalid': errors.origen }"
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
                :class="{ 'is-invalid': errors.origen }"
              >
                <option
                  v-for="puerto in puertos"
                  :key="puerto.id"
                  :value="puerto.nombre_puerto"
                >
                  {{ puerto.id }}- {{ puerto.nombre_puerto }}
                </option>
              </select>
              <div class="invalid-feedback" v-if="errors.origen">
                {{ errors.origen }}
              </div>
            </div>

            <!-- Campo: tipo_producto -->
            <div class="mb-3">
              <label for="tipo_producto" class="form-label"
                >Tipo de Producto</label
              >
              <select
                class="form-select"
                v-model="formData.tipo_producto"
                id="tipo_producto"
                name="tipo_producto"
                :class="{ 'is-invalid': errors.tipo_producto }"
              >
                <option value="producto">Producto</option>
                <option value="contenedor">Contenedor</option>
                <option value="combustible">Combustible</option>
              </select>
              <div class="invalid-feedback" v-if="errors.tipo_producto">
                {{ errors.tipo_producto }}
              </div>
            </div>

            <!-- Campo: tipo_combustible -->
            <div class="mb-3" v-if="mostrarCampoCombustible">
              <label for="tipo_combustible" class="form-label"
                >Tipo de Combustible</label
              >
              <select
                class="form-select"
                v-model="formData.tipo_combustible"
                id="tipo_combustible"
                name="tipo_combustible"
                :class="{ 'is-invalid': errors.tipo_combustible }"
              >
                <option value="combustible_blanco">Combustible blanco</option>
                <option value="combustible_negro">Combustible negro</option>
                <option value="combustible_turbo">Combustible turbo</option>
              </select>
              <div class="invalid-feedback" v-if="errors.tipo_combustible">
                {{ errors.tipo_combustible }}
              </div>
            </div>

            <!-- Campo: TEF -->
            <div class="mb-3" v-if="mostrarCampoCombustible">
              <label for="tipo_equipo_ferroviario" class="form-label"
                >Tipo de equipo ferroviario <span style="color: red">*</span></label
              >
              <select
                class="form-select"
                v-model="formData.tipo_equipo_ferroviario"
                id="tipo_equipo_ferroviario"
                name="tipo_equipo_ferroviario"
                required
                :class="{ 'is-invalid': errors.tipo_equipo_ferroviario }"
              >
                <option
                  v-for="tipo_equipo_ferroviario in tipos_equipos_ferroviarios"
                  :key="tipo_equipo_ferroviario.id"
                  :value="tipo_equipo_ferroviario.id"
                >
                  {{ tipo_equipo_ferroviario.id }}-{{
                  tipo_equipo_ferroviario.tipo_equipo_name }} -
                  {{ tipo_equipo_ferroviario.descripcion }}
                </option>
              </select>
              <small v-if="!formData.tipo_equipo_ferroviario && formData.original_equipo" class="text-muted">
                Valor actual: {{ formData.original_equipo }}
              </small>
              <div class="invalid-feedback" v-if="errors.tipo_equipo_ferroviario">
                {{ errors.tipo_equipo_ferroviario }}
              </div>
            </div>  
          </div>

          <!-- Columna 2 -->
          <div class="col-md-6">
            <!-- Campo: plan_mensual -->
            <div class="mb-3">
              <label for="plan_mensual" class="form-label"
                >Plan mensual <span style="color: red">*</span></label
              >
              <input
                type="number"
                class="form-control"
                v-model="formData.plan_mensual"
                id="plan_mensual"
                name="plan_mensual"
                required
                :class="{ 'is-invalid': errors.plan_mensual }"
              />
              <div class="invalid-feedback" v-if="errors.plan_mensual">
                {{ errors.plan_mensual }}
              </div>
            </div>

            <!-- Campo: plan_anual -->
            <div class="mb-3">
              <label for="plan_anual" class="form-label"
                >Plan anual <span style="color: red">*</span></label
              >
              <input
                type="number"
                class="form-control"
                v-model="formData.plan_anual"
                id="plan_anual"
                name="plan_anual"
                required
                :class="{ 'is-invalid': errors.plan_anual }"
              />
              <div class="invalid-feedback" v-if="errors.plan_anual">
                {{ errors.plan_anual }}
              </div>
            </div>

            <!-- Campo: plan_acumulado_dia_anterior -->
            <div class="mb-3">
              <label for="plan_acumulado_dia_anterior" class="form-label"
                >Plan acumulado día anterior</label
              >
              <input
                type="number"
                class="form-control"
                v-model="formData.plan_acumulado_dia_anterior"
                id="plan_acumulado_dia_anterior"
                name="plan_acumulado_dia_anterior"
                readonly
              />
            </div>

            <!-- Campo: real_acumulado_dia_anterior -->
            <div class="mb-3">
              <label for="real_acumulado_dia_anterior" class="form-label"
                >Real acumulado día anterior</label
              >
              <input
                type="number"
                class="form-control"
                v-model="formData.real_acumulado_dia_anterior"
                id="real_acumulado_dia_anterior"
                name="real_acumulado_dia_anterior"
                readonly
              />
            </div>

            <!-- Campo: producto -->
            <div class="mb-3" v-if="mostrarCampoProducto">
              <label for="producto" class="form-label">
                Productos
                <button class="create-button ms-2" @click="abrirModalAgregarProducto">
                  <i class="bi bi-plus-circle large-icon"></i>
                </button>
              </label>
              <div v-if="productos.length === 0" class="alert alert-warning">
                No se pudieron cargar los productos disponibles
              </div>
              <select
                v-else
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
                  {{ producto.producto_codigo }}-{{ producto.tipo_embalaje_name }}
                </option>
              </select>
              <small class="text-muted">Mantén presionado Ctrl o Shift para seleccionar múltiples productos</small>
              
              <!-- Mostrar productos actuales si hay discrepancia -->
              <div v-if="formData.original_productos.length > 0" class="mt-3">
                <h6>Productos actualmente asociados:</h6>
                <ul>
                  <li v-for="(prod, index) in formData.original_productos" :key="index">
                    {{ prod.id }} - {{ prod.producto_name || prod.nombre_producto || 'Producto sin nombre' }}
                  </li>
                </ul>
              </div>
            </div>

            <!-- Campo: observaciones -->
            <div class="mb-3">
              <label for="observaciones" class="form-label"
                >Observaciones</label
              >
              <textarea
                class="form-control"
                v-model="formData.observaciones"
                id="observaciones"
                name="observaciones"
                rows="3"
                :class="{ 'is-invalid': errors.observaciones }"
              ></textarea>
              <div class="invalid-feedback" v-if="errors.observaciones">
                {{ errors.observaciones }}
              </div>
            </div>
          </div>
        </div>

        <!-- Botón de envío -->
        <div class="text-center">
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="loading"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Guardar cambios
          </button>
          <button @click="volver_principal" class="btn btn-secondary">Volver</button>
        </div>
      </form>
    </div>
    <br>
  </div>

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
name: "EditarVagonProducto",
components: {
  NavbarComponent,
  ModalAgregarProductoVagonesProductos,
},

data() {
  return {
    mostrarModalProducto: false,
    loading: false,
    formData: {
      tipo_equipo_ferroviario: "",
      tipo_origen: "ac_ccd",
      origen: "",
      tipo_combustible: "",
      tipo_producto: "",
      plan_mensual: "",
      plan_anual: "",
      plan_acumulado_dia_anterior: 0,
      real_acumulado_dia_anterior: 0,
      lista_productos: [], // Array de strings
      original_productos: [], // Array de objetos completos
      observaciones: "",
      original_equipo: null, // Para mostrar el valor actual de tef aunque no esté en opciones
    },
    errors: {},
    userGroups: [],
    userPermissions: [],
    productos: [],
    tipos_equipos_ferroviarios: [],
    puertos: [],
    entidades: [],
  };
},

computed: {
  mostrarCampoProducto() {
    return this.formData.tipo_producto === 'producto';    
  },
  mostrarCampoCombustible() {
    return this.formData.tipo_producto === 'combustible';    
  }
},

watch: {
  'formData.tipo_combustible': {
    handler(newVal) {
      if (newVal) {
        this.getNoLocomotoras();
      }
    },
    immediate: true
  }
},

async mounted() {
  await this.fetchUserPermissionsAndGroups();
  await this.getProductos();
  await this.getNoLocomotoras();
  await this.getEntidades();
  await this.getPuertos();
  await this.loadVagonData();
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

  // Cargar datos del vagon a editar
  async loadVagonData() {
    this.loading = true;
    try {
        const vagonId = this.$route.params.id;
        if (!vagonId) {
            throw new Error('No se proporcionó ID de vagón');
        }

        // 1. Obtener datos del vagón
        const response = await axios.get(`/ufc/vagones-productos/${vagonId}/`);
        console.log('RESPUESTA COMPLETA:', response.data);

        // 2. Procesar equipo ferroviario
        let equipoFerroviarioId = '';
        if (response.data.tipo_equipo_ferroviario) {
            if (typeof response.data.tipo_equipo_ferroviario === 'object') {
                equipoFerroviarioId = response.data.tipo_equipo_ferroviario.id?.toString() || '';
            } else {
                equipoFerroviarioId = response.data.tipo_equipo_ferroviario.toString();
            }
        }

        // 3. MANEJO ESPECÍFICO PARA PRODUCTOS - VERSIÓN DEFINITIVA
        let productosAsociados = [];
        let productosOriginales = [];
        
        // Caso 1: producto es un array de IDs
        if (Array.isArray(response.data.producto)) {
            productosAsociados = response.data.producto
                .filter(id => id != null && !isNaN(id))
                .map(id => id.toString());
            
            productosOriginales = this.productos.filter(p =>
                productosAsociados.includes(p.id.toString())
            );
        }
        // Caso 2: producto es un array de objetos
        else if (Array.isArray(response.data.producto) && response.data.producto.length > 0 && typeof response.data.producto[0] === 'object') {
            productosOriginales = response.data.producto.filter(p => p && p.id != null);
            productosAsociados = productosOriginales.map(p => p.id.toString());
        }
        // Caso 3: producto_ids está disponible
        else if (Array.isArray(response.data.producto_ids)) {
            productosAsociados = response.data.producto_ids
                .filter(id => id != null)
                .map(id => id.toString());
            productosOriginales = this.productos.filter(p =>
                productosAsociados.includes(p.id.toString())
            );
        }
        // Caso 4: producto es un ID directo
        else if (response.data.producto && !isNaN(response.data.producto)) {
            productosAsociados = [response.data.producto.toString()];
            const productoEncontrado = this.productos.find(p =>
                p.id.toString() === response.data.producto.toString()
            );
            if (productoEncontrado) {
                productosOriginales = [productoEncontrado];
            }
        }

        // 4. Establecer datos del formulario
        this.formData = {
            tipo_equipo_ferroviario: equipoFerroviarioId,
            tipo_origen: response.data.tipo_origen || 'ac_ccd',
            origen: response.data.origen || '',
            tipo_combustible: response.data.tipo_combustible || '',
            tipo_producto: response.data.tipo_producto || '',
            plan_mensual: response.data.plan_mensual || 0,
            plan_anual: response.data.plan_anual || 0,
            plan_acumulado_dia_anterior: response.data.plan_acumulado_dia_anterior || 0,
            real_acumulado_dia_anterior: response.data.real_acumulado_dia_anterior || 0,
            lista_productos: productosAsociados,
            observaciones: response.data.observaciones || '',
            original_productos: productosOriginales,
            original_equipo: response.data.tipo_equipo_ferroviario?.tipo_equipo_name ||
                            response.data.tipo_equipo_ferroviario_name ||
                            ''
        };

        // 5. Forzar actualización del select multiple
        this.$nextTick(() => {
            this.formData.lista_productos = [...productosAsociados];
            console.log('SELECT ACTUALIZADO CON:', this.formData.lista_productos);
        });

    } catch (error) {
        console.error("Error al cargar datos:", error);
        let errorMsg = "Error al cargar el vagón";
        if (error.response?.data?.detail) {
            errorMsg += `: ${error.response.data.detail}`;
        }
        Swal.fire("Error", errorMsg, "error");
        this.$router.push({ name: 'infoOperativo' });
    } finally {
        this.loading = false;
    }
  },

  // Envío del formulario
  async submitForm() {
      this.loading = true;
      this.errors = {};
      
      try {
        // Validar permisos
        if (!this.hasGroup('AdminUFC')) {
          Swal.fire("Error", "No tiene permiso para realizar esta acción", "error");
          return;
        }

        // 1. Manejar cambios en el tipo de producto
        if (this.formData.tipo_producto === 'producto') {
          // Si el tipo es producto, limpiar campos de combustible
          this.formData.tipo_combustible = "-";
          this.formData.tipo_equipo_ferroviario = "";
        } 
        else if (this.formData.tipo_producto === 'contenedor') {
          // Si el tipo es contenedor, limpiar campos de combustible y productos
          this.formData.tipo_combustible = "-";
          this.formData.tipo_equipo_ferroviario = "";
          this.formData.lista_productos = [];
        } 
        else if (this.formData.tipo_producto === 'combustible') {
          // Si el tipo es combustible, limpiar campo de productos
          this.formData.lista_productos = [];
        }

        // 2. Preparar los IDs de productos (siempre se preparan, aunque pueda estar vacío)
        const productosParaEnviar = this.prepararProductosParaEnvio();
      
        // 3. Validar que los productos seleccionados existan (solo si hay productos y es tipo producto)
        if (this.formData.tipo_producto === 'producto' && productosParaEnviar.length > 0) {
          const productosValidos = await this.validarProductos(productosParaEnviar);
          if (!productosValidos) {
            Swal.fire("Error", "Uno o más productos seleccionados no existen", "error");
            return;
          }
        }

        // 4. Preparar datos para enviar
        const datosEnvio = {
          ...this.formData,
          producto_ids: productosParaEnviar,
        };

        // 5. Enviar la solicitud PUT al backend
        const vagonId = this.$route.params.id;
        await axios.put(`/ufc/vagones-productos/${vagonId}/`, datosEnvio);
      
        // 6. Mostrar mensaje de éxito
        Swal.fire("Éxito", "Los cambios se han guardado correctamente", "success")
          .then(() => {
            this.$router.push({ name: 'InfoOperativo' });
          });
      } catch (error) {
        console.error("Error al guardar:", error.response);
      
        // Manejar errores de validación del backend
        if (error.response?.status === 400) {
          this.errors = error.response.data;
        } else {
          let errorMsg = "No se pudo guardar el registro";
          if (error.response?.data) {
            errorMsg += `: ${JSON.stringify(error.response.data)}`;
          }
          Swal.fire("Error", errorMsg, "error");
        }
      } finally {
        this.loading = false;
      }
    },

  prepararProductosParaEnvio() {
    return this.formData.lista_productos
      .map(id => {
        const idNum = parseInt(id);
        return isNaN(idNum) ? null : idNum;
      })
      .filter(id => id !== null);
  },

  async validarProductos(idsProductos) {
    try {
      const response = await axios.post("/ufc/producto-vagon/verificar/", {
        producto_ids: idsProductos.map(id => parseInt(id))
      });
      return response.data.todos_existen;
    } catch (error) {
      console.error("Error al validar productos:", error);
      return false;
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
      lista_productos: [],
      observaciones: "",
    };
    this.errors = {};
  },

  volver_principal() {
    this.$router.push({ name: "InfoOperativo" });
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
      this.tipos_equipos_ferroviarios = response.data.map(item => ({
        ...item,
        id: item.id.toString() // Convertir IDs a string
      }));
      
      console.log('Equipos ferroviarios cargados:', this.tipos_equipos_ferroviarios);
    } catch (error) {
      console.error("Error al obtener los equipos ferroviarios:", error);
      Swal.fire("Error", "Hubo un error al obtener los equipos ferroviarios.", "error");
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
      if (response.data && response.data.results) {
        this.productos = response.data.results.map(p => ({
          ...p,
          id: p.id?.toString() || '' // Conversión segura a string
        }));
      } else {
        console.error('Estructura inesperada en productos:', response.data);
        this.productos = [];
      }
    } catch (error) {
      console.error("Error al obtener productos:", error);
      this.productos = [];
    }
  },
},
};
</script>
  
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
  
  /* Estilos para validación */
  .is-invalid {
    border-color: #dc3545;
  }
  
  .invalid-feedback {
    color: #dc3545;
    font-size: 0.875em;
  }
  
  /* Estilos para loading */
  .spinner-border {
    margin-right: 5px;
  }
  </style>