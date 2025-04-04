<template>
  <div>
    <div style=" background-color: #003366; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    <br />
    <br />
    <div class="search-container">
    <form class="d-flex search-form" @submit.prevent="search_estructura" >
      <div class="input-container">
        <i class="bi bi-search"></i>
      <input 
      class="form-control form-control-sm me-2" 
      type="search" 
      placeholder="Nombre" 
      aria-label="Search" 
      v-model="searchQuery" 
      @input="handleSearchInput" 
      style="width: 200px; padding-left: 5px;margin-top: -70px;" >
    </div>
    </form>
  </div>
    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="/AdicionarEstructura">
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h3 style="margin-top: -33px; font-size: 18px;
    margin-right: 460px;color: #002A68;">Listado de estructuras de ubicaciones</h3>
    <br />
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Nombre</th>
            <th scope="col">Terminal</th>
            <th scope="col">Tipo de estructura</th>
            <th scope="col">Estructura padre</th>           
            <th scope="col" >Capacidad</th>
            <th scope="col" >Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item) in estructuras" :key="item.id">
            <td>{{ item.nombre_estructura_ubicacion }}</td>
            <td>{{ item.terminal_name }}</td>
            <td>{{ item.tipo_estructura_name }}</td>
            <td>{{ item.estructura_padre_name }}</td>            
            <td>{{ item.capacidad }}</td>
            <td >
              <button @click="openEstructuradeUbicacionDetailsModal(item)" class="btn btn-info btn-small btn-eye" 
              v-html="showNoId ? '<i class=\'bi bi-eye-slash-fill\'></i>' : '<i class=\'bi bi-eye-fill\'></i>'">
              </button>
              <span v-if="hasGroup('Admin')">
                <button class="btn btn-warning btn-small">
                  <router-link :to="{name: 'EditarEstructura', params: {id:item.id}}">
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
    </div>
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
</template>

<script>
import Swal from 'sweetalert2'
import axios from 'axios';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'EstructurasView',
  components: {
    NavbarComponent
  },
  data() {
    return {
      estructuras: [],
      searchQuery: '',
      debounceTimeout: null,
      busqueda_existente: true,
      userPermissions: [],
      userGroups: [],
      showNoId: false,
      currentPage: 1,      // Página actual
      totalPages: 1,       // Total de páginas
      pages: []            // Lista de páginas visibles
    }
  },
  async created() {
    await this.fetchUserPermissionsAndGroups();
    await this.get_estructuras();
  },
  methods: {
    toggleNoIdVisibility() {
      this.showNoId = !this.showNoId;
    },
    hasPermission(permission) {
      if (!this.userPermissions) return false;
      return this.userPermissions.some(p => p.name === permission);
    },
    hasGroup(group) {
      if (!this.userGroups) return false;
      return this.userGroups.some(g => g.name === group);
    },
    async fetchUserPermissionsAndGroups() {
      try {
        const userId = localStorage.getItem('userid');
        if (userId) {
          const response = await axios.get(`/apiAdmin/user/${userId}/permissions-and-groups/`);
          this.userPermissions = response.data.permissions || [];
          this.userGroups = response.data.groups || [];
        }
      } catch (error) {
        console.error('Error al obtener permisos y grupos:', error);
      }
    },
    async get_estructuras() {
      this.$store.commit('setIsLoading', true);
      try {
        const response = await axios.get('/api/estructuras_ubicacion/', {
          params: {
            page: this.currentPage,
            search: this.searchQuery
          }
        });
        this.estructuras = response.data.results;
        this.totalPages = Math.ceil(response.data.count / 15);
        this.updatePages();
        this.busqueda_existente = this.estructuras.length > 0;
      } catch (error) {
        console.error('Error al obtener las estructuras:', error);
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    },
    async search_estructura() {
      this.$store.commit('setIsLoading', true);
      this.currentPage = 1; // Reset to first page when searching
      try {
        const response = await axios.get('/api/estructuras_ubicacion/', {
          params: {
            page: this.currentPage,
            search: this.searchQuery
          }
        });
        this.estructuras = response.data.results;
        this.totalPages = Math.ceil(response.data.count / 15);
        this.updatePages();
        this.busqueda_existente = this.estructuras.length > 0;
      } catch (error) {
        console.error('Error al buscar estructuras:', error);
        this.busqueda_existente = false;
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
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed) {
          this.delete_estructura(id)
        }
      })
    },
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.search_estructura();
      }, 300);
    },
    async delete_estructura(id) {
      try {
        await axios.delete(`/api/estructuras_ubicacion/${id}/`);
        // If it was the last item on the page, go back one page
        if (this.estructuras.length === 1 && this.currentPage > 1) {
          this.currentPage -= 1;
        }
        await this.get_estructuras();
        Swal.fire('Eliminado!', 'La estructura ha sido eliminada exitosamente.', 'success');
      } catch (error) {
        console.error("Error al eliminar la estructura:", error);
        Swal.fire('Error', 'Hubo un error al eliminar la estructura.', 'error');
      }
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        this.get_estructuras();
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
    openEstructuradeUbicacionDetailsModal(EstructuradeUbicacion) {
      Swal.fire({
        title: 'Detalles de la Estructura',
        html: `
          <div style="text-align: left;">
            <p><strong>Nombre:</strong> ${EstructuradeUbicacion.nombre_estructura_ubicacion}</p>
            <p><strong>Terminal:</strong> ${EstructuradeUbicacion.terminal_name}</p>
            <p><strong>Tipo de estructura:</strong> ${EstructuradeUbicacion.tipo_estructura_name}</p>
            <p><strong>Estructura padre:</strong> ${EstructuradeUbicacion.estructura_padre_name}</p>
            <p><strong>Capacidad:</strong> ${EstructuradeUbicacion.capacidad}</p>     
          </div>
        `,
        width: '600px',
        customClass: {
          popup: 'custom-swal-popup',
          title: 'custom-swal-title',
          htmlContainer: 'custom-swal-html',
        },
      });
    }
  }
}
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

th, td {
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

/* Estilos para la paginación */
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
  border: 1px solid #dee2e6;
  padding: 5px 10px;
}

.page-item.active .page-link {
  background-color: #002A68;
  border-color: #002A68;
  color: white;
}

.page-item.disabled .page-link {
  color: #6c757d;
  pointer-events: none;
  background-color: #fff;
  border-color: #dee2e6;
}
</style>