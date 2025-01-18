<template>
  <div aria-hidden="true" role="dialog" aria-modal="true" @click.self="closeModal()"
    :class="['fixed inset-0 overflow-y-auto flex justify-center items-center transition-colors', open ? 'bg-black bg-opacity-35' : 'hidden']">
    <div v-if="open"
      :class="['dark:bg-darkGray w-2/6 bg-white rounded shadow py-8 px-10 transition-all ease-in max-h-[75vh] overflow-y-auto', open ? 'scale-100 opacity-100' : 'scale-125 opacity-0']">
      <slot />
    </div>
    
  </div>
</template>

<script setup lang="ts">
defineProps<{
  open: boolean;
}>();

const emit = defineEmits(['close']);

const closeModal = () => {
  emit('close');
};
</script>