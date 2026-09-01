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
    class="liquid-glass flex h-9 w-9 cursor-pointer items-center justify-center rounded-full text-zinc-700 transition-all duration-300 hover:scale-110 hover:text-sky-500 dark:text-zinc-200"
    :aria-label="isDark ? t('theme.toLight') : t('theme.toDark')"
    @click="toggleDark()"
  >
    <Transition name="theme-flip" mode="out-in">
      <AppIcon :name="isDark ? 'moon' : 'sun'" :size="18" :key="String(isDark)" />
    </Transition>
  </button>
</template>

<style scoped>
/* 主题切换时图标翻转过渡，避免生硬跳变 */
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
