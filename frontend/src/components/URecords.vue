<template>
  <div class="container mt-4">
    <h2>Your Bookings</h2>

    <!-- Assigned Bookings Section -->
    <h3>Assigned Bookings</h3>
    <div v-if="assignedBookings.length > 0" class="list-group mb-4">
      <div v-for="booking in assignedBookings" :key="booking.id" class="list-group-item">
        <div class="d-flex justify-content-between align-items-center">
          <h5>{{ booking.service.name }}</h5>
          <span>{{ formatDate(booking.booking_date) }}</span>
        </div>
        <p>Category: {{ booking.service.category }}</p>
        <p>Assigned Professional: {{ booking.professional.name }} (Rating: {{ booking.professional.rating }})</p>
        <p>Phone: {{ booking.professional.phone }}</p>
        <div class="mt-2">
          <button @click="previewBooking(booking)" class="btn btn-primary btn-sm">Preview</button>
          <button @click="rescheduleBooking(booking)" class="btn btn-warning btn-sm">Reschedule</button>
        </div>
      </div>
    </div>

    <!-- Completed Bookings Section -->
    <h3>Completed Bookings</h3>
    <div v-if="completedBookings.length > 0" class="list-group mb-4">
      <div v-for="booking in completedBookings" :key="booking.id" class="list-group-item">
        <div class="d-flex justify-content-between align-items-center">
          <h5>{{ booking.service.name }}</h5>
          <span>{{ formatDate(booking.booking_date) }}</span>
        </div>
        <div class="mt-2">
          <button @click="previewBooking(booking)" class="btn btn-primary btn-sm">Preview</button>
          <button v-if="showRatingOption(booking.booking_date)" @click="rateBooking(booking)" class="btn btn-success btn-sm">Rate</button>
        </div>
      </div>
    </div>

    <!-- Preview Modal -->
    <b-modal v-model="isPreviewModalOpen" title="Booking Details" @ok="closePreviewModal">
      <div v-if="selectedBooking">
        <p>Service: {{ selectedBooking.service.name }}</p>
        <p>Quantity: {{ selectedBooking.quantity }}</p>
        <p>Expected Time: {{ selectedBooking.service.time_required }} hours</p>
        <p>Fare: Rs. {{ selectedBooking.service.price * selectedBooking.quantity }}</p>
      </div>
    </b-modal>

    <!-- Reschedule Modal -->
    <b-modal v-model="isRescheduleModalOpen" title="Reschedule Booking" @ok="confirmReschedule">
      <label for="reschedule-date">Date:</label>
      <input type="date" id="reschedule-date" v-model="rescheduleDate" class="form-control" />
      
      <label for="reschedule-time" class="mt-2">Time:</label>
      <select id="reschedule-time" v-model="rescheduleTime" class="form-control">
        <option v-for="time in availableTimes" :key="time" :value="time">{{ time }}</option>
      </select>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';

export default {
  data() {
    return {
      assignedBookings: [],
      completedBookings: [],
      selectedBooking: null,
      isPreviewModalOpen: false,
      isRescheduleModalOpen: false,
      rescheduleDate: '',
      rescheduleTime: '',
      availableTimes: ['7:00 AM', '9:00 AM', '11:00 AM', '1:00 PM', '3:00 PM', '5:00 PM', '7:00 PM'],
    };
  },
  created() {
    this.fetchBookings();
  },
  methods: {
    async fetchBookings() {
      try {
        const response = await axios.get('/api/service_requests');
        const bookings = response.data;
        this.assignedBookings = bookings.filter(b => b.status === 'Assigned' || b.status === 'Requested');
        this.completedBookings = bookings.filter(b => b.status === 'Completed');
      } catch (error) {
        console.error("Failed to fetch bookings:", error);
      }
    },
    previewBooking(booking) {
      this.selectedBooking = booking;
      this.isPreviewModalOpen = true;
    },
    closePreviewModal() {
      this.isPreviewModalOpen = false;
      this.selectedBooking = null;
    },
    rescheduleBooking(booking) {
      this.selectedBooking = booking;
      this.isRescheduleModalOpen = true;
    },
    async confirmReschedule() {
      try {
        await axios.put(`/api/service_requests/${this.selectedBooking.id}`, {
          new_booking_date: `${this.rescheduleDate} ${this.rescheduleTime}`
        });
        this.isRescheduleModalOpen = false;
        alert('Booking rescheduled successfully');
        this.fetchBookings();
      } catch (error) {
        console.error("Failed to reschedule booking:", error);
      }
    },
    showRatingOption(bookingDate) {
      const twoDaysAfterBooking = new Date(bookingDate);
      twoDaysAfterBooking.setDate(twoDaysAfterBooking.getDate() + 2);
      return new Date() >= twoDaysAfterBooking;
    },
    formatDate(date) {
      return new Date(date).toLocaleString();
    },
  },
};
</script>

