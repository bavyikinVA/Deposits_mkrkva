<template>
  <span class="badge"><slot /></span>
</template>

<style scoped>
.badge {
  display: inline-flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 999px;
  background: #eef8fd;
  border: 1px solid #d8edf8;
  color: #337da5;
  font-size: 13px;
  font-weight: 700;
}
</style>