<template>
  <div class="main-container">
    <!-- Navigation Bar -->
    <div class="navigation-bar">
      <div class="nav-header">
        <h2><i>Admin Dashboard</i></h2>
        <div class="nav-buttons">
          <button 
            @click="navigateTo('AHome')"
            :class="{ active: currentRoute === 'AHome' }"
          >Home</button>
          <button 
            @click="navigateTo('AProfs')"
            :class="{ active: currentRoute === 'AProfs' }"
          >Professionals</button>
          <button 
            @click="navigateTo('AUsers')"
            :class="{ active: currentRoute === 'AUsers' }"
          >Users</button>
          <button 
            @click="navigateTo('ARequests')"
            :class="{ active: currentRoute === 'ARequests' }"
          >Service Requests</button>
          <button 
            @click="navigateTo('ASummary')"
            :class="{ active: currentRoute === 'ASummary' }"
          >Summary</button>
          <button @click="logout" class="logout-btn">Logout</button>
        </div>
      </div>
    </div>

    <!-- Search Section -->
    <div class="search-section">
      <div class="search-filters">
        <input 
          v-model="searchQuery" 
          placeholder="Search services..." 
          @input="filterServices"
          class="search-input" 
        />
        <select 
          v-model="selectedCategory" 
          @change="filterServices"
          class="category-select"
        >
          <option value="">All Categories</option>
          <option v-for="category in categories" :key="category" :value="category">
            {{ category }}
          </option>
        </select>
      </div>
      
      <div class="add-service-section">
        <button 
          @click="navigateTo('AddServices')" 
          class="add-service-btn"
        >
          + Add New Service
        </button>
      </div>
    </div>

    <!-- Content Area -->
    <div class="content-area">
      <div class="services-container">
        <div v-for="category in groupedServices" :key="category.name" class="category-section">
          <h3 class="category-title">{{ category.name }}</h3>
          <div class="services-grid">
            <div v-for="service in category.services" :key="service.id" class="service-card">
              <div class="service-header">
                <h4>{{ service.name }}</h4>
                <span class="rating">{{ service.avg_rating }} ⭐</span>
              </div>
              <p class="description">{{ service.description }}</p>
              <div class="service-details">
                <p><i class="time-icon">⏰</i> {{ service.time_required }} mins</p>
                <p><i class="price-icon">💰</i> ₹{{ service.base_price }}</p>
              </div>
              <div class="action-buttons">
                <button 
                  @click="editService(service.id)" 
                  class="edit-btn"
                >
                  Edit
                </button>
                <button 
                  @click="deleteService(service.id)" 
                  class="delete-btn"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
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
      categories: ['Cleaning', 'Plumbing', 'Electrical', 'Painting'],
      services: [],
      filteredServices: [],
      currentRoute: 'AHome'
    };
  },
  computed: {
    groupedServices() {
      const grouped = {};
      this.filteredServices.forEach(service => {
        if (!grouped[service.category]) {
          grouped[service.category] = {
            name: service.category,
            services: []
          };
        }
        grouped[service.category].services.push(service);
      });
      return Object.values(grouped);
    }
  },
  methods: {
    navigateTo(page) {
      this.$router.push({ name: page });
    },
    logout() {
      localStorage.clear();
      this.$router.push("/login");
    },
    async fetchServices() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get("http://127.0.0.1:5000/adminservice", {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.services = response.data;
        this.filterServices();
      } catch (error) {
        console.error("Error fetching services:", error);
        if (error.response?.status === 401) {
          this.$router.push('/login');
        }
      }
    },
    filterServices() {
      this.filteredServices = this.services.filter((service) =>
        service.name.toLowerCase().includes(this.searchQuery.toLowerCase()) &&
        (this.selectedCategory ? service.category === this.selectedCategory : true)
      );
    },
    editService(serviceId) {
      this.$router.push({ name: 'EditServices', params: { id: serviceId } });
    },
    async deleteService(serviceId) {
      if (confirm('Are you sure you want to delete this service?')) {
        try {
          const token = localStorage.getItem('token');
          await axios.delete(`http://127.0.0.1:5000/adminservice/${serviceId}`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          await this.fetchServices();
          alert('Service deleted successfully');
        } catch (error) {
          console.error('Error deleting service:', error);
          alert('Failed to delete service');
        }
      }
    }
  },
  mounted() {
    this.fetchServices();
  }
};
</script>

<style scoped>
.main-container {
  background-color: #2d3748;
  color: white;
  min-height: 100vh;
  padding: 0;
}

.navigation-bar {
  background: #2d3748;
  padding: 1rem 2rem;
  border-radius: 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 0;
  margin-left: 5px;
  margin-right:2px;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-buttons {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.nav-buttons button {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: #444;
  color: #f8f9fa;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.nav-buttons button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-buttons button.active {
  background: #0d6efd;
  color: white;
}

.logout-btn {
  background: #dc3545 !important;
  color: white !important;
}

.search-section {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
}

.search-filters {
  display: flex;
  gap: 20px;
  margin-top: 110px;
  margin-bottom: 15px;
  width: 100%;
}

.search-input, .category-select {
  padding: 12px 20px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
  color: #333;
}

.search-input {
  flex: 2;
  min-width: 0;
}

.category-select {
  flex: 1;
  min-width: 200px;
}

.search-input:focus, .category-select:focus {
  outline: none;
  border-color: #0d6efd;
  box-shadow: 0 0 0 3px rgba(13,110,253,0.25);
}

.add-service-section {
  width: 100%;
  text-align: right;
  padding: 10px 0;
  border-bottom: 1px solid #444;
  margin-bottom: 20px;
}

.add-service-btn {
  padding: 12px 24px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.add-service-btn:hover {
  background-color: #218838;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.content-area {
  padding: 20px;
}

.services-container {
  max-width: 1200px;
  margin: 0 auto;
}

.category-title {
  margin: 20px 0;
  color: #f8f9fa;
  font-size: 1.5rem;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 25px;
  margin-bottom: 30px;
}

.service-card {
  background: #444;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.service-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.service-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.service-header h4 {
  margin: 0;
  color: #f8f9fa;
  font-size: 1.2rem;
}

.rating {
  color: #ffd700;
}

.description {
  color: #dee2e6;
  margin: 10px 0;
  line-height: 1.4;
}

.service-details {
  display: flex;
  gap: 20px;
  margin: 15px 0;
  color: #adb5bd;
}

.service-details p {
  display: flex;
  align-items: center;
  gap: 5px;
  margin: 0;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.action-buttons button {
  flex: 1;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.edit-btn {
  background-color: #ffc107;
  color: #000;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
}

.edit-btn:hover, .delete-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

@media (max-width: 768px) {
  .search-filters {
    flex-direction: column;
    gap: 10px;
  }

  .search-input, .category-select {
    width: 100%;
  }

  .category-select {
    min-width: 100%;
  }

  .services-grid {
    grid-template-columns: 1fr;
  }

  .nav-buttons {
    justify-content: center;
  }
}
</style>