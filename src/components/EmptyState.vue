<script setup lang="ts">
defineProps<{ title?: string; hint?: string }>()
</script>

<template>
  <div class="flex flex-col items-center gap-3 py-12 text-center">
    <svg class="h-20 w-20 opacity-70" viewBox="0 0 96 96" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="48" cy="48" r="34" class="fill-sky-200/60 dark:fill-sky-500/20" />
      <path d="M30 54c6 8 30 8 36 0" stroke="currentColor" stroke-width="3" stroke-linecap="round" class="text-sky-500/70" />
      <circle cx="38" cy="42" r="3.5" class="fill-sky-600/70" />
      <circle cx="58" cy="42" r="3.5" class="fill-sky-600/70" />
    </svg>
    <p class="text-base font-medium text-zinc-700 dark:text-zinc-200">{{ title ?? '这里还空空如也' }}</p>
    <p class="text-sm text-zinc-500 dark:text-zinc-400">{{ hint ?? '内容正在路上，先去别处逛逛吧～' }}</p>
  </div>
</template>
