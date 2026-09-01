import express from 'express'
import bcrypt from 'bcryptjs'
import jwt from 'jsonwebtoken'
import { db } from './db.js'

const router = express.Router()

/* 生产环境务必通过环境变量提供密钥；本地开发使用下方默认值即可。 */
const JWT_SECRET = process.env.JWT_SECRET || 'dev-only-secret-change-me'
const TOKEN_TTL = '7d'

const signToken = (user) => jwt.sign({ id: user.id, username: user.username }, JWT_SECRET, { expiresIn: TOKEN_TTL })
const auth = (req, res, next) => {
  const header = req.headers.authorization
  if (!header?.startsWith('Bearer ')) return res.status(401).json({ error: '未登录' })
  try {
    req.user = jwt.verify(header.slice(7), JWT_SECRET)
    next()
  } catch {
    res.status(401).json({ error: '登录已过期，请重新登录' })
  }
}

router.post('/register', (req, res) => {
  const { username, password } = req.body ?? {}
  if (typeof username !== 'string' || !/^[a-zA-Z0-9_-]{3,20}$/.test(username))
    return res.status(400).json({ error: '用户名需为 3-20 位字母、数字、下划线或短横线' })
  if (typeof password !== 'string' || password.length < 6)
    return res.status(400).json({ error: '密码至少 6 位' })

  const exists = db.prepare('SELECT id FROM users WHERE username = ?').get(username)
  if (exists) return res.status(409).json({ error: '用户名已被占用' })

  const hash = bcrypt.hashSync(password, 10)
  const info = db.prepare('INSERT INTO users (username, password) VALUES (?, ?)').run(username, hash)
  res.status(201).json({ token: signToken({ id: info.lastInsertRowid, username }) })
})

router.post('/login', (req, res) => {
  const { username, password } = req.body ?? {}
  const user = typeof username === 'string' ? db.prepare('SELECT * FROM users WHERE username = ?').get(username) : undefined
  if (!user || !bcrypt.compareSync(String(password ?? ''), user.password))
    return res.status(401).json({ error: '用户名或密码错误' })
  res.json({ token: signToken(user) })
})

router.get('/me', auth, (req, res) => res.json({ username: req.user.username }))

export default router
export { auth }
