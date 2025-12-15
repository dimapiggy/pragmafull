<template>
  <div class="task-form-card">
    <!-- Заголовок -->
    <div class="task-form-header">
      <button 
        class="back-btn"
        @click="$emit('close')"
        title="Вернуться к задачам"
      >
        ←
      </button>
      <h2 class="task-form-title">{{ isEditing ? 'Редактировать задачу' : 'Создать новую задачу' }}</h2>
    </div>

    <!-- Форма -->
    <form @submit.prevent="handleSubmit" class="task-form">
      <!-- Основные поля -->
      <div class="form-group">
        <label for="task-title">Название задачи *</label>
        <input
          id="task-title"
          v-model="formData.title"
          type="text"
          placeholder="Что нужно сделать?"
          required
          class="form-input"
          :disabled="loading"
        >
      </div>
      
      <div class="form-group">
        <label for="task-description">Описание</label>
        <textarea
          id="task-description"
          v-model="formData.description"
          placeholder="Дополнительные детали..."
          class="form-textarea"
          rows="3"
          :disabled="loading"
        ></textarea>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="task-deadline">Дедлайн</label>
          <input
            id="task-deadline"
            v-model="formData.deadline"
            type="datetime-local"
            class="form-input"
            :disabled="loading"
          >
        </div>
        
        <!-- Поле для выбора тега -->
        <div class="form-group">
          <label for="task-tag">Тег</label>
          <div class="tag-selector">
            <div class="tag-options">
              <button
                v-for="tagOption in tagOptions"
                :key="tagOption.id"
                type="button"
                class="tag-option"
                :class="{ 
                  'tag-option-selected': formData.tag_id === tagOption.id,
                  'tag-option-colored': tagOption.color
                }"
                :style="{ backgroundColor: tagOption.color || '#6c757d' }"
                @click="selectTag(tagOption.id)"
                :title="tagOption.name"
              >
                {{ tagOption.name }}
              </button>
              <button
                type="button"
                class="tag-option tag-option-new"
                @click="showNewTagForm = true"
                title="Создать новый тег"
              >
                + Новый тег
              </button>
            </div>
            
            <!-- Форма создания нового тега -->
            <div v-if="showNewTagForm" class="new-tag-form">
              <div class="new-tag-inputs">
                <input
                  v-model="newTagName"
                  type="text"
                  placeholder="Название тега"
                  class="new-tag-input"
                  @keyup.enter="createNewTag"
                >
                <div class="color-picker">
                  <div 
                    v-for="color in colorPalette" 
                    :key="color"
                    class="color-option"
                    :style="{ backgroundColor: color }"
                    :class="{ 'color-option-selected': newTagColor === color }"
                    @click="newTagColor = color"
                    :title="color"
                  />
                </div>
              </div>
              <div class="new-tag-actions">
                <button
                  type="button"
                  class="new-tag-btn save"
                  @click="createNewTag"
                  :disabled="!newTagName.trim()"
                >
                  Создать
                </button>
                <button
                  type="button"
                  class="new-tag-btn cancel"
                  @click="cancelNewTag"
                >
                  Отмена
                </button>
              </div>
            </div>
            
            <!-- Кнопка сброса выбора тега -->
            <button
              v-if="formData.tag_id"
              type="button"
              class="clear-tag-btn"
              @click="clearTag"
            >
              Убрать тег
            </button>
          </div>
        </div>
      </div>
      
      <!-- Раздел метрик -->
      <div class="metrics-section">
        <div class="form-row">
          <div class="form-group">
            <label for="metric-l">L (трудоёмкость)</label>
            <input
              id="metric-l"
              v-model.number="formData.metrics.l"
              type="number"
              min="0"
              max="10"
              step="0.1"
              class="form-input"
              @input="updatePriority"
              :disabled="loading"
            >
            <div class="metric-help">Насколько задача трудоёмкая? (0-10)</div>
          </div>
          <div class="form-group">
            <label for="metric-v">V (важность)</label>
            <input
              id="metric-v"
              v-model.number="formData.metrics.v"
              type="number"
              min="0"
              max="10"
              step="0.1"
              class="form-input"
              @input="updatePriority"
              :disabled="loading"
            >
            <div class="metric-help">Насколько задача важная? (0-10)</div>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="metric-d">D (срочность)</label>
            <input
              id="metric-d"
              v-model.number="formData.metrics.d"
              type="number"
              min="0"
              max="10"
              step="0.1"
              class="form-input"
              @input="updatePriority"
              :disabled="loading"
            >
            <div class="metric-help">Насколько задача срочная? (0-10)</div>
          </div>
          <div class="form-group">
            <label for="metric-e">E (энергия)</label>
            <input
              id="metric-e"
              v-model.number="formData.metrics.e"
              type="number"
              min="0"
              max="10"
              step="0.1"
              class="form-input"
              @input="updatePriority"
              :disabled="loading"
            >
            <div class="metric-help">Сколько энергии требуется? (0-10)</div>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="metric-re">RE (ресурсы)</label>
            <input
              id="metric-re"
              v-model.number="formData.metrics.re"
              type="number"
              min="0"
              max="10"
              step="0.1"
              class="form-input"
              @input="updatePriority"
              :disabled="loading"
            >
            <div class="metric-help">Сколько ресурсов требуется? (0-10)</div>
          </div>
        </div>
      </div>
    </form>
    
    <!-- Кнопки действий прикрепленные к низу экрана с использованием ButtonMain -->
    <div class="form-actions-sticky">
      <ButtonMain
        variant="solid"
        tag="button"
        type="submit"
        height="48px"
        :disabled="!formData.title.trim() || loading"
        @click="handleSubmit"
        class="confirm-btn"
      >
        {{ loading ? 'Сохранение...' : isEditing ? 'Сохранить изменения' : 'Создать задачу' }}
      </ButtonMain>
      <ButtonMain
        variant="white"
        tag="button"
        height="48px"
        :disabled="loading"
        @click="$emit('close')"
        class="cancel-btn"
      >
        Отмена
      </ButtonMain>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useNuxtApp } from '#imports';
import ButtonMain from '~/components/ui/ButtonMain.vue';

const { $customFetch } = useNuxtApp();

const props = defineProps({
  task: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['submit', 'close']);

const API_BASE = 'http://localhost:8000';

// Расширенный массив цветов для тегов (18 цветов)
const colorPalette = [
  '#3B82F6', // синий
  '#10B981', // зеленый
  '#F59E0B', // янтарный
  '#EF4444', // красный
  '#8B5CF6', // фиолетовый
  '#EC4899', // розовый
  '#14B8A6', // бирюзовый
  '#F97316', // оранжевый
  '#6366F1', // индиго
  '#84CC16', // лаймовый
  '#06B6D4', // голубой
  '#A855F7', // пурпурный
  '#22C55E', // изумрудный
  '#EAB308', // желтый
  '#78716C', // серый
  '#DC2626', // красный-700
  '#7C3AED', // фиолетовый-600
  '#0EA5E9', // небесный
  '#F43F5E', // розовый-600
];

// Данные формы
const formData = ref({
  title: '',
  description: '',
  deadline: '',
  tag_id: null,
  metrics: {
    l: 1.0,
    v: 1.0,
    d: 1.0,
    e: 1.0,
    re: 1.0
  }
});

// Список доступных тегов
const tagOptions = ref([]);
const showNewTagForm = ref(false);
const newTagName = ref('');
const newTagColor = ref(colorPalette[0]);

// Проверяем, редактируем ли существующую задачу
const isEditing = computed(() => !!props.task);

// Функция для получения цвета на основе названия тега (детерминированная)
const getColorForTag = (tagName) => {
  if (!tagName) return colorPalette[0];
  
  // Создаем хэш из названия тега для детерминированного выбора цвета
  let hash = 0;
  for (let i = 0; i < tagName.length; i++) {
    hash = ((hash << 5) - hash) + tagName.charCodeAt(i);
    hash = hash & hash;
  }
  
  const index = Math.abs(hash) % colorPalette.length;
  return colorPalette[index];
};

// Загружаем теги при монтировании
onMounted(async () => {
  await loadTags();
});

// Инициализация формы
watch(() => props.task, (newTask) => {
  if (newTask) {
    formData.value = {
      title: newTask.title || '',
      description: newTask.description || '',
      deadline: newTask.deadline ? formatForInput(newTask.deadline) : '',
      tag_id: newTask.tag?.id || null,
      metrics: newTask.metrics || {
        l: 1.0,
        v: 1.0,
        d: 1.0,
        e: 1.0,
        re: 1.0
      }
    };
  } else {
    formData.value = {
      title: '',
      description: '',
      deadline: '',
      tag_id: null,
      metrics: {
        l: 1.0,
        v: 1.0,
        d: 1.0,
        e: 1.0,
        re: 1.0
      }
    };
  }
}, { immediate: true });

// Рассчитываем приоритет
const calculatedPriority = computed(() => {
  const { l, v, d, e, re } = formData.value.metrics;
  const numerator = 1.2 * l + v + d;
  const denominator = e + re;
  
  if (denominator === 0) {
    return numerator === 0 ? 0 : numerator;
  }
  
  return numerator / denominator;
});

// Форматирование даты для input[type="datetime-local"]
const formatForInput = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toISOString().slice(0, 16);
};

// Загрузка тегов
const loadTags = async () => {
  try {
    const tags = await $customFetch(`${API_BASE}/tags/`, {
      method: 'GET',
      credentials: 'include',
    });
    
    if (Array.isArray(tags)) {
      // Присваиваем цвета тегам, если они не пришли с сервера
      tagOptions.value = tags.map(tag => ({
        ...tag,
        color: tag.color || getColorForTag(tag.name)
      }));
    } else {
      // В случае если ответ не массив, создаем базовые теги с цветами
      tagOptions.value = [
        { id: 1, name: 'Работа', color: getColorForTag('Работа') },
        { id: 2, name: 'Личное', color: getColorForTag('Личное') },
        { id: 3, name: 'Срочно', color: getColorForTag('Срочно') },
        { id: 4, name: 'Идеи', color: getColorForTag('Идеи') },
        { id: 5, name: 'Проект', color: getColorForTag('Проект') },
      ];
    }
  } catch (err) {
    console.error('❌ Ошибка загрузки тегов:', err);
    // В случае ошибки создаем базовые теги с цветами
    tagOptions.value = [
      { id: 1, name: 'Работа', color: getColorForTag('Работа') },
      { id: 2, name: 'Личное', color: getColorForTag('Личное') },
      { id: 3, name: 'Срочно', color: getColorForTag('Срочно') },
      { id: 4, name: 'Идеи', color: getColorForTag('Идеи') },
      { id: 5, name: 'Проект', color: getColorForTag('Проект') },
    ];
  }
};

// Создание нового тега
const createNewTag = async () => {
  if (!newTagName.value.trim()) return;

  try {
    const newTag = await $customFetch(`${API_BASE}/tags/`, {
      method: 'POST',
      body: {
        name: newTagName.value.trim(),
        color: newTagColor.value
      },
      credentials: 'include',
    });

    // Добавляем новый тег в список
    tagOptions.value.push({
      ...newTag,
      color: newTag.color || newTagColor.value
    });
    
    // Выбираем новый тег
    formData.value.tag_id = newTag.id;
    
    // Сбрасываем форму создания тега
    cancelNewTag();
  } catch (err) {
    console.error('❌ Ошибка создания тега:', err);
    alert('Не удалось создать тег');
  }
};

// Отмена создания нового тега
const cancelNewTag = () => {
  showNewTagForm.value = false;
  newTagName.value = '';
  newTagColor.value = colorPalette[0];
};

// Выбор тега
const selectTag = (tagId) => {
  formData.value.tag_id = tagId;
  showNewTagForm.value = false;
};

// Очистка выбора тега
const clearTag = () => {
  formData.value.tag_id = null;
};

// Обновление приоритета
const updatePriority = () => {
  // Автоматически вычисляется через computed свойство
};

// Обработка отправки формы
const handleSubmit = async () => {
  if (!formData.value.title.trim() || props.loading) return;
  
  const taskData = {
    title: formData.value.title.trim(),
    description: formData.value.description || null,
    deadline: formData.value.deadline ? new Date(formData.value.deadline).toISOString() : null,
    tag_id: formData.value.tag_id || null,
    metrics: formData.value.metrics
  };
  
  emit('submit', { 
    data: taskData, 
    isEditing, 
    taskId: props.task?.id 
  });
};
</script>

<style scoped>
.task-form-card {
  margin-top: 12px;
  position: relative;
  padding: 24px;
  border: 1px solid #dee2e6;
  border-radius: 15px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 100px; /* Отступ для кнопок */
  min-height: calc(100vh - 200px); /* Минимальная высота */
  display: flex;
  flex-direction: column;
}

.task-form-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e9ecef;
  flex-shrink: 0;
}

.task-form-title {
  margin: 0;
  font-size: 20px;
  color: #212529;
  font-weight: 600;
  flex: 1;
}

.back-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #6c757d;
  cursor: pointer;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #f8f9fa;
  color: #212529;
}

.task-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
  flex: 1;
  overflow-y: auto;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #495057;
}

.form-group label[for="task-title"]::after {
  content: '*';
  color: #dc3545;
  margin-left: 4px;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #ced4da;
  border-radius: 30px;
  font-size: 15px;
  color: #212529;
  background: white;
  transition: all 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #86b7fe;
  box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

/* Стили для метрик */
.metrics-section {
  margin-top: 10px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
  border: 1px solid #e9ecef;
}

.metrics-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0;
  margin-bottom: 20px;
  color: #495057;
  font-size: 16px;
}

.priority-preview {
  font-size: 14px;
  font-weight: 600;
  color: #0d6efd;
  background: white;
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid #dee2e6;
}

.metric-help {
  font-size: 12px;
  color: #6c757d;
  margin-top: 6px;
  font-style: italic;
}

.calculated-priority-display {
  text-align: center;
  padding: 16px;
  background: white;
  border-radius: 8px;
  border: 2px solid #28a745;
}

.priority-value {
  font-size: 28px;
  font-weight: bold;
  color: #28a745;
  display: block;
  margin-bottom: 8px;
}

.priority-formula {
  font-size: 12px;
  color: #6c757d;
  font-family: monospace;
  background: #f8f9fa;
  padding: 4px 8px;
  border-radius: 4px;
}

/* Стили для выбора тега */
.tag-selector {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tag-options {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-option {
  padding: 6px 12px;
  border: 1px solid #dee2e6;
  border-radius: 16px;
  background: #f8f9fa;
  color: #495057;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.tag-option-colored {
  color: white;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.tag-option-colored::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(0, 0, 0, 0.1) 100%);
  border-radius: 14px;
}

.tag-option:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
}

.tag-option-selected {
  border-color: #212529;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
}

.tag-option-new {
  background: white;
  border: 1px dashed #0d6efd;
  color: #0d6efd;
}

.tag-option-new:hover {
  background: #f0f7ff;
}

.clear-tag-btn {
  align-self: flex-start;
  padding: 4px 8px;
  background: none;
  border: none;
  color: #6c757d;
  font-size: 12px;
  cursor: pointer;
  text-decoration: underline;
  transition: color 0.2s;
}

.clear-tag-btn:hover {
  color: #dc3545;
}

/* Форма создания нового тега */
.new-tag-form {
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.new-tag-inputs {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 12px;
}

.new-tag-input {
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 14px;
  width: 100%;
}

.new-tag-input:focus {
  outline: none;
  border-color: #86b7fe;
  box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.1);
}

.color-picker {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: center;
}

.color-option {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s;
}

.color-option:hover {
  transform: scale(1.1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.color-option-selected {
  border-color: #212529;
  box-shadow: 0 0 0 2px white, 0 0 0 4px #212529;
}

.new-tag-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.new-tag-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.new-tag-btn.save {
  background: #0d6efd;
  color: white;
}

.new-tag-btn.save:hover:not(:disabled) {
  background: #0b5ed7;
}

.new-tag-btn.save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.new-tag-btn.cancel {
  background: #6c757d;
  color: white;
}

.new-tag-btn.cancel:hover {
  background: #5a6268;
}

/* Кнопки действий прикрепленные к низу экрана */
.form-actions-sticky {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px 20px;
  background: white;
  border-top: 1px solid #e9ecef;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 16px;
  z-index: 100;
  max-width: 800px;
  margin: 0 auto;
  justify-content: center;
}

.cancel-btn,
.confirm-btn {
  flex: 1;
  max-width: 220px;
}

/* Адаптивность */
@media (max-width: 768px) {
  .task-form-card {
    padding: 16px;
    margin-bottom: 90px;
    min-height: calc(100vh - 180px);
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .metrics-title {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .priority-preview {
    align-self: flex-start;
  }
  
  .form-actions-sticky {
    padding: 12px 16px;
    gap: 12px;
  }
  
  .cancel-btn,
  .confirm-btn {
    max-width: 200px;
    height: 44px;
  }
  
  .tag-options {
    gap: 6px;
  }
  
  .tag-option {
    padding: 5px 10px;
    font-size: 12px;
  }
  
  .color-option {
    width: 20px;
    height: 20px;
  }
}

@media (max-width: 480px) {
  .task-form-card {
    padding: 12px;
    margin-bottom: 80px;
    min-height: calc(100vh - 160px);
  }
  
  .task-form-title {
    font-size: 18px;
  }
  
  .form-actions-sticky {
    padding: 12px;
    gap: 12px;
    align-items: center;
  }
  
  .cancel-btn,
  .confirm-btn {
    max-width: 100%;
    width: 100%;
    height: 44px;
  }
  
  .tag-options {
    justify-content: center;
  }
}

/* Для очень маленьких экранов */
@media (max-height: 600px) {
  .task-form-card {
    margin-bottom: 70px;
  }
  
  .form-actions-sticky {
    padding: 10px 12px;
  }
  
  .cancel-btn,
  .confirm-btn {
    height: 42px;
  }
}
</style>