<template>
  <div style="background-color: #002a68; color: white; text-align: right">
    <h6>Bienvenido:</h6>
  </div>
  <Navbar-Component />
  <Producto-Vagones />
  <div class="container mt-2 px-6" style="padding-left: 10%">
    <div class="row mb-4">
      <h2 class="mb-4">Nuevo registro de situados</h2>

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
                required
              >
                <option
                  v-for="entidad in entidades"
                  :key="entidad.id"
                  :value="entidad.id"
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
                  :value="puerto.id"
                >
                  {{ puerto.id }}- {{ puerto.nombre_puerto }}
                </option>
              </select>
            </div>

            <!-- Campo: tipo_equipo -->
            <div class="mb-3">
              <label for="tipo_equipo" class="form-label"
                >Tipo de Equipo <span style="color: red">*</span></label
              >
              <select
                class="form-select"
                v-model="formData.tipo_equipo"
                id="tipo_equipo"
                name="tipo_equipo"
                @change="buscarEquipos"
                required
              >
                <option value="">Seleccione un tipo</option>
                <option
                  v-for="option in tipo_equipo_options"
                  :key="option.id"
                  :value="option.id"
                >
                  {{ option.text }}
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

            <div class="mb-3">
              <label for="operacion" class="form-label"
                >Operación <span style="color: red">*</span></label
              >
              <select
                class="form-select"
                v-model="formData.operacion"
                id="operacion"
                name="operacion"
                required
              >
                <option value="">Seleccione una operación</option>
                <option
                  v-for="option in t_operacion_options"
                  :key="option.id"
                  :value="option.id"
                >
                  {{ option.text }}
                </option>
              </select>
            </div>
          </div>

          <!-- Columna 2 -->
          <div class="col-md-6">
            <!-- Campo: producto -->
            <div class="mb-3">
              <label for="producto" class="form-label">
                  Producto
                  <button
                  class="create-button ms-2"
                  @click.prevent="abrirModalAgregarProducto"
                  >
                  <i class="bi bi-plus-circle large-icon"></i>
                  </button>
              </label>
              
              <template v-if="formData.estado === 'cargado'">
                  <select
                  v-if="!loading"
                  class="form-select"
                  v-model="formData.producto"
                  id="producto"
                  name="producto"
                  required
                  >
                  <option value="" disabled>Seleccione un producto</option>
                  <option 
                      v-for="producto in productos" 
                      :key="producto.id"
                      :value="producto.id"
                  >
                      {{ producto.id }}-{{ producto.producto_name }} - {{ producto.producto_codigo }}
                  </option>
                  </select>
                  <div v-else class="text-muted">
                  <i class="bi bi-arrow-repeat"></i> Cargando productos...
                  </div>
              </template>
              
              <div v-else class="text-muted">
                  (Seleccione "Cargado" para ver los productos)
              </div>
            </div>
            <ModalAgregarProducto
              v-if="mostrarModal"
              :visible="mostrarModal"
              @cerrar-modal="cerrarModal"
            />
            
            <!-- Campo: situados -->
            <div class="mb-3">
              <label for="situados" class="form-label">
                  Situados <span style="color: red">*</span>
              </label>
              <input
                  type="number"
                  class="form-control"
                  v-model.number="formData.situados"
                  id="situados"
                  name="situados"
                  min="1"
                  required
              >
            </div>

            <!-- Campo: pendiente_proximo_dia -->
            <div class="mb-3">
              <label for="pendiente_proximo_dia" class="form-label">
                  Pendientes al próximo día <span style="color: red">*</span>
              </label>
              <input
                  type="number"
                  class="form-control"
                  v-model.number="formData.pendiente_proximo_dia"
                  id="pendiente_proximo_dia"
                  name="pendiente_proximo_dia"
                  min="0"
                  required
              >
            </div>

            <!-- Campo: observaciones -->
            <div class="mb-3">
              <label for="observaciones" class="form-label"
                >Observaciones
              </label>
              <textarea
                class="form-control"
                v-model="formData.observaciones"
                id="observaciones"
                name="observaciones"
                rows="3"
              ></textarea>
            </div>
          </div>
        </div>

        <div class="text-center">
          <button 
              type="button" 
              class="btn btn-primary" 
              @click="submitForm"
              >
              Agregar
          </button>
          <button @click="confirmCancel" class="btn btn-secondary">
            Cancelar
          </button>
        </div>
      </form>
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
      formData: {
      tipo_origen: "ac_ccd",
      origen: "",
      tipo_equipo: "",
      estado: "cargado",
      operacion: "",
      producto: "",
      situados: 0,
      pendiente_proximo_dia: 0,
      observaciones: "",
    },
    entidades: [],
    puertos: [],
    productos: [],
    mostrarModal: false,
    loading: false,
    tipo_equipo_options: [
      { id: "casilla", text: "Casilla" },
      { id: "caj_gon", text: "Cajon o Gondola" },
    ],
    t_operacion_options: [
      { id: "carga", text: "Carga" },
      { id: "descarga", text: "Descarga" },
    ],
  };
},
mounted() {
  this.getProductos();
  this.getEntidades();
  this.getPuertos();
},
methods: {
  async getEntidades() {
    try {
      const response = await axios.get("/api/entidades/");
      this.entidades = response.data.results;
    } catch (error) {
      console.error("Error al obtener entidades:", error);
      Swal.fire("Error", "No se pudieron obtener las entidades", "error");
    }
  },
  
  async getProductos() {
    try {
      this.loading = true;
      const response = await axios.get("/api/productos/", {
        params: { limit: 100 },
      });

      if (response.status === 200) {
        this.productos = response.data.results.map(producto => ({
          id: producto.id,
          producto_name: producto.nombre_producto || producto.descripcion || `Producto ${producto.id}`,
          producto_codigo: producto.codigo || 'N/A',
          tipo_embalaje_name: producto.tipo_embalaje?.nombre || 'N/A'
        }));
      }
    } catch (error) {
      console.error("Error al obtener productos:", error);
      let errorMsg = "Error al cargar productos";

      if (error.response?.data?.detail) {
        errorMsg += `: ${error.response.data.detail}`;
      }

      Swal.fire("Error", errorMsg, "error");
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
  
  async submitForm() {
    try {
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
      
      if (this.formData.estado === "cargado" && !this.formData.producto) {
        errors.push("El campo Producto es requerido cuando el estado es Cargado");
      }
      
      if (this.formData.situados === null || this.formData.situados < 0) {
        errors.push("La cantidad de situados debe ser un número positivo");
      }

      if (this.formData.pendiente_proximo_dia === null || this.formData.pendiente_proximo_dia < 0) {
        errors.push("Los pendientes al próximo día deben ser un número positivo");
      }

      if (errors.length > 0) {
        throw new Error(errors.join("\n"));
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
        observaciones: this.formData.observaciones
      };

      // Enviar datos al endpoint correcto
      const response = await axios.post("http://127.0.0.1:8000/ufc/situados/", payload);

      if (response.status === 201) {
        Swal.fire({
          title: "Éxito",
          text: "Registro creado correctamente",
          icon: "success",
        }).then(() => {
          this.resetForm();
          this.$router.push({ name: "InfoOperativo" });
        });
      }
    } catch (error) {
      let errorMessage = "Error al crear el registro";
      
      if (error.message) {
        errorMessage = error.message;
      } else if (error.response?.data) {
        errorMessage = Object.values(error.response.data).join("\n");
      }
      
      Swal.fire("Error", errorMessage, "error");
      console.error("Error al enviar el formulario:", error);
    }
  },
  
  resetForm() {
    this.formData = {
      tipo_origen: "ac_ccd",
      origen: "",
      tipo_equipo: "",
      estado: "cargado",
      operacion: "",
      producto: "",
      situados: 0,
      pendiente_proximo_dia: 0,
      observaciones: "",
    };
  },
  
  confirmCancel() {
    Swal.fire({
      title: "¿Cancelar operación?",
      text: "Los datos no guardados se perderán",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Sí, cancelar",
      cancelButtonText: "No, continuar",
    }).then((result) => {
      if (result.isConfirmed) {
        this.resetForm();
        this.$router.push({ name: "InfoOperativo" });
      }
    });
  }
}
};
</script>

<style scoped>
.create-button {
background: none;
border: none;
color: green;
padding: 0;
cursor: pointer;
}

.create-button:hover {
color: darkgreen;
}

.large-icon {
font-size: 1.2rem;
}

.form-container {
max-width: 300px;
margin: 50px;
padding: 20px;
background-color: #f9f9f9;
border-radius: 8px;
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
font-family: "Franklin Gothic Medium", "Arial Narrow", Arial, sans-serif;
text-align: left;
margin-bottom: 20px;
font-size: 20px;
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
select,
textarea {
padding: 8px;
border: 1px solid #ccc;
border-radius: 4px;
width: 100%;
}

.btn {
margin: 0 5px;
padding: 8px 16px;
}

.text-warning {
color: #ffc107;
}

.text-success {
color: #28a745;
}

.text-danger {
color: #dc3545;
}
</style>