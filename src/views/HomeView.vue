<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import PostCard from '../components/PostCard.vue'
import AppIcon from '../components/AppIcon.vue'
import { posts, profile, username } from '../data'

const { t, locale } = useI18n()
/* 首页展示最近 3 篇 */
const recent = posts.slice(0, 3)

const bio = () => (locale.value === 'en' ? 'A developer who loves tinkering with frontend & tooling.' : t('site.tagline'))
</script>

<template>
  <div class="mx-auto max-w-4xl px-5 sm:px-8">
    <!-- Hero -->
    <section class="flex flex-col items-center gap-6 py-20 text-center sm:py-28">
      <div class="animate-reveal">
        <img
          :src="`https://github.com/${profile.name}.png`"
          :alt="profile.name"
          class="h-24 w-24 rounded-full border border-zinc-200 object-cover shadow-sm dark:border-zinc-700 sm:h-28 sm:w-28"
        />
      </div>
      <div class="animate-reveal" style="animation-delay: 80ms">
        <p class="text-sm text-zinc-500 dark:text-zinc-400">{{ t('home.hello') }}</p>
        <h1 class="mt-1 text-4xl font-bold tracking-tight text-zinc-900 sm:text-5xl dark:text-zinc-50">{{ username }}</h1>
      </div>
      <p class="max-w-md animate-reveal text-base leading-relaxed text-zinc-600 sm:text-lg dark:text-zinc-300" style="animation-delay: 160ms">
        {{ bio() }}
      </p>
      <div class="mt-2 flex animate-reveal flex-wrap items-center justify-center gap-4" style="animation-delay: 240ms">
        <a
          v-for="s in profile.socials"
          :key="s.name"
          :href="s.url"
          target="_blank"
          rel="noopener"
          class="flex items-center gap-1.5 text-sm font-medium text-zinc-500 transition-colors hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-100"
        >
          <AppIcon :name="s.icon" :size="16" />
          {{ s.name }}
        </a>
      </div>
    </section>

    <!-- 最近文章 -->
    <section class="pb-20">
      <div class="mb-6 flex items-center justify-between">
        <h2 class="text-lg font-semibold text-zinc-900 dark:text-zinc-50">{{ t('home.recent') }}</h2>
        <RouterLink
          to="/blog"
          class="link-underline flex items-center gap-1 text-sm font-medium text-zinc-500 transition-colors hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-100"
        >
          {{ t('home.allPosts') }}
          <AppIcon name="arrow-right" :size="14" />
        </RouterLink>
      </div>
      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <PostCard v-for="post in recent" :key="post.slug" :post="post" />
      </div>
    </section>
  </div>
</template>
