# boxiaolanya2008 · 个人博客

> [!NOTE]
> 这是一个纯 HTML + Markdown 的个人博客，没有后端，直接部署在 GitHub Pages 上。

## 功能

- 首页自动读取仓库 `posts/` 目录中的 Markdown 文件
- 文章详情页支持常用 Markdown 语法
- 桌面端固定侧边导航，移动端抽屉菜单
- 深浅色主题切换
- 项目区展示 GitHub 公开仓库
- 不需要 Node.js、数据库或构建步骤

## 快速开始

直接用浏览器打开 `index.html` 即可本地预览。部署时使用 GitHub Pages Actions，工作流会把仓库根目录发布到 Pages。

## 写文章

1. 在 `posts/` 目录新建 Markdown 文件，例如 `my-post.md`
2. 文件开头按 [posts/README.md](posts/README.md) 中的格式写 Front Matter
3. 推送 `main` 分支，首页会自动显示新文章

示例文章：

- [posts/hello-world.md](posts/hello-world.md)
- [posts/git-pages-guide.md](posts/git-pages-guide.md)

## 目录结构

```text
index.html      首页
post.html       文章详情页
app.js          首页逻辑与侧边导航
post.js         文章渲染与侧边导航
styles.css      首页样式
post.css        文章页样式
posts/          Markdown 文章目录
.github/        GitHub Pages 部署工作流
```

## 贡献

欢迎提 Issue 和 PR，动手前先看一下 [CONTRIBUTING.md](CONTRIBUTING.md) 和[行为准则](CODE_OF_CONDUCT.md)。

## License

[GPL-3.0](LICENSE)
