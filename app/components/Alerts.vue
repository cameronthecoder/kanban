<template>
    <!-- create an alert component -->
    <ul class="my-5">
        <li class="bg-gray-300 my-2 transition-all ease-in text-body text-gray-700 rounded px-4 py-2 font-bold" v-for="alert in alertStore.alerts" :key="alert.message">{{ alert.message }}</li>
    </ul>
</template>
<script lang="ts" setup>
import { useAlertStore } from '#build/imports';
const alertStore = useAlertStore();

watch(() => alertStore.alerts, () => {
    setTimeout(() => {
        alertStore.alerts = [];
    }, 5000);
}, { deep: true });


</script>