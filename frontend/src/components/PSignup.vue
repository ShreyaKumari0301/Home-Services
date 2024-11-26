<template>
  <div class="row">
    <div class="col-md-6 offset-md-3">
      <div>
        <h3>Professional Sign Up</h3>
        <hr />
        <form @submit.prevent="validateForm">
          <!-- Name Field -->
          <div class="form-group">
            <label>Name</label>
            <input type="text" class="form-control" v-model="name" placeholder="Enter your name" required />
          </div>

          <!-- Email Field -->
          <div class="form-group">
            <label>Email</label>
            <input type="email" class="form-control" v-model="email" placeholder="Enter your email" required />
          </div>

          <!-- Password Field -->
          <div class="form-group">
            <label>Password</label>
            <input type="password" class="form-control" v-model="password" placeholder="Enter your password" required />
          </div>

          <!-- Mobile Number Field -->
          <div class="form-group">
            <label>Mobile Number</label>
            <input type="text" class="form-control" v-model="mobileNumber" placeholder="Enter your mobile number" required />
          </div>

          <!-- Pincode Field -->
          <div class="form-group">
            <label>Pincode</label>
             <input 
    type="text" 
    class="form-control" 
    v-model="pincode" 
    placeholder="Enter pincodes (comma-separated for multiple)" 
    required 
  />
  <small class="form-text text-muted">For multiple pincodes, separate them with commas (e.g., 123456,234567)</small>
</div>

          <!-- Service Category Field -->
          <div class="form-group">
            <label>Service Category</label>
            <input type="text" class="form-control" v-model="serviceCategory" placeholder="Enter service category" required />
          </div>

          <!-- Experience Field -->
          <div class="form-group">
            <label>Experience (Years)</label>
            <input type="number" class="form-control" v-model="experience" placeholder="Enter years of experience" required />
          </div>

          <!-- Aadhar Card Field -->
          <div class="form-group">
            <label>Aadhar Card</label>
            <input type="text" class="form-control" v-model="aadharCard" placeholder="Enter your Aadhar card number" required />
          </div>

          <!-- Document Upload Field -->
          <div class="form-group">
            <label>Document</label>
            <input type="file" class="form-control" @change="handleFileUpload" required />
          </div>

          <!-- Submit Button -->
          <div class="my-3">
            <button type="submit" class="btn btn-primary">Sign Up</button>
          </div>
        </form>
      </div>
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
.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
}

.btn-primary {
  width: 100%;
}
</style>