<template>
    <div style="background-color: #002A68; color: white; text-align: right; padding: 10px;">
      <h6>Bienvenido:</h6>
    </div>
    <br />
    <Navbar-Component />
    <br>
    <h3>Registro de partes de UFC</h3>
    <br>
    <br>
      
      <router-link style="margin-right:1em" to="/InfoOperative" class="btn btn-primary">Informe Operativo</router-link>
      <router-link style="margin-right: 28em;" to="#" class="btn btn-primary" role="button" data-bs-toggle="button">CCD por producto</router-link>
      
      
</template>
  
<script>
  import NavbarComponent from '@/components/NavbarComponent.vue';
  
  export default {
    name: 'UFCView',
    components: {
      NavbarComponent,
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