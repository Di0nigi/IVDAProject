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
      const data = await response.json();
      editions.value = data.map(e => ({ ...e, reliabilityScore: Math.floor(Math.random() * 101) }));
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

    // Authority filter
    if (typeof activeFilters.authoritativeness === 'number' && activeFilters.authoritativeness > 0) {
      filtered = filtered.filter(e => {
        // MongoDB field is authoritativeness_score
        const val = e.authoritativeness_score ?? e.authoritativeness ?? e.Authoritativeness;
        return typeof val === 'number' && val >= activeFilters.authoritativeness;
      });
    }

    // Renown filter
    if (typeof activeFilters.renown === 'number' && activeFilters.renown > 0) {
      filtered = filtered.filter(e => {
        // MongoDB field is renown_score
        const val = e.renown_score ?? e.renown ?? e.Renown;
        return typeof val === 'number' && val >= activeFilters.renown;
      });
    }

    // Apply historical period filter
    if (activeFilters.historicalPeriod?.length > 0) {
      const selected = activeFilters.historicalPeriod.filter(f => f.status === 'selected').map(f => f.name);
      const excluded = activeFilters.historicalPeriod.filter(f => f.status === 'excluded').map(f => f.name);

      filtered = filtered.filter(e => {
        const periods = (e['Historical Period'] || '').toLowerCase().split(/[,;]+/).map(p => p.trim());
        const hasSelected = selected.length === 0 || selected.some(s => periods.includes(s));
        const hasExcluded = excluded.length > 0 && periods.some(p => excluded.includes(p));
        return hasSelected && !hasExcluded;
      });
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

    // Apply language filter
    if (activeFilters.language?.length > 0) {
      const selected = activeFilters.language.filter(f => f.status === 'selected').map(f => f.name);
      const excluded = activeFilters.language.filter(f => f.status === 'excluded').map(f => f.name);

      filtered = filtered.filter(e => {
        const langs = (e.Language || '').toLowerCase().split(/[,;]+/).map(l => l.trim());
        const hasSelected = selected.length === 0 || selected.some(s => langs.includes(s));
        const hasExcluded = excluded.length > 0 && langs.some(l => excluded.includes(l));
        return hasSelected && !hasExcluded;
      });
    }

    // Apply writing support filter
    if (activeFilters.writingSupport?.length > 0) {
      const selected = activeFilters.writingSupport.filter(f => f.status === 'selected').map(f => f.name);
      const excluded = activeFilters.writingSupport.filter(f => f.status === 'excluded').map(f => f.name);

      filtered = filtered.filter(e => {
        const supports = (e['Writing support'] || '').toLowerCase().split(/[,;]+/).map(s => s.trim());
        const hasSelected = selected.length === 0 || supports.some(s => selected.includes(s));
        const hasExcluded = excluded.length > 0 && supports.some(s => excluded.includes(s));
        return hasSelected && !hasExcluded;
      });
    }

    // Apply keywords filter
    if (activeFilters.keywords?.length > 0) {
      const selected = activeFilters.keywords.filter(f => f.status === 'selected').map(f => f.name);
      const excluded = activeFilters.keywords.filter(f => f.status === 'excluded').map(f => f.name);

      filtered = filtered.filter(e => {
        const keywords = (e.Keywords || '').toLowerCase().split('#').map(k => k.trim());
        const hasSelected = selected.length === 0 || keywords.some(k => selected.includes(k));
        const hasExcluded = excluded.length > 0 && keywords.some(k => excluded.includes(k));
        return hasSelected && !hasExcluded;
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
