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

    // console.log("graph data : ")
    // console.log(this.graphData.nodes[1]["label"])

    // Wait a tick to ensure container is sized
    await this.$nextTick();
    
    const containerWidth = this.$refs.graphContainer.clientWidth;
    const containerHeight = this.$refs.graphContainer.clientHeight;
    
    console.log("Container dimensions:", containerWidth, containerHeight);

    const nodes = new DataSet(
      this.graphData.nodes.map(n => ({
        ...n,
        group: n.label,
        size: 50
        
      }))
    );
    const edges = new DataSet(this.graphData.links.slice(0,1000));
    //console.log(nodes)

    const data = { nodes, edges };
    const options = {
      nodes:{
        shape : 'square',
        size: 60.6
        
       
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
        }
      }
    };

    this.networkInstance = new Network(this.$refs.graphContainer, data, options);
  }
},

  mounted() {
    this.fetchData()

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