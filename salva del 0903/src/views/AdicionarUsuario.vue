<template>
  <div class="form-container">
    <h2>Adicionar Usuario</h2>
    <form @submit.prevent="saveUser">
      <!-- Campos existentes -->
      <div class="form-group">
        <label for="username">Nombre</label>
        <input type="text" v-model="first_name" required />
        
      </div>

      <div class="form-group">
        <label for="username">Apellidos</label>
        <input type="text" v-model="last_name" required />
        
      </div>

      <div class="form-group">
        <label for="username"> usuario</label>
        <input type="text" v-model="username" required />
      
      </div>

      <div class="form-group">
        <label for="email">Correo electrónico</label>
        <input type="email" v-model="email" required />

      </div>

      <div class="form-group">
        <label for="organismo">Entidad</label>
        <select v-model="entidad" required>
          <option v-for="entidad in entidades" :value="entidad.id" :key="entidad.id">
            {{ entidad.nombre }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="organismo">Cargo</label>
        <select v-model="cargo" required>
          <option v-for="cargo in cargos" :value="cargo.id" :key="cargo.id">
            {{ cargo.nombre_cargo }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="password">Contraseña</label>
        <input
          type="password"
          v-model="password"
          required
          :class="{ 'input-error': !passwordsMatch && password && confirmPassword, 'input-success': passwordsMatch }"
        />
      </div>

      <!-- Nuevo campo para confirmar la contraseña -->
      <div class="form-group">
        <label for="confirmPassword">Confirmar contraseña</label>
        <input
          type="password"
          v-model="confirmPassword"
          required
          :class="{ 'input-error': !passwordsMatch && password && confirmPassword, 'input-success': passwordsMatch }"
        />
      </div>

      <!-- Contenedor principal para grupos y permisos -->
      <div class="groups-permissions-container">
        <!-- Contenedor de grupos -->
        <div class="groups-container">
          <div class="groups-panel">
            <h3>Grupos Disponibles</h3>
            <!-- Campo de búsqueda -->
          <input
            type="text"
            v-model="searchGruposDisponibles"
            placeholder="Buscar grupos..."
            class="search-input"
          />
          <ul>
            <li
              v-for="group in gruposDisponiblesFiltrados"
              :key="group.id"
              @click="agregarGrupo(group)"
            >
              {{ group.name }}
            </li>
          </ul>
          </div>

          <!-- Flecha de doble punta -->
          <div class="arrow-container">
            <i class="fas fa-arrows-alt-h"></i> <!-- Ícono de flecha de doble punta -->
          </div>

          <div class="groups-panel">
            <h3>Grupos Asignados</h3>
            <!-- Campo de búsqueda -->
          <input
            type="text"
            v-model="searchGruposAsignados"
            placeholder="Buscar grupos..."
            class="search-input"
          />
          <ul>
            <li
              v-for="group in gruposAsignadosFiltrados"
              :key="group.id"
              @click="quitarGrupo(group)"
            >
              {{ group.name }}
            </li>
          </ul>
          </div>
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
      </div>

      <div class="form-buttons">
        <button type="button">
          <router-link style="color:white;text-decoration:none" to="/Usuarios">Cancelar</router-link>
        </button>
        <button type="submit">Aceptar</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.form-container {
  max-width: 1200px; /* Aumentar el ancho para acomodar ambos contenedores */
  margin: 50px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-height: 1050px;
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
  display: block; /* Cambiar a bloque para alinear todo a la izquierda */
  text-align: left; /* Alinear el contenido a la izquierda */
}

label {  
  font-weight: bold;
  margin-bottom: 10px; /* Espacio entre la etiqueta y el campo de entrada */
}

input,
select {
  width: 50%; /* Hacer que los campos de entrada ocupen el 100% del ancho */
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box; /* Incluir el padding en el ancho total */
  margin-left: 10px;
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

.groups-permissions-container {
  display: flex;
  gap: 20px; /* Espacio entre los contenedores de grupos y permisos */
}

.groups-container,
.permissions-container {
  flex: 1; /* Ambos contenedores ocupan el mismo espacio */
  display: flex;
  gap: 20px;
  max-height: 350px;
}

.groups-panel,
.permissions-panel {
  flex: 1;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #fff;
  max-height: 400px; /* Altura máxima para habilitar el scroll */
  overflow-y: auto; /* Habilita el scroll vertical */
  position: relative; /* Contexto para position: sticky */
}

.groups-panel h3,
.permissions-panel h3 {
  margin-top: 0;
  font-size: 16px;
  text-align: center;
  position: sticky;
  top: 0; /* Fija el h3 en la parte superior del contenedor */
  background-color: #fff; /* Fondo para que no se superponga con el contenido */
  z-index: 2; /* Asegura que el h3 esté por encima del input */
  padding: 10px 0;
  border-bottom: 1px solid #ccc;
}

.groups-panel ul,
.permissions-panel ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.groups-panel li,
.permissions-panel li {
  padding: 8px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.2s;
}

.groups-panel li:hover,
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

/* Estilos para la validación de contraseñas */
.input-error {
  border-color: red !important;
}

.input-success {
  border-color: green !important;
}
</style>

<script>
import Swal from 'sweetalert2';
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      first_name: '',
      last_name:'',
      email: '',
      entidad: '',
      entidades: [], // Almacena todas las entidades del nomenclador
      cargo:'',
      cargos: [], // Almacena todos los cargos del nomenclador
      password: '',
      confirmPassword: '', // Nuevo campo de confirmación
      errors: '',      
      groupsDisponibles: [],
      groupsAsignados: [],
      permisosDisponibles: [], 
      permisosAsignados: [], 
      searchDisponibles: '', // Texto de búsqueda para permisos disponibles
      searchAsignados: '', // Texto de búsqueda para permisos asignados
      searchGruposDisponibles: '', // Texto de búsqueda para grupos disponibles
      searchGruposAsignados: '', // Texto de búsqueda para grupos asignados
      passwordsMatch: false, // Nueva propiedad para validación de contraseñas
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
  // Filtra los grupos disponibles según el texto de búsqueda
  gruposDisponiblesFiltrados() {
      return this.groupsDisponibles.filter(group =>
        group.name.toLowerCase().includes(this.searchGruposDisponibles.toLowerCase())
      );
    },
    // Filtra los grupos asignados según el texto de búsqueda
    gruposAsignadosFiltrados() {
      return this.groupsAsignados.filter(group =>
        group.name.toLowerCase().includes(this.searchGruposAsignados.toLowerCase())
      );
    },
  },
  watch: {
    // Observadores para validar las contraseñas mientras el usuario escribe
    password(newVal) {
      this.validatePasswords();
    },
    confirmPassword(newVal) {
      this.validatePasswords();
    },
  },
  mounted() {
    this.fetchGroups(); // Obtener los grupos disponibles
    this.fetchPermisosDisponibles(); // Obtener los permisos disponibles
    this.getEntidades();//obtener todas las entidades del nomenclador
    this.getCargos();//obtener todas lod cargos del nomenclador
  },
  methods: {
    // Obtener la lista de grupos desde el backend
    async fetchGroups() {
      try {
        const response = await axios.get('/apiAdmin/groups/'); // Asegúrate de que esta ruta devuelva los grupos
        this.groupsDisponibles = response.data;
      } catch (error) {
        console.error('Error al obtener los grupos:', error);
        Swal.fire('Error', 'No se pudieron cargar los grupos.', 'error');
      }
    },

    // Obtener la lista de permisos disponibles desde el backend
    async fetchPermisosDisponibles() {
      try {
        const response = await axios.get('/apiAdmin/permisos/'); // Asegúrate de que esta ruta devuelva los permisos
        this.permisosDisponibles = response.data;
      } catch (error) {
        console.error('Error al obtener los permisos:', error);
        Swal.fire('Error', 'No se pudieron cargar los permisos.', 'error');
      }
    },

    // Mover un grupo de disponibles a asignados
    agregarGrupo(group) {
      this.groupsAsignados.push(group);
      this.groupsDisponibles = this.groupsDisponibles.filter(g => g.id !== group.id);
    },

    // Mover un grupo de asignados a disponibles
    quitarGrupo(group) {
      this.groupsDisponibles.push(group);
      this.groupsAsignados = this.groupsAsignados.filter(g => g.id !== group.id);
    },

    // Mover un permiso de disponibles a asignados
    agregarPermiso(permiso) {
      this.permisosAsignados.push(permiso);
      this.permisosDisponibles = this.permisosDisponibles.filter(p => p.id !== permiso.id);
    },

    // Mover un permiso de asignados a disponibles
    quitarPermiso(permiso) {
      this.permisosDisponibles.push(permiso);
      this.permisosAsignados = this.permisosAsignados.filter(p => p.id !== permiso.id);
    },
    async getEntidades() {
      try {
        const response = await axios.get('/api/entidades/');
        this.entidades = response.data;
      } catch (error) {
        console.error('Error al obtener la entidad:', error);
      }
    },
    async getCargos() {
      try {
        const response = await axios.get('/api/cargos/');
        this.cargos = response.data;
      } catch (error) {
        console.error('Error al obtener la entidad:', error);
      }
    },

    // Validar si las contraseñas coinciden
    validatePasswords() {
      if (this.password && this.confirmPassword) {
        this.passwordsMatch = this.password === this.confirmPassword;
      } else {
        this.passwordsMatch = false;
      }
    },

    validateForm() {
      this.errors='';
      const nombre_regex = /^[A-ZÁÉÍÓÚ][a-záéíóúñ]+(?:\s[A-ZÁÉÍÓÚ][a-záéíóúñ]+)*$/;
      const apellidos_regex = /^[A-ZÁÉÍÓÚ][a-záéíóúñ]+(?:\s[A-ZÁÉÍÓÚ][a-záéíóúñ]+)*$/;
      const username_regex = /^[A-Za-z0-9_]{4,30}$/;
      const email_regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      const organismo_regex = /^[A-Za-záéíóúñ\s]{3,100}$/;
      const password_regex = /^.{8,}$/;


      let valid = true;

      if (!nombre_regex.test(this.first_name)) {
        this.errors += 'El nombre debe comenzar con mayúscula y solo contener letras (puede ser compuesto).'+'\n';
        valid = false;
      }

      if (!apellidos_regex.test(this.last_name)) {
        this.errors += 'El campo Apellidos debe comenzar con mayúscula y solo contener letras (puede ser compuesto).'+'\n';
        valid = false;
      }

      if (!username_regex.test(this.username)) {
        this.errors += 'El nombre de usuario debe tener entre 4 y 30 caracteres (solo letras, números y guiones bajos).'+'\n';
        valid = false;
      }

      if (!email_regex.test(this.email)) {
        this.errors += 'Ingrese un correo electrónico válido.'+'\n';
        valid = false;
      }

      if (!organismo_regex.test(this.organismo)) {
        this.errors += 'El organismo debe tener entre 3 y 100 caracteres (solo letras y espacios).'+'\n';
        valid = false;
      }

      if (!password_regex.test(this.password)) {
        this.errors += 'La contraseña debe tener al menos 8 caracteres.'+'\n';
        valid = false;
      }

      if (this.password !== this.confirmPassword) {
        this.errors += 'Las contraseñas no coinciden.'+'\n';
        valid = false;
      }

      if (!valid) {
        Swal.fire('Error!', this.errors, 'error');       
      }

      return valid;
    },

    async saveUser() {
      if (!this.validateForm()) {
        return;
      }

      this.$store.commit('setIsLoading', true);
      const userData = {
          username: this.username,
          email: this.email,
          first_name: this.first_name,
          last_name: this.last_name,
          entidad: this.entidad, // Asegúrate de que sea un ID válido
          cargo: this.cargo, // Asegúrate de que sea un ID válido
          password: this.password,
          groups: this.groupsAsignados.map(g => g.id), // Grupos asignados
          permissions: this.permisosAsignados.map(p => p.id), // Permisos asignados
        };

      try {
        await axios.post('/apiAdmin/creacion-usuario/', userData);  // Envía los datos al backend
        this.$router.push('/Usuarios');
        Swal.fire('Agregado!', 'El usuario ha sido creado exitosamente.', 'success');
      } catch (error) {
        console.log(error);
        Swal.fire('Error', 'Hubo un error al crear el usuario.', 'error');
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    }
  },
};
</script>