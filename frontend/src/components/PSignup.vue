<template>
  <div class="container">
    <div class="signup-form">
      <h3>Professional Registration</h3>
      <hr />
      <form @submit.prevent="validateForm">
        <!-- Your existing form fields -->
        <div class="form-group">
          <label>Name</label>
          <input type="text" class="form-control" v-model="name" placeholder="Enter your name" required />
        </div>

        <div class="form-group">
          <label>Email</label>
          <input type="email" class="form-control" v-model="email" placeholder="Enter your email" required />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input type="password" class="form-control" v-model="password" placeholder="Enter your password" required />
        </div>

        <div class="form-group">
          <label>Mobile Number</label>
          <input type="text" class="form-control" v-model="mobileNumber" placeholder="Enter your mobile number" required />
        </div>

        <div class="form-group">
          <label>Pincode</label>
          <input type="text" class="form-control" v-model="pincode" placeholder="Enter pincodes (comma-separated for multiple)" required />
          <small class="help-text">For multiple pincodes, separate them with commas (e.g., 123456,234567)</small>
        </div>

        <div class="form-group">
          <label>Service Category</label>
          <input type="text" class="form-control" v-model="serviceCategory" placeholder="Enter service category" required />
        </div>

        <div class="form-group">
          <label>Experience (Years)</label>
          <input type="number" class="form-control" v-model="experience" placeholder="Enter years of experience" required />
        </div>

        <div class="form-group">
          <label>Aadhar Card</label>
          <input type="text" class="form-control" v-model="aadharCard" placeholder="Enter your Aadhar card number" required />
        </div>

        <div class="form-group">
          <label>Document</label>
          <input type="file" class="form-control file-input" @change="handleFileUpload" required />
          <small class="help-text">Maximum file size: 5MB</small>
        </div>

        <button type="submit" class="submit-btn">Sign Up</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PSignup",
  data() {
    return {
      name: "",
      email: "",
      password: "",
      mobileNumber: "",
      pincode: "",
      serviceCategory: "",
      experience: "",
      aadharCard: "",
      document: null,
    };
  },
  methods: {
    handleFileUpload(event) {
      this.document = event.target.files[0];
    },
    async validateForm() {
      const mobileNumberPattern = /^\d{10}$/;


      if (!mobileNumberPattern.test(this.mobileNumber)) {
        alert("Mobile number must be exactly 10 digits.");
        return;
      }

      // Ensure document is uploaded
      if (!this.document) {
        alert("Please upload a document.");
        return;
      }

      // Check file size (5MB limit)
      const maxSize = 5 * 1024 * 1024; // 5MB in bytes
      if (this.document.size > maxSize) {
        alert("Document size must be less than 5MB");
        return;
      }

      const formData = new FormData();
      formData.append("name", this.name);
      formData.append("email", this.email);
      formData.append("password", this.password);
      formData.append("mobileNumber", this.mobileNumber);
      formData.append("pincode", this.pincode);
      formData.append("serviceCategory", this.serviceCategory);
      formData.append("experience", this.experience);
      formData.append("aadharCard", this.aadharCard);
      formData.append("document", this.document);

      console.log(this.pincode);

      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/professional/signup",
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        );

        if (response.status === 201) {
          alert(response.data.message);
          console.log("Professional signup successful", response.data);
          this.$router.push({ name: 'LoginPg' });
        }
      } catch (error) {
        console.error("Signup failed", error);
        if (error.response) {
          alert(error.response.data.message || "Signup failed");
        } else {
          alert("Network error occurred. Please try again.");
        }
      }
    }
  }
};
</script>

<style scoped>
body {
  background-color: #071228;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  margin: 0;
  font-family: Arial, sans-serif;
  color: white;
}

.container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 100vh;
  background-color: #071228;
  padding: 20px;
}

.signup-form {
  background-color: #1a2942;
  padding: 30px;
  border-radius: 15px;
  width: 100%;
  max-width: 500px;
  color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.signup-form h3 {
  margin-bottom: 20px;
  font-size: 24px;
  color: white;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: white;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 12px;
  border: 1px solid #2d4056;
  border-radius: 8px;
  background-color: #2d4056;
  color: white;
  transition: all 0.3s ease;
}

.file-input {
  padding: 8px;
  background-color: #2d4056;
}

.form-control:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 2px rgba(66, 153, 225, 0.2);
}

.help-text {
  display: block;
  margin-top: 5px;
  color: #a0aec0;
  font-size: 0.875rem;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  background-color: #4299e1;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 20px;
}

.submit-btn:hover {
  background-color: #3182ce;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

hr {
  border: none;
  border-top: 1px solid #2d4056;
  margin: 20px 0;
}
</style>