<template>
  <div class="network-wrapper">
    <h3 class="plot-title">Edition Similarity Network</h3>
    <div ref='graphContainer' class="graph-container"></div>
  </div>
</template>


<script>


import { Network, DataSet } from "vis-network/standalone";
import { useEditionsData } from "../composables/useEditionsData";
import { watch, onMounted, nextTick } from "vue";


export default {

emits: ['select'],

networkInstance: null,

data: () => ({
  fullGraphData: {nodes: [], links: []},
  graphData: {nodes: [], links: []},
  networkInstance: null,
  rawResponseData: null
}),

computed: {
  filteredEditions() {
    return useEditionsData().filteredEditions.value
  }
},


watch: {
  filteredEditions: {
    handler(newVal) {
      if (this.rawResponseData) {
        this.networkInstance.destroy();
        this.$refs.graphContainer.innerHTML = "";

        const filteredIds = new Set(this.filteredEditions.map(e => e.id));

        this.graphData.nodes = this.fullGraphData.nodes.filter(node => filteredIds.has(node.id));
        this.graphData.links = [...this.fullGraphData.links];

        this.loadGraph();
      }
    },
    deep: true
  },
},

async mounted() {
  await this.fetchData();
  this.loadGraph();
},

methods: {

  selectEdition(id) {
      console.log(this.filteredEditions)
      const edition = this.filteredEditions.find(e => e.id === id);
      console.log("edition", edition);
      this.$emit('select', edition);
  },

  loadGraph() {
    const containerWidth = this.$refs.graphContainer.clientWidth;
    const containerHeight = this.$refs.graphContainer.clientHeight;
    
    console.log("Container dimensions:", containerWidth, containerHeight);

    const parent = this.$el.parentElement;
    const rectWidth = parent.clientWidth;
    const rectHeight = parent.clientHeight;

    const groupPositions = {
      0: { x: -rectWidth/2, y: -rectHeight/1.8},
      1: { x: rectWidth/2, y: -rectHeight/1.8},  
      2: { x: 0, y: -rectHeight/1.8 },                           
      3: { x: -rectWidth/2, y: 0 },                                           
      4: { x: rectWidth/2, y: 0 },                                            
      5: { x: -rectWidth/2, y: rectHeight/1.8},                 
      6: { x: rectWidth/2, y: rectHeight/1.8},                 
    };

    const maxRadius = 100;
    const minDist = 20;

    const placed = [];

    const nodes = new DataSet(
      this.graphData.nodes.map(n => {
        let x, y;

        let attempts = 0;
        do {
          const angle = Math.random() * Math.PI * 2;
          const r = Math.sqrt(Math.random()) * maxRadius;

          x = (groupPositions[n.label]?.x ?? 0) + Math.cos(angle) * r;
          y = (groupPositions[n.label]?.y ?? 0) + Math.sin(angle) * r;

          attempts++;
          if (attempts > 2000) break;
        } while (
          placed.some(p => {
            const dx = p.x - x;
            const dy = p.y - y;
            return dx * dx + dy * dy < minDist * minDist;
          })
        );

        placed.push({ x, y });

        return {
          ...n,
          group: n.label,
          size: 8,
          x,
          y,
        };
      })
    );

    const edges = new DataSet(this.graphData.links.slice(500,1000));
    console.log(nodes) 

    const data = { nodes, edges };
    const options = {
      nodes:{
        shape : 'square',
        size: 8
      },
      edges: {
        width: 1,
        color: {
          color: 'rgba(200,200,200,1)',
          highlight: 'rgb(0,0,0)'
        },
        selectionWidth: 3,
      },
      layout: {
        improvedLayout: false
      },   
      physics: {
        enabled: false
      },
    };
    
    this.networkInstance = new Network(this.$refs.graphContainer, data, options);

      this.networkInstance.on('click', (properties) => {
        const ids = properties.nodes;
        const clickedNodes = nodes.get(ids);
        console.log('clicked nodes:', clickedNodes[0].id);
        if (clickedNodes.length > 0) {
          this.selectEdition(clickedNodes[0].id);
        }
    });
  },
  
  async fetchData() {
    var reqUrl = 'http://127.0.0.1:5000/texts/graphPoints'
    console.log("reqUrl" + reqUrl)

    const response = await fetch(reqUrl)
    const responseData = await response.json();

    this.graphData.nodes = responseData.nodes;
    this.graphData.links = responseData.links;
    this.fullGraphData.nodes = responseData.nodes;
    this.fullGraphData.links = responseData.links;
    this.rawResponseData = responseData;
  }
},

}


</script>

<style scoped>
.plot-title {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 10;
  margin: 0;
  font-family: sans-serif;
  font-size: 1.1em;
  font-weight: 600;
  color: #333;
}
.network-wrapper {
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
  background: white;
}

.graph-container {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  background: white;
}

.graph-container canvas {
  max-width: 100% !important;
  max-height: 100% !important;
  display: block;
  background: white;
}
</style>