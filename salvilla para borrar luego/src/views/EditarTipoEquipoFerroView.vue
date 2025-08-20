<template>
  <div>
    <div style=" background-color: #002A68; color: white; text-align: right;">
      <h6>Bienvenido:</h6>
    </div>  
    <br />
    <Navbar-Component />
    
    <div class="form-container" style="margin-left: 18em; width: 75%">
      <h3 style="color: #002A68;">Editar El tipo de equipo ferroviario {{ tipo_equipo_ferroviario.tipo_equipo }}</h3>
      <form @submit.prevent="submitForm" class="form-grid">
        <!-- Campo Tipo de Equipo -->
        <div class="mb-3">
          <label for="tipo_equipo" class="form-label">Tipo de equipo:<span style="color: red;">*</span></label>
          <select class="form-control" id="tipo_equipo" v-model="tipo_equipo_ferroviario.tipo_equipo" required>
            <option v-for="equipo in t_equipo_options" :value="equipo.value" :key="equipo.value">
              {{ equipo.text }}
            </option>
          </select>
        </div>

        <!-- Campo Tipo de Carga -->
        <div class="mb-3">
          <label for="tipo_carga" class="form-label">Tipo de carga:<span style="color: red;">*</span></label>
          <select class="form-control" id="tipo_carga" v-model="tipo_equipo_ferroviario.tipo_carga" required>
            <option v-for="carga in t_carga_options" :value="carga.value" :key="carga.value">
              {{ carga.text }}
            </option>
          </select>
        </div>

        <!-- Campo Tipo de Combustible -->
        <div class="mb-3">
          <label for="tipo_combustible" class="form-label">Tipo de combustible:<span style="color: red;">*</span></label>
          <select class="form-control" id="tipo_combustible" v-model="tipo_equipo_ferroviario.tipo_combustible" required>
            <option v-for="combustible in t_combustible_options" :value="combustible.value" :key="combustible.value">
              {{ combustible.text }}
            </option>
          </select>
        </div>

        <!-- Campo Longitud -->
        <div class="mb-3">
          <label for="longitud" class="form-label">Longitud (ft):<span style="color: red;">*</span></label>
          <input type="number" class="form-control" id="longitud" v-model="tipo_equipo_ferroviario.longitud" step="0.01" required />
        </div>

        <!-- Campo Peso Neto sin Carga -->
        <div class="mb-3">
          <label for="peso_neto_sin_carga" class="form-label">Peso neto sin carga(t):<span style="color: red;">*</span></label>
          <input type="number" class="form-control" id="peso_neto_sin_carga" v-model="tipo_equipo_ferroviario.peso_neto_sin_carga" step="0.01" required />
        </div>

        <!-- Campo Peso Máximo con Carga -->
        <div class="mb-3">
          <label for="peso_maximo_con_carga" class="form-label">Peso máximo con carga(t):<span style="color: red;">*</span></label>
          <input type="number" class="form-control" id="peso_maximo_con_carga" v-model="tipo_equipo_ferroviario.peso_maximo_con_carga" step="0.01" required />
        </div>

        <!-- Campo Capacidad Cúbica Máxima -->
        <div class="mb-3">
          <label for="capacidad_cubica_maxima" class="form-label">Capacidad cúbica máxima(ft3):<span style="color: red;">*</span></label>
          <input type="number" class="form-control" id="capacidad_cubica_maxima" v-model="tipo_equipo_ferroviario.capacidad_cubica_maxima" step="0.01" required />
        </div>

        <!-- Campo Descripción -->
        <div class="mb-3">
          <label for="descripcion" class="form-label">Descripción:<span style="color: red;">*</span></label>
          <input type="text" class="form-control" id="descripcion" v-model="tipo_equipo_ferroviario.descripcion" required />
        </div>

        <!-- Botones -->
        <div class="form-buttons">
          <button type="button" @click="confirmCancel" style="color:white;text-decoration:none">Cancelar</button>
          <button type="submit">Aceptar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
body {
  background-color: #F2F2F2;
}

.form-container {
  max-width: 680px; /* Ancho reducido */
  margin: 20px; /* Centra el formulario */
  padding: 20px;
  margin-left: 220px;
  background-color: rgb(245, 245, 245);
  border-radius: 8px;
}

h3 {
  text-align: left;
  margin-bottom: 20px;
  font-size: 18px;
}

.form-label {
  font-size: 14px;
  text-align: left;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 3 columnas de igual tamaño */
  gap: 15px; /* Espacio entre los elementos */
}

.mb-3 {
  width: 200px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-control {
  padding: 1px 0px; /* Padding reducido */
  height: 25px; /* Altura reducida */
  font-size: 14px; /* Tamaño de fuente reducido */
  border: 1px solid #ccc;
  border-radius: 2px;
  color: #000; /* Asegura que el texto sea negro */
  background-color: #fff; /* Asegura que el fondo sea blanco */
}

select option {
  color: #000; /* Asegura que el texto de las opciones sea negro */
  background-color: #fff; /* Asegura que el fondo de las opciones sea blanco */
}

.form-buttons {
  grid-column: span 3; /* Los botones ocupan las 2 columnas */
  display: flex;
  justify-content: flex-end;
  font-size: 14px;
}

button {
  margin-left: 10px;
  padding: 6px 15px; /* Padding reducido */
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  font-size: 14px; /* Tamaño de fuente reducido */
}

button[type="button"] {
  background-color: gray;
  color: white;
}

button[type="submit"] {
  background-color: #007bff;
  color: white;
}
</style>
  <script>
  import axios from 'axios';
  import Swal from 'sweetalert2'
  import NavbarComponent from '@/components/NavbarComponent.vue';

  export default {
          name: 'EditarTipoEquipoFerroView',
          components: {
    NavbarComponent,
  },

          data(){
          return{
            tipo_equipo_ferroviario:{}, 

            t_equipo_options: [
              { value: 'casilla', text: 'Casilla' },
              { value: 'caj_gon', text: 'Cajones o Góndola' },
              { value: 'planc_plat', text: 'Plancha o Plataforma' },
              { value: 'Plan_porta_cont', text: 'Plancha porta contenedores' },
              { value: 'cist_liquidos', text: 'Cisterna para líquidos' },
              { value: 'cist_solidos', text: 'Cisterna para sólidos' },
              { value: 'tolva_g_mineral', text: 'Tolva granelera(mineral)' },
              { value: 'tolva_g_agric', text: 'Tolva granelera(agrícola)' },
              { value: 'tolva_g_cemento', text: 'Tolva para cemento' },
              { value: 'volqueta', text: 'Volqueta' },
              { value: 'Vagon_ref', text: 'Vagón refrigerado' },
              { value: 'jaula', text: 'Jaula' },
              { value: 'locomotora', text: 'Locomotora' },
              { value: 'tren', text: 'Tren' },
            ],
            t_carga_options: [
              { value: 'combustible', text: 'Combustible' },
              { value: 'aceite', text: 'Aceite' },
              { value: 'miel', text: 'Miel' },
              { value: 'alcohol', text: 'Alcohol' },
              { value: 'quimicos', text: 'Químicos' },
              { value: 'contenedores', text: 'Contenedores' },
              { value: 'otros', text: 'Otros' },
            ],
            t_combustible_options: [
              { value: '-', text: '-' },
              { value: 'combustible_blanco', text: 'Combustible blanco' },
              { value: 'combustible_negro', text: 'Combustible negro' },
              { value: 'combustible_turbo', text: 'Combustible turbo' },
            ], 
     
          }
          },
          mounted() {
          this.get_tipo_equipo_ferroviario()
          },
          methods:{
            confirmCancel() {
    Swal.fire({
    title: '¿Está seguro de que quiere cancelar la operación?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    cancelmButtonText: 'Cancelar',
    confirmButtonText: 'Aceptar'
  }).then((result) => {
    if (result.isConfirmed) {
      window.history.back();
    }
  });
},
                  validateForm() {                   
                         
                          let valid = true;
                          
                          return valid;
                  },
                  async get_tipo_equipo_ferroviario(){
                  this.$store.commit('setIsLoading', true)
                          /* creamos una const para guardar el id seleccionado */
                          const tipo_equipo_ferroviario_id = this.$route.params.id /*ese id es el que se declaro en el path para pais en la ruta /router/index.vue*/

                          /*ahora llamamos a axios */
                          axios
                          /*con la comilla invertida y el nombre de la variable entre llaves y el simbolo $ se conforma una cadena para formar el path
                          que da solucion a la seleccion del usuario*/
                              .get(`/api/tipos_equipos/${tipo_equipo_ferroviario_id}/`)                    
                              .then(response => {                                
                                  this.tipo_equipo_ferroviario = response.data                        
                              })

                              .catch(error =>{
                                  console.log(error)
                              })
                          this.$store.commit('setIsLoading', false)
                          
                  },

                  /*funcion para enviar los datos al servidor */
                  async submitForm(){
                      if (!this.validateForm()) {
                                return;
                              }
                      this.$store.commit('setIsLoading', true) 
                      const tipo_equipo_ferroviario_id = this.$route.params.id
                      try {
                            await axios.patch(`/api/tipos_equipos/${tipo_equipo_ferroviario_id}/`, this.tipo_equipo_ferroviario);
                            this.$router.push('/TipoEquipoFerro');
                            Swal.fire('Actualizado!', 'El tipo de equipo ferroviario ha sido modificado exitosamente.', 'success');
                          } catch (error) {
                            console.log(error);
                            Swal.fire('Error', 'Hubo un error al actualizar el tipo de equipo ferroviario.', 'error');
                          } finally {
                            this.$store.commit('setIsLoading', false);
                          }
                      }         
                      
                         
            }    
  }
  </script>
