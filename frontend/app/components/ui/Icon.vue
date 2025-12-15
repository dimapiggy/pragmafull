<script lang="ts" setup>
import type { Component } from 'vue';

interface Props {
  icon: string
  width?: string | number
  height?: string | number
  size?: string | number
  color?: string
}

const props = defineProps<Props>();

const isMdiIcon = computed(() => {
  return props.icon.includes('mdi-');
});

const projectIcon = shallowRef<Component | null>(null);

const iconWidth = computed(() => {
  if (props.size) return `${props.size}px`;
  if (props.width) return `${props.width}px`;
  return null;
});

const iconHeight = computed(() => {
  if (props.size) return `${props.size}px`;
  if (props.height) return `${props.height}px`;
  return null;
});

const iconColor = computed(() => props.color || 'currentColor');

watch(() => props.icon, async () => {
  if (!isMdiIcon.value) {
    try {
      const iconModule = await import(`~/assets/icons/${props.icon}.svg?component`);
      projectIcon.value = iconModule.default;
    } catch {
      console.log(`Icon ${props.icon} not found`);
    }
  }
}, { immediate: true });
</script>

<template>
  <v-icon v-if="isMdiIcon" :icon="icon" :size="size" :color="iconColor" />

  <component
    :is="projectIcon"
    v-else
    class="icon"
    :style="{
      width: iconWidth,
      height: iconHeight,
      color: iconColor,
      display: 'block',
    }"
  />
</template>

<style lang="scss" scoped>
.icon {
  // 🔑 SVG сохраняет свои оригинальные размеры
  flex-shrink: 0;

  // Если нужно ограничить максимальный размер
  max-width: 100%;
  max-height: 100%;
}
</style>
