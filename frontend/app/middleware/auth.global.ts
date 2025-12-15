export default defineNuxtRouteMiddleware(async (to) => {
  const authStore = useAuthStore();

  await authStore.initializeFromCookie();

  if (!authStore.isAuth) {
    const clientUser = to.query.user;
    const clientAuthDate = to.query.auth_date;
    const clientHash = to.query.hash;

    if (clientUser && clientAuthDate && clientHash) {
      const urlInitData = `query_id=${to.query.query_id || ''}&user=${clientUser}&auth_date=${clientAuthDate}&hash=${clientHash}`;
      authStore.setInitData(urlInitData);
      await authStore.autoCheckUser();
    }
  }

  if (!to.meta.layout && !authStore.isAuth) {
    return navigateTo('/');
  } else if (to.meta.layout && authStore.isAuth) {
    return navigateTo('/main-page');
  }
});
