<template>
  <div class="container">
    <div class="form-container">
      <h3>Add Service</h3>
      <hr />
      <form @submit.prevent="handleAddService">
        <div class="form-group">
          <label>Name</label>
          <input type="text" v-model="name" class="form-control" placeholder="Enter service name" required />
        </div>
        <div class="form-group">
          <label>Base Price</label>
          <input type="number" v-model="base_price" class="form-control" placeholder="Enter base price" required />
        </div>
        <div class="form-group">
          <label>Description</label>
          <textarea v-model="description" class="form-control" placeholder="Enter service description" required></textarea>
        </div>
        <div class="form-group">
          <label>Category</label>
          <input type="text" v-model="category" class="form-control" placeholder="Enter category" required />
        </div>
        <div class="form-group">
          <label>Time Required (mins)</label>
          <input type="number" v-model="time_required" class="form-control" placeholder="Enter time required" required />
        </div>
        <div class="form-group">
          <label>Average Rating</label>
          <input type="number" step="0.1" min="0" max="5" v-model="avg_rating" class="form-control" placeholder="Enter average rating" required />
        </div>
        <button type="submit" class="submit-btn">Add Service</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AddService",
  data() {
    return {
      name: "",
      base_price: "",
      description: "",
      category: "",
      time_required: "",
      avg_rating: "",
    };
  },
  methods: {
    async handleAddService() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          alert("Unauthorized. Please log in.");
          this.$router.push("/login");
          return;
        }

        const response = await axios.post(
          "http://127.0.0.1:5000/adminservice",
          {
            name: this.name,
            base_price: this.base_price,
            description: this.description,
            category: this.category,
            time_required: this.time_required,
            avg_rating: this.avg_rating,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        console.log("Service added successfully:", response.data);
        alert("Service added successfully");
        this.resetForm();
        this.$router.push("/admin");
      } catch (error) {
        console.error("Failed to add service:", error);
        alert(error.response?.data?.message || "Failed to add service.");
      }
    },
    resetForm() {
      this.name = "";
      this.base_price = "";
      this.description = "";
      this.category = "";
      this.time_required = "";
      this.avg_rating = "";
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.form-container h3 {
  text-align: center;
  margin-bottom: 1rem;
}
.form-group {
  margin-bottom: 1rem;
}
.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 0.5rem;
}
.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
}
.submit-btn {
  display: block;
  width: 100%;
  padding: 0.75rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.submit-btn:hover {
  background-color: #0056b3;
}
</style>
