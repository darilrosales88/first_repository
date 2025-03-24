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
        <tr v-for="(item) in puertosFiltrados" :key="item.id">
       
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
    <h1 v-if="puertosFiltrados.length === 0 && searchQuery">
      No existe ningún registro asociado a ese parámetro de búsqueda.
    </h1>
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
      puertosFiltrados: [], // Lista filtrada de puertos
      searchQuery: '', // Añadido aquí
      debounceTimeout: null, // Añadido aquí
      userPermissions: [], // Almacenará los permisos del usuario
      userGroups: [],      // Almacenará los grupos del usuario
      showNoId: false,
    };
  },

  async created() {
    // Obtener los permisos y grupos del usuario al cargar el componente
    await this.fetchUserPermissionsAndGroups();
    this.getPuertos();
  },

  methods: {
    toggleNoIdVisibility() {
      this.showNoId = !this.showNoId; // Alternar la visibilidad de las columnas No e Id
    },
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

    async getPuertos() {
      try {
        const response = await axios.get('api/puertos/');
        this.puertos = response.data;
        this.puertosFiltrados = this.puertos; // Inicialmente, muestra todos los puertos
      } catch (error) {
        console.error('Error al obtener los puertos:', error);
      }
    },

    searchPuertos() {
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase(); // Convirtiendo a minúsculas el parámetro de búsqueda
        this.puertosFiltrados = this.puertos.filter(
          (puerto) =>
            puerto.nombre_pais.toLowerCase().includes(query) ||
            puerto.nombre_puerto.toLowerCase().includes(query)
        );
      } else {
        this.puertosFiltrados = this.puertos; // Si no hay búsqueda, muestra todos
      }
    },

    handleSearchInput() {
      clearTimeout(this.debounceTimeout);
      this.debounceTimeout = setTimeout(() => {
        this.searchPuertos();
      }, 300);
    },

    deleteItem(id) {
      Swal.fire({
        title: '¿Desea eliminar este puerto?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
      }).then((result) => {
        if (result.isConfirmed) {
          axios.delete(`api/puertos/${id}/`)
            .then(() => {
              this.getPuertos(); // Actualizar la lista de puertos después de eliminar
              Swal.fire(
                'Eliminado',
                'El puerto ha sido eliminado exitosamente.',
                'success'
              );
            })
            .catch(error => {
              console.error('Error al eliminar el puerto:', error);
              Swal.fire(
                'Error',
                'Hubo un error al eliminar el puerto.',
                'error'
              );
            });
        }
      });
    },
    openPuertoDetailsModal(Puerto) {
    // Mapear IDs de grupos a nombres
    const gruposAsignados = Puerto.groups && Puerto.groups.length > 0
        ? Puerto.groups
            .map(groupId => {
                const grupo = this.gruposDisponibles.find(g => g.id === groupId);
                return grupo ? grupo.name : 'Desconocido';
            })
            .join(', ')
        : 'Ninguno';

    // Mapear IDs de permisos a nombres
    const permisosAsignados = Puerto.Puerto_permissions && Puerto.Puerto_permissions.length > 0
        ? Puerto.Puerto_permissions
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
