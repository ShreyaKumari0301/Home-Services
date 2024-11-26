<template>
  <div class="orders-dashboard">
    <h2>My Service Requests</h2>
    
    <div v-if="orders.length === 0" class="no-orders">
      <p>No service requests found</p>
    </div>
    
    <div v-else class="orders-container">
      <div v-for="order in orders" :key="order.id" class="order-card">
        <div class="service-info">
          <h3>{{ order.service_name }}</h3>
          <p><strong>Booking Date:</strong> {{ order.booking_date }}</p>
          <p><strong>Time Slot:</strong> {{ order.time_slot }}</p>
          <p><strong>Quantity:</strong> {{ order.quantity }}</p>
          <p><strong>Total Price:</strong> ₹{{ order.total_price }}</p>
          <p><strong>Status:</strong> <span :class="'status-' + order.status">{{ order.status }}</span></p>
        </div>
        
        <div v-if="order.professional_details" class="professional-info">
          <h4>Professional Details</h4>
          <p><strong>Name:</strong> {{ order.professional_details.name }}</p>
          <p><strong>Phone:</strong> {{ order.professional_details.phone }}</p>
          <p><strong>Rating:</strong> {{ order.professional_details.rating }} ⭐</p>
        </div>
        
        <div v-else class="waiting-info">
          <p>Waiting for professional to accept your request...</p>
        </div>
        
        <div class="actions" v-if="order.status === 'confirmed'">
          <button 
            @click="closeService(order.id)"
            class="close-btn"
          >
            Close Service
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
      orders: []
    }
  },
  methods: {
    async fetchOrders() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/customer/service-requests', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.orders = response.data;
      } catch (error) {
        console.error('Error fetching orders:', error);
        if (error.response?.status === 401) {
          this.$router.push('/login');
        }
      }
    },
    async closeService(orderId) {
      try {
        const token = localStorage.getItem('token');
        await axios.put(`http://127.0.0.1:5000/customer/service-requests/${orderId}/close`, 
          {},
          {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          }
        );
        await this.fetchOrders();
      } catch (error) {
        console.error('Error closing service:', error);
        alert('Failed to close service');
      }
    }
  },
  mounted() {
    this.fetchOrders();
  }
}
</script>

<style scoped>
.orders-dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.order-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.service-info, .professional-info, .waiting-info {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 4px;
}

.waiting-info {
  grid-column: 1 / -1;
  text-align: center;
  color: #6c757d;
}

.actions {
  grid-column: 1 / -1;
  display: flex;
  justify-content: flex-end;
}

.close-btn {
  padding: 8px 16px;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.close-btn:hover {
  background: #c82333;
}

.status-pending {
  color: #f0ad4e;
}

.status-confirmed {
  color: #5cb85c;
}

.status-completed {
  color: #0275d8;
}

.status-closed {
  color: #d9534f;
}

.no-orders {
  text-align: center;
  padding: 40px;
  background: #f8f9fa;
  border-radius: 8px;
  color: #6c757d;
}
</style>