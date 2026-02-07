export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],
  compatibilityDate: '2025-02-06',
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:35000'
    }
  }
})
