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
import axios from 'axios';

export default {
    name: "AddService",
    data() {
        return {
            name: "",
            base_price: "",
            description: "",
            category: "",
            time_required: "",
            avg_rating: ""
        };
    },
    methods: {
        async handleAddService() {
            try {
                const response = await axios.post('http://127.0.0.1:5000/services', {
                    name: this.name,
                    base_price: this.base_price,
                    description: this.description,
                    category: this.category,
                    time_required: this.time_required,
                    avg_rating: this.avg_rating
                });
                console.log("Service added successfully", response.data);
                alert("Service added successfully");
                this.$router.push('/admin');

            } catch (error) {
                console.error("Failed to add service", error);
                alert("Failed to add service");
            }
        },
    }
};
</script>

<style>
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
