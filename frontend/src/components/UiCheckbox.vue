<template>
  <label class="check">
    <input :checked="modelValue" type="checkbox" @change="$emit('update:modelValue', $event.target.checked)" />
    <span>{{ label }}</span>
  </label>
</template>

<script setup>
defineProps({
  label: { type: String, default: '' },
  modelValue: { type: Boolean, default: false }
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
.check {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  color: var(--text);
}
</style>