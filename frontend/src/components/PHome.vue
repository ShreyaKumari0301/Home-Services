<template>
  <div class="main-container">
    <!-- Blocked Professional Message -->
    <div v-if="isBlocked" class="blocked-message">
      <h3>Account Blocked</h3>
      <p>{{ blockMessage }}</p>
      
      <!-- Show confirmed services for blocked professionals -->
      <div v-if="confirmedRequests.length > 0" class="confirmed-services">
        <h4>Your Confirmed Services</h4>
        <div class="services-grid">
          <div v-for="request in confirmedRequests" :key="request.id" class="service-card">
            <div class="service-header">
              <h4>{{ request.service_name }}</h4>
              <span :class="'status-badge ' + request.status">{{ request.status }}</span>
            </div>
            <div class="customer-details">
              <p><i class="user-icon">👤</i> {{ request.customer_name }}</p>
              <p><i class="phone-icon">📱</i> {{ request.customer_phone }}</p>
            </div>
            <div class="service-details">
              <p><i class="calendar-icon">📅</i> {{ request.booking_date }}</p>
              <p><i class="time-icon">⏰</i> {{ request.time_slot }}</p>
              <p><i class="price-icon">💰</i> ₹{{ request.total_price }}</p>
            </div>
            <div class="action-buttons">
              <button 
                v-if="request.status === 'pending'"
                @click="acceptRequest(request.id)"
                class="accept-btn"
              >
                Accept
              </button>
              <button 
                v-if="request.status === 'confirmed'"
                @click="completeRequest(request.id)"
                class="complete-btn"
              >
                Complete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Normal Dashboard for Active Professionals -->
    <div v-else>
      <div class="navigation-bar">
        <div class="nav-header">
          <h2><i>Professional Dashboard</i></h2>
          <div class="nav-buttons">
            <button 
              @click="navigateTo('PHome')"
              :class="{ active: currentRoute === 'PHome' }"
            >Home</button>
            <button 
              @click="navigateTo('PRequests')"
              :class="{ active: currentRoute === 'PRequests' }"
            >History</button>
            <button 
              @click="navigateTo('PProfile')"
              :class="{ active: currentRoute === 'PProfile' }"
            >Profile</button>
            <button 
              @click="navigateTo('PSummary')"
              :class="{ active: currentRoute === 'PSummary' }"
            >Summary</button>
            <button @click="logout" class="logout-btn">Logout</button>
          </div>
        </div>
        
        <!-- Search Section -->
        <div class="search-filters">
          <input 
            v-model="searchQuery" 
            placeholder="Search service requests..." 
            @input="filterRequests"
            class="search-input" 
          />
          <select 
            v-model="statusFilter"
            class="status-select"
            @change="filterRequests"
          >
            <option value="">All Status</option>
            <option value="pending">Pending</option>
            <option value="confirmed">Confirmed</option>
            <option value="completed">Completed</option>
          </select>
        </div>
      </div>
      
      <div class="content-area">
        <div class="services-container">
          <div v-for="status in groupedRequests" :key="status.name" class="category-section">
            <h3 class="category-title">{{ status.name }}</h3>
            <div class="services-grid">
              <div v-for="request in status.requests" :key="request.id" class="service-card">
                <div class="service-header">
                  <h4>{{ request.service_name }}</h4>
                  <span :class="'status-badge ' + request.status">{{ request.status }}</span>
                </div>
                <div class="customer-details">
                  <p><i class="user-icon">👤</i> {{ request.customer_name }}</p>
                  <p><i class="phone-icon">📱</i> {{ request.customer_phone }}</p>
                </div>
                <div class="service-details">
                  <p><i class="calendar-icon">📅</i> {{ request.booking_date }}</p>
                  <p><i class="time-icon">⏰</i> {{ request.time_slot }}</p>
                  <p><i class="price-icon">💰</i> ₹{{ request.total_price }}</p>
                </div>
                <div class="action-buttons">
                  <button 
                    v-if="request.status === 'pending'"
                    @click="acceptRequest(request.id)"
                    class="accept-btn"
                  >
                    Accept
                  </button>
                  <button 
                    v-if="request.status === 'confirmed'"
                    @click="completeRequest(request.id)"
                    class="complete-btn"
                  >
                    Complete
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PHome',
  data() {
    return {
      searchQuery: "",
      statusFilter: "",
      requests: [],
      filteredRequests: [],
      currentRoute: 'PHome',
      isBlocked: false,
      blockMessage: '',
      confirmedRequests: []
    };
  },
  computed: {
    groupedRequests() {
      const statusNames = {
        'requested': 'New Requests',
        'pending': 'Pending Requests',
        'confirmed': 'Ongoing Services',
        'completed': 'Completed Services'
      };
      
      const grouped = {};
      this.filteredRequests.forEach(request => {
        if (!grouped[request.status]) {
          grouped[request.status] = {
            name: statusNames[request.status] || request.status,
            requests: []
          };
        }
        grouped[request.status].requests.push(request);
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
    async fetchRequests() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/professional/requests', {
          headers: { Authorization: `Bearer ${token}` }
        });

        // Handle blocked professional response
        if (response.status === 403 && response.data.status === 'blocked') {
          this.isBlocked = true;
          this.blockMessage = response.data.message;
          this.confirmedRequests = response.data.confirmed_requests;
          return;
        }

        this.requests = response.data;
        this.filterRequests();
      } catch (error) {
        console.error('Error fetching requests:', error);
        if (error.response?.status === 401) {
          this.$router.push('/login');
        } else if (error.response?.status === 403) {
          this.isBlocked = true;
          this.blockMessage = error.response.data.message;
        }
      }
    },
    filterRequests() {
      this.filteredRequests = this.requests.filter(request => {
        const matchesStatus = !this.statusFilter || request.status === this.statusFilter;
        const searchLower = this.searchQuery.toLowerCase();
        const matchesSearch = !this.searchQuery || 
          request.service_name.toLowerCase().includes(searchLower) ||
          request.customer_name.toLowerCase().includes(searchLower);
        
        return (request.status === 'pending' || request.status === 'confirmed' || 
                request.status === 'completed' || request.status === 'requested') 
                && matchesStatus && matchesSearch;
      });
    },
    async acceptRequest(requestId) {
      try {
        const token = localStorage.getItem('token');
        await axios.put(`http://127.0.0.1:5000/professional/requests/${requestId}/accept`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
        await this.fetchRequests();
      } catch (error) {
        console.error('Error accepting request:', error);
        alert('Failed to accept request');
      }
    },
    async completeRequest(requestId) {
      try {
        const token = localStorage.getItem('token');
        await axios.put(`http://127.0.0.1:5000/professional/requests/${requestId}/complete`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
        await this.fetchRequests();
      } catch (error) {
        console.error('Error completing request:', error);
        alert('Failed to complete request');
      }
    },
    async cancelRequest(requestId) {
      try {
        const token = localStorage.getItem('token');
        await axios.put(`http://127.0.0.1:5000/professional/requests/${requestId}/cancel`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
        await this.fetchRequests();
      } catch (error) {
        console.error('Error cancelling request:', error);
        alert('Failed to cancel request');
      }
    }
  },
  mounted() {
    const token = localStorage.getItem("token");
    if (!token) {
      this.$router.push("/login");
      return;
    }
    this.fetchRequests();
  }
};
</script>

<style scoped>
.main-container {
  background-color: #1a365d;
  min-height: 100vh;
  padding: 20px;
  color: white;
}

.navigation-bar {
  background: #2d4a7c;
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
  background: #3d5a8c;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-buttons button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-buttons button.active {
  background: #6b46c1;
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

.search-input, .status-select {
  padding: 12px 16px;
  border: 1px solid #4a5568;
  border-radius: 8px;
  background: #1a365d;
  color: white;
  font-size: 1rem;
  flex: 1;
}

.search-input::placeholder {
  color: #a0aec0;
}

.category-section {
  margin-bottom: 40px;
}

.category-title {
  font-size: 1.5rem;
  color: #e2e8f0;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #4a5568;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.service-card {
  background: #2d4a7c;
  border-radius: 12px;
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
  color: white;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
}

.status-badge.pending {
  background: #ffd700;
  color: black;
}

.status-badge.confirmed {
  background: #48bb78;
  color: white;
}

.status-badge.completed {
  background: #4299e1;
  color: white;
}

.customer-details, .service-details {
  margin: 15px 0;
}

.customer-details p, .service-details p {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 8px 0;
  color: #e2e8f0;
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
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
}

.accept-btn {
  background: #48bb78;
}

.complete-btn {
  background: #4299e1;
}

.action-buttons button:hover {
  transform: translateY(-2px);
  opacity: 0.9;
}

@media (max-width: 768px) {
  .main-container {
    padding: 15px;
  }
  
  .nav-buttons {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .search-filters {
    flex-direction: column;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
  }
}

.blocked-message {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid #dc3545;
  border-radius: 12px;
  padding: 20px;
  margin: 20px 0;
  text-align: center;
}

.blocked-message h3 {
  color: #dc3545;
  margin-bottom: 10px;
}

.confirmed-services {
  margin-top: 30px;
}

.confirmed-services h4 {
  color: #e2e8f0;
  margin-bottom: 20px;
}
</style>
  color: white;
}

.customer-details, .service-details {
  margin: 15px 0;
}

.customer-details p, .service-details p {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 8px 0;
  color: #e2e8f0;
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
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
}

.accept-btn {
  background: #48bb78;
}

.complete-btn {
  background: #4299e1;
}

.action-buttons button:hover {
  transform: translateY(-2px);
  opacity: 0.9;
}

@media (max-width: 768px) {
  .main-container {
    padding: 15px;
  }
  
  .nav-buttons {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .search-filters {
    flex-direction: column;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
  }
}

.blocked-message {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid #dc3545;
  border-radius: 12px;
  padding: 20px;
  margin: 20px 0;
  text-align: center;
}

.blocked-message h3 {
  color: #dc3545;
  margin-bottom: 10px;
}

.confirmed-services {
  margin-top: 30px;
}

.confirmed-services h4 {
  color: #e2e8f0;
  margin-bottom: 20px;
}
</style>