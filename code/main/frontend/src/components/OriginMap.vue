<template>
  <div class="map-container">
    <h4 class="map-title">Place of Origin</h4>
    <div ref="mapElement" class="map"></div>
    <div v-if="!hasValidLocation" class="no-location">
      Location data not available
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, defineProps } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const props = defineProps({
  location: {
    type: String,
    default: null
  }
});

const mapElement = ref(null);
let map = null;
let marker = null;
const hasValidLocation = ref(false);

// Geocoding lookup for places of origin
const locationCoordinates = {
  // Countries
  'italy': [41.9028, 12.4964],
  'france': [46.2276, 2.2137],
  'england': [52.3555, -1.1743],
  'spain': [40.4637, -3.7492],
  'germany': [51.1657, 10.4515],
  'ireland': [53.1424, -7.6921],
  'greece': [39.0742, 21.8243],
  'egypt': [26.8206, 30.8025],
  'bulgaria': [42.7339, 25.4858],
  'wales': [52.1307, -3.7837],
  'scotland': [56.4907, -4.2026],
  'austria': [47.5162, 13.5501],
  'portugal': [39.3999, -8.2245],
  'netherlands': [52.1326, 5.2913],
  'belgium': [50.5039, 4.4699],
  'switzerland': [46.8182, 8.2275],
  'poland': [51.9194, 19.1451],
  'hungary': [47.1625, 19.5033],
  'croatia': [45.1, 15.2],
  'denmark': [56.2639, 9.5018],
  'norway': [60.4720, 8.4689],
  'iceland': [64.9631, -19.0208],
  'turkey': [38.9637, 35.2433],
  'israel': [31.0461, 34.8516],
  'palestine': [31.9522, 35.2332],
  'iraq': [33.2232, 43.6793],
  'iran': [32.4279, 53.6880],
  'syria': [34.8021, 38.9968],
  'libya': [26.3351, 17.2283],
  'united states': [37.0902, -95.7129],
  'united states of america': [37.0902, -95.7129],
  'canada': [56.1304, -106.3468],
  'mexico': [23.6345, -102.5528],
  'australia': [-25.2744, 133.7751],
  'new zealand': [-40.9006, 174.8860],
  'south africa': [-30.5595, 22.9375],
  'india': [20.5937, 78.9629],
  'vietnam': [14.0583, 108.2772],
  'europe': [54.5260, 15.2551],
  'united kingdom': [55.3781, -3.4360],
  
  // Cities
  'rome': [41.9028, 12.4964],
  'paris': [48.8566, 2.3522],
  'london': [51.5074, -0.1278],
  'madrid': [40.4168, -3.7038],
  'dublin': [53.3498, -6.2603],
  'athens': [37.9838, 23.7275],
  'cairo': [30.0444, 31.2357],
  'oxford': [51.7520, -1.2577],
  'cambridge': [52.2053, 0.1218],
  'vienna': [48.2082, 16.3738],
  'munich': [48.1351, 11.5820],
  'baghdad': [33.3152, 44.3661],
  'beirut': [33.8886, 35.4955],
  'damascus': [33.5138, 36.2765],
  'chicago': [41.8781, -87.6298],
  'aachen': [50.7753, 6.0839],
  'zürich': [47.3769, 8.5417],
  'geneva': [46.2044, 6.1432],
  'bologna': [44.4949, 11.3426],
  'florence': [43.7696, 11.2558],
  'venice': [45.4408, 12.3155],
  'verona': [45.4384, 10.9916],
  'naples': [40.8518, 14.2681],
  'milan': [45.4642, 9.1900],
  'göttingen': [51.5414, 9.9155],
  'berlin': [52.5200, 13.4050],
  'prague': [50.0755, 14.4378],
  'warsaw': [52.2297, 21.0122],
  'budapest': [47.4979, 19.0402],
  'istanbul': [41.0082, 28.9784],
  'constantinople': [41.0082, 28.9784],
  
  // Specific locations
  'mount sinai': [28.5392, 33.9750],
  'vercelli': [45.3205, 8.4180],
  'vindolanda': [54.9916, -2.3592],
  'san millán de la cogolla': [42.3267, -2.8731],
  'preslav': [43.1594, 26.8217],
  'aphrodisias': [37.7081, 28.7231],
  'cyrene': [32.8245, 21.8580],
  'tripoli': [32.8872, 13.1913],
  'qumran': [31.7444, 35.4586],
  'abbey of st. gall': [47.4239, 9.3767],
  'benevento': [41.1297, 14.7824],
  'bernburg': [51.7956, 11.7383],
  'erfurt': [50.9787, 11.0328],
  'flanders': [51.0543, 3.7174],
  'aquitaine': [44.8378, -0.5792],
  'constance': [47.6633, 9.1753],
  'salerno': [40.6824, 14.7681],
  'el escorial': [40.5898, -4.1476],
  'salamanca': [40.9701, -5.6635],
  'santander': [43.4623, -3.8099],
  'winchester': [51.0632, -1.3080],
  'lindisfarne': [55.6692, -1.8000],
  'monkwearmouth': [54.9241, -1.3800],
  'jarrow': [54.9800, -1.4892],
  "king's lynn": [52.7545, 0.3963],
  'yucatán': [20.7099, -89.0943],
  'campā': [15.5527, 108.0215],
  'bobbio': [44.7686, 9.3864],
  'luni': [44.0770, 10.0417],
  'derveni': [40.6908, 22.8611],
  'monastery of bobbio': [44.7686, 9.3864],
  'cottonian library': [51.5194, -0.1270],
  'british library': [51.5299, -0.1270],
  'cairo genizah': [30.0444, 31.2357],
  'newcastle': [54.9783, -1.6178],
  'puerto rico': [18.2208, -66.5901],
  'cuba': [21.5218, -77.7812],
  'venezuela': [6.4238, -66.5897],
  'łódź': [51.7592, 19.4560],
  'opava': [49.9386, 17.9028],
  'ljubljana': [46.0569, 14.5058],
  'nuremberg': [49.4521, 11.0767],
  'salzburg': [47.8095, 13.0550],
  'thuringia': [51.0110, 10.8453],
  'bremen': [53.0793, 8.8017],
  'cologne': [50.9375, 6.9603],
  'königsfelden': [47.4814, 8.2117],
  'windisch': [47.4814, 8.2117],
  
  // Regions
  'northern italy': [45.4654, 9.1859],
  'southern germany': [48.7758, 9.1829],
  'northern france': [48.8566, 2.3522],
  'northern spain': [42.8782, -2.5797],
  'brittany': [48.2020, -2.9326],
  'middle east': [29.2985, 42.5510],
  'north africa': [28.0339, 1.6596],
  'black sea': [43.4129, 34.2994],
  'cyrenaica': [32.1167, 20.0683],
  'western libya': [32.5000, 13.0000],
  'ancient cyrenaica': [32.8245, 21.8580],
  
  // Invalid/unknown
  'various': null,
  'not provided': null,
  'not specified': null,
  'unknown': null,
  'multiple': null,
  '440 places worldwide': null,
  'various scriptoria': null
};

const geocodeLocation = (locationStr) => {
  if (!locationStr) return null;
  
  const normalized = locationStr.toLowerCase().trim();
  
  // Direct match
  if (locationCoordinates[normalized] !== undefined) {
    return locationCoordinates[normalized];
  }
  
  // Partial match
  for (const [key, coords] of Object.entries(locationCoordinates)) {
    if (normalized.includes(key) && coords !== null) {
      return coords;
    }
  }
  
  return null;
};

const initMap = () => {
  if (!mapElement.value) return;
  
  // Initialize map with world view - much more zoomed out
  map = L.map(mapElement.value, {
    zoomControl: false,
    attributionControl: false,
    dragging: false,
    scrollWheelZoom: false,
    doubleClickZoom: false,
    boxZoom: false,
    keyboard: false,
    touchZoom: false
  }).setView([30, 0], 1.5); // World view centered, zoom level 1.5
  
  // Use a simpler tile layer with less detail
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 4,
    minZoom: 1
  }).addTo(map);
};

const updateMarker = () => {
  if (!map || !props.location) return;
  
  const coords = geocodeLocation(props.location);
  
  if (coords) {
    hasValidLocation.value = true;
    
    // Remove existing marker
    if (marker) {
      map.removeLayer(marker);
    }
    
    // Create a custom icon - larger and more visible
    const customIcon = L.icon({
      iconUrl: 'data:image/svg+xml;base64,' + btoa(`
        <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
          <circle cx="16" cy="16" r="8" fill="#E53935" stroke="white" stroke-width="2"/>
          <circle cx="16" cy="16" r="4" fill="white"/>
        </svg>
      `),
      iconSize: [32, 32],
      iconAnchor: [16, 16],
      popupAnchor: [0, -16]
    });
    
    // Add new marker with custom icon
    marker = L.marker(coords, { icon: customIcon }).addTo(map);
    marker.bindPopup(`<strong>${props.location}</strong>`, {
      closeButton: false
    }).openPopup();
    
    // Keep the world view but slightly adjust to show the marker
    // Don't zoom in - just pan to show the location in context
    map.setView(coords, 2); // Zoom level 2 shows continent level
  } else {
    hasValidLocation.value = false;
    
    // Remove marker if location is invalid
    if (marker) {
      map.removeLayer(marker);
      marker = null;
    }
    
    // Reset to world view
    map.setView([30, 0], 1.5);
  }
};

watch(() => props.location, () => {
  updateMarker();
});

onMounted(() => {
  initMap();
  updateMarker();
});

onUnmounted(() => {
  if (map) {
    map.remove();
  }
});
</script>

<style scoped>
.map-container {
  width: 100%;
  margin-top: 12px;
  position: relative;
}

.map-title {
  margin: 0 0 8px 0;
  font-size: 13px;
  font-weight: 600;
  color: #333;
}

.map {
  width: 100%;
  height: 200px;
  border-radius: 8px;
  border: 1px solid #d5d9df;
  background: #f8f9fa;
}

.no-location {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255, 255, 255, 0.9);
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 12px;
  color: #666;
  pointer-events: none;
  z-index: 1000;
}
</style>
