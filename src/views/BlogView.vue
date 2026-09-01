<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { computed, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { Delete, Star } from '@element-plus/icons-vue'
import PostCard from '../components/PostCard.vue'
import { postsApi, type DbPost } from '../api'
import { isLoggedIn } from '../store'

const { t } = useI18n()
const router = useRouter()

const posts = ref<DbPost[] | null>(null)
const loadError = ref(false)

onMounted(async () => {
  try {
    posts.value = await postsApi.list()
  } catch {
    loadError.value = true
    posts.value = []
  }
})

const activeTag = ref('ALL')
const allTags = computed(() => [...new Set((posts.value ?? []).flatMap((p) => p.tags ?? []))])

const filtered = computed(() =>
  activeTag.value === 'ALL' ? posts.value ?? [] : (posts.value ?? []).filter((p) => p.tags?.includes(activeTag.value)),
)

const archive = computed(() => {
  const map = new Map<string, number>()
  for (const p of posts.value ?? []) map.set(p.date.slice(0, 4), (map.get(p.date.slice(0, 4)) ?? 0) + 1)
  return [...map.entries()]
})

const deleting = ref('')

async function removePost(slug: string) {
  if (!window.confirm(t('editor.deleteConfirm'))) return
  deleting.value = slug
  try {
    await postsApi.remove(slug)
    posts.value = (posts.value ?? []).filter((p) => p.slug !== slug)
  } catch (e) {
    ElMessage.error(e instanceof Error ? e.message : String(e))
  } finally {
    deleting.value = ''
  }
}

const reviewCount = computed(() => (posts.value ?? []).filter((p) => p.review).length)
</script>

<template>
  <div class="mx-auto max-w-5xl px-5 py-12 sm:px-8 sm:py-16">
    <header class="mb-8 flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-[var(--fg)] sm:text-4xl">{{ t('blog.title') }}</h1>
        <p class="mt-2 flex items-center gap-2 text-sm text-[var(--fg-muted)]">
          <span>{{ t('blog.total', { n: posts?.length ?? 0 }) }}</span>
          <el-tag v-if="reviewCount" type="warning" effect="plain" size="small" round>
            <el-icon :size="13"><Star /></el-icon>
            {{ reviewCount }} Reviews
          </el-tag>
        </p>
      </div>
      <el-button v-if="isLoggedIn" type="primary" @click="router.push('/write')">
        {{ t('editor.new') }}
      </el-button>
    </header>

    <div v-if="posts === null" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <el-skeleton v-for="i in 6" :key="i" animated>
        <template #template>
          <el-skeleton-item variant="rect" class="!h-44" />
        </template>
      </el-skeleton>
    </div>

    <div v-else-if="loadError" class="page-panel p-8 text-center">
      <el-result icon="warning" :title="t('blog.backendDown')" />
    </div>

    <template v-else>
      <el-radio-group v-model="activeTag" class="mb-8 flex flex-wrap gap-2">
        <el-radio-button value="ALL">{{ t('blog.all') }}</el-radio-button>
        <el-radio-button v-for="tag in allTags" :key="tag" :value="tag">{{ tag }}</el-radio-button>
      </el-radio-group>

      <div v-if="filtered.length" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <div v-for="post in filtered" :key="post.slug" class="group relative">
          <PostCard :post="post" />
          <el-button
            v-if="isLoggedIn"
            class="absolute right-3 top-3 z-10 !p-2 opacity-0 focus:opacity-100 group-hover:opacity-100"
            type="danger"
            plain
            circle
            :loading="deleting === post.slug"
            :aria-label="t('editor.delete')"
            @click.prevent.stop="removePost(post.slug)"
          >
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
      </div>

      <div v-else class="page-panel p-14 text-center">
        <el-empty :description="t('blog.noPosts')" />
      </div>

      <footer v-if="archive.length" class="mt-12 border-t border-[var(--border)] pt-6">
        <div class="flex flex-wrap gap-x-6 gap-y-2 text-sm text-[var(--fg-muted)]">
          <span v-for="([year, count], i) in archive" :key="year" class="flex items-center gap-1.5">
            <span v-if="i > 0" class="text-[var(--fg-subtle)]">·</span>
            <span class="font-medium text-[var(--fg)]">{{ year }}</span>
            <el-tag size="small" effect="plain" round>{{ count }}</el-tag>
          </span>
        </div>
      </footer>
    </template>
  </div>
</template>
