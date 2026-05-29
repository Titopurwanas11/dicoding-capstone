<template>
  <div class="glass-panel view-container">
    <h2>Bulk CV Ranking</h2>
    <p class="subtitle">Upload multiple CVs to rank candidates against a job description.</p>
    
    <div class="form-group">
      <label>Upload Candidates (PDF/DOCX):</label>
      <input type="file" multiple @change="handleMultipleFileSelect" class="input-field file-input" />
      
      <!-- Select2 style tag-like display for selected files -->
      <div v-if="selectedFiles.length" class="file-tags-container">
        <div v-for="(file, index) in selectedFiles" :key="file.name" class="file-tag">
          <span class="file-name">{{ file.name }}</span>
          <button type="button" @click="removeFile(index)" class="remove-tag-btn">&times;</button>
        </div>
      </div>
    </div>
    
    <div class="form-group">
      <label>Job Description:</label>
      <textarea v-model="jobDescription" placeholder="Paste the job requirements here..." class="input-field textarea" rows="6"></textarea>
    </div>
    
    <button @click="rankCVs" :disabled="loading || !selectedFiles.length || !jobDescription" class="btn-primary">
      {{ loading ? 'Ranking Candidates...' : 'Rank Candidates' }}
    </button>
    
    <div v-if="rankings.length" class="results">
      <h3>Candidate Rankings</h3>
      <div class="table-container">
        <table class="ranking-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Candidate Name</th>
              <th>Match Score</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in rankings" :key="r.name">
              <td class="rank-col">#{{ r.rank }}</td>
              <td class="name-col">{{ r.name }}</td>
              <td class="score-col">
                <div class="score-bar-container">
                  <div class="score-bar" :style="{ width: r.score + '%' }"></div>
                  <span>{{ r.score }}%</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const selectedFiles = ref([])
const jobDescription = ref('')
const loading = ref(false)
const rankings = ref([])

const handleMultipleFileSelect = (e) => {
  const files = Array.from(e.target.files)
  // Merge unique files
  for (let f of files) {
    if (!selectedFiles.value.some(existing => existing.name === f.name)) {
      selectedFiles.value.push(f)
    }
  }
}

const removeFile = (index) => {
  selectedFiles.value.splice(index, 1)
}

const rankCVs = async () => {
  if (!selectedFiles.value.length || !jobDescription.value) {
    alert("Please upload at least one CV and provide Job Description")
    return
  }
  loading.value = true
  const fd = new FormData()
  for (let f of selectedFiles.value) {
    fd.append('cvs', f)
  }
  fd.append('job_description', jobDescription.value)
  try {
    const res = await axios.post('http://localhost:8000/api/hr/rank', fd)
    rankings.value = res.data
  } catch (error) {
    console.error(error)
    alert("Failed to rank candidates")
  }
  loading.value = false
}
</script>

<style scoped>
.file-tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(3, 105, 161, 0.2);
  border-radius: 8px;
  min-height: 42px;
}

.file-tag {
  display: inline-flex;
  align-items: center;
  background: var(--primary);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
}

.file-name {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.remove-tag-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.1rem;
  margin-left: 0.5rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  height: 100%;
}

.remove-tag-btn:hover {
  color: #EF4444;
}
</style>
