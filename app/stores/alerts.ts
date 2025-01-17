interface Alert {
    type: "error" | "success" | "info",
    message: string
}
export const useAlertStore = defineStore("alerts", {
    state: () => ({
        alerts: [] as Alert[], 
    }),
    actions: {
        addAlert(alert: Alert) {
            this.alerts.push(alert)
        },
        removeAlert(index: number) {
            this.alerts.splice(index, 1)
        }
    }
})