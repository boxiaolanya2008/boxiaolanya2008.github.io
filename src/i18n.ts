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
      site: {
        name: 'boxiaolanya2008',
        tagline: '一个喜欢折腾前端与工具链的开发者',
      },
      nav: {
        home: '首页',
        blog: '博客',
        projects: '项目',
        about: '关于',
      },
      home: {
        hello: '你好，我是',
        intro: '这里是我记录技术思考与生活随想的地方。写得不多，但每篇都认真。',
        recent: '最近文章',
        allPosts: '查看全部文章',
        follow: '找到我',
      },
      blog: {
        title: '博客',
        all: '全部',
        total: '共 {n} 篇',
        readMore: '阅读全文',
        noPosts: '该标签下还没有文章',
        noPostsHint: '换个标签看看',
        years: '归档',
      },
      projects: {
        title: '项目',
        all: '全部',
        repo: '查看仓库',
        homepage: '在线预览',
        noDesc: '暂无描述',
        fallback: 'GitHub 数据暂时拉取不到，以下为本地项目列表。',
        noRepos: '该标签下没有项目',
        noReposHint: '换个筛选条件',
        stars: '星标',
      },
      about: {
        title: '关于',
        bio: '我是 boxiaolanya2008，一名专注前端与工具链开发的工程师。这个博客用来沉淀日常的学习与踩坑记录。',
        skills: '常用技术',
        timeline: '时间线',
        contact: '联系我',
      },
      theme: {
        toDark: '切换到深色模式',
        toLight: '切换到浅色模式',
      },
      lang: {
        label: 'EN',
        aria: '切换语言',
      },
      footer: '用 Vue3 构建 · 部署于 GitHub Pages',
    },
    en: {
      site: {
        name: 'boxiaolanya2008',
        tagline: 'A developer who loves tinkering with frontend & tooling',
      },
      nav: {
        home: 'Home',
        blog: 'Blog',
        projects: 'Projects',
        about: 'About',
      },
      home: {
        hello: "Hi, I'm",
        intro: 'A place where I write down technical thoughts and daily musings. Few posts, but each one is written with care.',
        recent: 'Recent Posts',
        allPosts: 'View all posts',
        follow: 'Find me',
      },
      blog: {
        title: 'Blog',
        all: 'All',
        total: '{n} posts',
        readMore: 'Read more',
        noPosts: 'No posts under this tag yet',
        noPostsHint: 'Try another tag',
        years: 'Archive',
      },
      projects: {
        title: 'Projects',
        all: 'All',
        repo: 'View repo',
        homepage: 'Live demo',
        noDesc: 'No description yet',
        fallback: 'GitHub data unavailable right now, showing local projects.',
        noRepos: 'No projects under this filter',
        noReposHint: 'Try another filter',
        stars: 'stars',
      },
      about: {
        title: 'About',
        bio: "I'm boxiaolanya2008, an engineer focused on frontend and tooling. This blog is where I document daily learning and debugging notes.",
        skills: 'Skills',
        timeline: 'Timeline',
        contact: 'Contact',
      },
      theme: {
        toDark: 'Switch to dark mode',
        toLight: 'Switch to light mode',
      },
      lang: {
        label: '中文',
        aria: 'Switch language',
      },
      footer: 'Built with Vue3 · Deployed on GitHub Pages',
    },
  },
})
