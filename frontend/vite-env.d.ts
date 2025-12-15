/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_HOST: string
  readonly VITE_HOST_AUTH: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
