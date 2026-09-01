<script setup lang="ts">
import { computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Marked, type Token } from 'marked'
import { markedHighlight } from 'marked-highlight'
import { gfmHeadingId } from 'marked-gfm-heading-id'
import hljs from 'highlight.js/lib/core'
import javascript from 'highlight.js/lib/languages/javascript'
import typescript from 'highlight.js/lib/languages/typescript'
import xml from 'highlight.js/lib/languages/xml'
import css from 'highlight.js/lib/languages/css'
import bash from 'highlight.js/lib/languages/bash'
import json from 'highlight.js/lib/languages/json'
import python from 'highlight.js/lib/languages/python'
import rust from 'highlight.js/lib/languages/rust'
import sql from 'highlight.js/lib/languages/sql'
import markdown from 'highlight.js/lib/languages/markdown'

hljs.registerLanguage('javascript', javascript)
hljs.registerLanguage('typescript', typescript)
hljs.registerLanguage('xml', xml)
hljs.registerLanguage('css', css)
hljs.registerLanguage('bash', bash)
hljs.registerLanguage('json', json)
hljs.registerLanguage('python', python)
hljs.registerLanguage('rust', rust)
hljs.registerLanguage('sql', sql)
hljs.registerLanguage('markdown', markdown)

const ALERT_RE = /^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*/i

interface AlertToken {
  type: string
  alertType: string
  tokens?: Token[]
  raw: string
  text: string
}

const marked = new Marked(
  markedHighlight({
    langPrefix: 'hljs language-',
    highlight(code, lang) {
      if (lang && hljs.getLanguage(lang)) return hljs.highlight(code, { language: lang }).value
      return hljs.highlightAuto(code).value
    },
  }),
  gfmHeadingId(),
)
  .use({
    extensions: [
      {
        name: 'alert',
        renderer(token: { alertType?: string; tokens?: Token[] }) {
          return `<div class="markdown-alert markdown-alert-${token.alertType}"><div class="markdown-alert-body">${this.parser.parse(token.tokens ?? [])}</div></div>`
        },
      },
    ],
  })
  .use({
    walkTokens(token: Token) {
      if (token.type === 'blockquote') {
        const m = (token.text ?? '').match(ALERT_RE)
        if (m) {
          ;(token as AlertToken).type = 'alert'
          ;(token as AlertToken).alertType = m[1].toLowerCase()
          const p = token.tokens?.[0]
          if (p?.type === 'paragraph') {
            p.text = p.text.replace(ALERT_RE, '')
            p.raw = p.raw.replace(ALERT_RE, '')
            const first = p.tokens?.[0]
            if (first && 'text' in first) {
              first.text = first.text.replace(ALERT_RE, '')
              first.raw = first.raw.replace(ALERT_RE, '')
            }
          }
        }
      }
    },
  })

const props = defineProps<{ markdown: string }>()

const html = computed(() => {
  const rendered = marked.parse(props.markdown) as string
  /* 给代码块加标题栏：语言 + 复制按钮，方便在渲染预览里直接检查/复制代码 */
  return rendered.replace(
    /<pre><code class="hljs language-([^"]+)">([\s\S]*?)<\/code><\/pre>/g,
    (_, lang, code) => {
      const label = lang || 'text'
      return `<div class="markdown-code-shell"><div class="markdown-code-actions"><span>${label}</span><button type="button" data-code="${encodeURIComponent(decodeCode(code))}" title="复制代码">复制</button></div><pre><code class="hljs language-${label}">${code}</code></pre></div>`
    },
  )
})

function decodeCode(htmlCode: string) {
  const textarea = document.createElement('textarea')
  textarea.innerHTML = htmlCode
  return textarea.value
}

async function copyCode(event: MouseEvent) {
  const target = event.target as HTMLElement
  const button = target.closest('button[data-code]') as HTMLButtonElement | null
  if (!button) return
  const encoded = button.dataset.code ?? ''
  try {
    await navigator.clipboard.writeText(decodeURIComponent(encoded))
    ElMessage.success('代码已复制')
  } catch {
    ElMessage.error('复制失败')
  }
}
</script>

<template>
  <div class="markdown-body" v-html="html" @click="copyCode"></div>
</template>
