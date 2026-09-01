<script setup lang="ts">
/**
 * 动态 SVG 图标集：用 CSS 动画让图标本身动起来。
 * name: 图标名；size: 像素边长。
 * 警告：别动 path 里的坐标；动了会导致图标变形走样。
 */
const props = withDefaults(defineProps<{ name: string; size?: number }>(), { size: 20 })
</script>

<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="1.8"
    stroke-linecap="round"
    stroke-linejoin="round"
    class="svg-icon"
    :class="`icon-${name}`"
    aria-hidden="true"
  >
    <template v-if="name === 'github'">
      <path d="M9 19c-4.3 1.4-4.3-2.5-6-3m12 5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12.3 12.3 0 0 0-6.2 0C6.5 2.8 5.4 3.1 5.4 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21" />
    </template>

    <template v-else-if="name === 'bilibili'">
      <path d="M7.5 6.5 5 3.5M16.5 6.5l2.5-3" />
      <rect x="3" y="6.5" width="18" height="13" rx="3" />
      <path d="M9.5 11v4M14.5 11v4" class="anim-blink" />
    </template>

    <template v-else-if="name === 'mail'">
      <rect x="3" y="5" width="18" height="14" rx="3" />
      <path d="m4 7 8 6 8-6" class="anim-dash" />
    </template>

    <template v-else-if="name === 'sun'">
      <circle cx="12" cy="12" r="4" />
      <g class="anim-spin">
        <path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5 5l1.4 1.4M17.6 17.6 19 19M19 5l-1.4 1.4M6.4 17.6 5 19" />
      </g>
    </template>

    <template v-else-if="name === 'moon'">
      <path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5Z" class="anim-float" />
      <path d="m17 5 .5 1.5L19 7l-1.5.5L17 9l-.5-1.5L15 7l1.5-.5Z" class="anim-twinkle" />
    </template>

    <template v-else-if="name === 'home'">
      <path d="m3 11 9-8 9 8" class="anim-dash" />
      <path d="M5 10v10h14V10" />
      <path d="M10 20v-5h4v5" />
    </template>

    <template v-else-if="name === 'folder'">
      <path d="M3 7a2 2 0 0 1 2-2h4l2 2.5h8a2 2 0 0 1 2 2V17a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z" />
      <path d="M7 13h6" class="anim-dash" />
    </template>

    <template v-else-if="name === 'pen'">
      <path d="M4 20h4l11-11a2.1 2.1 0 0 0-3-3L5 17Z" />
      <path d="M13.5 6.5l3 3" class="anim-dash" />
    </template>

    <template v-else-if="name === 'clock'">
      <circle cx="12" cy="12" r="9" />
      <path d="M12 7v5l3.5 2" class="anim-tick" />
    </template>

    <template v-else-if="name === 'sparkle'">
      <path d="M12 3.5 13.8 9l5.5 1.8-5.5 1.8L12 18l-1.8-5.4L4.7 10.8 10.2 9Z" class="anim-twinkle" />
    </template>

    <template v-else-if="name === 'empty'">
      <rect x="3" y="4" width="18" height="16" rx="3" />
      <path d="M8 10h8M8 14h5" class="anim-dash" />
    </template>

    <template v-else-if="name === 'star'">
      <path d="m12 3.5 2.6 5.4 5.9.8-4.3 4.1 1 5.9-5.2-2.8-5.2 2.8 1-5.9L3.5 9.7l5.9-.8Z" class="anim-twinkle" />
    </template>

    <template v-else-if="name === 'globe'">
      <circle cx="12" cy="12" r="9" />
      <path d="M3 12h18" class="anim-dash" />
      <path d="M12 3c2.5 2.6 3.8 5.7 3.8 9S14.5 18.4 12 21c-2.5-2.6-3.8-5.7-3.8-9S9.5 5.6 12 3Z" class="anim-spin-slow" />
    </template>

    <template v-else-if="name === 'chevron'">
      <path d="m6 9 6 6 6-6" class="anim-dash" />
    </template>
  </svg>
</template>

<style scoped>
.svg-icon {
  flex-shrink: 0;
}

/* 虚线描边循环：像手绘一笔一笔画出来 */
.anim-dash {
  stroke-dasharray: 24;
  animation: dash-move 2.6s ease-in-out infinite;
}
@keyframes dash-move {
  0%, 100% { stroke-dashoffset: 0; opacity: 1; }
  50% { stroke-dashoffset: 10; opacity: 0.55; }
}

/* 缓慢自转，用于太阳光芒、时钟指针用 tick */
.anim-spin {
  transform-origin: 12px 12px;
  animation: spin 8s linear infinite;
}
.anim-spin-slow {
  transform-origin: 12px 12px;
  animation: spin 14s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 时钟指针摆动 */
.anim-tick {
  transform-origin: 12px 12px;
  animation: tick 4s ease-in-out infinite;
}
@keyframes tick {
  0%, 100% { transform: rotate(0deg); }
  50% { transform: rotate(120deg); }
}

/* 月亮轻浮动 + 星星闪烁 */
.anim-float { animation: float-y 3s ease-in-out infinite; }
@keyframes float-y {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-1.2px); }
}
.anim-twinkle { animation: twinkle 2.2s ease-in-out infinite; transform-origin: center; }
@keyframes twinkle {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.35; transform: scale(0.82); }
}

/* bilibili 眼睛眨动 */
.anim-blink { animation: blink 3.4s ease-in-out infinite; }
@keyframes blink {
  0%, 92%, 100% { transform: scaleY(1); }
  95% { transform: scaleY(0.15); }
}
.anim-blink { transform-origin: center; transform-box: fill-box; }
</style>
