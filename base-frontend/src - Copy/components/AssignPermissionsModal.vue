<!-- Este componente mostrará un modal para asignar permisos a un usuario. -->
<template>
    <div class="modal">
      <h2>Asignar Permisos a {{ user.username }}</h2>
      <ul>
        <li v-for="permission in availablePermissions" :key="permission">
          <label>
            <input type="checkbox" :value="permission" v-model="selectedPermissions" />
            {{ permission }}
          </label>
        </li>
      </ul>
      <button @click="assignPermissions">Asignar</button>
      <button @click="$emit('close')">Cerrar</button>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      user: Object,
      availablePermissions: Array,
    },
    data() {
      return {
        selectedPermissions: [],
      };
    },
    methods: {
      assignPermissions() {
        this.selectedPermissions.forEach(permission => {
          this.$emit('assign', this.user, permission);
        });
        this.$emit('close');
      },
    },
  };
  </script>
  
  <style scoped>
  .modal {
    /* Estilos para el modal */
  }
  </style>