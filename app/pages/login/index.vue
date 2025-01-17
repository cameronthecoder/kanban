<template>
    <div class="h-screen bg-gray-200">
        <div class="flex items-center justify-center h-full">
            <div class=" bg-white py-10 px-5 rounded-xl w-96">
                <img src="/logo-dark.svg" alt="Logo" class="w-32 mx-auto">
                <h1 class="text-2xl font-bold text-center mt-6">Welcome back! </h1>
                <p class="text-center text-gray-500 mt-2">Log in to your account to continue</p>
                <Alerts />
                <form class="mt-6" @submit.prevent="userLogin">
                    <div class="mb-4">
                        <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
                        <input v-model="username" type="text" id="username" name="username"
                            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                            required>
                    </div>
                    <div class="mb-6">
                        <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
                        <input v-model="password" type="password" id="password" name="password"
                            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
                            required>
                    </div>
                    <button type="submit"
                        class="w-full bg-primary text-white p-3 rounded-md focus:outline-none focus:ring focus:ring-primary">Log
                        in</button>
                </form>
                <p class="text-center mt-8 text-sm text-gray-500">Don't have an account? <a href="#"
                        class="text-primary">Sign up</a></p>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { useAuthStore } from '~/stores/auth';

const username = ref('');
const password = ref('');

const authStore = useAuthStore()
const userLogin = async () => {
    await authStore.login(username.value, password.value);
}

</script>