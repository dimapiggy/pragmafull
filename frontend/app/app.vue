<script setup>
import { onMounted, ref } from 'vue';
import { useAuthStore } from '~/stores/auth';

const authStore = useAuthStore();

// Состояния для отображения
const validationStatus = ref('');
const validationResult = ref(null);
const isValid = ref(false);
const logs = ref([]);

// Функция для добавления логов
const addLog = (message, type = 'info') => {
  const timestamp = new Date().toLocaleTimeString();
  logs.value.push({ timestamp, message, type });
  console.log(`[${type.toUpperCase()}] ${message}`);
  
  if (logs.value.length > 20) {
    logs.value.shift();
  }
};

// Функция валидации initData на сервере
const validateInitData = async (initData) => {
  addLog('🔐 Начинаем валидацию initData на сервере...', 'info');
  validationStatus.value = 'validating';
  
  try {
    const response = await $fetch('http://localhost:8000/auth/debug/validate', {
      method: 'POST',
      body: { initData },
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    validationResult.value = response;
    
    if (response.validation?.is_valid) {
      addLog('✅ InitData валидна! Пользователь подтвержден Telegram', 'success');
      addLog(`👤 ID: ${response.validation.user?.id}`, 'info');
      addLog(`📅 Дата авторизации: ${new Date(response.validation.auth_date * 1000).toLocaleString()}`, 'info');
      validationStatus.value = 'valid';
      isValid.value = true;
      return true;
    } else {
      addLog('❌ InitData невалидна!', 'error');
      addLog(`Причина: ${JSON.stringify(response)}`, 'error');
      validationStatus.value = 'invalid';
      isValid.value = false;
      return false;
    }
  } catch (error) {
    addLog(`❌ Ошибка валидации: ${error.message}`, 'error');
    
    // Если endpoint не существует, пробуем базовый check
    if (error.statusCode === 404) {
      addLog('⚠️ Endpoint валидации не найден, пробуем стандартную проверку...', 'warning');
      return await tryStandardAuth(initData);
    }
    
    validationStatus.value = 'error';
    isValid.value = false;
    return false;
  }
};

// Стандартная проверка авторизации (если endpoint валидации не реализован)
const tryStandardAuth = async (initData) => {
  try {
    authStore.setInitData(initData);
    const result = await authStore.autoCheckUser();
    
    if (result) {
      addLog('✅ Авторизация прошла успешно (через стандартный check)', 'success');
      validationStatus.value = 'auth_success';
      isValid.value = true;
      return true;
    } else {
      addLog('ℹ️ Пользователь не зарегистрирован', 'info');
      validationStatus.value = 'not_registered';
      isValid.value = false;
      return false;
    }
  } catch (error) {
    addLog(`❌ Ошибка стандартной авторизации: ${error.message}`, 'error');
    validationStatus.value = 'auth_error';
    isValid.value = false;
    return false;
  }
};

// Проверка Telegram Web App
const checkTelegramWebApp = () => {
  addLog('📱 Проверяем Telegram Web App...', 'info');
  
  if (!window.Telegram) {
    addLog('❌ window.Telegram не найден', 'error');
    return null;
  }
  
  if (!window.Telegram.WebApp) {
    addLog('❌ window.Telegram.WebApp не найден', 'error');
    return null;
  }
  
  const tg = window.Telegram.WebApp;
  const initData = tg.initData;
  
  if (!initData) {
    addLog('⚠️ Telegram Web App найден, но initData пустая', 'warning');
    return null;
  }
  
  addLog(`✅ Telegram Web App найден: v${tg.version} (${tg.platform})`, 'success');
  addLog(`🔐 InitData получена: ${initData.length} символов`, 'info');
  
  if (initData.length > 100) {
    addLog(`Превью: ${initData.substring(0, 100)}...`, 'debug');
  }
  
  return initData;
};

// Основная функция инициализации
const initializeApp = async () => {
  addLog('🚀 Инициализация приложения...', 'info');
  
  // 1. Проверяем Telegram Web App
  const initData = checkTelegramWebApp();
  
  if (!initData) {
    addLog('ℹ️ Telegram Web App не предоставил initData', 'info');
    addLog('💡 Откройте приложение через inline-кнопку в Telegram', 'info');
    validationStatus.value = 'no_initdata';
    return;
  }
  
  // 2. Валидируем initData на сервере
  const isValid = await validateInitData(initData);
  
  if (isValid) {
    addLog('🎉 Валидация пройдена! Приложение готово к работе.', 'success');
    
    // Если пользователь уже авторизован через store - всё ок
    // Если нет - autoCheckUser уже был вызван в tryStandardAuth
  } else {
    addLog('⚠️ Проблемы с валидацией или авторизацией', 'warning');
    
    // Показываем сообщение пользователю
    if (validationStatus.value === 'not_registered') {
      addLog('👤 Пожалуйста, пройдите регистрацию', 'info');
    } else if (validationStatus.value === 'invalid') {
      addLog('🔒 Проблема с безопасностью: невалидные данные Telegram', 'error');
    }
  }
};

onMounted(() => {
  addLog('🔄 App.vue загружен', 'info');
  
  // Запускаем инициализацию с задержкой, чтобы Telegram SDK успел загрузиться
  setTimeout(() => {
    initializeApp();
  }, 300);
});
</script>

<template>
  <div>
    <!--
    <div v-if="validationStatus" class="validation-panel">
      <div class="panel-header">
        <h3>🔐 Валидация Telegram Web App</h3>
        <span :class="{
          'status-badge valid': validationStatus === 'valid' || validationStatus === 'auth_success',
          'status-badge invalid': validationStatus === 'invalid' || validationStatus === 'error',
          'status-badge warning': validationStatus === 'not_registered' || validationStatus === 'no_initdata',
          'status-badge loading': validationStatus === 'validating'
        }">
          {{
            validationStatus === 'valid' || validationStatus === 'auth_success' ? '✅ ВАЛИДНО' :
            validationStatus === 'invalid' ? '❌ НЕВАЛИДНО' :
            validationStatus === 'not_registered' ? '👤 НЕ ЗАРЕГИСТРИРОВАН' :
            validationStatus === 'no_initdata' ? '📱 НЕТ ДАННЫХ' :
            validationStatus === 'validating' ? '🔄 ПРОВЕРКА...' :
            '❓ ОШИБКА'
          }}
        </span>
      </div>
      
      <div v-if="validationResult" class="validation-details">
        <h4>Результат валидации:</h4>
        <div class="details-grid">
          <div><strong>Длина данных:</strong> {{ validationResult.raw_length }} символов</div>
          <div><strong>Хэш присутствует:</strong> {{ validationResult.has_hash ? '✅ Да' : '❌ Нет' }}</div>
          <div><strong>Данные пользователя:</strong> {{ validationResult.has_user ? '✅ Да' : '❌ Нет' }}</div>
          <div><strong>Дата авторизации:</strong> {{ validationResult.has_auth_date ? '✅ Да' : '❌ Нет' }}</div>
        </div>
        
        <div v-if="validationResult.validation" class="validation-result">
          <div><strong>Валидность:</strong> {{ validationResult.validation.is_valid ? '✅ Да' : '❌ Нет' }}</div>
          
          <div v-if="validationResult.validation.user" class="user-data">
            <h5>Данные пользователя:</h5>
            <pre>{{ validationResult.validation.user }}</pre>
          </div>
        </div>
      </div>
      
      <div class="logs-section">
        <h4>📝 Логи валидации:</h4>
        <div class="logs-container">
          <div v-for="(log, index) in logs" :key="index" :class="['log-entry', log.type]">
            <span class="log-time">{{ log.timestamp }}</span>
            <span class="log-message">{{ log.message }}</span>
          </div>
        </div>
      </div>
      
      <div class="actions">
        <button @click="initializeApp" class="retry-btn">
          🔄 Повторить проверку
        </button>
        
        <a v-if="validationStatus === 'not_registered'" href="/auth" class="register-btn">
          📝 Перейти к регистрации
        </a>
      </div>
    </div>
    
    Основное приложение
    -->
    <AppHeader />
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<style scoped>
.validation-panel {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: white;
  border-bottom: 2px solid #e0e0e0;
  padding: 20px;
  z-index: 1000;
  max-height: 70vh;
  overflow-y: auto;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.panel-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.valid {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.status-badge.invalid {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.status-badge.warning {
  background: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

.status-badge.loading {
  background: #cce5ff;
  color: #004085;
  border: 1px solid #b8daff;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

.validation-details {
  margin: 20px 0;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #007bff;
}

.validation-details h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 16px;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
  margin-bottom: 15px;
  font-size: 14px;
}

.details-grid div {
  display: flex;
  gap: 8px;
  align-items: center;
}

.validation-result {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #ddd;
}

.user-data {
  margin-top: 10px;
  padding: 10px;
  background: white;
  border-radius: 4px;
  border: 1px solid #eee;
}

.user-data pre {
  margin: 10px 0 0 0;
  font-size: 12px;
  overflow: auto;
  max-height: 150px;
}

.logs-section {
  margin: 20px 0;
}

.logs-section h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #666;
}

.logs-container {
  max-height: 200px;
  overflow-y: auto;
  background: #1a1a1a;
  color: #f8f9fa;
  padding: 10px;
  border-radius: 6px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 12px;
}

.log-entry {
  padding: 4px 0;
  border-bottom: 1px solid #333;
  display: flex;
  gap: 15px;
}

.log-entry:last-child {
  border-bottom: none;
}

.log-time {
  color: #6c757d;
  min-width: 85px;
}

.log-entry.info .log-message {
  color: #17a2b8;
}

.log-entry.success .log-message {
  color: #28a745;
  font-weight: 500;
}

.log-entry.error .log-message {
  color: #dc3545;
  font-weight: 500;
}

.log-entry.warning .log-message {
  color: #ffc107;
}

.log-entry.debug .log-message {
  color: #6c757d;
  font-style: italic;
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.retry-btn {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}

.retry-btn:hover {
  background: #0056b3;
}

.register-btn {
  padding: 8px 16px;
  background: #28a745;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 14px;
  transition: background 0.2s;
}

.register-btn:hover {
  background: #218838;
}

/* Адаптивность */
@media (max-width: 768px) {
  .validation-panel {
    padding: 15px;
    max-height: 80vh;
  }
  
  .details-grid {
    grid-template-columns: 1fr;
  }
  
  .panel-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .actions {
    flex-direction: column;
  }
  
  .retry-btn,
  .register-btn {
    width: 100%;
    text-align: center;
  }
}
</style>