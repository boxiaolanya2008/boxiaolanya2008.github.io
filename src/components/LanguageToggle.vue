<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { RefreshRight } from '@element-plus/icons-vue'

const { locale, t } = useI18n()

function toggleLocale() {
  locale.value = locale.value === 'zh' ? 'en' : 'zh'
  localStorage.setItem('locale', locale.value)
  document.documentElement.lang = locale.value === 'zh' ? 'zh-CN' : 'en'
}
</script>

<template>
  <el-tooltip :content="t('lang.aria')" placement="bottom">
    <button class="header-icon-button" :aria-label="t('lang.aria')" @click="toggleLocale">
      <el-icon :size="17"><RefreshRight /></el-icon>
      <span class="ml-1 text-xs font-semibold">{{ t('lang.label') }}</span>
    </button>
  </el-tooltip>
</template>
