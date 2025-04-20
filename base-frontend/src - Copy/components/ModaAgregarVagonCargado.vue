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
    },
    data() {
      return {
        formData: {
          no_id: "",
          fecha_despacho: new Date().toISOString().substr(0, 10), // Fecha actual por defecto
          tipo_origen: "ac_ccd",
          origen: "",
          fecha_llegada: new Date().toISOString().substr(0, 10), // Fecha actual por defecto
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
    methods: {
        async submitForm() {
            try {
            await axios.post("ufc/registro-vagones-cargados/", this.formData);
            Swal.fire("Éxito", "Vagón agregado correctamente", "success");
            
            // Emitir evento personalizado para notificar al padre
            this.$emit('vagon-agregado');
            
            this.$emit('cerrar-modal');
            } catch (error) {
            console.error("Error al agregar vagón:", error);
            Swal.fire("Error", "No se pudo agregar el vagón", "error");
            }
        },
      cerrarModal() {
        this.$emit("cerrar-modal");
      },
      async getEquipos() {
        try {
            const response = await axios.get("/api/e-f-no-locomotora/");
            this.equipos_ferroviarios = response.data;
        } catch (error) {
            console.error("Error al obtener los equipos ferroviarios:", error);
            Swal.fire("Error", "Hubo un error al obtener los equipos ferroviarios.", "error");
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
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    width: 80%;
    max-width: 600px;
  }
  </style>
  