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
