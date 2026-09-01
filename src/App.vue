<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import en from 'element-plus/es/locale/lang/en'
import SiteHeader from './components/SiteHeader.vue'
import SiteFooter from './components/SiteFooter.vue'

const router = useRouter()
const { locale } = useI18n()
const elementLocale = computed(() => (locale.value === 'zh' ? zhCn : en))

/* 路由切换回到页首；必须 instant，CSS 的 smooth 会让长页面切页时停在底部 */
router.afterEach(() => window.scrollTo({ top: 0, behavior: 'instant' }))
</script>

<template>
  <div class="app-shell flex flex-col transition-colors">
    <el-config-provider :locale="elementLocale">
      <SiteHeader />
      <main class="flex-1">
        <RouterView v-slot="{ Component }">
          <Transition name="page" mode="out-in">
            <component :is="Component" :key="$route.path" />
          </Transition>
        </RouterView>
      </main>
      <SiteFooter />
    </el-config-provider>
  </div>
</template>
