<!--
  DEPRECATED: This component is no longer used.
  The functionality has been integrated directly into BarChart.vue as a settings popup.
  This file can be safely deleted.
-->

<template>
  <div class="selector-container">
    <h3>Bar Chart Selection</h3>
    
    <div class="selector-group">
      <label for="x-attribute">X-Axis (Groups):</label>
      <select 
        id="x-attribute" 
        v-model="selectedX" 
        @change="emitSelection"
        class="selector"
      >
        <option v-for="attr in attributes" :key="attr.value" :value="attr.value">
          {{ attr.label }}
        </option>
      </select>
    </div>

    <div class="selector-group">
      <label for="category-attribute">Categories (Stack):</label>
      <select 
        id="category-attribute" 
        v-model="selectedCategory" 
        @change="emitSelection"
        class="selector"
      >
        <option v-for="attr in attributes" :key="attr.value" :value="attr.value">
          {{ attr.label }}
        </option>
      </select>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const emit = defineEmits(['update:xAttribute', 'update:categoryAttribute', 'update:xLabel', 'update:categoryLabel']);

const selectedX = ref('Historical Period');
const selectedCategory = ref('Scholarly');

// Available attributes from the dataset, preliminary. we should either build an endpoint to get this or adjust so only sensible attributes can be used.
const attributes = [
  { value: 'Historical Period', label: 'Historical Period' },
  { value: 'Scholarly', label: 'Scholarly' },
  { value: 'Writing support', label: 'Writing Support' },
  { value: 'Language', label: 'Language' },
  { value: 'Open source/Open access', label: 'Open Access' },
  { value: 'OCR or keyed?', label: 'OCR/Keyed' },
  { value: 'Print facsimile (complementary output)', label: 'Print Facsimile' },
  { value: 'Audience', label: 'Audience' },
  { value: 'Institution(s)', label: 'Institution' },
];

const emitSelection = () => {
  const xAttr = attributes.find(a => a.value === selectedX.value);
  const catAttr = attributes.find(a => a.value === selectedCategory.value);
  
  emit('update:xAttribute', selectedX.value);
  emit('update:categoryAttribute', selectedCategory.value);
  emit('update:xLabel', xAttr?.label || selectedX.value);
  emit('update:categoryLabel', catAttr?.label || selectedCategory.value);
};

// Emit initial values
emitSelection();
</script>

<style scoped>
.selector-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
}

h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.selector-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-size: 13px;
  font-weight: 500;
  color: #555;
}

.selector {
  padding: 8px 12px;
  border: 1px solid #d5d9df;
  border-radius: 6px;
  background: white;
  font-size: 13px;
  color: #333;
  cursor: pointer;
  transition: border-color 0.2s;
}

.selector:hover {
  border-color: #999;
}

.selector:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.1);
}
</style>
