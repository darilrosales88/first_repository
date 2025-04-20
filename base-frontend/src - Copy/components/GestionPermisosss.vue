<template>
    <div>
      <h1>Gestión de Permisos</h1>
      <table>
        <thead>
          <tr>
            <th>Usuario</th>
            <th>Permisos</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.username }}</td>
            <td>{{ user.id }}</td>
            
          
            <td>
              <button @click="showAssignPermissionsModal(user)">Asignar Permisos</button>
              <button @click="revokePermission(user)">Revocar Permisos</button>
            </td>
          </tr>
        </tbody>
      </table>
      <AssignPermissionsModal
        v-if="showModal"
        :user="selectedUser"
        :availablePermissions="availablePermissions"
        @close="closeModal"
        @assign="assignPermission"
      />
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import AssignPermissionsModal from './AssignPermissionsModal.vue';  
  
  export default {
    name: 'GestionPermisos',
    data() {
      return {
        users: [],
        availablePermissions: ['view', 'add', 'change', 'delete'], // Ejemplo de permisos
        showModal: false,
        selectedUser: null,
      };
    },
    components: {
      AssignPermissionsModal,
    },
    methods: {
      async fetchUsers() {
        try {
          const response = await axios.get('/api/users/');
          this.users = response.data;
        } catch (error) {
          console.error('Error al obtener usuarios', error);
        }
      },
      showAssignPermissionsModal(user) {
        this.selectedUser = user;
        this.showModal = true;
      },
      closeModal() {
        this.showModal = false;
        this.selectedUser = null;
      },
      async assignPermission(user, permission) {
        try {
          await axios.post(`/api/users/${user.id}/assign_permission/`, { permission });
          this.fetchUsers(); // Actualiza la lista de usuarios
        } catch (error) {
          console.error('Error al asignar permisos', error);
        }
      },
      async revokePermission(user) {
        try {
          await axios.post(`/api/users/${user.id}/revoke_permission/`);
          this.fetchUsers(); // Actualiza la lista de usuarios
        } catch (error) {
          console.error('Error al revocar permisos', error);
        }
      }
    },
    created() {
      this.fetchUsers(); // Obtén los usuarios cuando se crea el componente
    },
  };
  </script>