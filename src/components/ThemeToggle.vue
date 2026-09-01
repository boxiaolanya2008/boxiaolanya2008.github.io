<script setup lang="ts">
import { useDark, useToggle } from '@vueuse/core'
import { useI18n } from 'vue-i18n'
import AppIcon from './AppIcon.vue'

/* 默认跟随系统，手动切换后持久化到 localStorage */
const isDark = useDark()
const toggleDark = useToggle(isDark)
const { t } = useI18n()
</script>

<template>
  <button
    class="flex h-9 w-9 cursor-pointer items-center justify-center rounded-md text-zinc-600 transition-all duration-300 hover:scale-105 hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-zinc-50"
    :aria-label="isDark ? t('theme.toLight') : t('theme.toDark')"
    @click="toggleDark()"
  >
    <Transition name="theme-flip" mode="out-in">
      <AppIcon :name="isDark ? 'moon' : 'sun'" :size="17" :key="String(isDark)" />
    </Transition>
  </button>
</template>

<style scoped>
.theme-flip-enter-active,
.theme-flip-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
.theme-flip-enter-from {
  transform: rotate(-90deg) scale(0.6);
  opacity: 0;
}
.theme-flip-leave-to {
  transform: rotate(90deg) scale(0.6);
  opacity: 0;
}
</style>
