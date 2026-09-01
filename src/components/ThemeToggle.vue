<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { Sunny, Moon } from '@element-plus/icons-vue'
import { useDark, useToggle } from '@vueuse/core'

const isDark = useDark()
const toggleDark = useToggle(isDark)
const { t } = useI18n()
</script>

<template>
  <el-tooltip :content="isDark ? t('theme.toLight') : t('theme.toDark')" placement="bottom">
    <button class="header-icon-button" :aria-label="isDark ? t('theme.toLight') : t('theme.toDark')" @click="toggleDark()">
      <el-icon :size="17"><Moon v-if="isDark" /><Sunny v-else /></el-icon>
    </button>
  </el-tooltip>
</template>
