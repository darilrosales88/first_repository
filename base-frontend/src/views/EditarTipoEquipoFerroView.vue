<template>
  <div class="form-container">
  <h2>Editar El tipo de equipo ferroviario {{ tipo_equipo_ferroviario.tipo_equipo }}</h2>
 
  <form @submit.prevent="submitForm">
    <div class="form-group">
        <label for="tipo_equipo">Tipo de equipo:</label>
        <select v-model="tipo_equipo_ferroviario.tipo_equipo" required>
          <option v-for="equipo in t_equipo_options" :value="equipo.value" :key="equipo.value">
            {{ equipo.text }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="tipo_carga">Tipo de carga:</label>
        <select v-model="tipo_equipo_ferroviario.tipo_carga" required>
          <option v-for="carga in t_carga_options" :value="carga.value" :key="carga.value">
            {{ carga.text }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="tipo_combustible">Tipo de combustible:</label>
        <select v-model="tipo_equipo_ferroviario.tipo_combustible" required>
          <option v-for="combustible in t_combustible_options" :value="combustible.value" :key="combustible.value">
            {{ combustible.text }}
          </option>
        </select>
      </div>
  <div class="form-group">
    <label for="longitud">Longitud (ft):</label>
    <input type="number" v-model="tipo_equipo_ferroviario.longitud" step="0.01" required />
  </div>
  <div class="form-group">
    <label for="peso_neto_sin_carga">Peso neto sin carga (t):</label>
    <input type="number" v-model="tipo_equipo_ferroviario.peso_neto_sin_carga" step="0.01" required />
  </div>
  <div class="form-group">
    <label for="peso_maximo_con_carga">Peso máximo con carga (t):</label>
    <input type="number" v-model="tipo_equipo_ferroviario.peso_maximo_con_carga" step="0.01" required />
  </div>
  <div class="form-group">
    <label for="capacidad_cubica_maxima">Capacidad cúbica máxima (ft3):</label>
    <input type="number" v-model="tipo_equipo_ferroviario.capacidad_cubica_maxima" step="0.01" required />
  </div>
  <div class="form-group">
    <label for="descripcion">Descripción:</label>
    <input type="text" v-model="tipo_equipo_ferroviario.descripcion" required />
  </div>
 

  <div class="form-buttons">
  <button type="button"><router-link style="color:white;text-decoration:none" to="/TipoEquipoFerro">Cancelar</router-link> </button>
  <button>Aceptar</button>
  </div>
  </form>
  </div>
  </template>
  <style scoped>
  .form-container {
  max-width: 450px;
  margin: 50px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  h2 {
  font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  text-align: left;
  margin-bottom: 20px;
  font-size: 20px;
  }

  form {
  display: flex;
  flex-direction: column;
  gap: 15px;

  }

  .form-group {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  font-size: 13px;
  }

  label {
  flex: 1;
  text-align: right;
  font-weight: bold;
  }

  input,select {
  flex: 2;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  }

  .form-buttons {
  display: flex;
  justify-content: end;
  font-size: 15px;
  }

  button {
  padding: 5px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  }

  button[type="button"] {
  background-color: #007bff;
  color: white;
  }

  button[type="submit"] {
  margin-left: 15px;
  background-color: #007bff;
  color: white;
  }
  </style>

  <script>
  import axios from 'axios';
  import Swal from 'sweetalert2'
  export default {
          name: 'EditarTipoEquipoFerroView',

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
              { value: 'combust_blanco', text: 'Combustible blanco' },
              { value: 'combustible_negro', text: 'Combustible negro' },
              { value: 'combustible_turbo', text: 'Combustible turbo' },
            ],   

          }
          },
          mounted() {
          this.get_tipo_equipo_ferroviario()
          },
          methods:{
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
