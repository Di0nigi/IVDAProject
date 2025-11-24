import { ref, computed } from 'vue';
import { useFilters } from './useFilters';

const editions = ref([]);
const loading = ref(true);
const error = ref(null);
let fetched = false;

export function useEditionsData() {
  const { activeFilters } = useFilters();

  // Fetch data once on first use
  const fetchEditions = async () => {
    if (fetched) return;
    fetched = true;
    
    try {
      const response = await fetch('http://127.0.0.1:5000/texts');
      editions.value = await response.json();
      loading.value = false;
    } catch (err) {
      console.error('Error fetching editions:', err);
      error.value = err;
      loading.value = false;
    }
  };

  // Computed filtered data
  const filteredEditions = computed(() => {
    let filtered = editions.value;

    // Apply period range filter - include if period_start or period_end falls within range
    if (activeFilters.periodRange) {
      const [min, max] = activeFilters.periodRange;
      filtered = filtered.filter(e => {
        const start = e.period_start;
        const end = e.period_end;
        
        // Include if either start or end falls within the selected range
        return (start !== undefined && start >= min && start <= max) ||
               (end !== undefined && end >= min && end <= max) ||
               // Also include if the work spans the entire selected range
               (start !== undefined && end !== undefined && start <= min && end >= max);
      });
    }

    // Apply historical period filter (OR logic within category)
    if (activeFilters.historicalPeriod?.length > 0) {
      filtered = filtered.filter(e =>
        activeFilters.historicalPeriod.includes(e['Historical Period'])
      );
    }

    // Apply scholarly filter
    if (activeFilters.scholarly !== null) {
      filtered = filtered.filter(e => e.Scholarly === activeFilters.scholarly);
    }

    // Apply digital filter
    if (activeFilters.digital !== null) {
      filtered = filtered.filter(e => e.Digital === activeFilters.digital);
    }

    // Apply images filter
    if (activeFilters.hasImages !== null) {
      if (activeFilters.hasImages === 'yes') {
        filtered = filtered.filter(e => e.Images === 'yes' || e.Images === 'partly');
      } else {
        filtered = filtered.filter(e => e.Images === activeFilters.hasImages);
      }
    }

    // Apply XML-TEI filter
    if (activeFilters.hasXMLTEI !== null) {
      if (activeFilters.hasXMLTEI === 'yes') {
        filtered = filtered.filter(e => 
          e['XML-TEI Transcription'] === 'yes' || e['XML-TEI Transcription'] === 'partly'
        );
      } else {
        filtered = filtered.filter(e => e['XML-TEI Transcription'] === activeFilters.hasXMLTEI);
      }
    }

    // Apply API filter
    if (activeFilters.hasAPI !== null) {
      filtered = filtered.filter(e => e.API === activeFilters.hasAPI);
    }

    // Apply open access filter
    if (activeFilters.openAccess !== null) {
      if (activeFilters.openAccess === 'yes') {
        filtered = filtered.filter(e => {
          const oa = e['Open source/Open access'];
          return oa && (oa.includes('Open Access') || oa === 'yes' || oa === 'partly');
        });
      } else {
        filtered = filtered.filter(e => e['Open source/Open access'] === activeFilters.openAccess);
      }
    }


    // Apply language filter (OR logic, exact match or substring)
    if (activeFilters.language?.length > 0) {
      filtered = filtered.filter(e => {
        const lang = (e.Language || '').toLowerCase();
        return activeFilters.language.some(l => lang && lang.includes(l.toLowerCase()));
      });
    }

    // Apply writing support filter (OR logic, exact match or substring)
    if (activeFilters.writingSupport?.length > 0) {
      filtered = filtered.filter(e => {
        const ws = (e['Writing support'] || '').toLowerCase();
        return activeFilters.writingSupport.some(w => ws && ws.includes(w.toLowerCase()));
      });
    }

    // Apply keywords filter (OR logic, substring match)
    if (activeFilters.keywords?.length > 0) {
      filtered = filtered.filter(e => {
        const kw = Array.isArray(e.Keywords) ? e.Keywords.map(k => k.toLowerCase()) : (e.Keywords || '').toLowerCase();
        return activeFilters.keywords.some(keyword => {
          if (Array.isArray(kw)) {
            return kw.some(k => k.includes(keyword.toLowerCase()));
          } else {
            return kw.includes(keyword.toLowerCase());
          }
        });
      });
    }

    return filtered;
  });

  return {
    editions,
    filteredEditions,
    loading,
    error,
    fetchEditions
  };
}
