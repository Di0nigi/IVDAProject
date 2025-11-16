<template>
  <div class="layout">

    <div class="box sidebar">Source List</div>

    <!-- Column 2 (middle) -->
    <div class="box graph">Key Words Relation Graph</div>
    <div class="box sliders">Sliders Panel</div>
    <div class="box tag-filter">Tag Filter</div>
    <div class="box timeline">Timeline Plot</div>

    <!-- Column 3 (right) -->
    <div class="box small-chart">Bar Chart</div>
    <div class="box bar-select">Bar Chart Selection</div>
    <div class="box pca">PCA Plot</div>
    <div class="box reliability">Reliability Sliders</div>

  </div>
</template>

<style scoped>
.layout {
  display: grid;
  height: 100vh;
  padding: 20px;
  gap: 20px;

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
