import { useAPI } from '~/compostables/useAPI'
import type { User } from '~/stores/auth'



export interface Board {
    id: number
    name: string
    owner_id: number,
    users: Array<User>,
    description: string,
    columns: any
}

export interface Event {
    type: string
    data: any
}

export interface Task {
    id: number,
    name: string,
    column_id: number,
    description: string,
    is_done: boolean,
}

export interface Column {
    board_id: number,
    name: string,
    id: number,
    tasks: Array<Task>
}


export const useBoardsStore = defineStore("boards", {
    
    state: () => ({
        boards: [] as Board[],
        board: undefined as Board | undefined,
        columns: {} as Column[],
        selectedTask: undefined as Task | undefined,
        websocket: {
            socket: undefined as WebSocket | undefined,
            status: "disconnected" as "disconnected" | "connecting" | "connected" | "error"
        }
    }),
    actions: {
        setSelectedTask(task: Task) {
            this.selectedTask = task
        },
        async fetchBoards() {
            const { data, status, error } = await useAPI<Board[]>('/api/boards/');
            if (data.value != null) {
                this.boards = data.value
                if (error) {
                    console.log("error fetching boards");
                }
            }
        },  
        connectToBoardsWebSocket() {
            this.websocket.status = "connecting"
            const loadingStore = useLoadingStore();
            loadingStore.setLoading(true);
            if (this.websocket.socket) {
                this.websocket.socket.close();
            }
            // TODO: get base url from config
            const ws = new WebSocket(`wss://sea-turtle-app-5uo5v.ondigitalocean.app/api/boards/${this.board?.id}/ws/?token=${useCookie("token").value}`)
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data) as Event

                switch (data.type) {
                    case "columns": {
                        console.log(data.data);
                        
                        this.columns = data.data as Column[]
                        break
                    }
                    case "add_column": {
                        const new_column = data.data as Column
                        new_column.tasks = []
                        this.columns.push(new_column)
                        break
                    }
                    case "edit_board": {
                        console.log(data.data);
                        
                        const board = data.data as Board
                        this.board = board
                        break
                    }
                    case "add_task": {
                        const task = data.data as Task
                        const column_id = task.column_id
                        const column = this.columns.find(column => column.id === column_id)
                        column?.tasks.push(task)
                        break
                    }
                    case "delete_column": {
                        console.log(data.data);
                        const column_id = (data.data as { id: number }).id
                        this.columns = this.columns.filter(column => column.id !== column_id)
                        break
                    }
                    case "move_task": {
                        console.log(data.data);
                        
                        const { task: Task, to } = data.data
                        const column = this.columns.find(column => column.id === to)
                        // remove task from column
                        const oldColumn = this.columns.find(column => column.tasks.find(t => t.id === Task.id))
                        if (oldColumn) {
                            oldColumn.tasks = oldColumn.tasks.filter(t => t.id !== Task.id)
                        }
                        column?.tasks.push(Task)
                        break
                    }
                }
                
            }

            ws.onopen = () => {
                this.websocket.status = "connected"
                loadingStore.setLoading(false);
                this.sendEvent({ type: "columns", data: {} })
            }

            ws.onclose = () => {
                loadingStore.setLoading(false);
                this.websocket.status = "disconnected"
            }

            ws.onerror = (error) => {
                console.log(error);
                
                this.websocket.status = "error"
            }


            this.websocket.socket = ws
        },
        sendEvent(event: Event) {
            if (this.websocket.socket) {
                    this.websocket.socket.send(JSON.stringify(event))
                }
        },
        setBoards(boards: Board[]) {
            this.boards = boards
        },
        setBoard(id: number) {
            this.board = this.boards.find(board => board.id === id)
        },
        async changeTaskColumn(task: Task, column_id: number) {
            // change the task to a different column
            console.log('Moving task:', task, 'to column_id:', column_id);
            await this.sendEvent({ type: "move_task", data: { task_id: task.id, to: column_id } })
            const column = this.columns.find(column => column.id === column_id)
            // remove task from column
            const oldColumn = this.columns.find(column => column.tasks.find(t => t.id === task.id))
        },
        async fetchBoard(id: number) {
            const { data, status, error } = await useAPI<Board>(`/api/boards/${id}`)
            if (data.value != null) {
                this.board = data.value
            }

            console.log(error);
            

            if (error) {
                navigateTo("/")
            }
        },
    },
});