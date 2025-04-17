<template>
  <div>
    <img style="width: 250px;" src="@/assets/Imagenes/mitrans.png">
    <NavbarComponent />

    <div class="search-container">
      <form class="d-flex search-form" @submit.prevent="searchEmbarcacion">
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="Nombre, tipo o nacionalidad"
          aria-label="Buscar"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px;"
        />
        <button class="btn btn-outline-success btn-sm" type="submit">Buscar</button>
      </form>
      <br>
    </div>

    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="/AdicionarEmbarcacion">
        Crear embarcación <i class="bi bi-plus-circle"></i>
      </router-link>
    </div>
    <br>

    <div class="table-responsive">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">No</th>
            <th scope="col">Nombre</th>
            <th scope="col">Nacionalidad</th>
            <th scope="col">Eslora</th>
            <th scope="col">Manga</th>
            <th scope="col">Calado máximo</th>
            <th scope="col">Desplazamiento máximo</th>
            <th scope="col">Tipo de embarcación</th>
            <th scope="col">Tipo de buque</th>
            <th scope="col">Tipo de patana</th>
            <th scope="col">IMO</th>
            <th scope="col">Potencia</th>
            <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in embarcacionesFiltradas" :key="item.id">
            <th scope="row" style="background-color:white">{{ index + 1 }}</th>
            <td>{{ item.nombre_embarcacion }}</td>
            <td>{{ item.nacionalidad_name }}</td>
            <td>{{ item.eslora }}</td>
            <td>{{ item.manga }}</td>
            <td>{{ item.calado_maximo }}</td>
            <td>{{ item.desplazamiento_maximo }}</td>
            <td>{{ getTipoEmbarcacionText(item.tipo_embarcacion) }}</td>
            <td>{{ getTipoBuqueText(item.tipo_buque) }}</td>
            <td>{{ getTipoPatanaText(item.tipo_patana) }}</td>
            <td>{{ getIMOText(item.imo) }}</td>
            <td>{{ getPotenciaText(item.potencia) }}</td>
            <td v-if="hasGroup('Admin')">
              <button @click.prevent="confirmDelete(item.id)" class="btn btn-danger">
                <i style="color:white" class="bi bi-trash"></i>
              </button>
              <button style="margin-left:10px" class="btn btn-warning">
                <router-link :to="{name: 'EditarEmbarcacion', params: {id: item.id}}">
                  <i style="color:white" class="bi bi-pencil-square"></i>
                </router-link>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Mensaje cuando no hay resultados -->
    <h1 v-if="embarcacionesFiltradas.length === 0 && searchQuery">
      No existe ningún registro asociado a ese parámetro de búsqueda.
    </h1>
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
    };
  },
  async created() {
    await this.fetchUserPermissionsAndGroups();
    await this.getEmbarcaciones();
  },
  methods: {
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
      return tipos_embarcaciones[value] || '-';
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
      return tipos_buques[value] || '-';
    },
    // Obtiene el texto asociado al valor del tipo de patana
    getTipoPatanaText(value) {
      const tipos_patanas = {
        pat_carga_seca: 'Patana de carga seca',
        pat_carga_liquida: 'Patana de carga líquida',
        patana_comb: 'Patana de combustible',
        patana_ro_ro: 'Patana Ro Ro',
      };
      return tipos_patanas[value] || '-';
    },
    // Obtiene el texto asociado al valor del tipo de patana
    
  getPotenciaText(value) {
    // Si el valor es un número mayor que 0, devuelve el número
    if ( value > 0) {
      return value;
    }
    // En cualquier otro caso, devuelve el símbolo "-"
    return '-';
  },
  getIMOText(value) {
    // Si el valor es un número mayor que 0, devuelve el número
    if ( value !=null && value !='') {
      return value;
    }
    // En cualquier otro caso, devuelve el símbolo "-"
    return '-';
  },

  },
};
</script>


<style scoped>
/*para el placeholder del buscador */
.search-container input::placeholder {
  font-size: 12px; /* Tamaño de la fuente más pequeño */
  color: #999;     /* Color del texto del placeholder */
}
.search-container {
  padding: 10px;
}

.search-form {
  display: flex;
  justify-content: flex-end;
  margin-left: auto;
}

@media (max-width: 768px) {
  .search-form {
    margin-left: auto;
    margin-right: 10px;
  }
}

th {
  background-color: #f2f2f2;
}

.btn {
  cursor: pointer;
  font-weight: bold;
}

.create-button-container {
  margin-top: -40px;
  text-align: left;
}

.create-button {
  text-decoration: none;
  color: black;
  padding-bottom: 2em;
}

@media (max-width: 768px) {
  .create-button-container {
    text-align: left;
    margin-right: 0;
  }
}
</style>