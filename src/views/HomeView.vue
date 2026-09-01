<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import AppIcon from '../components/AppIcon.vue'
import { profile, recentProgress } from '../data'

const { t, locale } = useI18n()
const avatarFailed = ref(false)

/* 标签颜色映射按原始中文 tag 作为 key，展示文案走 i18n */
const tagColor = (tag: string) =>
  ({
    发布: 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-300',
    前端: 'bg-sky-500/10 text-sky-600 dark:text-sky-300',
    博客: 'bg-fuchsia-500/10 text-fuchsia-600 dark:text-fuchsia-300',
  })[tag] ?? 'bg-zinc-500/10 text-zinc-600 dark:text-zinc-300'

</script>

<template>
  <div>
    <!-- 警告：此组件必须保持单根节点，外层 div 不能删；RouterView 的 Transition 不支持多根，模板顶部也不能放注释（dev 下会渲染成注释节点变成 fragment），否则页面互切时渲染不出来 -->
    <section class="flex min-h-[65vh] flex-col items-center justify-center gap-5 px-4 pt-24 text-center sm:gap-6 sm:pt-28">
      <!-- 头像直接用 GitHub 头像，加载失败退回本地占位 SVG -->
      <img
        :src="`https://github.com/${profile.name}.png`"
        :alt="profile.name"
        class="h-28 w-28 rounded-full border-2 border-white/60 object-cover shadow-xl transition-transform duration-300 hover:scale-105 sm:h-32 sm:w-32 dark:border-white/10"
        @error="avatarFailed = true"
        v-show="!avatarFailed"
      />
      <span v-if="avatarFailed" class="flex h-28 w-28 items-center justify-center rounded-full text-sky-400 sm:h-32 sm:w-32">
        <AppIcon name="sparkle" :size="96" />
      </span>
      <h1 class="animate-float-up bg-gradient-to-r from-sky-500 to-indigo-500 bg-clip-text text-4xl font-extrabold text-transparent sm:text-5xl">
        {{ profile.name }}
      </h1>
      <p class="animate-float-up text-base text-zinc-600 sm:text-lg dark:text-zinc-300" style="animation-delay: 120ms">
        {{ t('hero.tagline') }}
      </p>
      <div class="animate-float-up flex flex-wrap justify-center gap-3 sm:gap-4" style="animation-delay: 240ms">
        <a
          v-for="s in profile.socials"
          :key="s.name"
          :href="s.url"
          target="_blank"
          rel="noopener"
          class="liquid-glass flex h-11 items-center gap-2 rounded-full px-4 text-sm font-medium transition-all duration-300 hover:-translate-y-1 hover:shadow-lg sm:px-5"
        >
          <!-- GitHub 入口用 GitHub 头像当图标，其它入口用 SVG 图标 -->
          <img
            v-if="s.icon === 'github'"
            :src="`https://github.com/${profile.name}.png`"
            alt=""
            class="h-5 w-5 rounded-full object-cover"
          />
          <AppIcon v-else :name="s.icon" :size="17" />
          {{ s.name }}
        </a>
      </div>
    </section>

    <!-- 最近进展 -->
    <section class="mx-auto max-w-2xl px-4 pb-16 sm:px-0">
      <h2 class="mb-5 flex items-center gap-2 text-xl font-bold text-zinc-800 dark:text-zinc-100">
        <AppIcon name="sparkle" :size="20" class="text-sky-500" />
        {{ t('hero.recent') }}
      </h2>
      <div class="space-y-3">
        <div
          v-for="(p, i) in recentProgress"
          :key="p.date + p.text"
          class="liquid-glass animate-float-up flex flex-wrap items-center gap-x-4 gap-y-1 rounded-2xl px-4 py-3 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg sm:px-5 sm:py-3.5"
          :style="{ animationDelay: `${i * 100}ms` }"
        >
          <time class="shrink-0 text-xs font-semibold text-zinc-400">{{ p.date }}</time>
          <span class="min-w-0 flex-1 text-sm text-zinc-700 dark:text-zinc-200">
            {{ locale === 'en' ? p.textEn : p.text }}
          </span>
          <span class="shrink-0 rounded-full px-2.5 py-0.5 text-xs font-medium" :class="tagColor(p.tag)">
            {{ t('tags.' + p.tag) }}
          </span>
        </div>
      </div>
    </section>
  </div>
</template>
