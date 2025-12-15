<script setup lang="ts">
import Inputmask from 'inputmask';

const modelValue = defineModel<string | number | null>({ required: true });

export interface Props {
  label?: string
  hideLabel?: boolean
  type?: string
  placeholder?: string
  disabled?: boolean
  readonly?: boolean
  clearable?: boolean
  required?: boolean
  rightIcon?: string
  rightIconColor?: string
  leftIcon?: string
  disabledLeftIcon?: boolean
  hint?: string
  maxlength?: string | number
  error?: string | boolean
  compact?: boolean
  mask?: Inputmask.Options
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
});

const emit = defineEmits<{
  'input': [value: string | number | null]
  'change': [value: string | number | null]
  'click:left': []
  'click:right': []
  'click:clear': []
  'focus': []
  'blur': []
}>();

defineExpose({ focusInput, blurInput, selectInput });

const isInputFocused = ref<boolean>(false);
const inputEl = ref<HTMLInputElement | null>(null);

onMounted(() => {
  initMask();
});

function initMask() {
  if (props.mask && inputEl.value) {
    Inputmask(props.mask).mask(inputEl.value);
  }
}

function inputEvent(e: Event) {
  const target = e.target as HTMLInputElement;
  if (!props.maxlength || +target.value.length <= +props.maxlength) {
    modelValue.value = target.value;
    emit('input', modelValue.value);
  } else {
    inputEl.value!.value = target.value.slice(0, +props.maxlength);
  }
}

function clearInput() {
  modelValue.value = props.type !== 'number' ? '' : '0';
  emit('click:clear');
  focusInput();
}

function focusInput() {
  if (props.disabled || props.readonly) return;
  inputEl.value?.focus();
  isInputFocused.value = true;
}

function blurInput() {
  inputEl.value?.blur();
  isInputFocused.value = false;
  emit('blur');
}

function selectInput() {
  inputEl.value?.focus();
  inputEl.value?.select();
  isInputFocused.value = true;
}
</script>

<template>
  <div
    class="input-custom"
    :class="{ 'error-item': error }"
    v-bind="$attrs"
  >
    <div
      class="input-custom__input-wrap"
      :class="{
        'input-custom__input-wrap--with-left-icon': leftIcon,
        'input-custom__input-wrap--with-right-icon': clearable || rightIcon,
        'input-custom__input-wrap--disabled': disabled,
      }"
    >
      <label
        v-if="label && !hideLabel"
        class="input-custom__label"
      >
        {{ label }}
      </label>

      <div class="input-custom__input-block" :class="{ 'input-custom__input-block--required': required }">
        <input
          ref="inputEl"
          :value="modelValue"
          class="input-custom__input"
          :class="{ 'input-custom__input--compact': compact }"
          :type="type"
          :placeholder="placeholder"
          :disabled="disabled"
          :readonly="readonly"
          autocomplete="nope"
          :maxlength="maxlength"
          @focus="isInputFocused = true, $emit('focus')"
          @blur="isInputFocused = false, $emit('blur')"
          @input.stop="inputEvent"
          @change.stop="emit('change', $event.target?.value)"
        >
        <button
          v-if="(modelValue || modelValue == 0) && clearable && !disabled && !readonly && !rightIcon"
          type="button"
          class="input-custom__clear"
          @click.stop.prevent="clearInput"
        >
          <Icon icon="mdi-close" />
        </button>
        <button
          v-if="leftIcon"
          type="button"
          class="input-custom__left-icon"
          :disabled="disabledLeftIcon"
          @click.prevent="emit('click:left')"
        >
          <Icon :icon="leftIcon" color="#8AACCD" />
        </button>
        <button
          v-if="rightIcon"
          type="button"
          class="input-custom__right-icon"
          @click.prevent="emit('click:right')"
        >
          <Icon :icon="rightIcon" :color="rightIconColor ? rightIconColor : '#2B77F5'" />
        </button>
      </div>

      <div v-if="error && typeof error === 'string'" class="input-custom__error">{{ error }}</div>
      <div v-if="hint && !error" class="input-custom__hint">{{ hint }}</div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.input-custom {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

label {
  padding-left: 15px;
  text-align: left;
  font-weight: 500;
  color: $mainblue;
}

.input-custom__input-block {
  position: relative;
}

.input-custom__input {
  margin-top: 10px;
  width: 100%;
  height: 50px;
  border-radius: 25px;
  border: 1px solid $mainblue;
  padding: 0 20px;
  font-size: 14px;
  outline: none;
  transition: all 0.2s ease;
  background: #fff;
}

.input-custom__input::placeholder {
  color: #8fa1b3;
  font-size: 14px;
}

.input-custom__input:focus {
  border-color: #3e3ebb;
}

.input-custom__input:disabled {
  background: #f2f2f2;
  color: #8fa1b3;
  cursor: not-allowed;
}

.input-custom__clear {
  position: absolute;
  top: 0;
  bottom: 0;
  right: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  margin: auto;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.input-custom__input-wrap:hover .input-custom__clear,
.input-custom__input:focus ~ .input-custom__clear {
  opacity: 1;
}

.input-custom__left-icon,
.input-custom__right-icon {
  position: absolute;
  top: 25%;
  bottom: 0;
  display: flex;
  width: 24px;
  height: 24px;
  margin: auto;
}

.input-custom__left-icon {
  left: 14px;
}

.input-custom__right-icon {
  right: 14px;
}

.input-custom__error {
  color: #ff4d4f;
  font-size: 13px;
  padding-left: 15px;
}

.input-custom__hint {
  color: #8fa1b3;
  font-size: 13px;
  padding-left: 15px;
}
</style>
