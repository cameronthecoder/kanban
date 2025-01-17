<template>
    <div 
        class="flex flex-col gap-4 min-w-80 relative" 
        @drop="drop" 
        @dragover="allowDrop" 
        @dragenter="dragEnter" 
        @dragleave="dragLeave"
    >
        <div v-if="dragHovering" class="absolute rounded-sm inset-0 bg-primary opacity-20 animate-pulse"></div>
        <h1 class="font-bold text-xs flex items-center text-grayTheme dark:text-mediumGray uppercase tracking-theme">
            <div class="h-4 w-4 bg-primary rounded-full mr-3"></div>{{ column?.name }} ({{ column.tasks.length }})
        </h1>
        <Task v-for="task in column.tasks" :task="task" />
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Task from './Task.vue';
import { useBoardsStore } from '#build/imports';


const boardsStore = useBoardsStore();

const props = defineProps<({
    column: Column
})>();

const dragHovering = ref(false);
let dragCounter = 0;

const drop = async (ev: DragEvent) => {
    ev.preventDefault();
    dragHovering.value = false;
    dragCounter = 0;
    const data = ev.dataTransfer?.getData("text");
    if (data) {
        console.log(props.column);
        await boardsStore.changeTaskColumn(JSON.parse(data), props.column.id);
    }
    console.log("data",data);
};

const allowDrop = (ev: DragEvent) => {
    ev.preventDefault();
};

const dragEnter = (ev: DragEvent) => {
    ev.preventDefault();
    dragCounter++;
    dragHovering.value = true;
};

const dragLeave = (ev: DragEvent) => {
    ev.preventDefault();
    dragCounter--;
    if (dragCounter === 0) {
        dragHovering.value = false;
    }
};
</script>
