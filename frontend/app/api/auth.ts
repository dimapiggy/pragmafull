import useCustomFetch from '~/api/useCustomFetch';
import type { NitroFetchOptions, NitroFetchRequest } from 'nitropack/types';
import type { UseFetchOptions } from 'nuxt/app';

import type { fetchUrlType } from '~/types';
import type { IUser } from '~/types/user';
import type { IAuthResponse } from '~/types/auth';

const baseURL = `${import.meta.env.VITE_HOST}${import.meta.env.VITE_HOST_AUTH}/auth/`;

function useApiFetch<T>(url: fetchUrlType, options?: UseFetchOptions<T>) {
  return useCustomFetch<T>(url, {
    baseURL,
    ...options,
  });
};

function useApi<T>(url: string, options?: NitroFetchOptions<NitroFetchRequest>) {
  return useNuxtApp().$customFetch<T>(url, {
    baseURL,
    ...options,
  });
};

export function getProfileData() {
  return useApi<IUser>('/me', {
    method: 'GET',
    credentials: 'include',
  });
}

export function postRegisterUser(body: any) {
  return useApi<IAuthResponse>('/register', {
    method: 'POST',
    body,
    credentials: 'include',
  });
}

export function postCheckUser(body: { initData: string }) {
  return useApi<IAuthResponse>('/check', {
    method: 'POST',
    body,
    credentials: 'include',
  });
}

export function postRefreshToken() {
  return useApi<IAuthResponse>('/refresh', {
    method: 'POST',
    credentials: 'include',
  });
}

export function postLogout() {
  return useApi<any>('/logout', {
    method: 'POST',
    credentials: 'include',
  });
}
