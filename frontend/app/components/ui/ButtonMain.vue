<!-- components/ui/ButtonMain.vue -->
<script setup lang="ts">
import { NuxtLink } from '#components';

interface Props {
  variant?: 'solid' | 'white' | 'transparent'
  to?: string
  tag?: string
  height?: string
  fullWidth?: boolean
}

defineEmits(['click']);

const props = withDefaults(defineProps<Props>(), {
  variant: 'solid',
  height: '54px',
  fullWidth: false,
});

const buttonComponent = computed(() => {
  return props.to ? NuxtLink : props.tag ? props.tag : 'button';
});
</script>

<template>
  <component
    :is="buttonComponent"
    :to="to || undefined"
    class="blue-button"
    :class="[
      `blue-button--${props.variant}`,
      { 'blue-button--full-width': fullWidth },
    ]"
    @click="$emit('click')"
  >
    <slot />
  </component>
</template>

<style scoped lang="scss">
.blue-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 220px;
  height: v-bind('$props.height');
  flex-shrink: 0;
  font-size: 16px;
  font-weight: 500;
  border-radius: 100px;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  box-sizing: border-box;
}

.blue-button--full-width {
  width: 100% !important;
  max-width: 100%;
}

.blue-button--solid {
  color: $mainwhite;
  background-color: $mainblue;

  &:hover {
    background-color: $mainbluedarker;
  }
}

.blue-button--white {
  color: $mainblue;
  background-color: $mainwhite;
  border: 1px solid $mainblue;

  &:hover {
    background-color: rgb(243, 243, 243);
  }
}

.blue-button--transparent {
  color: $mainblue;
  background-color: transparent;
  border: none;
}
</style>
