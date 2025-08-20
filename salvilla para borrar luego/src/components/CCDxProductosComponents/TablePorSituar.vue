<template>
    <MainTableComponent 
    :content_headers = "headers"
    :content_list = "porSituarList"  />
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";
import MainTableComponent from "@/components/CCDxProductosComponents/MainTableComponent.vue";

export default {
  name: "TablePorSituar",
  components: {
    MainTableComponent,
  },
  data() {
    return {
        headers: ['Tipo Origen','Origen','Tipo Equipo','Estado','Producto','Por Situar','Acciones'],
        porSituarList: [{tipo_origen_name:'Puerto',origen: 'Puerto Uno', tipo_equipo_name:'Plancha',estado: 'vacio',producto:'',por_situar:''},
                        {tipo_origen_name:'Puerto',origen: 'Puerto Dos', tipo_equipo_name:'Plancha',estado: 'cargado',producto:'chicharo',por_situar:''},],
    };
  },

  async mounted() {},

  beforeUnmount() {},

  methods: {},
};
</script>
<style>

</style>