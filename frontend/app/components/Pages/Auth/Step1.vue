<script lang="ts" setup>
const step = defineModel<number>({ required: true });
</script>

<template>
  <div class="onb__wrapper">
    <img class="onb__logo" src="~/assets/svg/biglogo.svg" alt="Логотип">

    <h1 class="onb__title">Pragma</h1>

    <span class="onb__subtitle">Таск-трекер на каждый день</span>

    <ButtonMain @click="step++">Начать</ButtonMain>
  </div>
</template>

<style lang="scss" scoped>
.onb__wrapper {
  height: 100%;
  justify-content: center;
}

.onb__logo {
  height: 280px;
  width: auto;
  object-fit: contain;
}

.onb__title {
  font-weight: bold;
  font-size: 38px;
  line-height: 120%;
  letter-spacing: 2%;
  text-transform: uppercase;
}

.onb__subtitle {
  font-weight: 400;
  font-size: 20px;
  line-height: 120%;
  letter-spacing: 2%;
}
</style>
