<template>
  <div class="summary-section">
    <!-- Stat Cards Row -->
    <div class="summary-cards-row">
      <div class="mini-stat-card sub-glass-card">
        <div class="stat-icon-wrapper primary-bg">👥</div>
        <div class="stat-content">
          <span class="stat-label">Total Candidates</span>
          <span class="stat-number text-primary">{{ totalCandidates }}</span>
        </div>
      </div>

      <div class="mini-stat-card sub-glass-card">
        <div class="stat-icon-wrapper success-bg">🧩</div>
        <div class="stat-content">
          <span class="stat-label">Total Clusters</span>
          <span class="stat-number text-success">{{ totalClusters }}</span>
        </div>
      </div>

      <div class="mini-stat-card sub-glass-card">
        <div class="stat-icon-wrapper info-bg">👑</div>
        <div class="stat-content">
          <span class="stat-label">Largest Group</span>
          <span class="stat-number text-info">{{ largestClusterSize }} Candidates</span>
        </div>
      </div>
    </div>

    <!-- Section 6 — Cluster Highlight -->
    <div class="largest-group-highlight glass-panel" v-if="largestClusterName">
      <div class="largest-group-badge">
        <span>🏆 Largest Talent Group</span>
      </div>
      <div class="highlight-content">
        <h3 class="highlight-title">{{ largestClusterName }}</h3>
        <p class="highlight-desc">
          This group contains the largest concentration of candidates, indicating a strong pool of talent aligned with these skill sets.
        </p>
        <div class="highlight-stats">
          <span class="count-num">{{ largestClusterSize }}</span>
          <span class="count-lbl">Candidate Profiles</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  totalCandidates: {
    type: Number,
    required: true
  },
  totalClusters: {
    type: Number,
    required: true
  },
  largestClusterName: {
    type: String,
    default: ''
  },
  largestClusterSize: {
    type: Number,
    default: 0
  }
})
</script>

<style scoped>
.summary-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Stat Cards Row */
.summary-cards-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.mini-stat-card {
  display: flex;
  align-items: center;
  gap: 1.2rem;
  padding: 1.2rem 1.6rem;
  border-radius: 24px;
}

.sub-glass-card {
  background: rgba(255, 255, 255, 0.45);
  border: 1px solid var(--glass-border);
  box-shadow: 0 8px 32px rgba(15, 23, 42, 0.015);
}

.stat-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.35rem;
  box-shadow: 0 4px 10px rgba(15, 23, 42, 0.03);
}

.primary-bg {
  background-color: rgba(14, 165, 233, 0.12);
  border: 1px solid rgba(14, 165, 233, 0.22);
}

.success-bg {
  background-color: rgba(34, 197, 94, 0.12);
  border: 1px solid rgba(34, 197, 94, 0.22);
}

.info-bg {
  background-color: rgba(99, 102, 241, 0.12);
  border: 1px solid rgba(99, 102, 241, 0.22);
}

.text-primary {
  color: var(--primary-dark);
}

.text-success {
  color: #16A34A;
}

.text-info {
  color: var(--indigo);
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 0.78rem;
  font-weight: 800;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-number {
  font-size: 1.55rem;
  font-weight: 900;
  line-height: 1.2;
}

/* Highlight Card Style */
.largest-group-highlight {
  padding: 2.2rem;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.72);
  border: 2.5px solid rgba(14, 165, 233, 0.4);
  box-shadow: 0 20px 50px rgba(14, 165, 233, 0.14), var(--shadow-soft);
  position: relative;
  overflow: visible;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.largest-group-highlight:hover {
  transform: translateY(-4px);
  box-shadow: 0 28px 60px rgba(14, 165, 233, 0.22), var(--shadow-strong);
  border-color: rgba(14, 165, 233, 0.6);
}

.largest-group-badge {
  position: absolute;
  top: -14px;
  left: 28px;
  background: linear-gradient(135deg, #0EA5E9 0%, #2563EB 100%);
  color: white;
  padding: 0.45rem 1.2rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 855;
  letter-spacing: 0.6px;
  box-shadow: 0 8px 22px rgba(14, 165, 233, 0.4);
  z-index: 2;
  text-transform: uppercase;
}

.highlight-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
  margin-top: 0.5rem;
}

.highlight-title {
  margin: 0;
  font-size: 1.55rem;
  font-weight: 850;
  color: var(--text-soft);
  flex-grow: 1;
}

.highlight-desc {
  font-size: 0.94rem;
  color: var(--text-muted);
  line-height: 1.6;
  max-width: 480px;
}

.highlight-stats {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(14, 165, 233, 0.08);
  border: 1.5px solid rgba(14, 165, 233, 0.3);
  padding: 0.65rem 1.2rem;
  border-radius: 20px;
  color: #0284C7;
  min-width: 130px;
}

.count-num {
  font-size: 1.6rem;
  font-weight: 900;
  line-height: 1.1;
}

.count-lbl {
  font-size: 0.62rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  opacity: 0.9;
  white-space: nowrap;
}

@media (max-width: 768px) {
  .summary-cards-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .highlight-content {
    flex-direction: column;
    align-items: stretch;
    gap: 1.2rem;
  }

  .highlight-stats {
    align-self: flex-start;
  }
}
</style>
