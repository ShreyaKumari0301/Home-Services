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
            <td>
              <button @click="goToCart(service.id)">Add to Cart</button>
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
import axios from "axios";

export default {
  data() {
    return {
      searchQuery: "",
      selectedCategory: "",
      categories: [], // Will be dynamically loaded from the backend
      services: [],
      filteredServices: [],
    };
  },
  methods: {
    async fetchServices() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/services");
        this.services = response.data;
        this.filterServices();
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    async fetchCategories() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/categories");
        this.categories = response.data;
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
    },
    filterServices() {
      this.filteredServices = this.services.filter((service) =>
        service.name.toLowerCase().includes(this.searchQuery.toLowerCase()) &&
        (this.selectedCategory ? service.category === this.selectedCategory : true)
      );
    },
    goToCart(serviceId) {
      if (serviceId) {
        this.$router.push({ 
          name: 'UCart', 
          params: { serviceId: serviceId.toString() } 
    });
    }},
    navigateTo(page) {
      this.$router.push({ name: page });
    },
    logout() {
      localStorage.clear();
      alert("Logged out successfully.");
      this.$router.push("/login");
    },
  },
  mounted() {
    const token = localStorage.getItem("token");
    const userrole = localStorage.getItem("userrole");

    if (token) {
      if (userrole === "User") {
        this.fetchServices();
        this.fetchCategories();
      } else if (userrole === "Admin") {
        this.$router.push("/admin");
      } else {
        this.$router.push("/professional");
      }
    } else {
      this.$router.push("/login");
    }
  },
};
</script>
