export const useLoadingStore = defineStore("loading", {
    state: () => ({
        isLoading: false
    }),
    actions: {
        setLoading(isLoading: boolean) {
            this.isLoading = isLoading
        }
    }
})