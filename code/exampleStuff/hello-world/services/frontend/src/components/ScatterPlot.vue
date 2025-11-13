<template>
  <div>
    <v-row align="center" justify="center" class="mt-1 mb-0">
      <h3>Overview of {{ $props.selectedCategory }} Companies</h3>
    </v-row>
    <div style="height: 90vh">
      <div id='myScatterPlot' style="height: inherit"></div>
    </div>
  </div>
</template>
<script>
import Plotly from 'plotly.js/dist/plotly';
//import PieChart  from './PieChart.vue';
export default {
  name: "ScatterPlot",
  props: [
    "selectedCategory"
  ],
  data: () => ({
    ScatterPlotData: {x: [], y: [], name: [],colorType :[]},
  }),
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      // req URL to retrieve companies from backend
      var reqUrl = 'http://127.0.0.1:5000/companies?category=' + this.$props.selectedCategory
      console.log('ReqURL ' + reqUrl)
      console.log(this.$props.selectedCategory)
      
      // await response and data
      const response = await fetch(reqUrl);
      const responseData = await response.json();
      //console.log(responseData)
      this.ScatterPlotData={x: [], y: [], name: [],colorType :[]};

      // transform data to usable by scatterplot
      responseData.forEach((company) => {
        this.ScatterPlotData.name.push(company.name);
        this.ScatterPlotData.x.push(company.employees);
        this.ScatterPlotData.y.push(company.founding_year);
        if (company.category === 'health'){this.ScatterPlotData.colorType.push("lightgreen")}
        else if (company.category === 'bank'){this.ScatterPlotData.colorType.push("red")}
        else if (company.category === 'tech') {this.ScatterPlotData.colorType.push("darkcyan")}
        //console.log(company.name)
        //console.log(company.category)
      })
      // after the data is loaded, draw the plot
      this.drawScatterPlot();
    },
    drawScatterPlot() {
      //let colorList = []
      //var companyType = this.$props.selectedCategory;

      
      //console.log(this.ScatterPlotData.colorType)
      var trace1 = {
        y: this.ScatterPlotData.x,
        x: this.ScatterPlotData.y,
        mode: 'markers',
        type: 'scatter',
        text: this.ScatterPlotData.name,
        marker: {
          color: this.ScatterPlotData.colorType,
          size: 12
        }
      };
      /*
      var traceHealth = {
        y: this.ScatterPlotData.x,
        x: this.ScatterPlotData.y,
        mode: 'markers',
        type: 'scatter',
        text: this.ScatterPlotData.name,
        marker: {
          color: 'blue',
          size: 12
        }
      };
      var traceBank={
        y: this.ScatterPlotData.x,
        x: this.ScatterPlotData.y,
        mode: 'markers',
        type: 'scatter',
        text: this.ScatterPlotData.name,
        marker: {
          color: 'red',
          size: 12
        }
      };*/

      var data = [trace1];
      var layout = {

        xaxis: {
        title: {
          text: 'Years'}},
        yaxis: {
          title: {
          text: 'Money'}}};
      var config = {responsive: true, displayModeBar: false}
      Plotly.newPlot('myScatterPlot', data, layout, config);
      this.clickScatterPlot()
    },
    clickScatterPlot() {
      //PieChart.drawHiglighted();
      var that = this
      var myPlot = document.getElementById('myScatterPlot')
      myPlot.on('plotly_click', function (data) {
        for (var i = 0; i < data.points.length; i++) {

          // get the index of point
          let pn = data.points[i].pointNumber;

          // emit event to change the currently selected company in the a) configuration panel
          // and b) update the Profit View
          that.$emit('changeCurrentlySelectedCompany', pn + 1)

          // revert all colors
          //console.log(console.log(typeof this.ScatterPlotData.colorType))
         
          //var colors = ["#000000" * 15]
          var colors = []//Array(15).fill("#000000");
          for (var j = 0; j < 15; j++){
            colors.push(that.ScatterPlotData.colorType[j])
          }
         //console.log(that.ScatterPlotData.colorType)
          
          
          //colors = that.ScatterPlotData.colorType
          //console.log(typeof colors)

          // and change currently selected color to blue
          colors[pn] = '#3777ee';

          // update the marker and plot
          var update = {'marker': {color: colors, size: 12}};
          Plotly.restyle('myScatterPlot', update);
          //const myPlot = document.getElementById("myPieChart");
          //myPlot.dispatchEvent(new MouseEvent("click", { bubbles: true }));

        }
      });
    }
  },
  watch: {
   selectedCategory: function () {
   this.ScatterPlotData.x = [];
   this.ScatterPlotData.y = [];

    this.fetchData();
   }
   },
}
</script>
