<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import CapsuleNav from './components/CapsuleNav.vue'
import ThemeToggle from './components/ThemeToggle.vue'
import LanguageToggle from './components/LanguageToggle.vue'
import AppIcon from './components/AppIcon.vue'
import ParticleField from './components/ParticleField.vue'
import { username } from './data'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

/* 3D 背景（ThreeBackground.vue）已下线：白底上蓝灰立方体被反馈像"灰色杂质"。
   组件保留在 components 里，想恢复时在模板背景层里加回：
   <ThreeBackground /> */

const { t } = useI18n()
const router = useRouter()

/* 路由切换回到页首，避免停在上一页的滚动位置 */
router.afterEach(() => window.scrollTo({ top: 0 }))
</script>

<template>
  <!-- 背景光斑：液态玻璃的折射需要背后有颜色层次才出效果 -->
  <div class="pointer-events-none fixed inset-0 -z-10 overflow-hidden bg-white dark:from-zinc-950 dark:via-zinc-900 dark:to-indigo-950 dark:bg-gradient-to-br">
    <div class="absolute -top-24 -left-24 h-96 w-96 animate-blob rounded-full bg-sky-400/60 blur-3xl dark:bg-sky-600/20"></div>
    <div class="absolute top-1/3 -right-24 h-[28rem] w-[28rem] animate-blob rounded-full bg-indigo-400/50 blur-3xl dark:bg-indigo-700/20" style="animation-delay: -6s"></div>
    <div class="absolute bottom-0 left-1/4 h-80 w-80 animate-blob rounded-full bg-fuchsia-300/55 blur-3xl dark:bg-fuchsia-800/10" style="animation-delay: -12s"></div>
    <ParticleField />
  </div>

  <CapsuleNav />
  <div class="fixed top-4 right-4 z-50 flex gap-2">
    <LanguageToggle />
    <ThemeToggle />
  </div>

  <!-- 无缝页面切换 -->
  <RouterView v-slot="{ Component }">
    <Transition name="page" mode="out-in">
      <component :is="Component" />
    </Transition>
  </RouterView>

  <footer class="flex items-center justify-center gap-1.5 pb-10 text-center text-sm text-zinc-500 dark:text-zinc-400">
    <AppIcon name="github" :size="14" />
    <span>© 2026 {{ username }} · {{ t('footer') }}</span>
  </footer>
</template>

<style scoped>
.page-enter-active,
.page-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.page-enter-from {
  opacity: 0;
  transform: translateY(12px);
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
