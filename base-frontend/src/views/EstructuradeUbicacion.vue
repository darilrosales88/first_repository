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
            <td>{{ item.tipo_estructura_name }}</td><!-- nacionalidad_name esta declarado en el serializador -->
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
import Swal from 'sweetalert2'
import axios from 'axios';
import NavbarComponent from '@/components/NavbarComponent.vue';

export default {
  name: 'EmbarcacionView',

  components:{
      NavbarComponent
  },

  data(){
      return{
          estructuras: [],
          searchQuery: '', // Añadido aquí
          debounceTimeout: null, // Añadido aquí
          busqueda_existente: true, // Variable para controlar la visibilidad del <h1> de la busqueda
          userPermissions: [], // Almacenará los permisos del usuario
          userGroups: [],      // Almacenará los grupos del usuario
          showNoId: false,
      }
  },

  mounted() {
      this.get_estructuras()
  },
  async created() {
        // Obtener los permisos y grupos del usuario al cargar el componente
        await this.fetchUserPermissionsAndGroups();
      },
 methods:{
  toggleNoIdVisibility() {
      this.showNoId = !this.showNoId; // Alternar la visibilidad de las columnas No e Id
    },
  // Verifica si el usuario tiene un permiso específico
  hasPermission(permission) {
      if (!this.userPermissions) return false; // Verificación adicional
      return this.userPermissions.some(p => p.name === permission);
    },
    hasGroup(group) {
      if (!this.userGroups) return false; // Verificación adicional
      return this.userGroups.some(g => g.name === group);
    },
    // Obtiene los permisos y grupos del usuario desde el backend
    async fetchUserPermissionsAndGroups() {
      try {
        const userId = localStorage.getItem('userid');
        if (userId) {
          const response = await axios.get(`/apiAdmin/user/${userId}/permissions-and-groups/`);
          this.userPermissions = response.data.permissions || []; // Inicializa como array vacío si es undefined
          this.userGroups = response.data.groups || []; // Inicializa como array vacío si es undefined
        }
      } catch (error) {
        console.error('Error al obtener permisos y grupos:', error);
      }
    },
    async get_estructuras() {
    this.$store.commit('setIsLoading', true);

    try {
        const response = await axios.get('/api/estructuras_ubicacion/');
        console.log('Datos recibidos:', response.data);  // Verifica los datos recibidos
        this.estructuras = response.data;
    } catch (error) {
        console.error('Error al obtener las estructuras:', error);
    } finally {
        this.$store.commit('setIsLoading', false);
    }
},
      //metodo para buscar registros en base al parametro de búsqueda
      async search_estructura() {
          this.$store.commit('setIsLoading', true);

          axios
          //aqui nombre_embarcacion es el nombre que declaramos en el parametro al que se iguala la variable search
          //en la vista asociada al serializador del modelo en cuestion
              .get(`/api/estructuras_ubicacion/?nombre_estructura=${this.searchQuery}`)
              .then(response => {
                  this.estructuras = response.data;
                  // Actualiza showH1 basado en el resultado
                  this.busqueda_existente = this.estructuras.length > 0;
              })
              .catch(error => {
                  console.log(error);
                  this.busqueda_inexistente = false; // Asegura que busqueda_inexistente sea false en caso de error
              });

          this.$store.commit('setIsLoading', false);
      },
              
      // Usar SweetAlert2 para confirmar la eliminación
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
                  this.delete_embarcacion(id)
              }
          })
      },

      handleSearchInput() {
          clearTimeout(this.debounceTimeout);
          this.debounceTimeout = setTimeout(() => {
              this.search_estructura();
          }, 300); // Ajusta el tiempo de espera según sea necesario
      },

      // Eliminar embarcacion
      async delete_embarcacion(id) {
          try {
              await axios.delete(`/api/tipos_estructuras_ubicacion/${id}/`)
              // Actualizar la lista de estructuras eliminando el que se ha borrado
              this.estructuras = this.estructuras.filter(estructura => estructura.id !== id)

              Swal.fire('Eliminado!', 'La estructura ha sido eliminada exitosamente.', 'success')
            } catch (error) {
            
              console.error("Error al eliminar la estructura:", error)
              Swal.fire('Error', 'Hubo un error al eliminar la estructura.', 'error')
          }
      }, 
      openEstructuradeUbicacionDetailsModal(EstructuradeUbicacion) {
    // Mapear IDs de grupos a nombres
    const gruposAsignados = EstructuradeUbicacion.groups && EstructuradeUbicacion.groups.length > 0
        ? EstructuradeUbicacion.groups
            .map(groupId => {
                const grupo = this.gruposDisponibles.find(g => g.id === groupId);
                return grupo ? grupo.name : 'Desconocido';
            })
            .join(', ')
        : 'Ninguno';

    // Mapear IDs de permisos a nombres
    const permisosAsignados = EstructuradeUbicacion.EstructuradeUbicacion_permissions && 
    EstructuradeUbicacion.EstructuradeUbicacion_permissions.length > 0
        ? EstructuradeUbicacion.EstructuradeUbicacion_permissions
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
},    

  },


}
</script>