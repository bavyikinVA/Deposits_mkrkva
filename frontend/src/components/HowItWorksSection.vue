<template>
  <section class="container how-it-works">
    <div class="how-it-works__head">
      <h2 class="section-title">Как пользоваться</h2>
      <p class="section-subtitle">
        Подбор вклада занимает всего несколько шагов.
      </p>
    </div>

    <div class="how-it-works__grid">
      <article class="step-card card">
        <div class="step-card__index">01</div>
        <h3>Укажите сумму и срок</h3>
        <p>
          Задайте основные параметры вклада, чтобы система подобрала подходящие варианты.
        </p>
      </article>

      <article class="step-card card">
        <div class="step-card__index">02</div>
        <h3>Выберите подходящий вклад</h3>
        <p>
          Сравните предложения по ставке, условиям пополнения, капитализации и сроку.
        </p>
      </article>

      <article class="step-card card">
        <div class="step-card__index">03</div>
        <h3>Рассчитайте итоговую доходность</h3>
        <p>
          Перейдите в калькулятор и получите итоговую сумму и размер начисленных процентов.
        </p>
      </article>
    </div>
  </section>
</template>

<style scoped>
.how-it-works {
  padding: 18px 0 44px;
}

.how-it-works__head {
  margin-bottom: 20px;
}

.how-it-works__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.step-card {
  padding: 24px;
  background: linear-gradient(180deg, #ffffff 0%, #fbfeff 100%);
}

.step-card__index {
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #99d0ee 0%, #4da8d8 100%);
  color: #fff;
  font-weight: 800;
  font-size: 15px;
}

.step-card h3 {
  margin: 0 0 10px;
  font-size: 20px;
}

.step-card p {
  margin: 0;
  color: var(--text-soft);
  line-height: 1.6;
}

@media (max-width: 980px) {
  .how-it-works__grid {
    grid-template-columns: 1fr;
  }
}
</style>