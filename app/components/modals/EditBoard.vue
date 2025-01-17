<template>
    <Modal :open="open" @close="$emit('close')">
        <h1 class="text-large flex-grow text-black dark:text-white font-bold">Edit Board</h1>
        <label for="board_name" class="text-xs font-bold text-mediumGray mt-10 block">Board Name</label>
        <input type="text" id="board_name" name="board_name" v-model="name"
            class="mt-1 block w-full px-3 py-2 border bg-white dark:text-white dark:bg-darkBackground dark:border-darkLines border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
            required>
        <label for="board_name" class="text-xs font-bold text-mediumGray mb-4 mt-10 block">Board Columns</label>
            <div v-for="column in boardsStore.columns" :key="column.id" class="flex items-center flex-row gap-2">
            <input :value="column.name" type="text" id="new_column_name" name="new_column_name" 
                class="mt-1 block w-full px-3 py-2 border bg-white dark:text-white dark:bg-darkBackground dark:border-darkLines border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                required>
                <button @click="deleteColumn(column.id)" class="block px-3 py-2 border bg-white dark:text-white dark:bg-red-400 dark:border-darkLines border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-4">
  <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
</svg>

                </button>
            </div>  
            <input v-if="isAddingColumn" v-model="columnName" type="text" id="new_column_name" name="new_column_name" 
            class="mt-1 block w-full px-3 py-2 border bg-white dark:text-white dark:bg-darkBackground dark:border-darkLines border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
            required>
    

            <button @click="isAddingColumn = true" v-if="!isAddingColumn" class="bg-primary/10 hover:bg-primary/25 dark:bg-white text-primary border border-primary/10 px-4 py-2 mt-10 text-sm rounded-full font-bold">New Column</button>
        <button @click="saveChanges()" class="bg-primary px-4 py-4 text-white w-full mt-10 text-sm rounded-full font-bold">Save Changes</button>
    </Modal>
</template>
<script lang="ts" setup>
import { mapState } from 'pinia';
import { useBoardsStore } from '~/stores/boards';
const boardsStore = useBoardsStore();
const columnName = ref("");
const isAddingColumn = ref(false);
const emit = defineEmits(['close'])
const prevName = ref(boardsStore.board?.name);

const name = computed({
      get: () => boardsStore.board?.name,
      set: (value) => {
        if (boardsStore.board) {boardsStore.board.name = value || ''};
      },
    });


const deleteColumn = (id: number) => {
    boardsStore.sendEvent({
        type: 'delete_column',
        data: {
            "column_id": id
        }
    });
}

const saveChanges = () => {
    boardsStore.sendEvent({
        type: 'edit_board',
        data: {
            name: name.value,
        }
    });
    if (isAddingColumn.value) {
    
    boardsStore.sendEvent({
        type: 'add_column',
        data: {
            name: columnName.value
        }
        
    });
}   
    emit('close');
}


defineProps<{
    open: boolean;
}>();

</script>