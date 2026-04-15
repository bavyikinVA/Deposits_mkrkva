<template>
  <header class="header">
    <div class="container header__inner">
      <RouterLink to="/" class="header__brand">
        <span class="header__logo">%</span>
        <div>
          <div class="header__title">Deposit Match</div>
          <div class="header__caption">Подбор вкладов и расчёт доходности</div>
        </div>
      </RouterLink>

      <nav class="header__nav">
        <RouterLink to="/catalog" class="header__link">Вклады</RouterLink>
        <RouterLink to="/calculator" class="header__link">Калькулятор</RouterLink>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 20;
  backdrop-filter: blur(12px);
  background: rgba(255, 255, 255, 0.88);
  border-bottom: 1px solid rgba(153, 208, 238, 0.35);
}

.header__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  min-height: 82px;
}

.header__brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.header__logo {
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  background: linear-gradient(135deg, #99d0ee 0%, #4da8d8 100%);
  color: #fff;
  font-weight: 800;
}

.header__title {
  font-size: 18px;
  font-weight: 800;
}

.header__caption {
  font-size: 12px;
  color: var(--text-soft);
}

.header__nav {
  display: flex;
  align-items: center;
  gap: 18px;
}

.header__link {
  color: var(--text-soft);
  font-weight: 600;
}

.header__link.router-link-active {
  color: var(--text);
}

@media (max-width: 768px) {
  .header__inner {
    flex-direction: column;
    justify-content: center;
    padding: 14px 0;
  }
}
</style>