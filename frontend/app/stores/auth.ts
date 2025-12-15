import { getProfileData, postCheckUser, postRegisterUser } from '~/api/auth';
import type { IUser } from '~/types/user';
import type { IAuthResponse } from '~/types/auth';

export const useAuthStore = defineStore('auth', () => {
  const authToken = useCookie('ACCESS_TOKEN');
  const refreshToken = useCookie('REFRESH_TOKEN');
  const user = ref<IUser | null>(null);
  const initData = ref('');
  const loading = ref(false);
  const error = ref<string | null>(null);

  // isAuth = есть токен И данные пользователя
  const isAuth = computed(() => !!authToken.value && !!user.value);

  const setInitData = (data: string) => {
    initData.value = data;
  };

  async function initializeFromCookie() {
    console.log('initializeFromCookie called', {
      hasToken: !!authToken.value,
      hasUser: !!user.value,
    });

    if (user.value) return;

    // Есть access_token — загружаем профиль
    if (authToken.value && !user.value) {
      try {
        console.log('Loading profile data...');
        await loadProfileData();
        console.log('Profile loaded from cookie', {
          user: user.value,
          isAuth: isAuth.value,
        });
      } catch (err) {
        console.log('Failed to load profile from cookie, clearing tokens');
        clearTokens();
      }

      // Нет access_token, но есть refresh_token — пробуем обновить токен
    } else {
      const refreshToken = useCookie('REFRESH_TOKEN').value;
      if (refreshToken) {
        console.log('No access token, but refresh token exists — refreshing...');
        try {
          const newToken = await refresh(); // твоя функция из customFetch
          authToken.value = newToken;
          await loadProfileData();
          console.log('Profile loaded after refresh', {
            user: user.value,
            isAuth: isAuth.value,
          });
        } catch (err) {
          console.log('Refresh failed, logging out');
          clearTokens();
        }
      } else {
        console.log('No token or already has user');
      }
    }
  }

  async function loadProfileData() {
    try {
      console.log('Calling getProfileData...');
      const userData = await getProfileData();
      user.value = userData;
      console.log('User data set:', user.value);
    } catch (err: any) {
      error.value = err.message;
      throw err;
    }
  }

  async function autoCheckUser(): Promise<boolean> {
    if (!initData.value) return false;

    loading.value = true;
    try {
      console.log('autoCheckUser: calling postCheckUser...');
      const res: IAuthResponse = await postCheckUser({ initData: initData.value });

      // Детальный лог всего ответа
      console.log('autoCheckUser: full response', JSON.stringify(res, null, 2));
      console.log('autoCheckUser: response keys', Object.keys(res));

      if (res.exists) {
      // Проверяем разные возможные варианты названий токенов
        const accessToken = res.access_token || res.accessToken || (res as any).access;
        const refreshToken = res.refresh_token || res.refreshToken || (res as any).refresh;

        console.log('autoCheckUser: found tokens', {
          accessToken: !!accessToken,
          refreshToken: !!refreshToken,
        });

        if (accessToken) {
          authToken.value = accessToken;
          console.log('autoCheckUser: access token set');
        }
        if (refreshToken) {
          refreshToken.value = refreshToken;
          console.log('autoCheckUser: refresh token set');
        }

        await loadProfileData();
        console.log('autoCheckUser: completed', { isAuth: isAuth.value });
        return true;
      } else {
        user.value = res.prefill
          ? {
              id: 0,
            telegram_id: res.prefill.telegram_id || 0,
            username: res.prefill.username || '',
            first_name: res.prefill.fullname?.split(' ')[0] || '',
            last_name: res.prefill.fullname?.split(' ')[1] || '',
            fullname: res.prefill.fullname || '',
            task_creation_type: res.prefill.task_creation_type || 'quick',
            notifications_enabled: res.prefill.notifications_enabled || false,
            notification_time: res.prefill.notification_time || '09:00:00',
            assistantStyle: res.prefill.assistantStyle || 'restrained',
          } as IUser
          : null;

        return false;
      }
    } catch (e: any) {
      error.value = e?.data?.detail || 'Ошибка проверки пользователя';
      user.value = null;
      return false;
    } finally {
      loading.value = false;
    }
  }

  async function registerUser(form: Partial<IUser>): Promise<IAuthResponse> {
    if (!initData.value) throw new Error('No initData available');

    loading.value = true;
    try {
      const res: IAuthResponse = await postRegisterUser({
        ...form,
        initData: initData.value,
      });

      if (res.user) {
        // Регистрация успешна - выдаем куки и устанавливаем пользователя
        user.value = res.user;
        if (res.access_token) authToken.value = res.access_token;
        if (res.refresh_token) refreshToken.value = res.refresh_token;
      }
      return res;
    } catch (e: any) {
      error.value = e?.data?.detail || 'Ошибка регистрации';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  const logout = () => {
    clearTokens();
  };

  const clearTokens = () => {
    authToken.value = null;
    initData.value = '';
    user.value = null;
    error.value = null;
  };

  return {
    authToken,
    refreshToken,
    user,
    isAuth,
    loading,
    error,
    initData,
    loadProfileData,
    autoCheckUser,
    registerUser,
    logout,
    setInitData,
    clearTokens,
    initializeFromCookie,
  };
});
