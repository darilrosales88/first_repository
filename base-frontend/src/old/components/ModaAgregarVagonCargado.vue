<template>
    <div class="modal-overlay" v-if="visible" @click.self="cerrarModal">
      <div class="modal-content">
        <h2 class="mb-4">Nuevo registro de vagón cargado/descargado</h2>
        <form @submit.prevent="submitForm">
          <div class="row">
            <!-- Columna 1 -->
            <div class="col-md-6">
  
              <!-- Campo: equipo_ferroviario(excepto locomotora) -->
              <div class="mb-3">
                <label for="no_id" class="form-label"
                  >ID equipo ferroviario<span style="color: red">*</span></label
                >
                <select
                  class="form-select"
                  v-model="formData.no_id"
                  id="no_id"
                  name="no_id"
                  required
                >
                  <option
                    v-for="equipo in equipos_ferroviarios"
                    :key="equipo.id"
                    :value="equipo.numero_identificacion"
                  >
                    {{ equipo.id }}-{{ equipo.numero_identificacion }}
                  </option>
                </select>
              </div>
              
              <!-- campo fecha_despacho -->
              <div class="mb-3">
                <label for="fecha_despacho" class="form-label">Fecha de despacho <span style="color: red">*</span></label>
                <input
                    type="date"
                    class="form-control"
                    v-model="formData.fecha_despacho"
                    id="fecha_despacho"
                    name="fecha_despacho"
                    required
                />
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
            </div>
  
            <!-- Columna 2 -->
            <div class="col-md-6">
              <!-- campo fecha_llegada -->
              <div class="mb-3">
                <label for="fecha_llegada" class="form-label">Fecha de llegada <span style="color: red">*</span></label>
                <input
                    type="date"
                    class="form-control"
                    v-model="formData.fecha_llegada"
                    id="fecha_llegada"
                    name="fecha_llegada"
                    required
                />
              </div>
              <!-- Campo: observaciones -->
              <div class="mb-3">
                <label for="causas_incumplimiento" class="form-label"
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
              
              <!-- Aquí puedes agregar más campos para la columna 2 si es necesario -->
            </div>
          </div>
  
          <!-- Botón de envío -->
          <div class="text-center">
            <button type="submit" class="btn btn-primary">Guardar</button>
            <button @click="cerrarModal" class="btn btn-secondary">Volver</button>
          </div>
        </form>
      </div>
    </div>
</template>
  
  <script>
  import axios from "axios";
  import Swal from "sweetalert2";
  
  export default {
    name: "ModalVagonCargado",
    props: {
      visible: {
        type: Boolean,
        required: true,
      },
      tipoEquipo: {//esta es la variable que se usará para el tipo_equipo recibido desde el componente padre
      type: String,
      required: false,
      default: null
    }
    },
    data() {
      return {
        formData: {
          no_id: "",
          fecha_despacho: new Date().toISOString().split('T')[0], // Formato YYYY-MM-DD
          tipo_origen: "ac_ccd",
          origen: "",
          fecha_llegada: new Date().toISOString().split('T')[0], // Formato YYYY-MM-DD
          observaciones:""
        },
        equipos_ferroviarios: [],
        puertos: [],
        entidades: [],
      };
    },
    mounted() {
      this.getEquipos();      
      this.getEntidades();
      this.getPuertos();
    },
    watch: {//aqui es donde se escucha el valor enviado por el componente padre, con newVal
      tipoEquipo(newVal) {
        if (newVal) {
          this.getEquipos();
        }
      }
    },
    methods: {
      cerrarModal() {
        this.$emit("cerrar-modal");
      },
      
      async submitForm() {
  // Validación de campos
  if (!this.formData.no_id || !this.formData.fecha_despacho || !this.formData.origen) {
    Swal.fire("Error", "Por favor complete todos los campos obligatorios", "error");
    return;
  }
   
  /*validando que la fecha de despacho no sea mayor que la fecha de llegada */
  const fechaDespacho = new Date(this.formData.fecha_despacho);
  const fechaLlegada = new Date(this.formData.fecha_llegada || this.formData.fecha_despacho);
  
  if (fechaDespacho > fechaLlegada) {
    Swal.fire("Error", "La fecha de despacho no puede ser posterior a la fecha de llegada", "error");
    return;
  }

  // Emitir los datos del formulario SIN guardar en el backend
  this.$emit('vagon-agregado', {
    no_id: this.formData.no_id,
    fecha_despacho: this.formData.fecha_despacho,
    tipo_origen: this.formData.tipo_origen,
    origen: this.formData.origen,
    fecha_llegada: this.formData.fecha_llegada || this.formData.fecha_despacho,
    observaciones: this.formData.observaciones || ""
  });

  this.$emit('cerrar-modal');
  Swal.fire("Éxito", "Vagón preparado para asociar", "success");
},
async getEquipos() {
    try {
      let url = "/api/e-f-no-locomotora/";
      if (!this.tipoEquipo) {
        Swal.fire({
          title: "Error",
          text: "No se ha proporcionado un tipo de equipo, vaya al componente principal y escoja uno.",
          icon: "error",
          willClose: () => {
            this.cerrarModal();
          }
        });
        return;
      }
      
      // al tipo de equipo específico lo añadimos como parámetro          
      url += `?tipo_equipo=${this.tipoEquipo}`;
      const response = await axios.get(url);
      
      // en caso de que no exista EF para el tipo seleccionado en el componente padre
      if (response.data.length === 0) {
        Swal.fire({
          title: "Error",
          text: "No existen equipos ferroviarios para el tipo seleccionado.",
          icon: "error",
          willClose: () => {
            this.cerrarModal();
          }
        });
        return;
      }

      this.equipos_ferroviarios = response.data;
    } catch (error) {
      console.error("Error al obtener los equipos ferroviarios:", error);
      Swal.fire({
        title: "Error",
        text: "Hubo un error al obtener los equipos ferroviarios.",
        icon: "error",
        willClose: () => {
          this.cerrarModal();
        }
      });
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
    },
  };
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 2000; /* asegurar que es menor que el de SweetAlert */
  }
  
  .modal-content {
    background-color: white;
    padding: 25px;
    border-radius: 8px;
    width: 90%;
    max-width: 700px;
    max-height: 85vh;
    overflow-y: auto;
    position: relative;
    z-index: 2001; /* asegurar que es menor que el de SweetAlert */
  }

  /* Estilos para el modal hijo (debe estar en el componente hijo), que se sobreponga por encima del comp padre */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000; /* Mayor que cualquier otro elemento */
}

.modal-content {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  width: 90%;
  max-width: 700px;
  max-height: 85vh;
  overflow-y: auto;
  position: relative;
  z-index: 2001;
}

/* Ocultar elementos del padre cuando el modal está activo */
.v-show-modal-active {
  display: none !important;
}
  </style>
<style>
/* Estilo global para SweetAlert */
.swal2-container {
  z-index: 999999 !important;
}
</style>
  