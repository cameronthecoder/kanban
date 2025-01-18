<template>
    <Modal :open="open" @close="$emit('close')">
        <h1 class="text-large flex-grow text-black dark:text-white font-bold mb-5">Debug</h1>
        <p class="text-base font-bold text-mediumGray mt-10 block">WebSocket Host: <pre class="font-code text-sm bg-white p-2 rounded overflow-auto">{{ boardsStore.websocket.socket?.url }}</pre></p>
        <p class="text-base font-bold text-mediumGray mt-10 block">WebSocket Status: <pre class="font-code text-sm text-white uppercase">{{ boardsStore.websocket.status }}</pre></p>
        <p class="text-base font-bold text-mediumGray mt-10 block">Connection: <pre class="font-code bg-darkBackground p-2 rounded-md text-sm">{{ boardsStore.websocket.connection }}</pre></p>
        <p class="text-base font-bold text-mediumGray mt-10 block">Board: <pre class="font-code bg-darkBackground p-2 rounded-md text-sm">{{ boardsStore.board }}</pre></p>
        <p class="text-base font-bold text-mediumGray mt-10 block">Active Connections: <pre class="font-code bg-darkBackground p-2 rounded-md text-sm">{{ boardsStore.websocket.connections }}</pre></p>
        <button @click="boardsStore.logs = []" class="bg-primary mb-10 px-4 py-4 text-white w-full mt-10 text-sm rounded-full font-bold">Clear</button>
        <h1 class="text-large flex-grow text-black dark:text-white font-bold mb-5">Logs</h1>
        <ul class="space-y-4">
            <li v-for="log in boardsStore.logs" :id="log.title" class="flex gap-4 dark:bg-darkBackground p-5 items-center rounded-md">
                <div class="rounded-full p-2 bg-primary bg-opacity-30">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="size-6 text-white">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                    </svg>
                </div>
                <div>
                    <h1 class="text-base text-white font-bold">{{ log.title }}</h1>
                    <h1 class="mt-2 text-xs text-mediumGray uppercase font-bold font-code">{{ log.event }}</h1>
                </div>
            </li>


            
        </ul>
    </Modal>
</template>

<script lang="ts" setup>
import { useBoardsStore } from '~/stores/boards';
const boardsStore = useBoardsStore();
const props = defineProps<{
    open: boolean;
}>();

</script>