<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { computed, onBeforeUnmount, onMounted, ref, shallowRef } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { EditPen, View, Check, ChatLineSquare } from '@element-plus/icons-vue'
import { EditorView, keymap, lineNumbers, highlightActiveLine, drawSelection, placeholder } from '@codemirror/view'
import { EditorState, Compartment } from '@codemirror/state'
import { defaultKeymap, history, historyKeymap, indentWithTab } from '@codemirror/commands'
import { autocompletion, closeBrackets, closeBracketsKeymap, completionKeymap } from '@codemirror/autocomplete'
import { searchKeymap, highlightSelectionMatches } from '@codemirror/search'
import { syntaxHighlighting, defaultHighlightStyle, indentOnInput, bracketMatching } from '@codemirror/language'
import { markdown, markdownLanguage } from '@codemirror/lang-markdown'
import { html } from '@codemirror/lang-html'
import { javascript } from '@codemirror/lang-javascript'
import { css } from '@codemirror/lang-css'
import { json } from '@codemirror/lang-json'
import { sql } from '@codemirror/lang-sql'
import { python } from '@codemirror/lang-python'
import { rust } from '@codemirror/lang-rust'
import MarkdownContent from '../components/MarkdownContent.vue'
import { postsApi } from '../api'

const { t } = useI18n()
const router = useRouter()

const title = ref('')
const content = ref('')
const error = ref('')
const loading = ref(false)
const editorHost = ref<HTMLDivElement | null>(null)
const editorView = shallowRef<EditorView | null>(null)
const languageCompartment = new Compartment()

const reviewEnabled = ref(false)
const reviewSubject = ref('')
const reviewSubjectEn = ref('')
const reviewRating = ref(8)
const reviewSummary = ref('')
const reviewSummaryEn = ref('')
const reviewPros = ref('')
const reviewCons = ref('')
const reviewVerdict = ref('')
const reviewVerdictEn = ref('')

const editorStyle = EditorView.theme({
  '&': { height: '100%', fontSize: '14px', backgroundColor: 'transparent' },
  '.cm-scroller': { fontFamily: 'var(--font-mono)', lineHeight: '1.7', overflow: 'auto' },
  '.cm-content': { minHeight: '520px', padding: '16px 4px' },
  '.cm-gutters': { backgroundColor: 'transparent', border: 'none', color: 'var(--fg-subtle)' },
  '.cm-activeLine': { backgroundColor: 'var(--bg-subtle)' },
  '.cm-activeLineGutter': { backgroundColor: 'transparent' },
  '.cm-tooltip': { border: '1px solid var(--border)', borderRadius: '10px', backgroundColor: 'var(--bg)', color: 'var(--fg)', boxShadow: '0 12px 32px -18px rgba(15,23,42,.35)', overflow: 'hidden' },
  '.cm-tooltip-autocomplete > ul > li[aria-selected]': { backgroundColor: 'var(--accent-muted)', color: 'var(--accent-fg)' },
})

const markdownExtensions = () => [
  markdown({ base: markdownLanguage }),
  autocompletion({ override: [markdownCompletions] }),
]

const languageExtensions = (value: string) => {
  const blockMatch = value.match(/```(\w+)?/g)
  const lastLang = blockMatch?.[blockMatch.length - 1]?.replace(/```/, '') ?? ''
  if (['html', 'vue', 'xml'].includes(lastLang)) return [html()]
  if (['js', 'javascript'].includes(lastLang)) return [javascript()]
  if (['css'].includes(lastLang)) return [css()]
  if (['json'].includes(lastLang)) return [json()]
  if (['sql'].includes(lastLang)) return [sql()]
  if (['python'].includes(lastLang)) return [python()]
  if (['rust'].includes(lastLang)) return [rust()]
  return markdownExtensions()
}

function markdownCompletions(context: { pos: number; explicit?: boolean }) {
  const text = content.value
  const before = text.slice(0, context.pos)
  const word = before.match(/[\w-]*$/)?.[0] ?? ''
  if (!word && !context.explicit) return null

  const baseOptions: { label: string; detail: string; type: string; insertText?: string }[] = [
    { label: '```', detail: 'code block', type: 'keyword' },
    { label: '#', detail: 'heading', type: 'keyword' },
    { label: '##', detail: 'heading 2', type: 'keyword' },
    { label: '###', detail: 'heading 3', type: 'keyword' },
    { label: '>', detail: 'blockquote', type: 'keyword' },
    { label: '-', detail: 'list', type: 'keyword' },
    { label: '1.', detail: 'ordered list', type: 'keyword' },
    { label: '[x]', detail: 'task', type: 'keyword' },
    { label: '[!NOTE]', detail: 'note alert', type: 'keyword' },
    { label: '[!TIP]', detail: 'tip alert', type: 'keyword' },
    { label: '[!WARNING]', detail: 'warning alert', type: 'keyword' },
    { label: '[!CAUTION]', detail: 'caution alert', type: 'keyword' },
    { label: '[!IMPORTANT]', detail: 'important alert', type: 'keyword' },
    { label: '![alt](url)', detail: 'image', type: 'keyword' },
    { label: '[text](url)', detail: 'link', type: 'keyword' },
    { label: '**bold**', detail: 'bold', type: 'keyword' },
    { label: '*italic*', detail: 'italic', type: 'keyword' },
    { label: '`code`', detail: 'inline code', type: 'keyword' },
    { label: '---', detail: 'divider', type: 'keyword' },
    { label: '| col | col |', detail: 'table', type: 'keyword' },
  ]; const options = baseOptions.map((o) => ({ label: o.label, detail: o.detail, type: o.type, apply: o.insertText ?? o.label }))

  const token = before.match(/`{3}([\w-]*)$/)?.[1]
  if (token !== undefined) {
    const langs = ['typescript', 'javascript', 'html', 'css', 'json', 'sql', 'python', 'rust', 'bash', 'markdown']
    return { from: context.pos - token.length, options: langs.map((l) => ({ label: l, type: 'keyword' })) }
  }

  return {
    from: context.pos - word.length,
    options: options.filter((o) => o.label.startsWith(word) || o.label.toLowerCase().includes(word.toLowerCase())),
  }
}

function createEditor() {
  if (!editorHost.value) return
  const state = EditorState.create({
    doc: content.value,
    extensions: [
      lineNumbers(),
      history(),
      drawSelection(),
      indentOnInput(),
      bracketMatching(),
      closeBrackets(),
      highlightActiveLine(),
      highlightSelectionMatches(),
      syntaxHighlighting(defaultHighlightStyle, { fallback: true }),
      placeholder('支持 Markdown、HTML、JS 等代码补全，右侧实时预览'),
      keymap.of([...closeBracketsKeymap, ...defaultKeymap, ...searchKeymap, ...historyKeymap, ...completionKeymap, indentWithTab]),
      EditorView.updateListener.of((update) => {
        if (update.docChanged) content.value = update.state.doc.toString()
      }),
      editorStyle,
      languageCompartment.of(languageExtensions(content.value)),
    ],
  })

  editorView.value = new EditorView({ state, parent: editorHost.value })
}

function updateLanguage() {
  if (!editorView.value) return
  editorView.value.dispatch({
    effects: languageCompartment.reconfigure(languageExtensions(content.value)),
  })
}

onMounted(() => {
  createEditor()
})

onBeforeUnmount(() => {
  editorView.value?.destroy()
  editorView.value = null
})

const reviewMeta = computed(() => {
  if (!reviewEnabled.value) return undefined
  return {
    subject: reviewSubject.value.trim() || title.value.trim() || 'Review',
    subjectEn: reviewSubjectEn.value.trim() || undefined,
    rating: reviewRating.value,
    summary: reviewSummary.value.trim() || undefined,
    summaryEn: reviewSummaryEn.value.trim() || undefined,
    pros: reviewPros.value.split('\n').map((s) => s.trim()).filter(Boolean),
    cons: reviewCons.value.split('\n').map((s) => s.trim()).filter(Boolean),
    verdict: reviewVerdict.value.trim() || undefined,
    verdictEn: reviewVerdictEn.value.trim() || undefined,
  }
})

const submit = async () => {
  error.value = ''
  if (!title.value.trim()) {
    error.value = t('editor.emptyTitle')
    return
  }
  if (!content.value.trim()) {
    error.value = t('editor.emptyContent')
    return
  }
  loading.value = true
  try {
    const { slug } = await postsApi.create({
      title: title.value.trim(),
      content: content.value.trim(),
      review: reviewMeta.value,
    })
    ElMessage.success(t('editor.published'))
    router.push(`/blog/${slug}`)
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-7xl px-5 py-10 sm:px-8">
    <div class="mb-6 flex flex-wrap items-center justify-between gap-3">
      <h1 class="flex items-center gap-2 text-3xl font-bold tracking-tight text-[var(--fg)] sm:text-4xl">
        <el-icon :size="28"><EditPen /></el-icon>
        {{ t('editor.new') }}
      </h1>
      <el-button type="primary" :loading="loading" @click="submit">
        <el-icon class="mr-1"><Check /></el-icon>
        {{ t('editor.publish') }}
      </el-button>
    </div>

    <el-form label-position="top" class="space-y-4">
      <el-form-item :label="t('editor.title')" class="!mb-0">
        <el-input v-model="title" maxlength="80" show-word-limit placeholder="文章标题" />
      </el-form-item>

      <el-card shadow="never" class="!border-[var(--border)]">
        <template #header>
          <div class="flex flex-wrap items-center justify-between gap-3">
            <span class="flex items-center gap-2 text-sm font-semibold text-[var(--fg)]">
              <el-icon :size="16"><ChatLineSquare /></el-icon>
              {{ t('review.title') }}
            </span>
            <el-switch v-model="reviewEnabled" />
          </div>
        </template>
        <div v-if="reviewEnabled" class="grid gap-4 sm:grid-cols-2">
          <el-form-item :label="t('review.subject')">
            <el-input v-model="reviewSubject" :placeholder="t('review.subjectPlaceholder')" />
          </el-form-item>
          <el-form-item :label="t('review.rating')">
            <div class="flex w-full flex-col gap-2">
              <el-rate v-model="reviewRating" :max="10" show-score />
              <el-slider v-model="reviewRating" :min="1" :max="10" />
            </div>
          </el-form-item>
          <el-form-item :label="t('review.summary')">
            <el-input v-model="reviewSummary" type="textarea" :rows="2" />
          </el-form-item>
          <el-form-item :label="t('review.pros')">
            <el-input v-model="reviewPros" type="textarea" :rows="4" :placeholder="t('review.onePerLine')" />
          </el-form-item>
          <el-form-item :label="t('review.cons')">
            <el-input v-model="reviewCons" type="textarea" :rows="4" :placeholder="t('review.onePerLine')" />
          </el-form-item>
          <el-form-item :label="t('review.verdict')">
            <el-input v-model="reviewVerdict" type="textarea" :rows="2" />
          </el-form-item>
        </div>
      </el-card>

      <div class="grid gap-4 lg:grid-cols-2">
        <section class="page-panel overflow-hidden p-3">
          <div class="mb-2 flex items-center justify-between px-1">
            <span class="text-xs font-semibold text-[var(--fg-muted)]">Markdown</span>
            <span class="text-xs text-[var(--fg-subtle)]">Tab 补全 · Ctrl+Space 手动触发 · Ctrl+Z 撤销</span>
          </div>
          <div ref="editorHost" class="editor-code-input h-[560px] overflow-hidden rounded-xl border border-[var(--border)] bg-[var(--bg)]" />
        </section>
        <section class="page-panel overflow-hidden p-3">
          <div class="mb-2 flex items-center justify-between px-1">
            <span class="text-xs font-semibold text-[var(--fg-muted)]">渲染预览</span>
            <el-button link size="small" @click="updateLanguage">
              <el-icon class="mr-1"><View /></el-icon>
              刷新
            </el-button>
          </div>
          <div class="markdown-preview h-[560px] overflow-auto rounded-xl border border-[var(--border)] bg-[var(--bg)] p-4">
            <MarkdownContent v-if="content" :markdown="content" />
            <el-empty v-else :description="t('editor.previewEmpty')" />
          </div>
        </section>
      </div>

      <div class="flex flex-wrap items-center justify-end gap-3">
        <p v-if="error" class="mr-auto text-sm text-[var(--caution-fg)]">{{ error }}</p>
        <el-button type="primary" :loading="loading" @click="submit">
          <el-icon class="mr-1"><Check /></el-icon>
          {{ t('editor.publish') }}
        </el-button>
      </div>
    </el-form>
  </div>
</template>
