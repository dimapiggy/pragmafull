// https://nuxt.com/docs/api/configuration/nuxt-config
import svgLoader from 'vite-svg-loader';

export default defineNuxtConfig({
  modules: ['@pinia/nuxt', 'dayjs-nuxt', '@vueuse/nuxt', '@nuxt/eslint'],

  components: [
    {
      path: '~/components',
      pathPrefix: false,
    },
  ],
  devtools: { enabled: true },
  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no, interactive-widget=resizes-content, viewport-fit=cover',
      link: [],
      script: [
        {
          src: 'https://telegram.org/js/telegram-web-app.js?59',
          async: true,
          defer: true,
        },
      ],
    },
  },
  css: [
    '~/assets/styles/index.scss',
  ],
  router: {
    options: {
      scrollBehaviorType: 'smooth',
    },
  },
  build: {
    transpile: ['@vuepic/vue-datepicker'],
  },
  devServer: {
    host: '0.0.0.0', // важно для ngrok
  },
  compatibilityDate: '2025-07-15',
  nitro: {
    devServer: {
      watch: [],
    },
  },
  vite: {
    server: {
      allowedHosts: ['5ac70561ca5a.ngrok-free.app'],
    },
    plugins: [
      svgLoader({
        defaultImport: 'url',
      }),
    ],
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "~/assets/styles/vars.scss" as *;',
        },
      },
    },
  },
  postcss: {
    plugins: {
      cssnano: {
        preset: ['default', { cssDeclarationSorter: false }],
      },
    },
  },
  dayjs: {
    locales: ['ru'],
    defaultLocale: 'ru',
    plugins: ['customParseFormat'],
  },
  eslint: {
    config: {
      stylistic: true,
    },
  },
});
