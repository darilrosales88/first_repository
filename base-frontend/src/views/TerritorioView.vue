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
      <form class="d-flex search-form" @submit.prevent="search_territorio">
        <div class="input-container">
          <i class="bi bi-search"></i>
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="nombre del territorio"
          aria-label="Buscar"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px; padding-left: 5px;margin-top: -70px;" 
        />
      </div>
      </form>
      <br>
    </div>

    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="AdicionarTerritorio">
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h3 style="margin-top: -33px; font-size: 18px;
    margin-right: 600px;color: #002A68;">Listado de territorios</h3>
    <br />
    <div class="table-container">
  <table class="table" :fields="territorios">
    <thead>
      <tr>
        <th scope="col">Nombre</th>
        <th scope="col">Abreviatura</th>
        <th scope="col" >Acciones</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item) in territorios" :key="item.id">
        <td>{{ item.nombre_territorio }}</td>
        <td>{{ item.abreviatura }}</td>
        <td>
              <button @click="openTerritorioDetailsModal(item)" class="btn btn-info btn-small btn-eye" 
              v-html="showNoId ? '<i class=\'bi bi-eye-slash-fill\'></i>' : '<i class=\'bi bi-eye-fill\'></i>'">
              </button>
              <span v-if="hasGroup('Admin')">
          <button class="btn btn-warning btn-small">
                  <router-link :to="{name: 'EditarTerritorio', params: {id:item.id}}">
                    <i style="color:black" class="bi bi-pencil-square"></i>
                  </router-link>
                </button>
                <button  @click.prevent="confirmDelete(item.id)" class="btn btn-danger btn-small">
                  <i  class="bi bi-trash"></i>
                </button>
              </span>
            </td>
      </tr>
    </tbody>
  </table>
  <h1 v-if="!busqueda_existente">No existe ningún registro asociado a ese parámetro de búsqueda</h1>
</div>
</div>
</template>


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


<script>
import NavbarComponent from "@/components/NavbarComponent.vue";
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "HomeView",
  components: {
    NavbarComponent,
  },

  data() {
    return {
      territorios: [],
      searchQuery: '',
      debounceTimeout: null,
      busqueda_existente: true,
      userPermissions: [],
      userGroups: [],
    };
  },

  mounted() {
    this.get_territorios();
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

    async get_territorios() {
      this.$store.commit('setIsLoading', true);

      try {
        const response = await axios.get('/api/territorios/');
        this.territorios = response.data;
      } catch (error) {
        console.error("Error al obtener territorios:", error);
      }

      this.$store.commit('setIsLoading', false);
    },

    async search_territorio() {
      this.$store.commit('setIsLoading', true);

      try {
        const response = await axios.get(`/api/territorios/?nomb_territorio=${this.searchQuery}`);
        this.territorios = response.data;
        this.busqueda_existente = this.territorios.length > 0;
      } catch (error) {
        console.error("Error al buscar territorios:", error);
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
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed) {
          this.deleteTerritorio(id);
        }
      });
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.search_territorio();
      }, 300);
    },

    async deleteTerritorio(id) {
      this.$store.commit("setIsLoading", true);
      
      try {
        await axios.delete(`/api/territorios/${id}/`);
        this.territorios = this.territorios.filter(territ => territ.id !== id);

        Swal.fire('Eliminado!', 'El territorio ha sido eliminado exitosamente.', 'success');
      } catch (error) {
        console.error("Error al eliminar el territorio:", error);
        Swal.fire('Error', 'Hubo un error al eliminar el territorio.', 'error');
      }

      this.$store.commit("setIsLoading", false);
    },
    openTerritorioDetailsModal(Territorio) {
    // Mapear IDs de grupos a nombres
    const gruposAsignados = Territorio.groups && Territorio.groups.length > 0
        ? Territorio.groups
            .map(groupId => {
                const grupo = this.gruposDisponibles.find(g => g.id === groupId);
                return grupo ? grupo.name : 'Desconocido';
            })
            .join(', ')
        : 'Ninguno';

    // Mapear IDs de permisos a nombres
    const permisosAsignados = Territorio.Territorio_permissions && Territorio.Territorio_permissions.length > 0
        ? Territorio.Territorio_permissions
            .map(permisoId => {
                const permiso = this.permisosDisponibles.find(p => p.id === permisoId);
                return permiso ? permiso.name : 'Desconocido';
            })
            .join(', ')
        : 'Ninguno';

    Swal.fire({
        title: 'Detalles del Atraque',
        html: `
            <div style="text-align: left;">
                <p><strong>Nombre:</strong> ${Territorio.nombre_territorio}</p>
                <p><strong>Abreviatura:</strong> ${Territorio.abreviatura}</p>
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
