<template>
    <div class="ufc-header">
      <h6>Partes UFC</h6>
    </div>
    <Navbar-Component />
    <Producto-Vagones />
    <div class="container py-3" style="margin-left: 20em; width: 70%">
      <div class="card border">
        <div class="card-header bg-light border-bottom">
          <h5 class="mb-0 text-dark fw-semibold">
            <i class="bi bi-file-earmark-plus"></i> Nuevo registro pendiente a arrastre</h5>
        </div>
          <div class="card-body p-3">
            <form @submit.prevent="submitForm" class="ufc-form">
              <!-- Primera fila - Origen y Destino -->
              <div class="ufc-form-grid">
                <!-- Campo:Fecha de registro -->
              <div class="mb-3">
                <label for="fecha_registro" class="form-label small fw-semibold text-secondary">Fecha de registro</label>
                <input
                  type="text"
                  class="form-control form-control-sm border-secondary"
                  :value="formattedFechaRegistro"
                  id="fecha_registro"
                  name="fecha_registro"
                  readonly
                />
              </div>
                <!-- Grupo Origen -->
                <div class="ufc-form-group">
                  <div class="ufc-form-row">
                    <!-- Campo: tipo_origen -->
                    <div class="ufc-input-group paired">
                      <label for="tipo_origen" class="form-label small fw-semibold text-secondary">Tipo de Origen</label>
                      <select
                        class="form-select form-select-sm border-secondary"
                        v-model="formData.tipo_origen"
                        required>
                        <option value="" disabled>Seleccione un tipo</option>
                        <option v-for="item in tipo_origen_options" 
                                :key="item.id" 
                                :value="item.id">
                          {{ item.text }}
                        </option>
                      </select>
                    </div>
    
                    <!-- Campo: origen -->
                    <div class="ufc-input-group paired">
                      <label for="origen" class="form-label small fw-semibold text-secondary">Origen </label>
                      <select
                        v-if="formData.tipo_origen && formData.tipo_origen !== 'puerto'"
                        class="form-select form-select-sm border-secondary"
                        v-model="formData.origen"
                        required>
                        <option value="" disabled>Seleccione un origen</option>
                        <option
                          v-for="entidad in entidades"
                          :key="entidad.id"
                          :value="entidad.nombre">
                          {{ entidad.id }}-{{ entidad.nombre }}
                        </option>
                      </select>
    
                      <select
                        v-else-if="formData.tipo_origen === 'puerto'"
                        class="form-select form-select-sm border-secondary"
                        v-model="formData.origen"
                        required>
                        <option value="" disabled>Seleccione un puerto</option>
                        <option
                          v-for="puerto in puertos"
                          :key="puerto.id"
                          :value="puerto.nombre_puerto">
                          {{ puerto.id }}- {{ puerto.nombre_puerto }}
                        </option>
                      </select>
                      
                      <select
                        v-else
                        class="form-select form-select-sm border-secondary"
                        disabled>
                        <option value="">Seleccione primero el tipo de origen</option>
                      </select>
                    </div>
                  </div>
                </div>
    
                <!-- Grupo Destino -->
                <div class="ufc-form-group">
                  <div class="ufc-form-row">
                    <!-- Campo: tipo_destino -->
                    <div class="ufc-input-group paired">
                      <label for="tipo_destino" class="form-label small fw-semibold text-secondary">Tipo de Destino</label>
                      <select
                        class="form-select form-select-sm border-secondary"
                        v-model="formData.tipo_destino"
                        required>
                        <option value="" disabled>Seleccione un tipo</option>
                        <option v-for="item in tipo_destino_options" 
                                :key="item.id" 
                                :value="item.id">
                          {{ item.text }}
                        </option>
                      </select>
                    </div>
    
                    <!-- Campo: destino -->
                    <div class="ufc-input-group paired">
                      <label for="destino" class="form-label small fw-semibold text-secondary">Destino</label>
                      <select
                        v-if="formData.tipo_destino && formData.tipo_destino !== 'puerto'"
                        class="form-select form-select-sm border-secondary"
                        v-model="formData.destino"
                        required>
                        <option value="" disabled>Seleccione un destino</option>
                        <option
                          v-for="entidad in entidades"
                          :key="entidad.id"
                          :value="entidad.nombre">
                          {{ entidad.id }}-{{ entidad.nombre }}
                        </option>
                      </select>
    
                      <select
                        v-else-if="formData.tipo_destino === 'puerto'"
                        class="form-select form-select-sm border-secondary"
                        v-model="formData.destino"
                        required>
                        <option value="" disabled>Seleccione un puerto</option>
                        <option
                          v-for="puerto in puertos"
                          :key="puerto.id"
                          :value="puerto.nombre_puerto">
                          {{ puerto.id }}- {{ puerto.nombre_puerto }}
                        </option>
                      </select>
                      
                      <select
                        v-else
                        class="form-select form-select-sm border-secondary"
                        disabled>
                        <option value="">Seleccione primero el tipo de destino</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
    
              <!-- Segunda fila - Otros campos -->
              <div class="ufc-form-grid">
                <!-- Columna Izquierda -->
                <div class="ufc-form-column">
                  <!-- Campo: tipo_equipo -->
                  <div class="ufc-input-group">
                    <label for="tipo_equipo" class="form-label small fw-semibold text-secondary">Tipo de Equipo</label>
                    <select
                      class="form-select form-select-sm border-secondary"
                      v-model="formData.tipo_equipo"
                      required>
                      <option value="" disabled>Seleccione un tipo</option>
                      <option
                        v-for="option in tipo_equipo_options"
                        :key="option.id"
                        :value="option.id">
                        {{ option.text }}
                      </option>
                    </select>
                  </div>
    
                  <!-- Campo: estado -->
                  <div class="ufc-input-group">
                    <label for="estado" class="form-label small fw-semibold text-secondary">Estado</label>
                    <select
                      class="form-select form-select-sm border-secondary"
                      v-model="formData.estado"
                      @change="handleEstadoChange"
                      required>
                      <option value="cargado">Cargado</option>
                      <option value="vacio">Vacío</option>
                    </select>
                  </div>
                </div>
    
                <!-- Columna Derecha -->
                <div class="ufc-form-column">
                  <!-- Campo: operacion -->
                  <div class="ufc-input-group">
                    <label for="operacion" class="form-label small fw-semibold text-secondary">Operación</label>
                    <select
                      class="form-select form-select-sm border-secondary"
                      v-model="formData.operacion"
                      required>
                      <option value="" disabled>Seleccione una operación</option>
                      <option
                        v-for="option in t_operacion_options"
                        :key="option.id"
                        :value="option.id">
                        {{ option.text }}
                      </option>
                    </select>
                  </div>
    
                  <!-- Campo: cantidad_vagones -->
                  <div class="ufc-input-group">
                    <label for="cantidad_vagones" class="form-label small fw-semibold text-secondary">Cantidad de Vagones</label>
                    <div class="ufc-por-situar-container">
                      <input
                        type="number"
                        class="ufc-por-situar-input"
                        v-model.number="formData.cantidad_vagones"
                        min="1"
                        required>
                      <span class="ufc-por-situar-suffix">unidades</span>
                    </div>
                  </div>
                </div>
              </div>
    
              <!-- Tercera fila - Productos -->
              <div class="ufc-input-group full-width">
                <label for="producto" class="form-label small fw-semibold text-secondary">Productos <span v-if="formData.estado === 'cargado'" class="required"></span></label>
                <div class="ufc-input-with-action">
                  <div class="ufc-custom-select" @click="toggleProductosDropdown">
                    <div class="ufc-select-display">
                      {{ getSelectedProductosText() || 'Seleccione productos...' }}
                    </div>
                    <i class="bi bi-chevron-down ufc-select-arrow"></i>
                    
                    <div class="ufc-productos-dropdown" v-if="showProductosDropdown">
                      <div class="ufc-productos-search-container">
                        <input
                          type="text"
                          class="ufc-productos-search"
                          placeholder="Buscar productos..."
                          v-model="productoSearch"
                          @input="filterProductos"
                          @click.stop>
                      </div>
                      <div class="ufc-productos-options">
                        <div
                          v-for="producto in filteredProductos"
                          :key="producto.id"
                          class="ufc-producto-option"
                          :class="{ 'selected': formData.productos.includes(producto.id) }"
                          @click.stop="toggleProductoSelection(producto.id)">
                          {{ producto.id }}-{{ producto.producto_name }} - {{ producto.producto_codigo }}
                          <template v-if="producto.tipo_embalaje">
                            (Embalaje: {{ producto.tipo_embalaje.nombre || producto.tipo_embalaje.nombre_embalaje || 'N/A' }})
                          </template>
                        </div>
                      </div>
                    </div>
                  </div>
                  <button class="create-button ms-2" @click.stop.prevent="abrirModalAgregarProducto">
                    <i class="bi bi-plus-circle large-icon"></i>
                  </button>
                </div>
              </div>
    
              <!-- Observaciones (full width) -->
              <div class="ufc-input-group full-width">
                <label for="observaciones" class="form-label small fw-semibold text-secondary">Observaciones</label>
                <textarea
                  class="form-control form-control-sm border-secondary"
                  v-model="formData.observaciones"
                  rows="2"></textarea>
              </div>
    
              <!-- Botones de acción -->
              <div class="modal-footer">
                <div class=" d-flex justify-content-between align-items-center mb-4">
                  <button class="ufc-button secondary" @click="volver_principal">
                    <i class="bi bi-x-circle" me-1></i>Cancelar
                  </button>
                  <button type="submit" class=" ufc-button primary" >
                    <i class="bi bi-check-circle" me-1></i>Agregar
                  </button>
                </div>
              </div>
            </form>          
          </div>
        </div>
      </div>
      
      <ModalAgregarProducto v-if="mostrarModal" :visible="mostrarModal" @cerrar-modal="cerrarModal"/>

  </template>

  <script>
  import axios from "axios";
  import Swal from "sweetalert2";
  import NavbarComponent from "@/components/NavbarComponent.vue";
  import ModalAgregarProducto from "@/components/ModalAgregarProducto.vue";
  
  export default {
    name: "AdicionarPendienteArrastre",
    components: {
      NavbarComponent,
      ModalAgregarProducto,
    },
    data() {
      return {
        informeOperativoId: null,
        formData: {
          tipo_origen: "",
          origen: "",
          tipo_destino: "",
          destino: "",
          tipo_equipo: "",
          operacion: "",
          estado: "cargado",
          productos: [], 
          cantidad_vagones: 1,
          observaciones: "",
        },
        productoSearch: '',
        filteredProductos: [],
        showProductosDropdown: false,
        entidades: [],
        puertos: [],
        productos: [],
        loading: false,
        mostrarModal: false,
        tipo_origen_options: [
          { id: "ac_ccd", text: "comercial/AccesoCCD" },
          { id: "puerto", text: "Puerto" },
        ],
        tipo_destino_options: [
          { id: "ac_ccd", text: "comercial/AccesoCCD" },
          { id: "puerto", text: "Puerto" },
        ],
        tipo_equipo_options: [
          { id: "casilla", text: "Casilla" },
          { id: "caj_gon", text: "Cajon o Gondola" },
        ],
        t_operacion_options: [
          { id: "carga", text: "Carga" },
          { id: "descarga", text: "Descarga" },
        ],
      };
    },
    mounted() {
      this.getProductos();
      this.getEntidades();
      this.getPuertos();
      this.closeDropdownsOnClickOutside();
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
      async getEntidades() {
        try {
          const response = await axios.get("/api/entidades/");
          this.entidades = response.data.results;
        } catch (error) {
          console.error("Error al obtener entidades:", error);
          Swal.fire("Error", "No se pudieron obtener las entidades", "error");
        }
      },
  
      async getProductos() {
        this.loading = true;
        try {
          const response = await axios.get("/ufc/producto-vagon/", {
            params: {
              include_details: true
            }
          });
          
          this.productos = response.data.results.map(p => {
            const tipoEmbalaje = p.tipo_embalaje || {};
            return {
              ...p,
              tipo_embalaje: {
                nombre: tipoEmbalaje.nombre || tipoEmbalaje.nombre_embalaje || 'Sin embalaje'
              }
            };
          });
          this.filteredProductos = this.productos;
        } catch (error) {
          console.error("Error al obtener productos:", error);
          Swal.fire("Error", "No se pudieron cargar los productos", "error");
        } finally {
          this.loading = false;
        }
      },
  
      async getPuertos() {
        try {
          let allPuertos = [];
          let nextPage = "/api/puertos/";
  
          while (nextPage) {
            const response = await axios.get(nextPage);
            allPuertos = [...allPuertos, ...response.data.results];
            nextPage = response.data.next;
          }
  
          this.puertos = allPuertos;
        } catch (error) {
          console.error("Error al obtener los puertos:", error);
          Swal.fire("Error", "Hubo un error al obtener los puertos.", "error");
        }
      },
  
      abrirModalAgregarProducto() {
        this.showProductosDropdown = false;
        this.mostrarModal = true;
      },
  
      cerrarModal() {
        this.mostrarModal = false;
      },
  
      handleNuevoProducto(nuevoProducto) {
        this.getProductos();
        this.formData.productos.push(nuevoProducto.id);
        this.cerrarModal();
      },
  
      handleEstadoChange() {
        if (this.formData.estado === 'vacio') {
          this.formData.productos = [];
        }
      },
      volver_principal() {
        event.preventDefault();
        event.stopPropagation();
        Swal.fire({
          title: "¿Cancelar operación?",
          text: "Los datos no guardados se perderán",
          icon: "warning",
          showCancelButton: true,
          confirmButtonText: "Sí, cancelar",
          cancelButtonText: "No, continuar",
        }).then((result) => {
          if (result.isConfirmed) {
            this.resetForm();
            this.$router.push({ name: "InfoOperativo" });
          }
        });
      },
      async submitForm() {
        try {
          // 1. Verificar si existe un informe operativo para la fecha actual
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
          const informeDetalleResponse = await axios.get(`/ufc/informe-operativo/${this.informeOperativoId}/`);
          if (informeDetalleResponse.data.estado_parte === "Aprobado") {
            Swal.fire(
              "Error",
              "No se puede agregar registros a un informe operativo que ya ha sido aprobado.",
              "error"
            );
            return;
          }

          // 3. Validación de campos requeridos
          if (!this.formData.tipo_origen) {
            throw new Error("El campo Tipo de Origen es requerido");
          }
          
          if (!this.formData.origen) {
            throw new Error("El campo Origen es requerido");
          }
          
          if (!this.formData.tipo_destino) {
            throw new Error("El campo Tipo de Destino es requerido");
          }
          
          if (!this.formData.destino) {
            throw new Error("El campo Destino es requerido");
          }
          
          if (!this.formData.tipo_equipo) {
            throw new Error("El campo Tipo de Equipo es requerido");
          }
          
          if (!this.formData.operacion) {
            throw new Error("El campo Operación es requerido");
          }
          
          if (this.formData.estado === 'cargado' && this.formData.productos.length === 0) {
            throw new Error("Debe seleccionar al menos un producto cuando el estado es Cargado");
          }
          
          if (!this.formData.cantidad_vagones || this.formData.cantidad_vagones < 1) {
            throw new Error("La cantidad de vagones debe ser al menos 1");
          }

          // 4. Preparar los datos para enviar
          const payload = {
            tipo_origen: this.formData.tipo_origen,
            origen: this.formData.origen,
            tipo_destino: this.formData.tipo_destino,
            destino: this.formData.destino,
            tipo_equipo: this.formData.tipo_equipo,
            operacion: this.formData.operacion,
            estado: this.formData.estado,
            producto: this.formData.productos,
            cantidad_vagones: this.formData.cantidad_vagones,
            observaciones: this.formData.observaciones,
            informe_operativo: this.informeOperativoId // Añadir el ID del informe operativo
          };

          // 5. Enviar los datos al backend
          const response = await axios.post("/ufc/pendiente-arrastre/", payload);
          
          // 6. Mostrar mensaje de éxito
          Swal.fire({
            title: "¡Éxito!",
            text: "El registro ha sido creado correctamente",
            icon: "success",
            confirmButtonText: "Aceptar"
          }).then(() => {
            this.resetForm();
          });

        } catch (error) {
          console.error("Error al enviar el formulario:", error);
          
          let errorMessage = "Hubo un error al enviar el formulario";
          if (error.response) {
            if (error.response.data) {
              errorMessage = Object.values(error.response.data).join('\n');
            }
          } else if (error.message) {
            errorMessage = error.message;
          }
          
          Swal.fire({
            title: "Error",
            text: errorMessage,
            icon: "error",
            confirmButtonText: "Entendido"
          });
        }
      },
  
      resetForm() {
        this.formData = {
          tipo_origen: "",
          origen: "",
          tipo_destino: "",
          destino: "",
          tipo_equipo: "",
          operacion: "",
          estado: "cargado",
          productos: [],
          cantidad_vagones: 1,
          observaciones: "",
        };
      },
  
      confirmCancel() {
        Swal.fire({
          title: "¿Cancelar operación?",
          text: "Los datos no guardados se perderán",
          icon: "warning",
          showCancelButton: true,
          confirmButtonText: "Sí, cancelar",
          cancelButtonText: "No, continuar",
        }).then((result) => {
          if (result.isConfirmed) {
            this.resetForm();
            this.$router.push({ name: "InfoOperativo" });
          }
        });
      },
  
      toggleProductosDropdown() {
        if (this.mostrarModal) return;
        this.showProductosDropdown = !this.showProductosDropdown;
        if (this.showProductosDropdown) {
          this.productoSearch = '';
          this.filterProductos();
        }
      },
      
      filterProductos() {
        if (!this.productoSearch) {
          this.filteredProductos = this.productos;
          return;
        }
        const searchTerm = this.productoSearch.toLowerCase();
        this.filteredProductos = this.productos.filter(producto => 
          producto.producto_name.toLowerCase().includes(searchTerm) ||
          producto.producto_codigo.toLowerCase().includes(searchTerm) ||
          producto.id.toString().includes(searchTerm)
        );
      },
      
      toggleProductoSelection(productoId) {
        const index = this.formData.productos.indexOf(productoId);
        if (index === -1) {
          this.formData.productos.push(productoId);
        } else {
          this.formData.productos.splice(index, 1);
        }
      },
      
      getSelectedProductosText() {
        if (this.formData.productos.length === 0) return '';
        if (this.formData.productos.length === 1) {
          const producto = this.productos.find(p => p.id === this.formData.productos[0]);
          return producto ? `${producto.id}-${producto.producto_name}` : '1 producto seleccionado';
        }
        return `${this.formData.productos.length} productos seleccionados`;
      },
      
      closeDropdownsOnClickOutside() {
        document.addEventListener('click', (e) => {
          if (!e.target.closest('.ufc-custom-select')) {
            this.showProductosDropdown = false;
          }
          if (!e.target.closest('.ufc-modal-container') && !e.target.matches('.ufc-add-button')) {
            this.mostrarModal = false;
          }
        });
      }
    },
  };
  </script>

<style scoped>
/* Nuevos estilos para los campos apareados */
.ufc-form-row {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}

.ufc-input-group.paired {
  flex: 1;
  min-width: 0; /* Evita problemas de desbordamiento */
}

/* Ajustes para el grid principal */
.ufc-form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 15px;
}

@media (max-width: 768px) {
  .ufc-form-row {
    flex-direction: column;
    gap: 10px;
  }
  
  .ufc-form-grid {
    grid-template-columns: 1fr;
  }
}

/* Estilos para el select con búsqueda */
.ufc-custom-select {
  position: relative;
  width: 100%;
  cursor: pointer;
}

.ufc-select-display {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.85rem;
  background-color: white;
  min-height: 36px;
  display: flex;
  align-items: center;
  border-color: rgba(var(--bs-secondary-rgb),var(--bs-border-opacity)) !important;
}

.ufc-select-arrow {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  transition: transform 0.2s;
}

.ufc-custom-select.open .ufc-select-arrow {
  transform: translateY(-50%) rotate(180deg);
}

.ufc-productos-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  max-height: 300px;
  overflow-y: auto;
  background: white;
  border: 1px solid #ddd;
  border-radius: 0 0 6px 6px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 10;
  margin-top: 2px;
}

.ufc-productos-search-container {
  padding: 8px;
  border-bottom: 1px solid #eee;
  background: #f8f9fa;
}

.ufc-productos-search {
  width: 100%;
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.85rem;
}

.ufc-productos-search:focus {
  outline: none;
  border-color: #002a68;
}

.ufc-productos-options {
  max-height: 250px;
  overflow-y: auto;
}

.ufc-producto-option {
  padding: 8px 12px;
  font-size: 0.85rem;
  border-bottom: 1px solid #f0f0f0;
}

.ufc-producto-option:hover {
  background-color: #f5f5f5;
}

.ufc-producto-option.selected {
  background-color: #002a68;
  color: white;
}

/* Estilo para el botón de agregar */
.ufc-add-button {
  margin-left: 8px;
}

.ufc-form-container {
  font-family: 'Segoe UI', Roboto, -apple-system, sans-serif;
  color: #333;
  padding-bottom: 20px;
}

.ufc-header {
  background-color: #002a68;
  color: white;
  text-align: right;
  padding: 10px 15px;
  margin-bottom: 20px;
}

.ufc-header h6 {
  margin: 0;
  font-size: 1rem;
  font-weight: 500;
}

.ufc-form-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 15px;
}

.ufc-form-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.ufc-form-title {
  color: #002a68;
  font-size: 1.3rem;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}

.ufc-form-title i {
  font-size: 1.4rem;
}

.ufc-input-group {
  margin-bottom: 15px;
}

.ufc-input-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 0.85rem;
  font-weight: 500;
  color: #444;
}

.ufc-input-group .required {
  color: #e74c3c;
}

.ufc-select, .ufc-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.85rem;
  transition: all 0.2s;
  background-color: white;
}

.ufc-select:focus, .ufc-input:focus {
  border-color: #002a68;
  box-shadow: 0 0 0 3px rgba(0, 42, 104, 0.1);
  outline: none;
}

.ufc-textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  resize: vertical;
  min-height: 70px;
  font-family: inherit;
  font-size: 0.85rem;
}

.ufc-textarea:focus {
  border-color: #002a68;
  box-shadow: 0 0 0 3px rgba(0, 42, 104, 0.1);
  outline: none;
}

.ufc-input-with-action {
  display: flex;
  gap: 8px;
}

.ufc-add-button {
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 6px;
  width: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #002a68;
  transition: all 0.2s;
}

.ufc-add-button:hover {
  background: #e9ecef;
  color: #001a3d;
}

.ufc-add-button i {
  font-size: 1.1rem;
}

/* Estilo especial para el campo cantidad_vagones */
.ufc-por-situar-container {
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 6px;
  overflow: hidden;
  border-color: rgba(var(--bs-secondary-rgb),var(--bs-border-opacity)) !important;
}

.ufc-por-situar-input {
  flex: 1;
  border: none;
  padding: 8px 12px;
  font-size: 0.85rem;
  min-width: 0;
}

.ufc-por-situar-suffix {
  background: #f8f9fa;
  padding: 8px 12px;
  font-size: 0.8rem;
  color: #666;
  border-left: 1px solid #ddd;
}

/* Botones de acción */
.ufc-form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.ufc-button {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 1 rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  display: flex;
  align-items: center;
  gap: 6px;
}

.ufc-button.primary:hover {
  background: #003d8f;
}

.ufc-button.secondary {
    background:rgb(241, 81, 63);
    color: white;
}

.ufc-button.secondary:hover {
    background:rgb(228, 56, 37);
}

.create-button {
  text-decoration: none;
  color: green;
  margin-left: 940px;
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

/* Estilos para selects */
.ufc-select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 12px;
}

/* Estilos para el modal */
.ufc-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.ufc-modal-container {
  background: white;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow: auto;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
  animation: modalFadeIn 0.3s ease-out;
}

.ufc-modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #002a68;
  color: white;
  border-radius: 10px 10px 0 0;
}

.ufc-modal-header h3 {
  margin: 0;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.ufc-modal-close {
  background: transparent;
  border: none;
  color: white;
  font-size: 1.3rem;
  cursor: pointer;
  padding: 5px;
  transition: all 0.2s;
}

.ufc-modal-close:hover {
  color: #ccc;
}

.ufc-modal-body {
  padding: 20px;
}

.full-width {
  grid-column: 1 / -1;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>