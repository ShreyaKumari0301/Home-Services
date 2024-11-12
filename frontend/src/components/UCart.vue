<template>
  <div>
    <h2>Services in Your Cart</h2>
    <div v-if="cartItems.length">
      <div v-for="item in cartItems" :key="item.id" class="cart-item">
        <p>{{ item.service.name }} - Quantity: {{ item.quantity }}</p>
        <p>Price per unit: {{ item.service.base_price }} Rs</p>
        <p>Subtotal: {{ item.quantity * item.service.base_price }} Rs</p>
      </div>
      <div>
        <h3>Total Cost: {{ totalCost }} Rs</h3>
      </div>
    </div>
    
    <div v-else>
      <p>No items in your cart.</p>
    </div>

    <div v-if="cartItems.length">
      <h3>Booking Details</h3>
      <label>Select Booking Date:</label>
      <input type="date" v-model="bookingDate" />
      
      <label>Select Time Slot:</label>
      <div class="time-slots">
        <button v-for="slot in timeSlots" :key="slot" @click="selectTimeSlot(slot)">
          {{ slot }}
        </button>
      </div>

      <h4>Selected Slot: {{ selectedTimeSlot }}</h4>
      
      <button @click="placeOrder" :disabled="!selectedTimeSlot || !bookingDate">Place an Order</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      cartItems: [],
      bookingDate: '',
      timeSlots: ["7:00 AM", "9:00 AM", "11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM"],
      selectedTimeSlot: '',
      totalCost: 0
    };
  },
  mounted() {
    this.fetchCartItems();
  },
  methods: {
    fetchCartItems() {
      axios.get('http://127.0.0.1:5000/api/ucart')
        .then(response => {
          this.cartItems = response.data;
          this.calculateTotal();
        })
        .catch(error => {
          console.error("Error fetching cart items:", error);
        });
    },
    calculateTotal() {
      this.totalCost = this.cartItems.reduce((acc, item) => acc + (item.quantity * item.service.base_price), 0);
    },
    selectTimeSlot(slot) {
      this.selectedTimeSlot = slot;
    },
    placeOrder() {
      const orderData = {
        booking_date: this.bookingDate,
        booking_time: this.selectedTimeSlot,
        services: this.cartItems.map(item => ({ service_id: item.service_id, quantity: item.quantity })),
        total_cost: this.totalCost
      };
      
      axios.post('http://127.0.0.1:5000/api/place_order', orderData)
        .then(response => {
          alert('Order placed successfully!');
          this.$router.push('/dashboard'); // Navigate to another page if needed
        })
        .catch(error => {
          console.error("Error placing order:", error);
        });
    }
  }
};
</script>

<style scoped>
.cart-item {
  border-bottom: 1px solid #ddd;
  padding: 10px 0;
}
.time-slots button {
  margin: 5px;
  padding: 5px 10px;
}
</style>
