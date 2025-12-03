import { reactive, computed } from 'vue';

const filters = reactive({
  periodRange: [-800, 2000],
  historicalPeriod: [],
  scholarly: null,
  digital: null,
  hasImages: null,
  hasXMLTEI: null,
  hasAPI: null,
  openAccess: null,
  language: [],
  writingSupport: [],
  keywords: [],
  reliabilityWeights: {
    citations: 50,
    witnesses: 50,
    audience: 50
  }
});

export function useFilters() {
  const updateFilter = (filterName, value) => {
    const tagFilters = ['historicalPeriod', 'language', 'writingSupport', 'keywords'];
    if (tagFilters.includes(filterName)) {
      console.warn(`updateFilter should not be used for ${filterName}. Use toggleTagFilter instead.`);
      return;
    }
    if (Array.isArray(value)) {
      filters[filterName] = value.map(v => typeof v === 'string' ? v.toLowerCase() : v);
    } else {
      filters[filterName] = value;
    }
  };

  const toggleTagFilter = (filterKey, tag) => {
    const lowerCaseTag = tag.toLowerCase();
    const filterArray = filters[filterKey];
    const existingTagIndex = filterArray.findIndex(t => t.name === lowerCaseTag);

    if (existingTagIndex === -1) {
      // Not selected -> Selected
      filterArray.push({ name: lowerCaseTag, status: 'selected' });
    } else {
      const existingTag = filterArray[existingTagIndex];
      if (existingTag.status === 'selected') {
        // Selected -> Excluded
        existingTag.status = 'excluded';
      } else {
        // Excluded -> Not selected
        filterArray.splice(existingTagIndex, 1);
      }
    }
  };

  const updateReliabilityWeights = (weights) => {
    filters.reliabilityWeights = { ...weights };
  };

  const resetFilters = () => {
    filters.periodRange = [-800, 2000];
    filters.historicalPeriod = [];
    filters.scholarly = null;
    filters.digital = null;
    filters.hasImages = null;
    filters.hasXMLTEI = null;
    filters.hasAPI = null;
    filters.openAccess = null;
    filters.language = [];
    filters.writingSupport = [];
    filters.keywords = [];
    filters.reliabilityWeights = {
      citations: 50,
      witnesses: 50,
      audience: 50
    };
  };

  const hasActiveFilters = computed(() => {
    return filters.periodRange[0] !== -800 ||
           filters.periodRange[1] !== 2000 ||
           filters.historicalPeriod.length > 0 ||
           filters.scholarly !== null ||
           filters.digital !== null ||
           filters.hasImages !== null ||
           filters.hasXMLTEI !== null ||
           filters.hasAPI !== null ||
           filters.openAccess !== null ||
           filters.language.length > 0 ||
           filters.writingSupport.length > 0 ||
           filters.keywords.length > 0;
  });

  return {
    activeFilters: filters,
    updateFilter,
    toggleTagFilter,
    updateReliabilityWeights,
    resetFilters,
    hasActiveFilters
  };
}
