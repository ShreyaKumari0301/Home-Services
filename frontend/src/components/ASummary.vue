<template>
  <div class="summary-container">
    <h2>Service Summary</h2>

    <div class="chart-container">
      <h3>Customer Ratings</h3>
      <BarChart :data="ratingData" :labels="ratingLabels" :colors="ratingColors" />
    </div>

    <div class="chart-container">
      <h3>Requests Summary</h3>
      <BarChart :data="statusData" :labels="statusLabels" :colors="statusColors" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import BarChart from "@/components/BarChart.vue"; // Custom bar chart component

export default {
  name: "ASummary",
  components: { BarChart },
  data() {
    return {
      ratingData: [],
      ratingLabels: ["5 Stars", "4 Stars", "3 Stars", "2 Stars", "1 Star"],
      ratingColors: ["#4CAF50", "#8BC34A", "#CDDC39", "#FFC107", "#F44336"],
      statusData: [],
      statusLabels: ["Completed", "Assigned", "Cancelled"],
      statusColors: ["#4CAF50", "#2196F3", "#F44336"],
    };
  },
  async mounted() {
    try {
      const response = await axios.get("http://127.0.0.1:5000/summary_data");
      const { ratings, statuses } = response.data;

      // Setting data for the rating chart
      this.ratingData = [
        ratings["5"] || 0,
        ratings["4"] || 0,
        ratings["3"] || 0,
        ratings["2"] || 0,
        ratings["1"] || 0,
      ];

      // Setting data for the status chart
      this.statusData = [
        statuses.completed || 0,
        statuses.assigned || 0,
        statuses.cancelled || 0,
      ];
    } catch (error) {
      console.error("Failed to load summary data:", error);
    }
  },
};
</script>

<style>
.summary-container {
  max-width: 800px;
  margin: auto;
  text-align: center;
}

.chart-container {
  margin-bottom: 30px;
}
</style>
