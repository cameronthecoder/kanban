<template>
    <Modal :open="open" @close="$emit('close')">
        <h1 class="text-large flex-grow text-black dark:text-white font-bold">New Task</h1>
        <label for="name" class="text-xs font-bold text-mediumGray mt-10 block">Name</label>
        <input type="text" v-model="name" id="name" name="name"
            class="mt-1 block w-full px-3 py-2 border bg-white dark:text-white dark:bg-darkBackground dark:border-darkLines border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
            required>
        <label for="description" class="text-xs font-bold text-mediumGray mt-10 block">Description</label>
        <textarea id="description" name="description" v-model="description"
            class="mt-1 block w-full px-3 py-2 border bg-white dark:text-white dark:bg-darkBackground dark:border-darkLines border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
            required></textarea>
        <label for="status" class="text-xs font-bold text-mediumGray mb-4 mt-10 block">Status</label>
        <select id="status" name="status" v-model="column_id"
            class="mt-1 block w-full px-3 py-2 border bg-white dark:text-white dark:bg-darkBackground dark:border-darkLines border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
            required>
            <option v-for="column in boardsStore.columns" :key="column.id" :value="column.id">{{ column.name }}</option>
        </select>
    
        <button @click="saveChanges()" class="bg-primary px-4 py-4 text-white w-full mt-10 text-sm rounded-full font-bold">Save Changes</button>
    </Modal>
</template>
<script lang="ts" setup>
import { useBoardsStore } from '~/stores/boards';
const boardsStore = useBoardsStore();
const name = ref("");
const description = ref("");
const column_id = ref();
const emit = defineEmits(['close'])


const saveChanges = () => {
    boardsStore.sendEvent({
        type: 'add_task',
        data: {
            name: name.value,
            description: description.value,
            column_id: column_id.value
        }
    });
    emit('close');
}


defineProps<{
    open: boolean;
}>();

</script>