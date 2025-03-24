<template>
    <div style="background-color: #002A68; color: white; text-align: right; padding: 10px;">
      <h6>Bienvenido: {{ username }}</h6>
    </div>
    <br />
    <Navbar-Component /><br>

    <div style="margin-left:12em">
    <!-- Navbar con enlaces -->
    <nav>
      <ul>
        <li>
          <a
            href="#"
            @click.prevent="currentComponent = 'PorSituarCarga_Descarga'"
            :class="{ active: currentComponent === 'PorSituarCarga_Descarga' }"
          >
            Por Situar Carga/Descarga
          </a>
        </li>
        <li>
          <a
            href="#"
            @click.prevent="currentComponent = 'SituadoCarga_Descarga'"
            :class="{ active: currentComponent === 'SituadoCarga_Descarga' }"
          >
            Situado Carga/Descarga
          </a>
        </li>
        <li>
          <a
            href="#"
            @click.prevent="currentComponent = 'Cargados_Descargados'"
            :class="{ active: currentComponent === 'Cargados_Descargados' }"
          >
            Cargados
          </a>
        </li>
        <li>
          <a
            href="#"
            @click.prevent="currentComponent = 'PendientesArrastre'"
            :class="{ active: currentComponent === 'PendientesArrastre' }"
          >
            Pendientes
          </a>
        </li>
        <li>
          <a
            href="#"
            @click.prevent="currentComponent = 'EnTrenes'"
            :class="{ active: currentComponent === 'EnTrenes' }"
          >
            En Trenes
          </a>
        </li>
      </ul>
    </nav>

    <!-- Contenedor para las tablas -->
    <div>
      <component :is="currentComponent" />
    </div>
  </div>


</template>

<style scoped>
/* Estilos generales del navbar */
nav ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 15px;
  background-color: #f8f9fa; /* Fondo claro para el navbar */
  padding: 10px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Sombra suave */
}

nav ul li {
  display: inline;
}

/* Estilos base de los enlaces */
a {
  text-decoration: none;
  color: #333; /* Color de texto oscuro */
  cursor: pointer;
  padding: 10px 20px;
  border-radius: 5px;
  transition: all 0.3s ease;
  font-weight: 500;
  display: inline-block;
}

/* Estilo cuando el usuario pasa el mouse sobre el enlace */
a:hover {
  background-color: #e9ecef; /* Gris muy claro */
  color: #000; /* Color del texto */
  transform: translateY(-2px); /* Efecto de levantar */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Sombra más pronunciada */
}

/* Estilo para el enlace seleccionado */
a.active {
  background-color: #007bff; /* Azul */
  color: #fff; /* Texto blanco */
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3); /* Sombra azul */
  transform: translateY(-2px); /* Efecto de levantar */
}

/* Efecto al hacer clic */
a:active {
  transform: translateY(0); /* Vuelve a su posición original */
}
</style>



<style scoped>
nav ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 10px;
}

nav ul li {
  display: inline;
}

a {
  text-decoration: none;
  color: inherit;
  cursor: pointer;
}
</style>


<script>
import NavbarComponent from '@/components/NavbarComponent.vue'
import PorSituarCarga_Descarga from '@/components/PorSituarCarga_Descarga.vue';
import SituadoCarga_Descarga from '@/components/SituadoCarga_Descarga.vue';
import Cargados_Descargados from '@/components/Cargados_Descargados.vue';
import PendientesArrastre from '@/components/PendientesArrastre.vue';
import EnTrenes from '@/components/EnTrenes.vue';

export default {
  name: 'UFCView',
  components: {
    NavbarComponent,
    PorSituarCarga_Descarga,
    SituadoCarga_Descarga,
    Cargados_Descargados,
    PendientesArrastre,
    EnTrenes,
  },
  data() {
    return {
      currentComponent: 'PorSituarCarga_Descarga', // Componente inicial
    };
  },
};
</script>