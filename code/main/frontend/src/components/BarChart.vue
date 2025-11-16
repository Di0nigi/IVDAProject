<template>
  <div class="bar-chart-container">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
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

const props = defineProps({
  xAttribute: {
    type: String,
    default: 'Historical Period'
  },
  categoryAttribute: {
    type: String,
    default: 'Scholarly'
  },
  xLabel: {
    type: String,
    default: 'Historical Period'
  },
  categoryLabel: {
    type: String,
    default: 'Scholarly'
  }
});

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
    const categoryValue = edition[props.categoryAttribute] || 'Unknown';
    
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
          size: 10
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
  min-height: 200px;
}
</style>
