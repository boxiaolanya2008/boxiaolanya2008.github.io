import Database from 'better-sqlite3'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'
import { mkdirSync } from 'node:fs'

/* SQLite 数据库文件（本地持久化），首次运行自动建目录与表。 */
const root = join(dirname(fileURLToPath(import.meta.url)), '..')
const dataDir = join(root, 'data')
mkdirSync(dataDir, { recursive: true })
export const db = new Database(join(dataDir, 'blog.db'))
db.pragma('journal_mode = WAL')

db.exec(`
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  title_en TEXT,
  date TEXT NOT NULL,
  summary TEXT NOT NULL,
  summary_en TEXT,
  content TEXT NOT NULL,
  review_subject TEXT,
  review_subject_en TEXT,
  review_rating INTEGER,
  review_summary TEXT,
  review_summary_en TEXT,
  review_pros TEXT,
  review_cons TEXT,
  review_verdict TEXT,
  review_verdict_en TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
`)

/* 旧数据库只有基础字段时补 Review 列，避免已有 data/blog.db 无法写入评测。 */
const postColumns = db.prepare("PRAGMA table_info(posts)").all().map((c) => c.name)
for (const col of ['review_subject', 'review_subject_en', 'review_rating', 'review_summary', 'review_summary_en', 'review_pros', 'review_cons', 'review_verdict', 'review_verdict_en']) {
  if (!postColumns.includes(col)) db.exec(`ALTER TABLE posts ADD COLUMN ${col} TEXT`)
}
