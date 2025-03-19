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
      <form class="d-flex search-form" @submit.prevent="searchProvincias">
        <div class="input-container">
          <i class="bi bi-search"></i>
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="nombre de provincia"
          aria-label="Search"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px; padding-left: 5px;margin-top: -70px;" 
        />
      </div>
      </form>
    </div>
    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="/AdicionarProvincia">
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h3 style="margin-top: -33px; font-size: 18px;
    margin-right: 600px;color: #002A68;">Listado de provincias</h3>
    <br />
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Código</th>
            <th scope="col">Nombre de la provincia</th>
            <th scope="col">País</th>
            <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item) in provincias" :key="item.id">
            <td>{{ item.codigo }}</td>
            <td>{{ item.nombre_provincia }}</td>
            <td>{{ item.nombre_pais }}</td>
            <td>
              <button @click="openProvinciasDetailsModal(item)" class="btn btn-info btn-small btn-eye" 
              v-html="showNoId ? '<i class=\'bi bi-eye-slash-fill\'></i>' : '<i class=\'bi bi-eye-fill\'></i>'">
              </button>
              <span v-if="hasGroup('Admin')">
                <button class="btn btn-warning btn-small">
                  <router-link :to="{name: 'EditarProvincia', params: {id:item.id}}">
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
import Swal from 'sweetalert2';
import axios from 'axios';
import NavbarComponent from '@/components/NavbarComponent.vue';
import user_autenticado from '@/components/user_autenticado.vue';

export default {
  name: 'ProvinciaView',
  components: {
    user_autenticado,
    NavbarComponent
  },
  data() {
    return {
      provincias: [],
      searchQuery: '',
      busqueda_existente: true,
      debounceTimeout: null,
      userPermissions: [],
      userGroups: [],
      user_autenticado: '',
      showNoId: false,
    };
  },
  mounted() {
    this.getProvincias();
  },
  async created() {
    await this.fetchUserPermissionsAndGroups();
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
    // Obtiene los permisos y grupos del usuario desde el backend
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
    async getProvincias() {
      this.$store.commit('setIsLoading', true);
      axios.get('/api/provincias/')
        .then(response => {
          this.provincias = response.data;
        })
        .catch(error => {
          console.log(error);
        });
      this.$store.commit('setIsLoading', false);
    },
    async searchProvincias() {
      this.$store.commit('setIsLoading', true);
      axios.get(`/api/provincias/?nombre_prov=${this.searchQuery}`)
        .then(response => {
          this.provincias = response.data;
          this.busqueda_existente = this.provincias.length > 0;
        })
        .catch(error => {
          console.log(error);
          this.busqueda_existente = false;
        });
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
          this.deleteProvincia(id);
        }
      });
    },
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchProvincias();
      }, 300);
    },
    async deleteProvincia(id) {
      try {
        await axios.delete(`/api/provincias/${id}/`);
        this.provincias = this.provincias.filter(provincia => provincia.id !== id);
        Swal.fire('Eliminado!', 'La provincia ha sido eliminada exitosamente.', 'success');
      } catch (error) {
        console.error("Error al eliminar la provincia:", error);
        Swal.fire('Error', 'Hubo un error al eliminar la provincia.', 'error');
      }
    },
    openProvinciasDetailsModal(Provincias) {
    // Mapear IDs de grupos a nombres
    const gruposAsignados = Provincias.groups && Provincias.groups.length > 0
        ? Provincias.groups
            .map(groupId => {
                const grupo = this.gruposDisponibles.find(g => g.id === groupId);
                return grupo ? grupo.name : 'Desconocido';
            })
            .join(', ')
        : 'Ninguno';

    // Mapear IDs de permisos a nombres
    const permisosAsignados = Provincias.Provincias_permissions && Provincias.Provincias_permissions.length > 0
        ? Provincias.Provincias_permissions
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
                <p><strong>Código:</strong> ${Provincias.codigo}</p>
                <p><strong>Nombre de la provincia:</strong> ${Provincias.nombre_provincia}</p>
                <p><strong>País:</strong> ${Provincias.nombre_pais}</p>
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