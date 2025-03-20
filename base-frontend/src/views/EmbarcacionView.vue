<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido: </h6>
    </div>  
    <br />
    <Navbar-Component />
    <br />
    <br />

    <div class="search-container">
      <form class="d-flex search-form" @submit.prevent="searchEmbarcacion">
        <div class="input-container">
          <i class="bi bi-search"></i>
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="Nombre, tipo o nacionalidad"
          aria-label="Buscar"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px; padding-left: 5px;margin-top: -70px;" 
        />
      </div>
      </form>
    </div>

    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="/AdicionarEmbarcacion">
      <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h3 style="margin-top: -33px; font-size: 18px;
    margin-right: 560px;color: #002A68;">Listado de embarcaciones</h3>
    <br />
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Nombre</th>
            <th scope="col">Nacionalidad</th>
            <th scope="col">Eslora</th>
            <th scope="col" >Manga</th>
            <th scope="col" >Calado máximo</th>
            <th scope="col" >Desplazamiento máximo</th>
            <th scope="col">Tipo de embarcación</th>
            <th scope="col">Tipo de buque</th>
            <th scope="col" >Tipo de patana</th>
            <th scope="col" >IMO</th>
            <th scope="col" >Potencia</th>
            <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item) in embarcacionesFiltradas" :key="item.id">
            <td>{{ item.nombre_embarcacion }}</td>
            <td>{{ item.nacionalidad_name }}</td>
            <td >{{ item.eslora }}</td>
            <td >{{ item.manga }}</td>
            <td >{{ item.calado_maximo }}</td>
            <td >{{ item.desplazamiento_maximo }}</td>
            <td>{{ getTipoEmbarcacionText(item.tipo_embarcacion) }}</td>
            <td>{{ getTipoBuqueText(item.tipo_buque) }}</td>
            <td >{{ getTipoPatanaText(item.tipo_patana) }}</td>
            <td >{{ item.imo }}</td>
            <td >{{ item.potencia }}</td>
            <td>
              <button @click="openEmbarcacionDetailsModal(item)" class="btn btn-info btn-small btn-eye" 
              v-html="showNoId ? '<i class=\'bi bi-eye-slash-fill\'></i>' : '<i class=\'bi bi-eye-fill\'></i>'">
              </button>
              <span v-if="hasGroup('Admin')">
                <button  class="btn btn-warning btn-small">
                <router-link :to="{name: 'EditarEmbarcacion', params: {id: item.id}}">
                  <i style="color:black" class="bi bi-pencil-square"></i>
                </router-link>
              </button>
              <button  @click.prevent="confirmDelete(item.id)" class="btn btn-danger btn-small">
                <i s class="bi bi-trash"></i>
              </button>
            </span>
            </td>
          </tr>
        </tbody>
      </table>
    <!-- Mensaje cuando no hay resultados -->
    <h1 v-if="embarcacionesFiltradas.length === 0 && searchQuery">
      No existe ningún registro asociado a ese parámetro de búsqueda.
    </h1>
  </div>
  
  </div>
</template>

<script>
import Swal from 'sweetalert2';
import axios from 'axios';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'EmbarcacionView',
  components: {
    NavbarComponent,
  },
  data() {
    return {
      embarcaciones: [], // Lista completa de embarcaciones
      embarcacionesFiltradas: [], // Lista filtrada de embarcaciones
      searchQuery: '', // Término de búsqueda
      debounceTimeout: null, // Timeout para el debounce
      userPermissions: [], // Permisos del usuario
      userGroups: [], // Grupos del usuario
      currentPage: 1,
      totalPages: 1,
      pages: [],
    };
  },
  async created() {
    await this.fetchUserPermissionsAndGroups();
    await this.getEmbarcaciones();
  },
  methods: {
    toggleNoIdVisibility() {
      this.showNoId = !this.showNoId; // Alternar la visibilidad de las columnas No e Id
    },
    // Verifica si el usuario tiene un permiso específico
    hasPermission(permission) {
      return this.userPermissions.some(p => p.name === permission);
    },
    // Verifica si el usuario pertenece a un grupo específico
    hasGroup(group) {
      return this.userGroups.some(g => g.name === group);
    },
    // Obtiene los permisos y grupos del usuario
    async fetchUserPermissionsAndGroups() {
      try {
        const userId = localStorage.getItem('userid');
        if (userId) {
          const response = await axios.get(`/apiAdmin/user/${userId}/permissions-and-groups/`);
          this.userPermissions = response.data.permissions;
          this.userGroups = response.data.groups;
        }
      } catch (error) {
        console.error('Error al obtener permisos y grupos:', error);
      }
    },
    // Obtiene todas las embarcaciones
    async getEmbarcaciones() {
      try {
        const response = await axios.get('/api/embarcaciones/');
        this.embarcaciones = response.data;
        this.embarcacionesFiltradas = this.embarcaciones; // Inicialmente, muestra todas las embarcaciones
      } catch (error) {
        console.error('Error al obtener las embarcaciones:', error);
        Swal.fire('Error', 'No se pudieron cargar las embarcaciones.', 'error');
      }
    },
    // Filtra las embarcaciones según el término de búsqueda
    searchEmbarcacion() {
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        this.embarcacionesFiltradas = this.embarcaciones.filter(
          (embarcacion) =>
            embarcacion.nombre_embarcacion.toLowerCase().includes(query) ||
            embarcacion.tipo_embarcacion_name.toLowerCase().includes(query) ||
            embarcacion.nacionalidad_name.toLowerCase().includes(query)
        );
      } else {
        this.embarcacionesFiltradas = this.embarcaciones; // Si no hay búsqueda, muestra todas
      }
    },
    // Debounce para evitar múltiples llamadas durante la escritura
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchEmbarcacion();
      }, 300);
    },
    // Confirma la eliminación de una embarcación
    confirmDelete(id) {
      Swal.fire({
        title: '¿Estás seguro?',
        text: '¡No podrás revertir esta acción!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
        reverseButtons: true,
      }).then((result) => {
        if (result.isConfirmed) {
          this.deleteEmbarcacion(id);
        }
      });
    },
    // Elimina una embarcación
    async deleteEmbarcacion(id) {
      try {
        await axios.delete(`/api/embarcaciones/${id}/`);
        this.embarcaciones = this.embarcaciones.filter(embarcacion => embarcacion.id !== id);
        this.embarcacionesFiltradas = this.embarcacionesFiltradas.filter(embarcacion => embarcacion.id !== id);
        Swal.fire('Eliminado!', 'La embarcación ha sido eliminada exitosamente.', 'success');
      } catch (error) {
        console.error('Error al eliminar la embarcación:', error);
        Swal.fire('Error', 'Hubo un error al eliminar la embarcación.', 'error');
      }
    },
    // Obtiene el texto asociado al valor del tipo de embarcación
    getTipoEmbarcacionText(value) {
      const tipos_embarcaciones = {
        buque: 'Buque',
        remolcador: 'Remolcador',
        patana: 'Patana',
        otros: 'Otros',
      };
      return tipos_embarcaciones[value] || 'Desconocido';
    },
    // Obtiene el texto asociado al valor del tipo de buque
    getTipoBuqueText(value) {
      const tipos_buques = {
        buque_carga_gral: 'Buque de carga general',
        buque_granelero: 'Buque granelero',
        buque_ro_ro: 'Buque Ro Ro',
        buque_frig: 'Buque frigorífico',
        buque_tanque: 'Buque tanque',
        buque_gases: 'Buque de gases',
      };
      return tipos_buques[value] || 'Desconocido';
    },
    // Obtiene el texto asociado al valor del tipo de patana
    getTipoPatanaText(value) {
      const tipos_patanas = {
        pat_carga_seca: 'Patana de carga seca',
        pat_carga_liquida: 'Patana de carga líquida',
        patana_comb: 'Patana de combustible',
        patana_ro_ro: 'Patana Ro Ro',
      };
      return tipos_patanas[value] || 'Desconocido';
    },
    openEmbarcacionDetailsModal(Embarcacion) {
    // Mapear IDs de grupos a nombres
    const gruposAsignados = Embarcacion.groups && Embarcacion.groups.length > 0
        ? Embarcacion.groups
            .map(groupId => {
                const grupo = this.gruposDisponibles.find(g => g.id === groupId);
                return grupo ? grupo.name : 'Desconocido';
            })
            .join(', ')
        : 'Ninguno';

    // Mapear IDs de permisos a nombres
    const permisosAsignados = Embarcacion.Embarcacion_permissions && Embarcacion.Embarcacion_permissions.length > 0
        ? Embarcacion.Embarcacion_permissions
            .map(permisoId => {
                const permiso = this.permisosDisponibles.find(p => p.id === permisoId);
                return permiso ? permiso.name : 'Desconocido';
            })
            .join(', ')
        : 'Ninguno';

    Swal.fire({
        title: 'Detalles de la Embarcacion',
        html: `
            <div style="text-align: left;">
                <p><strong>Nombre:</strong> ${Embarcacion.nombre_embarcacion}</p>
                <p><strong>Nacionalidad:</strong> ${Embarcacion.nacionalidad_name}</p>
                <p><strong>Eslora:</strong> ${Embarcacion.eslora}</p>
                 <p><strong>Manga:</strong> ${Embarcacion.manga}</p>
                <p><strong>Calado máximo:</strong> ${Embarcacion.calado_maximo}</p>
                <p><strong>Desplazamiento maximo:</strong> ${Embarcacion.desplazamiento_maximo}</p>
                 <p><strong>Tipo de Embarcacion:</strong> ${Embarcacion.tipo_embarcacion}</p>
                <p><strong>Tipo de buque:</strong> ${Embarcacion.tipo_buque}</p>
                <p><strong>Tipo de Patana:</strong> ${Embarcacion.tipo_patana}</p>
                <p><strong>IMO:</strong> ${Embarcacion.imo}</p>
                <p><strong>Potencia:</strong> ${Embarcacion.potencia}</p>
                
            </div>
        `,
        width: '600px',
        customClass: {
            popup: 'custom-swal-popup',
            title: 'custom-swal-title',
            htmlContainer: 'custom-swal-html',
        },
    });
},
  },
};
</script>

<style scoped>
.search-container input::placeholder {
  font-size: 14px; 
  color: #999;   
}

body {
  overflow: scroll;
}

.search-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 5px;
}

.table-container {
  overflow-x: auto;
  max-width: 100%;
}
.input-container {
  position: relative;
  display: inline-block;
}

.input-container .bi {
  position: absolute;
  left: 180px;
  color: #999;
  margin-top: -55px;
  transform: translateY(-50%);
  pointer-events: none; /* Para que el ícono no interfiera con el clic en el input */
}
.large-icon {
  font-size: 1.7rem; /* Tamaño del ícono */
}
table {
  width: 84%;
  border-collapse: collapse;
  margin-left: 190px;
  margin-bottom: 10px;
  font-size: 0.875rem;
}

th, td {
  padding: 0.15rem; /* Reducir el padding */
  white-space: nowrap;
}


th {
  background-color: #f2f2f2;
}

.btn {
  cursor: pointer;
}

.btn-small {
  font-size: 22px; /* Aumenta el tamaño del ícono */
  color: black;
  margin-right: 5px;
  outline: none; /* Elimina el borde de foco */
  border: none;
  background: none; /* Elimina el fondo */
  padding: 0; /* Elimina el padding para que solo se vea el ícono */
}
.btn-eye {
  font-size: 22px; /* Aumenta el tamaño del ícono */
  margin-right: 5px;
  outline: none; /* Elimina el borde de foco */
  border: none;
  background: none; /* Elimina el fondo */
  padding: 0; /* Elimina el padding para que solo se vea el ícono */
}
.btn:hover {
  background: none; /* Asegura que no haya fondo al hacer hover */
}

.btn:focus {
  outline: none; /* Elimina el borde de foco al hacer clic */
  box-shadow: none; /* Elimina cualquier sombra de foco en algunos navegadores */
}

.create-button-container {
  margin-top: -80px;
  text-align: left;
}

.create-button {
  text-decoration: none;
  color: green;
  margin-left: 940px;
}

@media (max-width: 768px) {
  .create-button-container {
    text-align: left;
    margin-right: 0;
  }
}
</style>