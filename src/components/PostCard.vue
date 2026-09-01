<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import type { Post } from '../data'
import AppIcon from './AppIcon.vue'

defineProps<{ post: Post }>()
const { locale } = useI18n()

const localizedTitle = (p: Post) => (locale.value === 'en' && p.titleEn ? p.titleEn : p.title)
const localizedSummary = (p: Post) => (locale.value === 'en' && p.summaryEn ? p.summaryEn : p.summary)
</script>

<template>
  <article class="group rounded-xl border border-zinc-200/80 bg-white p-5 transition-all duration-300 hover:-translate-y-0.5 hover:border-zinc-300 hover:shadow-sm dark:border-zinc-800 dark:bg-zinc-900/60 dark:hover:border-zinc-700">
    <div class="flex items-center gap-3 text-xs text-zinc-400 dark:text-zinc-500">
      <time :datetime="post.date">{{ post.date }}</time>
      <span class="flex flex-wrap gap-1.5">
        <span
          v-for="tag in post.tags"
          :key="tag"
          class="rounded-full border border-zinc-200 px-2 py-0.5 text-[11px] text-zinc-500 dark:border-zinc-700 dark:text-zinc-400"
        >
          {{ tag }}
        </span>
      </span>
    </div>
    <h3 class="mt-3 text-lg font-semibold text-zinc-800 transition-colors group-hover:text-sky-600 dark:text-zinc-100 dark:group-hover:text-sky-400">
      <RouterLink :to="`/blog/${post.slug}`" class="link-underline">
        {{ localizedTitle(post) }}
      </RouterLink>
    </h3>
    <p class="mt-2 line-clamp-3 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
      {{ localizedSummary(post) }}
    </p>
    <div class="mt-4 flex items-center gap-1 text-xs font-medium text-zinc-400 transition-colors group-hover:text-sky-600 dark:group-hover:text-sky-400">
      {{ $t('blog.readMore') }}
      <AppIcon name="arrow-right" :size="13" class="transition-transform duration-300 group-hover:translate-x-0.5" />
    </div>
  </article>
</template>
