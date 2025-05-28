<template>
  <div class="container py-3">
    <!-- Encabezado -->
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-search me-2"></i>Rotación de los vagones
        </h5>
        <!-- Botón para abrir el modal -->
      </div>

      <!-- Cuerpo -->
      <div class="card-body p-3">

        <!-- Registro de rotación por tipo de equipo -->
        <div class="mt-4">
          <h6
            class="d-flex justify-content-between align-items-center text-secondary fw-semibold mb-3"
            style="padding: 0.5rem 1rem">
            
            <!-- Texto centrado -->
            <span class="d-flex align-items-center">
              <i class="bi bi-list-ul me-2"></i>
              Registro de rotación de cada tipo de equipo ferroviario
            </span>

            <!-- Botón alineado a la derecha -->
            <button class="btn btn-sm btn-primary" @click="mostrarModal = true">
              <i class="bi bi-plus-circle me-1"></i>Adicionar rotación
            </button>
          </h6>

          <table class="table table-sm table-bordered table-hover">
            <thead class="table-light">
              <tr>
                <th scope="col">Tipo de equipo ferroviario</th>
                <th scope="col">En servicio</th>
                <th scope="col">Plan carga</th>
                <th scope="col">Real carga</th>
                <th scope="col">Plan rotación</th>
                <th scope="col">Real rotación</th>
                <th scope="col">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(equipo, index) in registrosRotacion" :key="index">
                <td>
                  {{ equipo.tipo_equipo_ferroviario_nombre }}--{{
                    equipo.tipo_carga_name
                  }}
                </td>
                <td>{{ equipo.en_servicio }}</td>
                <td>{{ equipo.plan_carga }}</td>
                <td>{{ equipo.real_carga }}</td>
                <td>{{ equipo.plan_rotacion }}</td>
                <td>{{ equipo.real_rotacion }}</td>
                <td>
                  <button
                    class="btn btn-sm btn-outline-danger"
                    @click="eliminarRotacion(equipo.id)">
                    <i class="bi bi-trash"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="registrosRotacion.length === 0">
                <td colspan="7" class="text-center text-muted">
                  No hay resultados disponibles.
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Resumen general -->
        <div class="mt-4">
          <h6 class="text-secondary fw-semibold mb-3">
            <i class="bi bi-bar-chart-line me-2"></i>Resumen general
          </h6>

          <div class="row g-3">
            <div class="col-md-4">
              <div class="card border-secondary">
                <div class="card-body p-1">
                  <h6 class="card-title text-secondary fw-semibold">
                    Plan total carga
                  </h6>
                  <p class="card-text display-6 text-center">
                    {{ resumen.planCarga }}
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card border-secondary">
                <div class="card-body p-1">
                  <h6 class="card-title text-secondary fw-semibold">
                    Plan total de rotación
                  </h6>
                  <p class="card-text display-6 text-center">
                    {{ resumen.planRotacion }}
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card border-secondary">
                <div class="card-body p-1">
                  <h6 class="card-title text-secondary fw-semibold">
                    Total de vagones en servicio
                  </h6>
                  <p class="card-text display-6 text-center">
                    {{ resumen.totalVagonesEnServicio }}
                  </p>
                </div>
              </div>             
            </div>
            
          </div>

          <div class="row g-3 mt-1">
            <div class="col-md-6">
              <div class="card border-secondary">
                <div class="card-body p-1">
                  <h6 class="card-title text-secondary fw-semibold">
                    Total real carga
                  </h6>
                  <p class="card-text display-6 text-center">
                    {{ resumen.realCarga }}
                  </p>
                </div>
              </div>
            </div>

            <div class="col-md-6">
              <div class="card border-secondary">
                <div class="card-body p-1">
                  <h6 class="card-title text-secondary fw-semibold">
                    Total real de rotación
                  </h6>
                  <p class="card-text display-6 text-center">
                    {{ resumen.realRotacion }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para adicionar/editar rotación de vagones -->
    <div class="modal fade ufc-modal-overlay" :class="{ show: mostrarModal }" tabindex="-1" role="dialog" style="display: block; " v-if="mostrarModal">
      <div class="modal-dialog modal-dialog-centered" role="document" >
        <div class="modal-content" >
          <div class="ufc-modal-header">
            <h3 class="modal-title">
              {{
                modoEdicion
                  ? "Editar rotación de vagones"
                  : "Adicionar rotación de vagones"
              }}
            </h3>
            <button class="ufc-modal-close" @click="cerrarModal"><i class="bi bi-x"></i></button>
          </div>
          <div class="ufc-modal-body">
            
              <form @submit.prevent="modoEdicion ? actualizarRotacion() : guardarRotacion()">
                <div class="ufc-form-grid">
                  <!-- Tipo de equipo ferroviario -->
                  <div class="ufc-input-group">
                    <label for="tipoEquipo" class="form-label small fw-semibold text-secondary">
                      Tipo de equipo ferroviario
                    </label>

                    <select class="form-select form-select-sm" style="width:280px; padding: 8px 12px;" id="tipoEquipo" v-model="nuevaRotacion.tipoEquipo" required>
                      <option value="" disabled>
                        Seleccione un tipo de equipo
                      </option>
                      <option v-for="equipo in tiposEquiposFerroviarios":key="equipo.id" :value="equipo.id"> {{ equipo.tipo_equipo_name }}--{{equipo.tipo_carga_name}}
                      </option>
                    </select>
                  </div>

                  <!-- Vagones en servicio -->
                  <div class="ufc-input-group">
                    <label for="vagonesEnServicio" class="form-label small fw-semibold text-secondary" >
                      Vagones en servicio
                    </label>
                    <input type="number" class="form-control form-control-sm" style="width:165px; padding: 8px 12px;" id="vagonesEnServicio" v-model.number="nuevaRotacion.vagonesEnServicio" min="0" required/>
                  </div>
                </div>
              </form>
            
          </div>
          <div class="ufc-form-actions">
            <button type="button" class="ufc-button secondary" @click="cerrarModal">
              <i class="bi bi-x-circle"></i>Cancelar
            </button>
            <button type="button" class="ufc-button primary" @click="modoEdicion ? actualizarRotacion() : guardarRotacion()">
              <i class="bi bi-check-circle"></i>{{ modoEdicion ? "Actualizar" : "Aceptar" }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
export default {
  name: "ConsultaRotacionVagones",
  data() {
    return {
      resumen: {
        totalVagonesEnServicio: 0,
        planCarga: 0,
        realCarga: 0,
        planRotacion: 0,
        realRotacion: 0,
      },
      registrosRotacion: [],
      mostrarModal: false, // Controla la visibilidad del modal
      nuevaRotacion: {
        tipoEquipo: "",
        vagonesEnServicio: 0,
      },
      informeOperativoId: null,
      tiposEquiposFerroviarios: [],
      modoEdicion: false, // Indica si estamos editando o agregando un registro
      indiceEdicion: null, // Guarda el índice del registro que se está editando
    };
  },

  props: {
    informeId: {
      type: [String, Number],
      required: true,
    },
  },

  mounted() {
    this.get_rotaciones();
    this.getEquipos();
  },
  methods: {

    async get_rotaciones() {
      this.loading = true; // Activa el estado de carga
      const today = new Date();
      const fechaFormateada = `${today.getFullYear()}-${String(
        today.getMonth() + 1
      ).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;

      try {
        let allRotaciones = []; // Almacena todos los registros de rotaciones
        let nextPage = "/ufc/rotaciones/"; // URL inicial del endpoint
        const infoID = await axios.get(
          `/ufc/verificar-informe-existente/?fecha_operacion=${fechaFormateada}`
        );
        if (infoID.data.existe) {
          //Para la reutilizacion del componente se deberia usar el operador ternario en informe: props.informeId? props.informeId: infoID.data.id
          // Bucle para manejar paginación (si aplica)
          while (nextPage) {
            const response = await axios.get(nextPage, {
              params: {
                page: this.currentPage,
                page_size: this.itemsPerPage,
                informe: infoID.data.id,
              },
            });
            allRotaciones = [...allRotaciones, ...response.data.results]; // Agrega los resultados
            nextPage = response.data.next; // Actualiza la URL de la siguiente página
          }
        }

        // Asigna los datos obtenidos a una variable en el componente
        this.registrosRotacion = allRotaciones;

        // Calcula las sumas de los campos relevantes
        this.resumen.totalVagonesEnServicio = allRotaciones.reduce(
          (total, item) => total + item.en_servicio,
          0
        );
        this.resumen.planCarga = allRotaciones.reduce(
          (total, item) => total + item.plan_carga,
          0
        );
        this.resumen.realCarga = allRotaciones.reduce(
          (total, item) => total + item.real_carga,
          0
        );
        this.resumen.planRotacion = allRotaciones.reduce(
          (total, item) => total + item.plan_rotacion,
          0
        );
        this.resumen.realRotacion = allRotaciones.reduce(
          (total, item) => total + item.real_rotacion,
          0
        );

        // Opcional: Si necesitas realizar alguna transformación de datos, hazlo aquí
        console.log("Rotaciones cargadas:", this.registrosRotacion);
        console.log("Total vagones en servicio:", this.totalVagonesEnServicio);
        console.log("Plan de carga:", this.planCarga);
        console.log("Real de carga:", this.realCarga);
        console.log("Plan de rotación:", this.planRotacion);
        console.log("Real de rotación:", this.realRotacion);
      } catch (error) {
        console.error("Error al obtener las rotaciones:", error);
        Swal.fire("Error", "Hubo un error al cargar las rotaciones.", "error");
      } finally {
        this.loading = false; // Desactiva el estado de carga
      }
    },

    async getEquipos() {
      try {
        const response = await axios.get("/api/tipo-e-f-no-locomotora/");
        this.tiposEquiposFerroviarios = response.data;
      } catch (error) {
        console.error("Error al obtener los equipos:", error);
        Swal.fire("Error", "Hubo un error al obtener los equipos.", "error");
      }
    },

    cerrarModal() {
      this.mostrarModal = false;
      this.nuevaRotacion = {
        tipoEquipo: "",
        vagonesEnServicio: 0,
      };
      this.modoEdicion = false;
      this.indiceEdicion = null;
    },

    async verificarInformeOperativo() {
      try {
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

        if (informeResponse.data.existe) {
          this.informeOperativoId = informeResponse.data.id;
          return true;
        }
        return false;
      } catch (error) {
        console.error("Error al verificar informe:", error);
        return false;
      }
    },
    
    async guardarRotacion() {
      // 1. Verificar si existe informe operativo para la fecha actual
      const existeInforme = await this.verificarInformeOperativo();
      if (0) {
        Swal.fire(
          "Error",
          "No existe un informe operativo creado para la fecha actual. Debe crear uno primero.",
          "error"
        );
        this.$router.push({ name: "InfoOperativo" });
        return;
      }

      // 2. Validar campos obligatorios
      if (
        !this.nuevaRotacion.tipoEquipo ||
        this.nuevaRotacion.vagonesEnServicio <= 0
      ) {
        Swal.fire(
          "Campos incompletos",
          "Por favor, complete todos los campos obligatorios.",
          "warning"
        );
        return;
      }

      try {
        // 3. Hacer POST real a la API
        const response = await axios.post("/ufc/rotaciones/", {
          tipo_equipo_ferroviario: this.nuevaRotacion.tipoEquipo,
          en_servicio: this.nuevaRotacion.vagonesEnServicio,
          informe_operativo: this.informeOperativoId,
        });
        console.log("Esto es lo que se envia", {
          tipo_equipo_ferroviario: this.nuevaRotacion.tipoEquipo,
          en_servicio: this.nuevaRotacion.vagonesEnServicio,
          informe_operativo: this.informeOperativoId,
        });
        await this.get_rotaciones();
        // 4. Actualizar la tabla local con el nuevo registro desde la respuesta del backend

        // 5. Mostrar mensaje de éxito y cerrar el modal
        Swal.fire(
          "Éxito",
          "La rotación ha sido guardada correctamente.",
          "success"
        );
        this.cerrarModal();
      } catch (error) {
        console.error("Error al guardar la rotación:", error);

        let mensajeError = "Hubo un problema al guardar la rotación.";
        if (error.response && error.response.data) {
          const errores = error.response.data;
          mensajeError =
            Object.values(errores).flat().join(" ") ||
            "Hubo un problema al guardar la rotación.";
        }

        Swal.fire("Error", mensajeError, "error");
      }
    },

    async actualizarRotacion() {
      if (
        !this.nuevaRotacion.tipoEquipo ||
        this.nuevaRotacion.vagonesEnServicio <= 0
      ) {
        Swal.fire(
          "Error",
          "Por favor, complete todos los campos obligatorios.",
          "error"
        );
        return;
      }

      try {
        // Actualiza el registro en la tabla
        this.registrosRotacion[this.indiceEdicion] = {
          tipoEquipoFerroviario: this.nuevaRotacion.tipoEquipo,
          enServicio: this.nuevaRotacion.vagonesEnServicio,
          planCarga: 0,
          realCarga: 0,
          planRotacion: 0,
          realRotacion: 0,
        };
        Swal.fire(
          "Éxito",
          "La rotación ha sido actualizada correctamente.",
          "success"
        );
        this.cerrarModal();
      } catch (error) {
        console.error("Error al actualizar la rotación:", error);
        Swal.fire(
          "Error",
          "Hubo un problema al actualizar la rotación.",
          "error"
        );
      }
    },

    async eliminarRotacion(id) {
      try {
        const result = await Swal.fire({
          title: "¿Estás seguro?",
          text: "¡No podrás revertir esta acción!",
          icon: "warning",
          showCancelButton: true,
          cancelButtonText: '<i class="bi bi-x-circle me-1"></i>Cancelar',
          cancelButtonColor: "#f1513f",
          confirmButtonText: '<i class="bi bi-trash me-1"></i>Eliminar',
          confirmButtonColor: "#007bff",
          reverseButtons: true,
        });

        if (result.isConfirmed) {
          await axios.delete(`/ufc/rotaciones/${id}/`);
          await Swal.fire("Eliminado", "El registro ha sido eliminado correctamente.", "success");
          await this.get_rotaciones();
        }
      } catch (error) {
        console.error("Error al eliminar la rotación:", error);
        Swal.fire("Error", "Ocurrió un error al eliminar el registro.", "error");
      }
      },
  },
};
</script>

<style scoped>

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

.ufc-modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #002a68;
  color: white;
  border-radius: 0.5rem 0.5rem 0 0;
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

.ufc-modal-body .ufc-form-actions {
  border-top: 1px solid #eee;
  padding-top: 15px;
  margin-top: 0;
}

.ufc-modal-body {
  padding: 20px;
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

.ufc-form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
 
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
  margin: 15px 0;
}

.ufc-button.primary {
  margin-right: 20px;
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

.btn-outline-danger {
  color: #dc3545;
  border-color: #dc3545;
}

.btn-outline-danger:hover {
  color: #fff;
}

/* Resumen general */
.card {
  border-radius: 0.5rem;
  border: 1px solid #e0e0e0;
}

.card-body {
  padding: 1rem;
}

.display-6 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #0d6efd;
}

/* Tabla */
.table {
  font-size: 0.875rem;
}

.table thead th {
  background-color: #f8f9fa;
  border-color: #dee2e6;
  color: #495057;
  font-weight: 500;
}

.table tbody tr:hover {
  background-color: #f8f9fa;
}

/* Mensaje sin resultados */
.text-muted {
  font-size: 0.9rem;
  letter-spacing: 0.02rem;
}

/* Responsive */
@media (max-width: 768px) {
  .table-responsive {
    overflow-x: auto;
  }

  .table {
    min-width: 600px;
  }
}
</style>
