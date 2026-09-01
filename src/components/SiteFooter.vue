<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { username } from '../data'

const { t } = useI18n()
</script>

<template>
  <footer class="border-t border-zinc-200/70 dark:border-zinc-800">
    <div class="mx-auto flex max-w-4xl flex-col items-center justify-between gap-3 px-5 py-8 text-center text-sm text-zinc-500 sm:flex-row sm:px-8 sm:text-left dark:text-zinc-400">
      <span>© {{ new Date().getFullYear() }} {{ username }}</span>
      <span>{{ t('footer') }}</span>
    </div>
  </footer>
</template>
