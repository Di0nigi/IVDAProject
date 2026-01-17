<template>
  <div class="reliability-container">
    <!-- Header with title aligned left -->
    <div class="header-row">
      <h3>Reliability Score Influence</h3>
    </div>
    
    <!-- Citations Slider -->
    <div class="slider-group">
      <label>Citations</label>
      <div style="flex: 1;">
      <div class="single-slider-wrapper">
        <div class="single-track">
          <div class="single-fill" :style="citationsStyle"></div>
        </div>
        <input
          type="range"
          v-model.number="citations"
          :min="0"
          :max="100"
          class="slider single-slider"
        />
      </div>
      <div class="range-labels">
        <span>low</span>
        <span>High</span>
      </div>
      </div>
    </div>

    <!-- Value of Witnesses Slider -->
    <div class="slider-group">
      <label>Value of Witnesses</label>
      <div style="flex: 1;">
      <div class="single-slider-wrapper">
        <div class="single-track">
          <div class="single-fill" :style="witnessesStyle"></div>
        </div>
        <input
          type="range"
          v-model.number="witnesses"
          :min="0"
          :max="100"
          class="slider single-slider"
        />
      </div>
      <div class="range-labels">
        <span>low</span>
        <span>High</span>
      </div>
      </div>
    </div>

    <!-- Audience Slider -->
    <div class="slider-group">
      <label>Audience</label>
      <div style="flex: 1;">
      <div class="single-slider-wrapper">
        <div class="single-track">
          <div class="single-fill" :style="audienceStyle"></div>
        </div>
        <input
          type="range"
          v-model.number="audience"
          :min="0"
          :max="100"
          class="slider single-slider"
        />
      </div>
      <div class="range-labels">
        <span>low</span>
        <span>High</span>
      </div>
      </div>
    </div>

    <!-- Current Edition Score Display (below sliders) -->
    <div v-if="currentEdition" class="current-score-inline">
      <span class="score-label-inline">Current Edition Score:</span>
      <span class="score-value-inline" :style="scoreStyle">{{ currentScore }}</span>
    </div>

    <!-- Distribution Chart -->
    <div class="distribution-section">
      <h4>Score Distribution</h4>
      <div class="chart-container">
        <canvas ref="distributionCanvas"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, defineProps, onMounted, onUnmounted, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';
import { useFilters } from '../composables/useFilters';
import { useEditionsData } from '../composables/useEditionsData';

Chart.register(...registerables);

const props = defineProps({
  edition: {
    type: Object,
    default: null
  }
});

const { updateReliabilityWeights } = useFilters();
const { editions } = useEditionsData();

const citations = ref(50);
const witnesses = ref(50);
const audience = ref(50);
const distributionCanvas = ref(null);
let chartInstance = null;

const currentEdition = computed(() => props.edition);

const currentScore = computed(() => {
  if (!currentEdition.value) return 0;
  
  // Get binary values
  const citationVal = currentEdition.value.Citation_bin || 0;
  const witnessesVal = currentEdition.value.Value_of_witnesses_yes || 0;
  const audienceVal = currentEdition.value.Audience && 
                      currentEdition.value.Audience.toLowerCase() !== 'not provided' ? 1 : 0;
  
  // Calculate total weight
  const total = citations.value + witnesses.value + audience.value;
  if (total === 0) return 0;
  
  // Calculate weighted score
  const score = (citationVal * citations.value + 
                 witnessesVal * witnesses.value + 
                 audienceVal * audience.value) / total * 100;
  
  return Math.round(score);
});

const scoreStyle = computed(() => {
  const s = currentScore.value;
  let r, g, b;
  const maxIntensity = 200;
  if (s <= 50) {
    r = maxIntensity;
    g = Math.round(maxIntensity * (s / 50));
    b = 0;
  } else {
    r = Math.round(maxIntensity * (1 - (s - 50) / 50));
    g = maxIntensity;
    b = 0;
  }
  return {
    color: `rgb(${r},${g},${b})`,
    fontWeight: 'bold',
    fontSize: '24px'
  };
});

// Watch for slider changes and update global weights
watch([citations, witnesses, audience], () => {
  updateReliabilityWeights({
    citations: citations.value,
    witnesses: witnesses.value,
    audience: audience.value
  });
}, { immediate: true });

// Calculate distribution data
const distributionData = computed(() => {
  if (!editions.value || editions.value.length === 0) return null;
  
  const scores = editions.value.map(e => e.reliabilityScore || 0).filter(s => !isNaN(s));
  if (scores.length === 0) return null;
  
  // Create histogram bins (0-100 in steps of 5)
  const binSize = 5;
  const bins = Array.from({ length: 21 }, (_, i) => ({
    x: i * binSize,
    count: 0
  }));
  
  // Count scores in each bin
  scores.forEach(score => {
    const binIndex = Math.min(Math.floor(score / binSize), 20);
    bins[binIndex].count++;
  });
  
  // Convert to density (normalize)
  const maxCount = Math.max(...bins.map(b => b.count));
  const density = bins.map(b => ({
    x: b.x,
    y: maxCount > 0 ? (b.count / maxCount) * 100 : 0
  }));
  
  // Interpolate y-value for current score on the curve
  const currentScoreValue = currentScore.value;
  let currentY = 0;
  
  // Find the two bins that currentScore falls between
  for (let i = 0; i < density.length - 1; i++) {
    if (currentScoreValue >= density[i].x && currentScoreValue <= density[i + 1].x) {
      // Linear interpolation
      const x0 = density[i].x;
      const x1 = density[i + 1].x;
      const y0 = density[i].y;
      const y1 = density[i + 1].y;
      const t = (currentScoreValue - x0) / (x1 - x0);
      currentY = y0 + t * (y1 - y0);
      break;
    }
  }
  
  return { density, currentScore: currentScoreValue, currentY };
});

// Create/update chart
const createChart = () => {
  if (!distributionCanvas.value || !distributionData.value) return;
  
  if (chartInstance) {
    chartInstance.destroy();
  }
  
  const { density, currentScore, currentY } = distributionData.value;
  
  chartInstance = new Chart(distributionCanvas.value, {
    type: 'line',
    data: {
      datasets: [
        {
          label: 'Distribution',
          data: density,
          borderColor: 'rgba(74, 144, 226, 1)',
          backgroundColor: 'rgba(74, 144, 226, 0.2)',
          fill: true,
          tension: 0.4, // Smooth curve
          pointRadius: 0,
          borderWidth: 2
        },
        {
          label: 'Current Work',
          data: [{ x: currentScore, y: currentY }],
          borderColor: 'rgba(74, 144, 226, 1)',
          backgroundColor: 'rgba(74, 144, 226, 1)',
          pointRadius: 3,
          pointHoverRadius: 5,
          showLine: false,
          pointStyle: 'circle',
          borderWidth: 2
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          enabled: true,
          callbacks: {
            label: (context) => {
              if (context.datasetIndex === 1) {
                return `Current: ${currentScore}`;
              }
              return `Density: ${context.parsed.y.toFixed(1)}`;
            }
          }
        }
      },
      scales: {
        x: {
          type: 'linear',
          min: 0,
          max: 100,
          title: {
            display: true,
            text: 'Reliability Score',
            font: { size: 11 }
          },
          ticks: {
            stepSize: 20,
            font: { size: 10 }
          },
          grid: {
            display: true,
            color: 'rgba(0, 0, 0, 0.05)'
          }
        },
        y: {
          beginAtZero: true,
          max: 100,
          title: {
            display: true,
            text: 'Density',
            font: { size: 11 }
          },
          ticks: {
            display: false
          },
          grid: {
            display: false
          }
        }
      },
      interaction: {
        intersect: false,
        mode: 'index'
      }
    }
  });
};

// Update chart when data changes
watch(distributionData, () => {
  nextTick(() => {
    createChart();
  });
}, { deep: true });

onMounted(() => {
  nextTick(() => {
    createChart();
  });
});

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});

const citationsStyle = computed(() => {
  const percent = citations.value;
  return {
    width: `${percent}%`
  };
});

const witnessesStyle = computed(() => {
  const percent = witnesses.value;
  return {
    width: `${percent}%`
  };
});

const fundingStyle = computed(() => {
  const percent = funding.value;
  return {
    width: `${percent}%`
  };
});

const audienceStyle = computed(() => {
  const percent = audience.value;
  return {
    width: `${percent}%`
  };
});
</script>

<style scoped>
.reliability-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: 100%;
  padding: 4px;
  width: 100%;
  overflow-y: auto;
}

.header-row {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 8px;
  padding-left: 4px;
}

h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.slider-group {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
  margin: 8px 0;
}

label {
  font-size: 12px;
  font-weight: 500;
  color: #555;
  min-width: 140px;
  flex-shrink: 0;
}

.single-slider-wrapper {
  position: relative;
  height: 6px;
  flex: 1;
}

.single-track {
  position: absolute;
  width: 100%;
  height: 6px;
  background: #e0e0e0;
  border-radius: 3px;
  top: 0;
  left: 0;
}

.single-fill {
  position: absolute;
  height: 6px;
  background: #000;
  border-radius: 3px;
  left: 0;
}

.slider {
  position: absolute;
  width: 100%;
  height: 6px;
  border-radius: 3px;
  outline: none;
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
  top: 0;
  left: 0;
  margin: 0;
  pointer-events: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: white;
  border: 2px solid #000;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  pointer-events: all;
  transition: transform 0.2s ease;
}

.slider:hover::-webkit-slider-thumb {
  transform: scale(1.2);
}

.slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: white;
  border: 2px solid #000;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  pointer-events: all;
  transition: transform 0.2s ease;
}

.slider:hover::-moz-range-thumb {
  transform: scale(1.2);
}

.slider::-webkit-slider-runnable-track {
  background: transparent;
  height: 6px;
}

.slider::-moz-range-track {
  background: transparent;
  height: 6px;
}

.range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  color: #666;
  margin-top: 2px;
}

.current-score-inline {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 12px;
  background: #f5f5f5;
  border-radius: 6px;
}

.score-label-inline {
  font-size: 13px;
  font-weight: 500;
  color: #555;
}

.score-value-inline {
  font-size: 13px;
  font-weight: bold;
}

.distribution-section {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.distribution-section h4 {
  margin: 0;
  font-size: 12px;
  font-weight: 600;
  color: #333;
}

.chart-container {
  width: 100%;
  height: 140px;
  position: relative;
}
</style>
