const API_BASE = import.meta.env.VITE_API_BASE ?? '/api'

/* 简单的 token 持久化（仅 localStorage，够本地使用；Cookie 方案另需 httpOnly 后端） */
export const tokenStore = {
  get: () => localStorage.getItem('token'),
  set: (t: string) => localStorage.setItem('token', t),
  clear: () => localStorage.removeItem('token'),
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = { ...(options.headers as Record<string, string>) }
  const token = tokenStore.get()
  if (token) headers.Authorization = `Bearer ${token}`
  if (options.body && typeof options.body === 'string') headers['Content-Type'] = 'application/json'

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error((data as { error?: string }).error ?? `请求失败 (${res.status})`)
  return data as T
}

export const authApi = {
  register: (username: string, password: string) =>
    request<{ token: string }>('/auth/register', { method: 'POST', body: JSON.stringify({ username, password }) }),
  login: (username: string, password: string) =>
    request<{ token: string }>('/auth/login', { method: 'POST', body: JSON.stringify({ username, password }) }),
  me: () => request<{ username: string }>('/auth/me'),
}

export interface ReviewMeta {
  subject: string
  subjectEn?: string | null
  rating: number
  summary?: string | null
  summaryEn?: string | null
  pros?: string[]
  cons?: string[]
  verdict?: string | null
  verdictEn?: string | null
}

export interface DbPost {
  slug: string
  title: string
  titleEn?: string | null
  date: string
  summary: string
  summaryEn?: string | null
  content: string
  tags?: string[]
  review?: ReviewMeta | null
  db: true
}

/* 统一的文章类型：数据库文章（tags 可选） */
export type Post = DbPost

export const postsApi = {
  list: () => request<DbPost[]>('/posts'),
  create: (body: {
    title: string
    titleEn?: string
    summary?: string
    summaryEn?: string
    content: string
    review?: ReviewMeta
  }) => request<{ slug: string }>('/posts', { method: 'POST', body: JSON.stringify(body) }),
  remove: (slug: string) => request<{ ok: true }>(`/posts/${slug}`, { method: 'DELETE' }),
}
