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

// Simple geocoding lookup for common places (can be extended)
const locationCoordinates = {
  'italy': [41.9028, 12.4964],
  'rome': [41.9028, 12.4964],
  'france': [46.2276, 2.2137],
  'paris': [48.8566, 2.3522],
  'england': [52.3555, -1.1743],
  'london': [51.5074, -0.1278],
  'spain': [40.4637, -3.7492],
  'madrid': [40.4168, -3.7038],
  'germany': [51.1657, 10.4515],
  'ireland': [53.1424, -7.6921],
  'dublin': [53.3498, -6.2603],
  'greece': [39.0742, 21.8243],
  'athens': [37.9838, 23.7275],
  'egypt': [26.8206, 30.8025],
  'cairo': [30.0444, 31.2357],
  'mount sinai': [28.5392, 33.9750],
  'bulgaria': [42.7339, 25.4858],
  'vercelli': [45.3205, 8.4180],
  'vindolanda': [54.9916, -2.3592],
  'wales': [52.1307, -3.7837],
  'oxford': [51.7520, -1.2577],
  'various': null,
  'not provided': null,
  'not specified': null,
  'san millán de la cogolla': [42.3267, -2.8731],
  'preslav': [43.1594, 26.8217]
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
  
  // Initialize map centered on Europe
  map = L.map(mapElement.value, {
    zoomControl: true,
    attributionControl: false
  }).setView([45, 10], 4);
  
  // Add tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
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
    
    // Add new marker
    marker = L.marker(coords).addTo(map);
    marker.bindPopup(props.location).openPopup();
    
    // Center map on marker
    map.setView(coords, 6);
  } else {
    hasValidLocation.value = false;
    
    // Remove marker if location is invalid
    if (marker) {
      map.removeLayer(marker);
      marker = null;
    }
    
    // Reset to default view
    map.setView([45, 10], 4);
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
