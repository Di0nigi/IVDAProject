<template>
  <div class="layout">

    <div class="box sidebar">Source List</div>

    <!-- Column 2 (middle) -->
    <div class="box graph">Key Words Relation Graph</div>
    <div class="box sliders">
      <SlidersPanel />
    </div>
    <div class="box timeline">Timeline Plot</div>

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
    <div class="box pca">PCA Plot</div>
    <div class="box reliability">
      <ReliabilitySliders />
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue';
import BarChart from './components/BarChart.vue';
import BarChartSelector from './components/BarChartSelector.vue';
import SlidersPanel from './components/SlidersPanel.vue';
import ReliabilitySliders from './components/ReliabilitySliders.vue';

const xAttribute = ref('Historical Period');
const categoryAttribute = ref('Scholarly');
const xLabel = ref('Historical Period');
const categoryLabel = ref('Scholarly');
</script>

<style scoped>
.layout {
  display: grid;
  height: 100vh;
  padding: 20px 0 20px 0;
  gap: 20px;
  width: 1400px;

  /* middle column ~2.5x the width of right column */
  grid-template-columns: 200px 2.5fr 1fr;

  /* four equal-height rows for each column */
  grid-template-rows: 1fr 1fr 1fr 1fr;
}

.box {
  background: #f2f4f7;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid #d5d9df;
}

/* Left sidebar spans all rows */
.sidebar {
  grid-row: 1 / 5;
}

/* Middle column */
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
  grid-column: 3;
  grid-row: 3;
}

.reliability {
  grid-column: 3;
  grid-row: 4;
}
</style>
