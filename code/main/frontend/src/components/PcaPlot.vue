<template>
  <div>
    <div>
      <div id='myScatterPlot' class="myScatterPlot"></div>
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

    const xMin = Math.min(...x);
    const xMax = Math.max(...x);
    const yMin = Math.min(...y);
    const yMax = Math.max(...y);
    const xMin2 = Math.min(xMin, 0);
    const xMax2 = Math.max(xMax, 0);
    const yMin2 = Math.min(yMin, 0);
    const yMax2 = Math.max(yMax, 0);

    const layout = {
      width: 600,
      height: 400,


      margin: { l: 0, r: 0, t: 0, b: 0 },

  autosize: true,

xaxis: {
  fixedrange: false,
  autorange: false,
    range: [-5, 25], 
    zeroline: false,
    showline: true,
    label: false,
    linecolor: "black",
    anchor: "y"     // force crossing
  },
  yaxis: {
    autorange: false,
    fixedrange: false ,
    range: [-15, 5], 
    zeroline: false,
    showline: true,
    label: false,
    linecolor: "black",
    anchor: "x"     // force crossing
  }
    
    };

  const config = {
    displayModeBar: true,
    responsive: true
};


    Plotly.newPlot(containerId, [trace], layout, config);
}
}
}
</script>

<style>

.myScatterPlot {
  width: 100%;
  height: 100%;
}

</style>

