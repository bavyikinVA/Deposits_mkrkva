<template>
  <div class="grid deposit-grid">
    <DepositCard v-for="item in items" :key="item.id" :item="item" />
  </div>
</template>

<script setup>
import DepositCard from './DepositCard.vue'

defineProps({
  items: {
    type: Array,
    default: () => []
  }
})
</script>

<style scoped>
.deposit-grid {
  gap: 18px;
}
</style>