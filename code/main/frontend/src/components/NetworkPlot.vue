<template>
  <div class="network-wrapper">
    <div ref='graphContainer' class="graph-container"></div>
  </div>
</template>


<script>

import ForceGraph from 'force-graph';

export default {

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
    console.log(responseData)

    this.graphData.nodes = responseData.nodes;
    this.graphData.links = responseData.links;

    console.log("graph data : ")
    console.log(this.graphData)

    // Wait a tick to ensure container is sized
    await this.$nextTick();
    
    const containerWidth = this.$refs.graphContainer.clientWidth;
    const containerHeight = this.$refs.graphContainer.clientHeight;
    
    console.log("Container dimensions:", containerWidth, containerHeight);

    this.graph = ForceGraph()(this.$refs.graphContainer)
      .graphData(this.graphData)
      .width(containerWidth)
      .height(containerHeight)
      .linkDirectionalArrowLength(0)
      .linkDirectionalArrowRelPos(0)
      .nodeLabel(node => node.label)
      .linkLabel(link => link.label)
      .onNodeClick(node => {
        alert(`Node clicked: ${node.label}`);
      })
      .onLinkClick(link => {
        alert(`Link clicked: ${link.label}`);
      })
      .d3Force('charge', d3.forceManyBody().strength(-60))
      .d3Force('link', d3.forceLink().distance(40))
      .d3Force('x', d3.forceX().strength(1))
      .d3Force('y', d3.forceY().strength(0.01));
  },
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