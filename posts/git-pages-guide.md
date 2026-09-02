---
title: 用 GitHub Pages 部署纯 HTML 博客
date: 2026-09-01
summary: 记录这个博客改为静态 Markdown 模式后的部署方式。
tags:
  - GitHub Pages
  - 部署
draft: false
---

GitHub Pages 只能托管静态文件，所以纯 HTML 版本不再依赖后端。

## 发布流程

1. 在 `posts/` 新建或修改 Markdown 文件
2. 推送 `main` 分支
3. GitHub Pages 部署完成后自动生效

## 常见问题

- 文章列表加载失败时，页面会显示错误提示
- 文章格式错误时，默认使用文件名作为标题
- 不需要数据库、登录或构建命令

## 当前页面结构

- 桌面端：固定左侧侧边导航
- 移动端：顶部菜单按钮打开抽屉导航
- 文章与项目列表通过 GitHub API 动态读取
