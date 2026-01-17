<template>
  <div class="color-category-selector">
    <label for="color-category">Color by:</label>
    <select id="color-category" :value="modelValue" @change="$emit('update:modelValue', $event.target.value)">
      <option value="Language">Language</option>
      <option value="Writing support">Writing support</option>
      <option value="Historical Period">Historical Period</option>
      <!-- Add other relevant attributes here -->
    </select>
  </div>
</template>

<script setup>
defineProps(['modelValue']);
defineEmits(['update:modelValue']);
</script>

<style scoped>
.color-category-selector {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
  background-color: #f0f0f0;
  border-radius: 6px;
}
label {
  font-size: 12px;
  font-weight: 500;
}
select {
  padding: 4px;
  font-size: 12px;
  border-radius: 4px;
  border: 1px solid #ccc;
}
</style>
