import type { UseFetchOptions } from 'nuxt/app';
import type { fetchUrlType } from '~/types';

export default function useCustomFetch<T>(url: fetchUrlType, options?: UseFetchOptions<T>) {
  return useFetch(url, {
    ...options,
    $fetch: useNuxtApp().$customFetch as typeof $fetch,
  });
};
