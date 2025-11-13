<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col cols="12" md="2" class="sideBar">
          <v-row>
      <v-col cols="12" sm="12">
        <div class="control-panel-font">Company Overview</div>
      </v-col>
      </v-row>
      <v-row>
      <v-col cols="12" sm="12">
          <v-select
    :items="categories.values"
    label="Select a category"
    dense
    v-model="categories.selectedValue"
    @change="changeCategory"
    ></v-select>
    <v-row>
    <v-col cols="12" sm="12">
      <v-select
          :items="years.values"
          label="Select a year"
          dense
          v-model="years.selectedValue"
          @update:modelValue="changeYear"
      ></v-select>
    </v-col>
  </v-row>
      <v-row>
      <v-col cols="12" sm="12">
          <div class="control-panel-font">Profit View of Company</div>
      </v-col>
    
</v-row>
<v-row>
    <v-col cols="12" sm="12">
      <v-select
          :items="companies.values"
          label="Select a company"
          dense
          v-model="companies.selectedValue"
          @update:modelValue="this.changeCompany"
          
      ></v-select>
    </v-col>
  </v-row>
  <v-row>
    <v-col cols="12" sm="12">
      <v-select
          :items="algorithm.values"
          label="Select an algorithm for prediction"
          dense
          v-model="algorithm.selectedValue"
          @change="changeAlgorithm"
      ></v-select>
    </v-col>
  </v-row>
  <v-row v-if="poem" :key= linePlotId >
            <v-col cols="12" sm="10">
              <div class="containerPoem">
              <div class="control-panel-font"><strong>Poem:</strong></div>
              <div  class = "poemDisplay">
                 <div class="text-box" style="flex: 0 0 150px;" v-html="poem"></div>
              </div>
              </div>
              
            </v-col>
          </v-row>  

      </v-col>
      </v-row>
        </v-col>
        <v-col cols="12" md="3">
         <ScatterPlot  :key="scatterPlotId"
                 :selectedCategory="categories.selectedValue"
                 @changeCurrentlySelectedCompany="changeCurrentlySelectedCompany"
          />
        </v-col>
        <v-col cols="12" md="3">
          <LinePlot :key="linePlotId"
            :selectedCompany="companies.selectedValue"
            :selectedAlgorithm="algorithm.selectedValue"/>
        </v-col>
        <v-col cols="12" md="3">
          <PieChart :key="yearId"
          :selectedCategory="categories.selectedValue"
          :selectedYear="years.selectedValue"
          :selectedCompany="companies.selectedValue"
          @changeCurrentlySelectedCompany="changeCurrentlySelectedCompany"/>
          <p class="titleInfo">Company profit Info</p>
          <div class="infoDisplay">        
            <div class="text-box" style="flex: 0 0 150px;" v-html="groqInfo"></div>
            
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
import ScatterPlot from './ScatterPlot';
import LinePlot from './LinePlot';
import PieChart from './PieChart.vue';
export default {
  components: {ScatterPlot, LinePlot, PieChart},
  data: () => ({
    compDict:  new Map([["alphabet", 1], ["apple", 2],["amazon", 3],["microsoft", 4],["meta", 5],["united health", 6],["johnson and johnson", 7],["pfizer", 8],["cvs health", 9],["mckesson", 10],["ubs", 11],["credit suisse", 12],["jp morgan", 13],["goldman sachs", 14],["bank of america", 15]]),
    revCompDict : new Map([[1, "alphabet"],[2, "apple"],[3, "amazon"],[4, "microsoft"],[5, "meta"],[6, "united health"],[7, "johnson and johnson"],[8, "pfizer"],[9, "cvs health"],[10, "mckesson"],[11, "ubs"],[12, "credit suisse"],[13, "jp morgan"],[14, "goldman sachs"],[15, "bank of america"]]),
    yearDict:  new Map([["2021",0],["2020",1],["2019",2],["2018",3],["2017",4]]),
    scatterPlotId: 0,
    linePlotId: 0,
    yearId: 0,
    poem : "",
    groqInfo:"",
    categories: {
      values: ['All', 'tech', 'health', 'bank'],
      selectedValue: 'All'
    },
    companies: {
      values: ["alphabet","apple","amazon","microsoft","meta","united health","johnson and johnson","pfizer","cvs health","mckesson","ubs","credit suisse","jp morgan","goldman sachs","bank of america"], //[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
      selectedValue: "alphabet"
    },
    algorithm: {
      values: ['none', 'random', 'regression'],
      selectedValue: 'none'
    },
    years: {
      values : ["2017","2018","2019","2020","2021"],
      selectedValue : "2017"
    }
  }),
   mounted() {
    //this.fillMap();
    this.fetchPoem(this.companies.selectedValue);
    this.fetchAddInfo(this.companies.selectedValue);
  },
  methods:{
   async fetchPoem(companyId) {
      try {
        console.log(companyId);
        const response = await fetch('http://127.0.0.1:5000/poem/' + this.compDict.get(companyId));
        this.poem = await response.json();
        
      } catch (error) {
        console.error("Error fetching the poem:", error);
      }
    },
  async fetchAddInfo(companyId) {
      try {
        //console.log("crazyid");
        //console.log(companyId);
        var reqUrl = 'http://127.0.0.1:5000/companies/' + this.compDict.get(companyId)+ '?algorithm=' + 'none';
        //console.log("Fatto " + reqUrl)
      // await response and data
        const response0 = await fetch(reqUrl);
        const responseData = await response0.json();
        var profitSelected = 0;
        responseData.profit.forEach((profit) => {
          //console.log(profit);
          //console.log(this.years.selectedValue);
        if (profit.year.toString() === this.years.selectedValue){
          profitSelected=profit.value;
          //console.log(profitSelected);

        }
        
      
      })



        const response = await fetch('http://127.0.0.1:5000/info/' + this.compDict.get(companyId) + '?selectedYear=' + this.years.selectedValue + '&selectedProfit=' + profitSelected.toString());
        this.groqInfo = await response.json();
        //console.log(response);
        
      } catch (error) {
        console.error("Error fetching the info:", error);
      }
    },

    changeCurrentlySelectedCompany(companyId) {
        //console.log("here")
        //console.log(this.categories.selectedValue)
        var adjId = 0
        if (this.categories.selectedValue==="tech"){
          adjId = companyId
        }
        else if (this.categories.selectedValue==="health"){
          adjId = companyId+5

        }
        else if (this.categories.selectedValue==="bank"){
          adjId = companyId+10
        }
        else{
          adjId = companyId
        }
        console.log(adjId)
        this.companies.selectedValue = this.revCompDict.get(adjId)
        this.changeCompany()
        //console.log(companyId)
        //this.changeYear()
        
        },
    changeCategory() {
      this.scatterPlotId += 1
    },
    changeCompany() {
          //console.log(this.companies.selectedValue);
          this.fetchPoem(this.companies.selectedValue);
          this.fetchAddInfo(this.companies.selectedValue);
          this.linePlotId += 1
          
    },
    changeAlgorithm() {
          this.linePlotId += 1
    },
    changeYear(){
        this.fetchAddInfo(this.companies.selectedValue);
        this.yearId += 1
    }
  },
  
  
}
</script>
<style scoped>
.control-panel-font {
  font-family: "Open Sans", verdana, arial, sans-serif;
  align-items: center;
  font-size: 15px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  font-weight: 500;
  height: 40px;
  
}
.sideBar {
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: #fffee5;
  padding-left: 17px;
  height: calc(100vh - 50px);
  border-color: rgba(0, 0, 0, 0.253);
  border-width: 2px;
  box-shadow: #000000;
  border-radius: 0%;
}
.poemDisplay{

  height: 200px;      
  overflow-y: auto;   
  overflow-x: hidden;  
  border: 1px solid #ccc; 
  padding: 8px; 
  margin-top: 0px;

}
.infoDisplay{
  
  height: 200px;      
  overflow-y: auto;   
  overflow-x: hidden;  
  border: 1px solid #ccc; 
  padding: 8px; 

}
.titleInfo{
margin-top: -40px;

font-weight: bold;

}
.containerPoem{
  margin-top: -20px;
}
</style>