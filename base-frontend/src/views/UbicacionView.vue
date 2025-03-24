<template>
    <img style="width: 250px ;" src="@/assets/Imagenes/mitrans.png">
    <Navbar-Component />
    <br>
    <div class="create-button-container">
    <router-link
      class="create-button"
      to="/CrearUbicacion"
    >
      Crear nueva ubicación <i class="bi bi-plus-circle"></i>
    </router-link>
  </div>
<br>
<br>
<table class="table">
  <thead>
    <tr>
      <th scope="col">No</th>
      <th scope="col">Tipo de estructura de ubicaci&oacute;n</th>
      <th scope="col">Acciones</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="(item, index) in nombres_tipos_estructuras_ubicacion">
      <th scope="row">{{ item.id }}</th>
      <td>{{ item.nombre_tipo_estructura_ubicacion }}</td>
      
      <td>
        <button class="btn btn-danger"> 
          <router-link style="color:black" to="">
            <i style="color:white" class="bi bi-trash"></i>
          </router-link>
          </button> 
          <button style="margin-left:10px" class="btn btn-warning">
          <router-link to="">
            <i style="color:white" class="bi bi-pencil-square"></i>
          </router-link>
          </button>
      </td>
    </tr>
  </tbody>
  </table>
</template>
<style scoped>
.create-button-container {
  text-align: left;
}

.create-button {
  text-decoration: none;
  color: black;
}

@media (max-width: 768px) {
  .create-button-container {
    text-align: left;
    margin-right: 0;
  }
}
</style>

<script>
import axios from 'axios';
import NavbarComponent from '@/components/NavbarComponent.vue';

    export default {
      name: 'UbicacionView',
      components:{
        NavbarComponent
      },
      data(){
        return{
          nombres_tipos_estructuras_ubicacion:[],
        }
      },

      mounted(){
        this.getUbicacion();
      },

      methods:{
        getUbicacion(){
          axios.get('http://127.0.0.1:8000/tipos_estructuras_ubicacion/')
          .then(response =>{
            this.nombres_tipos_estructuras_ubicacion = response.data
          })
          .catch(error =>{
            console.log(error)
          })
        }
      }
    }
</script>