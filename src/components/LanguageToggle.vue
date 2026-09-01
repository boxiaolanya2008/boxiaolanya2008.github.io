<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import AppIcon from './AppIcon.vue'

const { locale, t } = useI18n()

/* 切换语言并持久化，同时同步 html lang 属性 */
function toggleLocale() {
  locale.value = locale.value === 'zh' ? 'en' : 'zh'
  localStorage.setItem('locale', locale.value)
  document.documentElement.lang = locale.value === 'zh' ? 'zh-CN' : 'en'
}
</script>

<template>
  <button
    class="liquid-glass flex h-9 cursor-pointer items-center gap-1.5 rounded-full px-3 text-xs font-semibold text-zinc-700 transition-all duration-300 hover:scale-105 hover:text-sky-500 dark:text-zinc-200"
    :aria-label="t('lang.aria')"
    @click="toggleLocale"
  >
    <AppIcon name="globe" :size="15" />
    {{ t('lang.label') }}
  </button>
</template>
