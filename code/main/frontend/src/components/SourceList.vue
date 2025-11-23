<template>
  <div class="source-container">
    <div class="search-bar">
      <input type="text" placeholder="Search..." v-model="searchQuery" />
    </div>
    <ul class="source-list">
    <li v-for="text in searchFilteredEditions" :key="text.id" class="list-item">
        <a href="#" @click.prevent="selectEdition(text.id)">
        {{ text['Edition name'] }}
        </a>
    </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed} from 'vue'
import { useEditionsData } from '../composables/useEditionsData'

const texts = ref([])
const selected = ref(null)
const searchQuery = ref('')

const { editions, filteredEditions, fetchEditions } = useEditionsData()

const emit = defineEmits(['select'])

function selectEdition(id) {
  const edition = filteredEditions.value.find(e => e.id === id)
  emit('select', edition)
}

const searchFilteredEditions = computed(() => {
  if (!searchQuery.value) return filteredEditions.value
  return filteredEditions.value.filter(text =>
    text['Edition name']
      .toLowerCase()
      .includes(searchQuery.value.toLowerCase())
  )
})
</script>

<style scoped>
.source-container {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  margin-bottom: 12px;
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

.source-list {
  list-style: none;
  padding: 0;
  margin: 0;
  padding-right: 6px;
  overflow-y: auto;
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.source-list a {
  color: #333;
  text-decoration: none;
  display: block;
  padding: 8px 12px;
  background: white;
  border: 1px solid #d5d9df;
  border-radius: 6px;
  transition: all 0.2s;
}

.source-list a:hover {
  background: #f5f5f5;
  border-color: #8f4e1f;
  color: #8f4e1f;
}

.list-item {
  list-style: none;
}
</style>
