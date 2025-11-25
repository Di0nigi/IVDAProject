<template>
  <div v-if="edition">
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
    </div>
    <p><strong>Author/Manager:</strong> {{ edition['Manager or Editor'] }}</p>
    <p><strong>Time/Century:</strong> {{ edition['Time/Century'] }}</p>
    <p> {{ edition.Content_Description }}</p>
  </div>

  <div v-else>
    <p>No edition selected</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import { useFilters } from '../composables/useFilters'

const props = defineProps({
  edition: {
    type: Object,
    default: null
  }
})

const { activeFilters, updateFilter } = useFilters();

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
</style>
