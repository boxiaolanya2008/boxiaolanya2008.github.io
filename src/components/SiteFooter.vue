<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { username } from '../data'

const { t } = useI18n()
</script>

<template>
  <footer class="border-t border-[var(--border)]">
    <div class="mx-auto flex max-w-5xl flex-col items-center justify-between gap-3 px-5 py-8 text-center sm:flex-row sm:px-8 sm:text-left">
      <span class="footer-line">© {{ new Date().getFullYear() }} {{ username }}</span>
      <span class="text-sm text-[var(--fg-subtle)]">{{ t('footer') }}</span>
    </div>
  </footer>
</template>
