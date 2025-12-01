<template>
  <div>
    <div>
      <div id="myScatterPlot" class="myScatterPlot"></div>
    </div>
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
      const parent = this.$el.parentElement;
      const parentWidth = parent.clientWidth;
      const parentHeight = parent.clientHeight;

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
        width: parentWidth,
        height: parentHeight,
        margin: { l: 0, r: 0, t: 0, b: 0 },
        autosize: true,
        xaxis: {
          zeroline: true,
          showline: true,
          linecolor: "black",
          anchor: "y",
        },
        yaxis: {
          zeroline: true,
          showline: true,
          linecolor: "black",
          anchor: "x",
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
