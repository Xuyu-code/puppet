<template>
  <section class="sp-card sp-card-pad showcase-strip">
    <h2 class="sp-section-title">
      皮影长廊
      <span class="strip-chips" aria-hidden="true">
        <i class="tone-vermilion"></i><i class="tone-yellow"></i><i class="tone-indigo"></i><i class="tone-jade"></i>
      </span>
      <span class="strip-sub">皮影元素示例 · 点击可放大欣赏</span>
    </h2>
    <div class="strip-scroll">
      <figure v-for="(item, i) in items" :key="item.name" class="puppet-card strip-card">
        <el-image
          :src="item.thumb"
          :preview-src-list="previewList"
          :initial-index="i"
          fit="contain"
          preview-teleported
          :alt="item.name"
        />
        <figcaption>
          <span class="cap-name">{{ item.name }}</span>
          <span class="tone-tag" :class="`tone-${item.tone}`">{{ item.category }}</span>
        </figcaption>
      </figure>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { showcaseItems } from '../data/showcase'

const items = showcaseItems
const previewList = computed(() => items.map((it) => it.full))
</script>
