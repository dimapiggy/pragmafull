<script setup lang="ts">
import type { NuxtError } from '#app';

const props = defineProps({
  error: Object as () => NuxtError,
});

useHead({
  title: () => props.error?.statusCode === 404 ? 'Страница не найдена' : 'Технические работы',
  meta: [
    { name: 'description', content: 'Возникла ошибка при работе сайта.' },
  ],
});

onMounted(() => console.log(props.error));
</script>

<template>
  <NuxtLayout name="not-auth">
    <div>
      <template v-if="error?.statusCode === 404">
        <div>
          404
        </div>

        <div>
          Страница не найдена
        </div>

        <NuxtLink to="/">
          Вернуться в систему
        </NuxtLink>
      </template>

      <template v-else>
        Ошибка в работе сайта
      </template>

      <pre v-show="false" style="white-space: break-spaces;">
        {{ error }}
      </pre>
    </div>
  </NuxtLayout>
</template>
