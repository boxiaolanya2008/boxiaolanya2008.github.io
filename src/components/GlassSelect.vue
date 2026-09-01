<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import AppIcon from './AppIcon.vue'

/**
 * 液态玻璃下拉选择框。
 * 警告：options 的 value 必须与 modelValue 用同一套语义值（不要拿界面文案当值），
 * 语言切换后文案会变，拿文案当值会导致选中态丢失。
 */
const props = defineProps<{
  options: { value: string; label: string }[]
  modelValue: string
  ariaLabel?: string
}>()

const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

const open = ref(false)
const root = ref<HTMLElement>()

const current = () => props.options.find((o) => o.value === props.modelValue)?.label ?? props.modelValue

function pick(value: string) {
  emit('update:modelValue', value)
  open.value = false
}

function onDocClick(e: MouseEvent) {
  if (root.value && !root.value.contains(e.target as Node)) open.value = false
}

onMounted(() => document.addEventListener('click', onDocClick))
onUnmounted(() => document.removeEventListener('click', onDocClick))
</script>

<template>
  <div ref="root" class="relative inline-block text-left">
    <button
      type="button"
      class="liquid-glass flex h-8 cursor-pointer items-center gap-2 rounded-full px-4 text-xs font-medium transition-all duration-300 hover:shadow-lg"
      :aria-label="ariaLabel"
      :aria-expanded="open"
      @click="open = !open"
    >
      {{ current() }}
      <AppIcon
        name="chevron"
        :size="13"
        class="text-zinc-400 transition-transform duration-300"
        :class="open ? 'rotate-180' : ''"
      />
    </button>

    <Transition name="drop">
      <ul
        v-if="open"
        class="liquid-glass absolute left-0 z-40 mt-2 max-h-60 w-40 overflow-auto rounded-2xl p-1.5"
      >
        <li v-for="o in options" :key="o.value">
          <button
            type="button"
            class="w-full cursor-pointer rounded-xl px-3 py-1.5 text-left text-xs font-medium transition-colors duration-150"
            :class="o.value === modelValue
              ? 'bg-sky-500/90 text-white'
              : 'text-zinc-600 hover:bg-white/40 dark:text-zinc-300 dark:hover:bg-white/10'"
            @click="pick(o.value)"
          >
            {{ o.label }}
          </button>
        </li>
      </ul>
    </Transition>
  </div>
</template>

<style scoped>
.drop-enter-active,
.drop-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.drop-enter-from,
.drop-leave-to {
  opacity: 0;
  transform: translateY(-6px) scale(0.97);
}
</style>
