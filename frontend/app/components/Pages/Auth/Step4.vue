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
          <Icon icon="01" />
          <img src="~/assets/svg/4step.svg" alt="">
        </div>
      </div>

      <div class="intro">
        <h2>Ваше имя:</h2>
        <div class="intro__text">
          Давайте познакомимся! Ваше имя поможет нам обращаться к вам по-дружески и персонализировать приложение.
        </div>
      </div>

      <InputCustom
        v-model="form.fullname"
        label="Ваше имя"
        placeholder="Введите ваше имя"
      />
    </div>

    <div class="onb__buttons">
      <div>
        <ButtonMain @click="step++">Продолжить</ButtonMain>
        <ButtonMain variant="transparent" @click="step--">Назад</ButtonMain>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.onb__wrapper {
  justify-content: space-between;
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
