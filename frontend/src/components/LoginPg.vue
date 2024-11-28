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
                <div class="register-options">
                    <router-link to="/signup">
                        <button type="button" class="register-btn user">Register as User</button>
                    </router-link>
                    <router-link to="/psignup">
                        <button type="button" class="register-btn professional">Register as Professional</button>
                    </router-link>
                </div>
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

        const { access_token, userrole } = response.data;

        if (access_token && userrole) {
          localStorage.setItem("token", access_token);
          localStorage.setItem("userrole", userrole);
          localStorage.setItem("email", this.email);

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
        }
      } catch (error) {
        console.error("Login error:", error);
        
        if (error.response?.status === 403) {
          alert(error.response.data.message);
        } else if (error.response?.status === 401) {
          alert("Invalid credentials. Please try again.");
        } else {
          alert("An error occurred. Please try again later.");
        }
      }
    }
  },
  mounted() {
    const token = localStorage.getItem("token");
    const userrole = localStorage.getItem("userrole");

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
    background-color: #1a2942;  /* Changed to a slightly lighter shade of dark blue */
    padding: 30px;
    border-radius: 15px;
    width: 100%;
    max-width: 400px;
    text-align: center;
    color: white;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.login-form label {
    color: white;
    font-weight: 500;
    margin-bottom: 5px;
    display: block;
    text-align: left;
}

.login-form h3 {
    margin-bottom: 20px;
    font-size: 24px;
    color: white;
}

.form-group {
    margin-bottom: 20px;
    text-align: left;
}

.form-control {
    width: 100%;
    padding: 12px;
    border: 1px solid #2d4056;  /* Darker border color */
    border-radius: 8px;
    box-sizing: border-box;
    margin-top: 5px;
    background-color: #2d4056;  /* Slightly lighter than form background */
    color: white;
    transition: all 0.3s ease;
}

.form-control:focus {
    outline: none;
    border-color: #4299e1;
    box-shadow: 0 0 0 2px rgba(66, 153, 225, 0.2);
}

.login-btn {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 8px;
    color: white;
    font-size: 16px;
    cursor: pointer;
    background-color: #4299e1;
    transition: all 0.3s ease;
    margin-bottom: 20px;
}

.register-options {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 10px;
}

.register-btn {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 8px;
    color: white;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.register-btn.user {
    background-color: #48bb78;  /* Green color */
}

.register-btn.professional {
    background-color: #805ad5;  /* Purple color */
}

.login-btn:hover,
.register-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.login-btn:hover {
    background-color: #3182ce;
}

.register-btn.user:hover {
    background-color: #38a169;
}

.register-btn.professional:hover {
    background-color: #6b46c1;
}

</style>

