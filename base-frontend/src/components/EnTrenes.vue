<template>
  <div style="padding: 20px">
    <button @click="toggleContentVisibility" class="btn btn-primary">
      <h2>En Trenes</h2>
    </button>

    <div v-if="showContent">
      <div class="d-flex" style="padding: 1%">
        <div class="create-button-container">
          <router-link
            v-if="hasPermission"
            class="create-button"
            to="AdicionarVagon"
          >
            <i class="bi bi-plus-circle large-icon"></i>
          </router-link>
        </div>

        <div class="search-container" style="padding-left: 10%">
          <form class="d-flex search-form" @submit.prevent="search_producto">
            <input
              class="form-control form-control-sm me-2"
              type="search"
              placeholder="Origen, Destino, Producto, Locomotora"
              aria-label="Search"
              v-model="searchQuery"
              @input="handleSearchInput"
              style="width: 200px"
            />
          </form>
        </div>
      </div>
      <div class="table-container" style="padding-left: 15%">
        <table class="table">
          <thead>
            <tr>
              <th scope="col" v-if="showNoId">No</th>
              <th scope="col">No</th>
              <th scope="col">Código_locomotora</th>
              <th scope="col">Tipo</th>
              <th scope="col">Estado</th>
              <th scope="col">Producto</th>
              <th scope="col">Cantidad de vagones</th>
              <th scope="col">Origen</th>
              <th scope="col">Destino</th>
              <th scope="col" v-if="showNoId">Descripción</th>
              <th scope="col" v-if="hasPermission">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(tren, index) in en_trenes" :key="tren.id">
              <th scope="row" style="background-color: white">
                {{ index + 1 }}
              </th>
              <td>{{ tren.numero_identificacion_locomotora }}</td>
              <td>{{ tren.tipo_equipo }}</td>
              <!-- nacionalidad_name esta declarado en el serializador -->
              <td>{{ tren.estado }}</td>
              <td>{{ tren.producto_name }}</td>
              <td>{{ tren.cantidad_vagones }}</td>
              <td>{{ tren.origen }}</td>
              <td>{{ tren.destino }}</td>

              <td>
                <!--   <button
                  @click="openCargoDetailsModal(item)"
                  class="btn btn-info btn-small btn-eye"
                  v-html="
                    showNoId
                      ? '<i class=\'bi bi-eye-slash-fill\'></i>'
                      : '<i class=\'bi bi-eye-fill\'></i>'
                  "
                ></button>

                <button class="btn btn-warning btn-small">
                  <router-link
                    :to="{ name: 'EditarEnTren', params: { id: item.id } }"
                  >
                    <i style="color: black" class="bi bi-pencil-square"></i>
                  </router-link>
                </button>
                <button class="btn btn-danger btn-small">
                  <i class="bi bi-trash"></i>
                </button> -->
                <button
                  @click="toggleNoIdVisibility"
                  class="btn btn-info btn-small btn-eye"
                  v-html="
                    showNoId
                      ? '<i class=\'bi bi-eye-slash-fill\'></i>'
                      : '<i class=\'bi bi-eye-fill\'></i>'
                  "
                ></button>
                <span v-if="hasPermission">
                  <button
                    class="btn btn-danger btn-small btn-eye"
                    style="margin-left: 3%"
                  >
                    <router-link
                      :to="{ name: 'EditarEnTren', params: { id: tren.id } }"
                    >
                      <i style="color: black" class="bi bi-pencil-square"></i>
                    </router-link>
                  </button>
                  <button
                    style="margin-left: 5px"
                    @click.prevent="confirmDelete(tren.id)"
                    class="btn btn-danger btn-small"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination-container" style="padding-left: 15%">
        <button
          @click="previousPage"
          :disabled="currentPage === 1"
          class="btn btn-primary"
        >
          Anterior
        </button>
        <span style="margin: 0 10px">
          Página {{ currentPage }} de {{ Math.ceil(totalItems / itemsPerPage) }}
        </span>
        <button
          @click="nextPage"
          :disabled="currentPage * itemsPerPage >= totalItems"
          class="btn btn-primary"
        >
          Siguiente
        </button>
      </div>
    </div>
    <!-- Aqui se acabo el contenido escondido -->
  </div>
</template>