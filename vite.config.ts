import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  /* 开发模式下把 /api 代理到本地 Express 后端（npm run dev:full） */
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
      },
    },
  },
  /* tsconfig.app.json 里配了 paths: { "@/*": ["src/*"] }，这里必须对齐，
     否则 TS 能解析 @/... 但 Vite 构建时会报找不到模块。
     用 import.meta.dirname 而不是 node:url，省掉 @types/node 依赖。 */
  resolve: {
    alias: {
      '@': new URL('./src', import.meta.url).pathname,
    },
  },
  build: {
    chunkSizeWarningLimit: 1200,
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-element-plus': ['element-plus', '@element-plus/icons-vue'],
          'vendor-markdown': ['marked', 'marked-gfm-heading-id', 'marked-highlight', 'highlight.js'],
        },
      },
    },
  },
})
