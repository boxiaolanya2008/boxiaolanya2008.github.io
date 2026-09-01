<script setup lang="ts">
defineProps<{ loading?: boolean }>()
</script>

<template>
  <!-- 骨架屏占位块：内容未就绪时先渲染灰色块，禁止白屏等待 -->
  <div v-if="loading" class="liquid-glass rounded-2xl p-5" aria-hidden="true">
    <div class="mb-3 h-5 w-2/5 animate-pulse rounded-lg bg-zinc-300/70 dark:bg-zinc-600/50"></div>
    <div class="mb-2 h-3.5 w-full animate-pulse rounded bg-zinc-300/60 dark:bg-zinc-600/40"></div>
    <div class="mb-2 h-3.5 w-5/6 animate-pulse rounded bg-zinc-300/60 dark:bg-zinc-600/40"></div>
    <div class="h-3.5 w-1/2 animate-pulse rounded bg-zinc-300/60 dark:bg-zinc-600/40"></div>
  </div>
  <div v-else class="liquid-glass group rounded-2xl p-5 transition-all duration-300 hover:-translate-y-1.5 hover:shadow-xl">
    <slot />
  </div>
</template>
