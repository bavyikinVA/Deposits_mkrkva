<template>
  <section class="container home-stats">
    <div class="home-stats__head">
      <h2 class="section-title">Статистика по базе</h2>
      <p class="section-subtitle">
        Краткая сводка по доступным предложениям вкладов.
      </p>
    </div>

    <div class="home-stats__grid">
      <article class="stats-card card">
        <span class="stats-card__label">Всего предложений</span>
        <strong class="stats-card__value">{{ stats.totalOffers }}</strong>
      </article>

      <article class="stats-card card">
        <span class="stats-card__label">Банков</span>
        <strong class="stats-card__value">{{ stats.totalBanks }}</strong>
      </article>

      <article class="stats-card card">
        <span class="stats-card__label">С пополнением</span>
        <strong class="stats-card__value">{{ stats.topupOffers }}</strong>
      </article>

      <article class="stats-card card">
        <span class="stats-card__label">С капитализацией</span>
        <strong class="stats-card__value">{{ stats.capitalizationOffers }}</strong>
      </article>
    </div>
  </section>
</template>

<script setup>
defineProps({
  stats: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.home-stats {
  padding: 18px 0 18px;
}

.home-stats__head {
  margin-bottom: 20px;
}

.home-stats__grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stats-card {
  padding: 24px;
  background: linear-gradient(180deg, #ffffff 0%, #f7fcff 100%);
}

.stats-card__label {
  display: block;
  color: var(--text-soft);
  font-size: 14px;
  margin-bottom: 10px;
}

.stats-card__value {
  display: block;
  font-size: 32px;
  font-weight: 800;
  line-height: 1.1;
  color: var(--text);
}

@media (max-width: 980px) {
  .home-stats__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .home-stats__grid {
    grid-template-columns: 1fr;
  }

  .stats-card__value {
    font-size: 28px;
  }
}
</style>