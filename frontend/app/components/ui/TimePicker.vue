<script setup lang="ts">
interface Props {
  label?: string
  icon?: string
  rightIcon?: string
  iconWidth?: string
  iconHeight?: string
  min?: string
  max?: string
  disabled?: boolean
  error?: string
}

const props = defineProps<Props>();

const modelValue = defineModel<string>({ required: true });

const pickedHours = ref<string>('');
const pickedMinutes = ref<string>('');
const isOpenTimepicker = ref<boolean>(false);

const timePickerFormatted = computed<string>(() => {
  if (pickedHours.value && pickedMinutes.value) {
    return `${pickedHours.value}:${pickedMinutes.value}`;
  } else if (pickedHours.value) {
    return `${pickedHours.value}:--`;
  } else if (pickedMinutes.value) {
    return `--:${pickedMinutes.value}`;
  }
  return '--:--';
});

watchEffect(() => {
  if (modelValue.value.split(':').length >= 2) {
    pickedHours.value = modelValue.value.split(':')[0];
    pickedMinutes.value = modelValue.value.split(':')[1];
  } else if (!modelValue.value) {
    pickedHours.value = '';
    pickedMinutes.value = '';
  }
});

function setTime(value: number, field: 'hours' | 'minutes') {
  if (isDisabledTime(value, field)) {
    return;
  }

  if (field === 'hours') {
    pickedHours.value = value.toString().padStart(2, '0');
  } else {
    pickedMinutes.value = value.toString().padStart(2, '0');

    if (pickedHours.value) {
      isOpenTimepicker.value = false;
    }
  }

  scrollToActiveTime('smooth');

  if (pickedHours.value && pickedMinutes.value) {
    modelValue.value = `${pickedHours.value}:${pickedMinutes.value}`;
  }
}

function onOpenTimePicker(value: boolean) {
  if (value) {
    scrollToActiveTime('instant');
  }
}

async function scrollToActiveTime(scrollBehavior: 'smooth' | 'instant') {
  await nextTick();

  const colsEl = document.querySelectorAll('.time-picker__dropdown-col');

  colsEl.forEach((col) => {
    const activeItem: HTMLDivElement | null = col.querySelector('.active');

    if (activeItem) {
      col.scrollTo({ top: activeItem.offsetTop - 80, behavior: scrollBehavior });
    }
  });
}

function isDisabledTime(value: number, field: 'hours' | 'minutes'): boolean {
  if (props.min || props.max) {
    const minHours = props.min ? props.min.split(':')[0] : '';
    const minMinutes = props.min ? props.min.split(':')[1] : '';
    const maxHours = props.max ? props.max.split(':')[0] : '';
    const maxMinutes = props.max ? props.max.split(':')[1] : '';

    if (field === 'hours') {
      if (props.min && props.max) {
        return (value < +minHours || value > +maxHours)
          || (value === +minHours && pickedMinutes.value < minMinutes)
          || (value === +maxHours && pickedMinutes.value > maxMinutes);
      } else if (props.min) {
        return (value < +minHours) || (value === +minHours && !!pickedMinutes.value && pickedMinutes.value < minMinutes);
      } else if (props.max) {
        return (value > +maxHours) || (value === +maxHours && !!pickedMinutes.value && pickedMinutes.value > maxMinutes);
      }
    } else {
      if ((minHours && pickedHours.value <= minHours) || (maxHours && pickedHours.value >= maxHours)) {
        if (minHours && pickedHours.value <= minHours) {
          return value < +minMinutes;
        } else if (maxHours && pickedHours.value >= maxHours) {
          return value > +maxMinutes;
        }
      }
      return false;
    }
  }
  return false;
}

function toggleTimepicker() {
  if (!props.disabled) {
    isOpenTimepicker.value = !isOpenTimepicker.value;
  }
}

function closeTimepicker() {
  isOpenTimepicker.value = false;
}
</script>

<template>
  <div class="time-picker__wrap">
    <InputCustom
      :model-value="timePickerFormatted"
      :label="label"
      placeholder="Выберите время"
      :left-icon="icon"
      :right-icon="rightIcon"
      :icon-width="iconWidth"
      :icon-height="iconHeight"
      readonly
      :disabled="disabled"
      :error="error"
      @click:right="toggleTimepicker"
      @click="toggleTimepicker"
      @blur="closeTimepicker"
    />

    <Transition name="timepicker">
      <div
        v-if="isOpenTimepicker"
        class="time-picker__dropdown"
        @mousedown.prevent
      >
        <div class="time-picker__dropdown-wrap">
          <div class="time-picker__dropdown-col">
            <div
              v-for="(hour, index) in 24"
              :key="hour"
              class="time-picker__dropdown-item"
              :class="{
                active: index.toString().padStart(2, '0') === pickedHours,
                disabled: isDisabledTime(index, 'hours'),
              }"
              @click="setTime(index, 'hours')"
            >
              {{ index.toString().padStart(2, '0') }}
            </div>
          </div>

          <div class="time-picker__dropdown-col">
            <div
              v-for="(minutes, index) in 60"
              :key="minutes"
              class="time-picker__dropdown-item"
              :class="{
                active: index.toString().padStart(2, '0') === pickedMinutes,
                disabled: isDisabledTime(index, 'minutes'),
              }"
              @click="setTime(index, 'minutes')"
            >
              {{ index.toString().padStart(2, '0') }}
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style lang="scss">
.time-picker__wrap {
  position: relative;
}

.time-picker__dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 1000;
  margin-top: 4px;
}

.time-picker__dropdown-wrap {
  display: flex;
  background: #fff;
  border-radius: 8px;
  box-shadow: 4px 4px 18px rgba(0, 0, 0, 0.15);
  border: 1px solid var(--Grayscale-200);
}

.time-picker__dropdown-col {
  flex: 1 1 50%;
  max-width: 50%;
  max-height: 200px;
  overflow-y: auto;
}

.time-picker__dropdown-item {
  padding: 8px 16px;
  cursor: pointer;
  transition: background var(--base-transition);

  &:hover {
    background: #F9FAFE;
  }

  &.active {
    color: #fff;
    background: #0D63F3;
  }

  &.disabled {
    opacity: 0.3;
    pointer-events: none;
  }
}

/* Анимации для плавного появления и исчезновения TimePicker */
.timepicker-enter-active,
.timepicker-leave-active {
  transition: all 0.3s ease;
}

.timepicker-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.timepicker-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
