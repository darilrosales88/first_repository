<template>
  <div class="ufc-modal-overlay" >
    <div class="ufc-modal-container" v-if="visible">
      <div class="ufc-modal-header">
        <h3><i class="bi bi-file-earmark-plus"></i>Nuevo registro de vagón cargado/descargado</h3>
        <button class="ufc-modal-close">
          <i class="bi bi-x" @click.self="cerrarModal"></i>
        </button>
      </div>
	  <div class="ufc-modal-body">
        <div class="ufc-form-grid">
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
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
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
                      {{ equipo.numero_identificacion }}
                    </option>
                  </select>
                </div>
                
                <!-- campo fecha_despacho -->
                <div class="mb-3">
                  <label for="fecha_despacho" class="form-label">Fecha de despacho <span style="color: red">*</span></label>
                  <input
                      type="date"
                      style="padding: 8px 12px"
                      class="form-control form-control-sm border-secondary"
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
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
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
                    style="padding: 8px 12px"
                    class="form-select form-select-sm border-secondary"
                    v-model="formData.origen"
                    id="origen"
                    name="origen"
                  >
                    <option
                      v-for="entidad in entidades"
                      :key="entidad.id"
                      :value="entidad.nombre"
                    >
                     {{ entidad.nombre }}
                    </option>
                  </select>
    
                  <select
                    v-else
                    class="form-select form-select-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="formData.origen"
                    id="origen"
                    name="origen"
                  >
                    <option
                      v-for="puerto in puertos"
                      :key="puerto.id"
                      :value="puerto.nombre_puerto"
                    >
                      {{ puerto.nombre_puerto }}
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
                      style="padding: 8px 12px"
                      class="form-control form-control-sm border-secondary"
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
                    class="form-control form-control-sm border-secondary"
                    style="padding: 8px 12px"
                    v-model="formData.observaciones"
                    id="observaciones"
                    name="observaciones"
                    rows="3"                  
                  ></textarea>
                </div>
                
                <!-- Aquí puedes agregar más campos para la columna 2 si es necesario -->
              </div>
			      </div>

            <!-- Botones del modal -->
            <div class="ufc-form-actions">
              <button
                type="button"
                class="ufc-button secondary"
                @click="cerrarModal">
                <i class="bi bi-x-circle"></i> Cancelar
              </button>
              <button
                type="submit"
                class="ufc-button primary">
                <i class="bi bi-check-circle"></i> Agregar
              </button>
            </div>
          </form>
        </div>
      </div>
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
},
async getEquipos() {
    try {
      let url = "/api/e-f-no-locomotora/";
      if (!this.tipoEquipo) {
        this.cerrarModal();
        Swal.fire({
          title: "Error",
          text: "Seleccione el tipo de equipo ferroviario",
          icon: "error",
          showCancelButton: false,
          confirmButtonText: "Aceptar",
          confirmButtonColor: "#ff4444"
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
    },
  };
  </script>
  
<style scoped>
/* Estilos para la sección de vagones asociados */
.ufc-vagones-container {
  margin-top: 30px;
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.ufc-vagones-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.ufc-vagones-header h3 {
  color: #002a68;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
}

.ufc-button.small {
  padding: 6px 12px;
  font-size: 0.8rem;
}

.ufc-vagones-table-container {
  overflow-x: auto;
}

.ufc-vagones-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.ufc-vagones-table th {
  background-color: #002a68;
  color: white;
  padding: 10px 12px;
  text-align: left;
  font-weight: 500;
  font-size: 0.85rem;
}

.ufc-vagones-table td {
  padding: 12px;
  border-bottom: 1px solid #eee;
  font-size: 0.85rem;
}

.ufc-vagones-table tr:hover {
  background-color: #f8f9fa;
}

.ufc-actions-cell {
  display: flex;
  gap: 8px;
}

.ufc-icon-button {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.ufc-icon-button i {
  font-size: 0.9rem;
}

.ufc-icon-button.warning {
  background-color: #ffc107;
  color: #212529;
}

.ufc-icon-button.warning:hover {
  background-color: #e0a800;
}

.ufc-icon-button.danger {
  background-color: #dc3545;
  color: white;
}

.ufc-icon-button.danger:hover {
  background-color: #c82333;
}

/* Estilo para estado vacío */
.ufc-vagones-empty {
  margin-top: 20px;
  text-align: center;
  padding: 30px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.ufc-empty-state {
  color: #6c757d;
}

.ufc-empty-state i {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #adb5bd;
}

.ufc-empty-state p {
  margin: 0;
  font-size: 0.9rem;
}

/* Estilos para el modal de vagón */
.ufc-modal-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.ufc-modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

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
.ufc-vagones-agregados {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.ufc-subtitle {
  color: #002a68;
  font-size: 1.1rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.ufc-table-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

.ufc-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

.ufc-table th {
  background-color: #f8f9fa;
  padding: 10px;
  text-align: left;
  border-bottom: 2px solid #ddd;
  color: #555;
}

.ufc-table td {
  padding: 10px;
  border-bottom: 1px solid #eee;
  vertical-align: middle;
}

.ufc-table tr:hover {
  background-color: #f5f5f5;
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
  background: rgb(241, 81, 63);
  color: white;
}

.ufc-button.secondary:hover {
  background: rgb(228, 56, 37);
}

.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
}

.btn-outline-danger:hover {
  color: #fff;
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
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.ufc-modal-container {
  background: white;
  border-radius: 10px;
  width: 90%;
  max-width: 600px;
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