<script setup lang="ts">
</script>

<template>
  <header class="header">
    <div class="header__left">
      <img src="~/assets/svg/logo.svg">
      <span class="header__brand">Pragma</span>
    </div>
  </header>
</template>

<style lang="scss" scoped>
.header {
  display: flex;
  align-items: center;
  height: $headerheight;
  padding: 0 15px;
  background-color: $mainblack;
}

.header__left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header__brand {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
}

.header__btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  cursor: pointer;
  color: #fff;
  transition: opacity 0.2s ease;

  &:hover {
    opacity: 0.8;
  }
}

.header__btn-text {
  font-size: 16px;
  line-height: 1;
}
</style>
