<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import GlassCard from '../components/GlassCard.vue'
import EmptyState from '../components/EmptyState.vue'
import GlassSelect from '../components/GlassSelect.vue'
import AppIcon from '../components/AppIcon.vue'
import { posts } from '../data'

const { t } = useI18n()

/* 标签筛选 + 按年份归档统计；用 ALL 哨兵值，语言切换不影响选中态 */
const activeTag = ref('ALL')
const tagOptions = computed(() => [
  { value: 'ALL', label: t('pages.all') },
  ...[...new Set(posts.flatMap((p) => p.tags))].map((v) => ({ value: v, label: v })),
])

const filtered = computed(() =>
  activeTag.value === 'ALL' ? posts : posts.filter((p) => p.tags.includes(activeTag.value)),
)

const archive = computed(() => {
  const map = new Map<string, number>()
  for (const p of posts) map.set(p.date.slice(0, 4), (map.get(p.date.slice(0, 4)) ?? 0) + 1)
  return [...map.entries()]
})
</script>

<template>
  <section class="mx-auto max-w-3xl px-4 pt-24 pb-16 sm:px-6 sm:pt-28 sm:pb-20">
    <div class="mb-6 flex items-center justify-between">
      <h2 class="flex items-center gap-2 text-2xl font-bold text-zinc-800 sm:text-3xl dark:text-zinc-100">
        <AppIcon name="pen" :size="26" class="text-sky-500" />
        {{ t('pages.blog') }}
      </h2>
      <span class="text-sm text-zinc-400">{{ t('pages.total', { n: posts.length }) }}</span>
    </div>

    <!-- 标签下拉筛选，默认选中「全部」 -->
    <div class="mb-6">
      <GlassSelect v-model="activeTag" :options="tagOptions" :aria-label="t('pages.blog')" />
    </div>

    <div v-if="filtered.length" class="space-y-5">
      <GlassCard v-for="post in filtered" :key="post.title">
        <article>
          <div class="flex items-baseline justify-between gap-4">
            <h3 class="text-lg font-bold text-zinc-800 dark:text-zinc-100">{{ post.title }}</h3>
            <time class="shrink-0 text-xs text-zinc-400">{{ post.date }}</time>
          </div>
          <p class="mt-2 text-sm text-zinc-600 dark:text-zinc-300">{{ post.summary }}</p>
          <div class="mt-3 flex items-center justify-between gap-4">
            <div class="flex flex-wrap gap-2">
              <span
                v-for="tp in post.tags"
                :key="tp"
                class="rounded-full bg-indigo-500/10 px-3 py-1 text-xs font-medium text-indigo-600 dark:text-indigo-300"
              >
                {{ tp }}
              </span>
            </div>
            <a v-if="post.url" :href="post.url" class="shrink-0 text-sm font-medium text-sky-500 hover:underline">
              {{ t('pages.readMore') }} →
            </a>
          </div>
        </article>
      </GlassCard>
    </div>
    <EmptyState v-else :title="t('empty.posts')" :hint="t('empty.postsHint')" />

    <!-- 归档统计 -->
    <div class="mt-10 flex items-center gap-3 text-sm text-zinc-500 dark:text-zinc-400">
      <AppIcon name="clock" :size="16" />
      <span v-for="([year, count], i) in archive" :key="year">
        {{ i > 0 ? '·' : '' }} {{ year }} {{ t('pages.yearPosts', { n: count }) }}
      </span>
    </div>
  </section>
</template>
