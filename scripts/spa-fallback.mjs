/**
 * 生成 dist/404.html：把构建产物 index.html 复制一份当 SPA 深链回退页。
 *
 * 为什么不能在 public/ 里放写死的 404.html：
 *   - public/ 下的文件是原样拷贝，里面若写 /src/main.ts 这种源码路径，产物的 dist/ 中根本不存在，
 *     GitHub Pages 在 /blog 这类深链上返回它就会白屏。
 *   - index.html 经过 Vite 处理后引用的是带 hash 的 /assets/*.js，必须构建完才能拿到。
 * 所以在 vite build 之后跑本脚本，复制最终产物。
 */
import { copyFileSync, existsSync, mkdirSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const src = resolve(root, 'dist/index.html')
const dest = resolve(root, 'dist/404.html')

if (!existsSync(src)) {
  console.error(`[spa-fallback] 找不到 ${src}，请先执行 vite build`)
  process.exit(1)
}

mkdirSync(dirname(dest), { recursive: true })
copyFileSync(src, dest)
console.log('[spa-fallback] dist/404.html <- dist/index.html')
