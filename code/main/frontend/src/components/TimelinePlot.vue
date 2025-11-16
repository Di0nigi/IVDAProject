<template>
  <div class="timeline-container">
        <div class="chart-wrapper">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { Chart, registerables } from 'chart.js';
import { useEditionsData } from '../composables/useEditionsData';
import { useColorPalette } from '../composables/useColorPalette';

Chart.register(...registerables);

const { filteredEditions } = useEditionsData();
const { getColorForCategory } = useColorPalette();

const chartCanvas = ref(null);
let chartInstance = null;

const chartData = computed(() => {
  const validData = filteredEditions.value
    .filter(e => e.period_start !== undefined && e.period_start !== null);
  
  if (validData.length === 0) {
    return { datasets: [], minYear: -600, maxYear: 2000 };
  }

  // Calculate min and max years from the data
  const allYears = validData.flatMap(e => [e.period_start, e.period_end].filter(y => y !== null && y !== undefined));
  const minYear = Math.min(...allYears);
  const maxYear = Math.max(...allYears);

  // Sort by start year to process chronologically
  const sortedData = validData
    .map(e => ({
      period: e['Historical Period'] || 'Unknown',
      name: e['Edition name'] || 'Unknown',
      timeCentury: e['Time/Century'] || 'Unknown',
      start: e.period_start || 0,
      end: e.period_end || e.period_start || 0
    }))
    .sort((a, b) => a.start - b.start);

  // Assign y positions avoiding overlaps
  const tracks = []; // Each track holds the end time of the last work on that track
  const data = sortedData.map(work => {
    // Find the first track where this work doesn't overlap
    let trackIndex = tracks.findIndex(trackEnd => work.start >= trackEnd);
    
    // If no available track, create a new one
    if (trackIndex === -1) {
      trackIndex = tracks.length;
      tracks.push(work.end);
    } else {
      tracks[trackIndex] = work.end;
    }
    
    return {
      ...work,
      yPosition: (trackIndex + 0.5) / Math.max(tracks.length + 1, 1)
    };
  });

  // Group by period for coloring
  const periods = [...new Set(data.map(d => d.period))];
  const datasets = periods.map(period => {
    const periodData = data.filter(d => d.period === period);
    const color = getColorForCategory(period);
    
    // Create line segments for each work
    const segments = periodData.map(work => ({
      type: 'line',
      xMin: work.start,
      xMax: work.end,
      yMin: work.yPosition,
      yMax: work.yPosition,
      borderColor: color,
      borderWidth: 2,
      label: work.name,
      period: work.period,
      start: work.start,
      end: work.end
    }));
    
    return {
      label: period,
      data: periodData.map(work => ({
        x: work.start, // Point at the start of the work
        y: work.yPosition,
        name: work.name,
        timeCentury: work.timeCentury,
        start: work.start,
        end: work.end,
        period: work.period
      })),
      backgroundColor: color,
      borderColor: color,
      borderWidth: 1,
      pointRadius: 2,
      pointHoverRadius: 6,
      segments: segments
    };
  });

  return { datasets, minYear, maxYear };
});

const createChart = () => {
  if (!chartCanvas.value) return;
  
  if (chartInstance) {
    chartInstance.destroy();
  }

  const { datasets, minYear, maxYear } = chartData.value;

  chartInstance = new Chart(chartCanvas.value, {
    type: 'scatter',
    data: { datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: false
        },
        // legend: {
        //   display: true,
        //   position: 'right',
        //   labels: {
        //     font: { size: 10 },
        //     boxWidth: 10
        //   }
        // },
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              const data = context.raw;
              return [
                `Name: ${data.name}`,
                `Period: ${data.period}`,
                `Time/Century: ${data.timeCentury}`
              ];
            }
          }
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Year',
            font: { size: 12, weight: 'bold' }
          },
          min: minYear-20,
          max: maxYear+10,
          ticks: {
            font: { size: 10 },
            callback: function(value) {
              return value.toString();
            }
          }
        },
        y: {
          display: false,
          min: -0.05,
          max: 1.05
        }
      }
    },
    plugins: [{
      id: 'timelineLines',
      afterDatasetsDraw(chart) {
        const ctx = chart.ctx;
        const xScale = chart.scales.x;
        const yScale = chart.scales.y;
        
        datasets.forEach(dataset => {
          if (dataset.segments) {
            dataset.segments.forEach(segment => {
              const x1 = xScale.getPixelForValue(segment.xMin);
              const x2 = xScale.getPixelForValue(segment.xMax);
              const y = yScale.getPixelForValue(segment.yMin);
              
              ctx.save();
              ctx.strokeStyle = segment.borderColor;
              ctx.lineWidth = segment.borderWidth;
              ctx.beginPath();
              ctx.moveTo(x1, y);
              ctx.lineTo(x2, y);
              ctx.stroke();
              ctx.restore();
            });
          }
        });
      }
    }]
  });
};

watch(chartData, () => {
  createChart();
}, { deep: true });

onMounted(() => {
  createChart();
});

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});
</script>

<style scoped>
.timeline-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  gap: 12px;
}

h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.chart-wrapper {
  flex: 1;
  position: relative;
  min-height: 0;
}

canvas {
  max-height: 100%;
}
</style>
