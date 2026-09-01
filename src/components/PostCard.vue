<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { Star, ArrowRight, CollectionTag, Clock } from '@element-plus/icons-vue'
import type { DbPost } from '../api'

const props = defineProps<{ post: DbPost }>()
const { locale } = useI18n()

const localizedTitle = computed(() =>
  props.post.titleEn && locale.value === 'en' ? props.post.titleEn : props.post.title,
)
const localizedSummary = computed(() =>
  props.post.summaryEn && locale.value === 'en' ? props.post.summaryEn : props.post.summary,
)
const reviewSubject = computed(() =>
  props.post.review?.subjectEn && locale.value === 'en' ? props.post.review.subjectEn : props.post.review?.subject,
)
</script>

<template>
  <article class="page-panel group p-5 transition-all duration-300 hover:-translate-y-0.5 hover:border-[var(--border-strong)]">
    <div class="mb-3 flex flex-wrap items-center gap-2 text-xs text-[var(--fg-subtle)]">
      <el-icon :size="14"><Clock /></el-icon>
      <time :datetime="post.date">{{ post.date }}</time>
      <el-tag v-for="tag in post.tags ?? []" :key="tag" size="small" type="info" effect="plain" round>
        {{ tag }}
      </el-tag>
      <span v-if="post.review" class="review-score">
        <el-icon :size="14"><Star /></el-icon>
        {{ post.review.rating.toFixed(1) }}
      </span>
    </div>

    <h3 class="text-lg font-semibold text-[var(--fg)] transition-colors group-hover:text-[var(--accent-fg)]">
      <RouterLink :to="`/blog/${post.slug}`" class="link-underline">
        {{ localizedTitle }}
      </RouterLink>
    </h3>

    <p v-if="reviewSubject" class="mt-1.5 flex items-center gap-1.5 text-xs font-medium text-[var(--accent-fg)]">
      <el-icon :size="14"><CollectionTag /></el-icon>
      {{ reviewSubject }}
    </p>

    <p class="mt-3 line-clamp-3 text-sm leading-relaxed text-[var(--fg-muted)]">
      {{ localizedSummary }}
    </p>

    <div class="mt-4 flex items-center gap-1 text-xs font-medium text-[var(--fg-subtle)] transition-colors group-hover:text-[var(--accent-fg)]">
      {{ $t('blog.readMore') }}
      <el-icon :size="13" class="transition-transform duration-300 group-hover:translate-x-0.5"><ArrowRight /></el-icon>
    </div>
  </article>
</template>
