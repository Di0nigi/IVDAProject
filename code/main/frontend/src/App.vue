<template>
  <div class="layout">

    <div class="left-column">
      <div class="box summary">
        <Summary :edition="selectedEdition" />
      </div>

      <div class="box sidebar">
        <SourceList @select="selectedEdition = $event" />
      </div>
    </div>

    <!-- Column 2 (middle) -->
    <div class="boxMlPlots network"><NetworkPlot @select="selectedEdition = $event" :edition="selectedEdition"/></div>
    <div class="box filters-panel">
      <div style="flex: 4.5; min-width: 220px;">
        <NewTagFilter />
      </div>
      <div style="flex: 1; min-width: 140px;">
        <SlidersPanel />
      </div>
    </div>
    <div class="box timeline">
      <TimelinePlot :color-attribute="colorAttribute" @select="selectedEdition = $event" />
    </div>

    <!-- New Legend Box -->
    <ColorLegend class="legend-box" title="Legend" :color-map="categoryColorMap" />

    <!-- Column 3 (right) -->
    <div class="box small-chart">
      <BarChart 
        :xAttribute="xAttribute" 
        :categoryAttribute="colorAttribute"
        :xLabel="xLabel"
        :categoryLabel="colorAttribute"
        @update:xAttribute="xAttribute = $event"
        @update:xLabel="xLabel = $event"
      />
    </div>
    <div class="boxMlPlots pca"><PcaPlot /></div>
    <!-- <div class="box reliability">
      <ReliabilitySliders />
    </div> -->

  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useEditionsData } from './composables/useEditionsData';
import { useColorPalette } from './composables/useColorPalette';
import BarChart from './components/BarChart.vue';
import SlidersPanel from './components/SlidersPanel.vue';
import NewTagFilter from './components/NewTagFilter.vue';
import TimelinePlot from './components/TimelinePlot.vue';
import SourceList from './components/SourceList.vue';
import Summary from './components/Summary.vue';
import PcaPlot from './components/PcaPlot.vue';
import NetworkPlot from './components/NetworkPlot.vue';
import ColorLegend from './components/ColorLegend.vue';

const xAttribute = ref('Historical Period');
const xLabel = ref('Historical Period');
const selectedEdition = ref(null);

const { editions, fetchEditions } = useEditionsData();
const { precomputeColorsForAttribute, categoryColorMap } = useColorPalette();

const colorAttribute = 'Language';

onMounted(() => {
  fetchEditions();
});

watch(editions, (newEditions) => {
    if (newEditions && newEditions.length > 0) {
        precomputeColorsForAttribute(newEditions, colorAttribute);
        if (!selectedEdition.value) {
            const randomIndex = Math.floor(Math.random() * newEditions.length);
            selectedEdition.value = newEditions[randomIndex];
        }
    }
}, { immediate: true });
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

  grid-template-columns: 0.8fr 0.6fr 1.3fr 0.4fr  0.4fr;

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

.boxMlPlots {
  background: #f2f4f7;
  border-radius: 12px;
  padding: 0px;
  border: 1px solid #d5d9df;
  position: relative;
  z-index: 1;
  overflow: hidden;

  display: flex;
  justify-content: center;   /* horizontal center */
  align-items: center;       /* vertical center */
  
}

.left-column {
  grid-row: 1 / -1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.summary {
  display: flex;
  flex-direction: column;
  overflow: auto;
  flex: 2.5;
}

.sidebar {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  flex: 2;
}

.graph {
  grid-column: 2;
  grid-row: 1;
}

.filters-panel {
  grid-column: 2 / 6;
  grid-row: 4;
  display: flex;
  gap: 20px;
}

.timeline {
  grid-column: 3 / 5;
  grid-row: 3;
}

.legend-box {
  grid-column: 5;
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
  grid-column: 2;
  grid-row: 3;

  width: 100%;
  height: 100%;


  border: 1px solid #d5d9df;

}

.reliability {
  grid-column: 3;
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
