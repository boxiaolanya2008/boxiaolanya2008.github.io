<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import GlassCard from '../components/GlassCard.vue'
import EmptyState from '../components/EmptyState.vue'
import GlassSelect from '../components/GlassSelect.vue'
import AppIcon from '../components/AppIcon.vue'
import { projects as fallbackProjects, username } from '../data'

interface Repo {
  name: string
  description: string | null
  html_url: string
  homepage: string | null
  language: string | null
  stargazers_count: number
  forks_count: number
  topics: string[]
  fork: boolean
}

const { t, locale } = useI18n()
const repos = ref<Repo[] | null>(null)
const failed = ref(false)
/* 用语义值 ALL 当哨兵，别拿界面文案当值；语言切换后文案变但选中态不丢 */
const activeTag = ref('ALL')

/* 直接渲染 GitHub 上的公开仓库；接口失败时退回本地数据，别让页面空白 */
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

const tagOptions = computed(() => {
  if (!repos.value) return [{ value: 'ALL', label: t('pages.all') }]
  const set = new Set<string>()
  for (const r of repos.value) {
    if (r.language) set.add(r.language)
    for (const tp of r.topics ?? []) set.add(tp)
  }
  return [{ value: 'ALL', label: t('pages.all') }, ...[...set].map((v) => ({ value: v, label: v }))]
})

const filtered = computed(() => {
  if (!repos.value) return []
  if (activeTag.value === 'ALL') return repos.value
  return repos.value.filter(
    (r) => r.language === activeTag.value || r.topics?.includes(activeTag.value),
  )
})
</script>

<template>
  <section class="mx-auto max-w-5xl px-4 pt-24 pb-16 sm:px-6 sm:pt-28 sm:pb-20">
    <h2 class="mb-6 flex items-center gap-2 text-2xl font-bold text-zinc-800 sm:text-3xl dark:text-zinc-100">
      <AppIcon name="folder" :size="26" class="text-sky-500" />
      {{ t('pages.projects') }}
    </h2>

    <!-- 标签下拉筛选，默认选中「全部」 -->
    <div v-if="repos" class="mb-6">
      <GlassSelect v-model="activeTag" :options="tagOptions" :aria-label="t('pages.projects')" />
    </div>

    <!-- 骨架屏：GitHub 数据未返回前先渲染占位块 -->
    <div v-if="!repos && !failed" class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      <GlassCard v-for="i in 6" :key="i" loading />
    </div>

    <!-- GitHub 仓库 -->
    <div v-else-if="repos" class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      <GlassCard v-for="r in filtered" :key="r.name">
        <div class="flex items-start justify-between gap-3">
          <h3 class="text-lg font-bold break-all text-zinc-800 dark:text-zinc-100">{{ r.name }}</h3>
          <span class="flex shrink-0 items-center gap-1 text-xs text-amber-500">
            <AppIcon name="star" :size="14" />
            {{ r.stargazers_count }}
          </span>
        </div>
        <p class="mt-2 line-clamp-3 min-h-10 text-sm text-zinc-600 dark:text-zinc-300">
          {{ r.description || t('pages.noDesc') }}
        </p>
        <div v-if="r.language || r.topics?.length" class="mt-4 flex flex-wrap gap-2">
          <span
            v-if="r.language"
            class="rounded-full bg-sky-500/10 px-3 py-1 text-xs font-medium text-sky-600 dark:text-sky-300"
          >
            {{ r.language }}
          </span>
          <span
            v-for="tp in (r.topics ?? []).slice(0, 3)"
            :key="tp"
            class="rounded-full bg-indigo-500/10 px-3 py-1 text-xs font-medium text-indigo-600 dark:text-indigo-300"
          >
            {{ tp }}
          </span>
        </div>
        <a
          :href="r.html_url"
          target="_blank"
          rel="noopener"
          class="mt-4 inline-flex items-center gap-1.5 text-sm font-medium text-sky-500 hover:underline"
        >
          <AppIcon name="github" :size="15" />
          {{ t('pages.repo') }}
        </a>
      </GlassCard>
      <div v-if="!filtered.length" class="sm:col-span-2 lg:col-span-3">
        <EmptyState :title="t('empty.repos')" :hint="t('empty.postsHint')" />
      </div>
    </div>

    <!-- GitHub 接口失败时的兜底数据 -->
    <template v-else>
      <p class="mb-6 flex items-center gap-2 text-sm text-amber-600 dark:text-amber-400">
        <AppIcon name="clock" :size="16" />
        {{ t('pages.fallback') }}
      </p>
      <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <GlassCard v-for="p in fallbackProjects" :key="p.name">
          <h3 class="text-lg font-bold text-zinc-800 dark:text-zinc-100">{{ p.name }}</h3>
          <p class="mt-2 text-sm text-zinc-600 dark:text-zinc-300">
            {{ locale === 'en' ? p.descriptionEn : p.description }}
          </p>
          <div class="mt-4 flex flex-wrap gap-2">
            <span
              v-for="tp in p.tags"
              :key="tp"
              class="rounded-full bg-sky-500/10 px-3 py-1 text-xs font-medium text-sky-600 dark:text-sky-300"
            >
              {{ tp }}
            </span>
          </div>
        </GlassCard>
      </div>
    </template>
  </section>
</template>
