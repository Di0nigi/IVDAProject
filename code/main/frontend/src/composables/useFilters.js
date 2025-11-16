import { reactive, computed } from 'vue';

const filters = reactive({
  periodRange: [-600, 2000],
  historicalPeriod: [],
  scholarly: null,
  digital: null,
  hasImages: null,
  hasXMLTEI: null,
  hasAPI: null,
  openAccess: null,
  language: [],
  writingSupport: [],
});

export function useFilters() {
  const updateFilter = (filterName, value) => {
    filters[filterName] = value;
  };

  const resetFilters = () => {
    filters.periodRange = [-600, 2000];
    filters.historicalPeriod = [];
    filters.scholarly = null;
    filters.digital = null;
    filters.hasImages = null;
    filters.hasXMLTEI = null;
    filters.hasAPI = null;
    filters.openAccess = null;
    filters.language = [];
    filters.writingSupport = [];
  };

  const hasActiveFilters = computed(() => {
    return filters.periodRange[0] !== -600 ||
           filters.periodRange[1] !== 2000 ||
           filters.historicalPeriod.length > 0 ||
           filters.scholarly !== null ||
           filters.digital !== null ||
           filters.hasImages !== null ||
           filters.hasXMLTEI !== null ||
           filters.hasAPI !== null ||
           filters.openAccess !== null ||
           filters.language.length > 0 ||
           filters.writingSupport.length > 0;
  });

  return {
    activeFilters: filters,
    updateFilter,
    resetFilters,
    hasActiveFilters
  };
}
