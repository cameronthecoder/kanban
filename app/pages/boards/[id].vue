<template>
  <button @click="openAuditLog = true" class="bg-white px-2 font-body rounded-md">Logs</button>
  <div class="relative h-full w-full" v-debounce:200ms="handleMouseMove" :debounce-events="'mousemove'">

<!-- Generator: Adobe Illustrator 24.1.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
 <div class="flex absolute items-center justify-center transition-all ease-in" v-show="connection.id != boardsStore.websocket.connection?.id" v-for="connection in boardsStore.websocket.connections" :id="connection.id" :style="{top: connection.mouse?.y + '%', left: connection.mouse?.x + '%'}">
 <svg  class="h-5" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
	 viewBox="0 0 48 48" style="enable-background:new 0 0 48 48;" xml:space="preserve">
<path style="fill:#35C1F1;" d="M14,7.054v30.663c0,0.91,1.062,1.407,1.761,0.824l7.078-5.903l4.664,10.728
	c0.232,0.533,0.851,0.777,1.384,0.545l1.865-0.811L14.634,6.091C14.276,6.246,14,6.593,14,7.054z"/>
<linearGradient id="SVGID_1_" gradientUnits="userSpaceOnUse" x1="21.3844" y1="6.3173" x2="35.5539" y2="39.0536">
	<stop  offset="0" style="stop-color:#46DFF9"/>
	<stop  offset="1" style="stop-color:#07D6F9"/>
</linearGradient>
<path style="fill:url(#SVGID_1_);" d="M33.089,40.938l-4.628-10.647l8.1-0.726c0.907-0.081,1.307-1.184,0.663-1.828L15.796,6.31
	c-0.336-0.336-0.793-0.379-1.162-0.219l16.118,37.011l1.792-0.779C33.077,42.091,33.321,41.471,33.089,40.938z"/>
<path style="fill:#199BE2;" d="M33.089,40.938l-4.628-10.647l8.1-0.726c0.907-0.081,1.307-1.184,0.663-1.828L15.796,6.31
	c-0.336-0.336-0.793-0.379-1.162-0.219l16.118,37.011l1.792-0.779C33.077,42.091,33.321,41.471,33.089,40.938z"/>
</svg> 
<span class="block rounded-xl px-2 bg-primary text-white  opacity-80 font-bold text-body">{{ connection.user.first_name }}</span>
 </div> 
        <div  class="h-full w-full overflow-x-auto" v-if="boardsStore.columns.length > 0 && boardsStore.board">
        <div class="flex gap-5 m-5 h-full">
            <Column v-for="column in boardsStore.columns" :key="column.id" :column="column"></Column>
            <NewColumn />
        </div>
    </div>
        <div class="h-full flex flex-col gap-4 justify-center items-center" v-else>
        <h1 class="text-sm text-mediumGray font-semibold">This board is empty. Create a new column to get started.</h1>
        <div>
            <button @click="open = true" class="bg-primary px-4 py-2 text-white rounded-full font-bold text-xs">Add New Column</button>
        </div>
    </div>

    <EditBoard :open="open" @close="open = false" />
    <AuditLog :open="openAuditLog" @close="openAuditLog = false" />
    </div>  
</template>
<script setup lang="ts">
const route = useRoute();
import EditBoard from '~/components/modals/EditBoard.vue';
import AuditLog from '~/components/modals/AuditLog.vue';
import { useBoardsStore } from '~/stores/boards';
const boardsStore = useBoardsStore();
const open = ref(false);
const openAuditLog = ref(false);

onMounted(async () => {
    await nextTick();
    boardsStore.setBoard(Number(route.params.id));
})



const mousePos = reactive({
    x: 0,
    y: 0
})

const handleMouseMove = (val: any, e: MouseEvent) => {
  const container = e.target as HTMLElement;
  const rect = container.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width) * 100;
  const y = ((e.clientY - rect.top) / rect.height) * 100;

  boardsStore.sendEvent({
    type: 'mouse_move',
    data: {
      x: x,
      y: y,
    }
  })
  
}
  
  
  


watch(
  () => boardsStore.boards,
  (newValue, oldValue) => {
    boardsStore.setBoard(Number(route.params.id));
    if (boardsStore.websocket.status === 'disconnected') {
      boardsStore.connectToBoardsWebSocket();
    }
  }
)

watch(
  () => boardsStore.board,
  (newValue, oldValue) => {
    if (boardsStore.websocket.status === 'disconnected') {
      boardsStore.connectToBoardsWebSocket();
    }
  }
)


definePageMeta({
    layout: 'main',
    middleware: 'auth'
})
</script>