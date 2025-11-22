<template>
  <div>
    <div>
      <div id='myScatterPlot'></div>
    </div>
  </div>
</template>


<script>
import Plotly from 'plotly.js/dist/plotly';
export default {
data: () => ({
  ScatterPlotData: {xCoor: [], yCoor: [], labels: []},
}),
mounted() {
  this.fetchData()
},
methods: {
  async fetchData() {
    var reqUrl = 'http://127.0.0.1:5000/texts/scatterPoints'
    console.log("reqUrl" + reqUrl)

    const response = await fetch(reqUrl)
    const responseData = await response.json();

    this.ScatterPlotData.xCoor = responseData.xCoor;
    this.ScatterPlotData.yCoor = responseData.yCoor;
    this.ScatterPlotData.labels = responseData.labels;

    this.drawScatterPlot("myScatterPlot", this.ScatterPlotData.xCoor, this.ScatterPlotData.yCoor, this.ScatterPlotData.labels)
  },

drawScatterPlot(containerId, x, y, labels) {
    const uniqueLabels = [...new Set(labels)];

    const colorMap = {};
    const colors = uniqueLabels.map((_, i) => {
        const hue = (i * 137.508) % 360;
        return `hsl(${hue}, 70%, 50%)`;
    });
    uniqueLabels.forEach((label, idx) => {
        colorMap[label] = colors[idx];
    });

    const pointColors = labels.map(l => colorMap[l]);

    const trace = {
        x: x,
        y: y,
        mode: "markers",
        type: "scatter",
        marker: {
            color: pointColors,
            size: 8
        },
        text: labels
    };

    const layout = {
        xaxis: { title: "X" },
        yaxis: { title: "Y" },
        margin: { t: 20 }
    };

    Plotly.newPlot(containerId, [trace], layout);
}
}
}
</script>