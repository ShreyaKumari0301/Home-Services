<template>
  <div class="main-container">
    <div class="navigation-bar">
      <div class="nav-header">
        <h2><i>My Orders</i></h2>
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
    </div>
    
    <div class="content-area">
      <div class="services-container">
        <div v-for="status in groupedOrders" :key="status.name" class="category-section">
          <h3 class="category-title">{{ status.name }}</h3>
          <div class="services-grid">
            <div v-for="order in status.orders" :key="order.id" class="service-card">
              <!-- Service Details Box -->
              <div class="details-box service-details">
                <div class="service-header">
                  <h4>{{ order.service_name }}</h4>
                  <span :class="['status-badge', order.status.toLowerCase()]">
                    {{ order.status }}
                  </span>
                </div>
                <div class="service-info">
                  <p><i class="calendar-icon">📅</i> {{ order.booking_date }}</p>
                  <p><i class="time-icon">⏰</i> {{ order.time_slot }}</p>
                  <p><i class="quantity-icon">🔢</i> Quantity: {{ order.quantity }}</p>
                  <p><i class="price-icon">💰</i> ₹{{ order.total_price }}</p>
                </div>
              </div>

              <!-- Professional Details Box -->
              <div v-if="order.professional_details" class="details-box professional-details">
                <h4>Professional Details</h4>
                <div class="professional-info">
                  <p><i class="user-icon">👤</i> {{ order.professional_details.name }}</p>
                  <p><i class="phone-icon">📱</i> {{ order.professional_details.phone }}</p>
                  <p><i class="star-icon">⭐</i> Rating: {{ order.professional_details.rating }}</p>
                </div>
              </div>

              <!-- Waiting Message -->
              <div v-else class="details-box waiting-message">
                <p>Waiting for professional to accept...</p>
              </div>

              <!-- Action Buttons -->
              <div class="button-container">
                <div v-if="order.status === 'confirmed'" class="action-group">
                  <button 
                    @click="closeRequest(order.id)" 
                    class="action-button close-btn"
                  >
                    Close Service
                  </button>
                  <button 
                    @click="cancelRequest(order.id)" 
                    class="action-button cancel-btn"
                  >
                    Cancel Service
                  </button>
                </div>
                <button 
                  v-if="!order.rated && order.status === 'completed'" 
                  @click="showRatingModal(order)" 
                  class="action-button rate-btn"
                >
                  Rate Service
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Rating Modal -->
    <div v-if="showRating" class="modal-overlay">
      <div class="modal-content">
        <h3>Rate Service</h3>
        <p class="rating-text">How would you rate this service?</p>
        <div class="star-rating">
          <span 
            v-for="star in 5" 
            :key="star"
            @click="setRating(star)"
            :class="{ active: star <= selectedRating }"
          >
            ⭐
          </span>
        </div>
        <div class="modal-buttons">
          <button 
            @click="closeRatingModal" 
            class="action-button cancel-btn"
          >
            Cancel
          </button>
          <button 
            @click="submitRating" 
            class="action-button submit-btn"
            :disabled="!selectedRating"
          >
            Submit
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      serviceRequests: [],
      showRating: false,
      selectedRating: 0,
      selectedRequest: null,
      currentRoute: 'UOrders'
    };
  },
  computed: {
    groupedOrders() {
      const statusOrder = ['pending', 'confirmed', 'completed'];
      const statusNames = {
        'pending': 'Requested Services',
        'confirmed': 'Confirmed Services',
        'completed': 'Completed Services'
      };
      
      const grouped = {};
      statusOrder.forEach(status => {
        const ordersWithStatus = this.serviceRequests.filter(order => order.status === status);
        if (ordersWithStatus.length > 0) {
          grouped[status] = {
            name: statusNames[status],
            orders: ordersWithStatus
          };
        }
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
    async fetchServiceRequests() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/customer/service-requests', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.serviceRequests = response.data;
      } catch (error) {
        console.error('Error fetching service requests:', error);
      }
    },
    async closeRequest(requestId) {
      try {
        const token = localStorage.getItem('token');
        await axios.put(`http://127.0.0.1:5000/customer/service-requests/${requestId}/close`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
        await this.fetchServiceRequests();
      } catch (error) {
        console.error('Error closing request:', error);
      }
    },
    showRatingModal(request) {
      this.selectedRequest = request;
      this.showRating = true;
      this.selectedRating = 0;
    },
    closeRatingModal() {
      this.showRating = false;
      this.selectedRequest = null;
      this.selectedRating = 0;
    },
    setRating(rating) {
      this.selectedRating = rating;
    },
    async submitRating() {
      if (!this.selectedRequest || !this.selectedRating) return;

      try {
        const token = localStorage.getItem('token');
        await axios.post(
          `http://127.0.0.1:5000/customer/service-requests/${this.selectedRequest.id}/rate`,
          { rating: this.selectedRating },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.closeRatingModal();
        await this.fetchServiceRequests();
      } catch (error) {
        console.error('Error submitting rating:', error);
      }
    }
  },
  mounted() {
    this.fetchServiceRequests();
  }
};
</script>

<style scoped>
.main-container {
  background-color: #f5f5f5;
  padding: 18px;
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
  padding: 8px 10px;
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

.content-area {
  margin-top: 1px;
}

.services-container {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  max-width: 800px;
  margin: 0 auto;
  color: black;
}

.category-section {
  margin-bottom: 40px;
}

.category-title {
  font-size: 1.5rem;
  color: #212529;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #dee2e6;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.service-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.service-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.details-box {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  color: black; /* Ensures the text inside the box is black */
}

.service-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
  font-weight: 500;
}

.status-badge.pending {
  background: #ffd700;
  color: #000;
}

.status-badge.confirmed {
  background: #4CAF50;
  color: white;
}

.status-badge.completed {
  background: #2196F3;
  color: white;
}

.service-info, .professional-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  color: black; /* Black text for service and professional details */
}

.service-info p,
.professional-info p {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
}

.waiting-message {
  text-align: center;
  color: black; /* Black text for waiting messages */
  padding: 15px;
}

.action-button {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
}

.action-button.close-btn {
  background: #dc3545;
}

.action-button.rate-btn {
  background: #ffc107;
  color: #000;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 12px;
  min-width: 300px;
  color: black;
}

.star-rating {
  margin: 20px 0;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.star-rating span {
  font-size: 24px;
  cursor: pointer;
  opacity: 0.3;
  color: black;
  transition: all 0.3s ease;
}

.star-rating span.active {
  opacity: 1;
  color: #ffd700;
}

.modal-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 20px;
}

.modal-buttons .action-button {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  min-width: 100px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.modal-buttons .cancel-btn {
  background: #dc3545;
  color: white;
}

.modal-buttons .submit-btn {
  background: #28a745;
  color: white;
}

.modal-buttons .submit-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
  opacity: 0.7;
}

.modal-buttons .action-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.rating-text {
  color: #495057;
  margin: 15px 0;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .main-container {
    padding: 10px;
  }
  
  .nav-buttons {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
