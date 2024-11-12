<template>
  <div>
    <div class="top-bar">
      <h2>Admin Dashboard</h2>
      <input v-model="searchQuery" placeholder="Search services..." @input="filterServices" />
      <select v-model="selectedCategory" @change="filterServices">
        <option value="">All Categories</option>
        <option v-for="category in categories" :key="category" :value="category">{{ category }}</option>
      </select>
      <button @click="navigateTo('AHome')">Home</button>
      <a v-on:click="logout" href="#">Logout</a>

      <button @click="navigateTo('ASummary')">Summary</button>
    </div>
    
    <div class="services-section">
      <button @click="addService">Add Service</button>
      <h3>Services</h3>
      <table class="services-table" v-if="filteredServices.length > 0">
        <thead>
          <tr>
            <th>Name</th>
            <th>Base Price</th>
            <th>Category</th>
            <th>Time Required</th>
            <th>Avg Rating</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in filteredServices" :key="service.id">
            <td>{{ service.name }}</td>
            <td>{{ service.base_price }}</td>
            <td>{{ service.category }}</td>
            <td>{{ service.time_required }}</td>
            <td>{{ service.avg_rating }}</td>
            <td>
              <button @click="editService(service.id)">Edit</button>
              <button @click="deleteService(service.id)">Delete</button>
            </td>
          </tr>
        </tbody> 
      </table>
      <div v-else>
        <p>No services found</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchQuery: '',
      selectedCategory: '',
      categories: ['Cleaning', 'Plumbing', 'Electrical'], // Example categories, dynamically load if needed
      services: [],
      filteredServices: []
    };
  },
  methods: {
  logout(){
      localStorage.clear()
      this.$router.push("/login")
    },
    async fetchServices() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/services');
        this.services = response.data;
        this.filterServices();
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    },
    filterServices() {
      this.filteredServices = this.services.filter((service) =>
        service.name.toLowerCase().includes(this.searchQuery.toLowerCase()) &&
        (this.selectedCategory ? service.category === this.selectedCategory : true)
      );
    },
    addService() {
      this.$router.push("/addservices");
    },
    editService(serviceId) {
      this.$router.push({ name: 'editservices', params: { id: serviceId } });
    },
    async deleteService(serviceId) {
      try {
        await axios.delete(`http://127.0.0.1:5000/services/${serviceId}`);
        this.fetchServices();
        alert('Service deleted successfully');
      } catch (error) {
        console.error('Error deleting service:', error);
      }
    },
    navigateTo(page) {
      this.$router.push({ name: page });
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push({ name: 'login' });
    }
  },
  mounted() {
    this.fetchServices();
  }
};
</script>
