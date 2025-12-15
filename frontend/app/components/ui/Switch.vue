<script setup lang="ts">
interface Props {
  modelValue: boolean
  label?: string
  labelAlign?: 'left' | 'right'
  additionalText?: string
  additionalTextColor?: string
  disabled?: boolean
  inline?: boolean
  readonly?: boolean
}

const props = defineProps<Props>();
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>();

function handleChange(event: Event) {
  const target = event.target as HTMLInputElement;
  emit('update:modelValue', target.checked);
};
</script>

<template>
  <label
    class="switch__wrap"
    :class="{ active: props.modelValue, disabled: !!props.disabled, inline: !!props.inline }"
  >
    <input
      v-show="false"
      type="checkbox"
      :checked="props.modelValue"
      :disabled="!!props.disabled"
      :readonly="!!props.readonly"
      @change="handleChange"
    >

    <div v-if="props.label" class="switch__label" :class="{ right: props.labelAlign === 'right' }">
      {{ props.label }}
    </div>

    <div v-if="props.additionalText" class="switch__additional-text" :style="{ color: props.additionalTextColor }">
      {{ props.additionalText }}
    </div>

    <div class="switch">
      <div class="switch__circle" :class="{ active: props.modelValue }" />
    </div>
  </label>
</template>

<style lang="scss">
.switch__wrap {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
  margin: 0;

  &.inline {
    width: max-content;
  }
}

.switch__wrap + .switch__wrap {
  margin-top: 16px;
}

.switch {
  position: relative;
  display: flex;
  align-items: center;
  flex-shrink: 0;
  width: 50px;
  height: 30px;
  border-radius: 50px;
  background: #71717A;
  transition: var(--base-transition);
  overflow: hidden;
}

.switch__circle {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 5px;
  width: 22px;
  height: 22px;
  margin: auto;
  border-radius: 50%;
  background: white;
  box-shadow: 0px 3px 8px rgba(0, 0, 0, 0.15), 0px 3px 1px rgba(0, 0, 0, 0.06);
  transition: var(--base-transition);

  &.active {
    left: 23px;
  }
}

.switch__label {
  font-size: 16px;
  line-height: 22px;
  color: var(--Grayscale-900);
  margin-right: auto;
  padding-right: 8px;

  &.right {
    padding-right: 0;
    margin-right: 8px;
  }
}

.switch__additional-text {
  font-size: 15px;
  line-height: 20px;
  color: #8AACCD;
  margin-right: 8px;
}

.switch__wrap.active {
  .switch {
    background: $mainblue;

  }

  .switch__label {
    color: #1D3145;
  }
}

.switch__wrap.disabled {
  cursor: not-allowed;

  .switch {
    opacity: .5;
  }
}
</style>
