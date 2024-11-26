<template>
  <div class="profile-container">
    <h2>User Profile</h2>
    <form @submit.prevent="updateProfile" class="profile-form">
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="user.name" required />
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="user.email" required />
      </div>
      <div class="form-group">
        <label for="mobile">Mobile Number:</label>
        <input type="tel" id="mobile" v-model="user.mobile_number" required />
      </div>
      <div class="form-group">
        <label for="address">Address:</label>
        <input type="text" id="address" v-model="user.address" required />
      </div>
      <div class="form-group">
        <label for="pincode">Pincode:</label>
        <input type="text" id="pincode" v-model="user.pincode" required />
      </div>
      <button type="submit" class="submit-btn">Update Profile</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UProfile',
  data() {
    return {
      user: {
        name: '',
        email: '',
        mobile_number: '',
        address: '',
        pincode: '',
      },
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem('token');
      const authValue = 'Bearer ' + token;

      const response = await axios.get('http://127.0.0.1:5000/profile', {
        headers: { Authorization: authValue },
      });
      this.user = response.data;
    } catch (error) {
      console.error('Error fetching user profile:', error);
      alert('An error occurred. Please try again later.');
    }
  },
  methods: {
    async updateProfile() {
      try {
        const token = localStorage.getItem('Auth-Token');
        let tokenValue = JSON.parse(token || null);
        const authValue = 'Bearer ' + token;
        const data = {
          name: this.user.name,
          email: this.user.email,
          mobile_number: this.user.mobile_number,
          address: this.user.address,
          pincode: this.user.pincode,
        };

        const response = await axios.put('http://127.0.0.1:5000/profile', data, {
          headers: { Authorization: authValue },
        });
        alert('Profile updated successfully.');
      } catch (error) {
        console.error('Error updating user profile:', error);
        alert('An error occurred. Please try again later.');
      }
    },
  },
};
</script>

<style scoped>
.profile-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.profile-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 5px;
  color: #555;
}

.form-group input[type="text"],
.form-group input[type="email"],
.form-group input[type="tel"] {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
}

.submit-btn {
  background-color: #007bff;
  color: #fff;
  font-size: 16px;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
  margin-top: 15px;
}

.submit-btn:hover {
  background-color: #0056b3;
}
</style>
