<template>
  <div class="form-container">
    <h2>Editar Grupo {{ grupo.name }}</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="nombre">Nombre:</label>
        <input type="text" v-model="grupo.name" required />
        <p v-if="nombre_error" class="help is-danger">{{ nombre_error }}</p>
      </div>
      <!-- Contenedor de permisos -->
      <div class="permissions-container">
          <div class="permissions-panel">
            <h3>Permisos Disponibles</h3>
            <!-- Campo de búsqueda -->
          <input
            type="text"
            v-model="searchDisponibles"
            placeholder="Buscar permisos..."
            class="search-input"
          />
          <ul>
            <li
              v-for="permiso in permisosDisponiblesFiltrados"
              :key="permiso.id"
              @click="agregarPermiso(permiso)"
            >
              {{ permiso.name }}
            </li>
          </ul>
          </div>

          <!-- Flecha de doble punta -->
          <div class="arrow-container">
            <i class="fas fa-arrows-alt-h"></i> <!-- Ícono de flecha de doble punta -->
          </div>

          <div class="permissions-panel">
            <h3>Permisos Asignados</h3>
            <!-- Campo de búsqueda -->
          <input
            type="text"
            v-model="searchAsignados"
            placeholder="Buscar permisos..."
            class="search-input"
          />
          <ul>
            <li
              v-for="permiso in permisosAsignadosFiltrados"
              :key="permiso.id"
              @click="quitarPermiso(permiso)"
            >
              {{ permiso.name }}
            </li>
          </ul>
          </div>
        </div>

      <!-- Botones de acción -->
      <div class="form-buttons">
        <button type="button">
          <router-link style="color:white;text-decoration:none" to="/groups">Cancelar</router-link>
        </button>
        <button type="submit">Aceptar</button>
      </div>
    </form>
  </div>
</template>
  <style scoped>
.form-container {
  max-width: 750px;
  margin: 50px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-height: 550px
}

h2 {
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  text-align: left;
  margin-bottom: 20px;
  font-size: 20px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  font-size: 13px;
}

label {
  flex: 1;
  text-align: right;
  font-weight: bold;
}

input,
select {
  flex: 2;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.form-buttons {
  display: flex;
  justify-content: end;
  font-size: 15px;
}

button {
  padding: 5px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

button[type="button"] {
  background-color: #007bff;
  color: white;
}

button[type="submit"] {
  margin-left: 15px;
  background-color: #007bff;
  color: white;
}

.permissions-container {
  display: flex;
  gap: 20px;
  max-height: 350px;
}

.permissions-panel {
  flex: 1;
  border: 1px solid #ccc;
  border-radius: 4px;
  
  background-color: #fff;
  max-height: 700px;
  overflow-y: auto;
}

.permissions-panel h3 {
  margin-top: 0;
  font-size: 16px;
  text-align: center;
  position: sticky; /* Hace que el título sea "pegajoso" */
  top: 0; /* Lo fija en la parte superior del contenedor */
  background-color: #fff; /* Fondo para que no se vea el contenido detrás */
  z-index: 1; /* Asegura que el título esté por encima del contenido */
  padding: 10px 0; /* Espaciado para mejor apariencia */
  border-bottom: 1px solid #ccc; /* Línea inferior para separar del contenido */
}

.permissions-panel ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.permissions-panel li {
  padding: 8px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.2s;
}

.permissions-panel li:hover {
  background-color: #f0f0f0;
}

.arrow-container {
  display: flex;
  align-items: center; /* Centra verticalmente la flecha */
  justify-content: center; /* Centra horizontalmente la flecha */
  font-size: 24px; /* Tamaño del ícono */
  color: #007bff; /* Color de la flecha */
}

/*estilo para la busqueda en los paneles */
.search-input {
  width: 95%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  position: sticky;
  top: 50px; /* Fija el input debajo del h3 (ajusta este valor según la altura del h3) */
  background-color: white; /* Fondo para que el texto no se superponga */
  z-index: 1; /* Asegura que esté por encima de los elementos que se desplazan */
}
  </style>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
  name: 'EditarGrupoView',
  data() {
    return {
      grupo: {}, // Datos del grupo
      nombre_error: null, // Mensaje de error para el nombre
      permisosDisponibles: [], // Lista de permisos disponibles
      permisosAsignados: [], // Lista de permisos asignados al grupo
      searchDisponibles: '', // Texto de búsqueda para permisos disponibles
      searchAsignados: '', // Texto de búsqueda para permisos asignados
    };
  },
  computed: {
    // Filtra los permisos disponibles según el texto de búsqueda
    permisosDisponiblesFiltrados() {
      return this.permisosDisponibles.filter(permiso =>
        permiso.name.toLowerCase().includes(this.searchDisponibles.toLowerCase())
      );
    },
    // Filtra los permisos asignados según el texto de búsqueda
    permisosAsignadosFiltrados() {
      return this.permisosAsignados.filter(permiso =>
        permiso.name.toLowerCase().includes(this.searchAsignados.toLowerCase())
      );
    },  
  },
  mounted() {
    this.getGrupo();
  },
  methods: {
    // Obtener los datos del grupo
    async getGrupo() {
  this.$store.commit('setIsLoading', true);
  const grupo_id = this.$route.params.id;
  try {
    const response = await axios.get(`/apiAdmin/obtener-grupo/${grupo_id}/`);
    this.grupo = response.data;
    this.permisosAsignados = response.data.permissions || [];

    // Obtener los permisos disponibles y filtrar los ya asignados
    await this.getPermisosDisponibles();
    this.permisosDisponibles = this.permisosDisponibles.filter(
      permiso => !this.permisosAsignados.some(p => p.id === permiso.id)
    );
  } catch (error) {
    console.error('Error al obtener el grupo:', error);
  } finally {
    this.$store.commit('setIsLoading', false);
  }
},

    // Obtener los permisos disponibles
    async getPermisosDisponibles() {
  try {
    const response = await axios.get('/apiAdmin/permisos/');
    this.permisosDisponibles = response.data;
  } catch (error) {
    console.error('Error al obtener los permisos disponibles:', error);
  }
},

    // Agregar un permiso al grupo
    agregarPermiso(permiso) {
      this.permisosAsignados.push(permiso); // Agregar al panel derecho
      this.permisosDisponibles = this.permisosDisponibles.filter(p => p.id !== permiso.id); // Quitar del panel izquierdo
    },

    // Quitar un permiso del grupo
    quitarPermiso(permiso) {
      this.permisosDisponibles.push(permiso); // Agregar al panel izquierdo
      this.permisosAsignados = this.permisosAsignados.filter(p => p.id !== permiso.id); // Quitar del panel derecho
    },

    // Enviar el formulario
    async submitForm() {
  if (!this.validateForm()) {
    return;
  }
  this.$store.commit('setIsLoading', true);
  const grupo_id = this.$route.params.id;
  try {
    const permisos_ids = this.permisosAsignados.map(p => p.id);
    await axios.patch(`/apiAdmin/editar-grupo/${grupo_id}/edit/`, {
      name: this.grupo.name,
      permissions: permisos_ids,
    });
    this.$router.push('/groups');
    Swal.fire('Actualizado!', 'El grupo ha sido modificado exitosamente.', 'success');
  } catch (error) {
    console.error('Error al actualizar el grupo:', error);
    Swal.fire('Error', 'Hubo un error al actualizar el grupo.', 'error');
  } finally {
    this.$store.commit('setIsLoading', false);
  }
},

    // Validar el formulario
    validateForm() {
      const nombre_regex = /^[A-Z][A-Za-záíóúé\s]{2,49}$/;
      if (!nombre_regex.test(this.grupo.name)) {
        this.nombre_error = 'Este campo comienza con mayúscula admite letras y espacios. Tamaño mínimo 3 caracteres y tamaño máximo 50 caracteres.';
        return false;
      }
      this.nombre_error = null;
      return true;
    },
  },
};
</script>