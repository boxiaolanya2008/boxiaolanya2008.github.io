# 贡献指南

感谢你对本项目的关注！

> [!NOTE]
> 提交 PR 前请确认以下检查项全部通过。

## 开发流程

1. Fork 仓库并克隆到本地
2. 新建分支：`git checkout -b feat/your-feature`
3. 修改 HTML、CSS、JS 或 `posts/` 下的 Markdown 文章
4. 提交修改：`git commit -m "feat: 描述你的改动"`
5. 推送并开 PR

## 提交前自检

- [ ] 直接在浏览器打开 `index.html` 或启动本地静态服务器检查页面
- [ ] 浅色 / 深色两套主题下均正常显示
- [ ] 桌面端侧边导航和移动端抽屉菜单均可用
- [ ] 新增或修改文章后，`posts/` 中的 Front Matter 和 Markdown 格式正确
- [ ] 不引入装饰性注释，只写必要的「为什么」注释

## 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)：

- `feat:` 新功能
- `fix:` 修复缺陷
- `docs:` 文档变更
- `style:` 样式调整（不影响逻辑）
- `refactor:` 重构
