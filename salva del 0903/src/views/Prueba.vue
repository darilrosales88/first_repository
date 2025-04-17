<template>
  <div>
    <img style="width: 250px;" src="@/assets/Imagenes/mitrans.png">
    <Navbar-Component />

    <form class="d-flex" @submit.prevent="search_embarcacion" style="padding: 10px; margin-left: 75em;">
      <input class="form-control form-control-sm me-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery" @input="handleSearchInput" style="width: 200px;">
      <button class="btn btn-outline-success btn-sm" type="submit">Search</button>
    </form>

    <div style="margin-top: -4em;">
      <br>
      <button @click="openAddEmbarcacionModal" v-if="hasGroup('Admin')" class="btn btn-primary">
        Crear embarcación &nbsp;<i class="bi bi-plus-circle"></i>
      </button>
      <br>
    </div>

    <br>

    <!-- Contenedor de la tabla con scroll horizontal 
     La clase table-responsive de Bootstrap envuelve la tabla y permite el scroll horizontal cuando el contenido excede el 
     ancho disponible.La tabla no debe tener  un ancho fijo, sino que se ajusta automáticamente al contenido.-->
    <div class="table-responsive" style="overflow-x: auto;">
      <table class="table" style="min-width: 100%;">
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
          <tr v-for="(item, index) in embarcaciones" :key="item.id">
            <th scope="row" style="background-color:white">{{ (index + 1) }}</th>
            <td>{{ item.nombre_embarcacion }}</td>
            <td>{{ item.nacionalidad_name }}</td>
            <td>{{ item.eslora }}</td>
            <td>{{ item.manga }}</td>
            <td>{{ item.calado_maximo }}</td>
            <td>{{ item.desplazamiento_maximo }}</td>
            <td>{{ getTipoEmbarcacionText(item.tipo_embarcacion) }}</td>
            <td>{{ getTipoBuqueText(item.tipo_buque) }}</td>
            <td>{{ getTipoPatanaText(item.tipo_patana) }}</td>
            <td>{{ item.imo }}</td>
            <td>{{ item.potencia }}</td>
            <td v-if="hasGroup('Admin')">
              <div style="display: flex; gap: 10px;">
                <button @click.prevent="confirmDelete(item.id)" class="btn btn-danger">
                  <i style="color:white" class="bi bi-trash"></i>
                </button>
                <button class="btn btn-warning">
                  <router-link :to="{name: 'EditarEmbarcacion', params: {id:item.id}}">
                    <i style="color:white" class="bi bi-pencil-square"></i>
                  </router-link>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>            
    </div>
    <h1 v-if="!busqueda_existente">No existe ningún registro asociado a ese parámetro de búsqueda</h1>
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
      embarcaciones: [],
      searchQuery: '',
      debounceTimeout: null,
      busqueda_existente: true,
      userPermissions: [],
      userGroups: [],
      nationalities: [],
    };
  },

  mounted() {
    this.get_embarcaciones();
    this.getNationalities();
  },

  async created() {
    await this.fetchUserPermissionsAndGroups();
  },

  methods: {
    hasPermission(permission) {
      return this.userPermissions.some(p => p.name === permission);
      },
    hasGroup(group) {
          return this.userGroups.some(g => g.name === group);
      },

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

    async get_embarcaciones() {
      this.$store.commit('setIsLoading', true);
      try {
        const response = await axios.get('/api/embarcaciones/');
        this.embarcaciones = response.data;
      } catch (error) {
        console.error(error);
      }
      this.$store.commit('setIsLoading', false);
    },

    async search_embarcacion() {
      this.$store.commit('setIsLoading', true);
      try {
        const response = await axios.get(`/api/embarcaciones/?nombre_embarcacion=${this.searchQuery}`);
        this.embarcaciones = response.data;
        this.busqueda_existente = this.embarcaciones.length > 0;
      } catch (error) {
        console.error(error);
        this.busqueda_existente = false;
      }
      this.$store.commit('setIsLoading', false);
    },

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
          this.delete_embarcacion(id);
        }
      });
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.search_embarcacion();
      }, 300);
    },

    async delete_embarcacion(id) {
      try {
        await axios.delete(`/api/embarcaciones/${id}/`);
        this.embarcaciones = this.embarcaciones.filter(embarcacion => embarcacion.id !== id);
        Swal.fire('Eliminado!', 'La embarcación ha sido eliminada exitosamente.', 'success');
      } catch (error) {
        console.error('Error al eliminar la embarcación:', error);
        Swal.fire('Error', 'Hubo un error al eliminar la embarcación.', 'error');
      }
    },

    getTipoEmbarcacionText(value) {
      const tipos_embarcaciones = {
        buque: 'Buque',
        remolcador: 'Remolcador',
        patana: 'Patana',
        otros: 'Otros',
      };
      return tipos_embarcaciones[value] || 'Desconocido';
    },

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

    getTipoPatanaText(value) {
      const tipos_patanas = {
        pat_carga_seca: 'Patana de carga seca',
        pat_carga_liquida: 'Patana de carga líquida',
        patana_comb: 'Patana de combustible',
        patana_ro_ro: 'Patana Ro Ro',
      };
      return tipos_patanas[value] || 'Desconocido';
    },

    async openAddEmbarcacionModal() {
  const { value: formValues } = await Swal.fire({
    title: 'Adicionar embarcación',
    html: `
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; width: 100%;">
        <div>
          <label for="nombre_embarcacion">Nombre</label>
          <input id="nombre_embarcacion" class="swal2-input" placeholder="Nombre" required style="width: 90%; padding: 5px; font-size: 14px;">
        </div>
        <div>
          <label for="nacionalidad">Nacionalidad</label>
          <select id="nacionalidad" class="swal2-select" required style="width: 90%; padding: 5px; font-size: 14px;">
            ${this.nationalities.map(n => `<option value="${n.id}">${n.nombre_pais}</option>`).join('')}
          </select>
        </div>
        <div>
          <label for="eslora">Eslora</label>
          <input id="eslora" class="swal2-input" type="number" placeholder="Eslora" step="0.01" required style="width: 90%; padding: 5px; font-size: 14px;">
        </div>
        <div>
          <label for="manga">Manga</label>
          <input id="manga" class="swal2-input" type="number" placeholder="Manga" step="0.01" required style="width: 90%; padding: 5px; font-size: 14px;">
        </div>
        <div>
          <label for="calado_maximo">Calado máximo</label>
          <input id="calado_maximo" class="swal2-input" type="number" placeholder="Calado máximo" step="0.01" required style="width: 90%; padding: 5px; font-size: 14px;">
        </div>
        <div>
          <label for="desplazamiento_maximo">Desplazamiento máximo</label>
          <input id="desplazamiento_maximo" class="swal2-input" type="number" placeholder="Desplazamiento máximo" step="0.01" required style="width: 90%; padding: 5px; font-size: 14px;">
        </div>
        <div>
          <label for="tipo_embarcacion">Tipo de embarcación</label>
          <select id="tipo_embarcacion" class="swal2-select" required style="width: 90%; padding: 5px; font-size: 14px;">
            <option value="buque">Buque</option>
            <option value="remolcador">Remolcador</option>
            <option value="patana">Patana</option>
            <option value="otros">Otros</option>
          </select>
        </div>
        <div>
          <label for="tipo_buque">Tipo de buque</label>
          <select id="tipo_buque" class="swal2-select" style="width: 90%; padding: 5px; font-size: 14px;">
            <option value="buque_carga_gral">Buque de carga general</option>
            <option value="buque_granelero">Buque granelero</option>
            <option value="buque_ro_ro">Buque Ro Ro</option>
            <option value="buque_frig">Buque frigorífico</option>
            <option value="buque_tanque">Buque tanque</option>
            <option value="buque_gases">Buque de gases</option>
            <option value="-">-</option>
          </select>
        </div>
        <div>
          <label for="tipo_patana">Tipo de patana</label>
          <select id="tipo_patana" class="swal2-select" style="width: 90%; padding: 5px; font-size: 14px;">
            <option value="pat_carga_seca">Patana de carga seca</option>
            <option value="pat_carga_liquida">Patana de carga líquida</option>
            <option value="patana_comb">Patana de combustible</option>
            <option value="patana_ro_ro">Patana Ro Ro</option>
            <option value="-">-</option>
          </select>
        </div>
        <div>
          <label for="imo">IMO</label>
          <input id="imo" class="swal2-input" placeholder="IMO" style="width: 90%; padding: 5px; font-size: 14px;">
        </div>
        <div>
          <label for="potencia">Potencia</label>
          <input id="potencia" class="swal2-input" type="number" placeholder="Potencia" step="0.01" style="width: 90%; padding: 5px; font-size: 14px;">
        </div>
      </div>
    `,
    width: '700px', // Ancho fijo del modal
    focusConfirm: false,
    showCancelButton: true, // Mostrar botón de cancelar
    confirmButtonText: 'Aceptar',
    cancelButtonText: 'Cancelar',
    preConfirm: () => {
      const nombre_embarcacion = document.getElementById('nombre_embarcacion').value;
      const nacionalidad = document.getElementById('nacionalidad').value;
      const eslora = parseFloat(document.getElementById('eslora').value);
      const manga = parseFloat(document.getElementById('manga').value);
      const calado_maximo = parseFloat(document.getElementById('calado_maximo').value);
      const desplazamiento_maximo = parseFloat(document.getElementById('desplazamiento_maximo').value);
      const tipo_embarcacion = document.getElementById('tipo_embarcacion').value;
      const tipo_buque = document.getElementById('tipo_buque').value;
      const tipo_patana = document.getElementById('tipo_patana').value;
      const imo = document.getElementById('imo').value;
      const potencia = parseFloat(document.getElementById('potencia').value);

      // Validar campos obligatorios
      if (!nombre_embarcacion || !nacionalidad || isNaN(eslora) || isNaN(manga) || isNaN(calado_maximo) || isNaN(desplazamiento_maximo) || !tipo_embarcacion) {
        Swal.showValidationMessage('Por favor, complete todos los campos obligatorios.');
        return false;
      }

      // Validar formato del IMO (si está presente)
      if (imo && !/^[A-Za-z]{3}[0-9]{7}$/.test(imo)) {
        Swal.showValidationMessage('El IMO debe comenzar con 3 letras seguidas de 7 dígitos.');
        return false;
      }

      return {
        nombre_embarcacion,
        nacionalidad,
        eslora,
        manga,
        calado_maximo,
        desplazamiento_maximo,
        tipo_embarcacion,
        tipo_buque: tipo_buque || '-',
        tipo_patana: tipo_patana || '-',
        imo: imo || null,
        potencia: isNaN(potencia) ? null : potencia,
      };
    },
  });

  if (formValues) {
    try {
      await axios.post('/api/embarcaciones/', formValues);
      Swal.fire('Éxito', 'La embarcación ha sido añadida exitosamente.', 'success');
      this.get_embarcaciones(); // Recargar la lista de embarcaciones
    } catch (error) {
      console.error(error);
      if (error.response && error.response.data) {
        Swal.fire('Error', `Hubo un error al agregar la embarcación: ${JSON.stringify(error.response.data)}`, 'error');
      } else {
        Swal.fire('Error', 'Hubo un error al agregar la embarcación.', 'error');
      }
    }
  }
},

    async getNationalities() {
      try {
        const response = await axios.get('/api/paises/');
        this.nationalities = response.data;
      } catch (error) {
        console.error('Error al obtener las nacionalidades:', error);
      }
    },
  },
};
</script>

<style scoped>
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