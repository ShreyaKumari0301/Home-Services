<template>
  <div class="ucart">
    <h2>Your Cart</h2>
    <div v-if="cartItems.length">
      <div v-for="(item, index) in cartItems" :key="index" class="cart-item">
        <h3>{{ item.name }}</h3>
        <p>{{ item.description }}</p>
        <p>Price: Rs. {{ item.base_price }}</p>
        
        <div>
          <label>Quantity: </label>
          <input type="number" v-model.number="item.quantity" @change="updateTotal" min="1" />
        </div>
        <p>Subtotal: Rs. {{ item.base_price * item.quantity }}</p>
      </div>
      <hr />
       <div>
    <h3>Choose a Date</h3>
    <input type="date" v-model="selectedDate" :min="today" :max="maxDate" />

    <h3>Choose a Time Slot</h3>
    <select v-model="selectedTime">
      <option v-for="hour in hours" :key="hour" :value="hour">{{ hour }}:00</option>
    </select>

    <button @click="placeOrder">Place Order</button>
  </div>
  <hr />
      <div class="charges">
        <p>Hygiene Charges: Rs. 39</p>
        <p>Total: Rs. {{ calculateTotal() }}</p>
      </div>
    </div>
    <div v-else>
      <p>Your cart is empty.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedDate: '',
      selectedTime: '07',
      today: new Date().toISOString().split('T')[0],
      maxDate: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString().split('T')[0],
      hours: [...Array(13).keys()].map(i => i + 7)  // Generates hours from 7 to 19 (7 AM to 7 PM)
    };
  },
  methods: {
    async placeOrder() {
      const bookingDateTime = `${this.selectedDate} ${this.selectedTime}:00`;
      const payload = {
        service_id: this.serviceId,
        user_id: this.userId,
        professional_id: this.professionalId,
        booking_date: bookingDateTime,
      };

      const response = await axios.post('/service_requests', payload);
      if (response.status === 201) {
        alert('Order placed successfully!');
        this.$router.push({ name: 'Records' });
      } else {
        alert(response.data.message || 'An error occurred while placing the order.');
      }
    }
  }
};
</script>


<style scoped>
.ucart {
  max-width: 600px;
  margin: 0 auto;
}
.cart-item {
  margin-bottom: 20px;
}
.charges {
  font-weight: bold;
  text-align: right;
}
</style>
