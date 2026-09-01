<script setup lang="ts">
import GlassCard from './GlassCard.vue'
import type { TimelineNode } from '../data'

defineProps<{ nodes: TimelineNode[] }>()
</script>

<template>
  <!-- 一条竖线串起节点，按时间倒序展示 -->
  <ol class="relative ml-3 border-l-2 border-sky-400/40 pl-8 dark:border-sky-400/30">
    <li
      v-for="(node, i) in nodes"
      :key="node.date"
      class="relative animate-float-up pb-10 last:pb-0"
      :style="{ animationDelay: `${i * 120}ms` }"
    >
      <span
        class="absolute top-1.5 -left-[41px] h-4 w-4 rounded-full border-4 border-white bg-sky-500 shadow-md dark:border-zinc-900"
      ></span>
      <GlassCard>
        <time class="text-xs font-semibold tracking-wide text-sky-500 dark:text-sky-400">{{ node.date }}</time>
        <h3 class="mt-1 text-lg font-bold text-zinc-800 dark:text-zinc-100">{{ node.title }}</h3>
        <p class="mt-1.5 text-sm text-zinc-600 dark:text-zinc-300">{{ node.detail }}</p>
      </GlassCard>
    </li>
  </ol>
</template>
