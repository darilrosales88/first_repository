<template>
    <div style="background-color: #002a68; color: white; text-align: right; padding: 10px;">
      <h6>CCDxProducto</h6>
    </div>
    <NavbarComponent />
    <div style="margin-left: 25em; width: 60%">
      <div class="container py-3">
        <div class="card border">
          <div class="card-header bg-light border-bottom">
            <h6 class="mb-0 text-dark fw-semibold">
              <i class="bi bi-clipboard-data me-2"></i>Fechas de operaciones - CCDxProducto
            </h6>
          </div>

          <div class="card-body p-3">
            <form @submit.prevent="submitForm">
              <div class="row mb-3 g-2">
                <div class="col-md-6">
                  <div class="form-group">
                    <label for="fechaActual" class="form-label small fw-semibold text-secondary">
                      <i class="bi bi-calendar-check me-2 text-primary"></i>Fecha
                      Actual
                    </label>
                    <input type="date"
                      class="form-control form-control-sm border-secondary"
                      id="fechaActual"
                      v-model="formData.fecha_actual"
                      required
                      :disabled="isExistingRecord"/>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="form-group">
                    <label for="fechaOperacion" class="form-label small fw-semibold text-secondary">
                      <i class="bi bi-calendar-check me-2 text-primary"></i>Fecha
                      Operación
                    </label>
                    <input
                      type="date"
                      class="form-control form-control-sm border-secondary"
                      id="FechaOperacion"
                      v-model="formData.fecha_operacion"
                      required
                      :disabled="isExistingRecord"/>
                  </div>
                </div>
                <div class="mb-3">
                  <label for="observaciones" class="form-label small fw-semibold text-secondary">
                    Observaciones
                  </label>
                  <textarea class="form-control form-control-sm border-secondary" v-model="formData.observaciones" rows="3"></textarea>
                </div>
              </div>

              <div class="d-flex justify-content-end gap-2 mt-4">
                <button
                  type="submit"
                  class="btn btn-primary"
                  @click="crearInforme"
                  :disabled="isExistingRecord">
                  <i class="bi bi-save me-2"></i>Crear 
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div style="margin-left: 16em; width: 80%">
      <TableCasillas/> 
    </div>
    <div style="margin-left: 16em; width: 80%">
        <nav>
            <ul>
                <li><a href="#" @click.prevent="currentComponent = 'TablePorSituar'" :class="{ active: currentComponent === 'TablePorSituar' }">Por Situar Carga/Descarga</a></li>
                <li><a href="#" @click.prevent="currentComponent = 'TableSituados'" :class="{ active: currentComponent === 'TableSituados' }">Situado Carga/Descarga</a></li>
                <li><a href="#" @click.prevent="currentComponent = 'TableCargaDescarga'" :class="{ active: currentComponent === 'TableCargaDescarga' }">Cargados/Descargados</a></li>
                <li><a href="#" @click.prevent="currentComponent = 'TablePendienteArrastre'" :class="{ active: currentComponent === 'TablePendienteArrastre' }">Pendientes</a></li>
                <li><a href="#" @click.prevent="currentComponent = 'TableEnTren'":class="{ active: currentComponent === 'TableEnTren' }">En Trenes</a></li>
            </ul>
        </nav>

        <div><component :is="currentComponent"/></div> 
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
import axios from "axios";
import Swal from "sweetalert2";
import NavbarComponent from "@/components/NavbarComponent.vue";
import TableCasillas from "@/components/CCDxProductosComponents/TableCasillas.vue";
import TablePorSituar from "@/components/CCDxProductosComponents/TablePorSituar.vue";
import TableSituados from "@/components/CCDxProductosComponents/TableSituados.vue";
import TableCargaDescarga from "@/components/CCDxProductosComponents/TableCargaDescarga.vue";
import TablePendienteArrastre from "@/components/CCDxProductosComponents/TablePendienteArrastre.vue";
import TableEnTren from "@/components/CCDxProductosComponents/TableEnTren.vue";


export default {
  name: "CCDxProductoView",

  components: {
    NavbarComponent,
    TableCasillas,
    TablePorSituar,
    TableSituados,
    TableCargaDescarga,
    TablePendienteArrastre,
    TableEnTren,
  },
  data() {
    const now = new Date();
    const offset = now.getTimezoneOffset() * 60000; // offset en milisegundos
    const localISOTime = new Date(now - offset).toISOString().split("T")[0];
    return {
        formData: {
            fecha_actual: localISOTime,
            fecha_operacion: localISOTime,
            observaciones: '',
            provincia: null,
            creado_por: null,
            aprobado_por: null,
        },
        userGroups: [],
        userPermissions: [],
        isExistingRecord: false,
        informeCCDxProductoId: null,
        currentComponent: "TablePorSituar",
    };
  },
  methods: {

    async fetchUserPermissionsAndGroups() {
      try {
        const userId = localStorage.getItem("userid");
        if (userId) {
          const response = await axios.get(`/apiAdmin/user/${userId}/permissions-and-groups/`);
          this.userPermissions = response.data?.permissions || [];
          this.userGroups = response.data?.groups || [];
        }
      } catch (error) {
        console.error("Error al obtener permisos:", {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status,
        });
        this.userPermissions = [];
        this.userGroups = [];
      }
    },

    hasPermission(permission) {
      if (!this.userPermissions || !Array.isArray(this.userPermissions)) {
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

    async obtenerUsername() {
      try {
        const userId = localStorage.getItem("userid");
        if (userId) {
          const response = await axios.get(`/apiAdmin/users/${userId}/`);
          this.formData.creado_por = response.data.id;
          this.formData.provincia = response.data.provincia.id;
        }
      } catch (error) {
        console.error("Error al obtener Nombre de Usuario:", error);
      }
    },

    async verificarInformeCCDxProducto() {
      try {
        const today = new Date();
        const fechaFormateada = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;
        const response = await axios.get("/ufc/verificar-informe-ccd-existente/", {params: { fecha_operacion: fechaFormateada },});
        if (response.data.existe) {
          this.informeCCDxProductoId = response.data.id;
          this.isExistingRecord = true;
          console.log(response);
          return true;
          
          //this.deleteInforme(response.data.id)
        } else {
          this.informeCCDxProductoId = null;
          this.isExistingRecord = false;
          this.showErrorToast("No existe un informe para la fecha actual.");
        }
        return false;
      } catch (error) {
        console.error("Error al verificar informe:", error);
        return false;
      }
    },

    async submitForm() {
      try {
        const dataToSend = {
          creado_por: this.formData.creado_por,
        };

        const response = await axios.post("/ufc/ccd-informe/",dataToSend);
        this.informeOperativoId = response.data.id;
        this.isExistingRecord = true;
        this.showSuccessToast("Informe creado");
      } catch (error) {
        console.error("Error al guardar operación:", error);
        this.showErrorToast("Error al crear el informe");
      }
    },

    async deleteInforme(id) {
      try {
        await axios.delete(`/ufc/ccd-informe/${id}/`);
        this.showSuccessToast("Informe eliminado");
      } catch (error) {
        console.error("Error al eliminar el informe:", error);
        this.showErrorToast("Error al eliminar el informe");
      }
    },

    async rechazar() {
      if (!this.hasGroup("RevisorUFC")) {
        this.showErrorToast("No tienes permiso para rechazar informes operativos");
        return;
      }
      const result = await Swal.fire({
        title: "¿Estás seguro?",
        text: "Está seguro que desea rechazar este informe operativo?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#002a68",
        cancelButtonColor: "#d33",
        confirmButtonText: "Continuar",
        cancelButtonText: "Cancelar",
      });

      if (result.isConfirmed) {
        await this.CambiarEstado("rechazado");
      }
    },

    async aprobar() {
      if (!this.hasGroup("RevisorUFC")) {
        this.showErrorToast("No tienes permiso para aprobar informes operativos");
        return;
      }

      const result = await Swal.fire({
        title: "¿Estás seguro?",
        text: "Está seguro que desea aprobar este informe operativo?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#002a68",
        cancelButtonColor: "#d33",
        confirmButtonText: "Continuar",
        cancelButtonText: "Cancelar",
      });
      
      if (result.isConfirmed) {
        await this.CambiarEstado("aprobado");
      }
    },

    async listo() {
      if (!this.hasGroup("AdminUFC")) {
        this.showErrorToast("No tienes permiso para cambiar a 'Listo' operativos");
        return;
      }
      const result = await Swal.fire({
        title: "¿Estás seguro?",
        text: "Está seguro que desea poner a 'Listo' este informe operativo?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#002a68",
        cancelButtonColor: "#d33",
        confirmButtonText: "Continuar",
        cancelButtonText: "Cancelar",
      });

      if (result.isConfirmed) {
        await this.CambiarEstado("listo");
      }
    },

    async CambiarEstado(NuevoEstado) {
      try {
        const existeInforme = await this.verificarInformeCCDxProducto;
        if (!existeInforme || !this.informeCCDxProductoId) {
          this.showErrorToast("No existe un informe operativo para la fecha actual");
          return;
        }
        const response = await axios.patch(`/ufc/ccd-informe/${this.informeCCDxProductoId}/`,
          { estado_parte: NuevoEstado },
          { headers: { "Content-Type": "application/json" } }
        );
        this.showSuccessToast(`Informe "${NuevoEstado}"`);
      } catch (error) {
        this.showErrorToast("Error al cambiar el estado");
        console.error(error);
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
  async created() {
    await this.obtenerUsername();
    await this.fetchUserPermissionsAndGroups();
    await this.verificarInformeCCDxProducto();
    
  },
};
</script>

<style scoped>

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
