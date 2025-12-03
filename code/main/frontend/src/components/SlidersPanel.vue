<template>
  <div class="sliders-container">
    <h3>Filter Editions</h3>
    <div class="sliders-column">

      

      <!-- Authoritativeness Slider (dummy) -->
      <div class="slider-group">
        <label>Authority</label>
        <div class="slider-with-labels">
          <div class="single-slider-wrapper">
            <div class="single-track">
              <div class="single-fill" :style="authoritativenessStyle"></div>
            </div>
            <input
              type="range"
              v-model.number="authoritativeness"
              :min="0"
              :max="100"
              class="slider single-slider"
            />
          </div>
        </div>
      </div>

      <!-- Shared labels for both sliders -->
      

      <!-- Renown Slider (dummy) -->
      <div class="slider-group">
        <label>Renown</label>
        <div class="slider-with-labels">
          <div class="single-slider-wrapper">
            <div class="single-track">
              <div class="single-fill" :style="renownStyle"></div>
            </div>
            <input
              type="range"
              v-model.number="renown"
              :min="0"
              :max="100"
              class="slider single-slider"
            />
          </div>
        </div>

        <div class="shared-labels">
        <div class="range-labels">
          <span>High</span>
          <span>Medium</span>
          <span>Moderate</span>
        </div>
      </div>
      </div>
    </div>

    <button 
      @click="reset" 
      class="reset-button"
    >
      Reset all filters
    </button>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useFilters } from '../composables/useFilters';

const { resetFilters, updateFilter, activeFilters } = useFilters();

const authoritativeness = ref(activeFilters.authoritativeness ?? 0);
const renown = ref(activeFilters.renown ?? 0);

const authoritativenessStyle = computed(() => ({
  width: `${authoritativeness.value}%`
}));

const renownStyle = computed(() => ({
  width: `${renown.value}%`
}));

// Watchers to update filters when sliders change
watch(authoritativeness, (val) => {
  updateFilter('authoritativeness', val);
});

watch(renown, (val) => {
  updateFilter('renown', val);
});

const reset = () => {
  resetFilters();
  authoritativeness.value = 0;
  renown.value = 0;
  updateFilter('authoritativeness', 0);
  updateFilter('renown', 0);
};
</script>

<style scoped>
.sliders-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  height: 100%;
  padding: 1px;
  align-items: center;
  justify-content: center;
  
}

.sliders-row {
  display: flex;
  flex-direction: row;
  gap: 1px;
  align-items: center;
  justify-content: center;
  flex: 1;
}

.shared-labels {
  display: flex;
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
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.slider-with-labels {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 0;
}

label {
  font-size: 13px;
  font-weight: 500;
  color: #555;
  text-align: center;
  writing-mode: horizontal-tb;
}

.range-slider-wrapper {
  position: relative;
  height: 6px;
  flex: 1;
}

.single-slider-wrapper {
  position: relative;
  width: 200px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.range-track, .single-track {
  position: absolute;
  height: 6px;
  width: 100%;
  background: #e0e0e0;
  border-radius: 3px;
  

  top: 50%;
  transform: translateY(-50%);
  left: 0;
}

.range-fill {
  position: absolute;
  height: 6px;
  background: #000000;
  border-radius: 3px;
}

.single-fill {
  position: absolute;
  height: 6px;
  background: #000;
  border-radius: 3px;
  top: 50%;
  transform: translateY(-50%);
  bottom: 0;
}

.slider {
  position: absolute;
  width: 200px;
  height: 20px;
  border-radius: 3px;
  outline: none;
  writing-mode: bt-lr;
  background: transparent;
  top: 0;
  left: 0;
  margin: 0;
  cursor: pointer;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: white;
  border: 2px solid #000;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  transition: transform 0.2s ease;
}

.slider:hover::-webkit-slider-thumb {
  transform: scale(1.2);
}

.slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: white;
  border: 2px solid #000;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  transition: transform 0.2s ease;
}

.slider:hover::-moz-range-thumb {
  transform: scale(1.2);
}

.slider::-webkit-slider-runnable-track {
  background: transparent;
  width: 6px;
}

.slider::-moz-range-track {
  background: transparent;
  width: 6px;
}

.range-labels {
  flex-direction: row;
  height: auto;
  width: 200px;
  justify-content:space-around;
  display: flex;
  
  font-size: 10px;
  color: #666;
  text-align: justify;
  gap: 5px;
  padding: 0 10px;
}

.reset-button {
  padding: 6px 12px;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
  align-self: center;
  margin-left: 11px;
}

.reset-button:hover {
  filter: brightness(80%);
}
</style>
