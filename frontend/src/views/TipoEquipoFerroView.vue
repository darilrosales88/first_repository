<template>
  <div>
    <div style=" background-color: #003366; color: white; text-align: right;">
      <h6>Bienvenido: </h6>
    </div>  
    <br />
    <Navbar-Component />
    <br />
    <br />
<div class="search-container">
      <form class="d-flex search-form" @submit.prevent="search_tipo_equipo">
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder=" tipo de carga"
          aria-label="Buscar"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px;"
        />
      </form>
    </div>
    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="AdicionarTipoEquipo">
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h6 style="margin-top: -31px; font-size: 19px;
    margin-right: 440px;">Listado de tipos de equipos ferroviarios:</h6>
    <br />
    <div class="table-container">
<table class="table">
<thead>
  <tr>
    <th scope="col" v-if="showNoId">No</th>
    <th scope="col">Tipo de equipo</th>
    <th scope="col">Tipo de carga</th>
    <th scope="col" v-if="showNoId">Tipo de combustible</th>
    <th scope="col" v-if="showNoId">Longitud</th>
    <th scope="col" v-if="showNoId">Peso neto sin carga</th>
    <th scope="col" v-if="showNoId">Peso máximo con carga</th>
    <th scope="col" v-if="showNoId">Capacidad cúbica máxima</th>
    <th scope="col">Descripción</th>
    <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
  </tr>
</thead>
<tbody>
  <tr v-for="(item, index) in tipos_equipos" :key="item.id">
    <th v-if="showNoId" scope="row" style="background-color: white;">{{ (index + 1) }}</th>
    <td>{{ getTipoEquipoText(item.tipo_equipo) }}</td>
    <td>{{ getTipoCargaText( item.tipo_carga) }}</td>
    <td v-if="showNoId">{{ getTipoCombustibleText(item.tipo_combustible )}}</td>
    <td v-if="showNoId">{{ item.longitud }}</td>
    <td v-if="showNoId">{{ item.peso_neto_sin_carga }}</td>
    <td v-if="showNoId">{{ item.peso_maximo_con_carga }}</td>
    <td v-if="showNoId">{{ item.capacidad_cubica_maxima }}</td>
    <td>{{ item.descripcion }}</td>
    <td >
              <button @click="toggleNoIdVisibility" class="btn btn-info btn-small btn-eye" 
              v-html="showNoId ? '<i class=\'bi bi-eye-slash-fill\'></i>' : '<i class=\'bi bi-eye-fill\'></i>'">
              </button>
              <span v-if="hasGroup('Admin')">
                <button class="btn btn-warning btn-small">
                  <router-link :to="{name: 'EditarTipoEquipoFerro', params: {id:item.id}}">
                    <i style="color:white" class="bi bi-pencil-square"></i>
                  </router-link>
                </button>
                <button style="margin-left:10px" @click.prevent="confirmDelete(item.id)" class="btn btn-danger btn-small">
                  <i style="color:white" class="bi bi-trash"></i>
                </button>
              </span>
            </td>
  </tr>
</tbody>
</table>
<h1 v-if="!busqueda_existente">No existe ningún registro asociado a ese parámetro de búsqueda.</h1>
</div>
</div>
</template>

<style scoped>

.search-container input::placeholder {
  font-size: 12px; 
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
.large-icon {
  font-size: 1.7rem; /* Tamaño del ícono */
}
table {
  width: 84%;
  border-collapse: collapse;
  margin-left: 190px;
  margin-bottom: 20px;
  font-size: 0.875rem;
  min-width: 300px;
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
  font-weight: bold;
}

.btn-small {
  padding: 0.25rem 0.45rem;
  font-size: 0.875rem;
}
.btn-eye {
  background-color: rgb(0, 71, 163);
  margin-right: 10px;
  color: white;
  border: none;
}

.create-button-container {
  margin-top: -40px;
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


<script>
import Swal from 'sweetalert2';
import axios from 'axios';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'TipoEquipoFerro',

  components: {
    NavbarComponent,
  },

  data() {
    return {
      tipos_equipos: [],
      searchQuery: '', // Añadido aquí
      debounceTimeout: null, // Añadido aquí
      busqueda_existente: true, // Variable para controlar la visibilidad del <h1> de la busqueda
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [],      // Almacenará los grupos del usuario
      showNoId: false,
    };
  },

  mounted() {
    this.get_tipos_equipos();
  },

  async created() {
    // Obtener los permisos y grupos del usuario al cargar el componente
    await this.fetchUserPermissionsAndGroups();
  },

  methods: {
    toggleNoIdVisibility() {
      this.showNoId = !this.showNoId; // Alternar la visibilidad de las columnas No e Id
    },
    // Verifica si el usuario tiene un permiso específico
    hasPermission(permission) {
      if (!this.userPermissions) return false; // Verificación adicional
      return this.userPermissions.some(p => p.name === permission);
    },
    hasGroup(group) {
      if (!this.userGroups) return false; // Verificación adicional
      return this.userGroups.some(g => g.name === group);
    },
    // Obtiene los permisos y grupos del usuario desde el backend
    async fetchUserPermissionsAndGroups() {
      try {
        const userId = localStorage.getItem('userid');
        if (userId) {
          const response = await axios.get(`/apiAdmin/user/${userId}/permissions-and-groups/`);
          this.userPermissions = response.data.permissions || []; // Inicializa como array vacío si es undefined
          this.userGroups = response.data.groups || []; // Inicializa como array vacío si es undefined
        }
      } catch (error) {
        console.error('Error al obtener permisos y grupos:', error);
      }
    },
    async get_tipos_equipos() {
      this.$store.commit('setIsLoading', true);

      axios
        .get('/api/tipos_equipos/')
        .then(response => {
          this.tipos_equipos = response.data;          
        })
        .catch(error => {
          console.log(error);
        });

      this.$store.commit('setIsLoading', false);
    },
    // Método para buscar registros en base al parámetro de búsqueda
    async search_tipo_equipo() {
      this.$store.commit('setIsLoading', true);

      axios
        .get(`/api/tipos_equipos/?busqueda_tipo_equipo__tipo_carga=${this.searchQuery}`)
        .then(response => {
          this.tipos_equipos = response.data;
          // Actualiza busqueda_existente basado en el resultado
          this.busqueda_existente = this.tipos_equipos.length > 0;
        })
        .catch(error => {
          console.log(error);
          this.busqueda_existente = false; // Asegura que busqueda_existente sea false en caso de error
        });

      this.$store.commit('setIsLoading', false);
    },
    // Usar SweetAlert2 para confirmar la eliminación
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
          this.delete_tipo_equipo(id);
        }
      });
    },
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.search_tipo_equipo();
      }, 300); // Ajusta el tiempo de espera según sea necesario
    },
    // Eliminar tipo de equipo
    async delete_tipo_equipo(id) {
      try {
        await axios.delete(`/api/tipos_equipos/${id}/`);
        // Actualizar la lista de tipos de equipo eliminando el que se ha borrado
        this.tipos_equipos = this.tipos_equipos.filter(tipo_equipo => tipo_equipo.id !== id);
        Swal.fire('Eliminado!', 'El tipo de equipo ferroviario ha sido eliminado exitosamente.', 'success');
      } catch (error) {
        console.error('Error al eliminar el tipo de equipo ferroviario:', error);
        Swal.fire('Error', 'Hubo un error al eliminar el tipo de equipo ferroviario.', 'error');
      }
    },
    // Función para que sea mostrado el texto asociado al valor del select
    getTipoEquipoText(value) {
      const tiposEquipos = {
        'casilla': 'Casilla',
        'caj_gon': 'Cajones o Góndola',
        'planc_plat': 'Plancha o Plataforma',
        'Plan_porta_cont': 'Plancha porta contenedores',
        'cist_liquidos': 'Cisterna para líquidos',
        'cist_solidos': 'Cisterna para sólidos',
        'tolva_g_mineral': 'Tolva granelera(mineral)',
        'tolva_g_agric': 'Tolva granelera(agrícola)',
        'tolva_g_cemento': 'Tolva para cemento',
        'volqueta': 'Volqueta',
        'Vagon_ref': 'Vagón refrigerado',
        'jaula': 'Jaula',
        'locomotora': 'Locomotora',
        'tren': 'Tren',
        // Añade aquí todos los tipos de equipo que necesites
      };
      return tiposEquipos[value] || 'Desconocido';
    },
    getTipoCargaText(value) {
      const tiposCarga = {
        'combustible': 'Combustible',
        'aceite': 'Aceite',
        'miel': 'Miel',
        'alcohol': 'Alcohol',
        'quimicos': 'Químicos',
        'contenedores': 'Contenedores',
        'otros': 'Otros',
        // Añade aquí todos los tipos de carga que necesites
      };
      return tiposCarga[value] || 'Desconocido';
    },
    getTipoCombustibleText(value) {
      const tiposCombustible = {
        'combust_blanco': 'Combustible blanco',
        'combustible_negro': 'Combustible negro',
        'combustible_turbo': 'Combustible turbo',
        // Añade aquí todos los tipos de combustible que necesites
      };
      return tiposCombustible[value] || 'Desconocido';
    },
  },
};
</script>