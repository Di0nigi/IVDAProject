<template>
    <div>
      <v-row align="center" justify="center" class="mt-1 mb-0">
        <h3>Share of Total Profits (Year {{ this.$props.selectedYear }})</h3>
      </v-row>
      <div style="height: 60vh">
        <v-col>
        <div id='myPieChart'  style="height: inherit"></div>
        </v-col>
      </div>
    </div>
</template>
<script>
import Plotly from 'plotly.js/dist/plotly';
export default {
  name: "PieChart",
  props: ["selectedCategory","selectedYear","selectedCompany"],
  data: () => ({
    //comp: ["alphabet","apple","amazon","microsoft","meta","united health","johnson and johnson","pfizer","cvs health","mckesson","ubs","credit suisse","jp morgan","goldman sachs","bank of america"],
    compDict:  new Map([["alphabet", 1], ["apple", 2],["amazon", 3],["microsoft", 4],["meta", 5],["united health", 6],["johnson and johnson", 7],["pfizer", 8],["cvs health", 9],["mckesson", 10],["ubs", 11],["credit suisse", 12],["jp morgan", 13],["goldman sachs", 14],["bank of america", 15]]),
    yearDict:  new Map([["2021",0],["2020",1],["2019",2],["2018",3],["2017",4]]),
    PieChartData: {profits: [], names: []},
    pieColors:  ["#e6194b", "#3cb44b", "#4363d8", "#f58231", "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe", "#008080", "#e6beff", "#9a6324","#800000", "#aaffc3", "#808000"  ]
  
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
      var reqUrl = 'http://127.0.0.1:5000/companies?category=' + this.$props.selectedCategory
      console.log("ReqURL " + reqUrl)
      // await response and data
      const response = await fetch(reqUrl);
      const responseData = await response.json();
      //console.log("data");
      //console.log(responseData);
      this.PieChartData = {profits: [], names: []},
      
      responseData.forEach((company) => {
        //console.log(this.$props.selectedYear)
       this.PieChartData.profits.push(company.profit[this.yearDict.get(this.$props.selectedYear)].value);
       this.PieChartData.names.push(company.name);

      })
      
      
     this.drawPiePlot()
    },
    drawPiePlot() {
        var data = [{
        values: this.computePercentages(this.PieChartData.profits),
        labels: this.PieChartData.names,
        type: 'pie',
        textinfo: "label+percent",
        textposition: "outside",
        marker:{
          colors: this.pieColors
        }
        
        }];

        var layout = {
        height: 400,
        width: 400,
        showlegend: false,
        margin: {"t": 0, "b": 0, "l": 120, "r": 120},
        };
        var config = {responsive: true, displayModeBar: false}

        Plotly.newPlot('myPieChart', data, layout,config);
  },
  drawHiglighted(selectedLabel){
    
    //this.drawPiePlot();
  
    var that = this;
    
    var myPlot = document.getElementById('myScatterPlot')
    myPlot.on('plotly_click', function () {
      //console.log(data);
      var pieChart = document.getElementById("myPieChart");
      let currentColors = pieChart.data[0].marker.colors;
      console.log("quisono");
      console.log(selectedLabel);
      //console.log(currentColors);
      var labels = that.PieChartData.names;
      console.log(labels);
      let nColors = [];
      
      for (let i = 0; i<labels.length; i++){
        //console.log("eoeoe");
        if (labels[i] === selectedLabel){

            nColors.push("#e3fc03");
            console.log("reached");
            
        }
        else{
          nColors.push(currentColors[i]);

        }
      }
      let update = { marker: { colors: nColors } };
      Plotly.restyle("myPieChart", update);
      pieChart.data[0].marker.colors = currentColors;




    });
   // let labels = that.PieChartData.names;
    
    //console.log(currentColors)
    
   /*

    /*const colors = labels.map((l, i) =>
    l === selectedLabel ? "#3777ee" : currentColors[i]
  );*/

    

  },
  computePercentages(){
    let acc = 0;
    let out = [];
    for (let elem of this.PieChartData.profits) {
    acc += elem;
        }
    for (let v of this.PieChartData.profits) {
            out.push((v / acc) * 100);
        }

        return out;
  }
},
watch: {
   selectedCategory: function () {
   this.PieChartData.profits = [];
   this.PieChartData.names = [];

    this.fetchData();
   },
   selectedYear :
   function () {
   this.PieChartData.profits = [];
   this.PieChartData.names = [];
    //console.log("eoekgr;mdeb");
    this.fetchData();
    //console.log("eoekgr;mdeb");
   },
   selectedCompany: function () {
        //console.log("eoekgr;mdeb");
        this.PieChartData.profits = [];
        this.PieChartData.names = [];
        this.fetchData();
        this.drawHiglighted(this.$props.selectedCompany);}
   },
 
}
</script>