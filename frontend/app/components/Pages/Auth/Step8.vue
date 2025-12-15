<script lang="ts" setup>
import type { IOnboardingForm } from '~/types/auth';

const form = defineModel<IOnboardingForm>('form', { required: true });

const emit = defineEmits<{
  saveUser: []
}>();

const { assistantStyleItems, inputTypeItems, notificationsItems } = storeToRefs(useSettingsStore());

const activeSelects = ref({
  taskType: false,
  assistantStyle: false,
  notifications: false,
});

const isEditingName = ref(false);

function toggleSelect(selectName: keyof typeof activeSelects.value) {
  Object.keys(activeSelects.value).forEach(function (key) {
    if (key !== selectName) {
      activeSelects.value[key as keyof typeof activeSelects.value] = false;
    }
  });

  activeSelects.value[selectName] = !activeSelects.value[selectName];
}

function toggleNameEditing() {
  isEditingName.value = !isEditingName.value;
}

function handleNameInputKeydown(event: KeyboardEvent) {
  if (event.key === 'Enter') {
    isEditingName.value = false;
  }
}

function startWork() {
  emit('saveUser');
}
</script>

<template>
  <div class="onb__wrapper">
    <h1>Финальный этап</h1>
    <img class="last__logo" src="~/assets/svg/logowithtext.svg" alt="">
    <h2 class="intro__title">Подтверждение данных:</h2>

    <div class="confirmation">
      <div class="input-column" :class="{ editing: isEditingName }">
        <div class="input-group">
          <div class="type-title">Имя:</div>
          <input
            v-model="form.fullname"
            :readonly="!isEditingName"
            type="text"
            placeholder="Введите имя"
            @keydown="handleNameInputKeydown"
          >
        </div>
        <img
          src="~/assets/icons/pencil.svg"
          alt=""
          class="icon"
          :class="{ active: isEditingName }"
          @click="toggleNameEditing"
        >
      </div>

      <div class="select-column">
        <div class="input-group">
          <div class="type-title">Тип добавления задач:</div>
          <AppSimpleSelect
            v-model="form.task_creation_type"
            :items="inputTypeItems"
            :readonly="true"
            :is-open="activeSelects.taskType"
            @update:is-open="activeSelects.taskType = $event"
          />
        </div>
        <img
          src="~/assets/icons/arrowright.svg"
          alt=""
          class="icon arrow"
          :class="{ rotated: activeSelects.taskType }"
          @click="toggleSelect('taskType')"
        >
      </div>

      <div class="select-column">
        <div class="input-group">
          <div class="type-title">Стиль ассистента:</div>
          <AppSimpleSelect
            v-model="form.assistantStyle"
            :items="assistantStyleItems"
            :readonly="true"
            :is-open="activeSelects.assistantStyle"
            @update:is-open="activeSelects.assistantStyle = $event"
          />
        </div>
        <img
          src="~/assets/icons/arrowright.svg"
          alt=""
          class="icon arrow"
          :class="{ rotated: activeSelects.assistantStyle }"
          @click="toggleSelect('assistantStyle')"
        >
      </div>

      <div class="select-column">
        <div class="input-group">
          <div class="type-title">Уведомления:</div>
          <AppSimpleSelect
            v-model="form.notifications_enabled"
            :items="notificationsItems"
            :readonly="true"
            :is-open="activeSelects.notifications"
            @update:is-open="activeSelects.notifications = $event"
          />
        </div>
        <img
          src="~/assets/icons/arrowright.svg"
          alt=""
          class="icon arrow"
          :class="{ rotated: activeSelects.notifications }"
          @click="toggleSelect('notifications')"
        >
      </div>

      <Transition>
        <div v-if="form.notifications_enabled" class="intro__time">
          <TimePicker
            :model-value="form.notification_time || '09:00'"
            label="Время уведомлений"
            right-icon="clock"
            min="00:00"
            max="23:59"
            @update:model-value="form.notification_time = $event"
          />
        </div>
      </Transition>
    </div>

    <div class="buttons">
      <ButtonMain @click="startWork">Начать работу</ButtonMain>
    </div>
  </div>
</template>

<style lang="scss" scoped>
strong {
  color: $mainblue;
}

h1 {
  text-align: left;
  font-weight: bold;
  font-size: 24px;
  line-height: 120%;
  color: $mainblue;
  width: 100%;
}

.type-title {
  color: $mainblue;
  margin-bottom: 4px;
  font-size: 14px;
}

.confirmation {
  width: 100%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  font-size: 16px;
  line-height: 140%;
  text-align: left;
}

.input-column,
.select-column {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #D4D4D8;
  padding: 5px 0;
  transition: border-color 0.3s ease;
}

.input-column.editing {
  border-bottom-color: $mainblue;
}

.input-group {
  display: flex;
  flex-direction: column;
  flex: 1;
  justify-content: center;
  padding: 5px 0;
  cursor: pointer;
}

.input-group input,
:deep(.app-simple-select__value) {
  border: none;
  background: transparent;
  font-size: 14px;
  color: #111;
  display: flex;
  align-items: flex-end;
  width: 100%;
  font-family: inherit;
  line-height: 1.4;
}

.input-group input:read-only {
  cursor: default;
  pointer-events: none;
}

.input-group input:not(:read-only) {
  cursor: text;
  pointer-events: all;
}

:deep(.app-simple-select__value) {
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

:deep(.app-simple-select__value) {
  font-weight: normal;
}

:deep(.app-simple-select__dropdown-item) {
  font-size: 14px;
  color: #111;
  font-weight: normal;
  line-height: 1.4;
  padding: 2px;
}

:deep(.app-simple-select__dropdown-item.active) {
  color: $mainblue;
  font-weight: 500;
}

:deep(.app-simple-select__value .icon) {
  width: 16px;
  height: 16px;
  color: #666;
  margin-left: auto;
}

.icon {
  cursor: pointer;
  margin-left: 8px;
  align-self: center;
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.input-column .icon {
  width: 20px;
  height: 20px;
  opacity: 0.7;
  transition: opacity 0.3s ease;
}

.input-column .icon.active,
.input-column .icon:hover {
  opacity: 1;
}

.select-column .icon.arrow {
  width: 10px;
  height: 10px;
}

.select-column .icon.arrow.rotated {
  transform: rotate(90deg);
}

input[type='time'] {
  width: 100%;
  padding: 8px 0;
  border: none;
  border-bottom: 1px solid grey;
  background: transparent;
  font-size: 16px;
  color: #111;
  text-align: left;
}

.intro__time {
  margin-top: 10px;
}
</style>
