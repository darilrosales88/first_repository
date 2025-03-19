<template> 
  
  <router-view/>
</template>
<script>
//la siguiente url es para incluir la librería de Bootstrap Icons en el proyecto, se desdcargó  y 
// esta offline en la ruta ...\src\assets\bootstrap-icons
import '@/assets/bootstrap-icons/bootstrap-icons.css';
import axios from 'axios'

    export default {
        name: 'App',
        components: {
           
        }, 
        beforeCreate(){/*para que se ejecute la funcion InitializeStore de la ruta store/index.js */
          this.$store.commit('initializeStore')
          if (this.$store.state.token) {/*estamos preguntando si se esta autenticado para igualar a axios.defaults.headers.common['Authorization']
                                        el valor del token, de la forma Token 89545nj34kj5jh453y495, por poner un ejemplo*/
                axios.defaults.headers.common['Authorization'] = "Token " + this.$store.state.token
            } else {
                axios.defaults.headers.common['Authorization'] = ""/*en caso contrario el valor de axios.defaults.headers.common['Authorization']
                                                                    es nulo */
            }

            /* if (!this.$store.state.team.id) {
                this.$router.push('/dashboard/add-team')
            } */
        }       
    }
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
