<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import AppIcon from './AppIcon.vue'

const items = [
  { path: '/', label: 'nav.home', icon: 'home' },
  { path: '/projects', label: 'nav.projects', icon: 'folder' },
  { path: '/blog', label: 'nav.blog', icon: 'pen' },
  { path: '/timeline', label: 'nav.timeline', icon: 'clock' },
] as const

const route = useRoute()
const { t } = useI18n()
</script>

<template>
  <nav
    class="liquid-glass fixed top-4 left-1/2 z-50 flex -translate-x-1/2 items-center gap-1 rounded-full p-1.5"
    :aria-label="t('nav.home') + ' / ' + t('nav.projects')"
  >
    <RouterLink
      v-for="item in items"
      :key="item.path"
      :to="item.path"
      class="relative flex items-center gap-1.5 rounded-full px-2.5 py-1.5 text-sm font-medium transition-all duration-300 sm:px-3.5 md:px-4"
      :class="route.path === item.path
        ? 'bg-sky-500/90 text-white shadow-lg shadow-sky-500/30'
        : 'text-zinc-600 hover:bg-white/40 dark:text-zinc-300 dark:hover:bg-white/10'"
    >
      <AppIcon :name="item.icon" :size="15" />
      <!-- 窄屏只显示图标，宽屏带文字，胶囊自适应收缩 -->
      <span class="hidden md:inline">{{ t(item.label) }}</span>
    </RouterLink>
  </nav>
</template>
