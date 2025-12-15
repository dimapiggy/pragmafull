<template>
  <div>
    <!-- Шапка (всегда видна) -->
    <div class="header">
      <div class="header-content">
        <!-- Левая часть: дата и день недели -->
        <div class="date-info">
          <div class="day-of-week">{{ currentDayOfWeek }}</div>
          <span class="date-dot"></span>
          <div class="current-date">{{ currentDate }}</div>
        </div>

        <!-- Правая часть: навигация -->
        <div class="header-right">
          <div class="nav-buttons">
            <button 
              class="nav-btn" 
              :class="{ active: !showTaskForm }"
              @click="goToTasks"
            >
              <Icon icon="home" />
            </button>
            <button 
              class="nav-btn" 
              @click="goToSettings" 
              title="Скоро будет доступно"
            >
              <Icon icon="settings" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Переключение задач/архива и кнопка создания (видно только в режиме задач) -->
    <div v-if="!showTaskForm" class="view-action-container">
      <div class="view-action-content">
        <!-- Левая часть: переключатель задач/архива -->
        <div class="view-switcher-text">
          <button 
            class="view-switcher-btn" 
            :class="{ active: currentView === 'tasks' }"
            @click="switchView('tasks')"
          >
            Задачи
          </button>

          <button
            class="view-switcher-btn"
            :class="{ active: currentView === 'archive' }"
            @click="switchView('archive')"
          >
            Архив
          </button>
        </div>

        <!-- Кнопка создания задачи -->
        <button 
          class="create-task-plus" 
          @click="openTaskForm()"
          title="Создать новую задачу"
          aria-label="Создать задачу"
        >
          +
        </button>
      </div>
    </div>

    <!-- Контент -->
    <div class="content">
      <!-- Если показываем форму создания/редактирования -->
      <div v-if="showTaskForm" class="task-form-wrapper">
        <TaskForm
          :task="taskToEdit"
          :loading="formLoading"
          @submit="handleFormSubmit"
          @close="closeTaskForm"
        />
      </div>

      <!-- Если показываем задачи/архив -->
      <div v-else>
        <!-- Если авторизован -->
        <div v-if="user">
          <!-- Загрузка -->
          <div v-if="loading" class="loading">
            <div class="loading-icon">⏳</div>
            Загрузка...
          </div>

          <!-- Список задач -->
          <div v-else>
            <!-- Пустые состояния -->
            <div v-if="currentView === 'tasks' && visibleTasks.length === 0" class="empty-state">
              <div class="empty-icon">📋</div>
              <h3 class="empty-title">Нет задач</h3>
              <p>Создайте первую задачу, нажав "+" в правом верхнем углу</p>
              <button class="create-first-btn" @click="openTaskForm()">
                Создать первую задачу
              </button>
            </div>

            <div v-if="currentView === 'archive' && visibleTasks.length === 0" class="empty-state">
              <div class="empty-icon">📁</div>
              <h3 class="empty-title">Архив пуст</h3>
              <p>Здесь будут отображаться завершённые задачи</p>
            </div>

            <!-- Список задач -->
            <div v-if="visibleTasks.length > 0" class="tasks-list">
              <TaskCard
                v-for="task in visibleTasks"
                :key="task.id"
                :task="task"
                :current-view="currentView"
                :loading="loading"
                @task-updated="updateTask"
                @task-archived="updateTask"
                @task-unarchived="updateTask"
                @task-deleted="removeTask"
                @subtask-added="addSubtaskToTask"
                @subtask-toggled="updateSubtaskInTask"
                @subtask-deleted="removeSubtaskFromTask"
                @edit-task="editTask"
              />
            </div>
          </div>
        </div>

        <!-- Если не авторизован -->
        <div v-else class="unauthorized">
          <h3>Не авторизован</h3>
          <p>Пожалуйста, войдите в систему</p>
          <button class="load-user-btn" @click="loadUser">Загрузить пользователя</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import TaskCard from '~/components/ui/TaskCard.vue';
import TaskForm from '~/components/ui/TaskForm.vue';

const { $customFetch } = useNuxtApp();

// Базовые URL
const API_BASE = 'http://localhost:8000';

// Данные
const user = ref(null);
const tasks = ref([]);
const loading = ref(false);
const formLoading = ref(false);
const error = ref('');
const currentView = ref('tasks');
const showTaskForm = ref(false);
const taskToEdit = ref(null);

// Вычисляемые свойства
const activeTasks = computed(() =>
  tasks.value.filter(task => !task.is_done && !task.archived),
);

const completedTasks = computed(() =>
  tasks.value.filter(task => task.is_done && !task.archived),
);

const archivedTasks = computed(() =>
  tasks.value.filter(task => task.archived),
);

const visibleTasks = computed(() => {
  if (currentView.value === 'archive') {
    return archivedTasks.value;
  } else {
    return tasks.value.filter(task => !task.archived);
  }
});

// Вспомогательные функции для даты
const currentDayOfWeek = computed(() => {
  const days = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
  return days[new Date().getDay()];
});

const currentDate = computed(() => {
  const now = new Date();
  const day = String(now.getDate()).padStart(2, '0');
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const year = now.getFullYear();
  return `${day}.${month}.${year}`;
});

// Методы для навигации
const goToTasks = () => {
  showTaskForm.value = false;
  taskToEdit.value = null;
};

const goToSettings = () => {
  alert('Страница настроек будет добавлена позже');
};

// Переключение вида
const switchView = (view) => {
  currentView.value = view;
};

// Методы для формы
const openTaskForm = (task = null) => {
  taskToEdit.value = task;
  showTaskForm.value = true;
};

const closeTaskForm = () => {
  showTaskForm.value = false;
  taskToEdit.value = null;
};

// Обработка отправки формы
const handleFormSubmit = async ({ data, isEditing, taskId }) => {
  formLoading.value = true;
  error.value = '';

  try {
    if (isEditing && taskId) {
      // Редактирование существующей задачи
      console.log('✏️ Редактируем задачу:', data);
      
      // Обновляем базовые данные задачи
      const updatedTask = await $customFetch(`${API_BASE}/tasks/${taskId}`, {
        method: 'PUT',
        body: {
          title: data.title.trim(),
          description: data.description || null,
          deadline: data.deadline ? new Date(data.deadline).toISOString() : null
        },
        credentials: 'include',
      });

      // Обновляем метрики
      if (data.metrics) {
        await $customFetch(`${API_BASE}/task-metrics/${taskId}`, {
          method: 'PUT',
          body: data.metrics,
          credentials: 'include',
        });
        
        // Обновляем задачу с новым приоритетом
        const metricsResponse = await $customFetch(`${API_BASE}/task-metrics/${taskId}`, {
          method: 'GET',
          credentials: 'include',
        });
        
        updatedTask.priority = metricsResponse.task_priority;
        updatedTask.metrics = metricsResponse.metrics;
      }

      // Обновляем задачу в списке
      const index = tasks.value.findIndex(t => t.id === taskId);
      if (index !== -1) {
        tasks.value[index] = updatedTask;
      }
      
    } else {
      // Создание новой задачи
      console.log('➕ Создаем задачу:', data);

      // Создаем задачу
      const createdTask = await $customFetch(`${API_BASE}/tasks/`, {
        method: 'POST',
        body: {
          title: data.title.trim(),
          description: data.description || null,
          deadline: data.deadline ? new Date(data.deadline).toISOString() : null
        },
        credentials: 'include',
      });

      // Добавляем метрики
      if (data.metrics) {
        const metricsResponse = await $customFetch(`${API_BASE}/task-metrics/${createdTask.id}`, {
          method: 'PUT',
          body: data.metrics,
          credentials: 'include',
        });
        
        createdTask.priority = metricsResponse.task_priority;
        createdTask.metrics = metricsResponse.metrics;
      }

      // Добавляем в начало списка
      tasks.value.unshift(createdTask);
    }

    // Закрываем форму
    closeTaskForm();
    
  } catch (err) {
    console.error('❌ Ошибка сохранения задачи:', err);
    error.value = `Ошибка сохранения задачи: ${err.message}`;
  } finally {
    formLoading.value = false;
  }
};

// Редактирование задачи
const editTask = (task) => {
  openTaskForm(task);
};

// Основные методы
const loadUser = async () => {
  try {
    console.log('🔍 Загружаем пользователя...');
    user.value = await $customFetch(`${API_BASE}/auth/me`, {
      method: 'GET',
      credentials: 'include',
    });
    console.log('✅ Пользователь загружен:', user.value);
  } catch (err) {
    console.error('❌ Ошибка загрузки пользователя:', err);
    error.value = 'Ошибка загрузки пользователя';
  }
};

const loadTasks = async () => {
  if (!user.value) return;

  loading.value = true;
  error.value = '';

  try {
    console.log('📡 Загружаем задачи...');
    const response = await $customFetch(`${API_BASE}/tasks/`, {
      method: 'GET',
      credentials: 'include',
    });

    if (Array.isArray(response)) {
      tasks.value = response;
    } else {
      console.warn('⚠️ Ответ не является массивом:', response);
      tasks.value = [];
    }
  } catch (err) {
    console.error('❌ Ошибка загрузки задач:', err);
    error.value = `Ошибка загрузки задач: ${err.message}`;
  } finally {
    loading.value = false;
  }
};

// Методы для обработки событий от TaskCard
const updateTask = (updatedTask) => {
  const index = tasks.value.findIndex(t => t.id === updatedTask.id);
  if (index !== -1) {
    tasks.value[index] = updatedTask;
  }
};

const removeTask = (taskId) => {
  tasks.value = tasks.value.filter(t => t.id !== taskId);
};

const addSubtaskToTask = ({ taskId, subtask }) => {
  const taskIndex = tasks.value.findIndex(t => t.id === taskId);
  if (taskIndex !== -1) {
    if (!tasks.value[taskIndex].subtasks) {
      tasks.value[taskIndex].subtasks = [];
    }
    tasks.value[taskIndex].subtasks.push(subtask);
  }
};

const updateSubtaskInTask = ({ taskId, subtask }) => {
  const taskIndex = tasks.value.findIndex(t => t.id === taskId);
  if (taskIndex !== -1) {
    const subtaskIndex = tasks.value[taskIndex].subtasks.findIndex(s => s.id === subtask.id);
    if (subtaskIndex !== -1) {
      tasks.value[taskIndex].subtasks[subtaskIndex] = subtask;
    }
  }
};

const removeSubtaskFromTask = ({ taskId, subtaskId }) => {
  const taskIndex = tasks.value.findIndex(t => t.id === taskId);
  if (taskIndex !== -1) {
    tasks.value[taskIndex].subtasks = tasks.value[taskIndex].subtasks.filter(s => s.id !== subtaskId);
  }
};

// Инициализация
onMounted(async () => {
  console.log('🚀 Инициализация страницы...');
  await loadUser();
  if (user.value) {
    await loadTasks();
  }
});
</script>

<style scoped>
/* Стили для страницы формы */
.task-form-wrapper {
  width: 100%;
}

/* Шапка */
.header {
  padding: 12px 20px;
  border-bottom: 1px solid #dee2e6;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 800px;
  margin: 0 auto;
}

.date-info {
  display: flex;
  gap: 8px;
}

.day-of-week {
  font-size: 16px;
  color: #212529;
  font-weight: 400;
}

.current-date {
  font-size: 16px;
  color: #212529;
  font-weight: 400;
}

.header-right {
  display: flex;
  align-items: center;
}

.nav-buttons {
  display: flex;
  gap: 8px;
  background: #e9ecef;
  padding: 4px;
  border-radius: 8px;
}

.nav-btn {
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.nav-btn.active {
  color: white;
}

.nav-btn:not(.active) {
  background: transparent;
  color: #495057;
}

.nav-btn:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
}

.view-action-container {
  padding: 10px 16px;
  border-bottom: 1px solid #e9ecef;
}

.view-action-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 800px;
  margin: 0 auto;
}

/* Переключатель в виде текста */
.view-switcher-text {
  display: flex;
  align-items: center;
  gap: 12px;
}

.view-switcher-btn {
  background: none;
  border: none;
  padding: 8px 4px;
  font-size: 24px;
  font-weight: 700;
  color: #6c757d;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
  position: relative;
}

.view-switcher-btn:hover {
  color: #495057;
}

.view-switcher-btn.active {
  color: #0d6efd;
}

.date-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  background-color: #0d6efd;
  border-radius: 50%;
  align-self: center;
}

.view-counter {
  background: #e9ecef;
  color: #6c757d;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 20px;
  text-align: center;
}

.view-switcher-btn.active .view-counter {
  background: #0d6efd;
  color: white;
}

.view-switcher-divider {
  color: #dee2e6;
  font-size: 14px;
}

.create-task-plus {
  background: none;
  border: none;
  color: #0d6efd;
  font-size: 40px;
  cursor: pointer;
  font-weight: 200;
  padding: 4px 8px;
  transition: all 0.2s;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 40px;
  min-height: 40px;
}

.create-task-plus:hover {
  color: #0b5ed7;
  transform: scale(1.1);
}

.create-task-plus:active {
  transform: scale(0.95);
}

.content {
  max-width: 800px;
  margin: 0 0;
  padding: 0px 12px 12px;
  width: 100%;
  box-sizing: border-box;
}

.content > div {
  width: 100%;
}

/* Статус бар */
.status-bar {
  margin-bottom: 20px;
  padding: 10px;
  background: #e7f3ff;
  border-radius: 6px;
  font-size: 14px;
}

.tasks-count {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
}

/* Ошибки */
.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 12px 16px;
  border-radius: 4px;
  margin-bottom: 20px;
  border: 1px solid #f5c6cb;
  position: relative;
}

.close-error {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #721c24;
  cursor: pointer;
  font-size: 18px;
  padding: 0;
  width: 24px;
  height: 24px;
}

/* Загрузка */
.loading {
  text-align: center;
  padding: 20px;
  color: #6c757d;
}

.loading-icon {
  margin-bottom: 10px;
  font-size: 24px;
}

/* Пустой список */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #adb5bd;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.empty-title {
  color: #6c757d;
  margin-bottom: 10px;
}

.create-first-btn {
  margin-top: 20px;
  padding: 10px 24px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
}

.create-first-btn:hover {
  background: #218838;
}

/* Список задач */
.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}

/* Статистика */
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin-top: 30px;
}

.stat-card {
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  border-left: 4px solid;
}

.stat-total {
  background: #e3f2fd;
  border-left-color: #0d6efd;
}

.stat-active {
  background: #d1e7dd;
  border-left-color: #198754;
}

.stat-completed {
  background: #fff3cd;
  border-left-color: #ffc107;
}

.stat-archived {
  background: #e2e3e5;
  border-left-color: #6c757d;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
}

.stat-total .stat-number {
  color: #0d6efd;
}

.stat-active .stat-number {
  color: #198754;
}

.stat-completed .stat-number {
  color: #ffc107;
}

.stat-archived .stat-number {
  color: #6c757d;
}

.stat-label {
  font-size: 12px;
  color: #495057;
  margin-top: 4px;
}

/* Не авторизован */
.unauthorized {
  text-align: center;
  padding: 60px 20px;
}

.unauthorized h3 {
  color: #212529;
  margin-bottom: 8px;
}

.unauthorized p {
  color: #6c757d;
  margin-bottom: 20px;
}

.load-user-btn {
  padding: 10px 20px;
  background: #0d6efd;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.load-user-btn:hover {
  opacity: 0.9;
}
</style>
