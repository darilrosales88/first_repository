<template>
    <MainTableComponent :contentHeaders = "headers"  />
</template>

<script>
import Swal from "sweetalert2";
import axios from "axios";
import MainTableComponent from "@/components/CCDxProductosComponents/MainTableComponent.vue";

export default {
  name: "TableSituados",
  components: {
    MainTableComponent,
  },
  data() {
    return {
        headers: ['Tipo Origen','Origen','Tipo Equipo','Estado','Operación','Porducto','Situados','Pendientes','Acciones'],
    };
  },

  async mounted() {},

  beforeUnmount() {},

  methods: {},
};
</script>
<style>

</style>