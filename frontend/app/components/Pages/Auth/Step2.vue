<script setup lang="ts">
const step = defineModel<number>({ required: true });
</script>

<template>
  <div class="onb__wrapper">
    <h1>Добро пожаловать в PRAGMA!</h1>
    <img src="~/assets/svg/2step.svg" alt="">
    <div class="intro__text">
      <p>Создавайте задачи за секунды, редактируйте сроки и приоритеты, отслеживайте прогресс в одном месте.</p>
      <p>От первого наброска до «Готово» — всё под рукой.</p>
    </div>

    <ButtonMain @click="step++">Продолжить</ButtonMain>
  </div>
</template>
