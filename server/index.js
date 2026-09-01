import express from 'express'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'
import authRouter from './auth.js'
import postsRouter from './posts.js'

const app = express()
app.use(express.json())
/* Express 5 默认对路径参数做 decodeURIComponent，遇到非 UTF-8 编码的字节会直接抛 URIError（500）。
   这里放宽：解码失败时保留原始值，交由路由层处理（如 404），避免整个请求崩溃。 */
app.set('decodeURIComponent', (v) => {
  try {
    return decodeURIComponent(v)
  } catch {
    return v
  }
})

app.use('/api/auth', authRouter)
app.use('/api/posts', postsRouter)

/* 生产模式下由 Express 托管构建产物（此时不再只是静态站）。 */
const root = join(dirname(fileURLToPath(import.meta.url)), '..')
const dist = join(root, 'dist')
app.use(express.static(dist))
app.get('/{*splat}', (req, res) => {
  if (req.path.startsWith('/api/')) return res.status(404).json({ error: 'Not found' })
  res.sendFile(join(dist, 'index.html'))
})

const PORT = process.env.PORT || 3000
app.listen(PORT, () => console.log(`[server] http://localhost:${PORT}`))
