<template>
  <div class="tag-filter-container">
    <div class="search-bar">
      <input type="text" placeholder="Search..." v-model="searchQuery" />
      <button @click="clearAllTags" class="clear-button">Clear All</button>
    </div>
    
    <div class="tag-panels">
      <!-- Not Selected Panel -->
      <div class="tag-panel">
        <h4>Not Selected</h4>
        <div class="tags-list">
          <button
            v-for="tag in availableTags"
            :key="tag.id"
            class="tag-button"
            :class="tag.color"
            @click="selectTag(tag)"
          >
            {{ tag.label }}
          </button>
        </div>
      </div>

      <!-- Selected Panel -->
      <div class="tag-panel selected-panel">
        <h4>Selected</h4>
        <div class="tags-list">
          <button
            v-for="tag in selectedTags"
            :key="tag.id"
            class="tag-button"
            :class="tag.color"
            @click="deselectTag(tag)"
          >
            {{ tag.label }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useFilters } from '../composables/useFilters';

const { updateFilter } = useFilters();

const searchQuery = ref('');

// All possible tags with their categories and colors- this would be much better if we didnt hardcode it. also not sure what to best do about the colors in here
const allTags = [
  // Languages
  { id: 'lat', label: 'LAT', category: 'language', color: 'dark' },
  { id: 'eng', label: 'ENG', category: 'language', color: 'dark' },
  { id: 'gre', label: 'GRE', category: 'language', color: 'dark' },
  { id: 'grc', label: 'GRC', category: 'language', color: 'dark' },
  { id: 'ger', label: 'GER', category: 'language', color: 'dark' },
  { id: 'fre', label: 'FRE', category: 'language', color: 'dark' },
  { id: 'ita', label: 'ITA', category: 'language', color: 'dark' },
  { id: 'spa', label: 'SPA', category: 'language', color: 'dark' },
  { id: 'wel', label: 'WEL', category: 'language', color: 'dark' },
  { id: 'ara', label: 'ARA', category: 'language', color: 'dark' },
  { id: 'heb', label: 'HEB', category: 'language', color: 'dark' },
  { id: 'non', label: 'NON', category: 'language', color: 'dark' },
  { id: 'dut', label: 'DUT', category: 'language', color: 'dark' },
  
  // Historical Periods
  { id: 'antiquity', label: 'Antiquity', category: 'period', color: 'red' },
  { id: 'middle-ages', label: 'Middle Ages', category: 'period', color: 'red' },
  { id: 'early-modern', label: 'Early Modern', category: 'period', color: 'red' },
  { id: 'long-nineteenth', label: 'Long Nineteenth Century', category: 'period', color: 'red' },
  { id: 'modern', label: 'Modern', category: 'period', color: 'red' },
  { id: 'contemporary', label: 'Contemporary', category: 'period', color: 'red' },
  
  // Writing Support
  { id: 'codex', label: 'Codex', category: 'support', color: 'dark' },
  { id: 'manuscript', label: 'Manuscript', category: 'support', color: 'dark' },
  { id: 'tablet', label: 'Tablet', category: 'support', color: 'dark' },
  { id: 'letter', label: 'Letter', category: 'support', color: 'dark' },
  { id: 'print', label: 'Print', category: 'support', color: 'dark' },
  { id: 'book', label: 'Book', category: 'support', color: 'dark' },
  { id: 'papyrus', label: 'Papyrus', category: 'support', color: 'dark' },
  { id: 'inscription', label: 'Inscription', category: 'support', color: 'dark' },
  { id: 'roll', label: 'Roll', category: 'support', color: 'dark' },
  { id: 'diary', label: 'Diary', category: 'support', color: 'dark' },
  { id: 'journal', label: 'Journal', category: 'support', color: 'dark' },
  
  // Features
  { id: 'xml-tei', label: 'XML-TEI download', category: 'feature', color: 'green' },
  { id: 'images', label: 'Images', category: 'feature', color: 'green' },
  { id: 'open-access', label: 'Open Access', category: 'feature', color: 'green' },
  { id: 'api', label: 'API', category: 'feature', color: 'green' },
  { id: 'scholarly', label: 'Scholarly', category: 'feature', color: 'green' },
  { id: 'digital', label: 'Digital', category: 'feature', color: 'green' },
  { id: 'glossary', label: 'Glossary', category: 'feature', color: 'green' },
  { id: 'transcription', label: 'Transcription', category: 'feature', color: 'green' },
];

const selectedTagIds = ref(new Set());

const availableTags = computed(() => {
  return allTags.filter(tag => {
    const isNotSelected = !selectedTagIds.value.has(tag.id);
    const matchesSearch = searchQuery.value === '' || 
      tag.label.toLowerCase().includes(searchQuery.value.toLowerCase());
    return isNotSelected && matchesSearch;
  });
});

const selectedTags = computed(() => {
  return allTags.filter(tag => selectedTagIds.value.has(tag.id));
});

const selectTag = (tag) => {
  selectedTagIds.value.add(tag.id);
  updateFilters();
};

const deselectTag = (tag) => {
  selectedTagIds.value.delete(tag.id);
  updateFilters();
};

const clearAllTags = () => {
  selectedTagIds.value.clear();
  updateFilters();
};

const updateFilters = () => {
  // Update filters based on selected tags
  const selected = Array.from(selectedTagIds.value);
  
  // Language filters
  const languages = allTags
    .filter(t => t.category === 'language' && selected.includes(t.id))
    .map(t => t.label);
  
  // Period filters
  const periods = allTags
    .filter(t => t.category === 'period' && selected.includes(t.id))
    .map(t => t.label);
  
  // Writing support filters
  const supports = allTags
    .filter(t => t.category === 'support' && selected.includes(t.id))
    .map(t => t.label);
  
  updateFilter('language', languages);
  updateFilter('historicalPeriod', periods);
  updateFilter('writingSupport', supports);
  
  // Feature filters (boolean)
  updateFilter('hasImages', selected.includes('images') ? 'yes' : null);
  updateFilter('openAccess', selected.includes('open-access') ? 'yes' : null);
  updateFilter('hasXMLTEI', selected.includes('xml-tei') ? 'yes' : null);
  updateFilter('hasAPI', selected.includes('api') ? 'yes' : null);
  updateFilter('scholarly', selected.includes('scholarly') ? 'yes' : null);
  updateFilter('digital', selected.includes('digital') ? 'yes' : null);
};
</script>

<style scoped>
.tag-filter-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: 100%;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-bar input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #d5d9df;
  border-radius: 6px;
  font-size: 13px;
  outline: none;
}

.search-bar input:focus {
  border-color: #4a90e2;
}

.clear-button {
  padding: 8px 16px;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: background 0.2s;
  white-space: nowrap;
}

.clear-button:hover {
  background: #d32f2f;
}

.tag-panels {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  flex: 1;
  min-height: 0;
}

.tag-panel {
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: white;
  border: 1px solid #d5d9df;
  border-radius: 8px;
  padding: 12px;
  min-height: 0;
  overflow: hidden;
}

.selected-panel {
  background: #f8f9fa;
}

h4 {
  margin: 0;
  font-size: 13px;
  font-weight: 600;
  color: #555;
  flex-shrink: 0;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  overflow-y: auto;
  align-content: flex-start;
  max-height: calc(4 * (22px + 6px));
}

.tag-button {
  padding: 6px 12px;
  border: none;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.tag-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.tag-button.dark {
  background: #2c3e50;
  color: white;
}

.tag-button.green {
  background: #4CAF50;
  color: white;
}

.tag-button.red {
  background: #f44336;
  color: white;
}
</style>
