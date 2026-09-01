/* Markdown 渲染端到端验证：创建一篇含 GFM + 警示块 + 代码高亮的文章，检查 API 返回 */
const BASE = 'http://localhost:3000/api'

async function req(path, { method = 'GET', token, body } = {}) {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(body ? { 'Content-Type': 'application/json' } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  })
  const text = await res.text()
  let data
  try {
    data = JSON.parse(text)
  } catch {
    data = text
  }
  return { status: res.status, data }
}

/* 登录 tester（先前注册过） */
const login = await req('/auth/login', { method: 'POST', body: { username: 'tester', password: 'secret123' } })
if (login.status !== 200) {
  console.log('❌ 无法登录 tester（可能账号不存在，先注册）:', login.status, JSON.stringify(login.data))
  const reg = await req('/auth/register', { method: 'POST', body: { username: 'tester', password: 'secret123' } })
  console.log('注册结果:', reg.status)
}
const token = (await req('/auth/login', { method: 'POST', body: { username: 'tester', password: 'secret123' } })).data.token

/* 一篇覆盖所有 Markdown 特性的文章 */
const md = `# 标题一

这是一个**加粗**、*斜体*、~~删除线~~和\`行内代码\`的段落。

## 列表

- 项目一
- 项目二
  - 子项目

1. 第一
2. 第二

## 警示块

> [!NOTE]
> 这是一条 Note 提示。

> [!TIP]
> 这是一条 **Tip** 提示。

> [!WARNING]
> 这是一条 Warning 提示。

> [!CAUTION]
> 这是一条 Caution 提示。

> [!IMPORTANT]
> 这是一条 Important 提示。

## 代码高亮

\`\`\`ts
interface User {
  id: number
  name: string
}

const u: User = { id: 1, name: 'demo' }
\`\`\`

## 表格

| 名称 | 说明 |
| ---- | ---- |
| Vue  | 前端框架 |
| Vite | 构建工具 |

## 任务列表

- [x] 已完成
- [ ] 未完成

---

引用测试：

> 这是一段普通引用，不是警示块。
`

const created = await req('/posts', {
  method: 'POST',
  token,
  body: { title: 'Markdown 渲染测试', content: md, summary: '测试 GFM、警示块与代码高亮。' },
})
console.log('创建文章:', created.status, JSON.stringify(created.data))
const slug = created.data.slug

const detail = await req(`/posts/${encodeURIComponent(slug)}`)
console.log('详情:', detail.status, '内容长度:', detail.data.content?.length)
const ok = detail.status === 200 && detail.data.content.includes('> [!NOTE]') && detail.data.content.includes('```ts')
console.log(ok ? '✅ 文章内容完整' : '❌ 内容缺失')

console.log('SLUG=' + slug)
