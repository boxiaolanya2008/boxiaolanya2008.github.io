<script setup lang="ts">
import { onMounted, onUnmounted, useTemplateRef } from 'vue'
import { useDark } from '@vueuse/core'

/**
 * 方块粒子背景：canvas 绘制小方块漂浮，浅/深主题自适应颜色。
 * 警告：别删 window 尺寸变化的 resize 重算；动了会导致窗口缩放后粒子跑出画布或密度错误。
 */
const isDark = useDark()
const canvas = useTemplateRef<HTMLCanvasElement>('particles')

let raf = 0
let ctx: CanvasRenderingContext2D | null = null
let particles: { x: number; y: number; size: number; vx: number; vy: number; rot: number; vr: number; alpha: number; color: string }[] = []
let w = 0
let h = 0

function spawn() {
  const count = Math.min(70, Math.floor((w * h) / 26000))
  /* 多彩粒子：天蓝/靛紫/玫红/青绿轮换，白底上更活泼 */
  const palette = ['59, 130, 246', '99, 102, 241', '217, 70, 239', '16, 185, 129', '244, 114, 182']
  particles = Array.from({ length: count }, () => ({
    x: Math.random() * w,
    y: Math.random() * h,
    size: 2 + Math.random() * 6,
    vx: (Math.random() - 0.5) * 0.35,
    vy: (Math.random() - 0.5) * 0.35,
    rot: Math.random() * Math.PI,
    vr: (Math.random() - 0.5) * 0.01,
    alpha: 0.15 + Math.random() * 0.35,
    color: palette[Math.floor(Math.random() * palette.length)] ?? '59, 130, 246',
  }))
}

function tick() {
  if (!ctx) return
  ctx.clearRect(0, 0, w, h)
  for (const p of particles) {
    p.x += p.vx
    p.y += p.vy
    p.rot += p.vr
    if (p.x < -10) p.x = w + 10
    if (p.x > w + 10) p.x = -10
    if (p.y < -10) p.y = h + 10
    if (p.y > h + 10) p.y = -10
    ctx.save()
    ctx.translate(p.x, p.y)
    ctx.rotate(p.rot)
    ctx.fillStyle = isDark.value
      ? `rgba(${p.color}, ${p.alpha * 0.8})`
      : `rgba(${p.color}, ${p.alpha})`
    ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size)
    ctx.restore()
  }
  raf = requestAnimationFrame(tick)
}

function resize() {
  const el = canvas.value
  if (!el || !el.parentElement) return
  w = el.width = el.parentElement.clientWidth
  h = el.height = el.parentElement.clientHeight
  spawn()
}

onMounted(() => {
  const el = canvas.value
  if (!el) return
  ctx = el.getContext('2d')
  if (!ctx) return
  resize()
  window.addEventListener('resize', resize)
  /* 用户开了减少动态效果就别做循环动画了 */
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) raf = requestAnimationFrame(tick)
})

onUnmounted(() => {
  cancelAnimationFrame(raf)
  window.removeEventListener('resize', resize)
})
</script>

<template>
  <canvas ref="particles" class="absolute inset-0 h-full w-full"></canvas>
</template>
