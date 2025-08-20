<template>        
    <div class="user-info">
      <p class="mb-0 me-3">Bienvenido, <b>{{ user_autenticado }}</b> /
        <a @click="logout()" class="logout-link">Cerrar sesión
          <i class="bi bi-box-arrow-right"></i>  <!-- Ícono de cierre de sesión -->
        </a> 
      </p>
    </div> 
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'user_autenticado',
    async created() {
      await this.datos_usuario_autenticado();
    },
    data() {
      return {
        user_autenticado: '',
      };
    },
    methods: {
      async datos_usuario_autenticado() {
        try {
          const userId = localStorage.getItem('userid');
          if (userId) {
            const response = await axios.get(`/api/user/${userId}/permissions-and-groups/`);
            this.user_autenticado = response.data.first_name;
          }
        } catch (error) {
          console.error('Error al obtener los datos del usuario:', error);
        }
      },
      async logout() {
        try {
          await axios.post('/api/v1/token/logout/');
          console.log('Logged out');
          // Eliminar los tokens y redirigir al inicio de sesión
          axios.defaults.headers.common['Authorization'] = '';
          localStorage.removeItem('token');
          localStorage.removeItem('username');
          localStorage.removeItem('userid');
          this.$store.commit('removeToken');
          this.$router.push("/");
        } catch (error) {
          console.log(JSON.stringify(error));
        }
      },
    },
  };
  </script>  

<style scoped>
.user-info {
  text-align: right;
  padding: 10px;
}

.user-info p {
  display: inline-block;
  background-color: #f8f9fa;  /* Fondo gris claro */
  padding: 10px 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.logout-link {
  color: #007bff;
  font-weight: bold;
  text-decoration: none;
}

.logout-link:hover {
  color: #0056b3;
  text-decoration: underline;
}

.logout-link i {
  margin-left: 5px;
}
</style>
  