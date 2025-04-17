<template>
  <div>
    <img style="width: 250px;" src="@/assets/Imagenes/mitrans.png" />
    <NavbarComponent />

    <div class="search-container">
      <form class="d-flex search-form" @submit.prevent="searchEntidad">
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="Buscar por nombre, abreviatura o OSDE/OACE"
          aria-label="Buscar"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px;"
        />
        <button class="btn btn-outline-success btn-sm" type="submit">
          Buscar
        </button>
      </form>
    </div>
    <br>

    <div class="create-button-container">
      <router-link
        v-if="hasGroup('Admin')"
        class="create-button"
        to="/AdicionarEntidades"
      >
        Adicionar Entidad <i class="bi bi-plus-circle"></i>
      </router-link>
    </div>
    <br />

    <table class="table">
      <thead>
        <tr>
          <th scope="col">No</th>
          <th scope="col">Nombre</th>
          <th scope="col">Abreviatura</th>
          <th scope="col">OSDE/OACE u Organismo</th>
          <th scope="col">Código REEUP</th>
          <th scope="col">Tipo de entidad</th>
          <th scope="col">Provincia</th>
          <th scope="col">Territorio</th>
          <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in entidadesFiltradas" :key="item.id">
          <th scope="row" style="background-color:white">{{ index + 1 }}</th>
          <td>{{ item.nombre }}</td>
          <td>{{ item.abreviatura }}</td>
          <td>{{ item.o_o_o_name }}</td>
          <td>{{ item.codigo_reeup }}</td>
          <td>{{ item.tipo_entidad_name }}</td>
          <td>{{ item.provincia_name }}</td>
          <td>{{ item.territorio_name }}</td>
          <td v-if="hasGroup('Admin')">
            <button @click.prevent="confirmDelete(item.id)" class="btn btn-danger">
              <i style="color: white" class="bi bi-trash"></i>
            </button>
            <router-link
              :to="{ name: 'EditarEntidades', params: { id: item.id } }"
              class="btn btn-warning"
              style="margin-left: 10px">
              <i style="color: white" class="bi bi-pencil-square"></i>
            </router-link>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Mensaje cuando no hay resultados -->
    <h1 v-if="entidadesFiltradas.length === 0 && searchQuery">
      No existe ningún registro asociado a ese parámetro de búsqueda.
    </h1>
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "EntidadesView",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      entidades: [], // Lista completa de entidades
      entidadesFiltradas: [], // Lista filtrada de entidades
      searchQuery: "", // Término de búsqueda
      debounceTimeout: null, // Timeout para el debounce
      userPermissions: [], // Permisos del usuario
      userGroups: [], // Grupos del usuario
    };
  },
  async created() {
    await this.fetchUserPermissionsAndGroups();
    await this.getEntidades();
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
    // Obtiene todas las entidades
    async getEntidades() {
      try {
        const response = await axios.get("/api/entidades/");
        this.entidades = response.data;
        this.entidadesFiltradas = this.entidades; // Inicialmente, muestra todas las entidades
      } catch (error) {
        console.error("Error al obtener las entidades:", error);
        Swal.fire('Error', 'No se pudieron cargar las entidades.', 'error');
      }
    },
    // Filtra las entidades según el término de búsqueda
    searchEntidad() {
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        this.entidadesFiltradas = this.entidades.filter(
          (entidad) =>
            entidad.nombre.toLowerCase().includes(query) ||
            entidad.abreviatura.toLowerCase().includes(query) ||
            entidad.o_o_o_name.toLowerCase().includes(query)
        );
      } else {
        this.entidadesFiltradas = this.entidades; // Si no hay búsqueda, muestra todas
      }
    },
    // Debounce para evitar múltiples llamadas durante la escritura
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchEntidad();
      }, 300);
    },
    // Confirma la eliminación de una entidad
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
          this.deleteEntidad(id);
        }
      });
    },
    // Elimina una entidad
    async deleteEntidad(id) {
      try {
        await axios.delete(`/api/entidades/${id}/`);
        this.entidades = this.entidades.filter(entidad => entidad.id !== id);
        this.entidadesFiltradas = this.entidadesFiltradas.filter(entidad => entidad.id !== id);
        Swal.fire("Eliminado!", "La entidad ha sido eliminada exitosamente.", "success");
      } catch (error) {
        console.error("Error al eliminar la entidad:", error);
        Swal.fire("Error", "Hubo un error al eliminar la entidad.", "error");
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
/*para el placeholder del buscador */
.search-container input::placeholder {
  font-size: 12px; /* Tamaño de la fuente más pequeño */
  color: #999;     /* Color del texto del placeholder */
}
</style>