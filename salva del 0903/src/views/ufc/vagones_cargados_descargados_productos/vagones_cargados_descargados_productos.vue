<template>
    <div>
      <img style="width: 250px;" src="@/assets/Imagenes/mitrans.png">
      <NavbarComponent />
  
      <div class="search-container">
        <form class="d-flex search-form" @submit.prevent="searchproductoVagon">
          <input
            class="form-control form-control-sm me-2"
            type="search"
            placeholder="Origen o tipo de equipo ferroviario"
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
        <router-link v-if="hasGroup('Admin')" class="create-button" to="/adicionar_productos_vagones_cargados_descargados">
          Adicionar producto de vagón <i class="bi bi-plus-circle"></i>
        </router-link> 
      </div>
      <br>
  
      <div class="table-responsive">
        <table class="table">
          <thead>
            <tr>
              <th scope="col">No</th>
              <th scope="col">Producto</th>
              <th scope="col">Tipo de embalaje</th>
              <th scope="col">Unidad de medida</th>
              <th scope="col">Cantidad</th>
              <th scope="col" v-if="hasGroup('Admin')">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in vagonesFiltrados" :key="item.id">
              <th scope="row" style="background-color:white">{{ index + 1 }}</th>
              <td>{{ item.producto_name }}</td>
            <td>{{ item.tipo_embalaje_name }}</td>
            <td>{{ item.unidad_medida_name }}</td>
            <td>{{ item.cantidad }}</td>
            <!-- <td>{{ item.causas_incumplimiento || '-' }}</td> -->
              <td v-if="hasGroup('Admin')">
                <button @click.prevent="confirmDelete(item.id)" class="btn btn-danger">
                  <i style="color:white" class="bi bi-trash"></i>
                </button>
                <!-- <button style="margin-left:10px" class="btn btn-warning">
                  <router-link :to="{name: 'EditarVagon', params: {id: item.id}}">
                    <i style="color:white" class="bi bi-pencil-square"></i>
                  </router-link>
                </button> -->
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Mensaje cuando no hay resultados -->
      <h1 v-if="vagonesFiltrados.length === 0 && searchQuery">
        No existe ningún registro asociado a ese parámetro de búsqueda.
      </h1>
    </div>
  </template>
  
  <script>
  import Swal from 'sweetalert2';
  import axios from 'axios';
  import NavbarComponent from '@/components/NavbarComponent.vue';
  
  export default {
    name: 'vagones_cargados_descargados',
    components: {
      NavbarComponent,
    },
    data() {
      return {
        vagones: [], // Lista completa de vagones
        vagonesFiltrados: [], // Lista filtrada de vagones
        searchQuery: '', // Término de búsqueda
        debounceTimeout: null, // Timeout para el debounce
        userPermissions: [], // Permisos del usuario
        userGroups: [], // Grupos del usuario
      };
    },
    async created() {
      await this.fetchUserPermissionsAndGroups();
      await this.getVagones();
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
      // Obtiene todos los vagones
      async getVagones() {
        try {
          const response = await axios.get('/ufc/productos-vagones-cargados-descargados/');
          this.vagones = response.data;
          this.vagonesFiltrados = this.vagones; // Inicialmente, muestra todos los vagones
          console.log('total de vagones',this,this.vagonesFiltrados)
        } catch (error) {
          console.error('Error al obtener los vagones:', error);
          Swal.fire('Error', 'No se pudieron cargar los productos de vagones.', 'error');
        }
      },
      // Filtra los vagones según el término de búsqueda
      searchVagon() {
        if (this.searchQuery) {
          const query = this.searchQuery.toLowerCase();
          this.vagonesFiltrados = this.vagones.filter(
            (vagon) =>
              vagon.origen.toLowerCase().includes(query) ||
              vagon.tipo_equipo_ferroviario_name.toLowerCase().includes(query)
          );
        } else {
          this.vagonesFiltrados = this.vagones; // Si no hay búsqueda, muestra todos
        }
      },
      // Debounce para evitar múltiples llamadas durante la escritura
      handleSearchInput() {
        clearTimeout(this.debounceTimeout);
        this.debounceTimeout = setTimeout(() => {
          this.searchVagon();
        }, 300);
      },
      // Confirma la eliminación de un vagón
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
            this.deleteVagon(id);
          }
        });
      },
      // Elimina un vagón
      async deleteVagon(id) {
        try {
          await axios.delete(`/ufc/productos-vagones-cargados-descargados/${id}/`);
          this.vagones = this.vagones.filter(vagon => vagon.id !== id);
          this.vagonesFiltrados = this.vagonesFiltrados.filter(vagon => vagon.id !== id);
          Swal.fire('Eliminado!', 'El producto de vagones ha sido eliminado exitosamente.', 'success');
        } catch (error) {
          console.error('Error al eliminar el vagón:', error);
          Swal.fire('Error', 'Hubo un error al eliminar el producto.', 'error');
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Estilos similares al componente anterior */
  .search-container input::placeholder {
    font-size: 12px;
    color: #999;
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