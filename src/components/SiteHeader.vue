<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import ThemeToggle from './ThemeToggle.vue'
import LanguageToggle from './LanguageToggle.vue'

const items = [
  { path: '/', label: 'nav.home' },
  { path: '/blog', label: 'nav.blog' },
  { path: '/projects', label: 'nav.projects' },
  { path: '/about', label: 'nav.about' },
] as const

const route = useRoute()
const { t } = useI18n()
const open = ref(false)

/* 路由切换后收起移动端菜单 */
watch(() => route.path, () => (open.value = false))
</script>

<template>
  <header class="sticky top-0 z-40 border-b border-zinc-200/70 bg-white/80 backdrop-blur-md dark:border-zinc-800 dark:bg-zinc-950/70">
    <div class="mx-auto flex h-16 max-w-4xl items-center justify-between gap-4 px-5 sm:px-8">
      <!-- 品牌 -->
      <RouterLink to="/" class="flex items-center gap-2 text-sm font-semibold tracking-tight text-zinc-800 dark:text-zinc-100">
        <span class="flex h-7 w-7 items-center justify-center rounded-full bg-zinc-900 text-xs text-white dark:bg-white dark:text-zinc-900">
          B
        </span>
        <span class="hidden sm:inline">{{ t('site.name') }}</span>
      </RouterLink>

      <!-- 桌面导航 -->
      <nav class="hidden items-center gap-1 md:flex" aria-label="Main">
        <RouterLink
          v-for="item in items"
          :key="item.path"
          :to="item.path"
          class="rounded-md px-3 py-1.5 text-sm transition-colors"
          :class="route.path === item.path || (item.path !== '/' && route.path.startsWith(item.path))
            ? 'bg-zinc-100 font-medium text-zinc-900 dark:bg-zinc-800 dark:text-zinc-50'
            : 'text-zinc-600 hover:bg-zinc-50 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-zinc-900 dark:hover:text-zinc-100'"
        >
          {{ t(item.label) }}
        </RouterLink>
      </nav>

      <!-- 右侧工具 -->
      <div class="flex items-center gap-1.5">
        <ThemeToggle />
        <LanguageToggle />
        <!-- 移动端菜单按钮 -->
        <button
          class="flex h-9 w-9 items-center justify-center rounded-md text-zinc-600 transition-colors hover:bg-zinc-100 md:hidden dark:text-zinc-300 dark:hover:bg-zinc-800"
          :aria-label="open ? 'Close menu' : 'Open menu'"
          :aria-expanded="open"
          @click="open = !open"
        >
          <svg v-if="!open" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round">
            <path d="M4 7h16M4 12h16M4 17h16" />
          </svg>
          <svg v-else class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round">
            <path d="M6 6l12 12M18 6 6 18" />
          </svg>
        </button>
      </div>
    </div>

    <!-- 移动端菜单 -->
    <Transition name="menu">
      <nav
        v-if="open"
        class="border-t border-zinc-200/70 px-5 py-3 md:hidden dark:border-zinc-800"
        aria-label="Mobile"
      >
        <div class="flex flex-col gap-1">
          <RouterLink
            v-for="item in items"
            :key="item.path"
            :to="item.path"
            class="rounded-md px-3 py-2.5 text-sm transition-colors"
            :class="route.path === item.path || (item.path !== '/' && route.path.startsWith(item.path))
              ? 'bg-zinc-100 font-medium text-zinc-900 dark:bg-zinc-800 dark:text-zinc-50'
              : 'text-zinc-600 hover:bg-zinc-50 dark:text-zinc-400 dark:hover:bg-zinc-900'"
          >
            {{ t(item.label) }}
          </RouterLink>
        </div>
      </nav>
    </Transition>
  </header>
</template>

<style scoped>
.menu-enter-active,
.menu-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.menu-enter-from,
.menu-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
