<template>
  <div class="app-shell">
    <!-- 超宽屏两侧淡雅皮影水印（<1400px 视口完全隐藏，置于内容之下；进场页不显示） -->
    <template v-if="!isBare">
      <img class="sp-ambient sp-ambient-left" :src="ambientPuppet" alt="" aria-hidden="true" />
      <img class="sp-ambient sp-ambient-right" :src="ambientPuppet" alt="" aria-hidden="true" />
    </template>

    <header v-if="!isBare" class="sp-header">
      <div class="sp-header-inner">
        <router-link to="/" class="sp-logo">
          <span class="sp-logo-seal">影</span>
          <span class="sp-logo-text">
            <span class="sp-logo-title sp-serif">河湟皮影 · 智能生成</span>
            <span class="sp-logo-sub">HEHUANG SHADOW PUPPETRY</span>
          </span>
        </router-link>
        <nav class="sp-nav">
          <router-link to="/workbench" class="sp-nav-link" active-class="active">生成工作台</router-link>
          <router-link to="/services" class="sp-nav-link" active-class="active">文创服务</router-link>
          <router-link to="/history" class="sp-nav-link" active-class="active">历史图库</router-link>
          <router-link to="/voices" class="sp-nav-link" active-class="active">实践风采</router-link>
          <router-link to="/about" class="sp-nav-link" active-class="active">关于</router-link>
        </nav>
      </div>
    </header>

    <main :class="isBare ? '' : 'sp-main'">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <footer v-if="!isBare" class="sp-footer">
      <span class="sp-serif">河湟皮影</span> · 国家级非物质文化遗产数字创作平台
      <span class="gold">◆</span> 用技术连接传统工艺与当代设计
      <div style="margin-top: 5px; font-size: 12px; opacity: 0.85">
        皮影装饰素材致谢：五天晴 · 皮影资料库（piying.design）
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import ambientPuppet from './assets/showcase/p07.webp'

const route = useRoute()
// bare 路由（进场页）：无导航/页脚/环境水印，整页自绘
const isBare = computed(() => !!route.meta.bare)
</script>
