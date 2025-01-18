import { defineNuxtPlugin } from '#app'
import VueDebounce, { vueDebounce } from 'vue-debounce'
export default defineNuxtPlugin((nuxtApp) => {
    nuxtApp.vueApp.directive("debounce", vueDebounce({
      lock: true, // Optional: Prevent new executions until debounce completes
    }));
  });