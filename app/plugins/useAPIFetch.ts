
export default defineNuxtPlugin((nuxtApp) => {
    const authStore = useAuthStore()
  
    const api = $fetch.create({
      baseURL: 'http://localhost:8000',
      onRequest({ request, options, error }) {
        if (authStore.token) {
          // note that this relies on ofetch >= 1.4.0 - you may need to refresh your lockfile
          options.headers.set('Authorization', `Bearer ${authStore.token}`)
        }
      },
      async onResponseError({ response }) {
        if (response.status === 401) {
          await nuxtApp.runWithContext(() => navigateTo('/login'))
        }
      }
    })
  
    // Expose to useNuxtApp().$api
    return {
      provide: {
        api
      }
    }
  })
  