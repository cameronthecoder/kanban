<template>
        <div class="h-full w-full overflow-x-auto" v-if="boardsStore.columns.length > 0 && boardsStore.board">
        <div class="flex gap-5 m-5 h-full">
            <Column v-for="column in boardsStore.columns" :key="column.id" :column="column"></Column>
            <NewColumn />
        </div>
    </div>
        <div class="h-full flex flex-col gap-4 justify-center items-center" v-else>
        <h1 class="text-sm text-mediumGray font-semibold">This board is empty. Create a new column to get started.</h1>
        <div>
            <button @click="open = true" class="bg-primary px-4 py-2 text-white rounded-full font-bold text-xs">Add New Column</button>
        </div>
    </div>

    <EditBoard :open="open" @close="open = false" />
</template>
<script setup lang="ts">
const route = useRoute();
import EditBoard from '~/components/modals/EditBoard.vue';
import { useBoardsStore } from '~/stores/boards';
const boardsStore = useBoardsStore();

const open = ref(false);

onMounted(async () => {
    await nextTick();
    boardsStore.setBoard(Number(route.params.id));
})


watch(
  () => boardsStore.boards,
  (newValue, oldValue) => {
    boardsStore.setBoard(Number(route.params.id));
    if (boardsStore.websocket.status === 'disconnected') {
      boardsStore.connectToBoardsWebSocket();
    }
  }
)

watch(
  () => boardsStore.board,
  (newValue, oldValue) => {
    if (boardsStore.websocket.status === 'disconnected') {
      boardsStore.connectToBoardsWebSocket();
    }
  }
)


definePageMeta({
    layout: 'main',
    middleware: 'auth'
})
</script>