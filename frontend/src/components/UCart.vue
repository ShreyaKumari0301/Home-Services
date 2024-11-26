<template>
  <div class="cart-container">
    <h2>Add Service to Cart</h2>
    
    <div v-if="service" class="service-details">
      <h3>{{ service.name }}</h3>
      
      <div class="quantity-section">
        <label>Quantity:</label>
        <input 
          type="number" 
          v-model.number="quantity" 
          min="1" 
          @change="calculateTotalPrice"
        />
      </div>
      
      <div class="booking-date-section">
        <label>Booking Date:</label>
        <div class="date-options">
          <button 
            v-for="(date, index) in bookingDates" 
            :key="index"
            @click="selectBookingDate(date)"
            :class="{ selected: selectedBookingDate === date }"
          >
            {{ date }}
          </button>
        </div>
      </div>
      <div class="time-slot-section">
        <label>Time Slot:</label>
        <div class="time-slots">
          <button 
            v-for="slot in timeSlots" 
            :key="slot"
            @click="selectTimeSlot(slot)"
            :class="{ 'selected': selectedTimeSlot === slot }"
          >
            {{ slot }}
          </button>
        </div>
      </div>
      <div class="price-section">
        <p>Base Price: {{ service.base_price }}</p>
        <p>Total Price: {{ totalPrice }}</p>
      </div>
      
      <button 
        @click="addToCart" 
        :disabled="!isFormValid"
      >
        Confirm Service Request
      </button>
    </div>
    
    <div v-else>
      <p>Loading service details...</p>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      service: null,
      quantity: 1,
      totalPrice: 0,
      selectedBookingDate: null,  // Changed from selectedDate to selectedBookingDate
      selectedTimeSlot: null,
      bookingDates: [],
      timeSlots: [
        '9:00 AM', '10:00 AM', '11:00 AM', 
        '12:00 PM', '1:00 PM', '2:00 PM', 
        '3:00 PM', '4:00 PM', '5:00 PM'
      ]
    };
  },
  computed: {
    isFormValid() {
      return this.service && 
             this.quantity > 0 && 
             this.selectedBookingDate && 
             this.selectedTimeSlot;
    }
  },
  methods: {
    calculateTotalPrice() {
      if (this.service) {
        this.totalPrice = this.service.base_price * this.quantity;
      }
    },
    generateBookingDates() {
      const today = new Date();
      this.bookingDates = [
        this.formatDate(today),
        this.formatDate(new Date(today.getTime() + 24*60*60*1000)),
        this.formatDate(new Date(today.getTime() + 2*24*60*60*1000)),
      ];
    },
    formatDate(date) {
      return date.toISOString().split('T')[0];
    },
    selectBookingDate(date) {
      this.selectedBookingDate = date;
    },
    selectTimeSlot(slot) {
      this.selectedTimeSlot = slot;
    },
    async addToCart() {
      try {
        // First get customer details
        const email = localStorage.getItem('email');
        const customerResponse = await axios.get(`http://127.0.0.1:5000/customer-details?email=${email}`);
        const customerDetails = customerResponse.data;

        const serviceRequestData = {
          service_id: this.service.id,
          customer_id: customerDetails.id,
          email: email,
          booking_date: this.selectedBookingDate,
          time_slot: this.selectedTimeSlot,
          quantity: this.quantity,
          total_price: this.totalPrice
        };

        const response = await axios.post('http://127.0.0.1:5000/service-requests', serviceRequestData);
        alert('Service request added successfully!');
        this.$router.push('/');
      } catch (error) {
        console.error('Error adding service request:', error);
        if (error.response?.data?.error) {
          alert(error.response.data.error);
        } else {
          alert('Failed to add service request. Please try again later.');
        }
      }
    }
  },
  async mounted() {
    try {
      const serviceId = this.$route.params.serviceId;
      const response = await axios.get(`http://127.0.0.1:5000/services/${serviceId}`);
      this.service = response.data;
      this.calculateTotalPrice();
      this.generateBookingDates();
    } catch (error) {
      console.error('Error fetching service details:', error);
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
/* Add these styles */
.cart-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.service-details {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.quantity-section,
.booking-date-section,
.time-slot-section,
.price-section {
  margin: 20px 0;
}

.date-options,
.time-slots {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 10px;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #007bff;
  color: white;
}

button.selected {
  background-color: #28a745;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

input[type="number"] {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 80px;
}

.price-section {
  font-size: 1.2em;
  font-weight: bold;
}
</style>