<template>
  <div class="row">
    <div class="col-md-6 offset-md-3">
      <div>
        <h3>Sign Up</h3>
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

          <!-- Address Field -->
          <div class="form-group">
            <label>Address</label>
            <input type="text" class="form-control" v-model="address" placeholder="Enter your address" required />
          </div>

          <!-- PinCode Field -->
          <div class="form-group">
            <label>PinCode</label>
            <input type="text" class="form-control" v-model="pincode" placeholder="Enter your pincode" required />
          </div>

          <!-- Submit Button -->
          <div class="my-3">
            <button type="submit" class="btn btn-primary">
              Sign Up
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "SignUp",
  data() {
    return {
      name: "",
      email: "",
      password: "",
      mobileNumber: "",
      address: "",
      pincode: "",
    };
  },
  methods: {
    async validateForm() {
      console.log(this.name, this.email, this.password, this.mobileNumber, this.address, this.pincode);
      // Validate mobile number and pincode
      const mobileNumberPattern = /^\d{10}$/;
      const pincodePattern = /^\d{6}$/;

      if (!mobileNumberPattern.test(this.mobileNumber)) {
        alert("Mobile number must be exactly 10 digits.");
        return;
      }

      if (!pincodePattern.test(this.pincode)) {
        alert("Pincode must be exactly 6 digits.");
        return;
      }

      // Proceed with form submission if validation passes
      // alert("Form is valid. Submitting...");
       try {
                const response = await axios.post('http://127.0.0.1:5000/register', {
                    email: this.email,
                    password: this.password,
                    name: this.name,
                    mobile_number: this.mobileNumber,
                    address: this.address,
                    pincode: this.pincode
                });
                console.log("RegistrationAPI successful", response.data);
                if (response.status == 201) {
                  alert(response.data.message)
                      console.log(response)
                      this.$router.push({ name: 'LoginPg' })
                  }
                // Handle success, e.g., store token, redirect, etc.
            } catch (error) {
                console.error("Login failed", error);
                // Handle error, e.g., display error message
            }
      // Add further submission logic here, if necessary.
    },
  },
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
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background-color: white; /* White background */
  color: black; /* Black text */
  transition: all 0.3s ease;
  font-size: 14px;
}

.form-control:hover {
  border-color: #3182ce; /* Light blue border on hover */
}

.form-control:focus {
  outline: none;
  border-color: #4299e1; /* Blue border on focus */
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.3); /* Subtle focus shadow */
}

.file-input {
  padding: 8px;
  background-color: white;
  color: black;
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
