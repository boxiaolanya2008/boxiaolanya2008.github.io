<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import TimeLine from '../components/TimeLine.vue'
import AppIcon from '../components/AppIcon.vue'
import { timeline } from '../data'

const { locale, t } = useI18n()

/* 按年份分组展示，年份单独打一个玻璃胶囊 */
const groups = computed(() => {
  const map = new Map<string, typeof timeline>()
  for (const node of timeline) {
    const year = node.date.slice(0, 4)
    if (!map.has(year)) map.set(year, [])
    map.get(year)!.push(node)
  }
  return [...map.entries()]
})

const localized = (node: (typeof timeline)[number]) =>
  locale.value === 'en'
    ? { ...node, title: node.titleEn, detail: node.detailEn }
    : node
</script>

<template>
  <section class="mx-auto max-w-3xl px-4 pt-24 pb-16 sm:px-6 sm:pt-28 sm:pb-20">
    <h2 class="mb-8 flex items-center gap-2 text-2xl font-bold text-zinc-800 sm:text-3xl dark:text-zinc-100">
      <AppIcon name="clock" :size="26" class="text-sky-500" />
      {{ t('pages.timeline') }}
    </h2>
    <div v-for="[year, nodes] in groups" :key="year" class="mb-4 last:mb-0">
      <span class="liquid-glass mb-5 inline-block rounded-full px-4 py-1 text-sm font-bold text-sky-500 dark:text-sky-400">
        {{ year }}
      </span>
      <TimeLine :nodes="nodes.map(localized)" />
    </div>
  </section>
</template>
