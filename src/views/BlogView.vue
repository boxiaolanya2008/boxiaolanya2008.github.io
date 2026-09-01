<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import PostCard from '../components/PostCard.vue'
import AppIcon from '../components/AppIcon.vue'
import { posts } from '../data'

const { t } = useI18n()

/* 标签筛选：用 ALL 哨兵值，语言切换不影响选中态 */
const activeTag = ref('ALL')
const allTags = computed(() => [...new Set(posts.flatMap((p) => p.tags))])

const filtered = computed(() =>
  activeTag.value === 'ALL' ? posts : posts.filter((p) => p.tags.includes(activeTag.value)),
)

/* 按年份归档统计 */
const archive = computed(() => {
  const map = new Map<string, number>()
  for (const p of posts) map.set(p.date.slice(0, 4), (map.get(p.date.slice(0, 4)) ?? 0) + 1)
  return [...map.entries()]
})
</script>

<template>
  <div class="mx-auto max-w-3xl px-5 py-14 sm:px-8 sm:py-20">
    <header class="mb-10">
      <h1 class="text-3xl font-bold tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50">{{ t('blog.title') }}</h1>
      <p class="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
        {{ t('blog.total', { n: posts.length }) }}
      </p>
    </header>

    <!-- 标签筛选 -->
    <div class="mb-8 flex flex-wrap gap-2">
      <button
        class="cursor-pointer rounded-full border px-3.5 py-1.5 text-sm transition-all duration-200"
        :class="activeTag === 'ALL'
          ? 'border-zinc-900 bg-zinc-900 text-white dark:border-zinc-50 dark:bg-zinc-50 dark:text-zinc-900'
          : 'border-zinc-200 text-zinc-600 hover:border-zinc-400 dark:border-zinc-700 dark:text-zinc-400 dark:hover:border-zinc-500'"
        @click="activeTag = 'ALL'"
      >
        {{ t('blog.all') }}
      </button>
      <button
        v-for="tag in allTags"
        :key="tag"
        class="cursor-pointer rounded-full border px-3.5 py-1.5 text-sm transition-all duration-200"
        :class="activeTag === tag
          ? 'border-zinc-900 bg-zinc-900 text-white dark:border-zinc-50 dark:bg-zinc-50 dark:text-zinc-900'
          : 'border-zinc-200 text-zinc-600 hover:border-zinc-400 dark:border-zinc-700 dark:text-zinc-400 dark:hover:border-zinc-500'"
        @click="activeTag = tag"
      >
        {{ tag }}
      </button>
    </div>

    <!-- 文章列表 -->
    <div v-if="filtered.length" class="grid gap-4">
      <PostCard v-for="post in filtered" :key="post.slug" :post="post" />
    </div>
    <div v-else class="py-16 text-center">
      <p class="text-zinc-600 dark:text-zinc-300">{{ t('blog.noPosts') }}</p>
      <p class="mt-1 text-sm text-zinc-400 dark:text-zinc-500">{{ t('blog.noPostsHint') }}</p>
    </div>

    <!-- 归档 -->
    <footer v-if="archive.length" class="mt-16 border-t border-zinc-100 pt-8 dark:border-zinc-800">
      <h2 class="mb-4 flex items-center gap-2 text-sm font-semibold text-zinc-700 dark:text-zinc-200">
        <AppIcon name="clock" :size="15" class="text-zinc-400" />
        {{ t('blog.years') }}
      </h2>
      <div class="flex flex-wrap gap-x-6 gap-y-2 text-sm text-zinc-500 dark:text-zinc-400">
        <span v-for="([year, count], i) in archive" :key="year" class="flex items-center gap-1.5">
          <span v-if="i > 0" class="text-zinc-300 dark:text-zinc-600">·</span>
          <span class="font-medium text-zinc-700 dark:text-zinc-200">{{ year }}</span>
          <span>{{ count }}</span>
        </span>
      </div>
    </footer>
  </div>
</template>
