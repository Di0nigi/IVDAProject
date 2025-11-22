<template>
  <div>
    <div>
      <div ref='graphContainer' style="height: 100%; width: 100%;"></div>
    </div>
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
    const responseData = await response.json();
    console.log(responseData)

    this.graphData.nodes = responseData.nodes;
    this.graphData.links = responseData.links;

    this.graph = ForceGraph()(this.$refs.graphContainer)
      .graphData(this.graphData)
      .linkDirectionalArrowLength(0) // disables arrows for undirected feel
      .linkDirectionalArrowRelPos(0)
      .nodeLabel(node => node.label) // shows node label on hover
      .linkLabel(link => link.label) // shows link label on hover
      .onNodeClick(node => {
        alert(`Node clicked: ${node.label}`);
      })
      .onLinkClick(link => {
        alert(`Link clicked: ${link.label}`);
      });
  },
},

  mounted() {
    this.fetchData()

  },
}
</script>