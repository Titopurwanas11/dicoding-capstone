<template>
  <div class="glass-panel view-container">
    <h2>Semantic Job Search</h2>
    <p class="subtitle">Upload your CV to search for matching jobs in the database semantically.</p>
    
    <div class="form-group">
      <label>Upload CV (PDF/DOCX):</label>
      <input type="file" @change="handleFileSelect" class="input-field file-input" />
    </div>
    
    <button @click="searchJobs" :disabled="loading || !selectedFile" class="btn-primary">
      {{ loading ? 'Searching Matching Jobs...' : 'Search Jobs' }}
    </button>
    
    <div v-if="results.length" class="results">
      <h3>Top Matches Based on your CV</h3>
      <div class="job-list">
        <div v-for="(job, index) in results" :key="job.url" class="job-card">
          <div class="job-rank">#{{ index + 1 }}</div>
          <div class="job-details">
            <a :href="job.url" target="_blank" class="job-title">{{ job.title }}</a>
            <div class="job-company">{{ job.company }} • {{ job.location }}</div>
          </div>
          <div class="job-score">{{ job.score }}% match</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const selectedFile = ref(null)
const loading = ref(false)
const results = ref([])

const handleFileSelect = (e) => { selectedFile.value = e.target.files[0] }

const searchJobs = async () => {
  if (!selectedFile.value) {
    alert("Please select a CV first")
    return
  }
  loading.value = true
  try {
    const formData = new FormData()
    formData.append('cv', selectedFile.value)
    const res = await axios.post('http://localhost:8000/api/jobs/semantic-search', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    results.value = res.data
  } catch (error) {
    console.error(error)
    alert("Failed to search jobs")
  }
  loading.value = false
}
</script>
