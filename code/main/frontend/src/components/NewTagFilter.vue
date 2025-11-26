<template>
  <div class="category-controls-row">
    <div class="category-control">
      <span class="category-title">Language</span>
      <span class="reset-pill-wrapper">
        <button class="reset-pill" @click="resetCategory('language')">Reset</button>
      </span>
    </div>
    <div class="category-control">
      <span class="category-title">Writing Support</span>
      <span class="reset-pill-wrapper">
        <button class="reset-pill" @click="resetCategory('support')">Reset</button>
      </span>
    </div>
    <div class="category-control">
      <span class="category-title">Period</span>
      <span class="reset-pill-wrapper">
        <button class="reset-pill" @click="resetCategory('period')">Reset</button>
      </span>
    </div>
    <div class="category-control">
      <span class="category-title">Keywords</span>
      <span class="reset-pill-wrapper">
        <button class="reset-pill" @click="resetCategory('keyword')">Reset</button>
      </span>
    </div>
  </div>
  <div class="new-tag-filter-container">
    <div class="tag-category-box">
      <div class="tags-list">
        <button
          v-for="tag in languageTags"
          :key="tag.id"
          @click="toggleTag(tag, 'language')"
          :class="['tag-button', getTagClass(tag, 'language')]"
        >
          <span>{{ tag.label }}</span>
          <span v-if="getTagStatus(tag, 'language') === 'selected'">
            <svg width="16" height="16" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 10.5L9 14.5L15 7.5" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          <span v-if="getTagStatus(tag, 'language') === 'excluded'">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M6 6L18 18" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </button>
      </div>
    </div>
    <div class="tag-category-box">
      <div class="tags-list">
        <button
          v-for="tag in supportTags"
          :key="tag.id"
          @click="toggleTag(tag, 'support')"
          :class="['tag-button', getTagClass(tag, 'support')]"
        >
          <span>{{ tag.label }}</span>
          <span v-if="getTagStatus(tag, 'support') === 'selected'">
            <svg width="16" height="16" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 10.5L9 14.5L15 7.5" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          <span v-if="getTagStatus(tag, 'support') === 'excluded'">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M6 6L18 18" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </button>
      </div>
    </div>
    <div class="tag-category-box">
      <div class="tags-list">
        <button
          v-for="tag in periodTags"
          :key="tag.id"
          @click="toggleTag(tag, 'period')"
          :class="['tag-button', getTagClass(tag, 'period')]"
        >
          <span>{{ tag.label }}</span>
          <span v-if="getTagStatus(tag, 'period') === 'selected'">
            <svg width="16" height="16" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 10.5L9 14.5L15 7.5" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          <span v-if="getTagStatus(tag, 'period') === 'excluded'">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M6 6L18 18" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </button>
      </div>
    </div>
    <div class="tag-category-box">
      <div class="tags-list">
        <button
          v-for="tag in keywordTags"
          :key="tag.id"
          @click="toggleTag(tag, 'keyword')"
          :class="['tag-button', getTagClass(tag, 'keyword')]"
        >
          <span>{{ tag.label }}</span>
          <span v-if="getTagStatus(tag, 'keyword') === 'selected'">
            <svg width="16" height="16" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 10.5L9 14.5L15 7.5" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          <span v-if="getTagStatus(tag, 'keyword') === 'excluded'">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M6 6L18 18" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>

import { ref, onMounted } from 'vue';
import { useFilters } from '../composables/useFilters';

const { activeFilters, toggleTagFilter, resetTagCategory } = useFilters();

const languageTags = ref([]);
const supportTags = ref([]);
const keywordTags = ref([]);
const periodTags = ref([]);

onMounted(async () => {
  // Fetch languages
  try {
    const res = await fetch('http://localhost:5000/texts/language/name');
    const data = await res.json();
    const allLangs = data.flatMap(item => (item.Language || '').split(/[,;]+/)).map(l => l.trim().toLowerCase()).filter(Boolean);
    const uniqueLangs = Array.from(new Set(allLangs));
    languageTags.value = uniqueLangs.map(lang => ({ id: lang, label: lang.toUpperCase() }));
  } catch (e) {
    languageTags.value = [];
  }
  // Fetch writing supports
  try {
    const res = await fetch('http://localhost:5000/texts/writingsupport/name');
    const data = await res.json();
    const allSupports = data.flatMap(item => (item['Writing support'] || '').split(/[,;]+/)).map(s => s.trim().toLowerCase()).filter(Boolean);
    const uniqueSupports = Array.from(new Set(allSupports));
    supportTags.value = uniqueSupports.map(support => ({ id: support, label: support }));
  } catch (e) {
    supportTags.value = [];
  }
  // Fetch keywords
  try {
    const res = await fetch('http://localhost:5000/texts/tags');
    const data = await res.json();
    const processedTags = data.allTags.flatMap(tag => tag.split('#')).filter(tag => tag.trim() !== '');
    const uniqueTags = [...new Set(processedTags.map(t => t.toLowerCase()))];
    keywordTags.value = uniqueTags.map(tag => ({ id: tag, label: tag }));
  } catch (e) {
    keywordTags.value = [];
  }
  // Fetch periods
  try {
    const res = await fetch('http://localhost:5000/texts/period/name');
    const data = await res.json();
    // Deduplicate and clean up periods
    const allPeriods = data.flatMap(item => (item['Historical Period'] || '').split(/[,;]+/)).map(p => p.trim().toLowerCase()).filter(Boolean);
    const uniquePeriods = Array.from(new Set(allPeriods));
    periodTags.value = uniquePeriods.map(period => ({ id: period, label: period }));
  } catch (e) {
    periodTags.value = [];
  }
});

const getFilterKey = (category) => {
  return category === 'period' ? 'historicalPeriod' :
         category === 'language' ? 'language' :
         category === 'support' ? 'writingSupport' :
         'keywords';
}

const toggleTag = (tag, category) => {
  const filterKey = getFilterKey(category);
  toggleTagFilter(filterKey, tag.id);
};

const getTagStatus = (tag, category) => {
    const filterKey = getFilterKey(category);
    const lowercasedId = tag.id.toLowerCase();
    const tagState = activeFilters[filterKey].find(t => t.name === lowercasedId);
    if (tagState) return tagState.status;

    const hasSelectionInCategory = activeFilters[filterKey].some(t => t.status === 'selected');
    if (hasSelectionInCategory) return 'muted';
    return 'neutral';
}


const getTagClass = (tag, category) => {
    const status = getTagStatus(tag, category);
    return `tag-${status}`;
}

const resetCategory = (category) => {
  const filterKey = getFilterKey(category);
  if (typeof resetTagCategory === 'function') {
    resetTagCategory(filterKey);
  } else {
    // fallback: clear all filters in category
    if (activeFilters[filterKey]) {
      activeFilters[filterKey].splice(0, activeFilters[filterKey].length);
    }
  }
};
</script>

<style scoped>
.category-controls-row {
  display: flex;
  gap: 8px;
  margin-bottom: 4px;
}
.category-control {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex: 1;
  position: relative;
}
.category-title {
  font-size: 13px;
  font-weight: 600;
  color: #333;
}
.reset-pill-wrapper {
  display: flex;
  justify-content: flex-end;
  flex: 1;
}
.new-tag-filter-container {
  display: flex;
  gap: 8px;
  height: 100%;
}

.tag-category-box {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
  background: white;
  border: 1px solid #d5d9df;
  border-radius: 8px;
  padding: 4px;
  overflow: hidden;
  height: 140px; /* Adjust as needed for your layout */
  position: relative;
}

.category-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2px;
}

.reset-pill {
  font-size: 11px;
  font-weight: 500;
  padding: 2px 12px;
  border-radius: 999px;
  background: transparent;
  color: #555;
  border: none;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  box-shadow: none;
  outline: none;
  position: relative;
  z-index: 1;
}
.reset-pill:hover {
  background: #E53935;
  color: #fff;
}

.tag-category-box h5 {
  margin: 0;
  font-size: 13px;
  font-weight: 600;
  color: #555;
  flex-shrink: 0;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 2px;
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  align-content: flex-start;
}

.tag-button {
  padding: 2px 8px;
  border: 1px solid transparent;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  height: 22px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.tag-button:hover {
  filter: brightness(80%);
  border-color: #4a90e2;
}

.tag-neutral {
  background: #e0e0e0;
  color: #333;
}
.tag-selected {
  background: #4CAF50;
  color: white;
}
.tag-excluded {
  background: #E53935;
  color: white;
}
.tag-muted {
  background: #f5f5f5;
  color: #aaa;
}
</style>
