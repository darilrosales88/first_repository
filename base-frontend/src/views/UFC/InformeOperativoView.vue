<template>
  <div
    style="
      background-color: #002a68;
      color: white;
      text-align: right;
      padding: 10px;
    "
  >
    <h6>Informe Operativo</h6>
  </div>Historial de cargados/descargados
  <button class="btn btn-link p-0">
          <router-link
            to="HistorialCargadoGescargado"
            title="Ver historial de vagones cargados descargados"
          >
            <i class="bi bi-plus-circle fs-3"></i>
          </router-link>
        </button>
  <br />
  <Navbar-Component /><br />
  <div style="margin-left: 17em; width: 73%">
    <Inf-Operative />    
  </div>

  <div style="margin-left: 12em">
    <h4>Transportación de las cargas</h4>
    <!-- Se centro este componente para una mejor visualizacion -->
    <div>
      <Vagones_productos />
    </div>
    <!-- Navbar con enlaces -->
    <nav>
      <ul>
        <li>
          <a
            href="#"
            @click.prevent="currentComponent = 'PorSituarCarga_Descarga'"
            :class="{ active: currentComponent === 'PorSituarCarga_Descarga' }"
          >
            Por Situar Carga/Descarga
          </a>
        </li>
        <li>
          <a
            href="#"
            @click.prevent="currentComponent = 'SituadoCarga_Descarga'"
            :class="{ active: currentComponent === 'SituadoCarga_Descarga' }"
          >
            Situado Carga/Descarga
          </a>
        </li>
        <li>
          <a
            href="#"
            @click.prevent="currentComponent = 'Cargados_Descargados'"
            :class="{ active: currentComponent === 'Cargados_Descargados' }"
          >
            Cargados
          </a>
        </li>
        <li>
          <a
            href="#"
            @click.prevent="currentComponent = 'PendientesArrastre'"
            :class="{ active: currentComponent === 'PendientesArrastre' }"
          >
            Pendientes
          </a>
        </li>
        <li>
          <a
            href="#"
            @click.prevent="currentComponent = 'EnTrenes'"
            :class="{ active: currentComponent === 'EnTrenes' }"
          >
            En Trenes
          </a>
        </li>
      </ul>
    </nav>

    <!-- Contenedor para las tablas -->
    <div>
      <component :is="currentComponent" />
    </div>
    <!-- Componente de Rotacion de vagones -->
    <ConsultaRotacionVagones />
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

.action-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

.action-btn:active {
  transform: translateY(1px);
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
a:hover {
  background-color: #e9ecef; /* Gris muy claro */
  color: #000; /* Color del texto */
  transform: translateY(-2px); /* Efecto de levantar */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Sombra más pronunciada */
}

/* Estilo para el enlace seleccionado */
a.active {
  background-color: #007bff; /* Azul */
  color: #fff; /* Texto blanco */
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3); /* Sombra azul */
  transform: translateY(-2px); /* Efecto de levantar */
}

/* Efecto al hacer clic */
a:active {
  transform: translateY(0); /* Vuelve a su posición original */
}
</style>

<style scoped>
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

<script>
import Swal from 'sweetalert2';
import axios from "axios";
import NavbarComponent from "@/components/NavbarComponent.vue";
import PorSituarCarga_Descarga from "@/components/PorSituarCarga_Descarga.vue";
import SituadoCarga_Descarga from "@/components/SituadoCarga_Descarga.vue";
import Cargados_Descargados from "@/components/Cargados_Descargados.vue";
import PendientesArrastre from "@/components/PendientesArrastre.vue";
import EnTrenes from "@/components/EnTrenes.vue";
import InfOperative from "@/components/InfOperative.vue";
import Vagones_productos from "@/components/Vagones_productos.vue";
import AdicionarVagonProducto from "@/views/UFC/AdicionarVagonesProductos.vue";
import ConsultaRotacionVagones from "@/components/RotacionVagonesView.vue";

export default {
  name: "UFCView",
  components: {
    NavbarComponent,
    PorSituarCarga_Descarga,
    SituadoCarga_Descarga,
    Cargados_Descargados,
    PendientesArrastre,
    EnTrenes,
    InfOperative,
    Vagones_productos,
    AdicionarVagonProducto,
    ConsultaRotacionVagones, 
  },
  data() {
    return {
      userPermissions: [],
      userGroups: [],
      currentComponent: "PorSituarCarga_Descarga",
      informeOperativoId: null,
      loadingPermissions: false,
    };
  },
  
  async created() {
    await this.fetchUserPermissionsAndGroups();
  },

  methods: {
    async rechazar() {      
      if (!this.hasPermission('puede_rechazar_informe')) {
        await Swal.fire({
          icon: 'error',
          title: 'Acceso denegado',
          text: 'No tienes permiso para rechazar informes operativos.',
          confirmButtonColor: '#002a68',
        });
        return;
      }      
      const result = await Swal.fire({
        title: '¿Estás seguro?',
        text: "Está seguro que desea rechazar este informe operativo?",
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#002a68',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, rechazar',
        cancelButtonText: 'Cancelar'
      });

      // Si el usuario confirma, proceder con la aprobación
      if (result.isConfirmed) {
        await this.CambiarEstado("Rechazado");
      }
    },

    async aprobar() {      
      if (!this.hasPermission('puede_aprobar_informe')) {
        await Swal.fire({
          icon: 'error',
          title: 'Acceso denegado',
          text: 'No tienes permiso para aprobar informes operativos.',
          confirmButtonColor: '#002a68',
        });
        return;
      }

      // Mostrar confirmación antes de aprobar
      const result = await Swal.fire({
        title: '¿Estás seguro?',
        text: "Está seguro que desea aprobar este informe operativo?",
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#002a68',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, aprobar',
        cancelButtonText: 'Cancelar'
      });

      // Si el usuario confirma, proceder con la aprobación
      if (result.isConfirmed) {
        await this.CambiarEstado("Aprobado");
      }
    },
    async listo() {      
      if (!this.hasPermission('puede_cambiar_a_listo')) {
        await Swal.fire({
          icon: 'error',
          title: 'Acceso denegado',
          text: 'No tienes permiso para cambiar el estado a Listo.',
          confirmButtonColor: '#002a68',
        });
        return;
      }      
      const result = await Swal.fire({
        title: '¿Estás seguro?',
        text: "Está seguro que desea poner a 'Listo' este informe operativo?",
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#002a68',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, poner a listo',
        cancelButtonText: 'Cancelar'
      });

      // Si el usuario confirma, proceder con la aprobación
      if (result.isConfirmed) {
        await this.CambiarEstado("Listo");
      }
    },

    hasPermission(permission) {
      if (!this.userPermissions || !Array.isArray(this.userPermissions)) {
        console.warn('userPermissions no está disponible o no es un array');
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
          const response = await axios.get(`/apiAdmin/user/${userId}/permissions-and-groups/`);
          
          // Verificación profunda de la respuesta
          console.log("Respuesta completa de permisos:", {
            permissions: response.data?.permissions,
            groups: response.data?.groups
          });

          this.userPermissions = response.data?.permissions || [];
          this.userGroups = response.data?.groups || [];
        }
      } catch (error) {
        console.error("Error al obtener permisos:", {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status
        });
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
            icon: 'error',
            title: 'Error',
            text: 'No existe un informe operativo para la fecha actual.',
            confirmButtonColor: '#002a68',
          });
          return;
        }

        const response = await axios.patch(
          `/ufc/informe-operativo/${this.informeOperativoId}/`, 
          { estado_parte: NuevoEstado },
          { headers: { 'Content-Type': 'application/json' } }
        );

        if (response.status === 200) {
          await Swal.fire({
            icon: 'success',
            title: 'Éxito',
            text: `Estado actualizado a "${NuevoEstado}" correctamente.`,
            confirmButtonColor: '#002a68',
          });
          this.$forceUpdate();
        }
      } catch (error) {
        console.error("Error al cambiar estado:", {
          url: error.config?.url,
          status: error.response?.status,
          data: error.response?.data
        });
        await Swal.fire({
          icon: 'error',
          title: 'Error',
          text: error.response?.data?.detail || 'Error al actualizar el estado.',
          confirmButtonColor: '#002a68',
        });
      }
    },

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
  }
};
</script>
