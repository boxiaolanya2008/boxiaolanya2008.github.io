# 贡献指南

感谢你对本项目的关注！

> [!NOTE]
> 提交 PR 前请确认以下检查项全部通过。

## 开发流程

1. Fork 仓库并克隆到本地
2. 安装依赖：`npm install`
3. 启动开发服务器：`npm run dev`
4. 新建分支：`git checkout -b feat/your-feature`
5. 提交修改：`git commit -m "feat: 描述你的改动"`
6. 推送并开 PR

## 提交前自检

- [ ] `npm run build` 通过（包含 vue-tsc 类型检查）
- [ ] 浅色 / 深色两套主题下均正常显示
- [ ] 新增组件遵循项目现有风格（液态玻璃、圆角卡片、微交互）
- [ ] 不引入装饰性注释，只写必要的「为什么」注释

## 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)：

- `feat:` 新功能
- `fix:` 修复缺陷
- `docs:` 文档变更
- `style:` 样式调整（不影响逻辑）
- `refactor:` 重构
