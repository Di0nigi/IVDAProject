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

    <h2>{{ edition['Edition name'] }}</h2>
    <div class="summary-tags-row">
      <button
        v-for="lang in splitTags(edition.Language)"
        :key="'lang-' + lang"
        class="tag-button summary-pill"
        @click="handleTagClick(lang, 'language')"
        :class="getTagClass(lang, 'language')"
      >
        {{ lang }}
      </button>
      <button
        v-for="support in splitTags(edition['Writing support'])"
        :key="'support-' + support"
        class="tag-button summary-pill"
        @click="handleTagClick(support, 'support')"
        :class="getTagClass(support, 'support')"
      >
        {{ support }}
      </button>

      <button
        v-if="edition['Historical Period']"
        class="tag-button summary-pill"
        @click="handleTagClick(edition['Historical Period'], 'period')"
        :class="getTagClass(edition['Historical Period'], 'period')"
      >
        {{ edition['Historical Period'] }}
      </button>
    
    <p><strong>Manager:</strong> {{ edition['Manager or Editor'] }}</p>
    <p><strong>Author:</strong> {{ edition['author'] }}</p>
    <p><strong>Philosophical/Artistic Direction:</strong> {{ edition['phil_direction'] }}</p>
    <a :href="edition['URL']" target="_blank" rel="noopener noreferrer" style="display:block;">
      <strong>Link: </strong> {{ edition['URL'] }}
    </a>
    <p><strong>OCR or keyed?:</strong> {{ edition['OCR or keyed?'] }}</p>
    <div class="row">
    <p ><strong>Time/Century:</strong> {{ edition['Time/Century'] }}</p>
    <div class="scoreBox">
       <button @click="relScore()" class="btStyle"  >
        <span> {{score}} </span>
       </button>
    </div>
    </div>
    <p> {{ edition.Content_Description }}</p>
    </div>
  </div>
  </div>


  <div v-else>
    <p>No edition selected</p>
  </div>  

</template>

<script setup>
import { defineProps, ref } from 'vue'
import { useFilters } from '../composables/useFilters'
import ReliabilitySliders from '../components/ReliabilitySliders.vue';


const props = defineProps({
  edition: {
    type: Object,
    default: null
  }
})

var scoreVis = ref(false);

var sc = Math.floor(Math.random()*101)

var score = sc.toString()

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
  return String(val).split(/[,;]+/).map(t => t.trim()).filter(Boolean);
}

function handleTagClick(tag, category) {
  let filterKey = category === 'period' ? 'historicalPeriod' : (category === 'language' ? 'language' : (category === 'support' ? 'writingSupport' : category));
  let current = [...activeFilters[filterKey]];
  if (!current.includes(tag)) {
    current.push(tag);
  } else {
    current = current.filter(t => t !== tag);
  }
  updateFilter(filterKey, current);
}

function getTagClass(tag, category) {
  let filterKey = category === 'period' ? 'historicalPeriod' : (category === 'language' ? 'language' : (category === 'support' ? 'writingSupport' : category));
  return activeFilters[filterKey].includes(tag) ? 'tag-selected' : 'tag-neutral';
}
</script>

<style scoped>

.summary-tags-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 10px;
}
.tag-button {
  padding: 2px 14px;
  border: none;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  min-height: 22px;
  line-height: 1.2;
}
.summary-pill {
  border-radius: 16px;
}
.tag-neutral {
  background: #e0e0e0;
  color: #333;
  font-size: 13px;
  padding: 2px 14px;
}
.tag-selected {
  background: #4CAF50;
  color: white;
  font-size: 13px;
  padding: 2px 14px;
}
.tag-muted {
  background: #f5f5f5;
  color: #aaa;
  font-size: 13px;
  padding: 2px 14px;
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
