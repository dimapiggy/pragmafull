<script lang="ts" setup>
const step = defineModel<number>({ required: true });
</script>

<template>
  <div class="onb__wrapper">
    <div class="content">
      <div class="onb__header">
        <h1>Начало работы</h1>
        <img src="~/assets/svg/3step.svg" alt="">
        <div class="intro__text">
          <p>Настройте приложение под себя: выберите параметры, которые вам важны.</p>
          <p>Не хотите сейчас? Пропустите — всё можно будет изменить позже в настройках.</p>
        </div>
      </div>
    </div>

    <div class="onb__buttons">
      <ButtonMain @click="step++">Продолжить</ButtonMain>
      <ButtonMain variant="white" @click="step+=5">Пропустить</ButtonMain>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.onb__wrapper {
  justify-content: space-between;
}

.onb__header {
  gap: 25px;
}

img {
  max-width: 90%;
  height: auto;
}
</style>
