<template>
  <div class="main-container">
    <!-- Navigation Bar -->
    <div class="navigation-bar">
      <div class="nav-header">
        <h2><i>Professional Management</i></h2>
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

    <div class="content-area">
      <div class="filters">
        <input 
          v-model="searchQuery" 
          placeholder="Search by name, email, or category..."
          class="search-input"
          @input="filterProfessionals"
        />
        <select 
          v-model="statusFilter"
          class="status-select"
          @change="filterProfessionals"
        >
          <option value="">All Status</option>
          <option value="Pending">Pending</option>
          <option value="Approved">Approved</option>
          <option value="Blocked">Blocked</option>
          <option value = "Reejected">Rejecteed</option>
        </select>
      </div>

      <div class="table-container">
        <table class="professionals-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Mobile</th>
              <th>Category</th>
              <th>Experience</th>
              <th>Rating</th>
              <th>Status</th>
              <th>Document</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="professional in filteredProfessionals" :key="professional.id">
              <td>{{ professional.name }}</td>
              <td>{{ professional.email }}</td>
              <td>{{ professional.mobile_number }}</td>
              <td>{{ professional.service_category }}</td>
              <td>{{ professional.experience }} years</td>
              <td>{{ professional.ratings }} ⭐</td>
              <td>
                <span :class="'status-' + professional.status.toLowerCase()">
                  {{ professional.status }}
                </span>
              </td>
              <td>
                <button 
                  @click="viewDocument(professional.id)" 
                  class="view-doc-btn"
                >
                  View Document
                </button>
              </td>
              <td class="actions-cell">
                <div class="action-buttons">
                  <!-- For Pending professionals -->
                  <button 
                    v-if="professional.status.toLowerCase() === 'pending'"
                    @click="updateStatus(professional.id, 'approved')"
                    class="action-btn approve-btn"
                  >
                    Approve
                  </button>
                  <button 
                    v-if="professional.status.toLowerCase() === 'pending'"
                    @click="updateStatus(professional.id, 'rejected')"
                    class="action-btn reject-btn"
                  >
                    Reject
                  </button>

                  <!-- For Approved professionals -->
                  <button 
                    v-if="professional.status.toLowerCase() === 'approved'"
                    @click="updateStatus(professional.id, 'blocked')"
                    class="action-btn block-btn"
                  >
                    Block
                  </button>

                  <!-- For Blocked professionals -->
                  <button 
                    v-if="professional.status.toLowerCase() === 'blocked'"
                    @click="updateStatus(professional.id, 'approved')"
                    class="action-btn unblock-btn"
                  >
                    Unblock
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Add this modal component -->
  <div v-if="showDocModal" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>Document View</h3>
        <button @click="closeModal" class="close-modal">&times;</button>
      </div>
      <iframe 
        v-if="documentUrl" 
        :src="documentUrl" 
        class="document-frame"
        type="application/pdf"
      ></iframe>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AProfs',
  data() {
    return {
      professionals: [],
      statusFilter: '',
      searchQuery: '',
      currentRoute: 'AProfs',
      showDocModal: false,
      documentUrl: null
    }
  },
  computed: {
    filteredProfessionals() {
      return this.professionals.filter(professional => {
        const matchesStatus = !this.statusFilter || 
          professional.status.toLowerCase() === this.statusFilter.toLowerCase();
        
        const searchLower = this.searchQuery.toLowerCase();
        const matchesSearch = !this.searchQuery || 
          professional.name.toLowerCase().includes(searchLower) ||
          professional.email.toLowerCase().includes(searchLower) ||
          professional.service_category.toLowerCase().includes(searchLower);
        
        return matchesStatus && matchesSearch;
      });
    }
  },
  methods: {
    navigateTo(page) {
      this.$router.push({ name: page });
    },
    logout() {
      localStorage.clear();
      this.$router.push("/login");
    },
    async fetchProfessionals() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/admin/professionals', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        console.log('Professionals data:', response.data);
        this.professionals = response.data;
      } catch (error) {
        console.error('Error fetching professionals:', error);
        if (error.response?.status === 401) {
          this.$router.push('/login');
        }
      }
    },
    async updateStatus(profId, newStatus) {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          this.$router.push('/login');
          return;
        }

        console.log(`Updating status for professional ${profId} to ${newStatus}`);

        const response = await axios.put(
          `http://127.0.0.1:5000/admin/professionals/${profId}/status`,
          { status: newStatus.toLowerCase() },
          { 
            headers: { 
              'Authorization': `Bearer ${token}`
            }
          }
        );

        if (response.status === 200) {
          await this.fetchProfessionals();
          alert('Professional status updated successfully');
        }
      } catch (error) {
        console.error('Error updating professional status:', error);
        alert(`Error: ${error.response?.data?.message || 'Failed to update status'}`);
      }
    },
    async viewDocument(profId) {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(
          `http://127.0.0.1:5000/admin/professionals/${profId}/document`,
          {
            headers: { Authorization: `Bearer ${token}` },
            responseType: 'blob'
          }
        );
        
        const blob = new Blob([response.data], { type: 'application/pdf' });
        this.documentUrl = URL.createObjectURL(blob);
        this.showDocModal = true;
      } catch (error) {
        console.error('Error fetching document:', error);
        alert('Error viewing document');
      }
    },
    closeModal() {
      this.showDocModal = false;
      if (this.documentUrl) {
        URL.revokeObjectURL(this.documentUrl);
        this.documentUrl = null;
      }
    }
  },
  mounted() {
    this.fetchProfessionals();
  }
};
</script>

<style scoped>
.main-container {
    background-color: #2d3748;
  min-height: 100vh;
  padding: 20px;
  color: white;
}

.navigation-bar {
  background: #2d3748;
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
  background: #444;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-buttons button.active {
  background: #0d6efd;
  color: white;
}

.nav-buttons button.logout-btn {
background: #dc3545 !important;
  color: white !important;
}

.content-area {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.filters {
    display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.filters input, .filters select {
 padding: 10px;
  border: 1px solid #4a5568;
  border-radius: 8px;
  background: #2d3748;
  color: white;
  flex: 1;
}
.search-input::placeholder {
  color: #a0aec0;
}
.table-container {
    background: #ffffff0d;
  border-radius: 12px;
  padding: 20px;
  overflow-x: auto;
  width: 100%;
}

.professionals-table {
  width: 100%;
  border-collapse: collapse;
  color: #e2e8f0;
  min-width: 1000px;
}

.professionals-table th,
.professionals-table td {
  padding: 12px;
  text-align: left;
border-bottom: 1px solid #4a5568;
}

.status-pending {
  color: #ffd700;
}

.status-approved {
  color: #48bb78;
}

.status-blocked {
  color: #f56565;
}

.status-rejected {
  color: #dc3545;
}

button {
 padding: 6px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  color: white;
  transition: all 0.3s ease;
}

.approve-btn {
  background-color: #28a745;
}

.block-btn {
  background-color:  #f56565;
}

.unblock-btn {
  background-color: #48bb78;
}

button:hover, .unblock-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.view-doc-btn {
  padding: 6px 12px;
  background-color: #4a5568;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-doc-btn:hover {
  background-color: #2d3748;
  transform: translateY(-1px);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #2d3748;
  padding: 20px;
  border-radius: 12px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.close-modal {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: white;
}

.document-frame {
  width: 100%;
  height: 80vh;
  border: none;
  background: white;
}

.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  color: white;
  white-space: nowrap;
  min-width: 80px;
}

.approve-btn {
  background-color: #28a745;
}

.block-btn {
  background-color: #dc3545;
}

.unblock-btn {
  background-color: #17a2b8;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  opacity: 0.9;
}

.reject-btn {
  background-color: #dc3545;
}

.status-Pending {
  color: #ffd700;
}

.status-Approved {
  color: #48bb78;
}

.status-Blocked {
  color: #f56565;
}

.status-Rejected {
  color: #dc3545;
}

.professionals-table td {
  padding: 12px;
  vertical-align: middle;
}

.actions-cell {
  min-width: 200px; /* Ensure enough space for buttons */
  padding: 8px !important;
}

.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: flex-start;
}

.action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  color: white;
  min-width: 80px;
  display: inline-block; /* Add this */
}

.approve-btn {
  background-color: #28a745;
}

.reject-btn {
  background-color: #dc3545;
}

.block-btn {
  background-color: #dc3545;
}

.unblock-btn {
  background-color: #17a2b8;
}

/* Make sure table cells have proper padding */
.professionals-table td {
  padding: 12px;
  vertical-align: middle;
  white-space: nowrap;
}

/* Add hover effect to buttons */
.action-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

/* Make sure the table container allows horizontal scroll */
.table-container {
  overflow-x: auto;
  margin: 20px 0;
  background: #ffffff0d;
  border-radius: 12px;
  padding: 20px;
}

.professionals-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 1200px; /* Ensure table doesn't get too cramped */
}
</style>