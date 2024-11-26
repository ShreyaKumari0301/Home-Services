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
      <button @click="navigateTo('AProfs')">Professional</button>
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
              <router-link :to = "'/editservices/'+ service.id">
                <button>Edit</button>
              </router-link>
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
      categories: ['Cleaning', 'Plumbing', 'Electrical'],
      services: [],
      filteredServices: []
    };
  },
  methods: {
    async fetchServices() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/adminservice', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.services = response.data;
        this.filterServices();
      } catch (error) {
        console.error('Error fetching services:', error);
        if (error.response?.status === 401) {
          this.$router.push('/login');
        }
      }
    },
    filterServices() {
      if (!this.services) return [];
      this.filteredServices = this.services.filter((service) =>
        service.name.toLowerCase().includes(this.searchQuery.toLowerCase()) &&
        (this.selectedCategory ? service.category === this.selectedCategory : true)
      );
    },
    addService() {
      this.$router.push("/addservices");
    },
    async deleteService(serviceId) {
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`http://127.0.0.1:5000/adminservice/${serviceId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        await this.fetchServices();
        alert('Service deleted successfully');
      } catch (error) {
        console.error('Error deleting service:', error);
        alert('Error deleting service');
      }
    },
    navigateTo(page) {
      this.$router.push({ name: page });
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    }
  },
  mounted() {
    this.fetchServices();
  }
};
</script>

<style scoped>
.top-bar {
  padding: 20px;
  background-color: #f8f9fa;
  display: flex;
  gap: 15px;
  align-items: center;
}

.services-section {
  padding: 20px;
}

.services-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.services-table th,
.services-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #007bff;
  color: white;
}

button:hover {
  background-color: #0056b3;
}

input, select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

a {
  text-decoration: none;
  color: #dc3545;
  cursor: pointer;
}

a:hover {
  text-decoration: underline;
}
</style>
