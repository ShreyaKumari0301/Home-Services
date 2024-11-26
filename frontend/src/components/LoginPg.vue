<template>
    <div class="container">
        <div class="login-form">
            <h3>Login</h3>
            <hr />
            <form @submit.prevent="handleSubmit">
                <div class="form-group">
                    <label>Email</label>
                    <input type="text" v-model="email" class="form-control" placeholder="Enter your email" required />
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" v-model="password" class="form-control" placeholder="Enter your password" required />
                </div>
                <button type="submit" class="login-btn">Login</button>
               <router-link to="/signup"> <button type="button" class="register-btn">Register</button></router-link>
            </form>
        </div>
    </div>
</template>
<script>
import axios from "axios";

export default {
  name: "LoginPg",
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async handleSubmit() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/login", {
          email: this.email,
          password: this.password,
        });

        // Destructure response data
        const { access_token, userrole } = response.data;

        // Check if token and role exist
        if (access_token && userrole) {
          // Store data in localStorage
          localStorage.setItem("token", access_token);
          localStorage.setItem("userrole", userrole);
          localStorage.setItem("email", this.email);

          // Redirect based on user role
          switch (userrole) {
            case "Admin":
              this.$router.push("/admin");
              break;
            case "User":
              this.$router.push("/");
              break;
            case "Professional":
              this.$router.push("/professional");
              break;
            default:
              console.error("Unknown user role.");
              alert("Unknown role. Please contact support.");
          }
        } else {
          console.error("Token or role is missing in response.");
          alert("Login failed. Please try again.");
        }
      } catch (error) {
        console.error("Login error:", error.response?.data?.message || error.message);
        alert("Invalid credentials or server issue. Please try again.");
      }
    },
  },
  mounted() {
    const token = localStorage.getItem("token");
    const userrole = localStorage.getItem("userrole");

    // Redirect based on stored token and user role
    if (token) {
      switch (userrole) {
        case "Admin":
          this.$router.push("/admin");
          break;
        case "User":
          this.$router.push("/");
          break;
        case "Professional":
          this.$router.push("/professional");
          break;
        default:
          console.error("Invalid user role in localStorage.");
      }
    }
  },
};
</script>


<style>
body {
    background-color: #071228;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    margin: 0;
    font-family: Arial, sans-serif;
    color: white;
}

.container {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
}

.login-form {
    background-color: #2d3748;
    padding: 30px;
    border-radius: 15px;
    width: 100%;
    max-width: 400px;
    text-align: center;
    color:white
}
.login-form label{
    color:white;
}
.login-form h3 {
    margin-bottom: px;
    font-size: 24px;
    color: white;

}

.form-group {
    margin-bottom: 15px;
    text-align: left;
}


.form-control {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-sizing: border-box;
    margin-top: 5px;
}

.login-btn {
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 8px;
    color: white;
    font-size: 16px;
    cursor: pointer;
    background-color: #4299e1;
    transition: background-color 0.3s ease;
    margin-top: 20px;
}
.register-btn {
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 8px;
    background-color: #4299e1;
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-top: 20px;
}

.login-btn:hover {
    background-color: #0056b3;
}
</style>
