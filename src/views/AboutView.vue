<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import AppIcon from '../components/AppIcon.vue'
import { profile, skills, timeline } from '../data'

const { t, locale } = useI18n()

const localized = (n: (typeof timeline)[number]) =>
  locale.value === 'en'
    ? { ...n, title: n.titleEn, detail: n.detailEn }
    : n
</script>

<template>
  <div class="mx-auto max-w-3xl px-5 py-14 sm:px-8 sm:py-20">
    <header class="mb-12">
      <h1 class="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50">{{ t('about.title') }}</h1>
    </header>

    <!-- 简介 -->
    <section class="mb-12">
      <p class="text-base leading-relaxed text-zinc-700 dark:text-zinc-300">
        {{ t('about.bio') }}
      </p>
    </section>

    <!-- 技能 -->
    <section class="mb-12">
      <h2 class="mb-5 text-lg font-semibold text-zinc-900 dark:text-zinc-50">{{ t('about.skills') }}</h2>
      <ul class="space-y-3">
        <li v-for="s in skills" :key="s.label" class="flex items-center gap-3">
          <span class="w-32 shrink-0 text-sm text-zinc-600 dark:text-zinc-300">{{ s.label }}</span>
          <div class="h-1.5 flex-1 overflow-hidden rounded-full bg-zinc-100 dark:bg-zinc-800">
            <div
              class="h-full rounded-full bg-zinc-400 transition-all duration-700 dark:bg-zinc-500"
              :style="{ width: `${(s.level / 5) * 100}%` }"
            ></div>
          </div>
        </li>
      </ul>
    </section>

    <!-- 时间线 -->
    <section class="mb-12">
      <h2 class="mb-6 text-lg font-semibold text-zinc-900 dark:text-zinc-50">{{ t('about.timeline') }}</h2>
      <ol class="relative ml-2 border-l border-zinc-200 pl-6 dark:border-zinc-800">
        <li v-for="node in timeline" :key="node.date" class="relative pb-8 last:pb-0">
          <span class="absolute top-1.5 -left-[31px] h-2.5 w-2.5 rounded-full bg-zinc-300 dark:bg-zinc-600"></span>
          <time class="text-xs font-medium text-zinc-400 dark:text-zinc-500">{{ localized(node).title }}</time>
          <p class="mt-1 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">{{ localized(node).detail }}</p>
        </li>
      </ol>
    </section>

    <!-- 联系 -->
    <section>
      <h2 class="mb-5 text-lg font-semibold text-zinc-900 dark:text-zinc-50">{{ t('about.contact') }}</h2>
      <div class="flex flex-wrap gap-3">
        <a
          v-for="s in profile.socials"
          :key="s.name"
          :href="s.url"
          target="_blank"
          rel="noopener"
          class="flex items-center gap-2 rounded-lg border border-zinc-200 px-4 py-2.5 text-sm font-medium text-zinc-700 transition-all duration-300 hover:-translate-y-0.5 hover:border-zinc-400 hover:shadow-sm dark:border-zinc-700 dark:text-zinc-200 dark:hover:border-zinc-500"
        >
          <AppIcon :name="s.icon" :size="16" />
          {{ s.name }}
        </a>
      </div>
    </section>
  </div>
</template>
