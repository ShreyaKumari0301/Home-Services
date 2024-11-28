<template>
  <div class="main-container">
    <!-- Navigation Bar from AHome -->
    <div class="navigation-bar">
      <div class="nav-header">
        <h2><i>Admin Dashboard</i></h2>
        <div class="nav-buttons">
          <button 
            @click="navigateTo('AHome')"
            :class="{ active: currentRoute === 'AHome' }"
          >Home</button>
          <button 
            @click="navigateTo('AProfs')"
            :class="{ active: currentRoute === 'AProfs' }"
          >Professionals</button>
          <button 
            @click="navigateTo('AUsers')"
            :class="{ active: currentRoute === 'AUsers' }"
          >Users</button>
          <button 
            @click="navigateTo('ARequests')"
            :class="{ active: currentRoute === 'ARequests' }"
          >Service Requests</button>
          <button 
            @click="navigateTo('ASummary')"
            :class="{ active: currentRoute === 'ASummary' }"
          >Summary</button>
          <button @click="logout" class="logout-btn">Logout</button>
        </div>
      </div>
    </div>

    <!-- Content Area with USummary's grid styling -->
    <div class="content-area">
      <div class="charts-container">
        <!-- Category Distribution -->
        <div class="chart-box">
          <h3>Service Category Distribution</h3>
          <canvas ref="categoryChart"></canvas>
        </div>

        <!-- Professional Status -->
        <div class="chart-box">
          <h3>Professional Status Overview</h3>
          <canvas ref="statusChart"></canvas>
        </div>

        <!-- Top Professionals -->
        <div class="chart-box">
          <h3>Top Rated Professionals</h3>
          <canvas ref="topProfsChart"></canvas>
        </div>

        <!-- Rating Distribution -->
        <div class="chart-box">
          <h3>Customer Rating Distribution</h3>
          <canvas ref="ratingChart"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Chart from 'chart.js/auto';

export default {
  name: "ASummary",
  data() {
    return {
      currentRoute: 'ASummary',
      charts: {
        categoryChart: null,
        statusChart: null,
        topProfsChart: null,
        ratingChart: null
      }
    }
  },
  methods: {
    navigateTo(page) {
      if (this.currentRoute !== page) {
        this.$router.push({ name: page });
      }
    },
    logout() {
      localStorage.clear();
      this.$router.push("/login");
    },
    async fetchSummaryData() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/admin/summary', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        console.log("Summary Data:", response.data);
        this.createCharts(response.data);
      } catch (error) {
        console.error('Error fetching summary data:', error);
        if (error.response?.status === 401) {
          this.$router.push('/login');
        }
      }
    },
    createCharts(data) {
      // Clear previous charts if they exist
      Object.values(this.charts).forEach(chart => {
        if (chart) chart.destroy();
      });

      // Category Distribution Pie Chart
      this.charts.categoryChart = new Chart(this.$refs.categoryChart, {
        type: 'pie',
        data: {
          labels: Object.keys(data.category_distribution),
          datasets: [{
            data: Object.values(data.category_distribution),
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: { color: '#e2e8f0' }
            }
          }
        }
      });

      // Professional Status Bar Chart
      if (data.professional_status && this.$refs.statusChart) {
        const statusData = {
          labels: Object.keys(data.professional_status),
          values: Object.values(data.professional_status)
        };

        this.charts.statusChart = new Chart(this.$refs.statusChart, {
          type: 'bar',
          data: {
            labels: statusData.labels,
            datasets: [{
              label: 'Number of Professionals',
              data: statusData.values,
              backgroundColor: [
                '#4CAF50',  // Approved - Green
                '#F44336',  // Blocked - Red
                '#FF9800',  // Pending - Orange
                '#2196F3'   // Rejected - Blue
              ],
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
                grid: {
                  color: '#4a5568'
                },
                ticks: {
                  color: '#e2e8f0',
                  font: {
                    size: 12
                  }
                }
              },
              x: {
                grid: {
                  color: '#4a5568'
                },
                ticks: {
                  color: '#e2e8f0',
                  font: {
                    size: 12
                  }
                }
              }
            },
            plugins: {
              legend: {
                display: false
              },
              title: {
                display: true,
                text: 'Professional Status Distribution',
                color: '#e2e8f0',
                font: {
                  size: 16
                }
              }
            }
          }
        });
      }

      // Top Professionals Bar Chart
      this.charts.topProfsChart = new Chart(this.$refs.topProfsChart, {
        type: 'bar',
        data: {
          labels: data.top_professionals.map(prof => prof.name),
          datasets: [{
            data: data.top_professionals.map(prof => prof.rating),
            backgroundColor: ['#4CAF50', '#2196F3', '#FFC107']
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              max: 5,
              ticks: { color: '#e2e8f0' }
            },
            x: {
              ticks: { color: '#e2e8f0' }
            }
          },
          plugins: {
            legend: { display: false }
          }
        }
      });

      // Rating Distribution Pie Chart
      this.charts.ratingChart = new Chart(this.$refs.ratingChart, {
        type: 'pie',
        data: {
          labels: ['5 Stars', '4 Stars', '3 Stars', '2 Stars', '1 Star'],
          datasets: [{
            data: [5,4,3,2,1].map(rating => data.rating_distribution[rating] || 0),
            backgroundColor: ['#4CAF50', '#8BC34A', '#FFCE56', '#FF9800', '#F44336']
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: { color: '#e2e8f0' }
            }
          }
        }
      });
    }
  },
  mounted() {
    this.fetchSummaryData();
  },
  beforeUnmount() {
    // Cleanup charts when component is destroyed
    Object.values(this.charts).forEach(chart => {
      if (chart) chart.destroy();
    });
  }
};
</script>

<style scoped>
.main-container {
  background-color: #2d3748;
  min-height: 100vh;
  color: white;
  padding: 0;
}

/* AHome's Navigation Bar Styling */
.navigation-bar {
  background: #2d3748;
  padding: 1rem 2rem;
  border-radius: 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 0;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-buttons {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.nav-buttons button {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: #444;
  color: #f8f9fa;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
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

/* USummary's Chart Grid Styling */
.content-area {
  padding: 20px;
  margin-top: 20px;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.chart-box {
  background: #2d3748;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
  height: 300px;
  display: flex;
  flex-direction: column;
}

.chart-box canvas {
  flex: 1;
  width: 100% !important;
  height: 100% !important;
}

.chart-box:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.chart-box h3 {
  text-align: center;
  margin-bottom: 15px;
  color: #f8f9fa;
  font-size: 1rem;
}

@media (max-width: 768px) {
  .nav-buttons {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .charts-container {
    grid-template-columns: 1fr;
    padding: 10px;
  }
  
  .chart-box {
    height: 250px;
  }
}
</style>
