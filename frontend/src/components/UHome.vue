<template>
  <div>
    <div class="top-bar">
      <h2>User Dashboard</h2>
      <input v-model="searchQuery" placeholder="Search services..." @input="filterServices" />
      <select v-model="selectedCategory" @change="filterServices">
        <option value="">All Categories</option>
        <option v-for="category in categories" :key="category" :value="category">{{ category }}</option>
      </select>
      <button @click="navigateTo('UHome')">Home</button>
      <button @click="navigateTo('UCart')">Cart</button>
      <button @click="navigateTo('UOrders')">Orders</button>
      <button @click="navigateTo('UProfile')">Profile</button>
      <button @click="navigateTo('USummary')">Summary</button>
      <button @click="logout">Logout</button>

    </div>
    
    <div class="services-section">
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
 <div v-if="service.quantity > 0">
        <button @click="decrementQuantity(service)">-</button>
        <span>{{ service.quantity }}</span>
        <button @click="incrementQuantity(service)">+</button>
      </div>

      <button v-else @click="addToCart(service)">Add</button>
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
    addToCart(service) {
      service.quantity = 1;
    },
    incrementQuantity(service) {
      service.quantity += 1;
    },
    decrementQuantity(service) {
      if (service.quantity > 1) {
        service.quantity -= 1;
      } else {
        service.quantity = 0;
      }
    },
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
