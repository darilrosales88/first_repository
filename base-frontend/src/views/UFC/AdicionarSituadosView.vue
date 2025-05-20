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
          <i class="bi bi-file-earmark-plus me-2"></i> Nuevo registro de situados</h5>
      </div>
        <div class="card-body p-3">
          <form @submit.prevent="submitForm">
            <div class="ufc-form-grid">
              <!-- Columna 1 -->
              <div>
                <!-- Campo:Fecha de registro -->
                <div class="mb-3">
                  <label for="fecha_registro" class="form-label small fw-semibold text-secondary"
                    >Fecha de registro</label
                  >
                  <input
                    type="text"
                    class="form-control form-control-sm border-secondary"
                    :value="formattedFechaRegistro"
                    id="fecha_registro"
                    name="fecha_registro"
                    readonly
                  />
                </div>
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
                <i class="bi bi-check-circle" me-1></i>Agregar
              </button>
            </div>
          </div>
        </form>

        


      </div>


<!-- Tabla de Vagones Asociados -->
<div class="ufc-vagones-container">
  <div class="ufc-vagones-header">
    <h3><i class="bi bi-train-freight-front"></i> Vagones Asociados</h3>
    <div>
      <span class="ufc-vagones-count">
        {{ vagonesAsociados.length }} / {{ formData.situados }}
      </span>
      <button 
        class="ufc-button primary small"
        @click="abrirModalAgregarVagon"
        :disabled="vagonesAsociados.length >= formData.situados"
      >
        <i class="bi bi-plus-circle"></i> Agregar Vagón
      </button>
    </div>
  </div>

  <!-- Tabla cuando hay datos -->
  <div v-if="vagonesAsociados.length > 0" class="ufc-vagones-table-container">
    <table class="ufc-vagones-table">
      <thead>
        <tr>
          <th>Equipo Ferroviario</th>
          <th>Días</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(vagon, index) in vagonesAsociados" :key="index">
          <td>{{ vagon.equipo_ferroviario_nombre }}</td>
          <td>{{ vagon.dias }}</td>
          <td class="ufc-actions-cell">
            <button 
              class="ufc-icon-button danger"
              @click="eliminarVagon(index)"
              title="Eliminar"
            >
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
            required
          >
            <option value="" disabled>Seleccione un equipo</option>
            <option 
              v-for="equipo in equiposFerroviarios" 
              :key="equipo.id"
              :value="equipo.id"
            >
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
            required
          />
        </div>

        <div class="ufc-modal-actions">
          <button 
            type="button" 
            class="ufc-button secondary"
            @click="cerrarModalVagon"
          >
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
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import NavbarComponent from "@/components/NavbarComponent.vue";
import ModalAgregarProducto from "@/components/ModalAgregarProducto.vue";

export default {
  name: "AdicionarSituados",
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
        tipo_equipo: "",
        estado: "cargado",
        operacion: "",
        productos: [], // Cambiamos de producto (singular) a productos (array)
        situados: 1,
        pendiente_proximo_dia: 0,
        observaciones: "",
      },
      entidades: [],
      puertos: [],
      productos: [],
      productoSearch: "",
      filteredProductos: [],
      showProductosDropdown: false,
      mostrarModal: false,
      loadingProducts: false,
      isSubmitting: false,

      tipo_origen_options: [
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
      vagonesAsociados: [], // Aquí se almacenarán los vagones antes de enviar
      equiposFerroviarios: [], // Lista de equipos disponibles
      mostrarModalVagon: false,
      vagonForm: {
        equipo_ferroviario: '',
        dias: 1
      },
      vagonEditIndex: null,
      modoEdicionVagon: false
    };
  },
  mounted() {
    this.getProductos();
    this.getEntidades();
    this.getPuertos();
    this.closeDropdownsOnClickOutside();
  },
  computed: {
    formattedFechaRegistro() {
      if (this.formData.fecha) {
        return new Date(this.formData.fecha).toLocaleString();
      }
      return new Date().toLocaleString();
    },
  },
  methods: {
    async abrirModalAgregarVagon() {
      try {
        // Cargar equipos ferroviarios disponibles
        const response = await axios.get('/api/equipos-ferroviarios/', {
          params: {
            exclude_tipo: 'locomotora', // Excluir locomotoras
            estado: 'activo' // Solo equipos activos
          }
        });
        
        // Filtrar equipos que no estén ya en la lista de vagones asociados
        const equiposDisponibles = response.data.results.filter(equipo => 
          !this.vagonesAsociados.some(v => v.equipo_ferroviario === equipo.id)
        );
        
        this.equiposFerroviarios = equiposDisponibles;
        
        if (this.equiposFerroviarios.length === 0) {
          Swal.fire({
            title: 'No hay equipos disponibles',
            text: 'Todos los equipos ferroviarios ya están asociados o no hay equipos activos',
            icon: 'info'
          });
          return;
        }
        
        this.modoEdicionVagon = false;
        this.vagonForm = {
          equipo_ferroviario: this.equiposFerroviarios[0]?.id || '',
          dias: 1
        };
        this.mostrarModalVagon = true;
      } catch (error) {
        console.error("Error al cargar equipos:", error);
        Swal.fire("Error", "No se pudieron cargar los equipos ferroviarios", "error");
      }
    },

    guardarVagon() {
      // Validación
      if (!this.vagonForm.equipo_ferroviario || !this.vagonForm.dias || this.vagonForm.dias < 1) {
        Swal.fire('Error', 'Complete todos los campos correctamente', 'error');
        return;
      }
      
      // Buscar el equipo seleccionado para obtener su nombre
      const equipoSeleccionado = this.equiposFerroviarios.find(
        e => e.id === this.vagonForm.equipo_ferroviario
      );
      
      const vagonData = {
        equipo_ferroviario: this.vagonForm.equipo_ferroviario,
        equipo_ferroviario_nombre: equipoSeleccionado 
          ? `${equipoSeleccionado.numero_identificacion} - ${equipoSeleccionado.tipo_equipo.tipo_equipo}`
          : 'Equipo no encontrado',
        dias: this.vagonForm.dias
      };
      
      if (this.modoEdicionVagon) {
        // Editar existente
        this.vagonesAsociados[this.vagonEditIndex] = vagonData;
        Swal.fire('Actualizado', 'El vagón ha sido actualizado', 'success');
      } else {
        // Agregar nuevo
        this.vagonesAsociados.push(vagonData);
        Swal.fire('Agregado', 'El vagón ha sido agregado', 'success');
      }
      
      // Actualizar el campo situados automáticamente
      this.formData.situados = this.vagonesAsociados.length;
      
      this.cerrarModalVagon();
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
          // Actualizar el campo situados automáticamente
          this.formData.situados = this.vagonesAsociados.length;
          Swal.fire(
            'Eliminado',
            'El vagón ha sido eliminado',
            'success'
          );
        }
      });
    },
  
  cerrarModalVagon() {
    this.mostrarModalVagon = false;
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
      try {
        let allProductos = [];
        let nextPage = "/ufc/producto-vagon/"; // URL inicial

        while (nextPage) {
          const response = await axios.get(nextPage);
          allProductos = [...allProductos, ...response.data.results];

          // Actualiza nextPage con la URL de la siguiente página (null si no hay más)
          nextPage = response.data.next;
        }

        this.productos = allProductos;
      } catch (error) {
        console.error("Error al obtener los productos:", error);
        Swal.fire("Error", "Hubo un error al obtener los productos.", "error");
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

    async getPuertos() {
      try {
        const response = await axios.get("/api/puertos/");
        this.puertos = response.data.results;
      } catch (error) {
        console.error("Error al obtener los puertos:", error);
        Swal.fire("Error", "Hubo un error al obtener los puertos.", "error");
      }
    },

    handleTipoOrigenChange() {
      this.formData.origen = "";
      if (this.formData.tipo_origen === "ac_ccd") {
        this.formData.tipo_origen = "ac_ccd";
      } else if (this.formData.tipo_origen === "puerto") {
        this.formData.tipo_origen = "puerto";
      }
    },

    abrirModalAgregarProducto() {
      this.mostrarModal = true;
    },

    cerrarModal() {
      this.mostrarModal = false;
      this.getProductos();
    },

    increment(field) {
      this.formData[field] += 1;
    },

    decrement(field) {
      if (this.formData[field] > (field === "situados" ? 1 : 0)) {
        this.formData[field] -= 1;
      }
    },

    async verificarInformeOperativo() {
      try {
        this.formData.fecha = new Date().toISOString();
        const today = new Date();
        const fechaFormateada = `${today.getFullYear()}-${String(
          today.getMonth() + 1
        ).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;

        const response = await axios.get("/ufc/verificar-informe-existente/", {
          params: { fecha_operacion: fechaFormateada },
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

      this.isSubmitting = true;
      try {
        // Validación mejorada
        const errors = [];

        if (
          !this.formData.tipo_origen ||
          !this.tipo_origen_options.some(
            (opt) => opt.id === this.formData.tipo_origen
          )
        ) {
          errors.push("Seleccione un tipo de origen válido");
        }

        if (!this.formData.origen) {
          errors.push("El campo Origen es requerido");
        }

        if (!this.formData.tipo_equipo) {
          errors.push("El campo Tipo de Equipo es requerido");
        }

        if (!this.formData.operacion) {
          errors.push("El campo Operación es requerido");
        }

        if (
          this.formData.estado === "cargado" &&
          this.formData.productos.length === 0
        ) {
          throw new Error(
            "Debe seleccionar al menos un producto cuando el estado es Cargado"
          );
        }

        if (this.formData.situados === null || this.formData.situados < 1) {
          errors.push("La cantidad de situados debe ser al menos 1");
        }

        if (
          this.formData.pendiente_proximo_dia === null ||
          this.formData.pendiente_proximo_dia < 0
        ) {
          errors.push(
            "Los pendientes al próximo día deben ser un número positivo"
          );
        }

        if (errors.length > 0) {
          throw new Error(errors.join("\n"));
        }

        if (this.vagonesAsociados.length !== this.formData.situados) {
        Swal.fire({
          title: 'Advertencia',
          text: `El número de vagones asociados (${this.vagonesAsociados.length}) no coincide con la cantidad "Situados" (${this.formData.situados}). ¿Desea actualizar el campo "Situados" para que coincida?`,
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Sí, actualizar',
          cancelButtonText: 'No, corregir manualmente'
        }).then((result) => {
          if (result.isConfirmed) {
            this.formData.situados = this.vagonesAsociados.length;
          }
        });
        return;
      }


        // Preparar datos para enviar
        const payload = {
          tipo_origen: this.formData.tipo_origen,
          origen: this.formData.origen,
          tipo_equipo: this.formData.tipo_equipo,
          estado: this.formData.estado,
          operacion: this.formData.operacion,
          producto: this.formData.productos, // Array de IDs
          situados: this.formData.situados,
          pendiente_proximo_dia: this.formData.pendiente_proximo_dia,
          observaciones: this.formData.observaciones,
          vagones_asociados: this.vagonesAsociados.map(v => ({
          equipo_ferroviario: v.equipo_ferroviario,
          dias: v.dias
        }))
        };
        

        // Enviar datos al endpoint
        const response = await axios.post("/ufc/situados/", payload);

        // Mostrar mensaje de éxito
        await Swal.fire({
          title: "¡Éxito!",
          text: "El registro ha sido creado correctamente",
          icon: "success",
          confirmButtonText: "Aceptar",
        });

        // Resetear el formulario después de enviar
        this.resetForm();
        this.$router.push({ name: 'ListaSituados' });

      } catch (error) {
        console.error("Error al enviar el formulario:", error);
        Swal.fire({
          title: "Error",
          text: error.message || "Ocurrió un error al procesar la solicitud",
          icon: "error",
        });
      } finally {
        this.isSubmitting = false;
      }
    },

    resetForm() {
      this.formData = {
        tipo_origen: "",
        origen: "",
        tipo_equipo: "",
        estado: "cargado",
        operacion: "",
        productos: [],
        situados: 1,
        pendiente_proximo_dia: 0,
        observaciones: "",
      };
      this.vagonesAsociados = [];
    },

    async confirmCancel() {
      const result = await Swal.fire({
        title: "¿Cancelar operación?",
        text: "Los datos no guardados se perderán",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Sí, cancelar",
        cancelButtonText: "No, continuar",
        reverseButtons: true,
      });

      if (result.isConfirmed) {
        this.resetForm();
        this.$router.push({ name: "InfoOperativo" });
      }
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
        this.formData.productos.push(productoId);
      } else {
        this.formData.productos.splice(index, 1);
      }
    },

    getSelectedProductosText() {
      if (this.formData.productos.length === 0) return "";

      // Si el estado es vacío, mostramos solo el conteo
      if (this.formData.estado === "vacio") {
        return `${this.formData.productos.length} producto(s) seleccionado(s)`;
      }

      // Para estado cargado, mostramos más detalles
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
