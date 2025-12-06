<template>
  <div class="color-legend">
    <div class="legend-title">{{ title }}</div>
    <ul class="legend-items">
      <li v-for="[category, color] in colorMap" :key="category" class="legend-item">
        <span class="color-swatch" :style="{ backgroundColor: color }"></span>
        <span class="category-name">{{ category }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: 'Legend'
  },
  colorMap: {
    type: Map,
    required: true
  }
});
</script>

<style scoped>
.color-legend {
  background: #f2f4f7;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid #d5d9df;
  
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow: hidden; /* Hide overflow on the main container */
}
.legend-title {
  font-weight: 600;
  font-size: 14px;
  border-bottom: 1px solid #d5d9df;
  padding-bottom: 8px;
  margin-bottom: 4px;
  flex-shrink: 0; /* Prevent title from shrinking */
}
.legend-items {
  list-style: none;
  padding: 0;
  margin: 0;
  overflow-y: auto; /* Allow this part to scroll */
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}
.color-swatch {
  width: 14px;
  height: 14px;
  border-radius: 4px;
  flex-shrink: 0;
}
.category-name {
  font-size: 12px;
  color: #333;
}
</style>
