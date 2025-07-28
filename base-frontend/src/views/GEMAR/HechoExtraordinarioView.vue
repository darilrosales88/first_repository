<template>
  <div
    style="
      background-color: #002a68;
      color: white;
      text-align: right;
      padding: 10px;
    "
  >
    <h6>Parte de hechos extraordinarios</h6>
  </div>

  <Navbar-Component /><br />

  <div style="margin-left: 25em; width: 60%">
    <div class="container py-3">
      <div class="card border">
        <div class="card-header bg-light border-bottom">
          <h6 class="mb-0 text-dark fw-semibold">
            <i class="bi bi-clipboard-data me-2"></i>Registro de hechos extraordinarios - Gemar
          </h6>
        </div>

        <div class="card-body p-3">
          <form @submit.prevent="submitForm">
              <div class="row mb-3 g-2">
                <div class="col-md-6">
                  <div class="form-group">
                    <label
                      for="fechaActual"
                      class="form-label small fw-semibold text-secondary"
                    >
                      <i class="bi bi-calendar-check me-2 text-primary"></i>Fecha
                      Actual
                    </label>
                    <input
                      type="date"
                      class="form-control form-control-sm border-secondary"
                      id="fechaActual"
                      v-model="formData.fecha_actual"
                      required
                      disabled
                    />
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-group">
                    <label
                      for="fechaOperacion"
                      class="form-label small fw-semibold text-secondary"
                    >
                      <i class="bi bi-calendar-check me-2 text-primary"></i>Fecha
                      Operación
                    </label>
                    <input
                      type="date"
                      class="form-control form-control-sm border-secondary"
                      id="FechaOperacion"
                      v-model="formData.fecha_operacion"
                      required
                      :disabled="isExistingRecord"
                    />
                  </div>
                </div>
              </div>

              <div class="d-flex justify-content-end gap-2 mt-4">
                <button
                  type="button"
                  class="btn btn-primary"
                  @click="crearParteHechoExtraordinario"
                  :disabled="isExistingRecord || loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  <i v-else class="bi bi-save me-2"></i>
                  {{ loading ? 'Creando...' : 'Crear parte de hecho extraordinario' }}
                </button>
              </div>
            </form>
        </div>
      </div>
    </div>
  </div>

  <div style="margin-left: 16em; width: 80%">
        <!-- Contenedor para las tablas -->
    <div>
      <component :is="currentComponent" />
    </div>
  </div>
  

  

  

  <div style="margin-left: 16em; width: 80%">
    <div class="action-buttons">
      <button class="action-btn reject" @click="rechazar">
        <i class="bi bi-x-circle"></i> Rechazar
      </button>
      <button class="action-btn ready" @click="listo">
        <i class="bi bi-check-circle"></i> Listo
      </button>
      <button class="action-btn approve" @click="aprobar">
        <i class="bi bi-check2-circle"></i> Aprobar
      </button>
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";
import NavbarComponent from "@/components/NavbarComponent.vue";
import hechos_extraordinarios from "@/components/GEMAR/hecho_extraordinario.vue";
export default {
  name: "HechoExtraordinarioView",
  components: {
    NavbarComponent,
    hechos_extraordinarios,   
  },
  data() {
    const now = new Date();
    const offset = now.getTimezoneOffset() * 60000;
    const localISOTime = new Date(now - offset).toISOString().split("T")[0];
    return {
      userPermissions: [],
      userGroups: [],
      currentComponent: "hechos_extraordinarios",
      informeOperativoId: null,
      loadingPermissions: false,
      isExistingRecord: false,
      existingRecordData: null, // Nuevo campo para almacenar datos del registro existente
      checkingExisting: true, // Nuevo campo para estado de verificación
      
      formData: {
        fecha_actual: localISOTime,
        fecha_operacion: localISOTime,
      },
      loading: false,
      error: null,
      success: false,
    };
  },

  async created() {
    await this.fetchUserPermissionsAndGroups();
    await this.verificarInformeOperativo();
  },

  methods: {
    async verificarInformeOperativo() {
      this.checkingExisting = true;
      try {
        const today = new Date();
        const fechaFormateada = `${today.getFullYear()}-${String(
          today.getMonth() + 1
        ).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;

        const response = await axios.get("/gemar/gemar-verificar-informe-existente/", {
          params: { fecha_actual: fechaFormateada },
        });

        if (response.data.existe) {
          this.informeOperativoId = response.data.id;
          this.isExistingRecord = true;
          this.existingRecordData = response.data; // Almacenar datos completos
          
          // Mostrar notificación automática
          //this.showExistingRecordNotification();
          return true;
        } else {
          this.informeOperativoId = null;
          this.isExistingRecord = false;
          this.existingRecordData = null;
        }
        return false;
      } catch (error) {
        console.error("Error al verificar informe:", error);
        this.showErrorToast("Error al verificar el informe existente");
        return false;
      } finally {
        this.checkingExisting = false;
      }
    },

    showExistingRecordNotification() {
      if (this.existingRecordData) {
        Swal.fire({
          icon: "info",
          title: "Parte existente",
          html: `
            <p>Ya existe un parte creado para esta fecha para el usuario autenticado</p>            
          `,
          confirmButtonColor: "#002a68",
        });
      }
    },

    async crearParteHechoExtraordinario() {
        this.loading = true;
        this.error = null;
        this.success = false;

        try {
            // Verificar si ya existe un informe
            const verificacion = await axios.get(
                "/gemar/gemar-verificar-informe-existente/",
                {
                    params: {
                        fecha_actual: this.formData.fecha_actual
                    }
                }
            );

            if (verificacion.data.existe) {
                this.isExistingRecord = true;
                await Swal.fire({
                    icon: "info",
                    title: "Informe existente",
                    text: `Ya existe un informe para la fecha ${this.formData.fecha_actual}`,
                    confirmButtonColor: "#002a68",
                });
                return;
            }

            // Preparar datos mínimos para enviar
            const datosEnvio = {
                fecha_operacion: this.formData.fecha_operacion,
                // No enviar fecha_actual, se asignará automáticamente
                // No enviar creado_por, se asignará automáticamente en el backend
            };

            // Crear el nuevo parte
            const response = await axios.post(
                "/gemar/gemar-partes-hechos-extraordinarios/",
                datosEnvio
            );

            // Manejar respuesta exitosa
            this.success = true;
            this.isExistingRecord = true;
            this.informeOperativoId = response.data.id;

            await Swal.fire({
                icon: "success",
                title: "Éxito",
                text: "Parte de hecho extraordinario creado correctamente",
                confirmButtonColor: "#002a68",
            });

            this.$forceUpdate();

        } catch (error) {
            console.error("Error al crear parte:", error);
            // Mostrar detalles del error si están disponibles
            this.error = error.response?.data || "Error al crear el parte";
            
            await Swal.fire({
                icon: "error",
                title: "Error",
                text: JSON.stringify(this.error),
                confirmButtonColor: "#002a68",
            });
        } finally {
            this.loading = false;
        }
    },
    async rechazar() {
      if (!this.hasGroup("RevisorUFC")) {
        await Swal.fire({
          icon: "error",
          title: "Acceso denegado",
          text: "No tienes permiso para rechazar informes operativos.",
          confirmButtonColor: "#002a68",
        });
        return;
      }
      const result = await Swal.fire({
        title: "¿Estás seguro?",
        text: "Está seguro que desea rechazar este informe operativo?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#002a68",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, rechazar",
        cancelButtonText: "Cancelar",
      });

      // Si el usuario confirma, proceder con la aprobación
      if (result.isConfirmed) {
        await this.CambiarEstado("Rechazado");
      }
    },

    async aprobar() {
      if (!this.hasGroup("RevisorUFC")) {
        await Swal.fire({
          icon: "error",
          title: "Acceso denegado",
          text: "No tienes permiso para aprobar informes operativos.",
          confirmButtonColor: "#002a68",
        });
        return;
      }

      // Mostrar confirmación antes de aprobar
      const result = await Swal.fire({
        title: "¿Estás seguro?",
        text: "Está seguro que desea aprobar este informe operativo?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#002a68",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, aprobar",
        cancelButtonText: "Cancelar",
      });

      // Si el usuario confirma, proceder con la aprobación
      if (result.isConfirmed) {
        await this.CambiarEstado("Aprobado");
      }
    },
    async listo() {
      if (!this.hasGroup("AdminUFC")) {
        await Swal.fire({
          icon: "error",
          title: "Acceso denegado",
          text: "No tienes permiso para cambiar el estado a Listo.",
          confirmButtonColor: "#002a68",
        });
        return;
      }
      const result = await Swal.fire({
        title: "¿Estás seguro?",
        text: "Está seguro que desea poner a 'Listo' este informe operativo?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#002a68",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, poner a listo",
        cancelButtonText: "Cancelar",
      });

      // Si el usuario confirma, proceder con la aprobación
      if (result.isConfirmed) {
        await this.CambiarEstado("Listo");
      }
    },

    hasPermission(permission) {
      if (!this.userPermissions || !Array.isArray(this.userPermissions)) {
        console.warn("userPermissions no está disponible o no es un array");
        return false;
      }
      return this.userPermissions.some((p) => p.codename === permission);
    },

    hasGroup(group) {
      if (!this.userGroups || !Array.isArray(this.userGroups)) {
        return false;
      }
      return this.userGroups.some((g) => g.name === group);
    },

    async fetchUserPermissionsAndGroups() {
        this.loadingPermissions = true;
        try {
          const userId = localStorage.getItem("userid");
          if (userId) {
            const response = await axios.get(
              `/apiAdmin/user/${userId}/permissions-and-groups/`
            );
            
            this.userPermissions = response.data?.permissions || [];
            this.userGroups = response.data?.groups || [];
            
            // Verificar si el usuario tiene permisos para GEMAR
            const hasGemarAccess = this.userGroups.some(g => 
              ['AdminGEMAR', 'VisualizadorGEMAR', 'AdminGemar', 'VisualizadorGemar'].includes(g.name)
            );
            
            if (!hasGemarAccess) {
              this.$router.push('/unauthorized');
            }
          }
        } catch (error) {
          console.error("Error al obtener permisos:", error);
          this.userPermissions = [];
          this.userGroups = [];
        } finally {
          this.loadingPermissions = false;
        }
      },

    async CambiarEstado(NuevoEstado) {
      try {
        const existeInforme = await this.verificarInformeOperativo();

        if (!existeInforme || !this.informeOperativoId) {
          await Swal.fire({
            icon: "error",
            title: "Error",
            text: "No existe un informe de HE para la fecha actual.",
            confirmButtonColor: "#002a68",
          });
          return;
        }

        const response = await axios.patch(
          `/ufc/informe-operativo/${this.informeOperativoId}/`,
          { estado_parte: NuevoEstado },
          { headers: { "Content-Type": "application/json" } }
        );

        if (response.status === 200) {
          await Swal.fire({
            icon: "success",
            title: "Éxito",
            text: `Estado actualizado a "${NuevoEstado}" correctamente.`,
            confirmButtonColor: "#002a68",
          });
          this.$forceUpdate();
        }
      } catch (error) {
        console.error("Error al cambiar estado:", {
          url: error.config?.url,
          status: error.response?.status,
          data: error.response?.data,
        });
        await Swal.fire({
          icon: "error",
          title: "Error",
          text:
            error.response?.data?.detail || "Error al actualizar el estado.",
          confirmButtonColor: "#002a68",
        });
      }
    },   
    handleRecordStatusChange(payload) {
      this.isExistingRecord = payload.isExisting;
      // Opcional: Mostrar feedback
      console.log("Estado actualizado:", payload);
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
/* Estilos mejorados para los botones de acción */
.action-buttons {
  display: flex;
  gap: 15px;
  margin: 30px auto; /* Centrado vertical y horizontal */
  justify-content: center; /* Centra los botones horizontalmente */
  padding: 20px 0;
  width: 100%;
}

.action-btn {
  padding: 12px 25px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 120px;
}

/* Estilos específicos para cada botón */
.approve {
  background-color: #28a745;
  color: white;
}

.approve:hover {
  background-color: #218838;
}

.reject {
  background-color: #dc3545;
  color: white;
}

.reject:hover {
  background-color: #c82333;
}

.ready {
  background-color: #17a2b8;
  color: white;
}

.ready:hover {
  background-color: #138496;
}

.action-btn i {
  margin-right: 8px;
  font-size: 18px;
}

/* Estilos generales del navbar */
nav ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 15px;
  background-color: #f8f9fa; /* Fondo claro para el navbar */
  padding: 10px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Sombra suave */
}

nav ul li {
  display: inline;
}

/* Estilos base de los enlaces */
a {
  text-decoration: none;
  color: #333; /* Color de texto oscuro */
  cursor: pointer;
  padding: 10px 20px;
  border-radius: 5px;
  transition: all 0.3s ease;
  font-weight: 500;
  display: inline-block;
}

/* Estilo cuando el usuario pasa el mouse sobre el enlace */
nav a:hover {
  background-color: #e9ecef; /* Gris muy claro */
  color: #000; /* Color del texto */
  transform: translateY(-2px); /* Efecto de levantar */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Sombra más pronunciada */
}

/* Estilo para el enlace seleccionado */
nav a.active {
  background-color: #007bff; /* Azul */
  color: #fff; /* Texto blanco */
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3); /* Sombra azul */
  transform: translateY(-2px); /* Efecto de levantar */
}

/* Efecto al hacer clic */
nav a:active {
  transform: translateY(0); /* Vuelve a su posición original */
}

nav ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 10px;
}

nav ul li {
  display: inline;
}

a {
  text-decoration: none;
  color: inherit;
  cursor: pointer;
}
</style>
