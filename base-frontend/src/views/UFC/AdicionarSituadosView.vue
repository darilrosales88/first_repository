<template>
  <!-- Encabezado corporativo -->
  <div class="ufc-header">
    <h6>Partes UFC</h6>
  </div>
  <Navbar-Component />
  <Producto-Vagones />
  <div class="ufc-form-container">
    <div class="ufc-form-wrapper">
      <div class="ufc-form-card">
        <h2 class="ufc-form-title">
          <i class="bi bi-clipboard-plus"></i>
          Nuevo registro de situados
        </h2>

        <form @submit.prevent="submitForm">
          <div class="ufc-form-grid">
            <!-- Columna 1 -->
            <div>
              <!-- Campo:Fecha de registro -->
              <div class="mb-3">
                <label for="fecha_registro" class="form-label"
                  >Fecha de registro</label
                >
                <input
                  type="text"
                  class="form-control"
                  :value="formattedFechaRegistro"
                  id="fecha_registro"
                  name="fecha_registro"
                  readonly
                />
              </div>
              <!-- Campo: tipo_origen -->
              <div class="ufc-input-group">
                <label for="tipo_origen">
                  Tipo de Origen <span class="required">*</span>
                </label>
                <select
                  class="ufc-select"
                  v-model="formData.tipo_origen"
                  id="tipo_origen"
                  name="tipo_origen"
                  required
                  :disabled="isSubmitting"
                  @change="handleTipoOrigenChange"
                >
                  @change="handleTipoOrigenChange" >
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
                <label for="origen">
                  Origen <span class="required">*</span>
                </label>
                <select
                  v-if="formData.tipo_origen === 'ac_ccd'"
                  class="ufc-select"
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
                    :value="entidad.nombre">
                    {{ entidad.id }}-{{ entidad.nombre }}
                  </option>
                </select>

                <select
                  v-else-if="formData.tipo_origen === 'puerto'"
                  class="ufc-select"
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

                <select v-else class="ufc-select" disabled>
                  <option value="">Seleccione primero el tipo de origen</option>
                </select>
              </div>

              <!-- Campo: tipo_equipo -->
              <div class="ufc-input-group">
                <label for="tipo_equipo">
                  Tipo de Equipo <span class="required">*</span>
                </label>
                <select
                  class="ufc-select"
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
                <label for="estado">
                  Estado <span class="required">*</span>
                </label>
                <select
                  class="ufc-select"
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
                <label for="operacion">
                  Operación <span class="required">*</span>
                </label>
                <select
                  class="ufc-select"
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
              <div class="ufc-input-group">
                <label for="productos"
                  >Productos
                  <span v-if="formData.estado === 'cargado'" class="required"
                    >*</span
                  ></label
                >
                <div class="ufc-input-with-action">
                  <div
                    class="ufc-custom-select"
                    @click="toggleProductosDropdown"
                  >
                    <div class="ufc-select-display">
                      {{
                        getSelectedProductosText() || "Seleccione productos..."
                      }}
                    </div>
                    <i class="bi bi-chevron-down ufc-select-arrow"></i>

                    <div
                      class="ufc-productos-dropdown"
                      v-if="showProductosDropdown"
                    >
                      <div class="ufc-productos-search-container">
                        <input
                          type="text"
                          class="ufc-productos-search"
                          placeholder="Buscar productos..."
                          v-model="productoSearch"
                          @input="filterProductos"
                          @click.stop
                        />
                      </div>
                      <div class="ufc-productos-options">
                        <div
                          v-for="producto in filteredProductos"
                          :key="producto.id"
                          class="ufc-producto-option"
                          :class="{
                            selected: formData.productos.includes(producto.id),
                          }"
                          @click.stop="toggleProductoSelection(producto.id)"
                        >
                          {{ producto.id }}-{{ producto.producto_name }} -
                          {{ producto.producto_codigo }}
                          <template v-if="producto.tipo_embalaje">
                            (Embalaje:
                            {{
                              producto.tipo_embalaje_name ||
                              producto.tipo_embalaje.nombre_embalaje ||
                              "N/A"
                            }})
                          </template>
                        </div>
                      </div>
                    </div>
                  </div>
                  <button
                    class="ufc-add-button"
                    @click.prevent="abrirModalAgregarProducto"
                    :disabled="isSubmitting"
                  >
                    <i class="bi bi-plus-lg"></i>
                  </button>
                </div>
              </div>

              <ModalAgregarProducto v-if="mostrarModal" :visible="mostrarModal" @cerrar-modal="cerrarModal"/>

              <!-- Campo: situados -->

              <!-- Campo: pendiente_proximo_dia -->
              <div class="ufc-input-group">
                <label for="pendiente_proximo_dia">
                  Pendientes al próximo día <span class="required">*</span>
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
              <div class="ufc-input-group">
                <label for="observaciones">Observaciones</label>
                <textarea
                  class="form-control form-control-sm border-secondary"
                  v-model="formData.observaciones"
                  id="observaciones"
                  name="observaciones"
                  rows="3"
                ></textarea>
              </div>
            </div>
          </div>

          <div class="ufc-form-actions">
            <button
              type="submit"
              class="ufc-button primary"
              :disabled="isSubmitting"
            >
              <span v-if="isSubmitting">
                <span class="spinner" role="status" aria-hidden="true"></span>
                Procesando...
              </span>
              <span v-else>Agregar</span>
            </button>
            <button
              type="button"
              @click="confirmCancel"
              class="ufc-button secondary"
              :disabled="isSubmitting"
            >
              Cancelar
            </button>
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
        producto: "", //Estaba escrito productos , en el form se llena producto
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
      entidades: [],
      puertos: [],
      productos: [],
      loading: false,
      entidades: [],
      puertos: [],
      productos: [],
      loading: false,
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
    };
  },

  mounted() {
    this.verificarInformeOperativo(); // Esto tu vo que ser agregado, ya que se estaba buscando un ID que no existia
    this.getProductos();
    this.getEntidades();
    this.getPuertos();
    this.getEquipos();
    this.filteredProductos = this.productos;
    this.closeDropdownsOnClickOutside();
  },

  computed: {
    formattedFechaRegistro() {
      if (this.formData.fecha) {
        return new Date(this.formData.fecha).toLocaleString("es-ES");
        return new Date(this.formData.fecha).toLocaleString("es-ES");
      }
      return new Date().toLocaleString("es-ES");
      return new Date().toLocaleString("es-ES");
    },
  },

  methods: {
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

        if (this.vagonesAgregados.length == 0) {
          Swal.fire({
            title: "Error",
            text: "Debe añadir al menos un vagón",
            icon: "error",
          });
          return;
        }

        if (
          this.formData.estado === "cargado" &&
          this.formData.producto.length === 0
        ) {
          this.showErrorToast(
            "Debe seleccionar al menos un producto cuando el estado es Cargado"
          );
          return;
        }

        if (this.vagonesAgregados.length !== this.formData.situados) {
          Swal.fire({
            title: "Advertencia",
            text: `El número de vagones asociados (${this.vagonesAgregados.length}) no coincide con la cantidad de "Situados" (${this.formData.situados}). ¿Desea actualizar el campo "Situados" para que coincida?`,
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Sí, actualizar",
            cancelButtonText: "No, corregir manualmente",
          }).then((result) => {
            if (result.isConfirmed) {
              this.formData.situados = this.vagonesAgregados.length;
            }
          });
          return;
        }

        if (this.vagonesAgregados.length !== this.formData.situados) {
          Swal.fire({
            title: "Advertencia",
            text: `El número de vagones asociados (${this.vagonesAgregados.length}) no coincide con la cantidad "Situados" (${this.formData.situados}). ¿Desea actualizar el campo "Situados" para que coincida?`,
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Sí, actualizar",
            cancelButtonText: "No, corregir manualmente",
          }).then((result) => {
            if (result.isConfirmed) {
              this.formData.situados = this.vagonesAgregados.length;
            }
          });
          return;
        }
        if (this.vagonesAgregados.length !== this.formData.situados) {
          Swal.fire({
            title: "Advertencia",
            text: `El número de vagones asociados (${this.vagonesAgregados.length}) no coincide con la cantidad "Situados" (${this.formData.situados}). ¿Desea actualizar el campo "Situados" para que coincida?`,
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Sí, actualizar",
            cancelButtonText: "No, corregir manualmente",
          }).then((result) => {
            if (result.isConfirmed) {
              this.formData.situados = this.vagonesAgregados.length;
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
          producto: this.formData.producto,
          situados: this.formData.situados,
          pendiente_proximo_dia: this.formData.pendiente_proximo_dia,
          observaciones: this.formData.observaciones,
        };
        // Configuración de axios para manejar mejor los errores
        const config = {
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          validateStatus: function (status) {
            return status >= 200 && status < 500;
          },
        };

        // Enviar datos al endpoint
        const response = await axios.post(
          "http://127.0.0.1:8000/ufc/situados/",
          payload,
          config
        );

        if (response.status === 201) {
          await Swal.fire({
            title: "Éxito",
            text: "Registro creado correctamente",
            icon: "success",
          });
          this.resetForm();
          this.$router.push({ name: "InfoOperativo" });
        } else {
          let errorMessage = "Error al crear el registro";
          if (response.data) {
            // Procesar errores del backend
            if (typeof response.data === "string") {
              errorMessage = response.data;
            } else if (response.data.detail) {
              errorMessage = response.data.detail;
            } else if (response.data.non_field_errors) {
              errorMessage = response.data.non_field_errors.join(", ");
            } else {
              errorMessage = Object.entries(response.data)
                .map(
                  ([key, value]) =>
                    `${key}: ${Array.isArray(value) ? value.join(", ") : value}`
                )
                .join("\n");
            }
          }
          throw new Error(errorMessage);
        }
      } catch (error) {
        console.error("Error en submitForm:", error);
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
        productos: [], // Resetear a array vacío
        situados: 1,
        pendiente_proximo_dia: 0,
        observaciones: "",
      };
      this.vagonesAgregados = [];
      this.vagonesAgregados = [];
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
      const index = this.formData.producto.indexOf(productoId);
      if (index === -1) {
        this.formData.producto.push(productoId);
      } else {
        this.formData.producto.splice(index, 1);
      }
    },
    getSelectedProductosText() {
      if (this.formData.producto.length === 0) return "";
      if (this.formData.producto.length === 1) {
        const producto = this.productos.find(
          (p) => p.id === this.formData.producto
        );
        return producto
          ? `${producto.id}-${producto.producto_name}`
          : "1 producto seleccionado";
      }
      return `${this.formData.producto.length} productos seleccionados`;
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
.ufc-vagones-agregados {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.ufc-subtitle {
  color: #002a68;
  font-size: 1.1rem;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.ufc-table-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

.ufc-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

.ufc-table th {
  background-color: #f8f9fa;
  padding: 10px;
  text-align: left;
  border-bottom: 2px solid #ddd;
  color: #555;
}

.ufc-table td {
  padding: 10px;
  border-bottom: 1px solid #eee;
  vertical-align: middle;
}

.ufc-table tr:hover {
  background-color: #f5f5f5;
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

.ufc-validation-message {
  padding: 10px;
  border-radius: 6px;
  font-size: 0.85rem;
  margin-top: 10px;
}

.ufc-validation-message.warning {
  background-color: #fff3cd;
  color: #856404;
  border-left: 4px solid #ffeeba;
}

.ufc-validation-message.success {
  background-color: #d4edda;
  color: #155724;
  border-left: 4px solid #c3e6cb;
}

.ufc-validation-message.error {
  background-color: #f8d7da;
  color: #721c24;
  border-left: 4px solid #f5c6cb;
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
.form-select:focus {
  border-color: #dc3545;
  box-shadow: 0 0 0 0.25rem rgba(220, 53, 69, 0.25);
  outline: 0;
}
.form-control:focus {
  border-color: #dc3545;
  box-shadow: 0 0 0 0.25rem rgba(220, 53, 69, 0.25);
  outline: 0;
}
</style>
