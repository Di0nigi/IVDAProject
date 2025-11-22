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
      <TagFilter />
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
      />
    </div>
    <div class="box bar-select">
      <BarChartSelector 
        @update:xAttribute="xAttribute = $event"
        @update:categoryAttribute="categoryAttribute = $event"
        @update:xLabel="xLabel = $event"
        @update:categoryLabel="categoryLabel = $event"
      />
    </div>
    <div class="pca"><PcaPlot /></div>
    <!-- <div class="box reliability">
      <ReliabilitySliders />
    </div> -->

  </div>
</template>

<script setup>
import { ref } from 'vue';
import BarChart from './components/BarChart.vue';
import BarChartSelector from './components/BarChartSelector.vue';
import SlidersPanel from './components/SlidersPanel.vue';
import TagFilter from './components/TagFilter.vue';
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
  height: 100vh;
  padding: 20px 0 20px 0;
  gap: 20px;
  width: 100%;
  max-width: 100%;

  grid-template-columns: 1fr 2.5fr 1fr;

  grid-template-rows: 1fr 1fr 1fr 1fr;
}

.box {
  background: #f2f4f7;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid #d5d9df;
}

.summary {
  grid-row: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar {
  grid-row: 2 / 5;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.graph {
  grid-column: 2;
  grid-row: 1;
}

.sliders {
  grid-column: 2;
  grid-row: 2;
}

.tag-filter {
  grid-column: 2;
  grid-row: 3;
}

.timeline {
  grid-column: 2;
  grid-row: 4;
}

.network {
  grid-column: 2;
  grid-row: 1;
  width: 100%;
  height: 100%;          
  min-height: 200px;
  overflow: auto;  
}

/* Right column */
.small-chart {
  grid-column: 3;
  grid-row: 1;
}

.bar-select {
  grid-column: 3;
  grid-row: 2;
}

.pca {
  grid-row: 3 / span 2;
  overflow-y: off ;
  overflow-x: off ;
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
}
</style>
