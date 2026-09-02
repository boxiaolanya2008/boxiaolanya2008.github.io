const GITHUB_USER = 'boxiaolanya2008'
const GITHUB_REPO = 'boxiaolanya2008.github.io'
const GITHUB_BRANCH = 'main'
const POSTS_DIR = 'posts'

const state = {
  posts: [],
  projects: [],
  error: '',
}

const postList = document.querySelector('#post-list')
const projectList = document.querySelector('#project-list')

/* GitHub Pages 无法列出目录，这里用 GitHub API 列出 posts/ 下的 Markdown 文件。
   普通用户 API 默认每小时 60 次，页面只请求一次目录，足够日常浏览。 */
async function listPostFiles() {
  const url = `https://api.github.com/repos/${GITHUB_USER}/${GITHUB_REPO}/contents/${POSTS_DIR}?ref=${GITHUB_BRANCH}`
  const res = await fetch(url)
  if (!res.ok) throw new Error(`GitHub API ${res.status}`)
  const files = await res.json()
  if (!Array.isArray(files)) throw new Error('posts 目录格式不正确')
  return files
    .filter((file) => file.name?.toLowerCase().endsWith('.md'))
    .sort((a, b) => a.name.localeCompare(b.name))
}

async function fetchText(url) {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`请求失败 (${res.status})`)
  return res.text()
}

function parseFrontMatter(raw) {
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/)
  const meta = {}
  if (!match) return { meta, content: raw }
  for (const line of match[1].split(/\r?\n/)) {
    const pair = line.match(/^([A-Za-z_][\w-]*):\s*(.*)$/)
    if (!pair) continue
    const key = pair[1]
    const value = pair[2].trim()
    if (value.startsWith('- ')) {
      meta[key] = match[1].split(/\r?\n/).map((item) => item.trim()).filter((item) => item.startsWith('- ')).map((item) => item.replace(/^-\s*/, '').trim())
    } else if (value === 'true') {
      meta[key] = true
    } else if (value === 'false') {
      meta[key] = false
    } else {
      meta[key] = value.replace(/^["']|["']$/g, '')
    }
  }
  return { meta, content: raw.slice(match[0].length) }
}

function slugify(name) {
  return name.toLowerCase().replace(/\.md$/, '').replace(/[^a-z0-9\u4e00-\u9fa5-]+/g, '-').replace(/^-+|-+$/g, '') || name
}

function safeText(value) {
  return String(value ?? '').replace(/[&<>"']/g, (char) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  })[char])
}

function safeUrl(value) {
  const url = String(value ?? '').trim()
  return /^https?:\/\//i.test(url) ? url : ''
}

function postHref(fileName) {
  return `post.html?file=${encodeURIComponent(fileName)}`
}

async function loadPosts() {
  try {
    const files = await listPostFiles()
    if (!files.length) {
      postList.innerHTML = '<div class="state-card">posts/ 目录还没有文章。</div>'
      return
    }

    const posts = []
    for (const file of files) {
      const raw = await fetchText(file.download_url)
      const { meta, content } = parseFrontMatter(raw)
      if (meta.draft === true) continue
      posts.push({
        slug: slugify(file.name),
        title: meta.title || file.name.replace(/\.md$/, ''),
        date: meta.date || '',
        summary: meta.summary || content.trim().split(/\r?\n/).find(Boolean)?.slice(0, 120) || '',
        tags: Array.isArray(meta.tags) ? meta.tags : [],
        file: postHref(file.name),
        raw: content,
      })
    }

    posts.sort((a, b) => String(b.date).localeCompare(String(a.date)) || a.title.localeCompare(b.title))
    state.posts = posts
    renderPosts()
  } catch (error) {
    state.error = error instanceof Error ? error.message : String(error)
    postList.innerHTML = `<div class="state-card">文章加载失败：${safeText(state.error)}。请检查 GitHub API 配额或 posts/ 目录。</div>`
  }
}

function renderPosts() {
  if (!state.posts.length) {
    postList.innerHTML = '<div class="state-card">还没有文章。</div>'
    return
  }

  postList.innerHTML = state.posts
    .map(
      (post) => `
        <article class="post-card">
          <div class="post-meta">
            <time datetime="${safeText(post.date)}">${safeText(post.date || '未标注日期')}</time>
          </div>
          <h3><a href="${safeText(post.file)}">${safeText(post.title)}</a></h3>
          <p class="post-summary">${safeText(post.summary)}</p>
          <div class="post-footer">
            <a href="${safeText(post.file)}">阅读全文</a>
            ${post.tags.map((tag) => `<span class="post-tag">${safeText(tag)}</span>`).join('')}
          </div>
        </article>
      `,
    )
    .join('')
}

async function loadProjects() {
  try {
    const url = `https://api.github.com/users/${GITHUB_USER}/repos?sort=updated&per_page=100`
    const res = await fetch(url)
    if (!res.ok) throw new Error(`GitHub API ${res.status}`)
    const repos = await res.json()
    const projects = repos.filter((repo) => !repo.fork).slice(0, 6)
    state.projects = projects
    renderProjects()
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error)
    projectList.innerHTML = `<div class="state-card">项目加载失败：${safeText(message)}。GitHub 数据暂不可用。</div>`
  }
}

function renderProjects() {
  if (!state.projects.length) {
    projectList.innerHTML = '<div class="state-card">暂无公开项目。</div>'
    return
  }

  projectList.innerHTML = state.projects
    .map((project) => {
      const url = safeUrl(project.html_url)
      const homepage = safeUrl(project.homepage)
      const description = safeText(project.description || '暂无描述')
      const language = safeText(project.language || '')
      return `
        <article class="project-card">
          <h3><a href="${safeText(url)}" target="_blank" rel="noopener">${safeText(project.name)}</a></h3>
          <p class="post-summary">${description}</p>
          <div class="project-links">
            ${language ? `<span class="project-tag">${language}</span>` : ''}
            ${homepage ? `<a href="${homepage}" target="_blank" rel="noopener">在线预览</a>` : ''}
            <a href="${safeText(url)}" target="_blank" rel="noopener">仓库</a>
          </div>
        </article>
      `
    })
    .join('')
}

function setupTheme() {
  const toggle = document.querySelector('#theme-toggle')
  const icon = document.querySelector('#theme-icon')
  const stored = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  const apply = (dark) => {
    document.documentElement.classList.add('theme-transition')
    document.documentElement.classList.toggle('dark', dark)
    icon.innerHTML = dark
      ? '<circle cx="12" cy="12" r="4"></circle><path d="M12 2v2m0 16v2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M2 12h2m16 0h2M4.9 19.1l1.4-1.4m11.4-11.4 1.4-1.4"></path>'
      : '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"></path>'
    window.setTimeout(() => document.documentElement.classList.remove('theme-transition'), 360)
  }
  apply(stored ? stored === 'dark' : prefersDark)
  toggle.addEventListener('click', () => {
    const dark = !document.documentElement.classList.contains('dark')
    localStorage.setItem('theme', dark ? 'dark' : 'light')
    apply(dark)
  })
}

document.querySelector('#year').textContent = new Date().getFullYear()
setupTheme()
loadPosts()
loadProjects()
