import { createI18n } from 'vue-i18n'

/* 语言持久化到 localStorage，首次访问跟随浏览器语言 */
const saved = localStorage.getItem('locale')
const locale = saved ?? (navigator.language.toLowerCase().startsWith('zh') ? 'zh' : 'en')

export const i18n = createI18n({
  legacy: false,
  locale,
  fallbackLocale: 'zh',
  messages: {
    zh: {
      nav: { home: '首页', projects: '项目', blog: '博客', timeline: '时间线' },
      hero: {
        tagline: '喜欢折腾前端与工具链的开发者',
        recent: '最近进展',
      },
      tags: { 发布: '发布', 前端: '前端', 博客: '博客', 工具: '工具', 随笔: '随笔' },
      pages: {
        projects: '项目 / 作品集',
        blog: '博客 / 文章',
        timeline: '时间线',
        all: '全部',
        total: '共 {n} 篇',
        repo: '查看仓库',
        readMore: '阅读全文',
        fallback: 'GitHub 数据暂时拉取不到，以下为本地项目列表。',
        noDesc: '暂无描述',
        yearPosts: '{n} 篇',
      },
      empty: {
        posts: '该标签下还没有文章',
        repos: '该标签下没有仓库',
        postsHint: '换个标签看看吧～',
      },
      theme: { toDark: '切换到深色模式', toLight: '切换到浅色模式' },
      lang: { label: 'English', aria: '切换语言' },
      footer: 'Built with Vue3 · Deployed on Cloudflare Pages',
    },
    en: {
      nav: { home: 'Home', projects: 'Projects', blog: 'Blog', timeline: 'Timeline' },
      hero: {
        tagline: 'A developer who loves tinkering with frontend & tooling',
        recent: 'Recent Updates',
      },
      tags: { 发布: 'Release', 前端: 'Frontend', 博客: 'Blog', 工具: 'Tools', 随笔: 'Notes' },
      pages: {
        projects: 'Projects / Portfolio',
        blog: 'Blog / Posts',
        timeline: 'Timeline',
        all: 'All',
        total: '{n} posts in total',
        repo: 'View repo',
        readMore: 'Read more',
        fallback: 'GitHub data unavailable right now, showing local projects.',
        noDesc: 'No description yet',
        yearPosts: '{n} posts',
      },
      empty: {
        posts: 'No posts under this tag yet',
        repos: 'No repos under this tag',
        postsHint: 'Try another tag~',
      },
      theme: { toDark: 'Switch to dark mode', toLight: 'Switch to light mode' },
      lang: { label: '中文', aria: 'Switch language' },
      footer: 'Built with Vue3 · Deployed on Cloudflare Pages',
    },
  },
})
