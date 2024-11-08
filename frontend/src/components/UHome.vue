<template>
  <div id="app">
    <h1>{{name}}</h1>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">Home Services</a>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="#">Home</a>
          </li>
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              id="categoryDropdown"
              role="button"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              Categories
            </a>
            <div class="dropdown-menu" aria-labelledby="categoryDropdown">
              <a
                v-for="cat in categories"
                :key="cat"
                class="dropdown-item"
                href="#"
                @click="selectCategory(cat)"
              >
                {{ cat }}
              </a>
            </div>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Summary</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Add to Cart</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Records</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Profile</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Logout</a>
          </li>
        </ul>
         
        <form class="form-inline my-2 my-lg-0">
          <input
            class="form-control mr-sm-2"
            type="search"
            placeholder="Search"
            aria-label="Search"
          />
          <button class="btn btn-outline-success my-2 my-sm-0" type="submit">
            Search
          </button>
         
        </form>
      </div>
    </nav>
    
    <div class="container">
      <!-- Render router views or specific components here -->
      <router-view />
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UHome",
  data() {
    return {
      categories: [],
      name: "Shreya",
    };
  },
  methods: {
    async fetchCategories() {
      try {
        const token = localStorage.getItem("token");
        const auth_token = `Bearer ${token}`;
        const config = {
            headers: {
              'Content-Type': 'application/json',
              'Authorization': auth_token
            }
          }
        const response = await axios.get("http://127.0.0.1:5000/categories", config)
        this.categories = response.data.categories;
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
    },
    selectCategory(category) {
      // Handle category selection
      console.log(`Selected category: ${category}`);
    },
  },
  mounted() {
    if (localStorage.getItem("token")) {
      // User is logged in, fetch categories
      this.fetchCategories();
    } else {
      // Redirect to login page
      this.$router.push("/login");
    }
    
  },
};
</script>

<style>
/* Global styles */
</style>
