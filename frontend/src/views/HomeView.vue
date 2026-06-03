<template>
  <div class="home-container">
    <div class="glass-panel hero">
      <h1>Welcome to CV Matcher Pro</h1>
      <p>Your intelligent assistant for job matching and CV analysis.</p>
    </div>

    <div class="glass-panel feature-group">
      <div class="accordion-header" @click="jobSeekerOpen = !jobSeekerOpen">
        <h2>Job Seeker Features</h2>
        <span class="icon">{{ jobSeekerOpen ? '▲' : '▼' }}</span>
      </div>
      <div class="accordion-content" v-show="jobSeekerOpen">
        <router-link to="/jobseeker/scrape" class="feature-card">
          <h3>Scrape & Find Matches</h3>
          <p>Find top job matches from LinkedIn based on your CV.</p>
        </router-link>
        <router-link to="/jobseeker/analyze" class="feature-card">
          <h3>Detailed CV-JD Analysis</h3>
          <p>See exactly which skills you match and which you are missing.</p>
        </router-link>
        <router-link to="/jobseeker/search" class="feature-card">
          <h3>Semantic Job Search</h3>
          <p>Search for jobs using natural language queries.</p>
        </router-link>
      </div>
    </div>

    <div class="glass-panel feature-group">
      <div class="accordion-header" @click="hrOpen = !hrOpen">
        <h2>HR Features</h2>
        <span class="icon">{{ hrOpen ? '▲' : '▼' }}</span>
      </div>
      <div class="accordion-content" v-show="hrOpen">
        <router-link to="/hr/rank" class="feature-card">
          <h3>Bulk CV Ranking</h3>
          <p>Upload multiple CVs and rank them against a job description.</p>
        </router-link>
        <router-link to="/hr/cluster" class="feature-card">
          <h3>Candidate Clustering</h3>
          <p>Automatically group candidates into talent clusters by skills.</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const jobSeekerOpen = ref(true)
const hrOpen = ref(true)
</script>

<style scoped>
.home-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.hero {
  text-align: center;
  margin-bottom: 2rem;
  padding: 3rem 2rem;
}

.hero h1 {
  color: #0369A1;
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature-group {
  margin-bottom: 1.5rem;
  padding: 0;
  overflow: hidden;
}

.accordion-header {
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.4);
  transition: background 0.3s ease;
}

.accordion-header:hover {
  background: rgba(255, 255, 255, 0.6);
}

.accordion-header h2 {
  margin: 0;
  color: #0C4A6E;
  font-size: 1.5rem;
}

.accordion-content {
  padding: 1.5rem;
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

.feature-card {
  display: block;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  background: rgba(255, 255, 255, 0.8);
  box-shadow: 0 10px 25px rgba(3, 105, 161, 0.1);
}

.feature-card h3 {
  color: #0369A1;
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.feature-card p {
  color: #475569;
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.5;
}
</style>
