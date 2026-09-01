<script setup lang="ts">
import { computed } from 'vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { HomeFilled, Reading, Grid, User, EditPen, SwitchButton, Menu, Close } from '@element-plus/icons-vue'
import ThemeToggle from './ThemeToggle.vue'
import LanguageToggle from './LanguageToggle.vue'
import { isLoggedIn, currentUser, logout } from '../store'
import { username, profile } from '../data'

const items = [
  { path: '/', label: 'nav.home', icon: HomeFilled },
  { path: '/blog', label: 'nav.blog', icon: Reading },
  { path: '/projects', label: 'nav.projects', icon: Grid },
  { path: '/about', label: 'nav.about', icon: User },
] as const

const route = useRouter()
const routePath = computed(() => route.currentRoute.value.path)
const { t } = useI18n()
const open = ref(false)
const isActive = (path: string) =>
  path === '/' ? routePath.value === '/' : routePath.value.startsWith(path)
const isLogged = computed(() => isLoggedIn.value)
const avatar = computed(() => `https://github.com/${username}.png?size=160`)

function handleLogout() {
  logout()
  if (routePath.value === '/write') route.push('/')
}
</script>

<template>
  <header class="site-nav sticky top-0 z-50">
    <div class="mx-auto flex h-16 max-w-6xl items-center justify-between gap-4 px-5 sm:px-8">
      <RouterLink to="/" class="flex items-center gap-3 text-sm font-semibold text-[var(--fg)]">
        <img :src="avatar" :alt="profile.name" class="h-8 w-8 rounded-full border border-[var(--border)] object-cover" />
        <span class="hidden sm:inline">{{ t('site.name') }}</span>
      </RouterLink>

      <nav class="hidden items-center gap-1 md:flex" aria-label="Main">
        <RouterLink
          v-for="item in items"
          :key="item.path"
          :to="item.path"
          class="nav-link"
          :class="{ active: isActive(item.path) }"
        >
          <el-icon :size="16"><component :is="item.icon" /></el-icon>
          <span>{{ t(item.label) }}</span>
        </RouterLink>
      </nav>

      <div class="flex items-center gap-1.5">
        <template v-if="isLogged">
          <el-tooltip :content="t('editor.new')" placement="bottom">
            <RouterLink to="/write" class="header-icon-button">
              <el-icon :size="17"><EditPen /></el-icon>
            </RouterLink>
          </el-tooltip>
          <el-tooltip :content="t('auth.loggedInAs', { name: currentUser })" placement="bottom">
            <button class="header-icon-button" @click="handleLogout">
              <el-icon :size="17"><SwitchButton /></el-icon>
            </button>
          </el-tooltip>
        </template>
        <RouterLink v-else to="/login" class="nav-cta">
          {{ t('auth.login') }}
        </RouterLink>

        <ThemeToggle />
        <LanguageToggle />
        <button class="header-icon-button md:hidden" aria-label="Menu" @click="open = !open">
          <el-icon :size="19"><Menu v-if="!open" /><Close v-else /></el-icon>
        </button>
      </div>
    </div>
  </header>
</template>
