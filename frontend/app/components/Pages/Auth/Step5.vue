<script lang="ts" setup>
import type { IOnboardingForm } from '~/types/auth';

const step = defineModel<number>({ required: true });
const form = defineModel<IOnboardingForm>('form', { required: true });
</script>

<template>
  <div class="onb__wrapper">
    <div class="content">
      <div class="onb__header">
        <h1>Начало работы</h1>
        <div class="header__top">
          <Icon icon="02" />
          <img src="~/assets/svg/5step.svg" alt="">
        </div>
      </div>

      <div class="intro">
        <h2>Тип добавления задач:</h2>
        <div class="intro__text">
          Выбирайте, как добавлять задачи: быстро, в пару кликов, или подробно — с приоритизацией по формуле. Работайте так, как удобно именно вам.
        </div>
      </div>
    </div>

    <div class="onb__buttons">
      <ButtonMain @click="form.task_creation_type = 'quick'; step++">
        Быстрый
      </ButtonMain>

      <div>
        <ButtonMain variant="white" @click="form.task_creation_type = 'detailed'; step++">
          Подробный
        </ButtonMain>
        <ButtonMain variant="transparent" @click="step--">Назад</ButtonMain>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.onb__wrapper {
  justify-content: space-between;
}

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  gap: 10px;
  margin-bottom: 30px;
}

.header__top {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  width: 100%;
}

img {
  max-width: 90%;
  height: auto;
}
</style>
