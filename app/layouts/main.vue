<template>
        <div class="flex flex-row h-screen">
            <Sidebar />
            <div class="flex-1 flex flex-col overflow-x-auto" id="container">
                <div class="bg-white dark:bg-darkGray dark:text-white p-5 border-b-2 dark:border-darkLines border-gray-200 flex flex-row justify-between items-center" id="navbar">
                    <div>
                    <h1 class="text-xl mb-3 font-semibold" v-if="boardsStore.board">{{boardsStore.board.name}} (id: {{boardsStore.board.id}})</h1>
                    </div>
                    <p class="py-2 px-4 text-xs bg-green-400 dark:text-darkGray rounded-full font-bold uppercase" v-if="boardsStore.board">
                        {{ boardsStore.websocket.status }} -
                        {{ boardsStore.websocket.connections.length }} connections
                    </p>
                    <div class="flex gap-4 items-center">
                        <button @click="open = true" v-if="boardsStore.columns.length > 0" class="bg-primary px-4 py-4 text-white text-sm rounded-full font-bold">Add New Task</button>
                        <img :src="'https://ui-avatars.com/api/?name=' + userStore.user?.first_name + '+' + userStore.user?.last_name + '&bold=true&font-size=0.33'"
                            class="h-12 w-12 rounded-full">
                    </div>
                </div>
                <div class="bg-primaryLight dark:bg-darkBackground flex-1">
            <slot />
        </div>
            </div>
            <NewTask :open="open" @close="open = false" />
    </div>
  </template>

  <script setup lang="ts"> 
  import { useBoardsStore } from '~/stores/boards';
  import NewTask  from '../components/modals/NewTask.vue';
    import { useAuthStore } from '~/stores/auth';
    const userStore = useAuthStore();
const boardsStore = useBoardsStore();
const open = ref(false);
onMounted(async () => {
    await nextTick();
    await boardsStore.fetchBoards()
})
  </script>