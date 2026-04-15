<template>
  <section class="container calculator-page">
    <div class="calculator-page__head">
      <h1 class="section-title">Калькулятор вкладов</h1>
    </div>

    <div class="calculator-page__layout">
      <CalculatorForm :variant-id="variantId" @submit="submit" />

      <div class="calculator-page__side">
        <UiLoader v-if="store.calculatorLoading || store.selectedVariantLoading" />

        <div v-else-if="store.selectedVariantError" class="calculator-page__error card">
          {{ store.selectedVariantError }}
        </div>

        <div v-else-if="store.calculatorError" class="calculator-page__error card">
          {{ store.calculatorError }}
        </div>

        <CalculationResultCard v-else :result="store.calculationResult" />
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import CalculationResultCard from '../components/CalculationResultCard.vue'
import CalculatorForm from '../components/CalculatorForm.vue'
import UiLoader from '../components/UiLoader.vue'
import { useDepositsStore } from '../stores/deposits'

const store = useDepositsStore()
const route = useRoute()

const variantId = computed(() => route.query.variant || '')

async function ensureVariantLoaded() {
  if (variantId.value) {
    await store.loadVariantById(variantId.value)
  }
}

onMounted(async () => {
  await ensureVariantLoaded()
})

watch(variantId, async () => {
  await ensureVariantLoaded()
})

async function submit(payload) {
  await store.runCalculation(payload)
}
</script>

<style scoped>
.calculator-page {
  padding: 28px 0 44px;
}

.calculator-page__head {
  margin-bottom: 22px;
}

.calculator-page__layout {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 20px;
  align-items: start;
}

.calculator-page__side {
  position: sticky;
  top: 100px;
}

.calculator-page__error {
  padding: 24px;
  color: #b42318;
}

@media (max-width: 980px) {
  .calculator-page__layout {
    grid-template-columns: 1fr;
  }

  .calculator-page__side {
    position: static;
  }
}
</style>