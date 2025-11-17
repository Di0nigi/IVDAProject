<template>
  <div v-if="edition">
    <h2>{{ edition['Edition name'] }}</h2>
    <p><strong>Author/Manager:</strong> {{ edition['Manager or Editor'] }}</p>
    <p><strong>Historical Period:</strong> {{ edition['Historical Period'] }}</p>
    <p><strong>Time/Century:</strong> {{ edition['Time/Century'] }}</p>
    <p><strong>Language:</strong> {{ edition.Language }}</p>
  </div>

  <div v-else>
    <p>No edition selected</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  edition: {
    type: Object,
    default: null
  }
})
</script>

<style scoped>
h2 {
  margin-bottom: 0.5em;
}

p {
  margin: 0.3em 0;
}
</style>
