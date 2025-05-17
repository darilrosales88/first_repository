<template>
    <Visualizar-Informe-Operativo />
</template>
<script>
import NavbarComponent from '@/components/NavbarComponent.vue';
import VisualizarInformeOperativo from '@/components/VisualizarInformeOperativo.vue';

    export default{
        name: 'InformeOperativoVisual',
        components:{
            VisualizarInformeOperativo,
            NavbarComponent
        }
    }
</script>