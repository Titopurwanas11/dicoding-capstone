<template>
  <div class="charts-card glass-panel">
    <h3 class="charts-title">Talent Pool Analysis</h3>
    
    <div class="charts-layout">
      <!-- Bar Chart -->
      <div class="chart-section sub-glass-card">
        <h4 class="chart-subtitle">Talent Count by Group</h4>
        <div class="chart-container">
          <canvas ref="barChartCanvas" id="cluster-bar-chart"></canvas>
        </div>
      </div>

      <!-- Doughnut Chart -->
      <div class="chart-section sub-glass-card">
        <h4 class="chart-subtitle">Talent Proportion</h4>
        <div class="chart-container">
          <canvas ref="doughnutChartCanvas" id="cluster-doughnut-chart"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const props = defineProps({
  clusters: {
    type: Array,
    required: true
  }
})

const barChartCanvas = ref(null)
const doughnutChartCanvas = ref(null)

let barChartInstance = null
let doughnutChartInstance = null

// Cohesive theme colors matching root variables
const themeColors = [
  '#0EA5E9', // Sky blue
  '#6366F1', // Indigo
  '#22C55E', // Green
  '#F59E0B', // Amber
  '#8B5CF6', // Purple
  '#EF4444'  // Red
]

const themeColorsAlpha = [
  'rgba(14, 165, 233, 0.75)',
  'rgba(99, 102, 241, 0.75)',
  'rgba(34, 197, 94, 0.75)',
  'rgba(245, 158, 11, 0.75)',
  'rgba(139, 92, 246, 0.75)',
  'rgba(239, 68, 68, 0.75)'
]

const drawCharts = () => {
  if (!barChartCanvas.value || !doughnutChartCanvas.value) return

  // Destroy previous instances
  if (barChartInstance) barChartInstance.destroy()
  if (doughnutChartInstance) doughnutChartInstance.destroy()

  const labels = props.clusters.map((c, index) => c.suggested_label || `Group ${index + 1}`)
  const counts = props.clusters.map(c => c.candidates.length)
  
  // Dynamic color assignments
  const bgColors = labels.map((_, i) => themeColorsAlpha[i % themeColorsAlpha.length])
  const borderColors = labels.map((_, i) => themeColors[i % themeColors.length])

  // 1. Draw Bar Chart
  const ctxBar = barChartCanvas.value.getContext('2d')
  barChartInstance = new Chart(ctxBar, {
    type: 'bar',
    data: {
      labels: labels.map(l => l.split(' / ').slice(0, 2).join(' / ')), // truncate labels slightly for space
      datasets: [{
        data: counts,
        backgroundColor: bgColors,
        borderColor: borderColors,
        borderWidth: 1.5,
        borderRadius: 8,
        barPercentage: 0.5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(15, 23, 42, 0.9)',
          titleFont: { family: 'Plus Jakarta Sans', weight: '700' },
          bodyFont: { family: 'Plus Jakarta Sans' },
          callbacks: {
            label: (context) => `Candidates: ${context.parsed.y}`
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: {
            color: '#1E3A5F',
            font: { family: 'Plus Jakarta Sans', weight: '800', size: 10 }
          }
        },
        y: {
          beginAtZero: true,
          grid: { color: 'rgba(148, 163, 184, 0.08)' },
          ticks: {
            color: '#64748B',
            font: { family: 'Plus Jakarta Sans', weight: '700', size: 10 },
            stepSize: 1
          }
        }
      }
    }
  })

  // 2. Draw Doughnut Chart
  const ctxDoughnut = doughnutChartCanvas.value.getContext('2d')
  doughnutChartInstance = new Chart(ctxDoughnut, {
    type: 'doughnut',
    data: {
      labels: labels.map(l => l.split(' / ')[0]), // use main label name for pie legend
      datasets: [{
        data: counts,
        backgroundColor: bgColors,
        borderColor: borderColors,
        borderWidth: 1.5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: {
            color: '#1E3A5F',
            font: { family: 'Plus Jakarta Sans', weight: '700', size: 10 },
            boxWidth: 12,
            padding: 8
          }
        },
        tooltip: {
          backgroundColor: 'rgba(15, 23, 42, 0.9)',
          titleFont: { family: 'Plus Jakarta Sans', weight: '700' },
          bodyFont: { family: 'Plus Jakarta Sans' },
          callbacks: {
            label: (context) => {
              const total = context.dataset.data.reduce((acc, v) => acc + v, 0)
              const val = context.raw
              const pct = ((val / total) * 100).toFixed(0)
              return ` Candidates: ${val} (${pct}%)`
            }
          }
        }
      },
      cutout: '60%'
    }
  })
}

// Watch clusters array
watch(() => props.clusters, (newClusters) => {
  if (newClusters && newClusters.length) {
    nextTick(() => {
      drawCharts()
    })
  }
}, { deep: true, immediate: true })

onUnmounted(() => {
  if (barChartInstance) barChartInstance.destroy()
  if (doughnutChartInstance) doughnutChartInstance.destroy()
})
</script>

<style scoped>
.charts-card {
  padding: 2rem;
  border-radius: 28px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.charts-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 850;
  color: var(--text-soft);
}

.charts-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.chart-section {
  padding: 1.4rem;
  border-radius: 22px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sub-glass-card {
  background: rgba(255, 255, 255, 0.45);
  border: 1px solid var(--glass-border);
  box-shadow: 0 8px 32px rgba(15, 23, 42, 0.015);
}

.chart-subtitle {
  margin: 0;
  font-size: 0.94rem;
  font-weight: 800;
  color: var(--text-soft);
}

.chart-container {
  position: relative;
  width: 100%;
  height: 220px;
}

@media (max-width: 768px) {
  .charts-layout {
    grid-template-columns: 1fr;
    gap: 1.2rem;
  }
}
</style>
