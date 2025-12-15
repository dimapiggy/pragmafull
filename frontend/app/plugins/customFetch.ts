import { appendResponseHeader } from 'h3';

import type { IAuthResponse } from '~/types/auth';

export default defineNuxtPlugin((nuxtApp) => {
  const authStore = useAuthStore();
  const { authToken } = storeToRefs(authStore);

  const $customFetch = $fetch.create({
    retryStatusCodes: [401],
    retry: 1,

    async onRequest({ request, options }) {
      options.query = options.query || {};
      console.log('⚡ customFetch request:', request);
      // options.query = prepareFilters(options.query);

      const authToken = useCookie('ACCESS_TOKEN');
      if (authToken.value) {
        options.headers = options.headers || {};
        options.headers.set('Authorization', `Bearer ${authToken.value}`);
      }
    },

    onResponse: async ({ response, request, options }) => {
      console.log('⚡ customFetch request:', request, {
        headers: options.headers,
        query: options.query,
        authToken: authToken.value,
      });

      if (response.status === 401 && authStore.isAuth) {
        console.log('401 detected, attempting token refresh...');
        await nuxtApp.runWithContext(async () => {
          try {
            const newToken = await refresh();
            authToken.value = newToken;

            options.headers.set('Authorization', `Bearer ${authToken.value}`);
          } catch (error) {
            authStore.logout();
            options.retry = false;
            console.error('Token refresh failed:', error);
          }
        });
      }
    },

    onResponseError({ response, request, options }) {},
  });

  let refreshTokenPromise: Promise<string | null> | null = null;

  async function refresh() {
    console.log('Refresh called');
    if (!refreshTokenPromise) {
      refreshTokenPromise = (async () => {
        try {
          const refresh = useCookie('REFRESH_TOKEN');

          const data = await $fetch<IAuthResponse>(`${import.meta.env.VITE_HOST}${import.meta.env.VITE_HOST_AUTH}/auth/refresh`, {
            method: 'POST',
            credentials: 'include',
            onResponse: async ({ response }) => {
              if (import.meta.server && response.headers.get('set-cookie')) {
                await nuxtApp.runWithContext(async () => {
                  const cookieHeader = response.headers.get('set-cookie');
                  const event = useRequestEvent();
                  if (event) appendResponseHeader(event, 'set-cookie', cookieHeader);
                });
              }
            },
          });

          return data.access_token;
        } catch (error) {
          console.dir('Token refresh failed:', error);
          if (error?.statusCode === 401 && error?.data?.detail === 'Token has expired. Please log in again.') {
            await nuxtApp.runWithContext(async () => {
              authStore.logout();
            });
          }
          throw error;
        } finally {
          refreshTokenPromise = null;
        }
      })();
    }

    return refreshTokenPromise;
  }

  // Expose to useNuxtApp().$customFetch
  return {
    provide: {
      customFetch: $customFetch,
    },
  };
});
