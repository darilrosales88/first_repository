import { createStore } from "vuex";
import Vue from "vue";

export default createStore({
  state: {
    isLoading: false, //variable para la barra de carga
    isAuthenticated: false,
    token: "",
    user: {
      id: 0,
      username: "",
      role: "", // Nuevo campo para el rol
    },
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem("token")) {
        /*aqui estamos preguntando si se tiene almacenado el token en el navegador */
        state.token = localStorage.getItem("token");
        state.isAuthenticated = true; /*cambiando el valor del estado de autenticado a true */
        state.user.username = localStorage.getItem("username");
        state.user.id = localStorage.getItem("userid");
        state.user.role = localStorage.getItem("role"); // Recuperar el rol desde localStorage
        console.log(state.user.username);
      } else {
        /*en caso de no estar autenticado poner la variable del token a vacio, el estado autenticado a falso */
        state.token = "";
        state.isAuthenticated = false;
        state.user.id = 0;
        state.user.username = "";
        state.user.role = ""; // Resetear el rol si no hay autenticación
      }
    },
    setAuthentication(state, value) {
      state.isAuthenticated = value;
    },
    setIsLoading(state, status) {
      /*cambiando el estado de carga */
      state.isLoading = status;
    },
    setToken(state, token) {
      /*funcion para modificar el token, cuando se está autenticado */
      state.token = token;
      state.isAuthenticated = true;
    },
    removeToken(state) {
      /*funcion para eliminar el token, se pone en falso la autenticacion, estas funciones seran usadas al abrir la app
                        por lo que se llamara a la misma desde App.vue */
      state.token = "";
      state.isAuthenticated = false;
    },
    setUser(state, user) {
      state.user = user;
    },
    setRole(state, role) {
      state.user.role = role; // Establecer el rol del usuario
    },
  },
  actions: {},
  modules: {},
});
