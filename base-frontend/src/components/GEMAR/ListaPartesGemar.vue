<template>
  <NavbarComponent />
  <div style="margin-left: 16em; width: 80%">
     <RegistrosPartesGEMAR /> 
  </div>

</template>

<script>
import NavbarComponent from "@/components/NavbarComponent.vue";
import RegistrosPartesGEMAR from "@/components/GEMAR/RegistrosPartesGemar.vue";

export default {
  name: "ListaPartesGemar",
  components: {
    NavbarComponent,
    RegistrosPartesGEMAR,
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
