<template>
    <Modal :open="open" @close="$emit('close')">
        <div class="flex flex-row space-between items-center mb-10">
        <h1 class="text-large flex-grow text-black dark:text-white font-bold">{{ boardsStore.selectedTask?.name }}</h1>
        <svg width="5" height="20" xmlns="http://www.w3.org/2000/svg"><g fill="#828FA3" fill-rule="evenodd"><circle cx="2.308" cy="2.308" r="2.308"/><circle cx="2.308" cy="10" r="2.308"/><circle cx="2.308" cy="17.692" r="2.308"/></g></svg>
    </div>
        <h2 class="text-body mt-5 leading-body text-mediumGray">{{ boardsStore.selectedTask?.description }}</h2>

        <Subtasks />
    </Modal>
</template>

<script setup lang="ts">
import { useBoardsStore } from '#build/imports';
import { Modal, Subtasks } from '#components';

const boardsStore = useBoardsStore();

defineProps<{
    open: boolean;
}>();
</script>