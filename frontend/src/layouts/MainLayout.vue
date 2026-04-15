<template>
  <div>
    <TheHeader />
    <main>
      <slot />
    </main>
  </div>
</template>

<script setup>
import TheHeader from '../components/TheHeader.vue'
</script>