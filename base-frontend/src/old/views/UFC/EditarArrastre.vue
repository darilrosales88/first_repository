<template>
    <div v-if="show" class="modal-backdrop">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Editar Tren</h5>
          <button @click="$emit('close')" class="btn-close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="$emit('save', tren)">
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
              />
            </div>
  
            <div class="mb-3">
              <label class="form-label">Producto</label>
              <select
                v-model="tren.producto"
                class="form-select"
                required
              >
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
  
            <div class="d-flex justify-content-end">
              <button
                type="button"
                @click="$emit('close')"
                class="btn btn-outline-secondary me-2"
              >
                Cancelar
              </button>
              <button type="submit" class="btn btn-primary">
                Actualizar
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "EditarArrastre",
    props: {
      show: Boolean,
      tren: Object,
      tipo_origen_options: Array,
      tipo_equipo_options: Array,
      estado_options: Array,
      producto_options: Array,
    },
  };
  </script>
  
  <style scoped>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1050;
  }
  
  .modal-content {
    background-color: #fff;
    border-radius: 8px;
    width: 90%;
    max-width: 600px;
    padding: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  }
  
  .modal-header {
    border-bottom: 1px solid #dee2e6;
    padding-bottom: 15px;
    margin-bottom: 20px;
  }
  
  .modal-title {
    font-size: 1.25rem;
    font-weight: 600;
  }
  
  .btn-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    opacity: 0.7;
  }
  </style>