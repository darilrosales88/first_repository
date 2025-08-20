<template>
    <NavbarComponent />
    <div style="margin-left: 25em; width: 60%">
        <FechaOperacion />
    </div>
    <div style="margin-left: 16em; width: 80%">
        <!-- Navbar con enlaces -->
        <nav>
            <ul>
                <li>
                    <a href="#" @click.prevent="currentComponent = 'TablePorSituar'"
                        :class="{ active: currentComponent === 'TablePorSituar' }"> Por Situar Carga/Descarga
                    </a>
                </li>
                <li>
                    <a href="#" @click.prevent="currentComponent = 'TableSituados'"
                        :class="{ active: currentComponent === 'TableSituados' }">Situado Carga/Descarga
                    </a>
                </li>
                <li>
                    <a href="#" @click.prevent="currentComponent = 'TableCargaDescarga'"
                        :class="{ active: currentComponent === 'TableCargaDescarga' }">Cargados
                    </a>
                </li>
                <li>
                    <a href="#" @click.prevent="currentComponent = 'TablePendienteArrastre'"
                        :class="{ active: currentComponent === 'TablePendienteArrastre' }">Pendientes
                    </a>
                </li>
                <li>
                    <a href="#" @click.prevent="currentComponent = 'TableEnTren'"
                        :class="{ active: currentComponent === 'TableEnTren' }">En Trenes
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

<script>
import NavbarComponent from "@/components/NavbarComponent.vue";
import FechaOperacion from "@/components/CCDxProductosComponents/FechaOperacionComponent.vue";
import TablePorSituar from "@/components/CCDxProductosComponents/TablePorSituar.vue";
import TableSituados from "@/components/CCDxProductosComponents/TableSituados.vue";
import TableCargaDescarga from "@/components/CCDxProductosComponents/TableCargaDescarga.vue";
import TablePendienteArrastre from "@/components/CCDxProductosComponents/TablePendienteArrastre.vue";
import TableEnTren from "@/components/CCDxProductosComponents/TableEnTren.vue";


export default {
  name: "CCDxProductoView",
  
  components: {
    NavbarComponent,
    FechaOperacion,
    TablePorSituar,
    TableSituados,
    TableCargaDescarga,
    TablePendienteArrastre,
    TableEnTren,
  },
  data() {
    return {
        currentComponent: "TablePorSituar",
        username: "", // Variable para almacenar el nombre del usuario
    };
  },
  created() {
    // Obtener el nombre del usuario desde localStorage al cargar el componente
    this.username = localStorage.getItem("username") || "Invitado";
  },
};
</script>
<style scoped>

.action-buttons {
  display: flex;
  gap: 15px;
  margin: 30px auto; /* Centrado vertical y horizontal */
  justify-content: center; /* Centra los botones horizontalmente */
  padding: 20px 0;
  width: 100%;
}

.action-btn {
  padding: 12px 25px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 120px;
}

/* Estilos específicos para cada botón */
.approve {
  background-color: #28a745;
  color: white;
}

.approve:hover {
  background-color: #218838;
}

.reject {
  background-color: #dc3545;
  color: white;
}

.reject:hover {
  background-color: #c82333;
}

.ready {
  background-color: #17a2b8;
  color: white;
}

.ready:hover {
  background-color: #138496;
}

.action-btn i {
  margin-right: 8px;
  font-size: 18px;
}
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
nav a:hover {
  background-color: #e9ecef; /* Gris muy claro */
  color: #000; /* Color del texto */
  transform: translateY(-2px); /* Efecto de levantar */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Sombra más pronunciada */
}

/* Estilo para el enlace seleccionado */
nav a.active {
  background-color: #007bff; /* Azul */
  color: #fff; /* Texto blanco */
  box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3); /* Sombra azul */
  transform: translateY(-2px); /* Efecto de levantar */
}

/* Efecto al hacer clic */
nav a:active {
  transform: translateY(0); /* Vuelve a su posición original */
}

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
