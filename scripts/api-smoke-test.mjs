/* 端到端 API 冒烟测试：注册 -> 登录 -> 发文章 -> 列表 -> 详情 -> 删除 */
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

const username = `user_${Date.now().toString(36)}`
let pass = 0
let fail = 0
const check = (name, cond, extra = '') => {
  if (cond) {
    pass++
    console.log(`  ✅ ${name}`)
  } else {
    fail++
    console.log(`  ❌ ${name} ${extra}`)
  }
}

console.log('== 注册 ==')
const reg = await req('/auth/register', { method: 'POST', body: { username, password: 'secret123' } })
check('注册返回 token', reg.status === 201 && typeof reg.data.token === 'string', JSON.stringify(reg.data))

console.log('== 重复注册 ==')
const dup = await req('/auth/register', { method: 'POST', body: { username, password: 'secret123' } })
check('重复注册 409', dup.status === 409, String(dup.status))

console.log('== 登录 ==')
const login = await req('/auth/login', { method: 'POST', body: { username, password: 'secret123' } })
check('登录返回 token', login.status === 200 && typeof login.data.token === 'string', JSON.stringify(login.data))
const token = login.data.token

console.log('== 发中文文章 ==')
const title = '中文标题测试'
const created = await req('/posts', {
  method: 'POST',
  token,
  body: { title, content: '第一段。\n\n第二段。', summary: '摘要' },
})
check('发布成功返回 slug', created.status === 201 && typeof created.data.slug === 'string', JSON.stringify(created.data))
const slug = created.data.slug
check('中文标题生成中文 slug', /[\u4e00-\u9fa5]/.test(slug), slug)

console.log('== 列表 ==')
const list = await req('/posts')
const found = list.data.find((p) => p.slug === slug)
check('列表包含新文章', list.status === 200 && !!found, JSON.stringify(list.data))
check('列表字段完整 (db=true)', found?.db === true && found.title === title, JSON.stringify(found))

console.log('== 详情（含中文 slug）==')
const detail = await req(`/posts/${encodeURIComponent(slug)}`)
check('详情返回正文', detail.status === 200 && detail.data.content.includes('第一段'), JSON.stringify(detail.data))

console.log('== 未授权访问 ==')
const noAuth = await req('/posts', { method: 'POST', body: { title: 'x', content: 'y' } })
check('未登录 401', noAuth.status === 401, String(noAuth.status))

console.log('== 删除 ==')
const del = await req(`/posts/${encodeURIComponent(slug)}`, { method: 'DELETE', token })
check('删除成功', del.status === 200 && del.data.ok === true, JSON.stringify(del.data))
const after = await req('/posts')
check('删除后列表不含该文章', !after.data.find((p) => p.slug === slug), JSON.stringify(after.data))

console.log('== 删除不存在文章 ==')
const del2 = await req('/posts/nonexistent-slug-xyz', { method: 'DELETE', token })
check('404', del2.status === 404, String(del2.status))

console.log(`\n结果: ${pass} 通过, ${fail} 失败`)
process.exit(fail ? 1 : 0)
