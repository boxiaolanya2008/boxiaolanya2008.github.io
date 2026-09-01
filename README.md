# boxiaolanya2008 · 个人博客

> [!NOTE]
> 这是我用 Vue3 搭的极简个人博客：排版干净、配色克制、浅深双主题跟随系统、支持中英双语，部署在 GitHub Pages 上。

## 功能特性

- **博客**：文章列表 + 标签筛选 + 按年份归档，每篇文章有独立详情页
- **用户系统**：本地注册 / 登录（SQLite 数据库 + JWT），登录后可发布新文章、删除自己的旧文章
- **极简设计**：大留白、细边框、单一强调色，不堆多余的装饰
- **主题**：浅色 / 深色两套配色，默认跟随系统，可手动切换并记住你的选择
- **多语言**：中英双语，一键切换，默认跟随浏览器语言，选择会持久化
- **响应式**：桌面端是顶部导航，移动端收起成折叠菜单，各种屏幕都能看
- **动画**：页面切换淡入、滚动浮现、卡片微交互，也尊重系统"减弱动效"的偏好
- **项目**：实时拉取 GitHub 公开仓库展示，接口挂了就回退到本地数据
- **字体**：自托管 Inter 可变字体，跨平台渲染一致，不会莫名乱掉

## 快速开始

> [!IMPORTANT]
> 需要 Node.js 20.19+ 或 22.12+

```bash
npm install
npm run dev      # 本地开发 http://localhost:5173
npm run build    # 构建，产物在 dist/
npm run preview  # 本地预览构建产物
```

## 本地完整模式（登录 / 发布 / 删除）

> [!IMPORTANT]
> 需要 Node.js 20.19+ 或 22.12+

前后端一起跑（Express 后端 + SQLite + Vite 前端，支持热更新）：

```bash
npm run dev:full   # 后端 http://localhost:3000 + 前端 http://localhost:5173
```

前端开发服务器通过 Vite 代理把 `/api` 转发到后端，登录、发文章、删文章都会写入本地的 `data/blog.db`。

> [!NOTE]
> - 用户注册后密码以 bcrypt 哈希存储，登录返回 JWT（默认 7 天有效，可通过环境变量 `JWT_SECRET` 覆盖密钥）。
> - 数据库文件在 `data/blog.db`（已加入 `.gitignore`，不会提交到仓库）。
> - 纯静态部署（GitHub Pages）时没有后端，文章列表自动退回内置的静态文章，登录入口隐藏，页面行为与之前一致。

## 部署到 GitHub Pages

仓库推到 `main` 分支后，`.github/workflows/deploy.yml` 会自动构建并发布。

第一次部署需要在仓库 **Settings → Pages → Source** 里选 **GitHub Actions**。

> [!TIP]
> 本站是 `*.github.io` 用户主页仓库，部署在根路径，所以 `vite.config.ts` 不用设 `base`。
> 如果哪天改成普通项目仓库（部署到 `/<repo>/`），记得加 `base: '/<repo>/'`。

### 关于 SPA 深链

GitHub Pages 是静态托管，直接访问 `/blog` 这类路径会 404。

我的做法是：在 `npm run build` 末尾用 `scripts/spa-fallback.mjs` 把 `dist/index.html` 复制成 `dist/404.html`。这样 404 时返回的是带正确资源引用的首页，由 vue-router 接管路由。

> [!WARNING]
> 别把 404 页写在 `public/404.html`。`public/` 里的文件是原样拷贝，只能写死源码路径（比如 `/src/main.ts`），但构建产物里根本没有这个文件，深链照样白屏。所以必须在 `vite build` **之后**再复制产物。

## 自定义内容

改 [src/data.ts](src/data.ts) 里的 `posts` / `projects` / `profile` / `skills` / `timeline` 就能换成你自己的内容；界面文案在 [src/i18n.ts](src/i18n.ts) 里维护中英两份。

## 贡献

欢迎提 Issue 和 PR，动手前先看一下 [CONTRIBUTING.md](CONTRIBUTING.md) 和[行为准则](CODE_OF_CONDUCT.md)。

## License

[GPL-3.0](LICENSE)
