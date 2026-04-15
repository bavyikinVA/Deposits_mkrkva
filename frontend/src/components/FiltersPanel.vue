<template>
  <aside class="filters card">
    <h3>Фильтры</h3>

    <div class="filters__grid">
      <UiInput v-model="localFilters.amount" label="Сумма" type="number" />

      <UiSelect
          v-model="termValue"
          label="Срок вклада"
          :options="termOptions"
      />

      <UiSelect
          v-model="localFilters.currency"
          label="Валюта"
          :options="currencyOptions"
      />

      <UiSelect
          v-model="capitalizationValue"
          label="Капитализация"
          :options="triStateOptions"
      />

      <UiSelect
          v-model="topupValue"
          label="Пополнение"
          :options="triStateOptions"
      />

      <UiSelect
          v-model="partialValue"
          label="Частичное снятие"
          :options="triStateOptions"
      />

      <UiSelect
          v-model="prolongValue"
          label="Автопролонгация"
          :options="triStateOptions"
      />
    </div>

    <div class="filters__actions">
      <button class="btn btn-primary" @click="submit">Показать предложения</button>
      <button class="btn btn-secondary" @click="reset">Сбросить</button>
    </div>
  </aside>
</template>

<script setup>
import { computed, reactive, watch } from 'vue'
import UiInput from './UiInput.vue'
import UiSelect from './UiSelect.vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'submit'])

const currencyOptions = [
  { value: 'RUB', label: 'RUB — российский рубль' },
  { value: 'USD', label: 'USD — доллар США' },
  { value: 'EUR', label: 'EUR — евро' },
  { value: 'CNY', label: 'CNY — китайский юань' },
  { value: 'JPY', label: 'JPY — японская иена' }
]

const termOptions = [
  { value: '', label: 'Не важно' },
  { value: '31', label: '31 день' },
  { value: '91', label: '3 месяца (91 день)' },
  { value: '181', label: '6 месяцев (181 день)' },
  { value: '367', label: '1 год (367 дней)' },
  { value: '548', label: '1.5 года (548 дней)' },
  { value: '730', label: '2 года (730 дней)' },
  { value: '1095', label: '3 года (1095 дней)' }
]

const triStateOptions = [
  { value: '', label: 'Не важно' },
  { value: 'true', label: 'Да' },
  { value: 'false', label: 'Нет' }
]

const localFilters = reactive({ ...props.modelValue })

watch(
    () => props.modelValue,
    (value) => Object.assign(localFilters, value),
    { deep: true }
)

const mapToUi = (value) => (value === null || value === undefined ? '' : String(value))
const mapFromUi = (value) => (value === '' ? null : value === 'true')

const capitalizationValue = computed({
  get: () => mapToUi(localFilters.capitalization_enabled),
  set: (value) => {
    localFilters.capitalization_enabled = mapFromUi(value)
  }
})

const topupValue = computed({
  get: () => mapToUi(localFilters.allow_topup),
  set: (value) => {
    localFilters.allow_topup = mapFromUi(value)
  }
})

const partialValue = computed({
  get: () => mapToUi(localFilters.allow_partial_withdraw),
  set: (value) => {
    localFilters.allow_partial_withdraw = mapFromUi(value)
  }
})

const prolongValue = computed({
  get: () => mapToUi(localFilters.auto_prolongation),
  set: (value) => {
    localFilters.auto_prolongation = mapFromUi(value)
  }
})

const termValue = computed({
  get: () => mapToUi(localFilters.term_days),
  set: (value) => {
    localFilters.term_days = value === '' ? null : Number(value)
  }
})

function submit() {
  const payload = {
    ...localFilters,
    amount: localFilters.amount ? Number(localFilters.amount) : null,
    term_days: localFilters.term_days ? Number(localFilters.term_days) : null,
    page: 1
  }

  emit('update:modelValue', payload)
  emit('submit', payload)
}

function reset() {
  const payload = {
    amount: 300000,
    term_days: 367,
    currency: 'RUB',
    capitalization_enabled: null,
    allow_topup: null,
    allow_partial_withdraw: null,
    auto_prolongation: null,
    page: 1,
    page_size: 12
  }

  Object.assign(localFilters, payload)
  emit('update:modelValue', payload)
  emit('submit', payload)
}
</script>

<style scoped>
.filters {
  padding: 24px;
}

.filters h3 {
  margin: 0 0 18px;
}

.filters__grid {
  display: grid;
  gap: 14px;
}

.filters__actions {
  display: grid;
  gap: 10px;
  margin-top: 18px;
}
</style>