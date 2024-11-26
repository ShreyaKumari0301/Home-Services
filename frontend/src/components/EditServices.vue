<template>
    <div class="container">
        <div class="form-container">
            <h3>Edit Service</h3>
            <hr />
            <form @submit.prevent="editService">
                <div class="form-group">
                    <label>Name</label>
                    <input type="text" v-model="service.name" class="form-control" placeholder="Enter service name" required />
                </div>
                <div class="form-group">
                    <label>Base Price</label>
                    <input type="number" v-model="service.base_price" class="form-control" placeholder="Enter base price" required />
                </div>
                <div class="form-group">
                    <label>Description</label>
                    <textarea v-model="service.description" class="form-control" placeholder="Enter service description"></textarea>
                </div>
                <div class="form-group">
                    <label>Category</label>
                    <input type="text" v-model="service.category" class="form-control" placeholder="Enter category" />
                </div>
                <div class="form-group">
                    <label>Time Required (mins)</label>
                    <input type="number" v-model="service.time_required" class="form-control" placeholder="Enter time required" />
                </div>
                <div class="form-group">
                    <label>Average Rating</label>
                    <input type="number" step="0.1" min="0" max="5" v-model="service.avg_rating" class="form-control" placeholder="Enter average rating" />
                </div>
                <button type="submit" class="submit-btn">Update Service</button>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'EditService',
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
    async EditService() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          alert("Unauthorized. Please log in.");
          this.$router.push("/login");
          return;
        }
        const response = await axios.put(
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

        console.log("Service updated successfully:", response.data);
        alert("Service updated successfully");
        this.resetForm();
        this.$router.push("/admin");
      } catch (error) {
        console.error("Failed to updated service:", error);
        alert(error.response?.data?.message || "Failed to update service.");
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
body {
    background-color: #025f5d;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    margin: 0;
    font-family: Arial, sans-serif;
}

.container {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
}

.form-container {
    background-color: #ffffff;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(88, 195, 199, 0.504);
    width: 100%;
    max-width: 400px;
    text-align: center;
}

h3 {
    margin-bottom: 20px;
    font-size: 24px;
    color: #333;
}

.form-group {
    margin-bottom: 15px;
    text-align: left;
}

label {
    font-size: 14px;
    color: #555;
}

.form-control {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-sizing: border-box;
    margin-top: 5px;
}

.form-control:focus {
    border-color: #007bff;
    outline: none;
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.3);
}

.submit-btn {
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 8px;
    background-color: #007bff;
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-top: 20px;
}

.submit-btn:hover {
    background-color: #0056b3;
}
</style>
