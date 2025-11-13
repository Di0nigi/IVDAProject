<template>
    <div>
      <v-row align="center" justify="center" class="mt-1 mb-0">
        <h3>Profit View of Company: {{ $props.selectedCompany }}</h3>
      </v-row>
      <div style="height: 90vh">
        <div id='myLinePlot' style="height: inherit"></div>
      </div>
    </div>
</template>
<script>
import Plotly from 'plotly.js/dist/plotly';
export default {
  name: "LinePlot",
  props: ["selectedCompany", "selectedAlgorithm"],
  data: () => ({
    //comp: ["alphabet","apple","amazon","microsoft","meta","united health","johnson and johnson","pfizer","cvs health","mckesson","ubs","credit suisse","jp morgan","goldman sachs","bank of america"],
    compDict:  new Map([["alphabet", 1], ["apple", 2],["amazon", 3],["microsoft", 4],["meta", 5],["united health", 6],["johnson and johnson", 7],["pfizer", 8],["cvs health", 9],["mckesson", 10],["ubs", 11],["credit suisse", 12],["jp morgan", 13],["goldman sachs", 14],["bank of america", 15]]),
    LinePlotData: {x: [], y: []}
  }),
  mounted() {
    //this.fillMap(),
    this.fetchData()
    

  },
  methods: {
    async fetchData() {
      // req URL to retrieve single company from backend
     // console.log("here3");
      //console.log(this.compDict.get(this.$props.selectedCompany));
      var reqUrl = 'http://127.0.0.1:5000/companies/' + this.compDict.get(this.$props.selectedCompany)+ '?algorithm=' + this.$props.selectedAlgorithm
      console.log("ReqURL " + reqUrl)
      // await response and data
      const response = await fetch(reqUrl);
      const responseData = await response.json();
      //console.log("data");
      //console.log(responseData);
      this.LinePlotData = {x: [], y: [], col:[]};
      //var i = 0;
      // transform data to usable by lineplot
      responseData.profit.forEach((profit) => {
        /*if (this.$props.selectedAlgorithm!=='none' && i==0 ){
          this.LinePlotData.col.push("red");
        }
        else{
          this.LinePlotData.col.push("blue")
        }*/

        this.LinePlotData.x.push(profit.year)
        this.LinePlotData.y.push(profit.value)
        //i++;
      })
      // draw the lineplot after the data is transformed
      this.drawLinePlot()
    },
    drawLinePlot() {
      
      var config = {responsive: true, displayModeBar: false}
      //Plotly.newPlot('myLinePlot', data, layout, config);

      var predData = {x: [], y: [],col : []}

      if (this.$props.selectedAlgorithm!=='none'){
        predData.x.push(this.LinePlotData.x.shift());
        predData.y.push(this.LinePlotData.y.shift());
        predData.col.push("red")
        predData.x.push(this.LinePlotData.x[0])
        predData.y.push(this.LinePlotData.y[0])
         predData.col.push("blue")
      }

      
      var trace1 = {
        x: this.LinePlotData.x,
        y: this.LinePlotData.y,
        name: "Recorded",
        //mode: "markers+lines",
        type: 'scatter',
      };
      console.log()
     var trace2 ={

      x: predData.x,
        y: predData.y,
        //mode: "markers+lines",
        type: 'scatter',
        name: "Projected",
        line: {
            color: predData.col,
            width: 2
              }

      }
      
      var data = [trace1,trace2];
      var layout = {
        xaxis: {
        title: {
          text: 'Years'}},
        yaxis: {
          title: {
          text: 'Profit'}}};
      Plotly.newPlot('myLinePlot', data, layout, config);
    }
  },
  watch: {
   selectedCompany() {
   this.LinePlotData.x = [];
   this.LinePlotData.y = [];
   //console.log("here2")

   this.fetchData();
   },
   selectedAlgorithm() {
   this.LinePlotData.x = [];
   this.LinePlotData.y = [];

   this.fetchData();
   }
   },
}
</script>