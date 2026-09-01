<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { ArrowRight, ChatLineSquare, Star, HomeFilled } from '@element-plus/icons-vue'
import PostCard from '../components/PostCard.vue'
import { profile, username } from '../data'
import { postsApi, type DbPost } from '../api'

const { t, locale } = useI18n()

const dbPosts = ref<DbPost[] | null>(null)
onMounted(async () => {
  try {
    dbPosts.value = await postsApi.list()
  } catch {
    dbPosts.value = []
  }
})

const recent = computed(() => [...(dbPosts.value ?? [])].sort((a, b) => b.date.localeCompare(a.date)).slice(0, 3))
const bio = () => (locale.value === 'en' ? 'A developer who loves tinkering with frontend & tooling.' : t('site.tagline'))
const avatar = computed(() => `https://github.com/${username}.png?size=320`)
const featuredReview = computed(() =>
  [...(dbPosts.value ?? [])]
    .filter((p) => p.review)
    .sort((a, b) => (b.review?.rating ?? 0) - (a.review?.rating ?? 0))[0],
)
</script>

<template>
  <div class="mx-auto max-w-6xl px-5 sm:px-8">
    <section class="home-hero grid gap-10 py-14 sm:py-20 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
      <div>
        <p class="mb-4 inline-flex items-center gap-2 rounded-full border border-[var(--border)] bg-[var(--bg-subtle)] px-3 py-1 text-xs font-medium text-[var(--fg-muted)]">
          <el-icon :size="14"><HomeFilled /></el-icon>
          github.com/{{ username }}
        </p>
        <h1 class="home-title text-5xl font-semibold tracking-tight text-[var(--fg)] sm:text-6xl">
          {{ username }}
          <span class="mt-4 block max-w-xl text-lg font-normal leading-relaxed text-[var(--fg-muted)] sm:text-xl">{{ bio() }}</span>
        </h1>
        <div class="mt-8 flex flex-wrap items-center gap-3">
          <el-button type="primary" size="large" @click="$router.push('/projects')">
            {{ t('projects.title') }}
          </el-button>
          <el-button size="large" @click="$router.push('/blog')">
            {{ t('blog.title') }}
            <el-icon class="ml-1"><ArrowRight /></el-icon>
          </el-button>
        </div>
      </div>

      <div class="home-avatar-wrap mx-auto w-full max-w-sm">
        <img
          :src="avatar"
          :alt="profile.name"
          class="home-avatar aspect-square w-full rounded-[2rem] border border-[var(--border)] object-cover shadow-[0_24px_70px_-28px_var(--accent)]"
        />
        <div class="home-avatar-caption">
          <span class="text-xs font-medium text-[var(--fg-subtle)]">GitHub Avatar</span>
          <span class="text-sm font-semibold text-[var(--fg)]">{{ profile.name }}</span>
        </div>
      </div>
    </section>

    <section v-if="featuredReview" class="home-featured mb-12">
      <div class="flex flex-wrap items-center justify-between gap-4">
        <p class="flex items-center gap-2 text-sm font-semibold text-[var(--fg)]">
          <el-icon :size="16"><ChatLineSquare /></el-icon>
          {{ t('review.featured') }}
        </p>
        <el-button type="primary" link @click="$router.push(`/blog/${featuredReview.slug}`)">
          {{ t('blog.readMore') }}
          <el-icon class="ml-1"><ArrowRight /></el-icon>
        </el-button>
      </div>
      <div class="mt-3 flex flex-wrap items-center gap-3">
        <span class="review-score">
          <el-icon :size="15"><Star /></el-icon>
          {{ featuredReview.review?.rating.toFixed(1) }}
        </span>
        <span class="text-base font-semibold text-[var(--fg)]">{{ featuredReview.title }}</span>
        <span class="text-sm text-[var(--fg-subtle)]">{{ featuredReview.review?.subject }}</span>
      </div>
    </section>

    <section class="pb-20">
      <div class="mb-6 flex items-center justify-between">
        <h2 class="text-lg font-semibold text-[var(--fg)]">{{ t('home.recent') }}</h2>
        <el-button link @click="$router.push('/blog')">
          {{ t('home.allPosts') }}
          <el-icon class="ml-1"><ArrowRight /></el-icon>
        </el-button>
      </div>

      <div v-if="dbPosts === null" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <el-skeleton v-for="i in 3" :key="i" animated>
          <template #template><el-skeleton-item variant="rect" class="!h-40" /></template>
        </el-skeleton>
      </div>

      <div v-else-if="recent.length" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <PostCard v-for="post in recent" :key="post.slug" :post="post" />
      </div>

      <div v-else class="page-panel p-10 text-center">
        <el-empty :description="t('home.noPostsYet')" />
      </div>
    </section>
  </div>
</template>
