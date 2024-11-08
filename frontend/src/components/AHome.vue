<template>
  <div class="home-container">
    <!-- Top Bar with Welcome Message, Search Box, Category Filter, and Buttons -->
    <div class="top-bar">
      <div class="welcome-message">
        <h2>Welcome Admin</h2>
      </div>
      <div class="search-container">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search..."
          class="search-box"
        />
      </div>
      <div class="category-filter">
        <select v-model="selectedCategory" @change="filterServices" class="category-dropdown">
          <option value="">Filter by Category</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>
      </div>
      <div class="buttons-container">
        <button @click="navigateTo('home')">Home</button>
        <button @click="navigateTo('professional')">Professional</button>
        <button @click="navigateTo('summary')">Summary</button>
        <button @click="logout">Logout</button>
      </div>
    </div>

    <!-- Services Table -->
    <div class="services-section">
      <h3>Services</h3>
      <table class="services-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Base Price</th>
            <th>Category</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in filteredServices" :key="service.id">
            <td>{{ service.name }}</td>
            <td>{{ service.base_price }}</td>
            <td>{{ service.category }}</td>
            <td>
              <button @click="editService(service.id)">Edit</button>
              <button @click="deleteService(service.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add Category and Add Service Options -->
    <div class="add-options">
      <button class="add-button" @click="addCategory">Add Category</button>
      <button class="add-button" @click="addService">Add Service</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      selectedCategory: '',
      categories: [],
      services: [], // Array to hold services fetched from backend
      filteredServices: [], // Filtered services based on search and category
    };
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await this.$axios.get('http://127.0.0.1:5000/categories');
        this.categories = response.data;
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
    async fetchServices() {
      try {
        const response = await this.$axios.get('http://127.0.0.1:5000/services');
        this.services = response.data;
        this.filteredServices = this.services; // Initially display all services
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    },
    filterServices() {
      this.filteredServices = this.services.filter((service) => {
        return (
          service.name.toLowerCase().includes(this.searchQuery.toLowerCase()) &&
          (this.selectedCategory ? service.category === this.selectedCategory : true)
        );
      });
    },
    navigateTo(page) {
      this.$router.push({ name: page });
    },
    logout() {
      // Add your logout functionality here
      this.$router.push({ name: 'login' });
    },
    addCategory() {
      // Navigate to add category page
      this.$router.push({ name: 'add-category' });
    },
    addService() {
      // Navigate to add service page
      this.$router.push({ name: 'add-service' });
    },
    editService(serviceId) {
      // Navigate to edit service page
      this.$router.push({ name: 'edit-service', params: { id: serviceId } });
    },
    deleteService(serviceId) {
      // Implement delete functionality
      this.$axios.delete(`http://127.0.0.1:5000/services/${serviceId}`)
        .then(() => {
          this.fetchServices(); // Refresh services list
          this.$toast.success('Service deleted successfully');
        })
        .catch((error) => {
          console.error('Error deleting service:', error);
          this.$toast.error('Failed to delete service');
        });
    },
  },
  mounted() {
    this.fetchCategories();
    this.fetchServices();
  },
};
</script>

<style scoped>
.home-container {
  padding: 20px;
  font-family: Arial, sans-serif;
}

/* Top Bar Styles */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.welcome-message h2 {
  margin: 0;
  font-size: 24px;
}

.search-container {
  flex: 1;
  margin-right: 20px;
}

.search-box {
  width: 100%;
  padding: 8px;
  font-size: 14px;
}

.category-filter {
  margin-right: 20px;
}

.category-dropdown {
  padding: 8px;
  font-size: 14px;
}

.buttons-container {
  display: flex;
  gap: 10px;
}

.buttons-container button {
  padding: 10px 15px;
  font-size: 14px;
  cursor: pointer;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
}

.buttons-container button:hover {
  background-color: #0056b3;
}

/* Services Section Styles */
.services-section {
  margin-top: 20px;
}

.services-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.services-table th,
.services-table td {
  padding: 10px;
  text-align: left;
  border: 1px solid #ddd;
}

.services-table th {
  background-color: #f4f4f4;
}

.services-table td button {
  margin-right: 5px;
  padding: 5px 10px;
  font-size: 14px;
  cursor: pointer;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
}

.services-table td button:hover {
  background-color: #218838;
}

.add-options {
  margin-top: 20px;
}

.add-button {
  padding: 10px 20px;
  font-size: 14px;
  cursor: pointer;
  background-color: #17a2b8;
  color: white;
  border: none;
  border-radius: 5px;
  margin-right: 10px;
}

.add-button:hover {
  background-color: #138496;
}
</style>
