# boxiaolanya2008 · 个人主页

> [!NOTE]
> Vue3 液态玻璃（Liquid Glass）风格个人主页，胶囊导航栏 + 多页面路由，浅色/深色主题跟随系统，部署于 Cloudflare Pages。

## 功能特性

- 🪟 **液态玻璃**：`backdrop-filter` + 高光描边，背后渐变光斑流动折射
- 💊 **胶囊导航栏**：固定顶部，vue-router 多页面切换，无缝过渡，窄屏自动收缩为纯图标
- 🌗 **主题**：浅色 / 深色两套配色，默认跟随系统，可手动切换并持久化
- 🌐 **多语言**：vue-i18n 中英双语，一键切换，跟随浏览器语言并持久化
- 🧊 **Three.js 3D 背景**：TresJS 渲染的玻璃立方体场景，独立 chunk 懒加载，不阻塞首屏
- 🧩 **必备组件**：TimeLine 时间线、卡片微交互（悬停浮起 + 投影加深）、空状态、骨架屏
- ⚡ **首页最近进展**：近几天的动态以玻璃卡片时间列表呈现
- 🎞️ **动画**：Lottie JSON 配置驱动 + 全套动态 SVG 图标 + 方块粒子背景
- ✍️ **字体**：自托管 Inter 可变字体，跨平台文字渲染一致

## 快速开始

> [!IMPORTANT]
> 需要 Node.js 20.19+ 或 22.12+

```bash
npm install
npm run dev      # 本地开发 http://localhost:5173
npm run build    # 构建，产物在 dist/
npm run preview  # 本地预览构建产物
```

## 部署到 Cloudflare Pages

> [!TIP]
> 方式一（推荐）：仓库推到 GitHub 后，在 Cloudflare Dashboard → Workers & Pages → 创建 Pages 项目 → 连接仓库
> - 构建命令：`npm run build`
> - 输出目录：`dist`

方式二：本地直接部署

```bash
npx wrangler pages deploy dist
```

## 自定义内容

修改 [src/data.ts](src/data.ts) 中的 `profile` / `recentProgress` / `projects` / `posts` / `timeline` 即可替换为你的个人信息；界面文案在 [src/i18n.ts](src/i18n.ts) 中维护中英两份；动画 JSON 放在 `public/lottie/`。

## 贡献

欢迎 Issue 与 PR，请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 与[行为准则](CODE_OF_CONDUCT.md)。

## License

[GPL-3.0](LICENSE)
