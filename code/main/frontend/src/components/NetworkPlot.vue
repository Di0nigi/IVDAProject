<template>
  <div style="width: 100%; height: 100%; overflow: hidden;">
    <div ref='graphContainer' style="height: 100%; width: 100%;"></div>
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

    this.graph = ForceGraph()(this.$refs.graphContainer)
      .graphData(this.graphData)
      .width(this.$refs.graphContainer.clientWidth)
      .height(this.$refs.graphContainer.clientHeight)
      .linkDirectionalArrowLength(0) // disables arrows for undirected feel
      .linkDirectionalArrowRelPos(0)
      .nodeLabel(node => node.label) // shows node label on hover
      .linkLabel(link => link.label) // shows link label on hover
      .onNodeClick(node => {
        alert(`Node clicked: ${node.label}`);
      })
      .onLinkClick(link => {
        alert(`Link clicked: ${link.label}`);
      })
      .d3Force('charge', d3.forceManyBody().strength(-60))     // nodes repel more strongly
      .d3Force('link', d3.forceLink().distance(40))            // shorter links to compact clusters
      .d3Force('x', d3.forceX().strength(1))                 // push nodes horizontally
      .d3Force('y', d3.forceY().strength(0.01));;
  },
},

  mounted() {
    this.fetchData()

  },
}
</script>