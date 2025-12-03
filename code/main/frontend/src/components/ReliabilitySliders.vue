<template>
  <div class="reliability-container">
    <h3>Reliability Score Influence</h3>
    
    <!-- Current Edition Score Display -->
    <div v-if="currentEdition" class="current-score">
      <div class="score-label">Current Edition Score:</div>
      <div class="score-value" :style="scoreStyle">{{ currentScore }}</div>
    </div>
    
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
import { ref, computed, watch, defineProps } from 'vue';
import { useFilters } from '../composables/useFilters';

const props = defineProps({
  edition: {
    type: Object,
    default: null
  }
});

const { updateReliabilityWeights } = useFilters();

const citations = ref(50);
const witnesses = ref(50);
const audience = ref(50);

const currentEdition = computed(() => props.edition);

const currentScore = computed(() => {
  if (!currentEdition.value) return 0;
  
  // Get binary values
  const citationVal = currentEdition.value.Citation_bin || 0;
  const witnessesVal = currentEdition.value.Value_of_witnesses_yes || 0;
  const audienceVal = currentEdition.value.Audience && 
                      currentEdition.value.Audience.toLowerCase() !== 'not provided' ? 1 : 0;
  
  // Calculate total weight
  const total = citations.value + witnesses.value + audience.value;
  if (total === 0) return 0;
  
  // Calculate weighted score
  const score = (citationVal * citations.value + 
                 witnessesVal * witnesses.value + 
                 audienceVal * audience.value) / total * 100;
  
  return Math.round(score);
});

const scoreStyle = computed(() => {
  const s = currentScore.value;
  let r, g, b;
  const maxIntensity = 200;
  if (s <= 50) {
    r = maxIntensity;
    g = Math.round(maxIntensity * (s / 50));
    b = 0;
  } else {
    r = Math.round(maxIntensity * (1 - (s - 50) / 50));
    g = maxIntensity;
    b = 0;
  }
  return {
    color: `rgb(${r},${g},${b})`,
    fontWeight: 'bold',
    fontSize: '24px'
  };
});

// Watch for slider changes and update global weights
watch([citations, witnesses, audience], () => {
  updateReliabilityWeights({
    citations: citations.value,
    witnesses: witnesses.value,
    audience: audience.value
  });
}, { immediate: true });

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

.current-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background: #f5f5f5;
  border-radius: 8px;
  margin-bottom: 16px;
}

.score-label {
  font-size: 12px;
  font-weight: 500;
  color: #555;
}

.score-value {
  font-size: 24px;
  font-weight: bold;
}
</style>
