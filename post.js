const GITHUB_USER = 'boxiaolanya2008'
const GITHUB_REPO = 'boxiaolanya2008.github.io'
const GITHUB_BRANCH = 'main'
const POSTS_DIR = 'posts'

const body = document.querySelector('.article-body')
const titleEl = document.querySelector('#post-title')
const dateEl = document.querySelector('#post-date')
const tagsEl = document.querySelector('#post-tags')
const sourceLink = document.querySelector('#source-link')

function currentFileName() {
  return decodeURIComponent(new URLSearchParams(location.search).get('file') || '')
}

function rawFileUrl(fileName) {
  return `https://raw.githubusercontent.com/${GITHUB_USER}/${GITHUB_REPO}/${GITHUB_BRANCH}/${POSTS_DIR}/${fileName}`
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
    } else {
      meta[key] = value.replace(/^["']|["']$/g, '')
    }
  }
  return { meta, content: raw.slice(match[0].length) }
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

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, (char) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  })[char])
}

function setStatus(message) {
  body.innerHTML = `<div class="state-card">${safeText(message)}</div>`
}

async function loadPost() {
  const fileName = currentFileName()
  if (!fileName.endsWith('.md')) {
    setStatus('文章文件名必须是 .md 后缀。')
    return
  }
  try {
    const raw = await (await fetch(rawFileUrl(fileName))).text()
    const { meta, content } = parseFrontMatter(raw)
    const title = meta.title || fileName.replace(/\.md$/, '')
    document.title = `${title} · boxiaolanya2008`
    titleEl.textContent = title
    dateEl.textContent = meta.date || ''
    dateEl.setAttribute('datetime', meta.date || '')
    tagsEl.innerHTML = (Array.isArray(meta.tags) ? meta.tags : [])
      .map((tag) => `<span class="post-tag">${safeText(tag)}</span>`)
      .join('')
    body.innerHTML = renderMarkdown(content)
    if (sourceLink) sourceLink.href = rawFileUrl(fileName)
  } catch (error) {
    setStatus(`文章加载失败：${error instanceof Error ? error.message : String(error)}`)
  }
}

function inline(text) {
  let result = escapeHtml(text)
  result = result.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
  result = result.replace(/__([^_]+)__/g, '<strong>$1</strong>')
  result = result.replace(/\*([^*]+)\*/g, '<em>$1</em>')
  result = result.replace(/~~([^~]+)~~/g, '<del>$1</del>')
  result = result.replace(/`([^`]+)`/g, '<code>$1</code>')
  result = result.replace(
    /\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g,
    '<a href="$2" target="_blank" rel="noopener">$1</a>',
  )
  result = result.replace(/!\[([^\]]*)\]\((https?:\/\/[^)\s]+)\)/g, (_, alt, src) => `<img src="${src}" alt="${alt}">`)
  return result
}

function renderMarkdown(markdown) {
  const lines = String(markdown).replace(/\r\n/g, '\n').split('\n')
  const html = []
  let i = 0
  let inCode = false
  let codeLang = ''
  let codeLines = []
  let listType = ''
  let inTable = false
  let tableRows = []
  let inTaskList = false

  const flushCode = () => {
    if (inCode) {
      const code = escapeHtml(codeLines.join('\n'))
      html.push(
        `<pre><code${codeLang ? ` class="language-${safeText(codeLang)}"` : ''}>${code}\n</code></pre>`,
      )
      codeLines = []
      codeLang = ''
      inCode = false
    }
  }

  const flushList = () => {
    if (listType) {
      html.push(`</${listType}>`)
      listType = ''
    }
  }

  const flushTable = () => {
    if (inTable) {
      const [header, , ...rows] = tableRows
      if (header) {
        const cells = (rows.length ? rows : [header]).map((row) =>
          row
            .split('|')
            .slice(1, -1)
            .map((cell) => `<td>${inline(cell.trim())}</td>`)
            .join(''),
        )
        const headCells = header
          .split('|')
          .slice(1, -1)
          .map((cell) => `<th>${inline(cell.trim())}</th>`)
          .join('')
        html.push(`<table><thead><tr>${headCells}</tr></thead><tbody>${cells.map((row) => `<tr>${row}</tr>`).join('')}</tbody></table>`)
      }
      tableRows = []
      inTable = false
    }
  }

  const flushTaskList = () => {
    if (inTaskList) {
      html.push('</ul>')
      inTaskList = false
    }
  }

  for (; i < lines.length; i++) {
    const line = lines[i]
    const codeFence = line.match(/^```(\w*)\s*$/)
    if (codeFence) {
      if (!inCode) {
        flushList()
        flushTable()
        flushTaskList()
        inCode = true
        codeLang = codeFence[1]
        continue
      }
      flushCode()
      continue
    }

    if (inCode) {
      codeLines.push(line)
      continue
    }

    const trimmed = line.trim()

    if (!trimmed) {
      flushList()
      flushTable()
      flushTaskList()
      continue
    }

    const heading = trimmed.match(/^(#{1,6})\s+(.*)$/)
    if (heading) {
      flushList()
      flushTable()
      flushTaskList()
      const level = heading[1].length
      html.push(`<h${level}>${inline(heading[2])}</h${level}>`)
      continue
    }

    const alert = trimmed.match(/^> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*(.*)$/i)
    if (alert) {
      flushList()
      flushTable()
      flushTaskList()
      html.push(
        `<div class="markdown-alert markdown-alert-${alert[1].toLowerCase()}">${inline(alert[2] || '')}</div>`,
      )
      continue
    }

    if (trimmed.startsWith('> ')) {
      flushList()
      flushTable()
      flushTaskList()
      html.push(`<blockquote>${inline(trimmed.slice(2))}</blockquote>`)
      continue
    }

    const task = trimmed.match(/^[-*]\s+\[([ xX])\]\s+(.*)$/)
    if (task) {
      flushList()
      flushTable()
      if (!inTaskList) {
        html.push('<ul class="task-list">')
        inTaskList = true
      }
      const checked = task[1].toLowerCase() === 'x' ? ' checked' : ''
      html.push(`<li><input type="checkbox" disabled${checked}>${inline(task[2])}</li>`)
      continue
    }

    if (/^[-*]\s+/.test(trimmed) || /^\d+\.\s+/.test(trimmed)) {
      flushTable()
      flushTaskList()
      const type = /^[-*]/.test(trimmed) ? 'ul' : 'ol'
      if (listType !== type) {
        flushList()
        html.push(`<${type}>`)
        listType = type
      }
      html.push(`<li>${inline(trimmed.replace(/^[-*]\s+/, '').replace(/^\d+\.\s+/, ''))}</li>`)
      continue
    }

    if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
      flushList()
      flushTaskList()
      if (!inTable) {
        inTable = true
        tableRows = []
      }
      tableRows.push(trimmed)
      continue
    }

    flushList()
    flushTable()
    flushTaskList()
    html.push(`<p>${inline(trimmed)}</p>`)
  }

  flushCode()
  flushList()
  flushTable()
  flushTaskList()
  return html.join('\n')
}

function setupTheme() {
  const toggle = document.querySelector('#theme-toggle')
  const icon = document.querySelector('#theme-icon')
  const stored = localStorage.getItem('theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  const apply = (dark) => {
    document.documentElement.classList.toggle('dark', dark)
    icon.innerHTML = dark
      ? '<circle cx="12" cy="12" r="4"></circle><path d="M12 2v2m0 16v2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M2 12h2m16 0h2M4.9 19.1l1.4-1.4m11.4-11.4 1.4-1.4"></path>'
      : '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"></path>'
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
loadPost()
