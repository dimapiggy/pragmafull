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
          <Icon icon="03" />
          <img src="~/assets/svg/6step.svg" alt="">
        </div>
      </div>

      <div class="intro">
        <h2>Стиль общения ассистента</h2>
        <div class="intro__points">
          <div class="intro__point">
            <div class="intro__text">
              <span class="intro__highlight">Сдержанный:</span> быстрые и конкретные ответы для тех, кто ценит время.
            </div>
          </div>

          <div class="intro__point">
            <div class="intro__text">
              <span class="intro__highlight">Дружелюбный:</span> тёплый, с нотками мотивации и поддержкой.
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="onb__buttons">
      <ButtonMain @click="form.assistantStyle = 'restrained'; step++">
        Сдержанный
      </ButtonMain>
      <div>
        <ButtonMain variant="white" @click="form.assistantStyle = 'friendly'; step++">
          Дружелюбный
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
.intro__highlight {
  color: $mainblue;
  font-weight: 600;
}
</style>
