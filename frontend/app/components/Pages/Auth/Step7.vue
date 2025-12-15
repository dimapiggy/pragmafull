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
          <Icon icon="04" />
          <img src="~/assets/svg/7step.svg" alt="">
        </div>
      </div>

      <div class="intro">
        <h2 class="intro__title">Уведомления</h2>
        <div class="intro__text">
          <p>Включить или выключить уведомления?</p>
          <p>Вы можете поменять этот параметр в любой момент в настройках приложения.</p>
        </div>

        <div class="intro__points">
          <div class="intro__point">
            <span class="intro__highlight">Уведомления</span>
          </div>
          <Switch v-model="form.notifications_enabled" />
        </div>

        <Transition>
          <div v-if="form.notifications_enabled" class="intro__time">
            <TimePicker
              :model-value="form.notification_time || '09:00'"
              label="Время уведомлений"
              right-icon="clock"
              min="00:00"
              max="23:59"
              @update:model-value="form.notification_time = $event"
            />
          </div>
        </Transition>
      </div>
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
  height: 100px;
}

.intro__time {
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

.time-input-wrap {
  margin-top: 15px;
  width: 100%;
}

.intro__points {
  flex-direction: row;
}

.onb__buttons {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 300px;
  align-items: center;
  margin-bottom: 40px;
  gap: 16px;
}

.onb__buttons .blue-button {
  font-weight: 700;
}

.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
