<template>
  <div class="layout">

    <div class="box summary">
      <Summary :edition="selectedEdition" />
    </div>

    <div class="box sidebar">
      <SourceList @select="selectedEdition = $event" />
    </div>

    <!-- Column 2 (middle) -->
    <div class="box network"><NetworkPlot /></div>
    <div class="box sliders">
      <SlidersPanel />
    </div>
    <div class="box tag-filter">
      <NewTagFilter />
    </div>
    <div class="box timeline">
      <TimelinePlot />
    </div>

    <!-- Column 3 (right) -->
    <div class="box small-chart">
      <BarChart 
        :xAttribute="xAttribute" 
        :categoryAttribute="categoryAttribute"
        :xLabel="xLabel"
        :categoryLabel="categoryLabel"
        @update:xAttribute="xAttribute = $event"
        @update:categoryAttribute="categoryAttribute = $event"
        @update:xLabel="xLabel = $event"
        @update:categoryLabel="categoryLabel = $event"
      />
    </div>
    <div class="boxScatter pca"><PcaPlot /></div>
    <!-- <div class="box reliability">
      <ReliabilitySliders />
    </div> -->

  </div>
</template>

<script setup>
import { VueForceGraph2D, VueForceGraph3D, VueForceGraphVR, VueForceGraphAR, GraphContextMenu } from 'vue-force-graph';
//app.use(VueForceGraph2D)
import { ref } from 'vue';
import BarChart from './components/BarChart.vue';
import BarChartSelector from './components/BarChartSelector.vue';
import SlidersPanel from './components/SlidersPanel.vue';
import NewTagFilter from './components/NewTagFilter.vue';
import ReliabilitySliders from './components/ReliabilitySliders.vue';
import TimelinePlot from './components/TimelinePlot.vue';
import SourceList from './components/SourceList.vue';
import Summary from './components/Summary.vue';
import PcaPlot from './components/PcaPlot.vue';
import NetworkPlot from './components/NetworkPlot.vue';

const xAttribute = ref('Historical Period');
const categoryAttribute = ref('Scholarly');
const xLabel = ref('Historical Period');
const categoryLabel = ref('Scholarly');
const selectedEdition = ref(null)
</script>

<style scoped>

.layout {
  display: grid;
  height: 100dvh;
  box-sizing: border-box;
  padding: 8px 0 8px 0;
  gap: 20px;
  width: 100%;
  max-width: 100%;

  grid-template-columns: 0.5fr 1fr 1fr 1fr 0.7fr;

  grid-template-rows: 1fr 1fr 1.5fr 1fr;
}

.box {
  background: #f2f4f7;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid #d5d9df;
  position: relative;
  z-index: 1;
}

.boxScatter {
  background: #f2f4f7;
  border-radius: 12px;
  padding: 0px;
  border: 1px solid #d5d9df;
  position: relative;
  z-index: 1;
  overflow: hidden;
  
}

.summary {
  grid-row: 1 / 3;
  display: flex;
  flex-direction: column;
  overflow: auto;
}

.sidebar {
  grid-row: 3 / 5;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.graph {
  grid-column: 2;
  grid-row: 1;
}

.sliders {
  grid-column: 5;
  grid-row: 4;
}

.tag-filter {
  grid-column: 2 / 5;
  grid-row: 4;
}

.timeline {
  grid-column: 2 / 5;
  grid-row: 3;
}

.network {
  grid-column: 2/4;
  grid-row: 1 / 3;
  overflow: hidden;
}

/* Right column */
.small-chart {
  grid-column: 4 / 6;
  grid-row: 1 / 3;
}

.pca {
  grid-column: 5;
  grid-row: 3;


  border: 1px solid #d5d9df;

}

.reliability {
  grid-column: 3;
  grid-row: 4;
}


</style>

<style>
html {
  color-scheme: light;
}


body {
  background: #ffffff;
  color: #000000;
  overflow: hidden;
}
</style>
