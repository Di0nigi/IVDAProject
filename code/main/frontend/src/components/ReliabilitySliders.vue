<template>
  <div class="reliability-container">
    <h3>Reliability Score Influence</h3>
    
    <!-- Citations Slider -->
    <div class="slider-group">
      <label>Citations</label>
      <div style="flex: 1;">
      <div class="single-slider-wrapper">
        <div class="single-track">
          <div class="single-fill" :style="citationsStyle"></div>
        </div>
        <input
          type="range"
          v-model.number="citations"
          :min="0"
          :max="100"
          class="slider single-slider"
        />
      </div>
      <div class="range-labels">
        <span>low</span>
        <span>High</span>
      </div>
      </div>
    </div>

    <!-- Value of Witnesses Slider -->
    <div class="slider-group">
      <label>Value of Witnesses</label>
      <div style="flex: 1;">
      <div class="single-slider-wrapper">
        <div class="single-track">
          <div class="single-fill" :style="witnessesStyle"></div>
        </div>
        <input
          type="range"
          v-model.number="witnesses"
          :min="0"
          :max="100"
          class="slider single-slider"
        />
      </div>
      <div class="range-labels">
        <span>low</span>
        <span>High</span>
      </div>
      </div>
    </div>

    <!-- Audience Slider -->
    <div class="slider-group">
      <label>Audience</label>
      <div style="flex: 1;">
      <div class="single-slider-wrapper">
        <div class="single-track">
          <div class="single-fill" :style="audienceStyle"></div>
        </div>
        <input
          type="range"
          v-model.number="audience"
          :min="0"
          :max="100"
          class="slider single-slider"
        />
      </div>
      <div class="range-labels">
        <span>low</span>
        <span>High</span>
      </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const citations = ref(50);
const witnesses = ref(50);
const funding = ref(50);
const audience = ref(50);

const citationsStyle = computed(() => {
  const percent = citations.value;
  return {
    width: `${percent}%`
  };
});

const witnessesStyle = computed(() => {
  const percent = witnesses.value;
  return {
    width: `${percent}%`
  };
});

const fundingStyle = computed(() => {
  const percent = funding.value;
  return {
    width: `${percent}%`
  };
});

const audienceStyle = computed(() => {
  const percent = audience.value;
  return {
    width: `${percent}%`
  };
});
</script>

<style scoped>
.reliability-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
  padding: 4px;
  width: 100%;
}

h3 {
  margin: 0;
  font-size: 14px;
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
  font-size: 12px;
  font-weight: 500;
  color: #555;
  min-width: 140px;
  flex-shrink: 0;
}

.single-slider-wrapper {
  position: relative;
  height: 6px;
  flex: 1;
}

.single-track {
  position: absolute;
  width: 100%;
  height: 6px;
  background: #e0e0e0;
  border-radius: 3px;
  top: 0;
  left: 0;
}

.single-fill {
  position: absolute;
  height: 6px;
  background: #000;
  border-radius: 3px;
  left: 0;
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
  border: 2px solid #000;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  pointer-events: all;
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
  pointer-events: all;
  transition: transform 0.2s ease;
}

.slider:hover::-moz-range-thumb {
  transform: scale(1.2);
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
  font-size: 10px;
  color: #666;
  margin-top: 2px;
}
</style>
