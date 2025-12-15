<template>
  <div
    class="task-card"
    :class="{
      'task-done': task.is_done,
      'task-archived': task.archived,
    }"
  >
    <!-- Верхняя часть с приоритетом, датой и тегом -->
    <div class="task-top-bar">
      <div class="task-left-info">
        <div class="task-priority-badge">
          <div
            class="priority-color"
            :style="{ backgroundColor: getPriorityColor(task.priority) }"
          />
          <div class="priority-value">{{ task.priority?.toFixed(2) || '0.00' }}</div>
        </div>

        <div v-if="task.deadline" class="deadline-container">
          <div class="deadline-badge" :class="{ overdue: isOverdue && currentView === 'tasks' }">
            <span class="deadline-text">{{ formatDeadline(task.deadline) }}</span>
            <span v-if="isOverdue && currentView === 'tasks'" class="overdue-indicator">!</span>
          </div>
        </div>
      </div>

      <div v-if="task.tag" class="task-tag-badge">
        <div
          class="tag-circle"
          :style="{ backgroundColor: getTagColor(task.tag.name) }"
        >
          <span class="tag-text">{{ task.tag.name }}</span>
        </div>
      </div>
    </div>

    <!-- Убрали разделительную линию -->

    <div class="task-content">
      <!-- Контент -->
      <div class="task-main">
        <div class="task-header">
          <h3 class="task-title" :class="{ 'task-title-done': task.is_done }">
            {{ task.title }}
          </h3>

          <!-- Бейджи (статусы) -->
          <span v-if="isOverdue && currentView === 'tasks'" class="badge badge-overdue">Просрочено</span>
          <span v-if="task.archived && currentView === 'tasks'" class="badge badge-archive">Архив</span>
          <span v-if="task.is_done && !task.archived && currentView === 'tasks'" class="badge badge-done">Выполнено</span>
          <span v-if="task.is_done && task.archived && currentView === 'archive'" class="badge badge-done">Выполнено</span>
        </div>

        <!-- Описание -->
        <div v-if="task.description" class="task-description">
          {{ task.description }}
        </div>

        <!-- Подзадачи -->
        <div v-if="task.subtasks && task.subtasks.length > 0" class="subtasks">
          <div class="subtasks-title">Подзадачи</div>
          <div class="subtasks-list">
            <div
              v-for="subtask in task.subtasks"
              :key="subtask.id"
              class="subtask-item"
            >
              <label class="subtask-checkbox-container">
                <input
                  type="checkbox"
                  :checked="subtask.is_done"
                  :disabled="loading || task.archived"
                  class="subtask-checkbox"
                  :title="task.archived ? 'Задача в архиве' : ''"
                  @change="() => toggleSubtaskDone(subtask.id)"
                >
                <span class="checkmark" />
                <span
                  class="subtask-title"
                  :class="{ 'subtask-done': subtask.is_done }"
                >
                  {{ subtask.title }}
                </span>
              </label>
              
              <!-- Иконки действий для подзадачи -->
              <div v-if="currentView === 'tasks' && !task.archived" class="subtask-actions">
                <button
                  :disabled="loading"
                  class="subtask-action-btn edit-btn"
                  title="Редактировать подзадачу"
                  @click="() => editSubtask(subtask)"
                >
                  <Icon icon="pencil" size="16" />
                </button>
                <button
                  :disabled="loading"
                  class="subtask-action-btn delete-btn"
                  title="Удалить подзадачу"
                  @click="() => deleteSubtask(subtask.id)"
                >
                  <Icon icon="trash" size="16" />
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Форма добавления подзадачи (стиль как в OnboardingForm) -->
        <div v-if="currentView === 'tasks' && !task.archived" class="subtask-creation-form">
          <!-- Поле для ввода (показывается только при создании) -->
          <div v-if="showSubtaskForm" class="subtask-input-column" :class="{ editing: isSubtaskInputActive }">
            <div class="subtask-input-group">
              <div class="subtask-type-title">Название подзадачи</div>
              <input
                ref="subtaskInputRef"
                v-model="newSubtaskTitle"
                type="text"
                placeholder="Введите название подзадачи"
                :disabled="loading"
                @focus="isSubtaskInputActive = true"
                @blur="isSubtaskInputActive = false"
                @keyup.enter="addNewSubtask"
              >
            </div>
          </div>

          <!-- Кнопка (меняет текст) -->
          <div class="subtask-button-container">
            <ButtonMain
              v-if="!showSubtaskForm"
              variant="white"
              full-width
              height="40px"
              @click="openSubtaskForm"
            >
              Создать подзадачу
            </ButtonMain>
            
            <ButtonMain
              v-else
              variant="solid"
              full-width
              height="40px"
              :disabled="!newSubtaskTitle?.trim() || loading"
              @click="addNewSubtask"
            >
              Сохранить подзадачу
            </ButtonMain>
            
            <button
              v-if="showSubtaskForm"
              class="cancel-subtask-btn-text"
              @click="closeSubtaskForm"
              :disabled="loading"
            >
              Отмена
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue';
import { useNuxtApp } from '#imports';
import ButtonMain from '~/components/ui/ButtonMain.vue';
import Icon from '~/components/ui/Icon.vue';

const { $customFetch } = useNuxtApp();

const props = defineProps({
  task: {
    type: Object,
    required: true,
  },
  currentView: {
    type: String,
    default: 'tasks',
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits([
  'task-updated',
  'task-archived',
  'task-unarchived',
  'task-deleted',
  'subtask-added',
  'subtask-toggled',
  'subtask-deleted',
  'edit-task',
  'edit-subtask',
]);

const API_BASE = 'http://localhost:8000';
const newSubtaskTitle = ref('');
const showSubtaskForm = ref(false);
const isSubtaskInputActive = ref(false);
const subtaskInputRef = ref(null);

// Массив красивых цветов для тегов и приоритетов
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
];

// Вычисляемые свойства
const isOverdue = computed(() => {
  if (!props.task.deadline || props.task.is_done || props.task.archived) return false;
  return new Date(props.task.deadline) < new Date();
});

// Методы
const editTask = () => {
  emit('edit-task', props.task);
};

const editSubtask = (subtask) => {
  emit('edit-subtask', { taskId: props.task.id, subtask });
};

const openSubtaskForm = async () => {
  showSubtaskForm.value = true;
  newSubtaskTitle.value = '';
  
  // Фокус на поле ввода после отрисовки
  await nextTick();
  if (subtaskInputRef.value) {
    subtaskInputRef.value.focus();
  }
};

const closeSubtaskForm = () => {
  showSubtaskForm.value = false;
  newSubtaskTitle.value = '';
  isSubtaskInputActive.value = false;
};

const formatDate = (dateString) => {
  try {
    const date = new Date(dateString);
    const now = new Date();
    const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return 'сегодня';
    if (diffDays === 1) return 'вчера';
    if (diffDays < 7) return `${diffDays} д. назад`;

    return date.toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'short',
    });
  } catch {
    return dateString;
  }
};

const formatDeadline = (dateString) => {
  try {
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}.${month}.${year}`;
  } catch {
    return dateString;
  }
};

const toggleTaskDone = async () => {
  if (props.loading) return;

  if (props.task.archived) {
    return;
  }

  const isDone = props.task.is_done;
  const endpoint = isDone ? `${props.task.id}/undone` : `${props.task.id}/done`;

  try {
    const updatedTask = await $customFetch(`${API_BASE}/tasks/${endpoint}`, {
      method: 'PATCH',
      credentials: 'include',
    });

    emit('task-updated', updatedTask);
  } catch (err) {
    console.error('❌ Ошибка обновления задачи:', err);
  }
};

const archiveTask = async () => {
  if (props.loading) return;

  try {
    const updatedTask = await $customFetch(`${API_BASE}/tasks/${props.task.id}/archive`, {
      method: 'PATCH',
      credentials: 'include',
    });

    emit('task-archived', updatedTask);
  } catch (err) {
    console.error('❌ Ошибка архивирования задачи:', err);
  }
};

const unarchiveTask = async () => {
  if (props.loading) return;

  try {
    const updatedTask = await $customFetch(`${API_BASE}/tasks/${props.task.id}/unarchive`, {
      method: 'PATCH',
      credentials: 'include',
    });

    emit('task-unarchived', updatedTask);
  } catch (err) {
    console.error('❌ Ошибка восстановления задачи:', err);
  }
};

const deleteTask = async () => {
  if (props.loading) return;
  if (!confirm('Вы уверены, что хотите удалить эту задачу?')) return;

  try {
    await $customFetch(`${API_BASE}/tasks/${props.task.id}`, {
      method: 'DELETE',
      credentials: 'include',
    });

    emit('task-deleted', props.task.id);
  } catch (err) {
    console.error('❌ Ошибка удаления задачи:', err);
  }
};

const toggleSubtaskDone = async (subtaskId) => {
  if (props.loading) return;

  if (props.task.archived) {
    return;
  }

  const subtask = props.task.subtasks.find(s => s.id === subtaskId);
  if (!subtask) return;

  const newDoneStatus = !subtask.is_done;

  try {
    const updatedSubtask = await $customFetch(`${API_BASE}/subtasks/${subtaskId}`, {
      method: 'PATCH',
      body: { is_done: newDoneStatus },
      credentials: 'include',
    });

    emit('subtask-toggled', { taskId: props.task.id, subtask: updatedSubtask });
  } catch (err) {
    console.error('❌ Ошибка обновления подзадачи:', err);
  }
};

const addNewSubtask = async () => {
  if (!newSubtaskTitle.value?.trim() || props.loading) return;

  if (props.task?.archived) {
    return;
  }

  const subtaskData = {
    task_id: props.task.id,
    title: newSubtaskTitle.value.trim(),
    is_done: false,
  };

  try {
    const createdSubtask = await $customFetch(`${API_BASE}/subtasks/`, {
      method: 'POST',
      body: subtaskData,
      credentials: 'include',
    });

    newSubtaskTitle.value = '';
    showSubtaskForm.value = false;
    isSubtaskInputActive.value = false;
    emit('subtask-added', { taskId: props.task.id, subtask: createdSubtask });
  } catch (err) {
    console.error('❌ Ошибка создания подзадачи:', err);
  }
};

const deleteSubtask = async (subtaskId) => {
  if (props.loading) return;
  if (!confirm('Вы уверены, что хотите удалить эту подзадачу?')) return;

  if (props.task?.archived) {
    return;
  }

  try {
    await $customFetch(`${API_BASE}/subtasks/${subtaskId}`, {
      method: 'DELETE',
      credentials: 'include',
    });

    emit('subtask-deleted', { taskId: props.task.id, subtaskId });
  } catch (err) {
    console.error('❌ Ошибка удаления подзадачи:', err);
  }
};

// Функция для получения цвета для тега (на основе хеша названия тега)
const getTagColor = (tagName) => {
  if (!tagName) return '#6c757d';
  
  // Создаем простой хеш из строки для детерминированного выбора цвета
  let hash = 0;
  for (let i = 0; i < tagName.length; i++) {
    hash = tagName.charCodeAt(i) + ((hash << 5) - hash);
  }
  
  // Используем хеш для выбора цвета из палитры
  const index = Math.abs(hash) % colorPalette.length;
  return colorPalette[index];
};

// Функция для получения цвета приоритета (использует ту же палитру)
const getPriorityColor = (priority) => {
  if (!priority && priority !== 0) return '#6c757d';

  // Нормализуем приоритет к диапазону 0-1
  const normalizedPriority = Math.min(Math.max(priority, 0), 1);
  
  // Выбираем цвет из палитры на основе приоритета
  // Высокий приоритет - теплые цвета (оранжевый, красный)
  // Низкий приоритет - холодные цвета (синий, зеленый)
  if (normalizedPriority >= 0.8) return colorPalette[3]; // красный для высокого приоритета
  if (normalizedPriority >= 0.6) return colorPalette[2]; // оранжевый
  if (normalizedPriority >= 0.4) return colorPalette[9]; // лаймовый
  if (normalizedPriority >= 0.2) return colorPalette[0]; // синий
  return colorPalette[14]; // серый для очень низкого приоритета
};
</script>

<style scoped>
/* Обновленные стили для компонента TaskCard */
.task-card {
  width: 100%;
  max-width: 100%;
  padding: 20px;
  border: 1px solid #dee2e6;
  border-radius: 10px;
  background: white;
  transition: all 0.2s;
  box-sizing: border-box;
  margin-bottom: 12px;
  position: relative;
}

.task-top-bar {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  gap: 16px;
  /* Убрали border-bottom и padding-bottom */
}

.task-left-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.task-priority-badge {
  display: flex;
  align-items: center;
  gap: 8px;
}

.priority-color {
  width: 16px;
  height: 16px;
  border-radius: 3px;
  flex-shrink: 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.priority-value {
  font-size: 20px;
  font-weight: 400;
  color: #212529;
  line-height: 1;
  letter-spacing: 2%;
}

/* Стили для дедлайна в синем кружочке */
.deadline-container {
  margin-top: 4px;
}

.deadline-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 0px;
  background-color: white;
  border: 1px solid #0d6efd;
  border-radius: 20px;
  color: #0d6efd;
  font-size: 14px;
  font-weight: 500;
  line-height: 1;
  min-width: 100px;
  text-align: center;
  transition: all 0.2s;
  position: relative;
}

.deadline-badge.overdue {
  border-color: #dc3545;
  color: #dc3545;
  background-color: #fff5f5;
}

.deadline-text {
  letter-spacing: 0.5px;
  font-size: 12px;
}

.overdue-indicator {
  position: absolute;
  top: -6px;
  right: -6px;
  width: 16px;
  height: 16px;
  background-color: #dc3545;
  color: white;
  border-radius: 50%;
  font-size: 10px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.task-tag-badge {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex-shrink: 0;
}

.tag-circle {
  height: 38px;
  border-radius: 19px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 60px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0 12px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.tag-circle:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.tag-text {
  font-size: 12px;
  font-weight: 600;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Основной контент задачи */
.task-content {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  width: 100%;
}

.checkmark {
  position: relative;
  height: 20px;
  width: 20px;
  background-color: white;
  border: 1px solid #0d6efd;
  border-radius: 4px;
  flex-shrink: 0;
  transition: all 0.2s;
}

.subtask-checkbox-container {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  cursor: pointer;
  user-select: none;
  flex: 1;
}

.subtask-checkbox-container:hover .checkmark {
  background-color: #f0f7ff;
}

.subtask-checkbox:checked ~ .checkmark {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.checkmark:after {
  content: " ";
  position: absolute;
  display: none;
}

.subtask-checkbox:checked ~ .checkmark:after {
  display: block;
}

.subtask-done {
  color: #0d6efd !important;
  text-decoration: line-through;
}

/* Обновленные стили для контейнера подзадачи */
.subtask-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 8px 0;
  width: 100%;
  border-bottom: 1px solid #f0f0f0;
}

.subtask-item:last-child {
  border-bottom: none;
}

.subtask-title {
  font-size: 14px;
  color: #495057;
  word-break: break-word;
  transition: all 0.2s;
}

.checkmark:after {
  left: 5.7px;
  top: 1.2px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 1.5px 1.5px 0;
  transform: rotate(45deg);
}

.task-main {
  flex: 1;
  min-width: 0;
  width: 100%;
}

.task-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.task-title {
  margin: 0;
  font-size: 18px;
  color: #212529;
  font-weight: 600;
  line-height: 1.3;
  flex: 1;
  min-width: 0;
  word-break: break-word;
}

.task-title-done {
  text-decoration: line-through;
  color: #6c757d;
}

/* Бейджи статусов */
.badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  color: white;
  font-weight: 500;
  white-space: nowrap;
}

.badge-overdue {
  background: #dc3545;
  font-weight: bold;
}

.badge-archive {
  background: #6c757d;
}

.badge-done {
  background: #28a745;
}

.task-description {
  color: #495057;
  margin-bottom: 20px;
  font-size: 15px;
  line-height: 1.5;
  white-space: pre-line;
  word-break: break-word;
}

/* Подзадачи */
.subtasks {
  margin-bottom: 20px;
  width: 100%;
}

.subtasks-title {
  font-size: 16px;
  color: #212529;
  margin-bottom: 12px;
}

.subtasks-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.subtask-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 6px;
  width: 100%;
}

.subtask-checkbox {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.subtask-title {
  font-size: 14px;
  color: #495057;
  flex: 1;
  word-break: break-word;
}

.subtask-done {
  text-decoration: line-through;
  color: #6c757d;
}

/* Иконки действий для подзадачи */
.subtask-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.subtask-action-btn {
  width: 28px;
  height: 28px;
  background: none;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  padding: 0;
}

.subtask-action-btn.edit-btn {
  color: #0d6efd;
}

.subtask-action-btn.edit-btn:hover:not(:disabled) {
  background-color: rgba(13, 110, 253, 0.1);
}

.subtask-action-btn.delete-btn {
  color: #dc3545;
}

.subtask-action-btn.delete-btn:hover:not(:disabled) {
  background-color: rgba(220, 53, 69, 0.1);
}

.subtask-action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Добавляем новые стили для формы создания подзадачи (в стиле OnboardingForm) */
.subtask-creation-form {
  margin-bottom: 20px;
  width: 100%;
}

.subtask-input-column {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #D4D4D8;
  padding: 5px 0;
  margin-bottom: 16px;
  transition: border-color 0.3s ease;
}

.subtask-input-column.editing {
  border-bottom-color: #0d6efd;
}

.subtask-input-group {
  display: flex;
  flex-direction: column;
  flex: 1;
  justify-content: center;
  padding: 5px 0;
  width: 100%;
}

.subtask-type-title {
  color: #0d6efd;
  margin-bottom: 4px;
  font-size: 16px;
  font-weight: 500;
}

.subtask-input-group input {
  border: none;
  background: transparent;
  font-size: 15px;
  color: #111;
  display: flex;
  align-items: flex-end;
  width: 100%;
  font-family: inherit;
  line-height: 1.4;
  padding: 4px 0;
}

.subtask-input-group input:focus {
  outline: none;
}

.subtask-input-group input::placeholder {
  color: #999;
  opacity: 0.7;
}

.subtask-button-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.cancel-subtask-btn-text {
  background: none;
  border: none;
  color: #6c757d;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  padding: 8px 0;
  text-align: center;
  transition: color 0.2s;
}

.cancel-subtask-btn-text:hover:not(:disabled) {
  color: #495057;
}

.cancel-subtask-btn-text:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Адаптивность для компонента */
@media (max-width: 768px) {
  .task-card {
    padding: 16px;
  }

  .task-top-bar {
    gap: 12px;
  }

  .task-tag-badge {
    align-self: flex-start;
  }

  .task-content {
    flex-direction: column;
  }

  .task-header {
    gap: 8px;
  }

  .task-title {
    font-size: 16px;
  }

  .task-description {
    font-size: 14px;
  }

  .subtask-action-btn {
    width: 24px;
    height: 24px;
  }
}

@media (max-width: 480px) {
  .task-card {
    padding: 12px;
  }

  .task-header {
    align-items: flex-start;
    gap: 6px;
  }

  .badge {
    font-size: 11px;
    padding: 3px 8px;
  }

  .subtask-action-btn {
    width: 22px;
    height: 22px;
  }
}
</style>