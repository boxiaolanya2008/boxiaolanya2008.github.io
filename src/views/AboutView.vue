<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { User, Medal, Calendar, Connection, Star, ArrowRight } from '@element-plus/icons-vue'
import { profile, skills, timeline } from '../data'

const { t, locale } = useI18n()

const localized = (n: (typeof timeline)[number]) =>
  locale.value === 'en' ? { ...n, title: n.titleEn, detail: n.detailEn } : n
</script>

<template>
  <div class="mx-auto max-w-4xl px-5 py-12 sm:px-8 sm:py-16">
    <header class="mb-10">
      <h1 class="flex items-center gap-2 text-3xl font-bold tracking-tight text-[var(--fg)] sm:text-4xl">
        <el-icon :size="28"><User /></el-icon>
        {{ t('about.title') }}
      </h1>
    </header>

    <section class="page-panel mb-8 p-6 sm:p-8">
      <p class="text-base leading-relaxed text-[var(--fg-muted)]">{{ t('about.bio') }}</p>
    </section>

    <section class="page-panel mb-8 p-6 sm:p-8">
      <h2 class="mb-6 flex items-center gap-2 text-lg font-semibold text-[var(--fg)]">
        <el-icon :size="18"><Medal /></el-icon>
        {{ t('about.skills') }}
      </h2>
      <div class="space-y-4">
        <div v-for="s in skills" :key="s.label" class="flex items-center gap-4">
          <span class="w-28 shrink-0 text-sm text-[var(--fg-muted)]">{{ s.label }}</span>
          <el-progress :percentage="s.level * 20" :show-text="false" :stroke-width="10" />
          <span class="w-6 text-right text-xs text-[var(--fg-subtle)]">{{ s.level }}</span>
        </div>
      </div>
    </section>

    <section class="page-panel mb-8 p-6 sm:p-8">
      <h2 class="mb-6 flex items-center gap-2 text-lg font-semibold text-[var(--fg)]">
        <el-icon :size="18"><Calendar /></el-icon>
        {{ t('about.timeline') }}
      </h2>
      <el-timeline>
        <el-timeline-item v-for="node in timeline" :key="node.date" :timestamp="node.date" placement="top">
          <p class="text-sm font-semibold text-[var(--fg)]">{{ localized(node).title }}</p>
          <p class="mt-1 text-sm leading-relaxed text-[var(--fg-muted)]">{{ localized(node).detail }}</p>
        </el-timeline-item>
      </el-timeline>
    </section>

    <section class="page-panel p-6 sm:p-8">
      <h2 class="mb-5 flex items-center gap-2 text-lg font-semibold text-[var(--fg)]">
        <el-icon :size="18"><Connection /></el-icon>
        {{ t('about.contact') }}
      </h2>
      <div class="flex flex-wrap gap-3">
        <el-button v-for="s in profile.socials" :key="s.name" tag="a" :href="s.url" target="_blank" rel="noopener">
          {{ s.name }}
          <el-icon class="ml-1"><ArrowRight /></el-icon>
        </el-button>
      </div>
      <p class="mt-5 flex items-center gap-1.5 text-xs text-[var(--fg-subtle)]">
        <el-icon :size="14"><Star /></el-icon>
        {{ t('footer') }}
      </p>
    </section>
  </div>
</template>
