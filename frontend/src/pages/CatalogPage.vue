<template>
  <section class="container catalog-page">
    <div class="catalog-page__head">
      <div>
        <h1 class="section-title">Каталог вкладов</h1>
        <p class="section-subtitle">Подбор вкладов по ключевым условиям.</p>
      </div>
      <div class="catalog-page__summary card">
        Найдено предложений: <strong>{{ store.total }}</strong>
      </div>
    </div>

    <div class="catalog-page__layout">
      <FiltersPanel v-model="filters" @submit="handleSubmit" />

      <div class="catalog-page__content">
        <UiLoader v-if="store.loading" />
        <div v-else-if="store.error" class="catalog-page__error card">{{ store.error }}</div>
        <UiEmptyState v-else-if="!store.items.length" />
        <DepositGrid v-else :items="store.items" />
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import DepositGrid from '../components/DepositGrid.vue'
import FiltersPanel from '../components/FiltersPanel.vue'
import UiEmptyState from '../components/UiEmptyState.vue'
import UiLoader from '../components/UiLoader.vue'
import { useDepositsStore } from '../stores/deposits'

const store = useDepositsStore()
const filters = ref({ ...store.filters })

async function handleSubmit(payload) {
  await store.loadDeposits(payload)
}

onMounted(async () => {
  await store.loadDeposits()
  filters.value = { ...store.filters }
})
</script>

<style scoped>
.catalog-page {
  padding: 28px 0 44px;
}

.catalog-page__head {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-end;
  margin-bottom: 22px;
}

.catalog-page__summary {
  padding: 18px 22px;
}

.catalog-page__layout {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 20px;
}

.catalog-page__content {
  min-width: 0;
}

.catalog-page__error {
  padding: 24px;
  color: #b42318;
}

@media (max-width: 980px) {
  .catalog-page__layout {
    grid-template-columns: 1fr;
  }

  .catalog-page__head {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>