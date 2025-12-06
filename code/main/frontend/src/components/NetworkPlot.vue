<template>
  <div class="network-wrapper">
    <h3 class="plot-title">Edition Similarity Network</h3>
    <div v-if="updateStatus" class="update-status" :class="updateStatus">
      {{ updateStatus === 'updating' ? 'Updating...' : 'Up to date' }}
    </div>
    <div ref='graphContainer' class="graph-container"></div>
  <div class="weights-filter">
    <button v-for="opt in [1, 2, 3, 4, 5]"
      :key="opt"
      :class="{ active: selectedWeight === opt }"
      @click="selectedWeight = opt; changeWeights(opt)"
      :title="'Number of related tags'"
      :disabled="!isSelectable(opt)">
      {{ opt }}
    </button>
  </div>
  </div>
</template>


<script>


import { Network, DataSet } from "vis-network/standalone";
import { useEditionsData } from "../composables/useEditionsData";
import { useFilters } from "../composables/useFilters";
import { markRaw } from "vue";

export default {

emits: ['select'],
props: ['edition'],

networkInstance: null,

setup(props) {
  const { activeFilters } = useFilters();
  return { activeFilters };
},

data: () => ({
  fullGraphData: {nodes: [], links: []},
  graphData: {nodes: [], links: []},
  networkInstance: null,
  rawResponseData: null,
  updateDebounceTimer: null,
  updateStatus: null,
  hasChanges: false,
  periodicCheckInterval: null,
  lastFilterState: null,
  changeDebounceTimer: null,
  selectedWeight: 3,
}),

computed: {
  filteredEditions() {
    return useEditionsData().filteredEditions.value
  }
},


watch: {
  activeFilters: {
    handler(newVal) {
      if (this.rawResponseData && this.networkInstance) {
        if (this.changeDebounceTimer) {
          clearTimeout(this.changeDebounceTimer);
        }
        
        this.changeDebounceTimer = setTimeout(() => {
          const currentState = JSON.stringify(newVal);
          if (this.lastFilterState !== currentState) {
            console.log('Network: Filters changed, marking for update');
            this.hasChanges = true;
            this.lastFilterState = currentState;
          }
        }, 500);
      }
    },
    deep: true
  },
  edition: {
    handler(newEdition, oldEdition) {
      if (newEdition && this.networkInstance && this.networkInstance.body && this.networkInstance.body.data) {
        this.$nextTick(() => {
          try {
            this.networkInstance.unselectAll();
            this.networkInstance.selectNodes([newEdition.id]);
          } catch (error) {
            console.warn('Error selecting node:', error);
          }
        });
      }
    }
  }
},

async mounted() {
  await this.fetchData();
  this.loadGraph();
  
  let checkCount = 0;
  
  this.periodicCheckInterval = setInterval(() => {
    checkCount++;
    
    if (this.hasChanges) {
      console.log('Network: Starting update...');
      this.updateStatus = 'updating';
      this.hasChanges = false;
      

      this.updateNetwork();
      console.log('Network: Update complete');
      this.updateStatus = 'up-to-date';
      
      setTimeout(() => {
        this.updateStatus = null;
      }, 1000);
    } else {
    }
  }, 1000);
},

beforeUnmount() {
  if (this.periodicCheckInterval) {
    clearInterval(this.periodicCheckInterval);
  }
  if (this.networkInstance) {
    this.networkInstance.destroy();
  }
},

methods: {

  selectEdition(id) {
      console.log(this.filteredEditions)
      const edition = this.filteredEditions.find(e => e.id === id);
      console.log("edition", edition);
      this.$emit('select', edition);
  },

  changeWeights(weight) {
    if (!this.isSelectable(weight)) return;
    const filteredEdges = this.graphData.links.filter(edge => edge.weight === weight)
    const edgesDataSet = this.networkInstance.body.data.edges;
    console.log(filteredEdges.length, "hello")

    edgesDataSet.clear()

    edgesDataSet.update(filteredEdges)
  },

  isSelectable(weight) {
    const filteredEdges = this.graphData.links.filter(edge => edge.weight === weight)
    if (filteredEdges.length > 0) {
      return true
    }
    else {
      return false
    }
  },

  updateNetwork() {
    if (!this.networkInstance || !this.networkInstance.body) return;
    
    const filteredIds = new Set(this.filteredEditions.map(e => e.id));
    const nodesDataSet = this.networkInstance.body.data.nodes;
    const edgesDataSet = this.networkInstance.body.data.edges;
    const allNodeIds = nodesDataSet.getIds();
    const allEdges = edgesDataSet.get();
    const nodeBatchUpdates = [];
    const edgeBatchUpdates = [];
    
    for (let i = 0; i < allNodeIds.length; i++) {
      const nodeId = allNodeIds[i];
      const shouldShow = filteredIds.has(nodeId);
      
      nodeBatchUpdates.push({
        id: nodeId,
        opacity: shouldShow ? 1 : 0.2,
        color: {
          border: "#000000",
          background: "#c2e0ff",
          hover: {
            border: '#de0f00',
            background: '#D2E5FF'
          } 
        }
      });
    }

    for (let i = 0; i < allEdges.length; i++) {
      const edge = allEdges[i];

      const isConnected =
        filteredIds.has(edge.from) && filteredIds.has(edge.to);

      console.log("edge", edge.id, isConnected)

      edgeBatchUpdates.push({
        id: edge.id,
        hidden: isConnected ? false : true
      });
    }

    console.log(edgeBatchUpdates)
    
    nodesDataSet.update(nodeBatchUpdates);
    edgesDataSet.update(edgeBatchUpdates);
  },

  loadGraph() {
    const containerWidth = this.$refs.graphContainer.clientWidth;
    const containerHeight = this.$refs.graphContainer.clientHeight;
    
    console.log("Container dimensions:", containerWidth, containerHeight);

    const parent = this.$el.parentElement;
    const rectWidth = parent.clientWidth;
    const rectHeight = parent.clientHeight;

    const radiusX = rectWidth * 0.4;  
    const radiusY = rectHeight * 0.4;  

    const groupPositions = {};
    for (let i = 0; i < 5; i++) {
      const angle = (i / 5) * Math.PI * 2;

      groupPositions[i] = {
        x: Math.cos(angle) * radiusX,
        y: Math.sin(angle) * radiusY
      };
    }
    const maxRadius = 90;
    const minDist = 10;

    const placed = [];

    const nodes = new DataSet(
      this.graphData.nodes.map(n => {
        let x, y;
        let attempts = 0;

        const base = groupPositions[n.label] ?? { x: 0, y: 0 };
        do {
          const angle = Math.random() * Math.PI * 2;
          const r = Math.sqrt(Math.random()) * maxRadius;

          x = base.x + Math.cos(angle) * r;
          y = base.y + Math.sin(angle) * r;

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
          size: 4,
          borderWidth: 0.5,
          title: this.filteredEditions.find(e => e.id === n.id)["Edition name"],
          color: {
            border: "#000000",
            background: "#c2e0ff",
            hover: {
              border: '#de0f00',
              background: '#D2E5FF'} 
          },
          x,
          y,
        };
      })
    );

    const filteredEdges = this.graphData.links.filter(edge => edge.weight === 3)

    const edges = new DataSet(filteredEdges);  
    //console.log(nodes) 
    //console.log(filteredEdges.length, " number of links")
    //console.log(edges, " links")

    const data = { nodes, edges };
    const options = {
      interaction: { hover: true },
      nodes:{
        shape : 'square',
      },
      edges: {
        width: 1,
        color: {
          color: 'rgba(200,200,200,0.2)',
          highlight: 'rgb(0,0,0)',
        },
        selectionWidth: 2,
        smooth: false,
      },
      layout: {
        improvedLayout: false
      },   
      physics: {
        enabled: false
      },
      interaction: {
        hideEdgesOnDrag: true,
        hideEdgesOnZoom: true,
      }
    };
    
    this.networkInstance = markRaw(new Network(this.$refs.graphContainer, data, options));

    this.networkInstance.on('click', (properties) => {
        const ids = properties.nodes;
        const clickedNodes = nodes.get(ids);
        console.log('clicked nodes:', clickedNodes[0]?.id);
        if (clickedNodes.length > 0) {
          this.selectEdition(clickedNodes[0].id);
        }
    });

    this.networkInstance.on("showPopup", function (params) {
      
    });
    this.networkInstance.on("hidePopup", function () {
      console.log("hidePopup Event");
    });
  },
  
  async fetchData() {
    var reqUrl = 'http://127.0.0.1:5000/texts/graphPoints'
    console.log("reqUrl" + reqUrl)

    const response = await fetch(reqUrl)
    const responseData = await response.json();

    const filteredIds = new Set(this.filteredEditions.map(e => e.id));

    this.graphData.nodes = responseData.nodes.filter(node =>
      filteredIds.has(node.id)
    );
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

.weights-filterODp {
  position: fixed;
  top: 105px;
  left: 405px;
  z-index: 10;
  font-family: sans-serif;
  font-size: 1.1em;
  font-weight: 600;
  color: #000000;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.weights-filter {
  position: absolute;      /* relative to .network-wrapper */
  top: 23%;
  left: 2%;
  z-index: 20;             /* must be higher than graph canvas */
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-family: sans-serif;
  font-size: 1.1em;
  font-weight: 600;
  color: #000000;
}

.weights-filter button {
  padding: 6px 14px;
  margin-right: 6px;
  background: #e0e0e0;
  border-color: #1976d2;
  border-radius: 5px;
  border-width: 2px;
  cursor: pointer;
}

.weights-filter button.active {
  background: #9c9c9c;
  color: white;
}

.weights-filter button:disabled {
  background: #cccccc;
  color: #666666;
  border-color: #666666;
}

.weights-filter button:hover {
  background: #adadad;
}

.update-status {
  position: absolute;
  bottom: 10px;
  left: 10px;
  z-index: 10;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.update-status.updating {
  background: #FFC107;
  color: #333;
  animation: pulse 1.5s ease-in-out infinite;
}

.update-status.up-to-date {
  background: #4CAF50;
  color: white;
  animation: fadeIn 0.3s ease;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.8); }
  to { opacity: 1; transform: scale(1); }
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