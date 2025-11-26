<template>

  <div v-if="edition">
    
    <div class="slidersRel" v-if="scoreVis">
      <div class="column">

      
      <button @click="relScore()" >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M9 18l6-6-6-6"></path>
      </svg>
      </button>

      <div class="slidersContainer">
        <ReliabilitySliders />

        </div>
      </div>

    </div>

    <div v-else>

    <h2 style="margin-top: 0;">{{ edition['Edition name'] }}</h2>
    <div style="text-align: center; margin-bottom: 10px;">
        <a
          :href="edition['URL']"
          target="_blank"
          rel="noopener noreferrer"
          class="tag-button summary-pill"
          style="background:#1976d2; color:#fff; display:inline-flex; align-items:center; height:24px; margin-right:8px; vertical-align:middle;"
        >
          <span style="display:flex; align-items:center; justify-content:center; width:100%; height:100%;">Visit Website
            <svg style="margin-left:4px;" width="19" height="19" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M7 13L13 7M13 7H9M13 7V11" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </a>
    </div>
    <p> {{ edition.Content_Description }}</p>
    <div class="summary-tags-row">
      <div style="display: flex; flex-wrap: wrap; gap: 6px; align-items: center;">
        <button
          v-for="lang in splitTags(edition.Language)"
          :key="'lang-' + lang"
          class="tag-button summary-pill"
          @click="handleTagClick(lang, 'language')"
          :class="getTagClass(lang, 'language')"
        >
          {{ lang.toUpperCase() }}<span v-if="getTagClass(lang, 'language') === 'tag-selected'" style="margin-left:6px;display:inline-flex;align-items:center;">
            <svg width="15" height="15" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 10.5L9 14.5L15 7.5" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </button>
        <button
          v-for="support in splitTags(edition['Writing support'])"
          :key="'support-' + support"
          class="tag-button summary-pill"
          @click="handleTagClick(support, 'support')"
          :class="getTagClass(support, 'support')"
        >
          {{ support }}<span v-if="getTagClass(support, 'support') === 'tag-selected'" style="margin-left:6px;display:inline-flex;align-items:center;">
            <svg width="15" height="15" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 10.5L9 14.5L15 7.5" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </button>
        <button
          v-for="keyword in splitKeywords(edition.Keywords)"
          :key="'keyword-' + keyword"
          class="tag-button summary-pill"
          @click="handleTagClick(keyword, 'keyword')"
          :class="getTagClass(keyword, 'keyword')"
        >
          {{ keyword }}<span v-if="getTagClass(keyword, 'keyword') === 'tag-selected'" style="margin-left:6px;display:inline-flex;align-items:center;">
            <svg width="15" height="15" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 10.5L9 14.5L15 7.5" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </button>
        <button
          v-for="period in splitTags(edition['Historical Period'])"
          :key="'period-' + period"
          class="tag-button summary-pill"
          @click="handleTagClick(period, 'period')"
          :class="getTagClass(period, 'period')"
        >
          {{ period }}<span v-if="getTagClass(period, 'period') === 'tag-selected'" style="margin-left:6px;display:inline-flex;align-items:center;">
            <svg width="15" height="15" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 10.5L9 14.5L15 7.5" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </button>
        <div style="width:100%;height:1em;"></div>
        <button
          v-if="edition['OCR or keyed?']"
          class="tag-button summary-pill"
          :style="ocrPillStyle"
        >
          {{ edition['OCR or keyed?'] }}
        </button>
        <button
          v-if="edition['Open source/Open access']"
          class="tag-button summary-pill"
          :style="openAccessPillStyle"
        >
          {{ openAccessText }}
        </button>
        <button
          @click="relScore()"
          class="tag-button summary-pill"
          :style="reliabilityPillStyle"
        >
          Reliability: <span style="margin-left:6px;">{{score}}</span>
        </button>
      </div>
    
    <div style="margin-top:8px;margin-bottom:4px;">
      <p style="margin:0;text-align:left;"><strong>Manager:</strong> {{ edition['Manager or Editor'] }}</p>
      <p style="margin:0;text-align:left;"><strong>Author:</strong> {{ edition['author'] }}</p>
      <p style="margin:0;text-align:left;"><strong>Philosophical/Artistic Direction:</strong> {{ edition['phil_direction'] }}</p>
      <p style="margin:0;text-align:left;"><strong>Time/Century:</strong> {{ edition['Time/Century'] }}</p>
    </div>
    </div>
  </div>
  </div>


  <div v-else>
    <p>No edition selected</p>
  </div>  

</template>

<script setup>
import { defineProps, ref, computed } from 'vue'
import { useFilters } from '../composables/useFilters'
import ReliabilitySliders from '../components/ReliabilitySliders.vue';


const props = defineProps({
  edition: {
    type: Object,
    default: null
  }
})

var scoreVis = ref(false);

const score = computed(() => {
  if (props.edition) {
    return props.edition.reliabilityScore;
  }
  return 0;
});

const reliabilityPillStyle = computed(() => {
  // Convert score to number
  const s = Number(score.value);
  // Clamp between 0 and 100
  const clamped = Math.max(0, Math.min(100, s));
  // Interpolate color: 0=red, 50=yellow, 100=green
  let r, g, b;
  // Avoid very bright colors by reducing max intensity
  const maxIntensity = 180;
  if (clamped <= 50) {
    // Red to Yellow
    r = maxIntensity;
    g = Math.round(maxIntensity * (clamped / 50));
    b = 0;
  } else {
    // Yellow to Green
    r = Math.round(maxIntensity * (1 - (clamped - 50) / 50));
    g = maxIntensity;
    b = 0;
  }
  return {
    background: '#e0e0e0', // grey like other pills
    color: '#333',
    display: 'inline-flex',
    alignItems: 'center',
    height: '24px',
    fontWeight: 600,
    verticalAlign: 'middle',
    borderRadius: '12px',
    border: `3px solid rgb(${r},${g},${b})`,
    padding: '0 10px',
    boxSizing: 'border-box',
  };
});

const ocrPillStyle = computed(() => {
  if (!props.edition) return {};
  const ocr = props.edition['OCR or keyed?'] || '';
  let color = '#e0e0e0'; // default grey
  if (ocr.toLowerCase().includes('keyed')) {
    color = '#4CAF50'; // green
  } else if (ocr.toLowerCase().includes('ocr')) {
    color = '#2196F3'; // blue
  }
  return {
    background: color,
    color: 'white',
  };
});

const openAccessPillStyle = computed(() => {
  if (!props.edition) return {};
  const oa = props.edition['Open source/Open access'] || '';
  let color = '#e0e0e0'; // default grey
  if (oa.toLowerCase().includes('open access and open source')) {
    color = '#66BB6A'; // brighter green
  } else if (oa.toLowerCase().includes('yes') || oa.toLowerCase().includes('open access')) {
    color = '#4CAF50'; // green
  } else if (oa.toLowerCase().includes('partly')) {
    color = '#FFC107'; // yellow
  } else if (oa.toLowerCase() === 'no') {
    color = '#F44336'; // red
  }
  return {
    background: color,
    color: 'white',
  };
});

const openAccessText = computed(() => {
  if (!props.edition) return '';
  const oa = props.edition['Open source/Open access'] || '';
  if (oa.toLowerCase() === 'yes' || oa.toLowerCase() === 'open access') {
    return 'Open Access';
  }
  if (oa.toLowerCase().includes('open access and open source')) {
    return 'Open Access & Source';
  }
  return `Open Access: ${oa}`;
});


const { activeFilters, updateFilter } = useFilters();
const showReliability = ref(false);

function relScore(){

  //sc = Math.floor(Math.random()*101)

  //score = sc.toString()

  scoreVis.value = !scoreVis.value;

  console.log(scoreVis)

}

function splitTags(val) {
  if (!val) return [];
  return String(val).toLowerCase().split(/[,;]+/).map(t => t.trim()).filter(Boolean);
}

function splitKeywords(val) {
  if (!val) return [];
  return String(val).toLowerCase().split('#').map(t => t.trim()).filter(Boolean);
}

function handleTagClick(tag, category) {
  let filterKey = category === 'period' ? 'historicalPeriod' : (category === 'language' ? 'language' : (category === 'support' ? 'writingSupport' : (category === 'keyword' ? 'keywords' : category)));
  const lowercasedTag = typeof tag === 'string' ? tag.toLowerCase() : tag;
  let current = [...activeFilters[filterKey]];
  if (!current.includes(lowercasedTag)) {
    current.push(lowercasedTag);
  } else {
    current = current.filter(t => t !== lowercasedTag);
  }
  updateFilter(filterKey, current);
}

function getTagClass(tag, category) {
  let filterKey = category === 'period' ? 'historicalPeriod' : (category === 'language' ? 'language' : (category === 'support' ? 'writingSupport' : (category === 'keyword' ? 'keywords' : category)));
  const lowercasedTag = typeof tag === 'string' ? tag.toLowerCase() : tag;
  const isSelected = activeFilters[filterKey] && activeFilters[filterKey].includes(lowercasedTag);
  let hasSelectionInCategory = activeFilters[filterKey] && activeFilters[filterKey].length > 0;
  if (isSelected) return 'tag-selected';
  if (hasSelectionInCategory) return 'tag-muted';
  return 'tag-neutral';
}
</script>

<style scoped>

.summary-tags-row {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 10px;
}
.tag-button {
  padding: 1px 10px;
  border: none;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  min-height: 20px;
  line-height: 1.2;
}
.summary-pill {
  border-radius: 12px;
  height: 24px;
  padding: 0 10px;
  display: inline-flex;
  align-items: center;
  box-sizing: border-box;
}
.tag-neutral {
  background: #e0e0e0;
  color: #333;
  font-size: 12px;
  padding: 1px 10px;
}
.tag-selected {
  background: #4CAF50;
  color: white;
  font-size: 12px;
  padding: 1px 10px;
}
.tag-muted {
  background: #f5f5f5;
  color: #aaa;
  font-size: 12px;
  padding: 1px 10px;
}

.slidersRel{
  padding:0%;
  width: 100%;
  height: 100%;
}

.row{
  
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 50px;
}

.slidersContainer{
  display: flex;
  padding: 0%;
  width: 100%;
  height: 100%;

  

}
.btStyle{
  display: flex;
  border-radius: 100;
  background-color: #4CAF50;
  font-family: 'Courier New', Courier, monospace;
  justify-content: center;
  align-items: center;
  padding: 0;
  width: 40px;
  height: 30px;
  /* border-radius: 100; */
  /* background-color: #4CAF50; */
  /* width : 10;
  height: 10; */
}
.column{
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  gap: 50px;

}
</style>
