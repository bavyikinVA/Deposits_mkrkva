<template>
  <label class="field">
    <span class="field__label">{{ label }}</span>
    <select class="field__control" :value="modelValue" @change="$emit('update:modelValue', $event.target.value)">
      <option v-for="option in options" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
  </label>
</template>

<script setup>
defineProps({
  label: { type: String, default: '' },
  modelValue: { type: [String, Number], default: '' },
  options: { type: Array, default: () => [] }
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
.field {
  display: grid;
  gap: 8px;
}

.field__label {
  font-size: 14px;
  color: var(--text-soft);
  font-weight: 600;
}

.field__control {
  width: 100%;
  min-height: 50px;
  border-radius: 14px;
  border: 1px solid var(--border);
  padding: 0 16px;
  background: #fff;
}
</style>