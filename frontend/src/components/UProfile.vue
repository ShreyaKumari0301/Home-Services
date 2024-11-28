<template>
  <div class="main-container">
    <div class="navigation-bar">
      <div class="nav-header">
        <h2><i>My Profile</i></h2>
        <div class="nav-buttons">
          <button 
            @click="navigateTo('UHome')"
            :class="{ active: currentRoute === 'UHome' }"
          >Home</button>
          <button 
            @click="navigateTo('UOrders')"
            :class="{ active: currentRoute === 'UOrders' }"
          >Orders</button>
          <button 
            @click="navigateTo('UProfile')"
            :class="{ active: currentRoute === 'UProfile' }"
          >Profile</button>
          <button 
            @click="navigateTo('USummary')"
            :class="{ active: currentRoute === 'USummary' }"
          >Summary</button>
          <button @click="logout" class="logout-btn">Logout</button>
        </div>
      </div>
    </div>
    
    <div class="content-area">
      <div class="profile-container">
        <form @submit.prevent="updateProfile" class="profile-form">
          <!-- Email field (readonly) -->
          <div class="form-group">
            <label for="email">Email:</label>
            <input 
              type="email" 
              id="email" 
              v-model="user.email" 
              readonly 
              class="readonly-input"
            />
            <small class="form-text">Email cannot be changed</small>
          </div>

          <!-- Name field -->
          <div class="form-group">
            <label for="name">Name:</label>
            <input 
              type="text" 
              id="name" 
              v-model="user.name" 
              required 
            />
          </div>
          
          <!-- Mobile Number field -->
          <div class="form-group">
            <label for="mobile">Mobile Number:</label>
            <input 
              type="tel" 
              id="mobile" 
              v-model="user.mobile_number" 
              required 
              pattern="[0-9]{10}"
              title="Please enter a valid 10-digit mobile number"
            />
          </div>
          
          <!-- Address field -->
          <div class="form-group">
            <label for="address">Address:</label>
            <input 
              type="text" 
              id="address" 
              v-model="user.address" 
              required 
            />
          </div>
          
          <!-- Pincode field -->
          <div class="form-group">
            <label for="pincode">Pincode:</label>
            <input 
              type="text" 
              id="pincode" 
              v-model="user.pincode" 
              required 
              pattern="[0-9]{6}"
              title="Please enter a valid 6-digit pincode"
            />
          </div>
          
          <button type="submit" class="submit-btn">Update Profile</button>
        </form>
      </div>
    </div>
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
      currentRoute: 'UProfile'
    };
  },
  methods: {
    navigateTo(page) {
      this.$router.push({ name: page });
    },
    logout() {
      localStorage.clear();
      this.$router.push("/login");
    },
    async fetchUserProfile() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/uprofile', {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.user = response.data;
      } catch (error) {
        console.error('Error fetching user profile:', error);
        if (error.response?.status === 401) {
          this.$router.push('/login');
        } else {
          alert('Failed to load profile. Please try again later.');
        }
      }
    },
    async updateProfile() {
      try {
        const token = localStorage.getItem('token');
        await axios.put('http://127.0.0.1:5000/uprofile', 
          {
            name: this.user.name,
            mobile_number: this.user.mobile_number,
            address: this.user.address,
            pincode: this.user.pincode,
          },
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );
        alert('Profile updated successfully!');
      } catch (error) {
        console.error('Error updating profile:', error);
        alert('Failed to update profile. Please try again.');
      }
    }
  },
  mounted() {
    this.fetchUserProfile();
  }
};
</script>

<style scoped>
.main-container {
  background-color: #f5f5f5;
  padding: 18px;
}

.navigation-bar {
  background: white;
  padding: 1rem 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-buttons {
  display: flex;
  gap: 15px;
}

.nav-buttons button {
  padding: 8px 10px;
  border: none;
  border-radius: 8px;
  background: #f8f9fa;
  color: #495057;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-buttons button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-buttons button.active {
  background: #0d6efd;
  color: white;
}

.logout-btn {
  background: #dc3545 !important;
  color: white !important;
}

.content-area {
  margin-top: 1px;
}

.profile-container {
  background: white;
  border-radius: 12px;
  color : black;
  padding: 25px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  max-width: 800px;
  margin: 0 auto;
}

.profile-form {
  display: grid;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 500;
  color: #212529;
}

input {
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.readonly-input {
  background-color: #e9ecef;
  cursor: not-allowed;
}

input:focus:not(.readonly-input) {
  border-color: #0d6efd;
  outline: none;
  box-shadow: 0 0 0 0.25rem rgba(13,110,253,0.25);
}

.form-text {
  color: #6c757d;
  font-size: 0.875rem;
}

.submit-btn {
  padding: 12px;
  background-color: #0d6efd;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  background-color: #0b5ed7;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .main-container {
    padding: 10px;
  }
  
  .nav-buttons {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>

