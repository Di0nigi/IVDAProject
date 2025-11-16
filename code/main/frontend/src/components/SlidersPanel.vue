<template>
  <div class="sliders-container">
    <div class="header">
      <h3>Filters</h3>
      <button @click="reset" class="reset-button">Reset Filters</button>
    </div>
    
    <!-- Time/Century Range Slider -->
    <div class="slider-group">
      <label>Time/Century</label>
      <div style="flex: 1;">
      <div class="range-slider-wrapper">
        <div class="range-track">
          <div class="range-fill" :style="rangeStyle"></div>
        </div>
        <input
          type="range"
          v-model.number="periodRange[0]"
          :min="-600"
          :max="2000"
          :step="100"
          @input="updatePeriodFilter"
          class="slider range-slider"
        />
        <input
          type="range"
          v-model.number="periodRange[1]"
          :min="-600"
          :max="2000"
          :step="100"
          @input="updatePeriodFilter"
          class="slider range-slider"
        />
      </div>
      <div class="range-labels">
        <span>-600</span>
        <span>0</span>
        <span>400</span>
        <span>800</span>
        <span>1200</span>
        <span>1600</span>
        <span>2000</span>
      </div>
      </div>
    </div>

    <!-- Authoritativeness Slider (dummy) -->
    <div class="slider-group">
      <label>Authoritativeness</label>
      <div style="flex: 1;">
      <div class="single-slider-wrapper">
        <div class="single-track">
          <div class="single-fill reverse" :style="authoritativenessStyle"></div>
        </div>
        <input
          type="range"
          v-model.number="authoritativeness"
          :min="0"
          :max="100"
          class="slider single-slider"
        />
      </div>
      <div class="range-labels">
        <span>Moderate</span>
        <span>Medium</span>
        <span>High</span>
      </div>
      </div>
    </div>

    <!-- Renown Slider (dummy) -->
    <div class="slider-group">
      <label>Renown</label>
      <div style="flex: 1;">
      <div class="single-slider-wrapper">
        <div class="single-track">
          <div class="single-fill reverse" :style="renownStyle"></div>
        </div>
        <input
          type="range"
          v-model.number="renown"
          :min="0"
          :max="100"
          class="slider single-slider"
        />
      </div>
      <div class="range-labels">
        <span>obscure</span>
        <span>lesser known</span>
        <span>known</span>
        <span>well</span>
        <span>ubiquitous</span>
      </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useFilters } from '../composables/useFilters';

const { activeFilters, updateFilter, resetFilters } = useFilters();

const periodRange = ref([-600, 2000]);
const authoritativeness = ref(50);
const renown = ref(50);

onMounted(() => {
  periodRange.value = [...activeFilters.periodRange];
});

const rangeStyle = computed(() => {
  const min = periodRange.value[0];
  const max = periodRange.value[1];
  const totalRange = 2000 - (-600);
  const leftPercent = ((min - (-600)) / totalRange) * 100;
  const rightPercent = ((max - (-600)) / totalRange) * 100;
  
  return {
    left: `${leftPercent}%`,
    width: `${rightPercent - leftPercent}%`
  };
});

const authoritativenessStyle = computed(() => {
  const percent = authoritativeness.value;
  return {
    width: `${100 - percent}%`,
    left: `${percent}%`
  };
});

const renownStyle = computed(() => {
  const percent = renown.value;
  return {
    width: `${100 - percent}%`,
    left: `${percent}%`
  };
});

const updatePeriodFilter = () => {
  // Ensure min is not greater than max
  if (periodRange.value[0] > periodRange.value[1]) {
    const temp = periodRange.value[0];
    periodRange.value[0] = periodRange.value[1];
    periodRange.value[1] = temp;
  }
  updateFilter('periodRange', [...periodRange.value]);
};

const reset = () => {
  resetFilters();
  periodRange.value = [-600, 2000];
  authoritativeness.value = 50;
  renown.value = 50;
};
</script>

<style scoped>
.sliders-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
  padding: 4px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.slider-group {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
}

label {
  font-size: 13px;
  font-weight: 500;
  color: #555;
  min-width: 120px;
  flex-shrink: 0;
}

.range-slider-wrapper {
  position: relative;
  height: 6px;
  flex: 1;
}

.single-slider-wrapper {
  position: relative;
  height: 6px;
  flex: 1;
}

.range-track, .single-track {
  position: absolute;
  width: 100%;
  height: 6px;
  background: #e0e0e0;
  border-radius: 3px;
  top: 0;
  left: 0;
}

.range-fill {
  position: absolute;
  height: 6px;
  background: #4CAF50;
  border-radius: 3px;
}

.single-fill {
  position: absolute;
  height: 6px;
  background: #4CAF50;
  border-radius: 3px;
}

.single-fill.reverse {
  right: 0;
}

.slider {
  position: absolute;
  width: 100%;
  height: 6px;
  border-radius: 3px;
  outline: none;
  -webkit-appearance: none;
  appearance: none;
  background: transparent;
  top: 0;
  left: 0;
  margin: 0;
  pointer-events: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: white;
  border: 2px solid #4CAF50;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  pointer-events: all;
}

.slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: white;
  border: 2px solid #4CAF50;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  pointer-events: all;
}

.slider::-webkit-slider-runnable-track {
  background: transparent;
  height: 6px;
}

.slider::-moz-range-track {
  background: transparent;
  height: 6px;
}

.range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: #666;
  margin-top: 4px;
}

.reset-button {
  padding: 6px 12px;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: background 0.2s;
}

.reset-button:hover {
  background: #d32f2f;
}
</style>
