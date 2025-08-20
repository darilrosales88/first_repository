<template>
  <div class="container py-3">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Agregar Nuevo Tren</h2>
      <button @click="$router.go(-1)" class="btn btn-outline-secondary">
        <i class="bi bi-arrow-left"></i> Volver
      </button>
    </div>

    <div class="card">
      <div class="card-body">
        <form @submit.prevent="submitForm">
          <!-- Campo:Fecha de registro -->
          <div class="mb-3">
              <label for="fecha_registro" class="form-label">Fecha de registro</label>
              <input
                type="text"
                class="form-control"
                :value="formattedFechaRegistro"
                id="fecha_registro"
                name="fecha_registro"
                readonly
              />
            </div>
          <div class="mb-3">
            <label class="form-label">Origen</label>
            <input
              v-model="tren.origen"
              type="text"
              class="form-control"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Tipo de Origen</label>
            <select
              v-model="tren.tipo_origen"
              class="form-select"
              required
            >
              <option value="" disabled>Seleccione un tipo</option>
              <option
                v-for="option in tipo_origen_options"
                :value="option.id"
                :key="option.id"
              >
                {{ option.text }}
              </option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Tipo de Equipo</label>
            <select
              v-model="tren.tipo_equipo"
              class="form-select"
              required
            >
              <option value="" disabled>Seleccione un tipo</option>
              <option
                v-for="option in tipo_equipo_options"
                :value="option.id"
                :key="option.id"
              >
                {{ option.text }}
              </option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Estado</label>
            <select v-model="tren.estado" class="form-select" required>
              <option value="" disabled>Seleccione un estado</option>
              <option
                v-for="option in estado_options"
                :value="option.id"
                :key="option.id"
              >
                {{ option.text }}
              </option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Cantidad de Vagones</label>
            <input
              v-model="tren.cantidad_vagones"
              type="number"
              class="form-control"
              required
              min="0"
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Producto</label>
            <select
              v-model="tren.producto"
              class="form-select"
              required
            >
              <option value="" disabled>Seleccione un producto</option>
              <option
                v-for="option in producto_options"
                :value="option.id"
                :key="option.id"
              >
                {{ option.text }}
              </option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Destino</label>
            <input
              v-model="tren.destino"
              type="text"
              class="form-control"
              required
            />
          </div>

          <div class="d-flex justify-content-end mt-4">
            <button
              type="button"
              @click="$router.go(-1)"
              class="btn btn-outline-secondary me-2"
            >
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <span
                v-if="loading"
                class="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
              ></span>
              {{ loading ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Swal from 'sweetalert2'

export default {
  name: 'AgregarArrastre',
  data() {
    return {
      informeOperativoId: null,
      loading: false,
      tren: {
        origen: "",
        tipo_origen: "",
        tipo_equipo: "",
        estado: "",
        cantidad_vagones: "",
        producto: "",
        destino: "",
      },
      tipo_origen_options: [
        { id: "puerto", text: "Puerto" },
        { id: "acceso_comercial", text: "Acceso Comercial" },
      ],
      tipo_equipo_options: [
        { id: "casilla", text: "Casilla" },
        { id: "cajon_gondola", text: "Cajón o Góndola" },
      ],
      estado_options: [
        { id: "vacio", text: "Vacío" },
        { id: "cargado", text: "Cargado" },
      ],
      producto_options: [
        { id: "granos", text: "Granos" },
        { id: "minerales", text: "Minerales" },
        { id: "combustible", text: "Combustible" },
      ],
    }
  },
  computed:{
    formattedFechaRegistro() {
      if (this.formData.fecha) {
        return new Date(this.formData.fecha).toLocaleString();
      }
      return new Date().toLocaleString();
    }
  },
  methods: {
    async verificarInformeOperativo() {
      try {
        this.formData.fecha = new Date().toISOString();
        const today = new Date();
        const fechaFormateada = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;

        const response = await axios.get('/ufc/verificar-informe-existente/', {
          params: { fecha_operacion: fechaFormateada }
        });

        if (response.data.existe) {
          this.informeOperativoId = response.data.id;
          return true;
        }
        return false;
      } catch (error) {
        console.error("Error al verificar informe:", error);
        return false;
      }
    },
    async submitForm() {
      // 1. Verifificar que el informe operativo existe ya para la fecha creada
        const existeInforme = await this.verificarInformeOperativo();
        if (!existeInforme) {
          Swal.fire(
            "Error",
            "No existe un informe operativo creado para la fecha actual. Debe crear uno primero.",
            "error"
          );
          this.$router.push({ name: "InfoOperativo" });
          return;
          
        }
        // 2. Verificar que el informe no esté en estado "Aprobado"
        const informeResponse = await axios.get(`/ufc/informe-operativo/${this.informeOperativoId}/`);
        console.log("anijijijijiji",informeResponse.data.estado_parte);
        if (informeResponse.data.estado_parte === "Aprobado") {
          Swal.fire(
            "Error",
            "No se puede agregar registros a un informe operativo que ya ha sido aprobado.",
            "error"
          );
          return;
        }

      this.loading = true
      try {
        const response = await axios.post('/ufc/pendiente-arrastre/', this.tren)
        Swal.fire({
          title: 'Éxito',
          text: 'Tren creado correctamente',
          icon: 'success',
          confirmButtonText: 'Aceptar'
        }).then(() => {
          this.$router.push({ name: 'GestionTrenes' })
        })
      } catch (error) {
        console.error('Error al crear el tren:', error)
        Swal.fire({
          title: 'Error',
          text: 'No se pudo crear el tren',
          icon: 'error',
          confirmButtonText: 'Aceptar'
        })
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.card {
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: 2rem;
}

.form-label {
  font-weight: 500;
}
</style>