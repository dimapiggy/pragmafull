<script setup lang="ts">
import { onClickOutside } from '@vueuse/core';

interface IItem {
  title: string
  value: string | number | boolean | null
}

const modelValue = defineModel<string | number | boolean | null>();

const props = defineProps<{
  items: IItem[]
  isOpen?: boolean
  readonly?: boolean
}>();

const emit = defineEmits<{
  'update:isOpen': [value: boolean]
}>();

const select = useTemplateRef('select');

onClickOutside(select, () => emit('update:isOpen', false));

const valueString = computed(() => {
  const found = props.items.find(i => i.value === modelValue.value);
  return found ? found.title : 'Не выбрано';
});

function selectItem(item: IItem) {
  modelValue.value = item.value;
  emit('update:isOpen', false);
}
</script>

<template>
  <div ref="select" class="app-simple-select__wrap" :class="{ opened: props.isOpen }">
    <div
      class="app-simple-select__value"
      @click="!props.readonly && emit('update:isOpen', !props.isOpen)"
    >
      {{ valueString }}
    </div>

    <Transition name="dropdown">
      <div v-if="props.isOpen" class="app-simple-select__dropdown">
        <div
          v-for="item in props.items"
          :key="item.title"
          class="app-simple-select__dropdown-item"
          :class="{ active: item.title === valueString }"
          @click="selectItem(item)"
        >
          {{ item.title }}
        </div>
      </div>
    </Transition>
  </div>
</template>

<style lang="scss">
.app-simple-select__wrap {
  position: relative;
  width: 100%;
}

.app-simple-select__value {
  display: flex;
  align-items: center;
  gap: 5px;
  line-height: 90%;
  cursor: pointer;
  color: #76333C;

  @media (max-width: 768px) {
    font-size: 14px;
  }

  .icon {
    flex-shrink: 0;
    transition: var(--base-transition);
  }
}

.app-simple-select__dropdown {
  position: absolute;
  top: calc(100% + 10px);
  left: 0;
  right: 0;
  padding: 10px;
  border-radius: 10px;
  border: #F2F2F2;
  background: #FFF;
  box-shadow: 0 4px 4px rgba(0,0,0,0.25);
  z-index: 2;
  width: 100%;
  box-sizing: border-box;
}

.app-simple-select__dropdown-item {
  width: 100%;
  font-size: 14px;
  line-height: 130%;
  cursor: pointer;
  transition: var(--base-transition);
  box-sizing: border-box;

  &:hover,
  &.active {
    color: #76333C;
  }

  & + & {
    margin-top: 10px;
  }
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.3s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
