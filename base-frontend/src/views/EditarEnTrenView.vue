<template>
  <div style="background-color: #002a68; color: white; text-align: right">
    <h6>Bienvenido:</h6>
  </div>
  <Navbar-Component />
  <Producto-Vagones />
  <div class="container mt-1" style="padding-left: 10%">
    <div class="row mb-4">
      <h2 class="mb-4">Editar vagón</h2>
      <form @submit.prevent="submitForm">
        <div class="row">
          <!-- Columna 1 -->
          <div class="col-md-6">
            <!-- Campo: locomotora -->
            <div class="mb-3">
              <label for="locomotora" class="form-label"
                >Locomotora<span style="color: red">*</span></label
              >
              <select
                class="form-select"
                v-model="formData.locomotora"
                id="locomotora"
                name="Locomotora"
                required
              >
                <option
                  v-for="locomotora in locomotoras"
                  :key="locomotora.id"
                  :value="locomotora.id"
                >
                  {{ locomotora.id }}-{{ locomotora.numero_identificacion }} -
                  {{ locomotora.tipo_equipo_name }}
                </option>
              </select>
            </div>

            <!-- Campo: tipo_origen -->
            <div class="mb-3">
              <label for="tipo_origen" class="form-label">Tipo de Origen</label>
              <select
                class="form-select"
                v-model="formData.tipo_origen"
                id="tipo_origen"
                name="tipo_origen"
              >
                <option value="ac_ccd">Acceso Comercial</option>
                <option value="puerto">Puerto</option>
              </select>
            </div>

            <!-- Campo: origen -->
            <div class="mb-3">
              <label for="origen" class="form-label">Origen</label>
              <select
                v-if="formData.tipo_origen !== 'puerto'"
                class="form-select"
                v-model="formData.origen"
                id="origen"
                name="origen"
              >
                <option
                  v-for="entidad in entidades"
                  :key="entidad.id"
                  :value="entidad.nombre"
                >
                  {{ entidad.id }}-{{ entidad.nombre }}
                </option>
              </select>

              <select
                v-else
                class="form-select"
                v-model="formData.origen"
                id="origen"
                name="origen"
              >
                <option
                  v-for="puerto in puertos"
                  :key="puerto.id"
                  :value="puerto.nombre_puerto"
                >
                  {{ puerto.id }}- {{ puerto.nombre_puerto }}
                </option>
              </select>
            </div>

            <!-- Campo: tipo_equipo -->
            <div class="mb-3">
              <label for="tipo_equipo" class="form-label"
                >Tipo de Equipo<span style="color: red">*</span></label
              >
              <select
                @click="buscarEquipos"
                class="form-select"
                v-model="formData.tipo_equipo"
                id="tipo_equipo"
                name="tipo_equipo"
                required
              >
                <option
                  v-for="equipo in equipos"
                  :key="equipo.id"
                  :value="equipo.id"
                >
                  {{ equipo.id }}-{{ equipo.tipo_equipo_name }}-
                  {{ equipo.tipo_carga_name }}
                </option>
              </select>
            </div>

            <!-- Campo: estado -->
            <div class="mb-3">
              <label for="estado" class="form-label"
                >Estado <span style="color: red">*</span></label
              >
              <select
                class="form-select"
                v-model="formData.estado"
                id="estado"
                name="estado"
                required
              >
                <option value="cargado">Cargado</option>
                <option value="vacio">Vacio</option>
              </select>
            </div>

            <!-- Campo: Vagon No ID -->
            <div class="mb-3">
              <label for="equipo_vagon" class="form-label"
                >Vagon No ID <span style="color: red">*</span></label
              >
              <select
                class="form-select"
                v-model="formData.equipo_vagon"
                id="equipo_vagon"
                name="equipo_vagon"
                required
              >
                <option v-for="item in equipos_vagones" :value="item.id">
                  {{ item.id }}-{{ item.numero_identificacion }}
                </option>
              </select>
            </div>
          </div>

          <!--   <div class="mb-3">
            <label for="equipo_id" class="form-label">Vagon No ID</label>
            <select
              @click="buscarEquipos"
              class="form-select"
              v-model="formData.equipo_vagon"
              id="equipo_vagon"
              name="equipo_vagon"
            >
              <option
                v-for="equipo_vagon in equipos_vagones"
                :value="equipo_vagon.id"
              >
                {{ equipo_vagon.id }}-{{ equipo_vagon.numero_identificacion }}
              </option>
            </select>
          </div> -->

          <!-- Columna 2 -->
          <div class="col-md-6">
            <!-- Campo: tipo_destino -->
            <div class="mb-3">
              <label for="tipo_destino" class="form-label"
                >Tipo de Destino <span style="color: red">*</span></label
              >
              <select
                class="form-select"
                v-model="formData.tipo_destino"
                id="tipo_destino"
                name="tipo_destino"
                required
              >
                <option value="ac_ccd">Acceso Comercial</option>
                <option value="puerto">Puerto</option>
              </select>
            </div>

            <!-- Campo: destino -->
            <div class="mb-3">
              <label for="destino" class="form-label">Destino</label>
              <select
                v-if="formData.tipo_destino !== 'puerto'"
                class="form-select"
                v-model="formData.destino"
                id="destino"
                name="destino"
              >
                <option
                  v-for="entidad in entidades"
                  :key="entidad.id"
                  :value="entidad.nombre"
                >
                  {{ entidad.id }}-{{ entidad.nombre }}
                </option>
              </select>

              <select
                v-else
                class="form-select"
                v-model="formData.destino"
                id="destino"
                name="destino"
              >
                <option
                  v-for="puerto in puertos"
                  :key="puerto.id"
                  :value="puerto.nombre_puerto"
                >
                  {{ puerto.id }}- {{ puerto.nombre_puerto }}
                </option>
              </select>
            </div>

            <!-- Campo: producto -->
            <div class="mb-3">
              <label for="producto" class="form-label"
                >Producto<button
                  class="create-button ms-2"
                  @click="abrirModalAgregarProducto"
                >
                  <i class="bi bi-plus-circle large-icon"></i></button
              ></label>
              <select
                v-if="formData.estado === 'cargado'"
                class="form-select"
                v-model="formData.producto"
                id="producto"
                name="producto"
              >
                <option v-for="producto in productos" :value="producto.id">
                  {{ producto.id }}-{{ producto.producto_name }} -{{
                    producto.producto_codigo
                  }}-{{ producto.tipo_embalaje_name }}
                </option>
              </select>
            </div>

            <!-- Campo: cantidad_vagones -->

            <!-- Campo: observaciones -->
            <div class="mb-3">
              <label for="observaciones" class="form-label"
                >Observaciones <span style="color: red">*</span></label
              >
              <textarea
                class="form-control"
                v-model="formData.observaciones"
                id="observaciones"
                name="observaciones"
                rows="3"
                required
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Botón de envío -->
      </form>
      <div class="text-center">
        <button @click="submitForm" class="btn btn-primary">Guardar</button>
        <button @click="volverEnTren" class="btn btn-secondary">Volver</button>
      </div>
    </div>

    <!-- Segunda fila: Lista de vagones -->
  </div>
</template>

<style scoped>
.create-button {
  text-decoration: none;
  color: green;
  margin-left: 940px;
}

.form-container {
  max-width: 300px;
  margin: 50px;
  padding: 20px;
  background-color: f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  font-family: "Franklin Gothic Medium", "Arial Narrow", Arial, sans-serif;
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
  text-align: left;
  display: flex;
  width: 260px;
  flex-direction: column;
  gap: 5px;
  font-size: 14px;
}

label {
  font-weight: bold;
}

input,
select {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.form-buttons {
  display: flex;
  justify-content: end;
  font-size: 15px;
}

button {
  margin-left: 10px;
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
import axios from "axios";
import Swal from "sweetalert2";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "AdicionarEnTren",
  components: {
    NavbarComponent,
  },
  data() {
    return {
      formData: {
        locomotora: "",
        tipo_origen: "acc_d",
        origen: "",
        tipo_equipo: "",
        estado: "cargado",
        tipo_destino: "ac_ccd",
        destino: "",
        producto: "",
        observaciones: "",
        equipo_vagon: "",
      },
      productos: [],
      equipos: [],
      equipos_vagones: [],
      locomotoras: [],
      puertos: [],
      entidades: [],
      vagon: [],
    };
  },

  mounted() {
    // Llama al método para obtener los puertos
    this.getProductos();
    this.getEquipos();
    this.getLocomotoras();
    this.getEntidades();
    this.getPuertos();
    this.getTren();
  },

  methods: {
    confirmCancel() {
      Swal.fire({
        title: "¿Está seguro de que quiere cancelar la operación?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        cancelmButtonText: "Cancelar",
        confirmButtonText: "Aceptar",
      }).then((result) => {
        if (result.isConfirmed) {
          window.history.back();
        }
      });
    },

    resetForm() {
      // Restablece los valores del formulario
      this.formData = {
        locomotora: "puerto",
        tipo_origen: "acc_d",
        origen: "",
        tipo_equipo: "",
        estado: "cargado",
        tipo_destino: "ac_ccd",
        destino: "",
        producto: "",
        observaciones: "",
        equipo_vagon: "",
      };

      // Restablecer el número de identificación seleccionado

      // Opcional: Limpiar el localStorage si es necesario
    },
    async getTren() {
      this.$store.commit("setIsLoading", true);
      const vagon_id = this.$route.params.id;
      try {
        const response = await axios.get(`/ufc/en-trenes/${vagon_id}/`);
        this.vagon = response.data;
        this.formData = {
          locomotora: this.vagon["locomotora"],
          tipo_origen: this.vagon["tipo_origen"],
          origen: this.vagon["origen"],
          tipo_equipo: this.vagon["tipo_equipo"],
          estado: this.vagon["estado"],
          tipo_destino: this.vagon["tipo_destino"],
          destino: this.vagon["destino"],
          producto: this.vagon["producto"],
          observaciones: this.vagon["observaciones"],
          equipo_vagon: this.vagon["equipo_vagon"],
        };
        console.log(formData);
      } catch (error) {
        console.error("Error al obtener el vagon:", error);
      }
      this.$store.commit("setIsLoading", false);
    },

    async submitForm() {
      try {
        // Acceder a los datos del vagón
        const vagon_id = this.$route.params.id;
        await axios.patch(`/ufc/en-trenes/${vagon_id}/`, this.formData); // Enviar los datos al servidor

        Swal.fire(
          "Agregado!",
          "El formulario sido añadido exitosamente.",
          "success"
        );
      } catch (error) {
        console.error("Error al agregar el formulario:", error);
        Swal.fire(
          "Error",
          `${error["response"]["data"]["non_field_errors"][0]}`,
          "error"
        );
      }
    },

    onVagonChange(event) {
      // Obtener el ID seleccionado
      const selectedId = this.formData.equipo_vagon;

      // Buscar el objeto correspondiente en equipos_vagones
      const selectedVagon = this.equipos_vagones.find(
        (vagon) => vagon.id === selectedId
      );

      // Guardar el número de identificación en una variable
      if (selectedVagon) {
        this.numeroIdentificacionSeleccionado =
          selectedVagon.numero_identificacion;
        console.log(
          "Número de identificación seleccionado:",
          this.numeroIdentificacionSeleccionado
        );
      } else {
        this.numeroIdentificacionSeleccionado = null;
      }
    },

    async getLocomotoras() {
      try {
        const response = await axios.get(
          "/api/equipos_ferroviarios/?id_tipo_equipo_territorio=locomo"
        );
        this.locomotoras = response.data;
      } catch (error) {
        console.error("Error al obtener las Locomotoras:", error);
        Swal.fire(
          "Error",
          "Hubo un error al obtener las Locomotoras.",
          "error"
        );
      }
    },

    async buscarEquipos() {
      try {
        const peticion =
          "/api/equipos_ferroviarios/?id_tipo_equipo_territorio=" +
          this.formData.tipo_equipo;
        const response = await axios.get(peticion);
        this.equipos_vagones = response.data;
      } catch (error) {
        console.error("Error al obtener los equipos:", error);
        Swal.fire("Error", "Hubo un error al obtener los equipos.", "error");
      }
    },

    async getEntidades() {
      try {
        const response = await axios.get("/api/entidades/");
        this.entidades = response.data;
      } catch (error) {
        console.error("Error al obtener las entidades:", error);
        Swal.fire("Error", "Hubo un error al obtener las entidades.", "error");
      }
    },
    volverEnTren() {
      // Redirige a la vista "AdicionarProductoVagon"
      this.$router.go(-1);
    },

    async getPuertos() {
      try {
        const response = await axios.get("/api/puertos/");
        this.puertos = response.data;
      } catch (error) {
        console.error("Error al obtener los puertos:", error);
        Swal.fire("Error", "Hubo un error al obtener los puertos.", "error");
      }
    },

    async getEquipos() {
      try {
        const response = await axios.get("/api/tipo-e-f-no-locomotora/");
        this.equipos = response.data;
      } catch (error) {
        console.error("Error al obtener los equipos:", error);
        Swal.fire("Error", "Hubo un error al obtener los equipos.", "error");
      }
    },

    async getProductos() {
      try {
        const response = await axios.get("/ufc/producto-vagon/");
        this.productos = response.data;
      } catch (error) {
        console.error("Error al obtener los productos:", error);
        Swal.fire("Error", "Hubo un error al obtener los productos.", "error");
      }
    },
    abrirModalAgregarProducto() {
      // Redirige a la vista "AdicionarProductoVagon"
      localStorage.setItem("formData", JSON.stringify(this.formData));
      this.$router.push({ name: "AdicionarProductoVagon" });
    },

    eliminarVagon(index) {
      // Eliminar un vagón de la lista
      this.vagonesAgregados.splice(index, 1);
      localStorage.setItem(
        "vagonesAgregados",
        JSON.stringify(this.vagonesAgregados)
      );
      Swal.fire("Éxito", "Vagón eliminado correctamente.", "success");
    },

    validateForm() {
      const nombre_atraque_regex = /^[A-Z][A-Za-z ]{2,99}$/;
      let errorMessage = "";

      if (!nombre_atraque_regex.test(this.nombre_atraque)) {
        errorMessage +=
          'El campo "Nombre" debe comenzar con mayúscula, seguir con letras y espacios, y tener entre 3 y 100 caracteres.\n';
      }

      if (errorMessage) {
        Swal.fire({
          icon: "error",
          title: "Error de validación",
          text: errorMessage,
        });
        return false; // Detener el envío del formulario
      }

      return true; // El formulario es válido
    },
  },
};
</script>
