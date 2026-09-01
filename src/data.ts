export interface SocialLink {
  name: string
  url: string
  icon: 'github' | 'bilibili' | 'mail'
}

export interface Project {
  name: string
  description: string
  descriptionEn: string
  tags: string[]
  url?: string
  repo?: string
}

export interface Post {
  slug: string
  title: string
  titleEn?: string
  date: string
  summary: string
  summaryEn?: string
  tags: string[]
  content: string
}

export interface TimelineNode {
  date: string
  title: string
  titleEn: string
  detail: string
  detailEn: string
}

export const username = 'boxiaolanya2008'

export const profile = {
  name: username,
  avatar: '/avatar.svg',
  bio: '喜欢折腾前端与工具链的开发者',
  socials: [
    { name: 'GitHub', url: 'https://github.com/boxiaolanya2008', icon: 'github' },
    { name: 'Bilibili', url: 'https://space.bilibili.com/432258335', icon: 'bilibili' },
    { name: 'Email', url: 'mailto:3520687734@qq.com', icon: 'mail' },
  ] as SocialLink[],
}

export const skills: { label: string; level: number }[] = [
  { label: 'TypeScript', level: 4 },
  { label: 'Vue', level: 4 },
  { label: 'Node.js', level: 3 },
  { label: 'CSS / Tailwind', level: 4 },
  { label: 'React', level: 2 },
  { label: 'Rust', level: 1 },
]

export const posts: Post[] = [
  {
    slug: 'deploy-to-github-pages',
    title: '把个人主页部署到 GitHub Pages 的完整流程',
    titleEn: 'Deploying a personal site to GitHub Pages',
    date: '2026-08-28',
    summary: '从构建命令到 SPA 深链回退，记录一次完整的静态站点部署过程。',
    summaryEn: 'From build commands to SPA deep-link fallback, a complete static-site deploy walkthrough.',
    tags: ['部署', '博客'],
    content:
      'GitHub Pages 是个人主页最省心的托管方案。\n\n这次部署踩了深链的坑：直接访问 /blog 这类路径会 404。解决方式是在 vite build 之后把 dist/index.html 复制成 dist/404.html，让 404 时返回带正确资源引用的首页，由 vue-router 接管路由。\n\n关键点：不要把 404 页写在 public/ 里。public/ 下的文件是原样拷贝，里面写死的 /src/main.ts 在构建产物中根本不存在。',
  },
  {
    slug: 'liquid-glass-css',
    title: '用 CSS 复刻 iOS 液态玻璃效果',
    titleEn: 'Recreating the iOS liquid-glass look with CSS',
    date: '2026-08-15',
    summary: 'backdrop-filter 与高光描边的组合拳，低成本的玻璃质感方案。',
    summaryEn: 'backdrop-filter plus highlight strokes — a cheap way to get a glass look.',
    tags: ['CSS', '前端'],
    content:
      '液态玻璃的核心是 backdrop-filter: blur + saturate，配合内高光描边营造通透感。\n\n要点：blur 数值不宜过大（18px 左右），saturate 增强背后色彩的通透性，再加一层 inset 高光让边缘有玻璃的厚度感。\n\n注意 backdrop-filter 不支持时要有降级——用半透明背景色兜底，别让内容看不清。',
  },
  {
    slug: 'vue-composition-api',
    title: 'Vue3 组合式 API 上手笔记',
    titleEn: 'Notes on the Vue3 Composition API',
    date: '2026-07-20',
    summary: 'ref 与 reactive 的选择、composable 的拆分时机，以及踩过的响应式坑。',
    summaryEn: 'ref vs reactive, when to split composables, and reactive pitfalls I hit.',
    tags: ['Vue', '前端'],
    content:
      'ref 用于标量，reactive 用于对象，但组合式里我倾向全用 ref，配合解构不会丢失响应性。\n\ncomposable 的拆分时机：一段逻辑被两个以上组件复用，或单组件超过 150 行，就值得抽。\n\n最大的坑是 reactive 解构后丢失响应性，务必用 toRefs 或干脆全用 ref。',
  },
  {
    slug: 'dev-environment-2026',
    title: '我的 2026 上半年开发环境盘点',
    titleEn: 'My dev environment, first half of 2026',
    date: '2026-07-05',
    summary: '终端、编辑器、字体与常用 CLI 工具的当前配置一览。',
    summaryEn: 'A rundown of my current terminal, editor, fonts, and daily CLI tools.',
    tags: ['工具', '随笔'],
    content:
      '终端：Kitty + zsh，配 Starship 提示符。\n\n编辑器：Neovim + LSP，主打轻量。\n\n字体：自托管 Inter Variable，跨平台渲染一致，也解决了中文环境下的字体回退问题。',
  },
]

export const fallbackProjects: Project[] = [
  {
    name: '个人主页',
    description: 'Vue3 + Tailwind 打造的极简个人博客，部署在 GitHub Pages。',
    descriptionEn: 'A minimal personal blog built with Vue3 + Tailwind, deployed on GitHub Pages.',
    tags: ['Vue', 'Tailwind'],
    repo: 'https://github.com/boxiaolanya2008',
  },
  {
    name: '工具箱 CLI',
    description: '日常开发提效小工具合集，一键生成常用配置。',
    descriptionEn: 'A collection of daily dev productivity tools that generate common configs in one command.',
    tags: ['Node.js', 'CLI'],
    repo: 'https://github.com/boxiaolanya2008',
  },
  {
    name: '像素小画板',
    description: '浏览器里的像素画工具，支持导出与撤销。',
    descriptionEn: 'A pixel art tool in the browser with export and undo support.',
    tags: ['Canvas', '前端'],
  },
]

export const timeline: TimelineNode[] = [
  {
    date: '2026-09-01',
    title: '博客上线',
    titleEn: 'Blog launched',
    detail: '极简版个人博客 v2.0 发布，部署至 GitHub Pages。',
    detailEn: 'Minimal personal blog v2.0 released, deployed on GitHub Pages.',
  },
  {
    date: '2026-08-15',
    title: '液态玻璃方案定稿',
    titleEn: 'Liquid glass approach finalized',
    detail: '确定了玻璃质感的技术路线。',
    detailEn: 'Settled on the technical approach for the glass look.',
  },
  {
    date: '2026-07-01',
    title: '入坑 Vue3 生态',
    titleEn: 'Diving into the Vue3 ecosystem',
    detail: '系统学习 Composition API，写下第一个组件。',
    detailEn: 'Studied the Composition API systematically and wrote my first component.',
  },
  {
    date: '2025-12-01',
    title: '注册 GitHub',
    titleEn: 'Joined GitHub',
    detail: '开源之旅从这里开始。',
    detailEn: 'The open source journey starts here.',
  },
]
