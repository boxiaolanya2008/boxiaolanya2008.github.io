<script setup lang="ts">
import { useRouter } from 'vue-router'
import SiteHeader from './components/SiteHeader.vue'
import SiteFooter from './components/SiteFooter.vue'

const router = useRouter()

/* 路由切换回到页首；必须 instant，CSS 的 smooth 会让长页面切页时停在底部 */
router.afterEach(() => window.scrollTo({ top: 0, behavior: 'instant' }))
</script>

<template>
  <div class="flex min-h-screen flex-col bg-white text-zinc-800 transition-colors dark:bg-zinc-950 dark:text-zinc-100">
    <SiteHeader />
    <main class="flex-1">
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" :key="$route.path" />
        </Transition>
      </RouterView>
    </main>
    <SiteFooter />
  </div>
</template>
