<script setup lang="ts">
import { useI18n } from 'vue-i18n'

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
    class="flex h-9 cursor-pointer items-center rounded-md px-2.5 text-xs font-semibold text-zinc-600 transition-all duration-300 hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-zinc-50"
    :aria-label="t('lang.aria')"
    @click="toggleLocale"
  >
    {{ t('lang.label') }}
  </button>
</template>
