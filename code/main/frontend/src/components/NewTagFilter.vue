<template>
  <div class="category-titles-row">
    <div class="category-title">Language</div>
    <div class="category-title">Writing Support</div>
    <div class="category-title">Period</div>
    <div class="category-title">Keywords</div>
  </div>
  <div class="new-tag-filter-container">
    <div class="tag-category-box">
      <div class="tags-list">
        <button
          v-for="tag in languageTags"
          :key="tag.id"
          @click="toggleTag(tag, 'language')"
          :class="getTagClass(tag, 'language')"
        >
          {{ tag.label }}<span v-if="getTagClass(tag, 'language') === 'tag-selected'" style="margin-left:6px;display:inline-flex;align-items:center;position:relative;top:3px;">
            <svg width="16" height="16" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 10.5L9 14.5L15 7.5" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
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
          :class="getTagClass(tag, 'support')"
        >
          {{ tag.label }}<span v-if="getTagClass(tag, 'support') === 'tag-selected'" style="margin-left:6px;display:inline-flex;align-items:center;position:relative;top:3px;">
            <svg width="16" height="16" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 10.5L9 14.5L15 7.5" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
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
          :class="getTagClass(tag, 'period')"
        >
          {{ tag.label }}<span v-if="getTagClass(tag, 'period') === 'tag-selected'" style="margin-left:6px;display:inline-flex;align-items:center;position:relative;top:3px;">
            <svg width="16" height="16" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 10.5L9 14.5L15 7.5" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
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
          :class="getTagClass(tag, 'keyword')"
        >
          {{ tag.label }}<span v-if="getTagClass(tag, 'keyword') === 'tag-selected'" style="margin-left:6px;display:inline-flex;align-items:center;position:relative;top:3px;">
            <svg width="16" height="16" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 10.5L9 14.5L15 7.5" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useFilters } from '../composables/useFilters';

const { activeFilters, updateFilter } = useFilters();

const languageTags = ref([]);
const supportTags = [
  { id: 'Manuscript', label: 'Manuscript' },
  { id: 'Letter', label: 'Letter' },
  { id: 'Codex', label: 'Codex' },
  { id: 'Print', label: 'Print' },
  { id: 'Book', label: 'Book' },
  { id: 'not_provided', label: 'not provided' },
  { id: 'Diary', label: 'Diary' },
  { id: 'Printed_book', label: 'Printed book' },
  { id: 'Journal', label: 'Journal' },

  { id: 'Tablet', label: 'Tablet' },
  { id: 'Print_edition', label: 'Print edition' },
  { id: 'Novel', label: 'Novel' },
  { id: 'Notebook', label: 'Notebook' },
  { id: 'Inscription', label: 'Inscription' },
  { id: 'Paper', label: 'Paper' },
  { id: 'Minutes', label: 'Minutes' },
];

// Dynamic tags from backend
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

const toggleTag = (tag, category) => {
  let filterKey = category === 'period' ? 'historicalPeriod' : (category === 'language' ? 'language' : (category === 'support' ? 'writingSupport' : (category === 'keyword' ? 'keywords' : category)));
  let current = [...activeFilters[filterKey]];
  const lowercasedId = tag.id.toLowerCase();
  if (!current.includes(lowercasedId)) {
    current.push(lowercasedId);
  } else {
    current = current.filter(t => t !== lowercasedId);
  }
  updateFilter(filterKey, current);
};

const getTagClass = (tag, category) => {
  let filterKey = category === 'period' ? 'historicalPeriod' : (category === 'language' ? 'language' : (category === 'support' ? 'writingSupport' : (category === 'keyword' ? 'keywords' : category)));
  const isSelected = activeFilters[filterKey] && activeFilters[filterKey].includes(tag.id.toLowerCase());
  let hasSelectionInCategory = activeFilters[filterKey] && activeFilters[filterKey].length > 0;
  if (isSelected) return 'tag-selected';
  if (hasSelectionInCategory) return 'tag-muted';
  return 'tag-neutral';
};
</script>

<style scoped>
.category-titles-row {
  display: flex;
  gap: 8px;
  margin-bottom: 2px;
}
.category-title {
  flex: 1;
  text-align: center;
  font-size: 13px;
  font-weight: 600;
  color: #333;
  padding-bottom: 2px;
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
  border-radius: 4px;
  padding: 4px;
  overflow: hidden;
  height: 140px; /* Adjust as needed for your layout */
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

/* Remove max-height, let .tags-list fill parent and scroll */

.tag-button {
  padding: 1px 3px;
  border: none;
  border-radius: 2px;
  font-size: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.tag-neutral {
  background: #e0e0e0;
  color: #333;
}

.tag-button {
  padding: 2px 8px;
  border: none;
  border-radius: 2px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  min-height: 22px;
  line-height: 1.2;
}

.tag-neutral {
  background: #e0e0e0;
  color: #333;
  font-size: 13px;
  padding: 2px 8px;
}
.tag-selected {
  background: #4CAF50;
  color: white;
  font-size: 13px;
  padding: 2px 8px;
}
.tag-muted {
  background: #f5f5f5;
  color: #aaa;
  font-size: 13px;
  padding: 2px 8px;
}
</style>
