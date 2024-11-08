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

                            <button type="submit" class="register-btn">Register</button>

            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

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
                const response = await axios.post('http://127.0.0.1:5000/login', {
                    email: this.email,
                    password: this.password
                });
                localStorage.setItem('token', response.data.access_token);
                localStorage.setItem('userrole', response.data.userrole);
                localStorage.setItem('name', response.data.username);
                alert("Login Successful");
                if (response.data.access_token && response.data.userrole == 'Admin') {
                    this.$router.push('/admin');
                }
                else if (response.data.access_token && response.data.userrole == 'User') {
                    this.$router.push('/');
                }
            } catch (error) {
                console.error("Login failed", error);
            }
        },
    },
    mounted() {
        if (localStorage.getItem("token")) {
            this.$router.push('/');
        }
    },
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

.login-form {
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

.login-btn {
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
.register-btn {
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 8px;
    background-color: #41933d;
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
