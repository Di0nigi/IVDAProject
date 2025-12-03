<template>
  <div class="plot-wrapper">
    <h3 class="plot-title">PCA grouping by Description</h3>
    <div id="myScatterPlot" class="myScatterPlot"></div>
  </div>
</template>

<script>
import Plotly from "plotly.js/dist/plotly";
import { useEditionsData } from "../composables/useEditionsData";
import { watch } from "vue";

export default {
  data() {
    return {
      ScatterPlotData: { ids: [], xCoor: [], yCoor: [], labels: [] },
      rawResponseData: null, // store raw data so we can recompute on filter change
    };
  },

  created() {
    const { filteredEditions } = useEditionsData();
    this.filteredEditions = filteredEditions;

    // REACTIVE WATCH ON FILTERED EDITIONS
    watch(
      this.filteredEditions,
      () => {
        if (this.rawResponseData) {
          this.processScatterData();
          this.drawScatterPlot(
            "myScatterPlot",
            this.ScatterPlotData.xCoor,
            this.ScatterPlotData.yCoor,
            this.ScatterPlotData.labels
          );
        }
      },
      { deep: true }
    );
  },

  mounted() {
    this.fetchData();
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
}
.plot-title {
  padding: 2px 10px;
  font-family: sans-serif;
  font-size: 0.8em;
  font-weight: 600;
  color: #333;
  flex-shrink: 0;
  text-align: center;
}
#myScatterPlot {
    flex-grow: 1;
    min-height: 0;
}
</style>
