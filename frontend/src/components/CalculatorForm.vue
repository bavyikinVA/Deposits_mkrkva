<template>
  <form class="calculator card" @submit.prevent="submit">
    <h2>Калькулятор вклада</h2>

    <div class="calculator__grid">
      <UiInput v-model="form.variant_id" label="ID варианта вклада" type="number" />
      <UiInput v-model="form.amount" label="Сумма" type="number" />

      <UiSelect
          v-model="termValue"
          label="Срок вклада"
          :options="termOptions"
      />

      <UiSelect
          v-model="form.open_method_code"
          label="Способ открытия"
          :options="openMethodOptions"
      />

      <UiSelect
          v-model="form.interest_scheme_code"
          label="Схема начисления процентов"
          :options="interestSchemeOptions"
      />

      <UiInput v-model="form.promo_code" label="Промокод" />
    </div>

    <div v-if="selectedVariant" class="calculator__selected">
      <div class="calculator__selected-title">Выбран вклад</div>
      <div class="calculator__selected-name">
        {{ selectedVariant.product?.bank?.name || 'Банк' }} — {{ selectedVariant.name }}
      </div>
      <div class="calculator__selected-meta">
        Сумма от {{ selectedVariant.min_amount }} ·
        срок от {{ selectedVariant.min_term_days }} дн.
        <template v-if="selectedVariant.max_term_days">
          до {{ selectedVariant.max_term_days }} дн.
        </template>
      </div>
    </div>

    <div class="calculator__checks">
      <UiCheckbox v-model="form.has_subscription" label="Есть подписка" />
      <UiCheckbox v-model="form.is_salary_client" label="Зарплатный клиент" />
      <UiCheckbox v-model="form.is_pension_client" label="Пенсионный клиент" />
      <UiCheckbox v-model="form.has_premium_package" label="Премиум-пакет" />
    </div>

    <div class="calculator__grid calculator__grid--secondary">
      <UiInput v-model="form.monthly_spend" label="Траты в месяц" type="number" />
      <UiInput v-model="form.savings_balance" label="Остаток на счетах" type="number" />
    </div>

    <button class="btn btn-primary" type="submit">Рассчитать доходность</button>
  </form>
</template>

<script setup>
import { computed, reactive, watch, watchEffect } from 'vue'
import { useDepositsStore } from '../stores/deposits'
import UiCheckbox from './UiCheckbox.vue'
import UiInput from './UiInput.vue'
import UiSelect from './UiSelect.vue'

const props = defineProps({
  variantId: {
    type: [String, Number],
    default: ''
  }
})

const emit = defineEmits(['submit'])

const store = useDepositsStore()
const selectedVariant = computed(() => store.selectedVariant)

const form = reactive({
  variant_id: '',
  amount: 300000,
  term_days: 367,
  open_method_code: '',
  interest_scheme_code: '',
  has_subscription: false,
  is_salary_client: false,
  is_pension_client: false,
  monthly_spend: '',
  savings_balance: '',
  has_premium_package: false,
  promo_code: ''
})

function normalizeOpenMethod(item) {
  if (!item) return null

  const source = item.open_method || item

  return {
    code: source.code || '',
    name: source.name || source.code || 'Не указано'
  }
}

function normalizeInterestScheme(item) {
  if (!item) return null

  const source = item.interest_scheme || item

  return {
    code: source.code || '',
    name: source.name || source.code || 'Не указано'
  }
}

function getOpenMethodLabel(method) {
  if (!method) return 'Не указано'
  if (method.name && method.name !== method.code) return method.name

  const map = {
    online: 'Онлайн',
    office: 'В отделении банка',
    branch: 'В отделении банка',
    mobile_app: 'В мобильном приложении',
    internet_bank: 'В интернет-банке',
    gosuslugi: 'Через Госуслуги'
  }

  return map[method.code] || method.name || method.code || 'Не указано'
}

function getInterestSchemeLabel(scheme) {
  if (!scheme) return 'Не указано'
  if (scheme.name && scheme.name !== scheme.code) return scheme.name

  const map = {
    end: 'Выплата в конце срока',
    monthly: 'Ежемесячная выплата',
    monthly_cap: 'Ежемесячно с капитализацией',
    quarterly: 'Ежеквартальная выплата',
    daily: 'Ежедневное начисление'
  }

  return map[scheme.code] || scheme.name || scheme.code || 'Не указано'
}

function getRateMethodCode(rate) {
  return (
      rate?.open_method?.code ||
      rate?.open_method_code ||
      rate?.open_method?.name ||
      ''
  )
}

function getRateSchemeCode(rate) {
  return (
      rate?.interest_scheme?.code ||
      rate?.interest_scheme_code ||
      ''
  )
}

function uniqueByCode(items) {
  const map = new Map()

  items.forEach((item) => {
    if (!item?.code) return
    if (!map.has(item.code)) {
      map.set(item.code, item)
    }
  })

  return [...map.values()]
}

function formatTermLabel(from, to) {
  const labels = {
    30: '1 месяц',
    31: '1 месяц',
    60: '2 месяца',
    61: '2 месяца',
    62: '2 месяца',
    91: '3 месяца',
    92: '3 месяца',
    181: '6 месяцев',
    182: '6 месяцев',
    183: '6 месяцев',
    367: '1 год',
    548: '1.5 года',
    730: '2 года',
    1095: '3 года'
  }

  if (from === to) {
    return labels[from] ? `${labels[from]} (${from} дн.)` : `${from} дн.`
  }

  if (
      [181, 182, 183].includes(from) &&
      [181, 182, 183].includes(to)
  ) {
    return '6 месяцев'
  }

  if (
      [60, 61, 62].includes(from) &&
      [60, 61, 62].includes(to)
  ) {
    return '2 месяца'
  }

  if (
      [91, 92].includes(from) &&
      [91, 92].includes(to)
  ) {
    return '3 месяца'
  }

  return `${from}–${to} дн.`
}

function getRepresentativeTerm(from, to) {
  if ([181, 182, 183].includes(from) && [181, 182, 183].includes(to)) {
    return 181
  }

  if ([60, 61, 62].includes(from) && [60, 61, 62].includes(to)) {
    return 60
  }

  if ([91, 92].includes(from) && [91, 92].includes(to)) {
    return 91
  }

  return Number(from)
}

const normalizedOpenMethods = computed(() => {
  const directMethods = (selectedVariant.value?.open_methods || [])
      .map(normalizeOpenMethod)
      .filter(Boolean)

  const rateMethods = (selectedVariant.value?.base_rates || [])
      .map((rate) => normalizeOpenMethod(rate?.open_method || { code: getRateMethodCode(rate), name: getRateMethodCode(rate) }))
      .filter((item) => item?.code)

  return uniqueByCode([...directMethods, ...rateMethods])
})

const normalizedInterestSchemes = computed(() => {
  const directSchemes = (selectedVariant.value?.interest_schemes || [])
      .map(normalizeInterestScheme)
      .filter(Boolean)

  const rateSchemes = (selectedVariant.value?.base_rates || [])
      .map((rate) => normalizeInterestScheme(rate?.interest_scheme || { code: getRateSchemeCode(rate), name: getRateSchemeCode(rate) }))
      .filter((item) => item?.code)

  return uniqueByCode([...directSchemes, ...rateSchemes])
})

const openMethodOptions = computed(() => {
  if (!normalizedOpenMethods.value.length) {
    return [{ value: '', label: 'Не указано' }]
  }

  return normalizedOpenMethods.value.map((method) => ({
    value: method.code,
    label: getOpenMethodLabel(method)
  }))
})

const interestSchemeOptions = computed(() => {
  if (!normalizedInterestSchemes.value.length) {
    return [{ value: '', label: 'Не указано' }]
  }

  return normalizedInterestSchemes.value.map((scheme) => ({
    value: scheme.code,
    label: getInterestSchemeLabel(scheme)
  }))
})

const filteredBaseRates = computed(() => {
  const rates = selectedVariant.value?.base_rates || []

  return rates.filter((rate) => {
    const methodCode = getRateMethodCode(rate)
    const schemeCode = getRateSchemeCode(rate)

    const methodOk = !form.open_method_code || methodCode === form.open_method_code
    const schemeOk = !form.interest_scheme_code || schemeCode === form.interest_scheme_code

    return methodOk && schemeOk
  })
})

const termOptions = computed(() => {
  if (!filteredBaseRates.value.length) {
    if (selectedVariant.value?.min_term_days) {
      return [{
        value: String(selectedVariant.value.min_term_days),
        label: `${selectedVariant.value.min_term_days} дн.`
      }]
    }

    return [{ value: '367', label: '1 год (367 дн.)' }]
  }

  const uniqueRanges = new Map()

  filteredBaseRates.value.forEach((rate) => {
    const from = Number(rate.term_from_days)
    const to = Number(rate.term_to_days)
    const key = `${from}-${to}`

    if (!uniqueRanges.has(key)) {
      uniqueRanges.set(key, {
        from,
        to,
        value: getRepresentativeTerm(from, to),
        label: formatTermLabel(from, to)
      })
    }
  })

  return [...uniqueRanges.values()]
      .sort((a, b) => a.value - b.value)
      .map((item) => ({
        value: String(item.value),
        label: item.label
      }))
})

const termValue = computed({
  get: () => String(form.term_days || ''),
  set: (value) => {
    form.term_days = value ? Number(value) : null
  }
})

watchEffect(() => {
  if (props.variantId) {
    form.variant_id = props.variantId
  }

  if (selectedVariant.value) {
    form.variant_id = selectedVariant.value.id
    form.amount = Number(selectedVariant.value.min_amount || 300000)

    const firstMethod = openMethodOptions.value[0]?.value || ''
    const firstScheme = interestSchemeOptions.value[0]?.value || ''

    form.open_method_code = firstMethod
    form.interest_scheme_code = firstScheme
  }
})

watch(
    () => [form.open_method_code, form.interest_scheme_code, selectedVariant.value?.id],
    () => {
      const availableTerms = termOptions.value
      const currentExists = availableTerms.some((item) => Number(item.value) === Number(form.term_days))

      if (!currentExists) {
        form.term_days = Number(availableTerms[0]?.value || selectedVariant.value?.min_term_days || 367)
      }
    },
    { immediate: true }
)

function submit() {
  emit('submit', {
    variant_id: Number(form.variant_id),
    amount: Number(form.amount),
    term_days: Number(form.term_days),
    open_method_code: form.open_method_code || null,
    interest_scheme_code: form.interest_scheme_code || null,
    has_subscription: form.has_subscription,
    is_salary_client: form.is_salary_client,
    is_pension_client: form.is_pension_client,
    monthly_spend: form.monthly_spend ? Number(form.monthly_spend) : null,
    savings_balance: form.savings_balance ? Number(form.savings_balance) : null,
    has_premium_package: form.has_premium_package,
    promo_code: form.promo_code || null,
    extra_context: {}
  })
}
</script>

<style scoped>
.calculator {
  padding: 28px;
}

.calculator h2 {
  margin: 0 0 18px;
}

.calculator__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin-bottom: 16px;
}

.calculator__grid--secondary {
  grid-template-columns: repeat(2, 1fr);
}

.calculator__checks {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
  margin-bottom: 16px;
}

.calculator__selected {
  margin-bottom: 16px;
  padding: 16px 18px;
  border-radius: 18px;
  background: #f5fbff;
  border: 1px solid var(--border);
}

.calculator__selected-title {
  color: var(--text-soft);
  font-size: 13px;
  margin-bottom: 6px;
}

.calculator__selected-name {
  font-weight: 700;
  margin-bottom: 4px;
}

.calculator__selected-meta {
  color: var(--text-soft);
  font-size: 14px;
}

@media (max-width: 900px) {
  .calculator__grid,
  .calculator__grid--secondary,
  .calculator__checks {
    grid-template-columns: 1fr;
  }
}
</style>