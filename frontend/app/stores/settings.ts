export const useSettingsStore = defineStore('settings', () => {
  const inputTypeItems = ref([
    { title: 'Быстрый', value: 'quick' },
    { title: 'Подробный', value: 'detailed' },
  ]);

  const assistantStyleItems = ref([
    { title: 'Сдержанный', value: 'restrained' },
    { title: 'Дружелюбный', value: 'friendly' },
  ]);

  const notificationsItems = ref([
    { title: 'Вкл.', value: true },
    { title: 'Выкл.', value: false },
  ]);

  return { inputTypeItems, assistantStyleItems, notificationsItems };
});
