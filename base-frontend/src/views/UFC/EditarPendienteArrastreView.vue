<template>
  <div class="ufc-form-container">
    <!-- Encabezado corporativo -->
    <div class="ufc-header">
      <h6>Partes UFC</h6>
    </div>
    
    <Navbar-Component />
    <Producto-Vagones />
    
    <div class="ufc-form-wrapper">
      <div class="ufc-form-card">
        <h2 class="ufc-form-title">
          <i class="bi bi-pencil-square"></i> Editar registro pendiente a arrastre
        </h2>

        <form @submit.prevent="submitForm" class="ufc-form">
          <!-- Primera fila - Origen y Destino -->
          <div class="ufc-form-grid">
            <!-- Grupo Origen -->
            <div class="ufc-form-group">
              <div class="ufc-form-row">
                <!-- Campo: tipo_origen -->
                <div class="ufc-input-group paired">
                  <label for="tipo_origen">Tipo de Origen <span class="required">*</span></label>
                  <select
                    class="ufc-select"
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
                  <label for="origen">Origen <span class="required">*</span></label>
                  <select
                    v-if="formData.tipo_origen && formData.tipo_origen !== 'puerto'"
                    class="ufc-select"
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
                    class="ufc-select"
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
                    class="ufc-select"
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
                  <label for="tipo_destino">Tipo de Destino <span class="required">*</span></label>
                  <select
                    class="ufc-select"
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
                  <label for="destino">Destino <span class="required">*</span></label>
                  <select
                    v-if="formData.tipo_destino && formData.tipo_destino !== 'puerto'"
                    class="ufc-select"
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
                    class="ufc-select"
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
                    class="ufc-select"
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
                <label for="tipo_equipo">Tipo de Equipo <span class="required">*</span></label>
                <select
                  class="ufc-select"
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
                <label for="estado">Estado <span class="required">*</span></label>
                <select
                  class="ufc-select"
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
                <label for="operacion">Operación <span class="required">*</span></label>
                <select
                  class="ufc-select"
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
                <label for="cantidad_vagones">Cantidad de Vagones <span class="required">*</span></label>
                <div class="ufc-por-situar-container">
                  <input
                    type="number"
                    class="ufc-por-situar-input"
                    v-model.number="formData.cantidad_vagones"
                    min="1"
                    required
                    readonly>
                  <span class="ufc-por-situar-suffix">unidades</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Tercera fila - Productos -->
          <div class="ufc-input-group full-width">
            <label for="producto">Productos <span v-if="formData.estado === 'cargado'" class="required">*</span></label>
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
              <button 
                class="ufc-add-button"
                @click.prevent="abrirModalAgregarProducto">
                <i class="bi bi-plus-circle"></i>
              </button>
            </div>
          </div>

          <!-- Observaciones (full width) -->
          <div class="ufc-input-group full-width">
            <label for="observaciones">Observaciones</label>
            <textarea
              class="ufc-textarea"
              v-model="formData.observaciones"
              rows="2"></textarea>
          </div>

          <!-- Botones de acción -->
          <div class="ufc-form-actions">
            <button type="button" class="ufc-button secondary" @click="confirmCancel">
              <i class="bi bi-x-circle"></i> Cancelar
            </button>
            <button type="submit" class="ufc-button primary">
              <i class="bi bi-check-circle"></i> Actualizar
            </button>
          </div>
        </form>

        <!-- Tabla de Vagones Asociados -->
        <div class="ufc-vagones-container">
          <div class="ufc-vagones-header">
            <h3><i class="bi bi-train-freight-front"></i> Vagones Asociados</h3>
            <button 
              class="ufc-button primary small"
              @click="abrirModalAgregarVagon">
              <i class="bi bi-plus-circle"></i> Agregar Vagón
            </button>
          </div>

          <!-- Tabla cuando hay datos -->
          <div v-if="vagonesAsociados.length > 0" class="ufc-vagones-table-container">
            <table class="ufc-vagones-table">
              <thead>
                <tr>
                  <th>No.</th>
                  <th>Equipo Ferroviario</th>
                  <th>Días</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(vagon, index) in vagonesAsociados" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td>{{ vagon.equipo_ferroviario_nombre }}</td>
                  <td>{{ vagon.dias }}</td>
                  <td class="ufc-actions-cell">
                    <button 
                      class="ufc-icon-button danger"
                      @click="eliminarVagon(index)"
                      title="Eliminar">
                      <i class="bi bi-trash"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Mensaje cuando no hay datos -->
          <div v-else class="ufc-vagones-empty">
            <div class="ufc-empty-state">
              <i class="bi bi-train-freight-front"></i>
              <p>No hay vagones asociados</p>
            </div>
          </div>
        </div>

        <!-- Modal para agregar/editar vagón -->
        <div v-if="mostrarModalVagon" class="ufc-modal-overlay">
          <div class="ufc-modal-container">
            <div class="ufc-modal-header">
              <h3>
                <i class="bi bi-train-freight-front"></i> 
                {{ modoEdicionVagon ? 'Editar Vagón' : 'Agregar Vagón' }}
              </h3>
              <button @click="cerrarModalVagon" class="ufc-modal-close">
                <i class="bi bi-x"></i>
              </button>
            </div>
            <div class="ufc-modal-body">
              <form @submit.prevent="guardarVagon" class="ufc-modal-form">
                <div class="ufc-input-group">
                  <label for="equipo_ferroviario">Equipo Ferroviario <span class="required">*</span></label>
                  <select
                    class="ufc-select"
                    v-model="vagonForm.equipo_ferroviario"
                    required>
                    <option value="" disabled>Seleccione un equipo</option>
                    <option 
                      v-for="equipo in equiposFerroviarios" 
                      :key="equipo.id"
                      :value="equipo.id">
                      {{ equipo.numero_identificacion }} - {{ equipo.tipo_equipo.tipo_equipo }}
                    </option>
                  </select>
                </div>

                <div class="ufc-input-group">
                  <label for="dias">Días <span class="required">*</span></label>
                  <input
                    type="number"
                    class="ufc-input"
                    v-model.number="vagonForm.dias"
                    min="1"
                    required/>
                </div>

                <div class="ufc-modal-actions">
                  <button 
                    type="button" 
                    class="ufc-button secondary"
                    @click="cerrarModalVagon">
                    Cancelar
                  </button>
                  <button type="submit" class="ufc-button primary">
                    {{ modoEdicionVagon ? 'Guardar Cambios' : 'Agregar' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal para agregar producto -->
    <div v-if="mostrarModal" class="ufc-modal-overlay">
      <div class="ufc-modal-container">
        <div class="ufc-modal-header">
          <h3><i class="bi bi-box-seam"></i> Nuevo Producto</h3>
          <button @click="cerrarModal" class="ufc-modal-close">
            <i class="bi bi-x"></i>
          </button>
        </div>
        <div class="ufc-modal-body">
          <ModalAgregarProducto
            :visible="mostrarModal"
            @cerrar-modal="cerrarModal"
          />
        </div>
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
  name: "EditarPendienteArrastre",
  components: {
    NavbarComponent,
    ModalAgregarProducto,
  },
  data() {
    return {
      registroId: null,
      formData: {
        tipo_origen: "",
        origen: "",
        tipo_destino: "",
        destino: "",
        tipo_equipo: "",
        operacion: "",
        estado: "cargado",
        productos: [],
        cantidad_vagones: 0,
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
      equiposFerroviarios: [],
      vagonesAsociados: [],
      mostrarModalVagon: false,
      modoEdicionVagon: false,
      vagonForm: {
        equipo_ferroviario: "",
        dias: 1
      },
      vagonEditIndex: null,
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
        { id: "tren", text: "Tren" },
      ],
      t_operacion_options: [
        { id: "carga", text: "Carga" },
        { id: "descarga", text: "Descarga" },
      ],
    };
  },
  async created() {
    this.registroId = this.$route.params.id;
    await this.getEquiposFerroviarios();
    await this.cargarRegistro();
    await this.getProductos();
    await this.getEntidades();
    await this.getPuertos();
    this.closeDropdownsOnClickOutside();
  },
  methods: {
    async getEquiposFerroviarios() {
      try {
        const response = await axios.get('/api/equipos-ferroviarios/');
        this.equiposFerroviarios = response.data.results;
      } catch (error) {
        console.error("Error al obtener equipos ferroviarios:", error);
        Swal.fire("Error", "No se pudieron obtener los equipos ferroviarios", "error");
      }
    },

    async cargarRegistro() {
      try {
        const response = await axios.get(`/ufc/pendiente-arrastre/${this.registroId}/`);
        const registro = response.data;
        
        // Mapear los datos del registro al formulario
        this.formData = {
          tipo_origen: registro.tipo_origen,
          origen: registro.origen,
          tipo_destino: registro.tipo_destino,
          destino: registro.destino,
          tipo_equipo: registro.tipo_equipo,
          operacion: registro.operacion,
          estado: registro.estado,
          productos: registro.producto || [],
          cantidad_vagones: registro.equipo_vagon?.length || 0,
          observaciones: registro.observaciones || "",
        };
        
        // Cargar vagones asociados
        if (registro.equipo_vagon_detalle) {
          this.vagonesAsociados = registro.equipo_vagon_detalle.map(v => ({
            id: v.id,
            equipo_ferroviario: v.equipo_ferroviario.id,
            equipo_ferroviario_nombre: v.equipo_ferroviario.numero_identificacion,
            dias: v.dias
          }));
        }
        
        // Actualizar productos filtrados después de cargar
        this.filteredProductos = this.productos;
      } catch (error) {
        console.error("Error al cargar el registro:", error);
        Swal.fire("Error", "No se pudo cargar el registro", "error");
        this.$router.push({ name: "InfoOperativo" });
      }
    },

    abrirModalAgregarVagon() {
      this.vagonForm = {
        equipo_ferroviario: "",
        dias: 1
      };
      this.modoEdicionVagon = false;
      this.mostrarModalVagon = true;
    },

    editarVagon(index) {
      const vagon = this.vagonesAsociados[index];
      this.vagonForm = {
        equipo_ferroviario: vagon.equipo_ferroviario,
        dias: vagon.dias
      };
      this.vagonEditIndex = index;
      this.modoEdicionVagon = true;
      this.mostrarModalVagon = true;
    },

    async guardarVagon() {
      try {
        if (this.modoEdicionVagon) {
          // Actualizar vagon existente
          const vagonId = this.vagonesAsociados[this.vagonEditIndex].id;
          await axios.put(`/ufc/vagones-asociados/${vagonId}/`, this.vagonForm);
          
          // Actualizar localmente
          const equipoSeleccionado = this.equiposFerroviarios.find(
            e => e.id === this.vagonForm.equipo_ferroviario
          );
          
          this.vagonesAsociados[this.vagonEditIndex] = {
            id: vagonId,
            equipo_ferroviario: this.vagonForm.equipo_ferroviario,
            equipo_ferroviario_nombre: equipoSeleccionado.numero_identificacion,
            dias: this.vagonForm.dias
          };
          
          Swal.fire("Éxito", "Vagón actualizado correctamente", "success");
        } else {
          // Crear nuevo vagon
          const response = await axios.post('/ufc/vagones-asociados/', {
            ...this.vagonForm,
            pendiente_arrastre: this.registroId
          });
          
          const nuevoVagon = response.data;
          const equipoSeleccionado = this.equiposFerroviarios.find(
            e => e.id === nuevoVagon.equipo_ferroviario
          );
          
          this.vagonesAsociados.push({
            id: nuevoVagon.id,
            equipo_ferroviario: nuevoVagon.equipo_ferroviario,
            equipo_ferroviario_nombre: equipoSeleccionado.numero_identificacion,
            dias: nuevoVagon.dias
          });
          
          this.formData.cantidad_vagones = this.vagonesAsociados.length;
          Swal.fire("Éxito", "Vagón agregado correctamente", "success");
        }
        
        this.cerrarModalVagon();
      } catch (error) {
        console.error("Error al guardar el vagón:", error);
        Swal.fire("Error", "No se pudo guardar el vagón", "error");
      }
    },

    async eliminarVagon(index) {
      const vagon = this.vagonesAsociados[index];
      try {
        await axios.delete(`/ufc/vagones-asociados/${vagon.id}/`);
        this.vagonesAsociados.splice(index, 1);
        this.formData.cantidad_vagones = this.vagonesAsociados.length;
        Swal.fire("Éxito", "Vagón eliminado correctamente", "success");
      } catch (error) {
        console.error("Error al eliminar el vagón:", error);
        Swal.fire("Error", "No se pudo eliminar el vagón", "error");
      }
    },

    cerrarModalVagon() {
      this.mostrarModalVagon = false;
      this.vagonForm = {
        equipo_ferroviario: "",
        dias: 1
      };
      this.vagonEditIndex = null;
      this.modoEdicionVagon = false;
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
      this.mostrarModal = true;
    },

    cerrarModal() {
      this.mostrarModal = false;
      this.getProductos();
    },

    handleEstadoChange() {
      if (this.formData.estado === 'vacio') {
        this.formData.productos = [];
      }
    },

    async submitForm() {
      try {
        // Validación de campos requeridos
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

        // Preparar los datos para enviar
        const payload = {
          tipo_origen: this.formData.tipo_origen,
          origen: this.formData.origen,
          tipo_destino: this.formData.tipo_destino,
          destino: this.formData.destino,
          tipo_equipo: this.formData.tipo_equipo,
          operacion: this.formData.operacion,
          estado: this.formData.estado,
          producto: this.formData.productos,
          cantidad_vagones: this.vagonesAsociados.length,
          observaciones: this.formData.observaciones,
          equipo_vagon: this.vagonesAsociados.map(v => v.id)
        };

        // Enviar los datos actualizados al backend
        const response = await axios.put(`/ufc/pendiente-arrastre/${this.registroId}/`, payload);
        
        // Mostrar mensaje de éxito
        Swal.fire({
          title: "¡Éxito!",
          text: "El registro ha sido actualizado correctamente",
          icon: "success",
          confirmButtonText: "Aceptar"
        }).then(() => {
          this.$router.push({ name: "InfoOperativo" });
        });

      } catch (error) {
        console.error("Error al enviar el formulario:", error);
        
        let errorMessage = "Hubo un error al actualizar el registro";
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
      });
    }
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
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  display: flex;
  align-items: center;
  gap: 6px;
}

.ufc-button.primary {
  background: #002a68;
  color: white;
}

.ufc-button.primary:hover {
  background: #003d8f;
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.ufc-button.secondary {
  background: white;
  color: #555;
  border: 1px solid #ddd;
}

.ufc-button.secondary:hover {
  background: #f8f9fa;
  border-color: #ccc;
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