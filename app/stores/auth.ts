// define a store for authentication
import { defineStore } from 'pinia'
import { useAPI } from '~/compostables/useAPI'
import { useBoardsStore } from './boards'



// define a list of endpoints
const endpoints = {
    token: `/api/auth/token/`,
}

// defie the user type
export interface User {
    username: string
    first_name: string
    last_name: string
    is_admin: boolean
}

// define the token response
export interface TokenResponse {
    access_token: string
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as User | null,
    token: useCookie('token').value,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    async login(username: string, password: string) {
        const { data, status, error } = await useAPI<TokenResponse>(endpoints.token, {
            method: 'POST',
            body: new URLSearchParams({ username: username, password: password, 'grant_type': 'password', }).toString(),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
            }
            });



        if (status.value == "success" && data.value != null) {
            this.token = data.value.access_token
            refreshCookie('token')
            useCookie('token').value = data.value.access_token
            navigateTo('/')
        } else {
          console.log(data.value);
          console.log(status.value);
          
        }
        
    },

    async updateUser() {
      const { data, status, error } = await useAPI<User>('/api/auth/user/')
      if (data.value != null) {
        this.user = data.value
      }
      console.log(error);
      
    },

    logout() {
      const boardsStore = useBoardsStore();
      this.user = null
      useCookie('token').value = null
      boardsStore.boards = []
      boardsStore.columns = []
      navigateTo('/login')
    },
  },
})