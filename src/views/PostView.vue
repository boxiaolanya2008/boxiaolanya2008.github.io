<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import AppIcon from '../components/AppIcon.vue'
import { posts } from '../data'

const route = useRoute()
const { locale, t } = useI18n()

const post = computed(() => posts.find((p) => p.slug === route.params.slug))

const title = computed(() =>
  post.value && locale.value === 'en' && post.value.titleEn ? post.value.titleEn : post.value?.title,
)

/* 把正文按空行切成段落渲染 */
const paragraphs = computed(() => post.value?.content.split(/\n\s*\n/) ?? [])
</script>

<template>
  <div class="mx-auto max-w-2xl px-5 py-12 sm:px-8 sm:py-16">
    <RouterLink
      to="/blog"
      class="link-underline mb-8 inline-flex items-center gap-1.5 text-sm text-zinc-500 transition-colors hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-100"
    >
      <AppIcon name="arrow-left" :size="14" />
      {{ t('nav.blog') }}
    </RouterLink>

    <template v-if="post">
      <article>
        <header class="mb-8">
          <div class="mb-4 flex flex-wrap items-center gap-3 text-xs text-zinc-400 dark:text-zinc-500">
            <time :datetime="post.date">{{ post.date }}</time>
            <span v-for="tag in post.tags" :key="tag" class="rounded-full border border-zinc-200 px-2.5 py-0.5 dark:border-zinc-700">
              {{ tag }}
            </span>
          </div>
          <h1 class="text-3xl font-bold leading-tight tracking-tight text-zinc-900 sm:text-4xl dark:text-zinc-50">
            {{ title }}
          </h1>
        </header>
        <div class="space-y-5 leading-relaxed text-zinc-700 dark:text-zinc-300">
          <p v-for="(para, i) in paragraphs" :key="i">{{ para }}</p>
        </div>
      </article>
    </template>
    <div v-else class="py-16 text-center">
      <p class="text-zinc-600 dark:text-zinc-300">404</p>
      <p class="mt-1 text-sm text-zinc-400 dark:text-zinc-500">{{ t('blog.noPosts') }}</p>
    </div>
  </div>
</template>
