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
  title: string
  date: string
  summary: string
  tags: string[]
  url?: string
}

export interface TimelineNode {
  date: string
  title: string
  titleEn: string
  detail: string
  detailEn: string
}

export interface Progress {
  date: string
  text: string
  textEn: string
  tag: string
}

export const username = 'boxiaolanya2008'

export const profile = {
  name: username,
  tagline: '喜欢折腾前端与工具链的开发者',
  avatar: '/avatar.svg',
  socials: [
    { name: 'GitHub', url: 'https://github.com/boxiaolanya2008', icon: 'github' },
    { name: 'Bilibili', url: 'https://space.bilibili.com/432258335', icon: 'bilibili' },
    { name: 'Email', url: 'mailto:3520687734@qq.com', icon: 'mail' },
  ] as SocialLink[],
}

/* 首页「最近进展」：展示近几天的动态，按日期倒序；文本字段带中英两份 */
export const recentProgress: Progress[] = [
  { date: '2026-09-01', text: '主页上线，部署至 Cloudflare Pages', textEn: 'Homepage launched, deployed on Cloudflare Pages', tag: '发布' },
  { date: '2026-08-31', text: '液态玻璃组件与胶囊导航栏联调完成', textEn: 'Liquid glass components and capsule nav integrated', tag: '前端' },
  { date: '2026-08-29', text: '接入 Lottie 动画与深色主题', textEn: 'Integrated Lottie animations and dark theme', tag: '前端' },
  { date: '2026-08-28', text: '写完 Cloudflare Pages 部署流程笔记', textEn: 'Finished notes on the Cloudflare Pages deploy flow', tag: '博客' },
]

export const projects: Project[] = [
  {
    name: '液态玻璃主页',
    description: 'Vue3 + Tailwind 打造的液态玻璃风格个人主页，部署在 Cloudflare Pages。',
    descriptionEn: 'A liquid-glass style personal homepage built with Vue3 + Tailwind, deployed on Cloudflare Pages.',
    tags: ['Vue3', 'Tailwind', 'Cloudflare'],
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

export const posts: Post[] = [
  {
    title: '把主页部署到 Cloudflare Pages 的完整流程',
    date: '2026-08-28',
    summary: '从构建命令到自定义域名，记录一次完整的静态站点部署过程。',
    tags: ['部署', 'Cloudflare'],
  },
  {
    title: '用 CSS 复刻 iOS 26 液态玻璃效果',
    date: '2026-08-15',
    summary: 'backdrop-filter 与 SVG 滤镜的组合拳，低成本的玻璃质感方案。',
    tags: ['CSS', '前端'],
  },
  {
    title: 'Vue3 组合式 API 上手笔记',
    date: '2026-07-20',
    summary: 'ref 与 reactive 的选择、composable 的拆分时机，以及踩过的响应式坑。',
    tags: ['Vue3', '前端'],
  },
  {
    title: '我的 2026 上半年开发环境盘点',
    date: '2026-07-05',
    summary: '终端、编辑器、字体与常用 CLI 工具的当前配置一览。',
    tags: ['工具', '随笔'],
  },
]

export const timeline: TimelineNode[] = [
  { date: '2026-09-01', title: '主页上线', titleEn: 'Homepage launched', detail: 'Vue3 液态玻璃主页 v1.0 发布，部署至 Cloudflare Pages。', detailEn: 'Liquid glass homepage v1.0 released, deployed on Cloudflare Pages.' },
  { date: '2026-08-15', title: '液态玻璃方案定稿', titleEn: 'Liquid glass approach finalized', detail: '确定用 backdrop-filter + SVG 滤镜复刻玻璃质感，弃用截图方案。', detailEn: 'Settled on backdrop-filter + SVG filters for the glass look, dropping the screenshot approach.' },
  { date: '2026-07-01', title: '入坑 Vue3 生态', titleEn: 'Diving into the Vue3 ecosystem', detail: '系统学习 Composition API，写下第一个组件。', detailEn: 'Studied the Composition API systematically and wrote my first component.' },
  { date: '2025-12-01', title: '注册 GitHub', titleEn: 'Joined GitHub', detail: '开源之旅从这里开始。', detailEn: 'The open source journey starts here.' },
]
