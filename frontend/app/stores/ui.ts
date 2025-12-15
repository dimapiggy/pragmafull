export const useUIStore = defineStore('ui', () => {
  const loading = ref(false);

  return {
    loading,
  };
});
