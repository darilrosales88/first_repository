<template>
  <div>
    <div style="background-color: #002a68; color: white; text-align: right; padding: 10px;">
      <h6>Informe Operativo</h6>
    </div>
    
    <NavbarComponent />
    
    <!-- Mostrar datos principales del informe -->
    <div style="margin-left: 17em; width: 73%">
      <InfOperativeView :informeId="informeId" />
    </div>

    <!-- Mostrar el resto de componentes relacionados -->
    <div style="margin-left: 12em">
      <h4>Transportación de las cargas</h4>
      <Vagones_productos :informeId="informeId" />
      
      <nav>
        <ul>
          <li>
            <a href="#" @click.prevent="currentComponent = 'PorSituarCarga_Descarga'" 
               :class="{ active: currentComponent === 'PorSituarCarga_Descarga' }">
              Por Situar Carga/Descarga
            </a>
          </li>
          <li>
            <a href="#" @click.prevent="currentComponent = 'SituadoCarga_Descarga'" 
               :class="{ active: currentComponent === 'SituadoCarga_Descarga' }">
              Situado Carga/Descarga
            </a>
          </li>
          <li>
            <a href="#" @click.prevent="currentComponent = 'Cargados_Descargados'" 
               :class="{ active: currentComponent === 'Cargados_Descargados' }">
              Cargados
            </a>
          </li>
          <li>
            <a href="#" @click.prevent="currentComponent = 'PendientesArrastre'" 
               :class="{ active: currentComponent === 'PendientesArrastre' }">
              Pendientes
            </a>
          </li>
          <li>
            <a href="#" @click.prevent="currentComponent = 'EnTrenes'" 
               :class="{ active: currentComponent === 'EnTrenes' }">
              En Trenes
            </a>
          </li>
        </ul>
      </nav>

      <!-- Componente dinámico -->
      <component :is="currentComponent" :informeId="informeId" />
      
      <ConsultaRotacionVagones :informeId="informeId" />
      
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
  </div>
</template>

<script>
import NavbarComponent from '@/components/NavbarComponent.vue';
import InfOperativeView from '@/components/InfOperativeView.vue';
import Vagones_productos from '@/components/Vagones_productos.vue';
import PorSituarCarga_Descarga from '@/components/PorSituarCarga_Descarga.vue';
import SituadoCarga_Descarga from '@/components/SituadoCarga_Descarga.vue';
import Cargados_Descargados from '@/components/Cargados_Descargados.vue';
import PendientesArrastre from '@/components/PendientesArrastre.vue';
import EnTrenes from '@/components/EnTrenes.vue';
import ConsultaRotacionVagones from '@/components/RotacionVagonesView.vue';
import Swal from 'sweetalert2';
import axios from 'axios';

export default {
  name: 'VisualizarInformeOperativo',
  components: {
    NavbarComponent,
    InfOperativeView,
    Vagones_productos,
    PorSituarCarga_Descarga,
    SituadoCarga_Descarga,
    Cargados_Descargados,
    PendientesArrastre,
    EnTrenes,
    ConsultaRotacionVagones
  },
  data() {
    return {
      informeId: null,
      currentComponent: 'PorSituarCarga_Descarga',
      userPermissions: [],
      userGroups: []
    };
  },
  created() {
    this.informeId = this.$route.params.id;
    this.fetchUserPermissionsAndGroups();
  },
  methods: {
    async fetchUserPermissionsAndGroups() {
      try {
        const userId = localStorage.getItem('userid');
        if (userId) {
          const response = await axios.get(`/apiAdmin/user/${userId}/permissions-and-groups/`);
          this.userPermissions = response.data.permissions;
          this.userGroups = response.data.groups;
        }
      } catch (error) {
        console.error("Error al obtener permisos y grupos:", error);
      }
    },
    hasGroup(group) {
      return this.userGroups.some(g => g.name === group);
    },
    async rechazar() {
      if (!this.hasGroup('RevisorUFC')) {
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

      if (result.isConfirmed) {
        await this.cambiarEstado("Rechazado");
      }
    },
    async aprobar() {
      if (!this.hasGroup('RevisorUFC')) {
        await Swal.fire({
          icon: "error",
          title: "Acceso denegado",
          text: "No tienes permiso para aprobar informes operativos.",
          confirmButtonColor: "#002a68",
        });
        return;
      }

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

      if (result.isConfirmed) {
        await this.cambiarEstado("Aprobado");
      }
    },
    async listo() {
      if (!this.hasGroup('AdminUFC')) {
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

      if (result.isConfirmed) {
        await this.cambiarEstado("Listo");
      }
    },
    async cambiarEstado(nuevoEstado) {
      try {
        const userId = localStorage.getItem('userid');
        const response = await axios.patch(
          `/ufc/informe-operativo/${this.informeId}/`,
          { 
            estado_parte: nuevoEstado,
            aprobado_por: nuevoEstado === "Aprobado" ? userId : null
          }
        );

        if (response.status === 200) {
          await Swal.fire({
            icon: "success",
            title: "Éxito",
            text: `Estado actualizado a "${nuevoEstado}" correctamente.`,
            confirmButtonColor: "#002a68",
          });
        }
      } catch (error) {
        console.error("Error al cambiar estado:", error);
        await Swal.fire({
          icon: "error",
          title: "Error",
          text: error.response?.data?.detail || "Error al actualizar el estado.",
          confirmButtonColor: "#002a68",
        });
      }
    }
  }
};
</script>

<style scoped>
/* Tus estilos existentes */
</style>