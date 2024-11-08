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
            <input
              type="text"
              class="form-control"
              v-model="name"
              placeholder="Enter your name"
              required
            />
          </div>

          <!-- Email Field -->
          <div class="form-group">
            <label>Email</label>
            <input
              type="email"
              class="form-control"
              v-model="email"
              placeholder="Enter your email"
              required
            />
          </div>

          <!-- Password Field -->
          <div class="form-group">
            <label>Password</label>
            <input
              type="password"
              class="form-control"
              v-model="password"
              placeholder="Enter your password"
              required
            />
          </div>

          <!-- Mobile Number Field -->
          <div class="form-group">
            <label>Mobile Number</label>
            <input
              type="text"
              class="form-control"
              v-model="mobileNumber"
              placeholder="Enter your mobile number"
              required
            />
          </div>

          <!-- Experience Field -->
          <div class="form-group">
            <label>Experience</label>
            <input
              type="number"
              class="form-control"
              v-model="experience"
              placeholder="Enter your experience in years"
              required
            />
          </div>

          <!-- PinCode Field -->
          <div class="form-group">
            <label>PinCode</label>
            <input
              type="text"
              class="form-control"
              v-model="pincode"
              placeholder="Enter your pincode"
              required
            />
          </div>

          <!-- Service Category Dropdown -->
          <div class="form-group">
            <label>Service Category</label>
            <select class="form-control" v-model="serviceCategory" required>
              <option value="salon-women">Salon for Women</option>
              <option value="salon-men">Salon for Men</option>
              <option value="ac-appliance">AC and Appliance Servicing</option>
              <option value="painting">Painting</option>
              <option value="electrician">Electrician</option>
              <option value="carpenter">Carpenters</option>
            </select>
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
export default {
  name: "PSignup",
  data() {
    return {
      name: "",
      email: "",
      password: "",
      mobileNumber: "",
      experience: null,
      pincode: "",
      serviceCategory: "",
    };
  },
  methods: {
    validateForm() {
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
      alert("Form is valid. Submitting...");
      // Add further submission logic here, if necessary.
    },
  },
};
</script>

<style>
h3 {
  color: purple;
}
</style>
