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
      <form class="d-flex search-form" @submit.prevent="searchOrganismos">
        <div class="input-container">
          <i class="bi bi-search"></i>
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="Buscar por nombre, abreviatura o código"
          aria-label="Search"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px; padding-left: 5px;margin-top: -70px;" 
        />
      </div>
      </form>
    </div>
    <div class="create-button-container">
      <router-link v-if="hasGroup('Admin')" class="create-button" to="/AdicionarOrganismos">
        <i class="bi bi-plus-circle large-icon"></i>
      </router-link>
    </div>
    <h3 style="margin-top: -33px; font-size: 18px;
    margin-right: 630px;color: #002A68;">Listado de organismos</h3>
    <br />
    <div class="table-container">
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Nombre</th>
          <th scope="col">Abreviatura</th>
          <th scope="col">Código REEUP</th>
          <th scope="col" >Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item) in organismos" :key="item.id">
          <td>{{ item.nombre }}</td>
          <td>{{ item.abreviatura }}</td>
          <td>{{ item.codigo_reeup }}</td>
          <td >
              <button @click="openOrganismosDetailsModal(item)" class="btn btn-info btn-small btn-eye" 
              v-html="showNoId ? '<i class=\'bi bi-eye-slash-fill\'></i>' : '<i class=\'bi bi-eye-fill\'></i>'">
              </button>
              <span v-if="hasGroup('Admin')">
                <button class="btn btn-warning btn-small">
                  <router-link :to="{name: 'EditarOrganismos', params: {id:item.id}}">
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
    <h1 v-if="!busqueda_existente && searchQuery">No existe ningún registro asociado a ese parámetro de búsqueda</h1>
    <h1 v-if="organismos.length === 0 && !loading && !searchQuery">No hay organismos registrados</h1>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from 'axios';
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: 'OrganismosView',
  components: {
    NavbarComponent,
  },
  data() {
    return {
      organismos: [],
      searchQuery: '',
      debounceTimeout: null,
      busqueda_existente: true,
      userPermissions: [],
      userGroups: [],
      loading: false,
      error: null,
      currentPage: 1,      // Página actual
      totalPages: 1,       // Total de páginas
      pages: [],           // Lista de páginas visibles
      itemsPerPage: 15      // Número de elementos por página
    };
  },
  async created() {
    await this.fetchUserPermissionsAndGroups();
    await this.get_organismos();
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
          this.userPermissions = response.data.permissions || [];
          this.userGroups = response.data.groups || [];
        }
      } catch (error) {
        console.error('Error al obtener permisos y grupos:', error);
      }
    },
    async get_organismos() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get("/api/osde/", {
          params: {
            page: this.currentPage,
            search: this.searchQuery
          },
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`
          }
        });

        // Asumiendo que el backend devuelve una respuesta paginada
        this.organismos = Array.isArray(response.data.results) ? response.data.results : response.data;
        this.totalPages = Math.ceil(response.data.count / this.itemsPerPage);
        this.updatePages();
        this.busqueda_existente = this.organismos.length > 0 || !this.searchQuery;
      } catch (error) {
        console.error("Error al obtener organismos:", error);
        this.error = error;
        if (error.response && error.response.status === 401) {
          Swal.fire("Sesión expirada", "Por favor inicie sesión nuevamente", "error");
          this.$router.push('/login');
        } else {
          Swal.fire("Error", "No se pudieron cargar los organismos", "error");
        }
        this.organismos = [];
        this.busqueda_existente = false;
      } finally {
        this.loading = false;
      }
    },
    async searchOrganismos() {
      try {
        this.loading = true;
        this.currentPage = 1; // Reiniciar a la primera página al realizar una búsqueda
        const response = await axios.get("/api/osde/", {
          params: {
            search: this.searchQuery,
            page: this.currentPage
          },
          headers: {
            'Authorization': `Token ${localStorage.getItem('token')}`
          }
        });
        this.organismos = Array.isArray(response.data.results) ? response.data.results : response.data;
        this.totalPages = Math.ceil(response.data.count / this.itemsPerPage);
        this.updatePages();
        this.busqueda_existente = this.organismos.length > 0;
      } catch (error) {
        console.error("Error en búsqueda:", error);
        this.busqueda_existente = false;
      } finally {
        this.loading = false;
      }
    },
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchOrganismos();
      }, 500);
    },
    confirmDelete(id) {
      Swal.fire({
        title: "¿Estás seguro?",
        text: "¡No podrás revertir esta acción!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
        reverseButtons: true,
      }).then((result) => {
        if (result.isConfirmed) {
          this.deleteOrganismo(id);
        }
      });
    },
    async deleteOrganismo(id) {
      try {
        await axios.delete(`/api/osde/${id}/`, {
          headers: {
            'Authorization': `Token ${localStorage.getItem('token')}`
          }
        });
        
        await this.get_organismos();
        Swal.fire(
          "Eliminado!",
          "El organismo ha sido eliminado exitosamente.",
          "success"
        );
      } catch (error) {
        console.error("Error al eliminar el organismo:", error);
        Swal.fire(
          "Error",
          error.response?.data?.message || "Hubo un error al eliminar el organismo.",
          "error"
        );
      }
    },
    openOrganismosDetailsModal(organismo) {
      Swal.fire({
        title: 'Detalles del Organismo',
        html: `
          <div style="text-align: left;">
            <p><strong>Nombre:</strong> ${organismo.nombre}</p>
            <p><strong>Abreviatura:</strong> ${organismo.abreviatura}</p>
            <p><strong>Código REEUP:</strong> ${organismo.codigo_reeup}</p>
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
        this.get_organismos();
      }
    },
    updatePages() {
      const startPage = Math.max(1, this.currentPage - 2);
      const endPage = Math.min(this.totalPages, this.currentPage + 2);
      this.pages = [];
      for (let i = startPage; i <= endPage; i++) {
        this.pages.push(i);
      }
    }
  }
};
</script>

<style scoped>
/* Tus estilos existentes... */

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

/* Mantén el resto de tus estilos... */
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
</style>