<template>
  <div class="network-wrapper">
    <div ref='graphContainer' class="graph-container"></div>
  </div>
</template>


<script>

import { Network, DataSet } from "vis-network/standalone";

export default {

networkInstance: null,

data: () => ({
  graphData: {nodes: [], links: []},
}),
methods: {
  async fetchData() {
    var reqUrl = 'http://127.0.0.1:5000/texts/graphPoints'
    console.log("reqUrl" + reqUrl)

    const response = await fetch(reqUrl)
    console.log("got response")
    const responseData = await response.json();
    console.log("got response data: ")

    this.graphData.nodes = responseData.nodes;
    this.graphData.links = responseData.links;

    // Wait a tick to ensure container is sized
    await this.$nextTick();
    
    const containerWidth = this.$refs.graphContainer.clientWidth;
    const containerHeight = this.$refs.graphContainer.clientHeight;
    
    console.log("Container dimensions:", containerWidth, containerHeight);

    const parent = this.$el.parentElement;
    const rectWidth = parent.clientWidth;
    const rectHeight = parent.clientHeight;

    const groupPositions = {
      0: { x: -rectWidth/2 + rectWidth/4, y: -rectHeight/2 + rectHeight/4 },
      1: { x: rectWidth/2 - rectWidth/4, y: -rectHeight/2 + rectHeight/4 },  
      2: { x: 0, y: -rectHeight/2 + rectHeight/4 },                           
      3: { x: -rectWidth/4, y: 0 },                                           
      4: { x: rectWidth/4, y: 0 },                                            
      5: { x: -rectWidth/4, y: rectHeight/2 - rectHeight/4 },                 
      6: { x: rectWidth/4, y: rectHeight/2 - rectHeight/4 },                 
    };

    const nodes = new DataSet(
      this.graphData.nodes.map(n => ({
        ...n,
        group: n.label,
        size: 100,
        x: groupPositions[n.label]?.x,
        y: groupPositions[n.label]?.y,
        
      }))
    );



    const gravityNodes = [
    { id: "gravity_0", x: -200, y: -200, fixed: true, physics: false, hidden: true },
    { id: "gravity_1", x: -150, y: -150, fixed: true, physics: false, hidden: true },
    { id: "gravity_2", x: 200, y: 200, fixed: true, physics: false, hidden: true },
    { id: "gravity_3", x: 150, y: 150, fixed: true, physics: false, hidden: true },
    { id: "gravity_4", x: -50, y: -50, fixed: true, physics: false, hidden: true },
    { id: "gravity_5", x: 0, y: 0, fixed: true, physics: false, hidden: true },
    { id: "gravity_6", x: 50, y: 50, fixed: true, physics: false, hidden: true },
    ];

    const extraEdges = this.graphData.nodes.map(n => ({
      from: n.id,
      to: "gravity_" + n.label,
      hidden: true,
      physics: true
    }));

    const edges = new DataSet(this.graphData.links.slice(5000,6000));
    console.log(nodes) 

    nodes.add(gravityNodes);
    edges.add(extraEdges);

    const data = { nodes, edges };
    const options = {
      nodes:{
        shape : 'square',
        size: 100
      },
      edges: {
        width: 2
      },
      layout: {
        improvedLayout: false
      },   
      physics: {
        enabled: true,
        solver: "forceAtlas2Based", 
        forceAtlas2Based: {
          gravitationalConstant: -50, 
          centralGravity: 0.008,       
          springLength: 100,          
          springConstant: 0.005,       
          damping: 0.4,               
          avoidOverlap: 0.9,
        },
        stabilization: {
          iterations: 500,            
          updateInterval: 25
        },
      },
      groups: {
      0: { physics: { springLength: 1000, springConstant: 500 } },
      1: { physics: { springLength: 1000, springConstant: 500 } },
      2: { physics: { springLength: 1000, springConstant: 500 } },
      3: { physics: { springLength: 1000, springConstant: 500 } },
      4: { physics: { springLength: 1000, springConstant: 500 } },
      5: { physics: { springLength: 1000, springConstant: 500 } },
      6: { physics: { springLength: 1000, springConstant: 500 } }
      
      }
    };

    this.networkInstance = new Network(this.$refs.graphContainer, data, options);
  }
},

  mounted() {
    this.fetchData()

  },
}

// function groupToX(group) {
//   switch(group) {
//     case 0: return -200;
//     case 1: return -150;
//     case 2: return 200;
//     case 3: return 150;
//     case 4: return -50;
//     case 5: return 0;
//     case 6: return 50;
//   }
// }

// function groupToY(group) {
//   switch(group) {
//     case 0: return -200;
//     case 1: return -150;
//     case 2: return 200;
//     case 3: return 150;
//     case 4: return -50;
//     case 5: return 0;
//     case 6: return 50;
//   }
// }

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