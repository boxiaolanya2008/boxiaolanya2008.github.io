<script setup lang="ts">
import { TresCanvas } from '@tresjs/core'
import GlassCubes from './GlassCubes.vue'
</script>

<template>
  <!-- 警告：canvas 容器必须保持 pointer-events-none，否则会挡住整页点击；透明度压低保住白底彩色观感 -->
  <div class="absolute inset-0 opacity-35 dark:opacity-25">
    <TresCanvas :alpha="true" clear-color="transparent" window-size>
      <TresPerspectiveCamera :position="([0, 0, 10] as any)" :fov="50" />
      <TresAmbientLight :intensity="2" />
      <TresDirectionalLight :position="([5, 5, 5] as any)" :intensity="1.5" />
      <GlassCubes />
    </TresCanvas>
  </div>
</template>
