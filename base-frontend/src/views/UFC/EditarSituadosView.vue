<template>
  <!-- Encabezado corporativo -->
  <div class="ufc-header">
    <h6>Partes UFC</h6>
  </div>
  <Navbar-Component />
  <Producto-Vagones />
  <div class="container py-3" style="margin-left: 20em; width: 70%">
    <div class="card border">
      <div class="card-header bg-light border-bottom">
        <h5 class="mb-0 text-dark fw-semibold">
          <i class="bi bi-file-earmark-plus me-2"></i>Editar registro de situados</h5>
      </div>
        <div class="card-body p-3">
          <form @submit.prevent="submitForm">
            <div class="ufc-form-grid">
              <!-- Columna 1 -->
              <div>
                <!-- Campo: tipo_origen -->
                <div class="ufc-input-group">
                  <label for="tipo_origen" class="form-label small fw-semibold text-secondary">
                    Tipo de Origen 
                  </label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    v-model="formData.tipo_origen"
                    id="tipo_origen"
                    name="tipo_origen"
                    required
                    :disabled="isSubmitting"
                    @change="handleTipoOrigenChange"
                  >
                    <option value="" disabled>Seleccione un tipo</option>
                    <option
                      v-for="option in tipo_origen_options"
                      :key="option.id"
                      :value="option.id"
                    >
                      {{ option.text }}
                    </option>
                  </select>
                </div>

                <!-- Campo: origen -->
                <div class="ufc-input-group">
                  <label for="origen" class="form-label small fw-semibold text-secondary">
                    Origen
                  </label>
                  <select
                    v-if="formData.tipo_origen === 'ac_ccd'"
                    class="form-select form-select-sm border-secondary"
                    v-model="formData.origen"
                    id="origen"
                    name="origen"
                    required
                    :disabled="isSubmitting"
                  >
                    <option value="" disabled>Seleccione un origen</option>
                    <option
                      v-for="entidad in entidades"
                      :key="entidad.id"
                      :value="entidad.nombre"
                    >
                      {{ entidad.id }}-{{ entidad.nombre }}
                    </option>
                  </select>

                  <select
                    v-else-if="formData.tipo_origen === 'puerto'"
                    class="form-select form-select-sm border-secondary"
                    v-model="formData.origen"
                    id="origen"
                    name="origen"
                    required
                    :disabled="isSubmitting"
                  >
                    <option value="" disabled>Seleccione un puerto</option>
                    <option
                      v-for="puerto in puertos"
                      :key="puerto.id"
                      :value="puerto.nombre_puerto"
                    >
                      {{ puerto.id }}- {{ puerto.nombre_puerto }}
                    </option>
                  </select>

                  <select v-else class="form-select form-select-sm border-secondary" disabled>
                    <option value="">Seleccione primero el tipo de origen</option>
                  </select>
                </div>

                <!-- Campo: tipo_equipo -->
                <div class="ufc-input-group">
                  <label for="tipo_equipo" class="form-label small fw-semibold text-secondary">
                    Tipo de Equipo 
                  </label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    v-model="formData.tipo_equipo"
                    id="tipo_equipo"
                    name="tipo_equipo"
                    required
                    :disabled="isSubmitting"
                  >
                    <option value="" disabled>Seleccione un tipo</option>
                    <option
                      v-for="option in tipo_equipo_options"
                      :key="option.id"
                      :value="option.id"
                    >
                      {{ option.text }}
                    </option>
                  </select>
                </div>

                <!-- Campo: estado -->
                <div class="ufc-input-group">
                  <label for="estado" class="form-label small fw-semibold text-secondary">
                    Estado 
                  </label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    v-model="formData.estado"
                    id="estado"
                    name="estado"
                    required
                    :disabled="isSubmitting"
                  >
                    <option value="cargado">Cargado</option>
                    <option value="vacio">Vacio</option>
                  </select>
                </div>

                <!-- Campo: operacion -->
                <div class="ufc-input-group">
                  <label for="operacion" class="form-label small fw-semibold text-secondary">
                    Operación
                  </label>
                  <select
                    class="form-select form-select-sm border-secondary"
                    v-model="formData.operacion"
                    id="operacion"
                    name="operacion"
                    required
                    :disabled="isSubmitting"
                  >
                    <option value="" disabled>Seleccione una operación</option>
                    <option
                      v-for="option in t_operacion_options"
                      :key="option.id"
                      :value="option.id"
                    >
                      {{ option.text }}
                    </option>
                  </select>
                </div>
              </div>

              <!-- Columna 2 -->
              <div>
                <!-- Campo: producto -->
                <div class="mb-3">
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

                <ModalAgregarProducto v-if="mostrarModal" :visible="mostrarModal" @cerrar-modal="cerrarModal"/>

                <!-- Campo: situados -->
                <div class="ufc-input-group">
                  <label for="situados" class="form-label small fw-semibold text-secondary">
                    Situados 
                  </label>
                  <div class="ufc-por-situar-container">
                    <input
                      type="number"
                      class="ufc-por-situar-input"
                      v-model.number="formData.situados"
                      id="situados"
                      name="situados"
                      min="1"
                      required
                      :disabled="isSubmitting"
                    />
                  </div>
                </div>

                <!-- Campo: pendiente_proximo_dia -->
                <div class="ufc-input-group">
                  <label for="pendiente_proximo_dia" class="form-label small fw-semibold text-secondary">
                    Pendientes al próximo día 
                  </label>
                  <div class="ufc-por-situar-container">
                    <input
                      type="number"
                      class="ufc-por-situar-input"
                      v-model.number="formData.pendiente_proximo_dia"
                      id="pendiente_proximo_dia"
                      name="pendiente_proximo_dia"
                      min="0"
                      required
                      :disabled="isSubmitting"
                    />
                  </div>
                </div>

                <!-- Campo: observaciones -->
                <div class="ufc-input-group" >
                  <label for="observaciones" class="form-label small fw-semibold text-secondary">Observaciones</label>
                  <textarea
                    class="form-control form-control-sm border-secondary"
                    v-model="formData.observaciones"
                    id="observaciones"
                    name="observaciones"
                    rows="3"
                    :disabled="isSubmitting"
                  ></textarea>
                </div>
              </div>
            </div>

            <div class="modal-footer">
            <div class=" d-flex justify-content-between align-items-center mb-4">
              <button class="ufc-button secondary" @click="volver_principal">
                <i class="bi bi-x-circle" me-1></i>Cancelar
              </button>
              <button type="submit" class=" ufc-button primary" >
                <i class="bi bi-check-circle" me-1></i>Actualizar
              </button>
            </div>
          </div>
          </form>
        </div>
      </div>
    </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import NavbarComponent from "@/components/NavbarComponent.vue";
import ModalAgregarProducto from "@/components/ModalAgregarProducto.vue";

export default {
  name: "EditarSituados",
  components: {
    NavbarComponent,
    ModalAgregarProducto,
  },
  data() {
    return {
      formData: {
        id: null,
        tipo_origen: "",
        origen: "",
        tipo_equipo: "",
        estado: "cargado",
        operacion: "",
        productos: [], // Cambiamos de producto (singular) a productos (array)
        situados: 0,
        pendiente_proximo_dia: 0,
        observaciones: "",
      },
      productoSearch: "",
      filteredProductos: [],
      showProductosDropdown: false,
      entidades: [],
      puertos: [],
      productos: [],
      mostrarModal: false,
      loading: false,
      registroId: null,
      tipo_origen_options: [
        { id: "ac_ccd", text: "comercial/AccesoCCD" },
        { id: "puerto", text: "Puerto" },
      ],
      tipo_equipo_options: [
  { id: "casilla", text: "Casilla" },
  { id: "caj_gon", text: "Cajones o Góndola" },
  { id: "planc_plat", text: "Plancha o Plataforma" },
  { id: "Plan_porta_cont", text: "Plancha porta contenedores" },
  { id: "cist_liquidos", text: "Cisterna para líquidos" },
  { id: "cist_solidos", text: "Cisterna para sólidos" },
  { id: "tolva_g_mineral", text: "Tolva granelera(mineral)" },
  { id: "tolva_g_agric", text: "Tolva granelera(agrícola)" },
  { id: "tolva_g_cemento", text: "Tolva para cemento" },
  { id: "volqueta", text: "Volqueta" },
  { id: "Vagon_ref", text: "Vagón refrigerado" },
  { id: "jaula", text: "Jaula" },
  { id: "locomotora", text: "Locomotora" },
  { id: "tren", text: "Tren" }
],
      t_operacion_options: [
        { id: "carga", text: "Carga" },
        { id: "descarga", text: "Descarga" },
      ],
      vagonesAsociados: [],
      mostrarModalVagon: false,
      modoEdicionVagon: false,
      vagonEditIndex: null,
      vagonForm: {
        equipo_ferroviario: '',
        dias: 1
      },
      equiposFerroviarios: []
    };
  },
  created() {
    this.registroId = this.$route.params.id;
    if (this.registroId) {
      this.cargarRegistro();
    }
    this.getProductos();
    this.getEntidades();
    this.getPuertos();
  },

  mounted() {
    this.filteredProductos = this.productos;
    this.closeDropdownsOnClickOutside();
  },

  methods: {
    async cargarRegistro() {
  this.loading = true;
  try {
    const response = await axios.get(`/ufc/situados/${this.registroId}/`);
    const registro = response.data;

    this.formData = {
      id: registro.id,
      tipo_origen: registro.tipo_origen,
      origen: registro.origen,
      tipo_equipo: registro.tipo_equipo,
      estado: registro.estado,
      operacion: registro.operacion,
      productos: registro.productos_info?.map((p) => p.id) || [],
      situados: parseInt(registro.situados) || 0,
      pendiente_proximo_dia: parseInt(registro.pendiente_proximo_dia) || 0,
      observaciones: registro.observaciones || "",
    };
    
    if (registro.vagones) {
      this.vagonesAsociados = registro.vagones.map(v => ({
        id: v.id,
        equipo_ferroviario: v.equipo_ferroviario,
        equipo_ferroviario_nombre: v.equipo_ferroviario_numero_identificacion,
        dias: v.dias
      }));
    }
  } catch (error) {
    console.error("Error al cargar el registro:", error);
    Swal.fire("Error", "No se pudo cargar el registro", "error");
    this.$router.push({ name: "InfoOperativo" });
  } finally {
    this.loading = false;
  }
},

    async abrirModalAgregarVagon() {
    try {
      const response = await axios.get('/api/equipos-ferroviarios/');
      this.equiposFerroviarios = response.data.results;
      
      // Excluir equipos ya asociados
      const equiposAsociados = this.vagonesAsociados.map(v => v.equipo_ferroviario);
      this.equiposFerroviarios = this.equiposFerroviarios.filter(
        e => !equiposAsociados.includes(e.id)
      );
      
      this.modoEdicionVagon = false;
      this.vagonForm = {
        equipo_ferroviario: '',
        dias: 1
      };
      this.mostrarModalVagon = true;
    } catch (error) {
      console.error("Error al cargar equipos:", error);
      Swal.fire("Error", "No se pudieron cargar los equipos ferroviarios", "error");
    }
  },
  
  
  
  eliminarVagon(index) {
    Swal.fire({
      title: '¿Eliminar vagón?',
      text: "Esta acción no se puede deshacer",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#002a68',
      cancelButtonColor: '#6c757d',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        this.vagonesAsociados.splice(index, 1);
        Swal.fire(
          'Eliminado',
          'El vagón ha sido eliminado',
          'success'
        );
      }
    });
  },
  
  async guardarVagon() {
    try {
      // Crear el vagón en el backend
      const response = await axios.post('/ufc/vagones-asociados/', this.vagonForm);
      const nuevoVagon = response.data;
      
      // Agregar a la lista local
      this.vagonesAsociados.push({
        id: nuevoVagon.id,
        equipo_ferroviario: nuevoVagon.equipo_ferroviario,
        equipo_ferroviario_nombre: nuevoVagon.equipo_ferroviario_numero_identificacion,
        dias: nuevoVagon.dias
      });
      
      this.cerrarModalVagon();
    } catch (error) {
      console.error("Error al guardar el vagón:", error);
      Swal.fire("Error", "No se pudo guardar el vagón", "error");
    }
  },
  
  cerrarModalVagon() {
    this.mostrarModalVagon = false;
    this.vagonEditIndex = null;
    this.modoEdicionVagon = false;
  },
        this.formData = {
          id: registro.id,
          tipo_origen: registro.tipo_origen || "",
          origen: registro.origen || "",
          tipo_equipo: registro.tipo_equipo || "",
          estado: registro.estado || "cargado",
          operacion: registro.operacion || "",
          productos: registro.productos_info
            ? registro.productos_info.map((p) => p.id)
            : [], // Array de IDs
          situados: registro.situados || 0,
          pendiente_proximo_dia: registro.pendiente_proximo_dia || 0,
          observaciones: registro.observaciones || "",
        };
      } catch (error) {
        console.error("Error al cargar el registro:", error);
        Swal.fire(
          "Error",
          "No se pudo cargar el registro para editar",
          "error"
        );
        this.$router.push({ name: "InfoOperativo" });
      } finally {
        this.loading = false;
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
          this.$router.push({ name: "InfoOperativo" });
        }
      });
    },

    async getEntidades() {
      try {
        let allEntidades = [];
        let nextPage = "/api/entidades/";

        while (nextPage) {
          const response = await axios.get(nextPage);
          allEntidades = [...allEntidades, ...response.data.results];
          nextPage = response.data.next;
        }

        this.entidades = allEntidades;
        return allEntidades;
      } catch (error) {
        console.error("Error al obtener entidades:", error);
        Swal.fire("Error", "No se pudieron obtener las entidades", "error");
        return [];
      }
    },

    async getProductos() {
      try {
        this.loading = true;
        const response = await axios.get("/ufc/producto-vagon/", {
          params: { limit: 100 },
        });

        if (response.status === 200) {
          this.productos = response.data.results.map((producto) => ({
            id: producto.id,
            producto_name:
              producto.producto_name ||
              producto.descripcion ||
              `Producto ${producto.id}`,
            producto_codigo: producto.producto_codigo || "N/A",
            tipo_embalaje_name: producto.tipo_embalaje?.nombre || "N/A",
          }));
        }
      } catch (error) {
        console.error("Error al obtener productos:", error);
        let errorMsg = "Error al cargar productos";

        if (error.response?.data?.detail) {
          errorMsg += `: ${error.response.data.detail}`;
        }

        Swal.fire("Error", errorMsg, "error");
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
      this.mostrarModal = true;
    },

    cerrarModal() {
      this.mostrarModal = false;
      this.getProductos();
    },

    async submitForm() {
  if (this.loading) return;
  
  this.loading = true;
  try {
    // Validación adicional
    if (this.formData.estado === 'cargado' && this.formData.productos.length === 0) {
      throw new Error("Debe seleccionar al menos un producto cuando el estado es Cargado");
    }

    const payload = {
      tipo_origen: this.formData.tipo_origen,
      origen: this.formData.origen,
      tipo_equipo: this.formData.tipo_equipo,
      estado: this.formData.estado,
      operacion: this.formData.operacion,
      producto: this.formData.productos, // Nota: el backend espera 'producto' no 'productos'
      pendiente_proximo_dia: this.formData.pendiente_proximo_dia.toString(),
      observaciones: this.formData.observaciones,
      vagones_ids: this.vagonesAsociados.map(v => v.id) // Enviar IDs de vagones asociados
    };

    const response = await axios.put(
      `/ufc/situados/${this.registroId}/`,
      payload
    );

    await Swal.fire({
      title: "Éxito",
      text: "Registro actualizado correctamente",
      icon: "success",
      confirmButtonColor: "#002a68"
    });
    
    this.$router.push({ name: "InfoOperativo" });
  } catch (error) {
    let errorMessage = "Error al actualizar el registro";
    
    if (error.response) {
      if (error.response.status === 400) {
        // Manejar errores de validación del backend
        const errors = error.response.data;
        errorMessage = Object.values(errors).flat().join("\n");
      } else if (error.response.status === 404) {
        errorMessage = "El registro no fue encontrado";
      }
    } else if (error.message) {
      errorMessage = error.message;
    }

    Swal.fire({
      title: "Error",
      text: errorMessage,
      icon: "error",
      confirmButtonColor: "#002a68"
    });
  } finally {
    this.loading = false;
  }
},
    confirmCancel() {
      Swal.fire({
        title: "¿Cancelar cambios?",
        text: "Los cambios no guardados se perderán",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, cancelar",
        cancelButtonText: "No, continuar",
      }).then((result) => {
        if (result.isConfirmed) {
          this.$router.push({ name: "InfoOperativo" });
        }
      });
    },

    toggleProductosDropdown() {
      this.showProductosDropdown = !this.showProductosDropdown;
      if (this.showProductosDropdown) {
        this.productoSearch = "";
        this.filterProductos();
      }
    },

    filterProductos() {
      if (!this.productoSearch) {
        this.filteredProductos = this.productos;
        return;
      }
      const searchTerm = this.productoSearch.toLowerCase();
      this.filteredProductos = this.productos.filter(
        (producto) =>
          producto.producto_name.toLowerCase().includes(searchTerm) ||
          producto.producto_codigo.toLowerCase().includes(searchTerm) ||
          producto.id.toString().includes(searchTerm)
      );
    },

    toggleProductoSelection(productoId) {
      const index = this.formData.productos.indexOf(productoId);
      if (index === -1) {
        this.formData.productos.push(productoId); // Agrega el producto
      } else {
        this.formData.productos.splice(index, 1); // Elimina el producto
      }
    },

    getSelectedProductosText() {
      if (this.formData.productos.length === 0) return "";
      if (this.formData.estado === "vacio") {
        return `${this.formData.productos.length} producto(s) seleccionado(s)`;
      }
      if (this.formData.productos.length === 1) {
        const producto = this.productos.find(
          (p) => p.id === this.formData.productos[0]
        );
        return producto
          ? `${producto.id}-${producto.producto_name}`
          : "1 producto seleccionado";
      }
      return `${this.formData.productos.length} productos seleccionados`;
    },

    closeDropdownsOnClickOutside() {
      document.addEventListener("click", (e) => {
        if (!e.target.closest(".ufc-custom-select")) {
          this.showProductosDropdown = false;
        }
      });
    },
  },
};
</script>

<style scoped>
/* Estilos para la sección de vagones asociados */
.ufc-vagones-container {
  margin-top: 30px;
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.ufc-vagones-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.ufc-vagones-header h3 {
  color: #002a68;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
}

.ufc-button.small {
  padding: 6px 12px;
  font-size: 0.8rem;
}

.ufc-vagones-table-container {
  overflow-x: auto;
}

.ufc-vagones-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.ufc-vagones-table th {
  background-color: #002a68;
  color: white;
  padding: 10px 12px;
  text-align: left;
  font-weight: 500;
  font-size: 0.85rem;
}

.ufc-vagones-table td {
  padding: 12px;
  border-bottom: 1px solid #eee;
  font-size: 0.85rem;
}

.ufc-vagones-table tr:hover {
  background-color: #f8f9fa;
}

.ufc-actions-cell {
  display: flex;
  gap: 8px;
}

.ufc-icon-button {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.ufc-icon-button i {
  font-size: 0.9rem;
}

.ufc-icon-button.warning {
  background-color: #ffc107;
  color: #212529;
}

.ufc-icon-button.warning:hover {
  background-color: #e0a800;
}

.ufc-icon-button.danger {
  background-color: #dc3545;
  color: white;
}

.ufc-icon-button.danger:hover {
  background-color: #c82333;
}

/* Estilo para estado vacío */
.ufc-vagones-empty {
  margin-top: 20px;
  text-align: center;
  padding: 30px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.ufc-empty-state {
  color: #6c757d;
}

.ufc-empty-state i {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #adb5bd;
}

.ufc-empty-state p {
  margin: 0;
  font-size: 0.9rem;
}

/* Estilos para el modal de vagón */
.ufc-modal-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.ufc-modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}




/* Estilos para el select personalizado de productos */
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

.ufc-select[multiple] {
  height: auto;
  min-height: 100px;
  padding: 8px;
}

.ufc-select[multiple] option {
  padding: 6px 8px;
  margin: 2px 0;
  border-radius: 4px;
}

.ufc-select[multiple] option:checked {
  background-color: #002a68;
  color: white;
}

.ufc-selected-products {
  font-size: 0.8rem;
  color: #666;
  margin-top: 5px;
}

.ufc-form-container {
  font-family: "Segoe UI", Roboto, -apple-system, sans-serif;
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

.ufc-form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

@media (max-width: 768px) {
  .ufc-form-grid {
    grid-template-columns: 1fr;
  }
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

.ufc-select,
.ufc-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.85rem;
  transition: all 0.2s;
  background-color: white;
}

.ufc-select:focus,
.ufc-input:focus {
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

.ufc-disabled {
  font-size: 0.8rem;
  color: #777;
  padding: 8px 0;
}

/* Estilo especial para el campo por situar */
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