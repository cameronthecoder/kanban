
<template>
<button @click="open = true" class="dark:bg-darkGray mt-8 bg-white min-h-full group justify-center min-w-80 flex items-center hover:bg-primary rounded-lg">
    <h1 class="text-2xl dark:text-white text-black group-hover:text-white font-bold">Add Column</h1>
</button>
<EditBoard :open="open" @close="open = false" />
</template>

<script setup lang="ts">
import EditBoard from './modals/EditBoard.vue';

const open = ref(false);

</script>