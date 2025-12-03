<template>
  <div class="network-wrapper">
    <h3 class="plot-title">Edition Similarity Network</h3>
    <div v-if="updateStatus" class="update-status" :class="updateStatus">
      {{ updateStatus === 'updating' ? 'Updating...' : 'Up to date' }}
    </div>
    <div ref='graphContainer' class="graph-container"></div>
  </div>
</template>


<script>


import { Network, DataSet } from "vis-network/standalone";
import { useEditionsData } from "../composables/useEditionsData";
import { useFilters } from "../composables/useFilters";
import { watch, onMounted, nextTick } from "vue";


export default {

emits: ['select'],

networkInstance: null,

setup() {
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
  changeDebounceTimer: null
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
        // Clear any pending change detection
        if (this.changeDebounceTimer) {
          clearTimeout(this.changeDebounceTimer);
        }
        
        // Wait 3000ms before marking as changed (batches rapid filter changes)
        this.changeDebounceTimer = setTimeout(() => {
          const currentState = JSON.stringify(newVal);
          if (this.lastFilterState !== currentState) {
            console.log('Network: Filters changed, marking for update');
            this.hasChanges = true;
            this.lastFilterState = currentState;
          }
        }, 3000);
      }
    },
    deep: true
  },
},

async mounted() {
  await this.fetchData();
  this.loadGraph();
  
  console.log('Network: Setting up 5-second update interval');
  let checkCount = 0;
  
  // Start periodic check for updates every 5 seconds
  this.periodicCheckInterval = setInterval(() => {
    checkCount++;
    console.log(`Network: Periodic check #${checkCount} (should be every 5 seconds)`);
    
    if (this.hasChanges) {
      console.log('Network: Starting update...');
      this.updateStatus = 'updating';
      this.hasChanges = false;
      
      setTimeout(() => {
        this.updateNetwork();
        console.log('Network: Update complete');
        this.updateStatus = 'up-to-date';
        
        setTimeout(() => {
          this.updateStatus = null;
        }, 2000);
      }, 100);
    } else {
      console.log('Network: No changes, skipping update');
    }
  }, 5000);
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

  updateNetwork() {
    if (!this.networkInstance || !this.networkInstance.body) return;
    
    const filteredIds = new Set(this.filteredEditions.map(e => e.id));
    const nodesDataSet = this.networkInstance.body.data.nodes;
    
    // Get all node IDs and update in batch
    const allNodeIds = nodesDataSet.getIds();
    const updates = [];
    
    for (let i = 0; i < allNodeIds.length; i++) {
      const nodeId = allNodeIds[i];
      const shouldShow = filteredIds.has(nodeId);
      const currentNode = nodesDataSet.get(nodeId);
      
      // Only update if visibility needs to change
      if (currentNode.hidden === shouldShow) {
        updates.push({
          id: nodeId,
          hidden: !shouldShow
        });
      }
    }
    
    // Single batch update
    if (updates.length > 0) {
      nodesDataSet.update(updates);
    }
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