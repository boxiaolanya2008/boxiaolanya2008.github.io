<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { Folder, Star, WarningFilled, ArrowRight } from '@element-plus/icons-vue'
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

onMounted(async () => {
  try {
    const res = await fetch(`https://api.github.com/users/${username}/repos?sort=updated&per_page=100`)
    if (!res.ok) throw new Error(`GitHub API ${res.status}`)
    const data: Repo[] = await res.json()
    repos.value = data.filter((r) => !r.fork).sort((a, b) => b.stargazers_count - a.stargazers_count)
  } catch {
    failed.value = true
  }
})

const showFallback = computed(() => failed.value || (repos.value !== null && repos.value.length === 0))
const fallbackDesc = (p: Project) => (locale.value === 'en' ? p.descriptionEn : p.description)
const repoDesc = (r: Repo) => r.description ?? t('projects.noDesc')
</script>

<template>
  <div class="mx-auto max-w-5xl px-5 py-12 sm:px-8 sm:py-16">
    <header class="mb-10">
      <h1 class="flex items-center gap-2 text-3xl font-bold tracking-tight text-[var(--fg)] sm:text-4xl">
        <el-icon :size="28"><Folder /></el-icon>
        {{ t('projects.title') }}
      </h1>
      <el-alert v-if="failed" :title="t('projects.fallback')" type="warning" show-icon :closable="false" class="mt-4" />
    </header>

    <div v-if="!repos && !failed" class="grid gap-4 sm:grid-cols-2">
      <el-skeleton v-for="i in 4" :key="i" animated>
        <template #template><el-skeleton-item variant="rect" class="!h-40" /></template>
      </el-skeleton>
    </div>

    <div v-else-if="repos && !showFallback" class="grid gap-4 sm:grid-cols-2">
      <a
        v-for="r in repos"
        :key="r.name"
        :href="r.html_url"
        target="_blank"
        rel="noopener"
        class="page-panel group p-5 transition-all duration-300 hover:-translate-y-0.5 hover:border-[var(--border-strong)]"
      >
        <div class="flex items-start justify-between gap-3">
          <h3 class="text-base font-semibold text-[var(--fg)] transition-colors group-hover:text-[var(--accent-fg)]">
            {{ r.name }}
          </h3>
          <span class="flex shrink-0 items-center gap-1 text-xs text-[var(--fg-subtle)]">
            <el-icon :size="13"><Star /></el-icon>
            {{ r.stargazers_count }}
          </span>
        </div>
        <p class="mt-2 line-clamp-3 min-h-10 text-sm leading-relaxed text-[var(--fg-muted)]">{{ repoDesc(r) }}</p>
        <div class="mt-4 flex flex-wrap items-center gap-2">
          <el-tag v-if="r.language" size="small" effect="plain" round>{{ r.language }}</el-tag>
          <el-tag v-for="tp in (r.topics ?? []).slice(0, 3)" :key="tp" size="small" type="info" effect="plain" round>
            {{ tp }}
          </el-tag>
          <el-icon class="ml-auto text-[var(--fg-subtle)] transition-transform group-hover:translate-x-0.5"><ArrowRight /></el-icon>
        </div>
      </a>
    </div>

    <div v-else class="grid gap-4 sm:grid-cols-2">
      <a
        v-for="p in fallbackProjects"
        :key="p.name"
        :href="p.repo ?? '#'"
        target="_blank"
        rel="noopener"
        class="page-panel group p-5 transition-all duration-300 hover:-translate-y-0.5 hover:border-[var(--border-strong)]"
      >
        <h3 class="text-base font-semibold text-[var(--fg)]">{{ p.name }}</h3>
        <p class="mt-2 line-clamp-3 min-h-10 text-sm leading-relaxed text-[var(--fg-muted)]">{{ fallbackDesc(p) }}</p>
        <div class="mt-4 flex flex-wrap items-center gap-2">
          <el-tag v-for="tp in p.tags" :key="tp" size="small" type="info" effect="plain" round>{{ tp }}</el-tag>
          <el-icon class="ml-auto text-[var(--fg-subtle)] transition-transform group-hover:translate-x-0.5"><ArrowRight /></el-icon>
        </div>
      </a>
    </div>

    <el-empty v-if="repos && repos.length === 0 && !failed" :description="t('projects.noRepos')" class="py-16" />
  </div>
</template>
