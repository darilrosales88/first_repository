<template>
  <div class="form-container">
    <h2>Editar Usuario {{ username }}</h2>
    <form @submit.prevent="updateUser">
      <!-- Campos existentes -->
      <div class="form-group">
        <label for="first_name">Nombre</label>
        <input type="text" v-model="first_name" required />
      </div>

      <div class="form-group">
        <label for="last_name">Apellidos</label>
        <input type="text" v-model="last_name" required />
      </div>

      <div class="form-group">
        <label for="username">Nombre de usuario</label>
        <input type="text" v-model="username" required />
      </div>

      <div class="form-group">
        <label for="email">Correo electrónico</label>
        <input type="email" v-model="email" required />
      </div>

      <div class="form-group">
        <label for="entidad">Entidad</label>
        <select v-model="entidad" required>
          <option v-for="entidad in entidades" :value="entidad.id" :key="entidad.id">
            {{ entidad.nombre }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="cargo">Cargo</label>
        <select v-model="cargo" required>
          <option v-for="cargo in cargos" :value="cargo.id" :key="cargo.id">
            {{ cargo.nombre_cargo }}
          </option>
        </select>
      </div>

      <div class="form-group">
      <label for="password">Contraseña (opcional)</label>
      <input 
        type="password" 
        v-model="password" 
        :class="{ 'input-error': !passwordsMatch && password && confirmPassword, 'input-success': passwordsMatch }"
        placeholder="Dejar en blanco para no cambiar"
      />
    </div>

    <div class="form-group">
      <label for="confirmPassword">Confirmar contraseña (opcional)</label>
      <input 
        type="password" 
        v-model="confirmPassword" 
        :class="{ 'input-error': !passwordsMatch && password && confirmPassword, 'input-success': passwordsMatch }"
        placeholder="Dejar en blanco para no cambiar"
      />
    </div>

      <!-- campo rol añadido -->
      <div class="form-group">
        <label for="role">Rol</label>
        <select v-model="role" required>
          <option value="operador">Operador</option>
          <option value="ufc">UFC</option>
          <option value="admin">Administrador</option>
        </select>
      </div>

      <!-- Contenedor principal para grupos y permisos -->
      <div class="groups-permissions-container">
        <!-- Contenedor de grupos -->
        <div class="groups-container">
          <div class="groups-panel">
            <h3>Grupos Disponibles</h3>
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

          <div class="arrow-container">
            <i class="fas fa-arrows-alt-h"></i>
          </div>

          <div class="groups-panel">
            <h3>Grupos Asignados</h3>
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

          <div class="arrow-container">
            <i class="fas fa-arrows-alt-h"></i>
          </div>

          <div class="permissions-panel">
            <h3>Permisos Asignados</h3>
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
        <button type="submit">Actualizar</button>
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
</style>

<script>
import Swal from 'sweetalert2';
import axios from 'axios';

export default {
  data() {
    return {
      first_name: '',
      last_name: '',
      username: '',
      email: '',
      entidad: '',
      entidades: [],
      cargo: '',
      cargos: [],      
      role: 'operador', // Valor por defecto para el rol
      password: '',
      confirmPassword: '',
      groupsDisponibles: [],
      groupsAsignados: [],
      permisosDisponibles: [],
      permisosAsignados: [],
      searchDisponibles: '',
      searchAsignados: '',
      searchGruposDisponibles: '',
      searchGruposAsignados: '',
      passwordsMatch: false,
    };
  },
  computed: {
    permisosDisponiblesFiltrados() {
      return this.permisosDisponibles.filter(permiso =>
        permiso.name.toLowerCase().includes(this.searchDisponibles.toLowerCase())
      );
    },
    permisosAsignadosFiltrados() {
      return this.permisosAsignados.filter(permiso =>
        permiso.name.toLowerCase().includes(this.searchAsignados.toLowerCase())
      );
    },
    gruposDisponiblesFiltrados() {
      return this.groupsDisponibles.filter(group =>
        group.name.toLowerCase().includes(this.searchGruposDisponibles.toLowerCase())
      );
    },
    gruposAsignadosFiltrados() {
      return this.groupsAsignados.filter(group =>
        group.name.toLowerCase().includes(this.searchGruposAsignados.toLowerCase())
      );
    },
  },
  watch: {
    password(newVal) {
      this.validatePasswords();
    },
    confirmPassword(newVal) {
      this.validatePasswords();
    },
  },
  mounted() {
    this.fetchGroups();
    this.fetchPermisosDisponibles();
    this.getEntidades();
    this.getCargos();
    this.fetchUser();
  },
  methods: {
    async fetchGroups() {
      try {
        const response = await axios.get('/apiAdmin/groups/');
        this.groupsDisponibles = response.data.results;
      } catch (error) {
        console.error('Error al obtener los grupos:', error);
        Swal.fire('Error', 'No se pudieron cargar los grupos.', 'error');
      }
    },
    async fetchPermisosDisponibles() {
      try {
        const response = await axios.get('/apiAdmin/permisos/');
        this.permisosDisponibles = response.data;
      } catch (error) {
        console.error('Error al obtener los permisos:', error);
        Swal.fire('Error', 'No se pudieron cargar los permisos.', 'error');
      }
    },
    async getEntidades() {
      try {
        const response = await axios.get('/api/entidades/');
        this.entidades = response.data.results;
      } catch (error) {
        console.error('Error al obtener las entidades:', error);
      }
    },
    async getCargos() {
      try {
        const response = await axios.get('/api/cargos/');
        this.cargos = response.data.results;
      } catch (error) {
        console.error('Error al obtener los cargos:', error);
      }
    },
    async fetchUser() {
      const userId = this.$route.params.id;
      try {
        const response = await axios.get(`/apiAdmin/obtener-usuario/${userId}/`);
        const user = response.data;
        this.first_name = user.first_name;
        this.last_name = user.last_name;
        this.username = user.username;
        this.email = user.email;
        this.entidad = user.entidad.id;
        this.cargo = user.cargo.id;
        this.groupsAsignados = user.groups || [];
        this.permisosAsignados = user.user_permissions || [];
        this.groupsDisponibles = this.groupsDisponibles.filter(
          group => !this.groupsAsignados.some(g => g.id === group.id)
        );
        this.permisosDisponibles = this.permisosDisponibles.filter(
          permiso => !this.permisosAsignados.some(p => p.id === permiso.id)
        );
      } catch (error) {
        console.error('Error al obtener los datos del usuario:', error);
        Swal.fire('Error', 'No se pudieron cargar los datos del usuario.', 'error');
      }
    },
    agregarGrupo(group) {
      this.groupsAsignados.push(group);
      this.groupsDisponibles = this.groupsDisponibles.filter(g => g.id !== group.id);
    },
    quitarGrupo(group) {
      this.groupsDisponibles.push(group);
      this.groupsAsignados = this.groupsAsignados.filter(g => g.id !== group.id);
    },
    agregarPermiso(permiso) {
      this.permisosAsignados.push(permiso);
      this.permisosDisponibles = this.permisosDisponibles.filter(p => p.id !== permiso.id);
    },
    quitarPermiso(permiso) {
      this.permisosDisponibles.push(permiso);
      this.permisosAsignados = this.permisosAsignados.filter(p => p.id !== permiso.id);
    },
    validatePasswords() {
      if (this.password && this.confirmPassword) {
        this.passwordsMatch = this.password === this.confirmPassword;
      } else {
        this.passwordsMatch = false;
      }
    },
    validateForm() {
      const nombre_regex = /^[A-ZÁÉÍÓÚ][a-záéíóúñ]+(?:\s[A-ZÁÉÍÓÚ][a-záéíóúñ]+)*$/;
      const apellidos_regex = /^[A-ZÁÉÍÓÚ][a-záéíóúñ]+(?:\s[A-ZÁÉÍÓÚ][a-záéíóúñ]+)*$/;
      const username_regex = /^[A-Za-z0-9_]{4,30}$/;
      const email_regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      const password_regex = /^.{8,}$/;

      let valid = true;

      if (!nombre_regex.test(this.first_name)) {
        Swal.fire('Error', 'El nombre debe comenzar con mayúscula y solo contener letras (puede ser compuesto).', 'error');
        valid = false;
      }

      if (!apellidos_regex.test(this.last_name)) {
        Swal.fire('Error', 'Los apellidos deben comenzar con mayúscula y solo contener letras (pueden ser compuestos).', 'error');
        valid = false;
      }

      if (!username_regex.test(this.username)) {
        Swal.fire('Error', 'El nombre de usuario debe tener entre 4 y 30 caracteres (solo letras, números y guiones bajos).', 'error');
        valid = false;
      }

      if (!email_regex.test(this.email)) {
        Swal.fire('Error', 'Ingrese un correo electrónico válido.', 'error');
        valid = false;
      }

      // Validaciones condicionales para contraseña
      if (this.password || this.confirmPassword) {
        if (this.password && !password_regex.test(this.password)) {
          Swal.fire('Error', 'La contraseña debe tener al menos 8 caracteres.', 'error');
          valid = false;
        }

        if (this.password !== this.confirmPassword) {
          Swal.fire('Error', 'Las contraseñas no coinciden.', 'error');
          valid = false;
        }
      }

      return valid;
    },
    async updateUser() {
      if (!this.validateForm()) {
        return;
      }

      this.$store.commit('setIsLoading', true);
      const userId = this.$route.params.id;
      const userData = {
        first_name: this.first_name,
        last_name: this.last_name,
        username: this.username,
        email: this.email,
        entidad: this.entidad,
        cargo: this.cargo,
        role: this.role,
        groups: this.groupsAsignados.map(g => g.id),
        user_permissions: this.permisosAsignados.map(p => p.id),
      };

      // Solo incluir la contraseña si se proporcionó
      if (this.password) {
        userData.password = this.password;
      }

      try {
        await axios.patch(`/apiAdmin/editar-usuario/${userId}/`, userData);
        this.$router.push('/Usuarios');
        Swal.fire('Actualizado!', 'El usuario ha sido actualizado exitosamente.', 'success');
      } catch (error) {
        console.log(error);
        Swal.fire('Error', 'Hubo un error al actualizar el usuario.', 'error');
      } finally {
        this.$store.commit('setIsLoading', false);
      }
    },
  },
};
</script>