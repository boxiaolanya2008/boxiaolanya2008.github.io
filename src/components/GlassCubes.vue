<script setup lang="ts">
import { ref } from 'vue'
import { useLoop } from '@tresjs/core'

/* 预生成立方体参数，避免每帧随机 */
const cubes = Array.from({ length: 10 }, (_, i) => ({
  position: [
    (Math.random() - 0.5) * 12,
    (Math.random() - 0.5) * 7,
    -2 - Math.random() * 5,
  ] as [number, number, number],
  size: 0.5 + Math.random() * 0.9,
  speed: 0.1 + Math.random() * 0.25,
  offset: i,
}))

const group = ref()

/* 必须在 TresCanvas 内部组件里调用 useLoop，否则拿不到渲染上下文 */
useLoop().onRender(({ elapsed }) => {
  const g = group.value
  if (!g) return
  g.rotation.y = elapsed * 0.04
  g.children.forEach((child: { rotation: { x: number; z: number }; position: { y: number } }, i: number) => {
    const c = cubes[i]
    if (!c) return
    child.rotation.x = elapsed * c.speed
    child.rotation.z = elapsed * c.speed * 0.6
    child.position.y = c.position[1] + Math.sin(elapsed * 0.4 + c.offset) * 0.5
  })
})
</script>

<template>
  <TresGroup ref="group">
    <TresMesh v-for="(c, i) in cubes" :key="i" :position="(c.position as any)">
      <TresBoxGeometry :args="[c.size, c.size, c.size]" />
      <TresMeshStandardMaterial
        color="#38bdf8"
        :opacity="0.18"
        :transparent="true"
        :roughness="0.15"
        :metalness="0.4"
      />
    </TresMesh>
  </TresGroup>
</template>
