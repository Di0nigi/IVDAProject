<template>
  <div class="plot-wrapper">
    <h3 class="plot-title">PCA grouping by Description</h3>
    <div v-if="updateStatus" class="update-status" :class="updateStatus">
      {{ updateStatus === 'updating' ? 'Updating...' : 'Up to date' }}
    </div>
    <div id="myScatterPlot" class="myScatterPlot"></div>
  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";
import { useEditionsData } from "../composables/useEditionsData";
import { useFilters } from "../composables/useFilters";
import { watch } from "vue";

export default {
  data() {
    return {
      ScatterPlotData: { ids: [], xCoor: [], yCoor: [], labels: [] },
      rawResponseData: null,
      updateStatus: null,
      hasChanges: false,
      periodicCheckInterval: null,
      lastFilterState: null,
      changeDebounceTimer: null
    };
  },

  created() {
    const { filteredEditions } = useEditionsData();
    const { activeFilters } = useFilters();
    this.filteredEditions = filteredEditions;
    this.activeFilters = activeFilters;

    // Watch for filter changes and mark for update
    watch(
      this.activeFilters,
      (newVal) => {
        if (this.rawResponseData) {
          // Clear any pending change detection
          if (this.changeDebounceTimer) {
            clearTimeout(this.changeDebounceTimer);
          }
          
          // Wait 3 seconds before marking as changed
          this.changeDebounceTimer = setTimeout(() => {
            const currentState = JSON.stringify(newVal);
            if (this.lastFilterState !== currentState) {
              console.log('PCA: Filters changed, marking for update');
              this.hasChanges = true;
              this.lastFilterState = currentState;
            }
          }, 1000);
        }
      },
      { deep: true }
    );
  },

  mounted() {
    this.fetchData();
    
    console.log('PCA: Setting up 5-second update interval');
    let checkCount = 0;
    
    // Start periodic check for updates every 5 seconds
    this.periodicCheckInterval = setInterval(() => {
      checkCount++;
      console.log(`PCA: Periodic check #${checkCount} (should be every 5 seconds)`);
      
      if (this.hasChanges) {
        console.log('PCA: Starting update...');
        this.updateStatus = 'updating';
        this.hasChanges = false;
        
          this.processScatterData();
          this.drawScatterPlot(
            "myScatterPlot",
            this.ScatterPlotData.xCoor,
            this.ScatterPlotData.yCoor,
            this.ScatterPlotData.labels
          );
          console.log('PCA: Update complete');
          this.updateStatus = 'up-to-date';
          
          setTimeout(() => {
            this.updateStatus = null;
          }, 1000);
      } else {
        console.log('PCA: No changes, skipping update');
      }
    }, 1000);
  },

  beforeUnmount() {
    if (this.periodicCheckInterval) {
      clearInterval(this.periodicCheckInterval);
    }
  },

  methods: {
    async fetchData() {
      const reqUrl = "http://127.0.0.1:5000/texts/scatterPoints";

      const response = await fetch(reqUrl);
      const responseData = await response.json();

      // store raw response for recomputation
      this.rawResponseData = responseData;

      // initial compute
      this.processScatterData();
      this.drawScatterPlot(
        "myScatterPlot",
        this.ScatterPlotData.xCoor,
        this.ScatterPlotData.yCoor,
        this.ScatterPlotData.labels
      );
    },

    processScatterData() {
      if (!this.rawResponseData) return;

      const responseData = JSON.parse(JSON.stringify(this.rawResponseData));

      const arr = [...this.filteredEditions.value].sort((a, b) => a.id - b.id);
      responseData.ids = responseData.ids.sort((a, b) => a - b);

      // RESET before recomputing (important for reactivity!)
      this.ScatterPlotData.ids = [];
      this.ScatterPlotData.xCoor = [];
      this.ScatterPlotData.yCoor = [];
      this.ScatterPlotData.labels = [];

      let i = 0; // filtered editions
      let j = 0; // response IDs

      while (i < arr.length && j < responseData.ids.length) {
        if (arr[i].id === responseData.ids[j]) {
          this.ScatterPlotData.xCoor.push(responseData.xCoor[j]);
          this.ScatterPlotData.yCoor.push(responseData.yCoor[j]);
          this.ScatterPlotData.labels.push(responseData.labels[j]);
          i++;
          j++;
        } else if (arr[i].id < responseData.ids[j]) {
          i++;
        } else {
          j++;
        }
      }
    },

    drawScatterPlot(containerId, x, y, labels) {
      const plotContainer = this.$el.querySelector('#' + containerId);
      if (!plotContainer) return;

      const uniqueLabels = [...new Set(labels)];

      const colorMap = {};
      const colors = uniqueLabels.map((_, i) => {
        const hue = (i * 137.508) % 360;
        return `hsl(${hue}, 70%, 50%)`;
      });
      uniqueLabels.forEach((label, idx) => {
        colorMap[label] = colors[idx];
      });

      const pointColors = labels.map((l) => colorMap[l]);

      const trace = {
        x,
        y,
        mode: "markers",
        type: "scatter",
        marker: { color: pointColors, size: 8 },
        text: labels,
      };

      const layout = {
        margin: { l: 25, r: 10, t: 10, b: 25 },
        autosize: true,
        xaxis: {
          visible: false,
        },
        yaxis: {
          visible: false,
        },
      };

      const config = { displayModeBar: true, responsive: true };
      Plotly.newPlot(containerId, [trace], layout, config);
    },
  },
};
</script>

<style>
</style>

<style scoped>
.plot-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  background-color: white;
  flex-direction: column;
  position: relative;
}
.plot-title {
  position: absolute;
  top: 260px;
  left: 10px;
  z-index: 10;
  margin: 0;
  font-family: sans-serif;
  font-size: 0.8em;
  font-weight: 600;
  color: #333;

}
.update-status {
  position: absolute;
  bottom: 10px;
  left: 10px;
  z-index: 10;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  transition: all 0.3s ease;
}
.update-status.updating {
  background: #FFC107;
  color: #333;
  animation: pulse 1.5s ease-in-out infinite;
}
.update-status.up-to-date {
  background: #4CAF50;
  color: white;
  animation: fadeIn 0.3s ease;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.8); }
  to { opacity: 1; transform: scale(1); }
}
#myScatterPlot {
    flex-grow: 1;
    min-height: 0;
}
</style>
