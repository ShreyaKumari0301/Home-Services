<template>
  <div class="profile">
    <h2>Profile</h2>
    <form @submit.prevent="updateProfile">
      <label>Name: <input v-model="user.name" /></label>
      <label>Email: <input v-model="user.email" disabled /></label>
      <label>Mobile Number: <input v-model="user.mobile_number" /></label>
      <label>Address: <input v-model="user.address" /></label>
      <button type="submit">Save</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: {
        name: '',
        email: '',
        mobile_number: '',
        address: ''
      }
    };
  },
  async created() {
    const response = await fetch('/profile', {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    });
    if (response.ok) {
      this.user = await response.json();
    }
  },
  methods: {
    async updateProfile() {
      const response = await fetch('/profile', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(this.user)
      });
      if (response.ok) {
        alert("Profile updated successfully");
      }
    }
  }
};
</script>

<style scoped>
.profile {
  max-width: 500px;
  margin: auto;
}
</style>
