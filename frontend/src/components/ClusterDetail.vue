<template>
  <div class="glass-panel cluster-detail-card">
    <div class="detail-header">
      <div class="icon-bubble">📂</div>
      <div class="header-text">
        <h3 class="group-title">{{ label || 'Talent Group Detail' }}</h3>
        <span class="group-count">{{ candidates.length }} Members in this group</span>
      </div>
    </div>

    <div class="candidates-container">
      <div 
        v-for="name in candidates" 
        :key="name" 
        class="candidate-row"
      >
        <span class="candidate-icon">📄</span>
        <span class="candidate-filename" :title="name">{{ name }}</span>
      </div>

      <div v-if="!candidates.length" class="empty-detail">
        Select a talent cluster from the list to view candidate members.
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  label: {
    type: String,
    default: ''
  },
  candidates: {
    type: Array,
    default: () => []
  }
})
</script>

<style scoped>
.cluster-detail-card {
  padding: 1.8rem;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.65);
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-soft);
  display: flex;
  flex-direction: column;
  gap: 1.6rem;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  border-bottom: 1px solid rgba(14, 116, 144, 0.08);
  padding-bottom: 1.2rem;
}

.icon-bubble {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: rgba(14, 165, 233, 0.08);
  border: 1px solid rgba(14, 165, 233, 0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.35rem;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.group-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 850;
  color: var(--text-soft);
}

.group-count {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-weight: 600;
}

.candidates-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.candidate-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.9rem 1.1rem;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.45);
  border: 1px solid rgba(148, 163, 184, 0.06);
  transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.candidate-row:hover {
  background: rgba(255, 255, 255, 0.75);
  border-color: rgba(14, 165, 233, 0.15);
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.02);
}

.candidate-icon {
  font-size: 1.1rem;
  line-height: 1;
}

.candidate-filename {
  font-size: 0.94rem;
  font-weight: 700;
  color: var(--text-soft);
  font-family: var(--mono);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.empty-detail {
  text-align: center;
  color: var(--text-muted);
  font-style: italic;
  padding: 2rem 0;
}
</style>
