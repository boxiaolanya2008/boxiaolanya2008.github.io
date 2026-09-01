<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import AppIcon from '../components/AppIcon.vue'
import { fallbackProjects, username } from '../data'
import type { Project } from '../data'

interface Repo {
  name: string
  description: string | null
  html_url: string
  homepage: string | null
  language: string | null
  stargazers_count: number
  topics: string[]
  fork: boolean
}

const { t, locale } = useI18n()
const repos = ref<Repo[] | null>(null)
const failed = ref(false)

/* 直接拉取 GitHub 上的公开仓库；接口失败时退回本地数据，别让页面空白 */
onMounted(async () => {
  try {
    const res = await fetch(`https://api.github.com/users/${username}/repos?sort=updated&per_page=100`)
    if (!res.ok) throw new Error(`GitHub API ${res.status}`)
    const data: Repo[] = await res.json()
    repos.value = data
      .filter((r) => !r.fork)
      .sort((a, b) => b.stargazers_count - a.stargazers_count)
  } catch {
    failed.value = true
  }
})

const showFallback = computed(() => failed.value || (repos.value !== null && repos.value.length === 0))

const fallbackDesc = (p: Project) => (locale.value === 'en' ? p.descriptionEn : p.description)
const repoDesc = (r: Repo) => r.description ?? t('projects.noDesc')
</script>

<template>
  <div class="mx-auto max-w-4xl px-5 py-14 sm:px-8 sm:py-20">
    <header class="mb-10">
      <h1 class="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50">{{ t('projects.title') }}</h1>
      <p v-if="failed" class="mt-3 flex items-center gap-2 text-sm text-amber-600 dark:text-amber-400">
        <AppIcon name="clock" :size="15" />
        {{ t('projects.fallback') }}
      </p>
    </header>

    <!-- 加载中骨架屏 -->
    <div v-if="!repos && !failed" class="grid gap-4 sm:grid-cols-2">
      <div v-for="i in 4" :key="i" class="h-40 animate-pulse rounded-xl border border-zinc-100 bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900"></div>
    </div>

    <!-- GitHub 仓库 -->
    <div v-else-if="repos && !showFallback" class="grid gap-4 sm:grid-cols-2">
      <a
        v-for="r in repos"
        :key="r.name"
        :href="r.html_url"
        target="_blank"
        rel="noopener"
        class="group rounded-xl border border-zinc-200/80 bg-white p-5 transition-all duration-300 hover:-translate-y-0.5 hover:border-zinc-300 hover:shadow-sm dark:border-zinc-800 dark:bg-zinc-900/60 dark:hover:border-zinc-700"
      >
        <div class="flex items-start justify-between gap-3">
          <h3 class="text-base font-semibold text-zinc-800 transition-colors group-hover:text-sky-600 dark:text-zinc-100 dark:group-hover:text-sky-400">
            {{ r.name }}
          </h3>
          <span class="flex shrink-0 items-center gap-1 text-xs text-zinc-400 dark:text-zinc-500">
            <AppIcon name="star" :size="13" />
            {{ r.stargazers_count }}
          </span>
        </div>
        <p class="mt-2 line-clamp-3 min-h-10 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
          {{ repoDesc(r) }}
        </p>
        <div class="mt-4 flex flex-wrap items-center gap-2">
          <span v-if="r.language" class="rounded-full bg-zinc-100 px-2.5 py-0.5 text-xs text-zinc-600 dark:bg-zinc-800 dark:text-zinc-300">
            {{ r.language }}
          </span>
          <span
            v-for="tp in (r.topics ?? []).slice(0, 3)"
            :key="tp"
            class="rounded-full border border-zinc-200 px-2.5 py-0.5 text-xs text-zinc-500 dark:border-zinc-700 dark:text-zinc-400"
          >
            {{ tp }}
          </span>
        </div>
      </a>
    </div>

    <!-- 本地兜底项目 -->
    <div v-else class="grid gap-4 sm:grid-cols-2">
      <a
        v-for="p in fallbackProjects"
        :key="p.name"
        :href="p.repo ?? '#'"
        target="_blank"
        rel="noopener"
        class="group rounded-xl border border-zinc-200/80 bg-white p-5 transition-all duration-300 hover:-translate-y-0.5 hover:border-zinc-300 hover:shadow-sm dark:border-zinc-800 dark:bg-zinc-900/60 dark:hover:border-zinc-700"
      >
        <h3 class="text-base font-semibold text-zinc-800 transition-colors group-hover:text-sky-600 dark:text-zinc-100 dark:group-hover:text-sky-400">
          {{ p.name }}
        </h3>
        <p class="mt-2 line-clamp-3 min-h-10 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
          {{ fallbackDesc(p) }}
        </p>
        <div class="mt-4 flex flex-wrap items-center gap-2">
          <span
            v-for="tp in p.tags"
            :key="tp"
            class="rounded-full border border-zinc-200 px-2.5 py-0.5 text-xs text-zinc-500 dark:border-zinc-700 dark:text-zinc-400"
          >
            {{ tp }}
          </span>
        </div>
      </a>
    </div>
  </div>
</template>
