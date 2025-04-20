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
      <form class="d-flex search-form" @submit.prevent="searchPuertos">
        <div class="input-container">
          <i class="bi bi-search"></i><!-- este es el icono de buscar -->
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="Buscar por nombre o país"
          aria-label="Buscar"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px; padding-left: 5px;margin-top: -70px;" 
        />
      </div>
      </form>
      <br>
    </div>
    <!-- Mostrar el botón "Crear nuevo puerto" solo si el usuario pertenece al grupo "Admin" -->
    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="/CrearPuerto">
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h3  style="margin-top: -33px; font-size: 18px;
    margin-right: 620px;color: #002A68;">Listado de puertos</h3>
    <br />
    <div class="table-container">
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Nombre</th>
          <th scope="col">País</th>
          <th scope="col">Provincia</th>
          <th scope="col">Servicio portuario</th>
          <th scope="col">Latitud</th>
          <th scope="col">Longitud</th>
          <!-- Mostrar la columna "Acción" solo si el usuario pertenece al grupo "Admin" -->
          <th scope="col" >Acción</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item) in puertos" :key="item.id">
          <td>{{ item.nombre_puerto }}</td>
          <td>{{ item.nombre_pais }}</td>
          <td>{{ item.nombre_provincia }}</td>
          <td>{{ item.servicio_portuario_name }}</td>
          <td>{{ item.latitud }}</td>
          <td>{{ item.longitud }}</td>
          <!-- Mostrar los botones de acciones solo si el usuario pertenece al grupo "Admin" -->
          <td >
              <button @click="openPuertoDetailsModal(item)" class="btn btn-info btn-small btn-eye" 
              v-html="showNoId ? '<i class=\'bi bi-eye-slash-fill\'></i>' : '<i class=\'bi bi-eye-fill\'></i>'">
              </button>
              <span v-if="hasGroup('Admin')">
                <button class="btn btn-warning btn-small">
                  <router-link :to="{name: 'EditarPuerto', params: {id:item.id}}">
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
    <!-- Mensaje cuando no hay resultados -->
    <h1 v-if="!busqueda_existente">No existe ningún registro asociado a ese parámetro de búsqueda.</h1>
    <!-- Paginación -->
    <nav aria-label="Page navigation example">
      <ul class="pagination">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">Anterior</a>
        </li>
        <li class="page-item" v-for="page in pages" :key="page" :class="{ active: page === currentPage }">
          <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">Siguiente</a>
        </li>
      </ul>
    </nav>
  </div>
</div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'PuertoView',
  components: {
    NavbarComponent,
  },

  data() {
    return {
      puertos: [],
      searchQuery: '',
      debounceTimeout: null,
      userPermissions: [],
      userGroups: [],
      showNoId: false,
      currentPage: 1,
      totalPages: 1,
      pages: [],
      busqueda_existente: true,
    };
  },

  async created() {
    await this.fetchUserPermissionsAndGroups();
    this.getPuertos();
  },

  methods: {
    toggleNoIdVisibility() {
      this.showNoId = !this.showNoId;
    },
    
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

    async getPuertos() {
      try {
        this.$store.commit("setIsLoading", true);
        const response = await axios.get('api/puertos/', {
          params: {
            page: this.currentPage,
            search: this.searchQuery,
          },
        });
        this.puertos = response.data.results;
        this.totalPages = Math.ceil(response.data.count / 15);
        this.updatePages();
        this.busqueda_existente = this.puertos.length > 0;
      } catch (error) {
        console.error('Error al obtener los puertos:', error);
        this.busqueda_existente = false;
      } finally {
        this.$store.commit("setIsLoading", false);
      }
    },

    async searchPuertos() {
      this.$store.commit("setIsLoading", true);
      this.currentPage = 1;
      try {
        const response = await axios.get('api/puertos/', {
          params: {
            search: this.searchQuery,
            page: this.currentPage,
          },
        });
        this.puertos = response.data.results;
        this.totalPages = Math.ceil(response.data.count / 15);
        this.updatePages();
        this.busqueda_existente = this.puertos.length > 0;
      } catch (error) {
        console.error('Error al buscar puertos:', error);
        this.busqueda_existente = false;
      } finally {
        this.$store.commit("setIsLoading", false);
      }
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchPuertos();
      }, 300);
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
          this.deletePuerto(id);
        }
      });
    },

    async deletePuerto(id) {
      try {
        await axios.delete(`api/puertos/${id}/`);
        this.puertos = this.puertos.filter((puerto) => puerto.id !== id);
        Swal.fire(
          'Eliminado!',
          'El puerto ha sido eliminado exitosamente.',
          'success'
        );
      } catch (error) {
        console.error('Error al eliminar el puerto:', error);
        Swal.fire('Error', 'Hubo un error al eliminar el puerto.', 'error');
      }
    },

    openPuertoDetailsModal(Puerto) {
      Swal.fire({
        title: 'Detalles del Puerto',
        html: `
          <div style="text-align: left;">
            <p><strong>Nombre:</strong> ${Puerto.nombre_puerto}</p>
            <p><strong>País:</strong> ${Puerto.nombre_pais}</p>
            <p><strong>Provincia:</strong> ${Puerto.nombre_provincia}</p>
            <p><strong>Servicio portuario:</strong> ${Puerto.servicio_portuario_name}</p>
            <p><strong>Latitud:</strong> ${Puerto.latitud}</p>
            <p><strong>Longitud:</strong> ${Puerto.longitud}</p>
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

    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        this.getPuertos();
      }
    },

    updatePages() {
      const startPage = Math.max(1, this.currentPage - 2);
      const endPage = Math.min(this.totalPages, this.currentPage + 2);
      this.pages = [];
      for (let i = startPage; i <= endPage; i++) {
        this.pages.push(i);
      }
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
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.page-item {
  margin: 0 5px;
}

.page-link {
  color: #002A68;
  border: 1px solid #002A68;
  padding: 5px 10px;
  border-radius: 5px;
}

.page-item.active .page-link {
  background-color: #002A68;
  border-color: #002A68;
  color: white;
}

.page-item.disabled .page-link {
  color: #6c757d;
  pointer-events: none;
  background-color: #e9ecef;
  border-color: #dee2e6;
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
