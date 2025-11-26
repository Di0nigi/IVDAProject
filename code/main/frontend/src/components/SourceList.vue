<template>
  <div class="source-container">
    <div class="search-bar">
      <input type="text" placeholder="Search..." v-model="searchQuery" />
    </div>
    <ul class="source-list">
      <li v-for="text in searchFilteredEditions" :key="text.id" class="list-item">
        <a href="#" @click.prevent="selectEdition(text.id)">
          <div class="list-item-content">
            <span>{{ text['Edition name'] }}</span>
            <div class="dots-container">
              <span class="dot" :style="{ backgroundColor: getOcrColor(text) }" title="OCR/Keyed"></span>
              <span class="dot" :style="{ backgroundColor: getOpenAccessColor(text) }" title="Open Access"></span>
              <span class="dot" :style="{ backgroundColor: getReliabilityColor(text) }" title="Reliability"></span>
            </div>
          </div>
        </a>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useEditionsData } from '../composables/useEditionsData';

const searchQuery = ref('');
const { filteredEditions } = useEditionsData();

const emit = defineEmits(['select']);

function selectEdition(id) {
  const edition = filteredEditions.value.find(e => e.id === id);
  emit('select', edition);
}

const searchFilteredEditions = computed(() => {
  if (!searchQuery.value) return filteredEditions.value;
  return filteredEditions.value.filter(text =>
    text['Edition name']
      .toLowerCase()
      .includes(searchQuery.value.toLowerCase())
  );
});

function getOcrColor(edition) {
  if (!edition) return '#e0e0e0';
  const ocr = edition['OCR or keyed?'] || '';
  if (ocr.toLowerCase().includes('keyed')) {
    return '#4CAF50'; // green
  } else if (ocr.toLowerCase().includes('ocr')) {
    return '#2196F3'; // blue
  }
  return '#e0e0e0'; // default grey
}

function getOpenAccessColor(edition) {
  if (!edition) return '#e0e0e0';
  const oa = edition['Open source/Open access'] || '';
  if (oa.toLowerCase().includes('open access and open source')) {
    return '#66BB6A'; // brighter green
  } else if (oa.toLowerCase().includes('yes') || oa.toLowerCase().includes('open access')) {
    return '#4CAF50'; // green
  } else if (oa.toLowerCase().includes('partly')) {
    return '#FFC107'; // yellow
  } else if (oa.toLowerCase() === 'no') {
    return '#F44336'; // red
  }
  return '#e0e0e0'; // default grey
}

function getReliabilityColor(edition) {
  const score = edition.reliabilityScore || 0;
  const clamped = Math.max(0, Math.min(100, score));
  let r, g, b;
  const maxIntensity = 180;
  if (clamped <= 50) {
    r = maxIntensity;
    g = Math.round(maxIntensity * (clamped / 50));
    b = 0;
  } else {
    r = Math.round(maxIntensity * (1 - (clamped - 50) / 50));
    g = maxIntensity;
    b = 0;
  }
  return `rgb(${r},${g},${b})`;
}
</script>

<style scoped>
.source-container {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  margin-bottom: 12px;
}

.search-bar input {
  flex: 1;
  padding: 4px 8px;
  border: 1px solid #d5d9df;
  border-radius: 6px;
  font-size: 12px;
  outline: none;
}

.search-bar input:focus {
  border-color: #4a90e2;
}

.source-list {
  list-style: none;
  padding: 0;
  margin: 0;
  padding-right: 6px;
  overflow-y: auto;
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
  overflow-x: hidden;
}

.source-list a {
  color: #333;
  text-decoration: none;
  display: block;
  padding: 8px 12px;
  background: white;
  border: 1px solid #d5d9df;
  border-radius: 6px;
  transition: all 0.2s;
}

.source-list a:hover {
  filter: brightness(90%);
  border-color: #4a90e2;
}

.list-item {
  list-style: none;
}

.list-item-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-width: 0;
}

.dots-container {
  display: flex;
  gap: 4px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  position: relative;
  cursor: help;
}

.dot:hover::after {
  content: attr(title);
  position: absolute;
  bottom: 125%;
  left: 50%;
  transform: translateX(-50%);
  background: #333;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 10px;
  white-space: nowrap;
  z-index: 1000;
  opacity: 1;
  transition: opacity 0.2s;
}

.dot::after {
    content: attr(title);
    position: absolute;
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    background: #333;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 10px;
    white-space: nowrap;
    z-index: 1000;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s;
}
.list-item-content span {
  display: block;
  max-width: 70%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
