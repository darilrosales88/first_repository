<template>
  <div>
    <div style="background-color: #002a68; color: white; text-align: right">
      <h6>Bienvenido:</h6>
    </div>
    <br />
    <img style="width: 250px;" src="@/assets/Imagenes/mitrans.png">
    <NavbarComponent />
    <br />
    <br />
    <div class="search-container">
      <form class="d-flex search-form" @submit.prevent="search_user">
        <div class="input-container">
          <i class="bi bi-search"></i>
          <input
            class="form-control form-control-sm me-2"
            type="search"
            placeholder="Search"
            aria-label="Search"
            v-model="searchQuery"
            @input="handleSearchInput"
            style="width: 200px; padding-left: 5px; margin-top: -70px"
          />
        </div>
      </form>
    </div>
    <div class="create-button-container">
      <router-link
        class="create-button"
        to="/AdicionarUsuario"
      >
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h3
      style="
        margin-top: -33px;
        font-size: 18px;
        margin-right: 630px;
        color: #002a68;
      "
    >
      Listado de usuarios
    </h3>
    <br />
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">No</th>
            <th scope="col">Nombre</th>
            <th scope="col">Apellidos</th>
            <th scope="col">Usuario</th>
            <th scope="col">Rol</th>
            <th scope="col">Email</th>
            <th scope="col">Entidad</th>
            <th scope="col">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in usuarios" :key="item.id">
            <th scope="row" style="background-color: white;">{{ (index + 1) }}</th>
            <td>{{ item.first_name }}</td>
            <td>{{ item.last_name }}</td>
            <td>{{ item.username }}</td>
            <td>{{ item.role_name }}</td>
            <td>{{ item.email }}</td>
            <td>{{ item.entidad_name }}</td>
            <td>
              <button
                @click="openUserDetailsModal(item)"
                class="btn btn-info btn-small btn-eye"
              >
                <i class="bi bi-eye-fill"></i>
              </button>
              <button class="btn btn-warning btn-small">
                <router-link :to="{name: 'EditarUsuario', params: {id:item.id}}">
                  <i style="color: black" class="bi bi-pencil-square"></i>
                </router-link>
              </button>
              <button
                @click.prevent="confirmDelete(item.id)"
                class="btn btn-danger btn-small"
              >
                <i class="bi bi-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
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
  pointer-events: none;
}

.large-icon {
  font-size: 1.7rem;
}

table {
  width: 84%;
  border-collapse: collapse;
  margin-left: 190px;
  margin-bottom: 10px;
  font-size: 0.875rem;
}

th,
td {
  padding: 0.15rem;
  white-space: nowrap;
}

th {
  background-color: #f2f2f2;
}

.btn {
  cursor: pointer;
}

.btn-small {
  font-size: 22px;
  color: black;
  margin-right: 5px;
  outline: none;
  border: none;
  background: none;
  padding: 0;
}

.btn-eye {
  font-size: 22px;
  margin-right: 5px;
  outline: none;
  border: none;
  background: none;
  padding: 0;
}

.btn:hover {
  background: none;
}

.btn:focus {
  outline: none;
  box-shadow: none;
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

/*estilos para el modal */
.custom-swal-popup {
  border-radius: 10px;
  font-family: Arial, sans-serif;
}

.custom-swal-title {
  font-size: 24px;
  color: #333;
}

.custom-swal-html {
  font-size: 16px;
  color: #555;
}
</style>

<script>
import Swal from 'sweetalert2';
import axios from 'axios';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'Usuarios',
  components: {
    NavbarComponent,
  },
  data() {
    return {
      usuarios: [],
      gruposDisponibles: [],  // Lista de grupos disponibles
      permisosDisponibles: [],  // Lista de permisos disponibles
      searchQuery: '',
      debounceTimeout: null,
    };
  },
  mounted() {
    this.get_usuarios();
    this.fetchGroups();
    this.fetchPermisosDisponibles();
  },
  methods: {
    async get_usuarios() {
      this.$store.commit('setIsLoading', true);
      try {
        const response = await axios.get('/apiAdmin/users/');
        this.usuarios = response.data.results;
      } catch (error) {
        console.error(error);
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    },
    async fetchGroups() {
              try {
                  const response = await axios.get('/apiAdmin/groups/');
                  this.gruposDisponibles = response.data.results;
              } catch (error) {
                  console.error('Error al obtener los grupos:', error);
              }
          },
          async fetchPermisosDisponibles() {
              try {
                  const response = await axios.get('/apiAdmin/permisos/');
                  this.permisosDisponibles = response.data;
              } catch (error) {
                  console.error('Error al obtener los permisos:', error);
              }
          },
      
    async search_user() {
      this.$store.commit('setIsLoading', true);
      try {
        const response = await axios.get(`/apiAdmin/users/?username=${this.searchQuery}`);
        this.usuarios = response.data;
      } catch (error) {
        console.error(error);
      } finally {
        this.$store.commit('setIsLoading', false);
      }
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
          this.delete_unidad(id);
        }
      });
    },
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.search_user();
      }, 300);
    },
    async delete_unidad(id) {
      try {
        await axios.delete(`/apiAdmin/users/${id}/`);
        this.usuarios = this.usuarios.filter(usuario => usuario.id !== id);
        Swal.fire('Eliminado!', 'El usuario se ha eliminado exitosamente.', 'success');
      } catch (error) {
        console.error('Error al eliminar el usuario:', error);
        Swal.fire('Error', 'Hubo un error al eliminar el usuario.', 'error');
      }
    },
    openUserDetailsModal(user) {
    // Mapear IDs de grupos a nombres
    const gruposAsignados = user.groups && user.groups.length > 0
        ? user.groups
            .map(groupId => {
                const grupo = this.gruposDisponibles.find(g => g.id === groupId);
                return grupo ? grupo.name : 'Desconocido';
            })
            .join(', ')
        : 'Ninguno';

    // Mapear IDs de permisos a nombres
    const permisosAsignados = user.user_permissions && user.user_permissions.length > 0
        ? user.user_permissions
            .map(permisoId => {
                const permiso = this.permisosDisponibles.find(p => p.id === permisoId);
                return permiso ? permiso.name : 'Desconocido';
            })
            .join(', ')
        : 'Ninguno';

    Swal.fire({
        title: 'Detalles del Usuario',
        html: `
            <div style="text-align: left;">
                <p><strong>Nombre:</strong> ${user.first_name}</p>
                <p><strong>Apellidos:</strong> ${user.last_name}</p>
                <p><strong>Usuario:</strong> ${user.username}</p>
                <p><strong>Email:</strong> ${user.email}</p>
                <p><strong>Entidad:</strong> ${user.entidad_name}</p>
                <p><strong>Cargo:</strong> ${user.cargo_name}</p>
                <p><strong>Grupos Asignados:</strong> ${gruposAsignados}</p>
                <p><strong>Permisos Asignados:</strong> ${permisosAsignados}</p>
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