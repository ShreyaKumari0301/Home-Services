<template>
  <div class="main-container">
    <div class="navigation-bar">
      <div class="nav-header">
        <h2><i>Welcome Aboard!</i></h2>
        <div class="nav-buttons">
          <button 
            @click="navigateTo('UHome')"
            :class="{ active: currentRoute === 'UHome' }"
          >Home</button>
          <button 
            @click="navigateTo('UOrders')"
            :class="{ active: currentRoute === 'UOrders' }"
          >Orders</button>
          <button 
            @click="navigateTo('UProfile')"
            :class="{ active: currentRoute === 'UProfile' }"
          >Profile</button>
          <button 
            @click="navigateTo('USummary')"
            :class="{ active: currentRoute === 'USummary' }"
          >Summary</button>
          <button @click="logout" class="logout-btn">Logout</button>
        </div>
      </div>
      
      <!-- Search Section -->
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
    </div>
    
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
                <p><i class="price-icon">💰</i> ₹ {{ service.base_price }}</p>
              </div>
              <button @click="goToCart(service.id)" class="book-button">
                Book Now
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UNavbar from './UNavbar.vue'
import axios from "axios";

export default {
  components: {
    UNavbar
  },
  data() {
    return {
      searchQuery: "",
      selectedCategory: "",
      categories: ['Cleaning', 'Plumbing'],
      services: [],
      filteredServices: []
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
    async fetchServices() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/services");
        this.services = response.data;
        this.filterServices();
      } catch (error) {
        console.error("Error fetching services:", error);
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
      }
    },
    navigateTo(page) {
      this.$router.push({ name: page });
    },
    logout() {
      localStorage.clear();
      this.$router.push("/login");
    },
    handleSearch(query) {
      this.searchQuery = query;
      this.filterServices();
    },
    handleCategoryChange(category) {
      this.selectedCategory = category;
      this.filterServices();
    }
  },
  mounted() {
    const token = localStorage.getItem("token");
    if (!token) {
      this.$router.push("/login");
      return;
    }
    this.fetchServices();
  }
};
</script>

<style scoped>
.main-container {
  background-color: #f5f5f5;
  padding: 30px;
  min-height: 100vh;
}

.navigation-bar {
  background: white;
  padding: 1rem 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-buttons {
  display: flex;
  gap: 15px;
}

.nav-buttons button {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: #f8f9fa;
  color: #495057;
  cursor: pointer;
  transition: all 0.3s ease;
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

.search-filters {
  display: flex;
  gap: 20px;
  margin-top: 15px;
}

.search-input, .category-select {
  padding: 10px 15px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-input:focus, .category-select:focus {
  outline: none;
  border-color: #0d6efd;
  box-shadow: 0 0 0 3px rgba(13,110,253,0.25);
}

.category-section {
  margin-bottom: 40px;
}

.category-title {
  font-size: 1.5rem;
  color: #212529;
  margin-bottom: 20px;
  padding-bottom: 8px;
  border-bottom: 2px solid #dee2e6;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 18px;
}

.service-card {
  background: white;
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.service-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.service-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.service-header h4 {
  margin: 0;
  color: #212529;
}

.rating {
  color: #ffc107;
}

.description {
  color: #6c757d;
  margin-bottom: 15px;
  line-height: 1.5;
}

.service-details {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  color: #495057;
}

.book-button {
  width: 100%;
  padding: 10px;
  background: #0d6efd;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.book-button:hover {
  background: #0b5ed7;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .services-grid {
    grid-template-columns: 1fr;
  }
}
</style>