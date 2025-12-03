<template>
  <div class="bar-chart-container">
    <!-- Settings gear icon -->
    <button @click="showSettings = !showSettings" :class="['settings-button', { 'back-mode': showSettings }]" :title="showSettings ? 'Show Chart' : 'Chart Settings'">
      <svg v-if="!showSettings" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="3"></circle>
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
      </svg>
      <span v-else>Back</span>
    </button>

    <div v-if="!showSettings" class="chart-view">
      <Bar :data="chartData" :options="chartOptions" />
    </div>

    <!-- Settings view -->
    <div v-else class="settings-view">
      <h3>Chart Settings</h3>
      
      <div class="selector-group">
        <label for="x-attribute">X-Axis (Groups):</label>
        <select 
          id="x-attribute" 
          :value="xAttribute" 
          @change="$emit('update:xAttribute', $event.target.value); updateLabel($event.target.value, 'x')"
          class="selector"
        >
          <option v-for="attr in attributes" :key="attr.value" :value="attr.value">
            {{ attr.label }}
          </option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js';
import { useEditionsData } from '../composables/useEditionsData';
import { useColorPalette } from '../composables/useColorPalette';

// Register Chart.js components
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const showSettings = ref(false);

const props = defineProps({
  xAttribute: {
    type: String,
    default: 'Language'
  },
  categoryAttribute: {
    type: String,
    default: 'Historical Period'
  },
  xLabel: {
    type: String,
    default: 'Language'
  },
  categoryLabel: {
    type: String,
    default: 'Historical Period'
  }
});

const emit = defineEmits(['update:xAttribute', 'update:xLabel']);

const attributes = [
  { value: 'Historical Period', label: 'Historical Period' },
  { value: 'Scholarly', label: 'Scholarly' },
  { value: 'Writing support', label: 'Writing Support' },
  { value: 'Language', label: 'Language' },
  { value: 'Open source/Open access', label: 'Open Access' },
  { value: 'Images', label: 'Images' },
  { value: 'OCR or keyed?', label: 'OCR/Keyed' },
  { value: 'Print facsimile (complementary output)', label: 'Print Facsimile' },
  { value: 'Audience', label: 'Audience' },
  { value: 'Institution(s)', label: 'Institution' },
];

const updateLabel = (value, type) => {
  const attr = attributes.find(a => a.value === value);
  if (type === 'x') {
    emit('update:xLabel', attr?.label || value);
  }
};

const { filteredEditions, loading, fetchEditions } = useEditionsData();
const { getColorForCategory, getBorderColor } = useColorPalette();

// Fetch data on mount
onMounted(() => {
  fetchEditions();
});

// Process data for stacked bar chart
const chartData = computed(() => {
  if (loading.value || !filteredEditions.value.length) {
    return { labels: [], datasets: [] };
  }

  // Group data by x-axis attribute
  const grouped = {};
  const categories = new Set();

  filteredEditions.value.forEach(edition => {
    const xValue = edition[props.xAttribute] || 'Unknown';
    let categoryValue = 'Unknown';

    if (props.categoryAttribute === 'Language') {
        const rawValue = edition.Language;
        if (rawValue) {
            const firstVal = Array.isArray(rawValue) ? rawValue[0] : String(rawValue);
            categoryValue = firstVal.split(/[,;]+/)[0].trim() || 'Unknown';
        }
    } else {
        const rawValue = edition[props.categoryAttribute];
        const value = Array.isArray(rawValue) ? rawValue[0] : rawValue;
        categoryValue = value || 'Unknown';
    }
    
    if (!grouped[xValue]) {
      grouped[xValue] = {};
    }
    if (!grouped[xValue][categoryValue]) {
      grouped[xValue][categoryValue] = 0;
    }
    grouped[xValue][categoryValue]++;
    categories.add(categoryValue);
  });

  const labels = Object.keys(grouped).sort();
  const categoryArray = Array.from(categories).sort();

  const datasets = categoryArray.map((category) => ({
    label: category,
    data: labels.map(label => grouped[label][category] || 0),
    backgroundColor: getColorForCategory(category),
    borderColor: getBorderColor(category),
    borderWidth: 1
  }));

  return { labels, datasets };
});

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display:false,
      position: 'top',
      labels: {
        font: {
          size: 11
        },
        boxWidth: 12
      }
    },
    title: {
      display: true,
      text: `${props.xLabel} by ${props.categoryLabel}`,
      font: {
        size: 14
      }
    }
  },
  scales: {
    x: {
      stacked: true,
      ticks: {
        font: {
          size: 0
        },
        maxRotation: 45,
        minRotation: 45,
        autoSkip: false
      }
    },
    y: {
      stacked: true,
      beginAtZero: true,
      ticks: {
        font: {
          size: 10
        }
      }
    }
  }
}));
</script>

<style scoped>
.bar-chart-container {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
}

/* Base style for the button, primarily for the 'gear' state */
.settings-button {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 28px;
  height: 28px;
  border: 1px solid #d5d9df;
  border-radius: 8px; /* Rounded square */
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  z-index: 10;
  padding: 0;
  color: #555; /* Default color for SVG */
}

/* Overrides when in 'back-mode' */
.settings-button.back-mode {
  width: auto;
  height: auto;
  padding: 4px 12px;
  border-radius: 16px; /* Pill shape */
  border: none;
  background: #f44336;
  color: white;
  font-size: 12px;
  font-weight: 500;
}

/* Hover effect specifically for the 'gear' state */

.settings-button:not(.back-mode):hover {

  transform: scale(0.95);

  border-color: #4a90e2;

  background-color: #eaf2fa;

}

.settings-button:not(.back-mode):hover svg {

  color: #4a90e2;

}



/* Hover effect specifically for the 'back' state */

.settings-button.back-mode:hover {

  transform: scale(1.05);

  filter: brightness(80%);

}

.chart-view {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.settings-view {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 40px 20px 20px 20px;
  box-sizing: border-box;
  overflow-y: auto;
}

.settings-view h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.selector-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-size: 13px;
  font-weight: 500;
  color: #555;
}

.selector {
  padding: 8px 12px;
  border: 1px solid #d5d9df;
  border-radius: 6px;
  background: white;
  font-size: 13px;
  color: #333;
  cursor: pointer;
  transition: border-color 0.2s;
}

.selector:hover {
  border-color: #999;
}

.selector:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.1);
}
</style>

