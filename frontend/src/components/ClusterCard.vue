<template>
  <div 
    class="glass-panel cluster-card" 
    :class="{ 'is-active': isActive }"
    @click="$emit('select', clusterId)"
  >
    <div class="card-header">
      <div class="cluster-badge">Group #{{ clusterId + 1 }}</div>
      <div class="count-badge">{{ count }} candidates</div>
    </div>
    
    <h4 class="cluster-label" :title="label">{{ label || `Talent Group ${clusterId + 1}` }}</h4>
  </div>
</template>

<script setup>
const props = defineProps({
  clusterId: {
    type: Number,
    required: true
  },
  label: {
    type: String,
    default: ''
  },
  count: {
    type: Number,
    required: true
  },
  isActive: {
    type: Boolean,
    default: false
  }
})

defineEmits(['select'])
</script>

<style scoped>
.cluster-card {
  padding: 1.4rem;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.6);
  border: 1.5px solid var(--glass-border);
  box-shadow: var(--shadow-soft);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.cluster-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-strong);
  border-color: rgba(14, 165, 233, 0.35);
}

/* Active Highlight Style */
.cluster-card.is-active {
  background: linear-gradient(135deg, rgba(14, 165, 233, 0.08) 0%, rgba(99, 102, 241, 0.06) 100%);
  border-color: rgba(14, 165, 233, 0.65);
  box-shadow: 0 12px 30px rgba(14, 165, 233, 0.12), var(--shadow-strong);
}

.cluster-card.is-active::before {
  content: '';
  position: absolute;
  inset: -1.5px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(14, 165, 233, 0.6), rgba(99, 102, 241, 0.4));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
}

.cluster-badge {
  font-size: 0.72rem;
  font-weight: 850;
  text-transform: uppercase;
  color: var(--primary-dark);
  background: rgba(14, 165, 233, 0.08);
  border: 1px solid rgba(14, 165, 233, 0.16);
  padding: 0.2rem 0.55rem;
  border-radius: 8px;
  letter-spacing: 0.5px;
}

.count-badge {
  font-size: 0.74rem;
  font-weight: 700;
  color: var(--text-muted);
}

.cluster-label {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--text-soft);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.is-active .cluster-label {
  color: var(--primary-dark);
}
</style>
