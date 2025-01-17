<template>
  <div>
    <!-- <div class="p-3 bg-primary text-white font-code text-xs overflow-auto tracking-tighter">USER_STORE: 
      <pre>
      {{ authStore }}
      </pre>

      <button @click="authStore.logout()" class="bg-red-700 px-4 py-2 uppercase font-code rounded-full">Logout</button>
    </div>  -->
    <NuxtLayout>
      <NuxtPage></NuxtPage>
      </NuxtLayout>
    </div>
</template>
<script setup lang="ts">
const authStore = useAuthStore()
const boardsStore = useBoardsStore()

</script>