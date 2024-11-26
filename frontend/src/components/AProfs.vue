<template>
  <div class="professionals-dashboard">
    <h2>Professional Management</h2>
    
    <div class="filters">
      <select v-model="statusFilter">
        <option value="">All Status</option>
        <option value="pending">Pending</option>
        <option value="approved">Approved</option>
        <option value="blocked">Blocked</option>
      </select>
      <input 
        v-model="searchQuery" 
        placeholder="Search by name or email..."
        @input="filterProfessionals"
      />
    </div>

    <table class="professionals-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Mobile</th>
          <th>Service Category</th>
          <th>Experience</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="prof in filteredProfessionals" :key="prof.id">
          <td>{{ prof.name }}</td>
          <td>{{ prof.email }}</td>
          <td>{{ prof.mobile_number }}</td>
          <td>{{ prof.service_category }}</td>
          <td>{{ prof.experience }} years</td>
          <td>
            <span :class="'status-' + prof.status">{{ prof.status }}</span>
          </td>
          <td>
            <button 
              v-if="prof.status === 'pending'"
              @click="updateStatus(prof.id, 'approved')"
              class="approve-btn"
            >
              Approve
            </button>
            <button 
              v-if="prof.status === 'approved'"
              @click="updateStatus(prof.id, 'blocked')"
              class="block-btn"
            >
              Block
            </button>
            <button 
              v-if="prof.status === 'blocked'"
              @click="updateStatus(prof.id, 'approved')"
              class="unblock-btn"
            >
              Unblock
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      professionals: [],
      statusFilter: '',
      searchQuery: ''
    }
  },
  computed: {
    filteredProfessionals() {
      return this.professionals.filter(prof => {
        const matchesStatus = !this.statusFilter || prof.status === this.statusFilter;
        const searchLower = this.searchQuery.toLowerCase();
        const matchesSearch = !this.searchQuery || 
          prof.name.toLowerCase().includes(searchLower) ||
          prof.email.toLowerCase().includes(searchLower);
        
        return matchesStatus && matchesSearch;
      });
    }
  },
  methods: {
    async fetchProfessionals() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/admin/professionals', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        this.professionals = response.data;
      } catch (error) {
        console.error('Error fetching professionals:', error);
      }
    },
    async updateStatus(profId, newStatus) {
      try {
        const token = localStorage.getItem('token');
        await axios.put(`http://127.0.0.1:5000/admin/professionals/${profId}/status`, 
          { status: newStatus },
          { headers: { 'Authorization': `Bearer ${token}` }}
        );
        await this.fetchProfessionals();
      } catch (error) {
        console.error('Error updating professional status:', error);
      }
    }
  },
  mounted() {
    this.fetchProfessionals();
  }
}
</script>

<style scoped>
.professionals-dashboard {
  padding: 20px;
}

.filters {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.filters select, .filters input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.professionals-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.professionals-table th,
.professionals-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.status-pending {
  color: #f0ad4e;
}

.status-approved {
  color: #5cb85c;
}

.status-blocked {
  color: #d9534f;
}

button {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  color: white;
}

.approve-btn {
  background-color: #5cb85c;
}

.block-btn {
  background-color: #d9534f;
}

.unblock-btn {
  background-color: #5bc0de;
}

button:hover {
  opacity: 0.9;
}
</style>