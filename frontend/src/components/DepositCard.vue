<template>
  <article class="deposit card">
    <div class="deposit__top">
      <div class="deposit__bank-wrap">
        <div class="deposit__bank">{{ item.product?.bank?.name || 'Банк' }}</div>
        <h3>{{ item.name }}</h3>
        <p v-if="item.description" class="deposit__description">
          {{ item.description }}
        </p>
      </div>

      <div class="deposit__rate">
        <span class="deposit__rate-label">Номинальная ставка</span>
        <UiBadge>{{ percent(displayRate) }}</UiBadge>
      </div>
    </div>

    <div class="deposit__features">
      <span class="deposit__feature" :class="{ 'is-active': item.allow_topup }">
        Пополнение: {{ item.allow_topup ? 'Да' : 'Нет' }}
      </span>
      <span class="deposit__feature" :class="{ 'is-active': item.allow_partial_withdraw }">
        Частичное снятие: {{ item.allow_partial_withdraw ? 'Да' : 'Нет' }}
      </span>
      <span class="deposit__feature" :class="{ 'is-active': item.auto_prolongation }">
        Автопролонгация: {{ item.auto_prolongation ? 'Да' : 'Нет' }}
      </span>
      <span class="deposit__feature">
        Валюта: {{ item.product?.currency || 'RUB' }}
      </span>
    </div>

    <div class="deposit__grid">
      <div class="deposit__metric">
        <span>Минимальная сумма</span>
        <strong>{{ currency(item.min_amount, item.product?.currency || 'RUB') }}</strong>
      </div>

      <div class="deposit__metric">
        <span>Срок</span>
        <strong>{{ daysToMonthsLabel(item.min_term_days) }}</strong>
      </div>

      <div class="deposit__metric">
        <span>Номинальная ставка</span>
        <strong>{{ percent(displayRate) }}</strong>
      </div>

      <div class="deposit__metric">
        <span>Способы открытия</span>
        <strong>{{ openMethodsLabel }}</strong>
      </div>

      <div class="deposit__metric">
        <span>Схемы начисления</span>
        <strong>{{ interestSchemesLabel }}</strong>
      </div>
    </div>

    <div class="deposit__footer">
      <div class="deposit__footer-info">
        <div class="deposit__hint">Выберите вклад и сразу перейдите к расчёту</div>
      </div>

      <div class="deposit__actions">
        <RouterLink
            class="btn btn-secondary"
            :to="`/calculator?variant=${item.id}`"
            @click="selectVariant"
        >
          В калькулятор
        </RouterLink>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useFormatters } from '../composables/useFormatters'
import { useDepositsStore } from '../stores/deposits'
import UiBadge from './UiBadge.vue'

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
})

const store = useDepositsStore()
const { currency, percent, daysToMonthsLabel } = useFormatters()

const displayRate = computed(() => {
  return (
      props.item.matched_final_nominal_rate ??
      props.item.matched_rate?.nominal_rate ??
      props.item.nominal_rate ??
      props.item.base_rate?.nominal_rate ??
      null
  )
})

const openMethodsLabel = computed(() => {
  if (!props.item.open_methods?.length) return 'Не указано'
  return props.item.open_methods.map((method) => method.name).join(', ')
})

const interestSchemesLabel = computed(() => {
  if (!props.item.interest_schemes?.length) return 'Не указано'
  return props.item.interest_schemes.map((scheme) => scheme.name).join(', ')
})

function selectVariant() {
  store.setSelectedVariant(props.item)
}
</script>

<style scoped>
.deposit {
  padding: 24px;
  border-radius: 24px;
  background: linear-gradient(180deg, #ffffff 0%, #fcfeff 100%);
}

.deposit__top {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: flex-start;
  margin-bottom: 18px;
}

.deposit__bank {
  color: var(--primary-deep);
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 8px;
}

.deposit h3 {
  margin: 0 0 8px;
  font-size: 24px;
  line-height: 1.2;
}

.deposit__description {
  margin: 0;
  color: var(--text-soft);
  line-height: 1.5;
}

.deposit__rate {
  min-width: 160px;
  display: grid;
  gap: 8px;
  justify-items: end;
}

.deposit__rate-label {
  color: var(--text-soft);
  font-size: 13px;
}

.deposit__features {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 18px;
}

.deposit__feature {
  padding: 8px 12px;
  border-radius: 999px;
  background: #f5fbff;
  border: 1px solid var(--border);
  color: var(--text-soft);
  font-size: 13px;
  font-weight: 600;
}

.deposit__feature.is-active {
  color: #1a6d91;
  background: #eef8fd;
}

.deposit__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
}

.deposit__metric {
  padding: 16px;
  border-radius: 18px;
  background: #fbfeff;
  border: 1px solid #e6f3fa;
}

.deposit__metric span {
  display: block;
  color: var(--text-soft);
  margin-bottom: 6px;
  font-size: 14px;
}

.deposit__metric strong {
  font-size: 16px;
  line-height: 1.4;
}

.deposit__footer {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
}

.deposit__hint {
  color: var(--text-soft);
  font-size: 14px;
}

.deposit__actions {
  display: flex;
  gap: 10px;
}

@media (max-width: 760px) {
  .deposit__top,
  .deposit__footer {
    flex-direction: column;
    align-items: stretch;
  }

  .deposit__rate {
    justify-items: start;
  }

  .deposit__grid {
    grid-template-columns: 1fr;
  }
}
</style>