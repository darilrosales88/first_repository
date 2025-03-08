<template>
  <div>
    <img style="width: 250px;" src="@/assets/Imagenes/mitrans.png">
    <Navbar-Component />
    <div class="search-container">
      <form class="d-flex search-form" @submit.prevent="searchOrganismos">
        <input
          class="form-control form-control-sm me-2"
          type="search"
          placeholder="Search"
          aria-label="Search"
          v-model="searchQuery"
          @input="handleSearchInput"
          style="width: 200px;"
        />
        <button class="btn btn-outline-success btn-sm" type="submit">Buscar</button>
      </form>
    </div>
    <div class="create-button-container" v-if="hasGroup('Admin')">
      <router-link
        class="create-button"
        to="/AdicionarOrganismos"
      >
        Adicionar organismo <i class="bi bi-plus-circle"></i>
      </router-link>
    </div>
    <br />
    <br />
    <table class="table">
      <thead>
        <tr>
          <th scope="col">No</th>
          <th scope="col">Nombre</th>
          <th scope="col">Abreviatura</th>
          <th scope="col">Código REEUP</th>
          <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in organismos" :key="item.id">
          <th scope="row">{{ (index + 1) }}</th>
          <td>{{ item.nombre }}</td>
          <td>{{ item.abreviatura }}</td>
          <td>{{ item.codigo_reeup }}</td>
          <td v-if="hasGroup('Admin')">
            <button @click.prevent="confirmDelete(item.id)" class="btn btn-danger">
              <i style="color: white" class="bi bi-trash"></i>
            </button>
            <button style="margin-left: 10px" class="btn btn-warning">
              <router-link :to="{ name: 'EditarOrganismos', params: { id: item.id } }">
                <i style="color: white" class="bi bi-pencil-square"></i>
              </router-link>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <h1 v-if="!busqueda_existente">No existe ningún registro asociado a ese parámetro de búsqueda</h1>
</template>

<style scoped>
.create-button-container {
  margin-top: -40px;
  text-align: left;
  padding-bottom: 2em;
}

.create-button {
  text-decoration: none;
  color: black;
}

@media (max-width: 768px) {
  .create-button-container {
    text-align: left;
    margin-right: 0;
  }
}
</style>

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
</style>

<style scoped>
  body {
    overflow: scroll;
  }
  </style>
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
      searchQuery: '', // Para la búsqueda
      debounceTimeout: null, // Para el debounce en la búsqueda
      busqueda_existente: true, // Controla la visibilidad del mensaje de búsqueda
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [],      // Almacenará los grupos del usuario
    };
  },
  async created() {
    // Obtener los permisos y grupos del usuario al cargar el componente
    await this.fetchUserPermissionsAndGroups();
  },
  mounted() {
    this.get_organismos();
  },
  methods: {
    // Verifica si el usuario tiene un permiso específico
    hasPermission(permission) {
      return this.userPermissions.some(p => p.name === permission);
      },
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
    get_organismos() {
      this.$store.commit("setIsLoading", true);
      axios
        .get("http://127.0.0.1:8000/api/osde/")
        .then((response) => {
          this.organismos = response.data;
          this.busqueda_existente = true; // Reinicia la variable al cargar todos los cargos
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async searchOrganismos() {
      this.$store.commit("setIsLoading", true);

      axios
        .get(`/api/osde/?nombre=${this.searchQuery}`)
        .then((response) => {
          this.organismos = response.data;
          // Actualiza busqueda_existente basado en el resultado
          this.busqueda_existente = this.organismos.length > 0;
        })
        .catch((error) => {
          console.log(error);
          this.busqueda_existente = false;// Asegura que busqueda_existente sea false en caso de error
        });

      this.$store.commit("setIsLoading", false);
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
    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchOrganismos();
      }, 300); // Ajusta el tiempo de espera según sea necesario
    },
    async deleteOrganismo(id) {
      try {
        await axios.delete(`/api/osde/${id}/`);

        this.organismos = this.organismos.filter((item) => item.id !== id);
        Swal.fire(
          "Eliminado!",
          "La unidad de medida ha sido eliminada exitosamente.",
          "success"
        );
      } catch (error) {
        console.error("Error al eliminar la unidad de medida:", error);
        Swal.fire("Error", "Hubo un error al eliminar la unidad de medida.", "error");
      }
    },
  },
};
</script>

 