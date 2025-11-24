<template>
  <div class="new-tag-filter-container">
    <div class="tag-category-box">
      <h5>Language</h5>
      <div class="tags-list">
        <button
          v-for="tag in languageTags"
          :key="tag.id"
          @click="toggleTag(tag, 'language')"
          :class="getTagClass(tag, 'language')"
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
          @click="toggleTag(tag, 'support')"
          :class="getTagClass(tag, 'support')"
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
          @click="toggleTag(tag, 'period')"
          :class="getTagClass(tag, 'period')"
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
          @click="toggleTag(tag, 'keyword')"
          :class="getTagClass(tag, 'keyword')"
        >
          {{ tag.label }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useFilters } from '../composables/useFilters';

const { updateFilter } = useFilters();
const selectedTagIds = ref(new Set());

// Hardcoded languages and supports (until backend endpoints are fixed)
const languageTags = [
  { id: 'lat', label: 'LAT' },
  { id: 'eng', label: 'ENG' },
  { id: 'gre', label: 'GRE' },
  { id: 'grc', label: 'GRC' },
  { id: 'ger', label: 'GER' },
  { id: 'fre', label: 'FRE' },
  { id: 'ita', label: 'ITA' },
  { id: 'spa', label: 'SPA' },
  { id: 'wel', label: 'WEL' },
  { id: 'ara', label: 'ARA' },
  { id: 'heb', label: 'HEB' },
  { id: 'non', label: 'NON' },
  { id: 'dut', label: 'DUT' },
];
const supportTags = [
  { id: 'codex', label: 'Codex' },
  { id: 'manuscript', label: 'Manuscript' },
  { id: 'tablet', label: 'Tablet' },
  { id: 'letter', label: 'Letter' },
  { id: 'print', label: 'Print' },
  { id: 'book', label: 'Book' },
  { id: 'papyrus', label: 'Papyrus' },
  { id: 'inscription', label: 'Inscription' },
  { id: 'roll', label: 'Roll' },
  { id: 'diary', label: 'Diary' },
  { id: 'journal', label: 'Journal' },
];

// Dynamic tags from backend
const keywordTags = ref([]);
const periodTags = ref([]);

onMounted(async () => {
  // Fetch keywords
  try {
    const res = await fetch('http://localhost:5000/texts/tags');
    const data = await res.json();
    keywordTags.value = data.allTags.map(tag => ({ id: tag, label: tag }));
  } catch (e) {
    keywordTags.value = [];
  }
  // Fetch periods
  try {
    const res = await fetch('http://localhost:5000/texts/period/name');
    const data = await res.json();
    // Deduplicate and clean up periods
    const uniquePeriods = Array.from(new Set(data.map(item => item['Historical Period'])));
    periodTags.value = uniquePeriods.map(period => ({ id: period, label: period }));
  } catch (e) {
    periodTags.value = [];
  }
});

const toggleTag = (tag, category) => {
  const tagId = `${category}:${tag.id}`;
  if (selectedTagIds.value.has(tagId)) {
    selectedTagIds.value.delete(tagId);
  } else {
    selectedTagIds.value.add(tagId);
  }
  updateFilters();
};

const getTagClass = (tag, category) => {
  const tagId = `${category}:${tag.id}`;
  const isSelected = selectedTagIds.value.has(tagId);
  let hasSelectionInCategory = false;
  for (let id of selectedTagIds.value) {
    if (id.startsWith(category + ':')) {
      hasSelectionInCategory = true;
      break;
    }
  }
  if (isSelected) return 'tag-selected';
  if (hasSelectionInCategory) return 'tag-muted';
  return 'tag-neutral';
};

const updateFilters = () => {
  const selected = Array.from(selectedTagIds.value);
  const languages = selected.filter(id => id.startsWith('language:')).map(id => id.split(':')[1]);
  const periods = selected.filter(id => id.startsWith('period:')).map(id => id.split(':')[1]);
  const supports = selected.filter(id => id.startsWith('support:')).map(id => id.split(':')[1]);
  const keywords = selected.filter(id => id.startsWith('keyword:')).map(id => id.split(':')[1]);
  updateFilter('language', languages);
  updateFilter('historicalPeriod', periods);
  updateFilter('writingSupport', supports);
  updateFilter('keywords', keywords);
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

/* Only for period and keywords tag lists: limit height to 4 tags and make scrollable */
.tag-category-box:nth-child(3) .tags-list,
.tag-category-box:last-child .tags-list {
  max-height: 96px; /* 4 tags * 22px height + gap */
  overflow-y: auto;
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
