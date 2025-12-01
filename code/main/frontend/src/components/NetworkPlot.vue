<template>
  <div class="network-wrapper">
    <div ref='graphContainer' class="graph-container"></div>
  </div>
</template>


<script>

import { Network, DataSet } from "vis-network/standalone";
import { useEditionsData } from "../composables/useEditionsData";


export default {

emits: ['select'],

networkInstance: null,

data: () => ({
  graphData: {nodes: [], links: []},
  networkInstance: null,
  filteredEditions: useEditionsData().filteredEditions
}),
methods: {

  selectEdition(id) {
      const edition = this.filteredEditions.find(e => e.id === id);
      console.log("edition", edition);
      this.$emit('select', edition);
  },
  
  async fetchData() {
    var reqUrl = 'http://127.0.0.1:5000/texts/graphPoints'
    console.log("reqUrl" + reqUrl)

    const response = await fetch(reqUrl)
    const responseData = await response.json();

    this.graphData.nodes = responseData.nodes;
    this.graphData.links = responseData.links;

    await this.$nextTick();
    
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
  }
},

  mounted() {
  this.$nextTick(() => {
    this.fetchData();
  });
  },
}


</script>

<style scoped>
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