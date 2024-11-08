<template>
  <div class="category-page">
    <h2>{{ category }} Services</h2>
    <div class="service-list">
      <div v-for="service in services" :key="service.id" class="service-box">
        <h3>{{ service.name }}</h3>
        <p>{{ service.description }}</p>
        <p>Base Price: {{ service.basePrice }}</p>
        <div class="quantity-control">
          <button @click="decreaseQuantity(service)">v</button>
          <span>{{ service.quantity }}</span>
          <button @click="increaseQuantity(service)">^</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["category"],
  data() {
    return {
      services: [], // Fetch services for the category from API
    };
  },
  methods: {
    increaseQuantity(service) {
      service.quantity += 1;
      // Add service to cart with updated quantity
    },
    decreaseQuantity(service) {
      if (service.quantity > 0) {
        service.quantity -= 1;
      }
    },
  },
};
</script>

<style>
/* Add styling for service boxes and quantity controls */
</style>
