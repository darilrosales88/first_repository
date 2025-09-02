<template>
  <div style="margin-left: 16.5em; width: 79%">
    <div style="background-color: #002a68; color: white; text-align: right; padding: 10px;">
      <h6>Detalle de Parte Combinado</h6>
    </div>

    <Navbar-Component /><br />

    <div class="container py-3">
      <div class="card border">
        <div class="card-header bg-light border-bottom d-flex justify-content-between align-items-center">
          <h6 class="mb-0 text-dark fw-semibold">
            <i class="bi bi-clipboard-data me-2"></i>Detalle del Parte
          </h6>
          <button class="btn btn-sm btn-outline-secondary" @click="$router.go(-1)">
            <i class="bi bi-arrow-left me-1"></i> Volver
          </button>
        </div>

        <div class="card-body p-3">
          <!-- Aquí mostrarías los detalles específicos del parte -->
          <div v-if="loading" class="text-center">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Cargando...</span>
            </div>
          </div>
          
          <div v-else-if="parte">
            <!-- Información del parte -->
            <div class="row mb-3">
              <div class="col-md-4">
                <strong>Tipo:</strong> {{ getTipoParte(parte.tipo_parte) }}
              </div>
              <div class="col-md-4">
                <strong>Fecha:</strong> {{ formatDateTime(parte.fecha_actual) }}
              </div>
              <div class="col-md-4">
                <strong>Estado:</strong> 
                <span :class="'status-' + getStatusClass(parte.estado_parte)">
                  {{ parte.estado_parte }}
                </span>
              </div>
            </div>
            
            <!-- Más detalles según el tipo de parte -->
            
            <!-- Botones de acción -->
            <div class="d-flex justify-content-end gap-2 mt-4">
              <!-- Solo mostrar para estados editables -->
              <button v-if="parte.estado_parte === 'creado' && hasGroup('AdminGEMAR')" 
                      @click="editarParte" 
                      class="btn btn-sm btn-outline-primary">
                <i class="bi bi-pencil me-1"></i> Editar
              </button>
              
              <button v-if="parte.estado_parte === 'creado' && hasGroup('AdminGEMAR')" 
                      @click="eliminarParte" 
                      class="btn btn-sm btn-outline-danger">
                <i class="bi bi-trash me-1"></i> Eliminar
              </button>
              
              <button v-if="hasGroup('RevisorGEMAR')" 
                      @click="aprobarParte" 
                      class="btn btn-sm btn-outline-success">
                <i class="bi bi-check-circle me-1"></i> Aprobar
              </button>
              
              <button v-if="hasGroup('RevisorGEMAR')" 
                      @click="rechazarParte" 
                      class="btn btn-sm btn-outline-warning">
                <i class="bi bi-x-circle me-1"></i> Rechazar
              </button>
              
              <button v-if="hasGroup('AdminGEMAR')" 
                      @click="marcarListo" 
                      class="btn btn-sm btn-outline-info">
                <i class="bi bi-check-all me-1"></i> Listo
              </button>
            </div>
          </div>
          
          <div v-else class="text-center text-muted">
            <i class="bi bi-exclamation-circle fs-4"></i>
            <p class="mt-2">No se pudo cargar la información del parte</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "DetalleParteCombinado",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      parte: null,
      loading: true,
      userGroups: [],
    };
  },
  async created() {
    await this.fetchUserGroups();
    await this.cargarDetalleParte();
  },
  methods: {
    async fetchUserGroups() {
      try {
        const userId = localStorage.getItem("userid");
        if (userId) {
          const response = await axios.get(`/apiAdmin/user/${userId}/permissions-and-groups/`);
          this.userGroups = response.data.groups || [];
        }
      } catch (error) {
        console.error("Error al obtener grupos de usuario:", error);
        this.userGroups = [];
      }
    },
    
    hasGroup(groupName) {
      return this.userGroups.some(group => group.name === groupName);
    },
    
    async cargarDetalleParte() {
      try {
        const parteId = this.$route.params.id;
        
        if (!parteId) {
          throw new Error("ID del parte no válido");
        }

        // Usar el nuevo endpoint de detalle
       const response = await axios.get(`/gemar/gemar-partes-combinados/${parteId}/detalle_parte`);
        this.parte = response.data;
        
      } catch (error) {
        console.error("Error al cargar detalle del parte:", error);
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "No se pudo cargar la información del parte",
          confirmButtonColor: "#002a68",
        }).then(() => {
          this.$router.go(-1);
        });
      } finally {
        this.loading = false;
      }
    },

    async cambiarEstado(nuevoEstado) {
      try {
        const response = await axios.patch(
          `/gemar-partes-combinados/${this.$route.params.id}/actualizar-estado/`,
          { estado_parte: nuevoEstado }
        );
        
        if (response.status === 200) {
          this.parte.estado_parte = nuevoEstado;
          Swal.fire({
            icon: "success",
            title: "Éxito",
            text: `Estado cambiado a "${nuevoEstado}" correctamente`,
            confirmButtonColor: "#002a68",
          });
        }
      } catch (error) {
        console.error("Error al cambiar estado:", error);
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "No se pudo cambiar el estado del parte",
          confirmButtonColor: "#002a68",
        });
      }
    },

    async aprobarParte() {
      const result = await Swal.fire({
        title: "¿Estás seguro?",
        text: "¿Desea aprobar este parte?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#002a68",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, aprobar",
        cancelButtonText: "Cancelar",
      });

      if (result.isConfirmed) {
        await this.cambiarEstado("aprobado");
      }
    },
    
    async rechazarParte() {
      const result = await Swal.fire({
        title: "¿Estás seguro?",
        text: "¿Desea rechazar este parte?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#002a68",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, rechazar",
        cancelButtonText: "Cancelar",
      });

      if (result.isConfirmed) {
        await this.cambiarEstado("rechazado");
      }
    },
    
    async marcarListo() {
      const result = await Swal.fire({
        title: "¿Estás seguro?",
        text: "¿Desea marcar este parte como listo?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#002a68",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, marcar como listo",
        cancelButtonText: "Cancelar",
      });

      if (result.isConfirmed) {
        await this.cambiarEstado("listo");
      }
    },

    async eliminarParte() {
      const result = await Swal.fire({
        title: "¿Estás seguro?",
        text: "Esta acción no se puede deshacer",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
      });

      if (result.isConfirmed) {
        try {
          await axios.delete(`/gemar-partes-combinados/${this.$route.params.id}/eliminar/`);
          Swal.fire({
            icon: "success",
            title: "Éxito",
            text: "Parte eliminado correctamente",
            confirmButtonColor: "#002a68",
          });
          this.$router.go(-1);
        } catch (error) {
          console.error("Error al eliminar parte:", error);
          Swal.fire({
            icon: "error",
            title: "Error",
            text: error.response?.data?.error || "No se pudo eliminar el parte",
            confirmButtonColor: "#002a68",
          });
        }
      }
    },
    
    editarParte() {
      // Redirigir a la vista de edición según el tipo de parte
      const tipo = this.parte.tipo_parte;
      if (tipo === 'HECHO_EXTRAORDINARIO') {
        this.$router.push(`/gemar/hechos-extraordinarios/editar/${this.parte.id}`);
      } else if (tipo === 'EXISTENCIA_MERCANCIA') {
        this.$router.push(`/gemar/existencias-mercancia/editar/${this.parte.id}`);
      } else if (tipo === 'PBIP') {
        this.$router.push(`/gemar/partes-pbip/editar/${this.parte.id}`);
      } else if (tipo === 'PROGRAMACION_MANIOBRAS') {
        this.$router.push(`/gemar/programacion-maniobras/editar/${this.parte.id}`);
      } else {
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "Tipo de parte no reconocido para edición",
          confirmButtonColor: "#002a68",
        });
      }
    },
    
    getTipoParte(tipo) {
      const tipos = {
        'HECHO_EXTRAORDINARIO': 'Hecho Extraordinario',
        'PROGRAMACION_MANIOBRAS': 'Programación Maniobras',
        'PBIP': 'PBIP',
        'EXISTENCIA_MERCANCIA': 'Existencia Mercancía'
      };
      return tipos[tipo] || tipo;
    },
    
    getStatusClass(status) {
      if (!status) return 'default';
      
      const statusLower = status.toLowerCase();
      if (statusLower.includes('aprobado')) return 'success';
      if (statusLower.includes('pendiente') || statusLower.includes('creado')) return 'warning';
      if (statusLower.includes('rechazado') || statusLower.includes('cancelado')) return 'danger';
      if (statusLower.includes('listo')) return 'info';
      return 'default';
    },
    
    formatDateTime(dateTime) {
      if (!dateTime) return '-';
      const date = new Date(dateTime + 'Z');
      return date.toLocaleDateString('es-ES', { 
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone 
      });
    },

    volverAtras() {
      this.$router.go(-1);
    }
  },
};
</script>

<style scoped>
/* Estilos para estados */
.status-success {
  background-color: rgba(40, 167, 69, 0.1);
  color: #28a745;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-warning {
  background-color: rgba(255, 193, 7, 0.1);
  color: #ffc107;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-danger {
  background-color: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-info {
  background-color: rgba(23, 162, 184, 0.1);
  color: #17a2b8;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-default {
  background-color: rgba(108, 117, 125, 0.1);
  color: #6c757d;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}
</style>