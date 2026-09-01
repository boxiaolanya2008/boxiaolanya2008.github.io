<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { User, Lock, Key } from '@element-plus/icons-vue'
import { authApi, tokenStore } from '../api'
import { setUser } from '../store'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()

const mode = ref<'login' | 'register'>('login')
const username = ref('')
const password = ref('')
const confirm = ref('')
const error = ref('')
const loading = ref(false)

const toggleMode = () => {
  mode.value = mode.value === 'login' ? 'register' : 'login'
  error.value = ''
}

const submit = async () => {
  error.value = ''
  if (mode.value === 'register' && password.value !== confirm.value) {
    error.value = t('auth.passwordsMismatch')
    return
  }
  loading.value = true
  try {
    const res =
      mode.value === 'login'
        ? await authApi.login(username.value, password.value)
        : await authApi.register(username.value, password.value)
    tokenStore.set(res.token)
    setUser(username.value)
    ElMessage.success(mode.value === 'login' ? t('auth.login') : t('auth.register'))
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/'
    router.replace(redirect)
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="mx-auto flex max-w-md flex-col px-5 py-16 sm:px-8">
    <div class="page-panel p-6 sm:p-8">
      <div class="mb-8 text-center">
        <el-icon :size="34" class="text-[var(--accent)]"><Key /></el-icon>
        <h1 class="mt-3 text-2xl font-bold tracking-tight text-[var(--fg)]">
          {{ mode === 'login' ? t('auth.login') : t('auth.register') }}
        </h1>
      </div>

      <el-form label-position="top" @submit.prevent="submit">
        <el-form-item :label="t('auth.username')">
          <el-input v-model="username" :prefix-icon="User" maxlength="20" autocomplete="username" />
        </el-form-item>
        <el-form-item :label="t('auth.password')">
          <el-input v-model="password" :prefix-icon="Lock" type="password" show-password autocomplete="current-password" />
        </el-form-item>
        <el-form-item v-if="mode === 'register'" :label="t('auth.confirmPassword')">
          <el-input v-model="confirm" :prefix-icon="Lock" type="password" show-password autocomplete="new-password" />
        </el-form-item>

        <p v-if="error" class="mb-3 text-sm text-[var(--caution-fg)]">{{ error }}</p>

        <el-button type="primary" class="w-full" :loading="loading" @click="submit">
          {{ mode === 'login' ? t('auth.submit') : t('auth.register') }}
        </el-button>
      </el-form>

      <el-divider />
      <el-button link class="w-full" @click="toggleMode">
        {{ mode === 'login' ? t('auth.noAccount') : t('auth.hasAccount') }}
      </el-button>
    </div>
  </div>
</template>
