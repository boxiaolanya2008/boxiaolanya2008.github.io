import { computed, ref } from 'vue'
import { authApi, tokenStore } from './api'

const username = ref('')
const ready = ref(false)

/* 应用启动时恢复登录态 */
export async function restoreSession() {
  if (!tokenStore.get()) {
    ready.value = true
    return
  }
  try {
    const me = await authApi.me()
    username.value = me.username
  } catch {
    tokenStore.clear()
  }
  ready.value = true
}

export function setUser(name: string) {
  username.value = name
}

export function logout() {
  tokenStore.clear()
  username.value = ''
}

export const isLoggedIn = computed(() => username.value !== '')
export const currentUser = computed(() => username.value)
export const sessionReady = computed(() => ready.value)
