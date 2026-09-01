import express from 'express'
import { db } from './db.js'
import { auth } from './auth.js'

const router = express.Router()

const splitLines = (value) =>
  typeof value === 'string' ? value.split('\n').map((s) => s.trim()).filter(Boolean) : undefined

/* 数据库文章 = 本地可写数据源；返回给前端的结构带 content 全文与 db 标记。 */
const toPost = (row) => ({
  slug: row.slug,
  title: row.title,
  titleEn: row.title_en,
  date: row.date,
  summary: row.summary,
  summaryEn: row.summary_en,
  content: row.content,
  review:
    row.review_subject || row.review_rating != null
      ? {
          subject: row.review_subject ?? row.title,
          subjectEn: row.review_subject_en,
          rating: Number(row.review_rating) || 0,
          summary: row.review_summary,
          summaryEn: row.review_summary_en,
          pros: splitLines(row.review_pros),
          cons: splitLines(row.review_cons),
          verdict: row.review_verdict,
          verdictEn: row.review_verdict_en,
        }
      : null,
  db: true,
})

router.get('/', (req, res) => {
  const rows = db.prepare('SELECT * FROM posts ORDER BY date DESC, id DESC').all()
  res.json(rows.map(toPost))
})

router.get('/:slug', (req, res) => {
  const row = db.prepare('SELECT * FROM posts WHERE slug = ?').get(req.params.slug)
  if (!row) return res.status(404).json({ error: '文章不存在' })
  res.json(toPost(row))
})

const slugify = (s) =>
  String(s)
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 80) || 'post'

router.post('/', auth, (req, res) => {
  const { title, titleEn, summary, summaryEn, content, review } = req.body ?? {}
  if (typeof title !== 'string' || !title.trim()) return res.status(400).json({ error: '标题不能为空' })
  if (typeof content !== 'string' || !content.trim()) return res.status(400).json({ error: '正文不能为空' })

  const date = new Date().toISOString().slice(0, 10)
  let slug = slugify(title)
  /* 撞 slug 时追加短随机后缀，避免覆盖既有文章 */
  while (db.prepare('SELECT id FROM posts WHERE slug = ?').get(slug)) {
    slug = `${slugify(title)}-${Math.random().toString(36).slice(2, 6)}`
  }
  const r = review && typeof review === 'object' ? review : {}
  const pros = Array.isArray(r.pros) ? r.pros.filter(Boolean).join('\n') : null
  const cons = Array.isArray(r.cons) ? r.cons.filter(Boolean).join('\n') : null
  db.prepare(
    `INSERT INTO posts (
      slug, title, title_en, date, summary, summary_en, content,
      review_subject, review_subject_en, review_rating, review_summary, review_summary_en,
      review_pros, review_cons, review_verdict, review_verdict_en
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
  ).run(
    slug,
    title.trim(),
    titleEn ?? null,
    date,
    (summary ?? title).trim(),
    summaryEn ?? null,
    content.trim(),
    r.subject || null,
    r.subjectEn ?? null,
    Number.isFinite(Number(r.rating)) ? Math.max(0, Math.min(10, Number(r.rating))) : null,
    r.summary ?? null,
    r.summaryEn ?? null,
    pros,
    cons,
    r.verdict ?? null,
    r.verdictEn ?? null,
  )
  res.status(201).json({ slug })
})

router.delete('/:slug', auth, (req, res) => {
  const info = db.prepare('DELETE FROM posts WHERE slug = ?').run(req.params.slug)
  if (info.changes === 0) return res.status(404).json({ error: '文章不存在' })
  res.json({ ok: true })
})

export default router
