<template>
  <div class="bar-chart-container">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
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

const editions = ref([]);
const loading = ref(true);

// Fetch data from backend
const fetchData = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/texts');
    editions.value = await response.json();
    loading.value = false;
  } catch (error) {
    console.error('Error fetching data:', error);
    loading.value = false;
  }
};

fetchData();

// Process data for stacked bar chart
const chartData = computed(() => {
  if (loading.value || !editions.value.length) {
    return { labels: [], datasets: [] };
  }

  // Group data by x-axis attribute
  const grouped = {};
  const categories = new Set();

  editions.value.forEach(edition => {
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

  // Generate colors for each category - we need to make that seperate in the longterm, so that color linking is ensured across graphs
  const colors = [
    'rgba(54, 162, 235, 0.8)',
    'rgba(255, 99, 132, 0.8)',
    'rgba(75, 192, 192, 0.8)',
    'rgba(255, 206, 86, 0.8)',
    'rgba(153, 102, 255, 0.8)',
    'rgba(255, 159, 64, 0.8)',
    'rgba(201, 203, 207, 0.8)'
  ];

  const datasets = categoryArray.map((category, index) => ({
    label: category,
    data: labels.map(label => grouped[label][category] || 0),
    backgroundColor: colors[index % colors.length],
    borderColor: colors[index % colors.length].replace('0.8', '1'),
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

// Watch for prop changes and refetch if needed
watch([() => props.xAttribute, () => props.categoryAttribute], () => {
  // Chart will automatically update via computed property
});
</script>

<style scoped>
.bar-chart-container {
  width: 100%;
  height: 100%;
  min-height: 200px;
}
</style>
