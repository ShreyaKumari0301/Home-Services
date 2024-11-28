<template>
  <div class="main-container">
    <div class="navigation-bar">
      <div class="nav-header">
        <h2><i>My Summary</i></h2>
        <div class="nav-buttons">
          <button 
            @click="navigateTo('UHome')"
            :class="{ active: currentRoute === 'UHome' }"
          >Home</button>
          <button 
            @click="navigateTo('UOrders')"
            :class="{ active: currentRoute === 'UOrders' }"
          >Orders</button>
          <button 
            @click="navigateTo('UProfile')"
            :class="{ active: currentRoute === 'UProfile' }"
          >Profile</button>
          <button 
            @click="navigateTo('USummary')"
            :class="{ active: currentRoute === 'USummary' }"
          >Summary</button>
          <button @click="logout" class="logout-btn">Logout</button>
        </div>
      </div>
    </div>
    
    <div class="content-area">
      <div class="charts-container">
        <div class="chart-box">
          <h3>Services by Category</h3>
          <canvas ref="categoryChart"></canvas>
        </div>
        <div class="chart-box">
          <h3>Service Request Status</h3>
          <canvas ref="statusChart"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart } from 'chart.js/auto';
import axios from 'axios';

export default {
  name: 'USummary',
  data() {
    return {
      categoryChart: null,
      statusChart: null,
      currentRoute: 'USummary'
    };
  },
  methods: {
    navigateTo(page) {
      this.$router.push({ name: page });
    },
    logout() {
      localStorage.clear();
      this.$router.push("/login");
    },
    async fetchSummaryData() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/user/summary', {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        this.renderCharts(response.data);
      } catch (error) {
        console.error("Error fetching summary data:", error);
      }
    },
    renderCharts(data) {
      // Destroy existing charts if they exist
      if (this.categoryChart) this.categoryChart.destroy();
      if (this.statusChart) this.statusChart.destroy();

      // Category Pie Chart
      const categoryCtx = this.$refs.categoryChart.getContext('2d');
      this.categoryChart = new Chart(categoryCtx, {
        type: 'pie',
        data: {
          labels: Object.keys(data.category_stats),
          datasets: [{
            data: Object.values(data.category_stats),
            backgroundColor: [
              '#FF6384',
              '#36A2EB',
              '#FFCE56',
              '#4BC0C0',
              '#9966FF'
            ]
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'bottom'
            }
          }
        }
      });

      // Status Bar Chart
      const statusCtx = this.$refs.statusChart.getContext('2d');
      this.statusChart = new Chart(statusCtx, {
        type: 'bar',
        data: {
          labels: Object.keys(data.status_stats),
          datasets: [{
            label: 'Number of Requests',
            data: Object.values(data.status_stats),
            backgroundColor: [
              '#FF6384',
              '#36A2EB',
              '#4BC0C0',
              '#FF9F40'
            ]
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1
              }
            }
          }
        }
      });
    }
  },
  mounted() {
    this.fetchSummaryData();
  }
};
</script>

<style scoped>
.main-container {
  background-color: #f5f5f5;
  padding: 30px;
  min-height: 100vh;
}

.navigation-bar {
  background: white;
  padding: 1rem 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-buttons {
  display: flex;
  gap: 15px;
}

.nav-buttons button {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background: #f8f9fa;
  color: #495057;
  cursor: pointer;
  transition: all 0.3s ease;
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

.content-area {
  margin-top: 20px;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.chart-box {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.chart-box h3 {
  text-align: center;
  margin-bottom: 20px;
  color: #212529;
}

@media (max-width: 768px) {
  .main-container {
    padding: 15px;
  }
  
  .nav-buttons {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
