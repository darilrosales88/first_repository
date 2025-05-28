<template>
  <div
    style="
      background-color: #002a68;
      color: white;
      text-align: right;
      padding: 1px;
    "
  >
    <h6>Bienvenido:</h6>
  </div>
  <br />
  <NavbarComponent />
  <br />
  <h3>Registro de partes de UFC</h3>
  <br />
  <br />

  <router-link
    style="margin-right: 1em"
    to="/InfoOperativo"
    class="btn btn-primary"
    >Informe Operativo</router-link
  >
  <router-link
    style="margin-right: 28em"
    to="#"
    class="btn btn-primary"
    role="button"
    data-bs-toggle="button"
    >CCD por producto</router-link
  >
  <div class="d-flex justify-content-center">
    <RegistrosPartesUFC />
  </div>
</template>

<script>
import NavbarComponent from "@/components/NavbarComponent.vue";
import RegistrosPartesUFC from "@/components/RegistrosPartesUFC.vue";

export default {
  name: "UFCView",
  components: {
    NavbarComponent,
    RegistrosPartesUFC,
  },
  data() {
    return {
      username: "", // Variable para almacenar el nombre del usuario
    };
  },
  created() {
    // Obtener el nombre del usuario desde localStorage al cargar el componente
    this.username = localStorage.getItem("username") || "Invitado";
  },
};
</script>
