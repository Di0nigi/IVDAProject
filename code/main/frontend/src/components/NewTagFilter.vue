<template>
  <div class="new-tag-filter-container">
    <div class="tag-category-box">
      <h5>Language</h5>
      <div class="tags-list">
        <button
          v-for="tag in languageTags"
          :key="tag.id"
          @click="toggleTag(tag)"
          :class="getTagClass(tag)"
        >
          {{ tag.label }}
        </button>
      </div>
    </div>
    <div class="tag-category-box">
      <h5>Writing Support</h5>
      <div class="tags-list">
        <button
          v-for="tag in supportTags"
          :key="tag.id"
          @click="toggleTag(tag)"
          :class="getTagClass(tag)"
        >
          {{ tag.label }}
        </button>
      </div>
    </div>
    <div class="tag-category-box">
      <h5>Period</h5>
      <div class="tags-list">
        <button
          v-for="tag in periodTags"
          :key="tag.id"
          @click="toggleTag(tag)"
          :class="getTagClass(tag)"
        >
          {{ tag.label }}
        </button>
      </div>
    </div>
    <div class="tag-category-box">
      <h5>Keywords</h5>
      <div class="tags-list">
        <button
          v-for="tag in keywordTags"
          :key="tag.id"
          @click="toggleTag(tag)"
          :class="getTagClass(tag)"
        >
          {{ tag.label }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useFilters } from '../composables/useFilters';

const { updateFilter } = useFilters();

const selectedTagIds = ref(new Set());

// Placeholder tags, divided by category
const allTags = [
  // Languages
  { id: 'lat', label: 'LAT', category: 'language' },
  { id: 'eng', label: 'ENG', category: 'language' },
  { id: 'gre', label: 'GRE', category: 'language' },
  { id: 'grc', label: 'GRC', category: 'language' },
  { id: 'ger', label: 'GER', category: 'language' },
  { id: 'fre', label: 'FRE', category: 'language' },
  { id: 'ita', label: 'ITA', category: 'language' },
  { id: 'spa', label: 'SPA', category: 'language' },
  { id: 'wel', label: 'WEL', category: 'language' },
  { id: 'ara', label: 'ARA', category: 'language' },
  { id: 'heb', label: 'HEB', category: 'language' },
  { id: 'non', label: 'NON', category: 'language' },
  { id: 'dut', label: 'DUT', category: 'language' },
  
  // Historical Periods
  { id: 'antiquity', label: 'Antiquity', category: 'period' },
  { id: 'middle-ages', label: 'Middle Ages', category: 'period' },
  { id: 'early-modern', label: 'Early Modern', category: 'period' },
  { id: 'long-nineteenth', label: 'Long Nineteenth Century', category: 'period' },
  { id: 'modern', label: 'Modern', category: 'period' },
  { id: 'contemporary', label: 'Contemporary', category: 'period' },
  
  // Writing Support
  { id: 'codex', label: 'Codex', category: 'support' },
  { id: 'manuscript', label: 'Manuscript', category: 'support' },
  { id: 'tablet', label: 'Tablet', category: 'support' },
  { id: 'letter', label: 'Letter', category: 'support' },
  { id: 'print', label: 'Print', category: 'support' },
  { id: 'book', label: 'Book', category: 'support' },
  { id: 'papyrus', label: 'Papyrus', category: 'support' },
  { id: 'inscription', label: 'Inscription', category: 'support' },
  { id: 'roll', label: 'Roll', category: 'support' },
  { id: 'diary', label: 'Diary', category: 'support' },
  { id: 'journal', label: 'Journal', category: 'support' },
  
  // Keywords (Placeholders)
  { id: 'keyword1', label: 'Keyword 1', category: 'keyword' },
  { id: 'keyword2', label: 'Keyword 2', category: 'keyword' },
  { id: 'keyword3', label: 'Keyword 3', category: 'keyword' },
  { id: 'keyword4', label: 'Keyword 4', category: 'keyword' },
  { id: 'keyword5', label: 'Keyword 5', category: 'keyword' },
];

const languageTags = allTags.filter(tag => tag.category === 'language');
const supportTags = allTags.filter(tag => tag.category === 'support');
const periodTags = allTags.filter(tag => tag.category === 'period');
const keywordTags = allTags.filter(tag => tag.category === 'keyword');

const toggleTag = (tag) => {
  if (selectedTagIds.value.has(tag.id)) {
    selectedTagIds.value.delete(tag.id);
  } else {
    selectedTagIds.value.add(tag.id);
  }
  updateFilters();
};

const getTagClass = (tag) => {
  const isSelected = selectedTagIds.value.has(tag.id);
  const hasSelectionInCategory = allTags.some(t => t.category === tag.category && selectedTagIds.value.has(t.id));

  if (isSelected) {
    return 'tag-selected';
  }
  if (hasSelectionInCategory) {
    return 'tag-muted';
  }
  return 'tag-neutral';
};

const updateFilters = () => {
  const selected = Array.from(selectedTagIds.value);
  
  const languages = allTags
    .filter(t => t.category === 'language' && selected.includes(t.id))
    .map(t => t.label);
  
  const periods = allTags
    .filter(t => t.category === 'period' && selected.includes(t.id))
    .map(t => t.label);
  
  const supports = allTags
    .filter(t => t.category === 'support' && selected.includes(t.id))
    .map(t => t.label);

  // Note: Keywords are not yet hooked up to filters
  
  updateFilter('language', languages);
  updateFilter('historicalPeriod', periods);
  updateFilter('writingSupport', supports);
};
</script>

<style scoped>
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
  overflow-y: auto;
  align-content: flex-start;
}

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
