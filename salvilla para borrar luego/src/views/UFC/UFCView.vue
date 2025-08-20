<template>

  <NavbarComponent />
  <div style="margin-left: 16em; width: 80%">
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
