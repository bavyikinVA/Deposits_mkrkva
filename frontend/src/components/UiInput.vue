<template>
  <label class="field">
    <span class="field__label">{{ label }}</span>
    <input
        class="field__control"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        @input="$emit('update:modelValue', $event.target.value)"
    />
  </label>
</template>

<script setup>
defineProps({
  label: { type: String, default: '' },
  modelValue: { type: [String, Number], default: '' },
  placeholder: { type: String, default: '' },
  type: { type: String, default: 'text' }
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