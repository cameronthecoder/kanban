
import { useLoadingStore } from "#build/imports"
export default defineNuxtPlugin((nuxtApp) => {
    const authStore = useAuthStore()
    const alerts = useAlertStore()
    const route = useRoute()
    const loadingStore = useLoadingStore()
  
    const api = $fetch.create({
      baseURL: 'https://sea-turtle-app-5uo5v.ondigitalocean.app/',
      onRequest({ request, options, error }) {
        loadingStore.setLoading(true)
        if (authStore.token) {
          // note that this relies on ofetch >= 1.4.0 - you may need to refresh your lockfile
          options.headers.set('Authorization', `Bearer ${authStore.token}`)
        }
      },
      async onResponse({ response }) {
        loadingStore.setLoading(false);
      },
      async onResponseError({ response }) {
        if (response.status === 401 && route.path !== '/login') {
          alerts.addAlert({
            type: 'error',
            message: 'You need to be logged in to access this page'
          })
          await nuxtApp.runWithContext(() => navigateTo('/login'))
        } else if (response.status === 500) {
          alerts.addAlert({
            type: 'error',
            message: 'An error occurred, please try again later'
          })
        } else if (response.status == 403) {
          alerts.addAlert({
            type: 'error',
            message: 'You do not have permission to access this page'
          })
        } else if (response.status == 401) {
          alerts.addAlert({
            type: 'error',
            message: 'Invalid credentials'
          })
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
  