export default defineNuxtRouteMiddleware(async (to, from) => {
    const isAuthenticated = useAuthStore().isLoggedIn
    if (isAuthenticated === false) {
      return navigateTo('/login')
    }
    await useAuthStore().updateUser()
  })