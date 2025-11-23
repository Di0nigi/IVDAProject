<template>
  <div class="timeline-container">
    <div class="chart-wrapper">
      <canvas ref="chartCanvas"></canvas>
    </div>

    <!-- Time/Century Range Slider -->
    <div class="slider-group">
      <label>Time/Century</label>
      <div style="flex: 1;">
        <div class="range-slider-wrapper">
          <div class="range-track">
            <div class="range-fill" :style="rangeStyle"></div>
          </div>
          <input
            type="range"
            v-model.number="periodRange[0]"
            :min="-600"
            :max="2000"
            :step="100"
            @input="updatePeriodFilter"
            class="slider range-slider"
          />
          <input
            type="range"
            v-model.number="periodRange[1]"
            :min="-600"
            :max="2000"
            :step="100"
            @input="updatePeriodFilter"
            class="slider range-slider"
          />
        </div>
        <div class="range-labels">
          <span>-600</span>
          <span>0</span>
          <span>400</span>
          <span>800</span>
          <span>1200</span>
          <span>1600</span>
          <span>2000</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { Chart, registerables } from 'chart.js';
import { useEditionsData } from '../composables/useEditionsData';
import { useColorPalette } from '../composables/useColorPalette';
import { useFilters } from '../composables/useFilters';

Chart.register(...registerables);

const { filteredEditions } = useEditionsData();
const { getColorForCategory } = useColorPalette();
const { activeFilters, updateFilter } = useFilters();

const periodRange = ref([-600, 2000]);

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

const rangeStyle = computed(() => {
  const min = periodRange.value[0];
  const max = periodRange.value[1];
  const totalRange = 2000 - (-600);
  const leftPercent = ((min - (-600)) / totalRange) * 100;
  const rightPercent = ((max - (-600)) / totalRange) * 100;
  
  return {
    left: `${leftPercent}%`,
    width: `${rightPercent - leftPercent}%`
  };
});

const updatePeriodFilter = () => {
  if (periodRange.value[0] > periodRange.value[1]) {
    const temp = periodRange.value[0];
    periodRange.value[0] = periodRange.value[1];
    periodRange.value[1] = temp;
  }
  updateFilter('periodRange', [...periodRange.value]);
};

onMounted(() => {
  periodRange.value = [...activeFilters.periodRange];
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

.slider-group {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
  margin-top: 6px;
}

label {
  font-size: 13px;
  font-weight: 500;
  color: #555;
  min-width: 120px;
  flex-shrink: 0;
  align-self: flex-start;
  margin-top: -8px;
}

.range-slider-wrapper {
  position: relative;
  height: 6px;
  flex: 1;
}

.range-track {
  position: absolute;
  width: 100%;
  height: 6px;
  background: #e0e0e0;
  border-radius: 3px;
  top: 0;
  left: 0;
}

.range-fill {
  position: absolute;
  height: 6px;
  background: #000000;
  border-radius: 3px;
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
  border: 2px solid #000000;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  pointer-events: all;
}

.slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: white;
  border: 2px solid #000000;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  pointer-events: all;
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
  font-size: 11px;
  color: #666;
  margin-top: 4px;
}
</style>
