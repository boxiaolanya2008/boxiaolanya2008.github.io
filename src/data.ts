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
    title: '博客 v2 重构完成',
    titleEn: 'Blog v2 rebuilt',
    detail: '完成 Element Plus 主题、GitHub 头像、Review 评测、CodeMirror 代码补全与实时 Markdown 预览。',
    detailEn: 'Shipped Element Plus theme, GitHub avatar, Review posts, CodeMirror autocomplete and live Markdown preview.',
  },
  {
    date: '2026-08-15',
    title: '本地写作模式落地',
    titleEn: 'Local writing mode landed',
    detail: '接入 Express + SQLite + JWT，实现注册登录、文章发布与删除。',
    detailEn: 'Added Express + SQLite + JWT for auth, publishing and deleting posts.',
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
