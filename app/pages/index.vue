<template>
    <div class="h-full flex flex-col gap-4 justify-center items-center">
        <h1 class="text-sm text-grayTheme font-semibold text-mediumGray">Please select a board from the sidebar</h1>
        <div>
            <button class="bg-primary px-4 py-2 text-white rounded-full font-bold text-xs">Add Board</button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Sidebar } from '#components';
import { useAPI } from '~/compostables/useAPI';
import { useBoardsStore } from '~/stores/boards';
const boardsStore = useBoardsStore()
definePageMeta({
    middleware: 'auth',
    layout: 'main'
})







</script>