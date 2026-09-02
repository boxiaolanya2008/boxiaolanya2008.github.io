# posts 文章目录

这个目录里的 Markdown 文件会被首页自动读取并展示。

## 文件命名

文件名会作为访问时的标识，建议使用英文小写和短横线，例如：

- `hello-world.md`
- `git-pages-guide.md`

## Front Matter 格式

每个文件开头使用 YAML Front Matter，至少包含 `title` 和 `date`：

```markdown
---
title: 文章标题
date: 2026-09-02
summary: 文章摘要
tags:
  - 标签一
  - 标签二
draft: false
---

这里是正文，使用 Markdown 编写。
```

## 字段说明

- `title`：文章标题，必填
- `date`：发布日期，建议 `YYYY-MM-DD`
- `summary`：列表页摘要，可选
- `tags`：标签列表，可选
- `draft`：设为 `true` 时不会显示在列表中，可选

## 支持的 Markdown

首页详情页支持常见的 GFM 语法：标题、段落、列表、引用、表格、任务列表、行内代码、代码块、图片和链接。
