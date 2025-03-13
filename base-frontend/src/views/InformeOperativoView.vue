<template>
  <div>
    <img style="width: 250px" src="@/assets/Imagenes/mitrans.png" />
    <Navbar-Component />
    <EnTrenes />
    <!-- Contenedor de la tabla con scroll horizontal 
     La clase table-responsive de Bootstrap envuelve la tabla y permite el scroll horizontal cuando el contenido excede el 
     ancho disponible.La tabla no debe tener  un ancho fijo, sino que se ajusta automáticamente al contenido.-->
  </div>
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";
import NavbarComponent from "@/components/NavbarComponent.vue";
import EnTrenes from "@/components/EnTrenes.vue";

export default {
  name: "InformeOperativoView",

  components: {
    NavbarComponent,
    EnTrenes,
  },

  methods: {},
};
</script>

<style scoped>
.search-container {
  padding: 10px;
}
li {
  margin-top: 0.1%;
  scale: 0.75;
  padding-right: 80%;
}

.search-form {
  display: flex;

  margin-right: 50%;
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
