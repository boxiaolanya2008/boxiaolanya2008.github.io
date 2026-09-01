<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ArrowLeft, Delete, Star, CircleCheck, CircleClose } from '@element-plus/icons-vue'
import MarkdownContent from '../components/MarkdownContent.vue'
import { postsApi, type DbPost } from '../api'
import { isLoggedIn } from '../store'

const route = useRoute()
const router = useRouter()
const { locale, t } = useI18n()

const dbPosts = ref<DbPost[] | null>(null)
const loadError = ref(false)

postsApi
  .list()
  .then((list) => (dbPosts.value = list))
  .catch(() => {
    loadError.value = true
    dbPosts.value = []
  })

const post = computed(() => dbPosts.value?.find((p) => p.slug === route.params.slug))

const title = computed(() =>
  post.value && locale.value === 'en' && post.value.titleEn ? post.value.titleEn : post.value?.title,
)

const reviewSubject = computed(() =>
  post.value?.review?.subjectEn && locale.value === 'en' ? post.value.review.subjectEn : post.value?.review?.subject,
)
const reviewSummary = computed(() =>
  post.value?.review?.summaryEn && locale.value === 'en' ? post.value.review.summaryEn : post.value?.review?.summary,
)
const reviewVerdict = computed(() =>
  post.value?.review?.verdictEn && locale.value === 'en' ? post.value.review.verdictEn : post.value?.review?.verdict,
)

const deleting = ref(false)

async function removePost() {
  const target = post.value
  if (!target || !window.confirm(t('editor.deleteConfirm'))) return
  deleting.value = true
  try {
    await postsApi.remove(target.slug)
    ElMessage.success(t('editor.deleted'))
    router.replace('/blog')
  } catch (e) {
    ElMessage.error(e instanceof Error ? e.message : String(e))
  } finally {
    deleting.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-3xl px-5 py-12 sm:px-8 sm:py-16">
    <el-button link class="mb-8" @click="router.push('/blog')">
      <el-icon class="mr-1"><ArrowLeft /></el-icon>
      {{ t('nav.blog') }}
    </el-button>

    <div v-if="dbPosts === null" class="space-y-4">
      <el-skeleton animated>
        <template #template>
          <el-skeleton-item variant="h1" class="!w-2/3" />
          <el-skeleton-item variant="text" />
          <el-skeleton-item variant="text" class="!w-5/6" />
        </template>
      </el-skeleton>
    </div>

    <div v-else-if="loadError" class="page-panel p-8 text-center">
      <el-result icon="warning" :title="t('blog.backendDown')" />
    </div>

    <template v-else-if="post">
      <article>
        <header class="mb-8">
          <div class="mb-4 flex flex-wrap items-center gap-3 text-xs text-[var(--fg-subtle)]">
            <time :datetime="post.date">{{ post.date }}</time>
            <el-tag v-for="tag in post.tags ?? []" :key="tag" size="small" type="info" effect="plain" round>
              {{ tag }}
            </el-tag>
          </div>
          <h1 class="text-3xl font-bold leading-tight tracking-tight text-[var(--fg)] sm:text-4xl">
            {{ title }}
          </h1>

          <div v-if="post.review" class="page-panel mt-6 p-5">
            <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
              <div>
                <p class="text-sm font-medium text-[var(--accent-fg)]">{{ t('review.subject') }}：{{ reviewSubject }}</p>
                <el-rate v-if="post.review.rating" :model-value="post.review.rating / 2" disabled class="mt-2" />
              </div>
              <span class="review-score">
                <el-icon :size="15"><Star /></el-icon>
                {{ post.review.rating.toFixed(1) }} / 10
              </span>
            </div>

            <p v-if="reviewSummary" class="text-sm leading-relaxed text-[var(--fg-muted)]">{{ reviewSummary }}</p>

            <div v-if="post.review.pros?.length || post.review.cons?.length" class="mt-4 grid gap-4 sm:grid-cols-2">
              <div v-if="post.review.pros?.length" class="rounded-xl bg-[var(--tip-bg)] p-4">
                <p class="mb-2 flex items-center gap-1.5 text-sm font-semibold text-[var(--tip-fg)]">
                  <el-icon><CircleCheck /></el-icon>
                  {{ t('review.pros') }}
                </p>
                <ul class="space-y-1.5 text-sm text-[var(--fg)]">
                  <li v-for="item in post.review.pros" :key="item">· {{ item }}</li>
                </ul>
              </div>
              <div v-if="post.review.cons?.length" class="rounded-xl bg-[var(--caution-bg)] p-4">
                <p class="mb-2 flex items-center gap-1.5 text-sm font-semibold text-[var(--caution-fg)]">
                  <el-icon><CircleClose /></el-icon>
                  {{ t('review.cons') }}
                </p>
                <ul class="space-y-1.5 text-sm text-[var(--fg)]">
                  <li v-for="item in post.review.cons" :key="item">· {{ item }}</li>
                </ul>
              </div>
            </div>

            <p v-if="reviewVerdict" class="mt-4 border-t border-[var(--border)] pt-3 text-sm font-medium text-[var(--fg)]">
              {{ t('review.verdict') }}：{{ reviewVerdict }}
            </p>
          </div>
        </header>

        <MarkdownContent :markdown="post.content" />
      </article>

      <div v-if="isLoggedIn" class="mt-10 border-t border-[var(--border)] pt-6">
        <el-button type="danger" plain :loading="deleting" @click="removePost">
          <el-icon class="mr-1"><Delete /></el-icon>
          {{ t('editor.delete') }}
        </el-button>
      </div>
    </template>

    <div v-else class="page-panel p-14 text-center">
      <el-empty description="404" />
      <p class="mt-1 text-sm text-[var(--fg-subtle)]">{{ t('blog.noPosts') }}</p>
    </div>
  </div>
</template>
