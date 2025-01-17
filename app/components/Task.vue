<template>
    <div role="button" @click="openModal()"  class="bg-white group dark:bg-darkGray p-4 rounded-md group shadow-sm hover:bg-primary hover:cursor-pointer hover:text-white" @dragstart="onDragging" draggable="true">
        <h1 class="font-bold text-sm dark:text-white">{{task?.name}}</h1>
        <h1 class="text-mediumGray group-hover:text-white text-body mt-3">0 of 3 subtasks</h1>
    </div>

    <TaskModal :open="open" @close="open = false" />
</template>
<script setup lang="ts">
import { useBoardsStore } from '#build/imports';
import TaskModal from './modals/TaskModal.vue';
const boardsStore = useBoardsStore();

const open = ref(false);

const props = defineProps<{
    task: Task
}>();

const openModal = () => {
    open.value = true;
    boardsStore.setSelectedTask(props.task);
}

const onDragging = (e: any) => {    
    e.dataTransfer.setData('text/plain', JSON.stringify(props.task))
    e.dataTransfer.effectAllowed = 'move'
}
</script>