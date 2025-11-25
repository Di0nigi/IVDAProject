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
          {{ tag.label }}
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
          {{ tag.label }}
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
          {{ tag.label }}
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
  { id: 'LAT', label: 'LAT' },
  { id: 'ENG', label: 'ENG' },
  { id: 'GER', label: 'GER' },
  { id: 'HUN', label: 'HUN' },
  { id: 'FRE', label: 'FRE' },
  { id: 'ITA', label: 'ITA' },
  { id: 'GRC', label: 'GRC' },
  { id: 'SPA', label: 'SPA' },
  { id: 'ENM', label: 'ENM' },
  { id: 'POL', label: 'POL' },
  { id: 'ARA', label: 'ARA' },
  { id: 'HEB', label: 'HEB' },
  { id: 'DUT', label: 'DUT' },
  { id: 'FRO', label: 'FRO' },
  { id: 'GMH', label: 'GMH' },
  { id: 'DEU', label: 'DEU' },
  { id: 'ANG', label: 'ANG' },
  { id: 'FRA', label: 'FRA' },
  { id: 'ARC', label: 'ARC' },
  { id: 'DAN', label: 'DAN' },
];
const supportTags = [
  { id: 'Manuscript', label: 'Manuscript' },
  { id: 'Letter', label: 'Letter' },
  { id: 'Manuscript_Print', label: 'Manuscript; Print' },
  { id: 'Codex', label: 'Codex' },
  { id: 'Print', label: 'Print' },
  { id: 'Book', label: 'Book' },
  { id: 'not_provided', label: 'not provided' },
  { id: 'Diary', label: 'Diary' },
  { id: 'Printed_book', label: 'Printed book' },
  { id: 'Manuscript_Letter', label: 'Manuscript; Letter' },
  { id: 'Journal', label: 'Journal' },
  { id: 'Manuscript_Book', label: 'Manuscript; Book' },
  { id: 'Tablet', label: 'Tablet' },
  { id: 'Print_edition', label: 'Print edition' },
  { id: 'List_diary_entry', label: 'List; diary entry' },
  { id: 'Printed_book_Manuscript', label: 'Printed book; Manuscript' },
  { id: 'Novel', label: 'Novel' },
  { id: 'Manuscript_Codex', label: 'Manuscript; Codex' },
  { id: 'Letter_postcard', label: 'Letter; postcard' },
  { id: 'Letter_manuscript', label: 'Letter; manuscript' },
  { id: 'Notebook', label: 'Notebook' },
  { id: 'Inscription', label: 'Inscription' },
  { id: 'Manuscript_Roll', label: 'Manuscript; Roll' },
  { id: 'Letter_diary_entry_list', label: 'Letter; diary entry; list' },
  { id: 'Paper', label: 'Paper' },
  { id: 'Oral_history_interviews_video_audio', label: 'Oral history interviews; video; audio' },
  { id: 'Minutes', label: 'Minutes' },
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
