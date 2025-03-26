<template>
    <div class="container">
      <!-- Fila para el icono y el buscador -->
      <div class="d-flex justify-content-between align-items-center mb-3">
        <!-- Icono de agregar (a la izquierda) -->
        <button class="btn btn-link p-0" @click="showModal = true">
          <i class="bi bi-plus-circle fs-3"></i> <!-- Icono grande -->
        </button>
  
        <!-- Buscador (a la derecha) -->
        <div class="search-container">
          <input
            type="text"
            class="form-control"
            placeholder="Buscar..."
            v-model="searchQuery"
            @input="filterTable"
          />
          <i class="bi bi-search search-icon"></i> <!-- Icono de lupa -->
        </div>
      </div>
  
      <!-- Tabla -->
      <table class="table table-responsive">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Origen</th>
            <th scope="col">Tipo de equipo</th>
            <th scope="col">Estado</th>
            <th scope="col">Operacion</th>
            <th scope="col">Producto</th>
            <th scope="col">Situados</th>
            <th scope="col">Dias</th>
            <th scope="col">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in situados" :key="item.id">
            <th scope="row">{{ (index + 1) }}</th>
            <td>{{ item.tipo_origen }}</td>
            <td>{{ item.tipo_equipo }}</td>
            <td>{{ item.estado }}</td>
            <td>{{ item.operacion }}</td>
            <td>{{ item.producto }}</td>
            <td>{{ item.situados }}</td>
            <td>{{ item.pendiente_proximo_dia }}</td>
            <td>
              <button class="btn btn-warning btn-small">
                <router-link to="">
                  <i style="color: black" class="bi bi-pencil-square"></i>
                </router-link>
              </button>
              <button style="margin-left:1em" class="btn btn-danger btn-small">
                <i class="bi bi-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <!-- Modal para agregar nuevos datos -->
      <div v-if="showModal" class="modal-backdrop">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Agregar nuevo registro</h5>
            <button type="button" class="btn-close" @click="showModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addNewItem">
              <div class="mb-3">
                <label for="origen" class="form-label">Origen</label>
                <input type="text" class="form-control" id="origen" v-model="newItem.origen" required />
              </div>
              <div class="mb-3">
                <label for="tipoEquipo" class="form-label">Tipo de equipo</label>
                <input type="text" class="form-control" id="tipoEquipo" v-model="newItem.tipoEquipo" required />
              </div>
              <div class="mb-3">
                <label for="estado" class="form-label">Estado</label>
                <input type="text" class="form-control" id="estado" v-model="newItem.estado" required />
              </div>
              <div class="mb-3">
                <label for="operacion" class="form-label">Operacion</label>
                <input type="text" class="form-control" id="operacion" v-model="newItem.operacion" required />
              </div>
              <div class="mb-3">
                <label for="producto" class="form-label">Producto</label>
                <input type="text" class="form-control" id="producto" v-model="newItem.producto" required />
              </div>
              <div class="mb-3">
                <label for="situados" class="form-label">Situados</label>
                <input type="text" class="form-control" id="situados" v-model="newItem.situados" required />
              </div>
              <div class="mb-3">
                <label for="dias" class="form-label">Dias</label>
                <input type="text" class="form-control" id="dias" v-model="newItem.dias" required />
              </div>
                <button style="margin-right:1em" type="submit" class="btn btn-primary btn-sm">Agregar</button>
                <button type="button" class="btn btn-secondary btn-sm"  @click="showModal = false">Cancelar</button>
              
              
            </form>
          </div>
        </div>
      </div>
    </div>
</template>
  
  <script>
import Swal from "sweetalert2";
import axios from "axios";
  export default {
    data() {
      return {
        searchQuery: "", // Query de búsqueda
        situados: [],
        debounceTimeout: null, // Añadido aquí
        busqueda_existente: true, // Variable para controlar la visibilidad del mensaje de búsqueda
        userPermissions: [], // Almacenará los permisos del usuario
        userGroups: [],      // Almacenará los grupos del usuario
      };
    },
    
    mounted(){
      this.getSituados();
    },

    methods: {
      getSituados(){
        axios.get('http://127.0.0.1:8000/api/situados/')
        .then((response)=>{
          console.log(response.data)
          this.situados = response.data
        })
      }
    },
  };
  </script>
  
  <style scoped>
  /* Estilos para el contenedor del buscador */
  .search-container {
    position: relative;
    width: 100%;
    max-width: 300px; /* Ancho máximo del buscador */
  }
  
  /* Estilos para el input del buscador */
  .search-container input {
    padding-right: 40px; /* Espacio para el icono de lupa */
    border-radius: 20px; /* Bordes redondeados */
  }
  
  /* Estilos para el icono de lupa */
  .search-icon {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    color: #888; /* Color del icono */
    pointer-events: none; /* Evita que el icono interfiera con el input */
  }
  
  /* Estilos para la tabla responsive */
  .table-responsive {
    overflow-x: auto; /* Permite desplazamiento horizontal en pantallas pequeñas */
  }
  
  /* Estilos para el modal */
  .modal-backdrop {
    
    top: 0;
    left: 0;
    width: 100%;
    height: 90%;
    background-color: transparent; /* Fondo semitransparente */
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000; /* Asegura que el modal esté por encima de todo */
  }
  
  .modal-content {
    background-color: #fff;
    padding: 20px;
    border-radius: 10px;
    width: 90%;
    max-width: 500px; /* Ancho máximo del modal */
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #ddd;
    padding-bottom: 10px;
    margin-bottom: 20px;
  }
  
  .modal-title {
    margin: 0;
  }
  
  .btn-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
  }
  
  .modal-body {
    margin-bottom: 20px;
  }
  
  /* Estilos para el icono de agregar */
  .btn-link {
    color: #007bff; /* Color azul para el icono */
    text-decoration: none; /* Sin subrayado */
  }
  
  .btn-link:hover {
    color: #0056b3; /* Color azul más oscuro al pasar el mouse */
  }
  </style>