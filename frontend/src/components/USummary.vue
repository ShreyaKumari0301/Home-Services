<template>
  <div class="summary">
    <h2>Service Requests</h2>
    <canvas id="serviceRequestsChart"></canvas>
  </div>
</template>

<script>
import { Bar } from 'chart.js';

export default {
  name: 'Summary',
  data() {
    return {
      chart: null,
      requestData: {
        Requested: 0,
        Closed: 0,
        Assigned: 0,
      }
    };
  },
  async mounted() {
    await this.fetchSummaryData();
    this.renderChart();
  },
  methods: {
    async fetchSummaryData() {
      try {
        const response = await fetch('/api/summary', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (response.ok) {
          this.requestData = await response.json();
        }
      } catch (error) {
        console.error("Error fetching summary data:", error);
      }
    },
    renderChart() {
      const ctx = document.getElementById('serviceRequestsChart').getContext('2d');
      this.chart = new Bar(ctx, {
        type: 'bar',
        data: {
          labels: ['Requested', 'Closed', 'Assigned'],
          datasets: [{
            label: 'Service Requests',
            data: [this.requestData.Requested, this.requestData.Closed, this.requestData.Assigned],
            backgroundColor: ['#3498db', '#2ecc71', '#e74c3c'],
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: { beginAtZero: true }
          }
        }
      });
    }
  }
};
</script>

<style scoped>
.summary {
  text-align: center;
}
canvas {
  max-width: 600px;
  margin: auto;
}
</style>
