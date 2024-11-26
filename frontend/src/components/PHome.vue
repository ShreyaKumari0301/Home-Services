<template>
  <div class="dashboard">
    <h2>Available Service Requests</h2>
    
    <div v-if="pendingApproval" class="pending-approval">
      <h3>Account Pending Approval</h3>
      <p>Your account is currently under review. You'll be able to view and accept service requests once approved.</p>
    </div>
    
    <div v-else class="requests-container">
      <div v-if="serviceRequests.length === 0" class="no-requests">
        <p>No service requests available at this time.</p>
      </div>
      
      <div v-for="request in serviceRequests" :key="request.id" class="request-card">
        <div class="service-info">
          <h3>{{ request.service_name }}</h3>
          <p><strong>Quantity:</strong> {{ request.quantity }}</p>
          <p><strong>Total Price:</strong> ₹{{ request.total_price }}</p>
          <p><strong>Date:</strong> {{ request.booking_date }}</p>
          <p><strong>Time Slot:</strong> {{ request.time_slot }}</p>
        </div>
        
        <div class="customer-info">
          <h4>Customer Details</h4>
          <p><strong>Name:</strong> {{ request.customer_name }}</p>
          <p><strong>Phone:</strong> {{ request.customer_phone }}</p>
          <p><strong>Address:</strong> {{ request.customer_address }}</p>
          <p><strong>Pincode:</strong> {{ request.service_pincode }}</p>
        </div>
        
        <button 
          @click="acceptRequest(request.id)"
          :disabled="request.status !== 'pending'"
          class="accept-btn"
        >
          Accept Request
        </button>
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
      pendingApproval: false
    }
  },
  methods: {
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    },
    async fetchRequests() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/professional/service-requests', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.serviceRequests = response.data;
        this.pendingApproval = false;
      } catch (error) {
        console.error('Error fetching requests:', error);
        if (error.response?.status === 401) {
          this.$router.push('/login');
        } else if (error.response?.status === 403) {
          this.pendingApproval = true;
        }
      }
    },
    async acceptRequest(requestId) {
      try {
        const token = localStorage.getItem('token');
        await axios.put(
          'http://127.0.0.1:5000/professional/service-requests',
          { service_request_id: requestId },
          {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          }
        );
        await this.fetchRequests();
      } catch (error) {
        console.error('Error accepting request:', error);
        alert('Failed to accept request');
      }
    }
  },
  mounted() {
    this.fetchRequests();
  }
}
</script>

<style scoped>
.request-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.service-info, .customer-info {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 4px;
}

.accept-btn {
  grid-column: 1 / -1;
  padding: 10px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.accept-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}
</style>