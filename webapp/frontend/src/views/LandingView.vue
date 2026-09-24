<template>
  <div class="scene" :class="{ ready: entered }">
    <!-- 场景本体（幕布升起时同步亮灯 brightness 0.75→1） -->
    <div class="scene-body" :class="{ lit }">
      <!-- 巨型黑色镂空龙纹（火龙素材黑化，左侧巨物） -->
      <img class="dragon" :src="p15" alt="" aria-hidden="true" />

      <!-- 圆月（泥金，外圈呼吸光晕） -->
      <div class="moon" aria-hidden="true">
        <div class="moon-halo"></div>
        <div class="moon-disc"></div>
      </div>

      <!-- 天空极淡云纹带（缓慢平移） -->
      <div class="cloud-band" aria-hidden="true"></div>

      <!-- 天空水墨大字标题块 -->
      <div class="scene-title">
        <h1 class="st-title" aria-label="河湟皮影">
          <svg class="ink-title" viewBox="0 0 640 150" role="img" aria-hidden="true">
            <defs>
              <filter id="ink-rough" x="-6%" y="-6%" width="112%" height="112%">
                <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="3" seed="7" result="n" />
                <feDisplacementMap in="SourceGraphic" in2="n" scale="6" xChannelSelector="R" yChannelSelector="G" />
              </filter>
            </defs>
            <g filter="url(#ink-rough)" font-family="'STXingkai','STKaiti','KaiTi',serif" font-size="118" font-weight="700">
              <g class="ink-char"><text x="18" y="118" fill="#f4ead2" transform="rotate(-2 78 75)">河</text></g>
              <g class="ink-char"><text x="178" y="116" fill="#f0e4c8" transform="rotate(1.5 238 75)">湟</text></g>
              <g class="ink-char"><text x="338" y="119" fill="#f4ead2" transform="rotate(-1 398 75)">皮</text></g>
              <g class="ink-char"><text x="498" y="117" fill="#efe3c6" transform="rotate(2 558 75)">影</text></g>
            </g>
          </svg>
        </h1>
        <p class="st-sub sp-serif">智能生成 · 非遗新传</p>
        <p class="st-desc">从一笔线稿到一幅皮影，让传统纹样在数字光影中重生</p>
        <div class="st-actions">
          <router-link to="/workbench" class="st-enter sp-serif">进入工作台</router-link>
          <router-link to="/about" class="st-about">了解非遗皮影 →</router-link>
        </div>
      </div>

      <!-- 金色戏台地面（上深下浅琥珀，前沿回纹金带） -->
      <div class="stage-floor" aria-hidden="true"></div>

      <!-- 地面草丛剪影点缀 -->
      <svg class="grass grass-left" viewBox="0 0 120 60" aria-hidden="true">
        <g fill="#0a0d14">
          <path d="M8 60 Q14 34 4 18 Q20 30 20 52 Q26 26 40 12 Q32 34 30 54 Q40 38 52 30 Q42 46 40 60 Z" />
          <path d="M70 60 Q76 40 68 26 Q82 36 82 54 Q88 34 100 24 Q94 42 92 56 Q100 46 108 42 Q102 52 100 60 Z" />
        </g>
      </svg>
      <svg class="grass grass-right" viewBox="0 0 120 60" aria-hidden="true">
        <g fill="#0a0d14">
          <path d="M8 60 Q14 34 4 18 Q20 30 20 52 Q26 26 40 12 Q32 34 30 54 Q40 38 52 30 Q42 46 40 60 Z" />
          <path d="M70 60 Q76 40 68 26 Q82 36 82 54 Q88 34 100 24 Q94 42 92 56 Q100 46 108 42 Q102 52 100 60 Z" />
        </g>
      </svg>

      <!-- 右侧远处屋舍剪影（简约 SVG 双层屋檐） -->
      <svg class="house" viewBox="0 0 220 120" aria-hidden="true">
        <g fill="#0a0d14">
          <path d="M8 52 Q60 34 110 48 Q160 34 212 52 L196 58 Q110 44 24 58 Z" />
          <rect x="46" y="58" width="128" height="7" />
          <path d="M0 88 Q110 62 220 88 L202 96 Q110 78 18 96 Z" />
          <rect x="26" y="96" width="168" height="7" />
          <rect x="42" y="103" width="9" height="15" />
          <rect x="169" y="103" width="9" height="15" />
        </g>
      </svg>

      <!-- 人物群组背光（戏台幕布暖黄背光，与圆月成双光区） -->
      <div class="troupe-glow" aria-hidden="true"></div>

      <!-- 剧团：左丫鬟 — 八仙桌+皮影笔记本（贵妃桌后操作） — 右王帽生 -->
      <div class="troupe">
        <img class="actor actor-left" :src="p10" alt="" />
        <div class="table-scene" aria-hidden="true">
          <svg viewBox="0 0 340 210" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <radialGradient id="screenGrad" cx="50%" cy="42%" r="75%">
                <stop offset="0%" stop-color="#f7e0a6" />
                <stop offset="55%" stop-color="#e8c87e" />
                <stop offset="100%" stop-color="#cfa255" />
              </radialGradient>
              <radialGradient id="glowGrad" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="rgba(246, 220, 150, 0.55)" />
                <stop offset="70%" stop-color="rgba(246, 220, 150, 0)" />
              </radialGradient>
            </defs>

            <!-- 八仙桌：黑色剪影，牙条描金 -->
            <g fill="#0b0e15">
              <rect x="14" y="96" width="312" height="15" rx="3" />
              <rect x="26" y="111" width="288" height="9" rx="2" />
              <rect x="34" y="120" width="13" height="76" rx="2" />
              <rect x="293" y="120" width="13" height="76" rx="2" />
              <rect x="40" y="164" width="260" height="6" rx="2" />
            </g>
            <g stroke="#c9a24f" stroke-width="1.1" opacity="0.55" fill="none">
              <line x1="30" y1="115.5" x2="310" y2="115.5" />
            </g>
            <g fill="#c9a24f" opacity="0.55">
              <rect x="54" y="113" width="5" height="5" transform="rotate(45 56.5 115.5)" />
              <rect x="102" y="113" width="5" height="5" transform="rotate(45 104.5 115.5)" />
              <rect x="150" y="113" width="5" height="5" transform="rotate(45 152.5 115.5)" />
              <rect x="198" y="113" width="5" height="5" transform="rotate(45 200.5 115.5)" />
              <rect x="246" y="113" width="5" height="5" transform="rotate(45 248.5 115.5)" />
            </g>

            <!-- 皮影风笔记本电脑：黑机身镂空描金，屏幕暖金光 -->
            <path d="M100 96 L240 96 L252 108 Q254 112 248 112 L92 112 Q86 112 88 108 Z"
              fill="#0b0e15" stroke="rgba(201, 162, 79, 0.35)" stroke-width="1" />
            <rect x="155" y="100" width="30" height="5" rx="2" fill="rgba(201, 162, 79, 0.25)" />
            <g stroke="#c9a24f" stroke-width="0.9" opacity="0.5" fill="none">
              <line x1="100" y1="108" x2="240" y2="108" />
            </g>
            <g fill="#c9a24f" opacity="0.5">
              <rect x="126" y="105.5" width="5" height="5" transform="rotate(45 128.5 108)" />
              <rect x="206" y="105.5" width="5" height="5" transform="rotate(45 208.5 108)" />
            </g>
            <rect x="110" y="18" width="120" height="78" rx="6" fill="#0d1017"
              stroke="rgba(201, 162, 79, 0.45)" stroke-width="1" />
            <rect class="screen-face" x="117" y="25" width="106" height="64" rx="3" fill="url(#screenGrad)" />
            <!-- 屏幕内容：朱红篆刻小章「AI」+ 两侧代码纹样短线 -->
            <g>
              <rect x="158" y="42" width="24" height="24" rx="4" fill="#b33727"
                stroke="rgba(248, 239, 221, 0.55)" stroke-width="1" transform="rotate(-3 170 54)" />
              <text x="170" y="59" text-anchor="middle" font-size="12" font-weight="700" fill="#f8efdd"
                font-family="'STKaiti','KaiTi',serif" transform="rotate(-3 170 54)">AI</text>
              <g fill="#8a6c34" opacity="0.8">
                <rect x="128" y="46" width="18" height="2.6" rx="1.3" />
                <rect x="128" y="54" width="24" height="2.6" rx="1.3" />
                <rect x="128" y="62" width="14" height="2.6" rx="1.3" />
                <rect x="194" y="46" width="18" height="2.6" rx="1.3" />
                <rect x="188" y="54" width="24" height="2.6" rx="1.3" />
                <rect x="198" y="62" width="14" height="2.6" rx="1.3" />
              </g>
            </g>

            <!-- 屏幕前暖光辉光 -->
            <ellipse class="screen-glow" cx="170" cy="62" rx="118" ry="62" fill="url(#glowGrad)" />
          </svg>
        </div>
        <img class="actor actor-lead" :src="p03" alt="" />
        <img class="actor actor-far" :src="p06" alt="" />
      </div>

      <!-- 前景树石剪影（黑化假山花树，近景压边） -->
      <img class="tree tree-left" :src="p13" alt="" aria-hidden="true" />
      <img class="tree tree-right" :src="p14" alt="" aria-hidden="true" />

      <!-- 平台数据带：真实生成统计 + 服务活动常量（实践活动中） -->
      <div class="stats-band" aria-label="平台数据">
        <span class="stat-item"><b>{{ statsText.completed }}</b><i>累计生成</i></span>
        <span class="stat-item"><b>{{ statsText.candidates }}</b><i>候选产出</i></span>
        <span class="stat-item"><b>{{ statsText.completed ? '在线' : '待创作' }}</b><i>平台状态</i></span>
        <span class="stat-divider" aria-hidden="true"></span>
        <span class="stat-item"><b>{{ sessionsText }}</b><i>实践活动场次</i></span>
        <span class="stat-item"><b>{{ headcountText }}</b><i>覆盖人次</i></span>
        <span class="stat-badge">实践活动中</span>
      </div>

      <div class="scene-credit">皮影素材致谢：五天晴 · 皮影资料库（piying.design）</div>
    </div>

    <!-- 幕布层：幕后影子（黑影摇曳）→ 卷幕升起 -->
    <div v-if="curtainVisible" class="curtain" :class="{ lifting }" @click="skipCurtain">
      <div class="curtain-paper">
        <img class="shadow shadow-a" :src="p01" alt="" aria-hidden="true" />
        <img class="shadow shadow-b" :src="p04" alt="" aria-hidden="true" />
        <img class="shadow shadow-c" :src="p05" alt="" aria-hidden="true" />
        <div class="curtain-caption sp-serif">好戏开场……</div>
      </div>
      <div class="curtain-rod" aria-hidden="true"></div>
    </div>

    <!-- 加载页：真实资源预加载进度，完成后淡出 -->
    <transition name="loader-fade">
      <div v-if="loading" class="preloader" @click="skipLoader">
        <div class="pre-seal sp-serif">影</div>
        <div class="pre-title sp-serif">河湟皮影</div>
        <div class="pre-num sp-serif">{{ progress }}<span class="pre-pct">%</span></div>
        <div class="pre-bar" role="progressbar" :aria-valuenow="progress" aria-valuemin="0" aria-valuemax="100">
          <i class="pre-bar-cap"></i>
          <div class="pre-bar-track">
            <div class="pre-bar-fill" :style="{ width: progress + '%' }"></div>
          </div>
          <i class="pre-bar-cap"></i>
        </div>
        <div class="pre-hint">资源加载中 · 点击可跳过</div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { fetchStats } from '../api/client'
import p01 from '../assets/showcase/p01.webp'
import p03 from '../assets/showcase/p03.webp'
import p04 from '../assets/showcase/p04.webp'
import p05 from '../assets/showcase/p05.webp'
import p06 from '../assets/showcase/p06.webp'
import p10 from '../assets/showcase/p10.webp'
import p13 from '../assets/showcase/p13.webp'
import p14 from '../assets/showcase/p14.webp'
import p15 from '../assets/showcase/p15.webp'

// ---------------------------------------------------------------------------
// 开场编排：加载页 → 幕后影子（幕布+黑影摇曳）→ 卷幕升起+亮灯 → 标题书写
// ---------------------------------------------------------------------------
const PRELOAD_KEY = 'hh-landing-preloaded'
const MIN_SHOW_MS = 1200
const SHADOW_MS = 1600 // 幕后影子阶段时长
const LIFT_MS = 2000 // 幕布升起时长（与 CSS transition 一致）

const loading = ref(false) // 加载页
const curtainVisible = ref(false) // 幕布层
const lifting = ref(false) // 幕布升起
const lit = ref(true) // 场景亮灯（brightness 1）
const entered = ref(true) // 场景编排（标题书写/按钮/循环动画）是否启动
const progress = ref(100)
const targetProgress = ref(100)
let smoothTimer = null
let liftTimer = null
let revealTimer = null

// ---------------------------------------------------------------------------
// 平台数据带：真实生成统计（/api/stats）+ 服务活动常量（实践活动进行中）
// ---------------------------------------------------------------------------
// 服务活动数据：实践活动按计划推进中，结束后据实更新；0 展示为「—」，不虚构
const SERVICE_SESSIONS = 0
const SERVICE_HEADCOUNT = 0

const stats = ref(null)
const statsText = computed(() => ({
  completed: stats.value ? stats.value.completed_generations : '—',
  candidates: stats.value ? stats.value.total_candidates : '—',
}))
const sessionsText = computed(() => (SERVICE_SESSIONS > 0 ? SERVICE_SESSIONS : '—'))
const headcountText = computed(() => (SERVICE_HEADCOUNT > 0 ? SERVICE_HEADCOUNT : '—'))

function startLift() {
  lifting.value = true
  lit.value = true // 场景同步亮灯
  revealTimer = setTimeout(() => {
    curtainVisible.value = false
    entered.value = true // 标题书写 + 按钮淡入 + 循环动画
  }, LIFT_MS + 100)
}

// 加载完成：加载页淡出，露出幕后影子（影子阶段开始）
function finish() {
  sessionStorage.setItem(PRELOAD_KEY, '1')
  if (smoothTimer) {
    clearInterval(smoothTimer)
    smoothTimer = null
  }
  loading.value = false
  liftTimer = setTimeout(startLift, SHADOW_MS)
}

// 点击加载页：跳过加载页，直接进入影子阶段
function skipLoader() {
  if (loading.value) finish()
}

// 点击幕布：跳过开场，直接进入场景终态
function skipCurtain() {
  if (liftTimer) clearTimeout(liftTimer)
  if (revealTimer) clearTimeout(revealTimer)
  lifting.value = true
  lit.value = true
  curtainVisible.value = false
  entered.value = true
}

onMounted(() => {
  // 平台真实统计（静默失败则显示 —）
  fetchStats()
    .then((s) => {
      stats.value = s
    })
    .catch(() => {
      stats.value = null
    })

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const previewMode = new URLSearchParams(window.location.search).get('preview') === '1'
  if (reduced || previewMode || sessionStorage.getItem(PRELOAD_KEY)) return

  entered.value = false
  lit.value = false
  loading.value = true
  curtainVisible.value = true
  progress.value = 0
  targetProgress.value = 0

  // 显示层平滑追赶真实进度（真实进度为每图一跳的离散值）
  smoothTimer = setInterval(() => {
    if (progress.value < targetProgress.value) {
      const gap = targetProgress.value - progress.value
      progress.value = Math.min(targetProgress.value, progress.value + Math.max(1, Math.ceil(gap * 0.16)))
    }
  }, 40)

  const urls = [p01, p03, p04, p05, p06, p10, p13, p14, p15]
  const start = performance.now()
  let done = 0
  const tick = () => {
    done += 1
    targetProgress.value = Math.round((done / urls.length) * 100)
  }
  Promise.all(
    urls.map(
      (u) =>
        new Promise((resolve) => {
          const im = new Image()
          im.onload = im.onerror = () => {
            tick()
            resolve()
          }
          im.src = u
        }),
    ),
  ).then(async () => {
    const remain = MIN_SHOW_MS - (performance.now() - start)
    if (remain > 0) await new Promise((r) => setTimeout(r, remain))
    finish()
  })
})
</script>

<style scoped>
/* ---------------------------------------------------------------------------
 * 进场页：夜幕灯影皮影戏场景 + 幕布开场
 * ------------------------------------------------------------------------- */
.scene {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  background-color: #2f6ea6;
}

/* 场景本体：亮灯过渡只作用于场景层（不含幕布/加载页） */
.scene-body {
  position: absolute;
  inset: 0;
  overflow: hidden;
  filter: brightness(0.75);
  transition: filter 2s ease;
  background-color: #2f6ea6;
  background-image:
    /* 宣纸纤维纹理（极淡） */
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='280' height='280'%3E%3Cfilter id='p'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23p)' opacity='0.04'/%3E%3C/svg%3E"),
    /* 星点（上部深夜区，极淡） */
    radial-gradient(circle 1.6px at 16% 12%, rgba(255, 246, 220, 0.3), transparent 70%),
    radial-gradient(circle 1.2px at 32% 7%, rgba(255, 246, 220, 0.24), transparent 70%),
    radial-gradient(circle 1.8px at 55% 11%, rgba(255, 246, 220, 0.26), transparent 70%),
    radial-gradient(circle 1.3px at 78% 9%, rgba(255, 246, 220, 0.22), transparent 70%),
    /* 群青天空：顶深向下渐亮 */
    linear-gradient(180deg, #2c689e 0%, #3f83bd 34%, #57a0cf 62%, #4b92c4 100%);
}

.scene-body.lit {
  filter: brightness(1);
}

/* ---------------------------------------------------------------------------
 * 巨型黑色镂空龙纹（左侧 40%+，微超左边缘）
 * ------------------------------------------------------------------------- */
.dragon {
  position: absolute;
  left: -3%;
  top: 10%;
  width: 44%;
  z-index: 2;
  pointer-events: none;
  filter: brightness(0);
  opacity: 0.34;
}

/* ---------------------------------------------------------------------------
 * 圆月与月晕
 * ------------------------------------------------------------------------- */
.moon {
  position: absolute;
  top: 7%;
  right: 7%;
  width: min(25vmin, 290px);
  aspect-ratio: 1;
  z-index: 1;
  pointer-events: none;
}

.moon-halo {
  position: absolute;
  inset: -42%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(240, 210, 140, 0.5), rgba(240, 210, 140, 0.14) 48%, transparent 70%);
}

.moon-disc {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='m'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.16' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23m)' opacity='0.1'/%3E%3C/svg%3E"),
    radial-gradient(circle at 42% 38%, #f4ddb0 0%, #ecd096 46%, #ddb877 78%, #cfa659 100%);
  box-shadow:
    inset -8px -10px 26px rgba(146, 106, 44, 0.35),
    0 0 46px rgba(240, 210, 140, 0.45);
}

/* ---------------------------------------------------------------------------
 * 天空云纹带（极淡，缓慢平移）
 * ------------------------------------------------------------------------- */
.cloud-band {
  position: absolute;
  top: 21%;
  left: 0;
  width: 200%;
  height: 24px;
  z-index: 1;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='90' height='22' viewBox='0 0 90 22'%3E%3Cpath d='M4 17 H86 M10 17 Q10 8 19 8 Q27 8 27 14 Q27 18 22 18 M33 17 Q33 7 43 7 Q52 7 52 14 Q52 18 46 18 M58 17 Q58 10 67 10 Q75 10 75 15' fill='none' stroke='rgba(240,232,212,0.9)' stroke-width='1.6'/%3E%3C/svg%3E") repeat-x left center / 90px 22px;
  opacity: 0.1;
  pointer-events: none;
}

/* ---------------------------------------------------------------------------
 * 天空水墨大字标题块
 * ------------------------------------------------------------------------- */
.scene-title {
  position: absolute;
  top: 5%;
  left: 50%;
  transform: translateX(-50%);
  z-index: 5;
  text-align: center;
}

.st-title {
  margin: 0;
}

/* 水墨毛笔字：feDisplacementMap 干笔毛刺 + 单字 fill 微差拟墨迹浓淡 */
.ink-title {
  display: block;
  width: min(50vw, 960px);
  height: auto;
  margin: 0 auto;
  filter:
    drop-shadow(0 3px 2px rgba(10, 20, 35, 0.55))
    drop-shadow(0 0 22px rgba(232, 201, 126, 0.25));
}

/* 书写浮现：clip-path 自左向右逐字擦出（负边距给毛刺留空间） */
.ink-char {
  clip-path: inset(-12% 106% -12% -6%);
}

.st-sub {
  margin: 8px 0 0;
  font-size: clamp(16px, 1.5vw, 22px);
  letter-spacing: 12px;
  color: #f0d9a0;
  text-shadow: 0 1px 2px rgba(10, 20, 35, 0.55);
}

.st-desc {
  margin: 12px 0 0;
  font-size: 13px;
  letter-spacing: 2px;
  color: rgba(244, 238, 222, 0.85);
  text-shadow: 0 1px 2px rgba(10, 20, 35, 0.45);
}

.st-actions {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
}

/* 朱红印章风进入按钮 */
.st-enter {
  display: inline-block;
  padding: 13px 42px;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: 6px;
  color: #f8efdd;
  text-decoration: none;
  border-radius: 8px;
  border: 1px solid rgba(142, 42, 30, 0.6);
  background:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='90' height='90'%3E%3Cfilter id='s'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23s)' opacity='0.16'/%3E%3C/svg%3E"),
    linear-gradient(135deg, var(--sp-vermilion), var(--sp-vermilion-deep));
  box-shadow:
    inset 0 0 0 1.5px rgba(248, 239, 221, 0.35),
    0 6px 22px rgba(10, 20, 35, 0.45);
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.st-enter:hover {
  transform: translateY(-2px);
  box-shadow:
    inset 0 0 0 1.5px rgba(248, 239, 221, 0.4),
    0 10px 28px rgba(10, 20, 35, 0.55);
}

.st-about {
  font-size: 13px;
  letter-spacing: 2px;
  color: rgba(244, 238, 222, 0.8);
  text-decoration: none;
  border-bottom: 1px dashed rgba(227, 200, 140, 0.7);
  padding-bottom: 1px;
  transition: color 0.2s ease;
}

.st-about:hover {
  color: #f0d49a;
}

/* ---------------------------------------------------------------------------
 * 金色戏台地面（上深下浅琥珀 + 木板缝纹理 + 前沿回纹金带）
 * ------------------------------------------------------------------------- */
.stage-floor {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 18%;
  z-index: 1;
  background-image:
    repeating-linear-gradient(0deg, rgba(60, 40, 14, 0.06) 0 2px, transparent 2px 26px),
    linear-gradient(180deg, #a67c33 0%, #c9a35a 26%, #e0c184 58%, #ecd6a4 100%);
  pointer-events: none;
}

.stage-floor::before {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  height: 8px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='8' viewBox='0 0 16 8'%3E%3Cpath d='M0 7.5H16 M2.5 7.5V2.5H13.5V5.5H5.5V4H10.5' fill='none' stroke='%237a5a20' stroke-width='0.9'/%3E%3C/svg%3E") center / 16px 8px repeat-x;
  opacity: 0.42;
}

/* 地面草丛剪影 */
.grass {
  position: absolute;
  bottom: 2.5%;
  z-index: 2;
  width: min(7vw, 104px);
  height: auto;
  opacity: 0.8;
  pointer-events: none;
}

.grass-left {
  left: 6%;
}

.grass-right {
  right: 8%;
  transform: scaleX(-1);
}

/* ---------------------------------------------------------------------------
 * 右侧远处屋舍剪影
 * ------------------------------------------------------------------------- */
.house {
  position: absolute;
  right: 2.5%;
  bottom: 15.5%;
  width: min(16vw, 300px);
  height: auto;
  z-index: 2;
  opacity: 0.66;
  pointer-events: none;
}

/* ---------------------------------------------------------------------------
 * 人物群组背光（戏台幕布暖黄背光）
 * ------------------------------------------------------------------------- */
.troupe-glow {
  position: absolute;
  left: 50%;
  bottom: 8%;
  transform: translateX(-50%);
  width: min(60vw, 1100px);
  height: min(58vh, 640px);
  z-index: 2;
  background: radial-gradient(ellipse at 50% 58%, rgba(250, 220, 145, 0.52), rgba(246, 210, 130, 0.22) 46%, transparent 70%);
  pointer-events: none;
}

/* ---------------------------------------------------------------------------
 * 剧团：人物围桌（视觉中心），脚下接触阴影落地
 * ------------------------------------------------------------------------- */
.troupe {
  position: absolute;
  left: 50%;
  bottom: 4.5%;
  transform: translateX(-50%);
  z-index: 3;
  display: flex;
  align-items: flex-end;
}

.troupe::before {
  content: "";
  position: absolute;
  left: 3%;
  right: 3%;
  bottom: -4px;
  height: 46px;
  z-index: 0;
  background: radial-gradient(ellipse at 50% 50%, rgba(20, 14, 6, 0.3), transparent 68%);
  pointer-events: none;
}

.actor {
  position: relative;
  z-index: 1;
  transform-origin: 50% 100%;
  pointer-events: none;
}

.actor-left {
  height: min(52vh, 590px);
  margin-right: -64px;
  filter: brightness(0.88) drop-shadow(0 12px 16px rgba(5, 10, 20, 0.4));
}

.actor-lead {
  height: min(58vh, 670px);
  margin-left: -172px;
  filter:
    drop-shadow(0 0 24px rgba(240, 210, 140, 0.22))
    drop-shadow(0 16px 20px rgba(5, 10, 20, 0.42));
}

.actor-far {
  height: min(45vh, 480px);
  margin-left: -26px;
  filter: brightness(0.8) drop-shadow(0 10px 14px rgba(5, 10, 20, 0.4));
}

.table-scene {
  position: relative;
  z-index: 3;
  width: min(26vw, 520px);
  pointer-events: none;
}

.table-scene svg {
  display: block;
  width: 100%;
  height: auto;
}

/* ---------------------------------------------------------------------------
 * 前景树石剪影
 * ------------------------------------------------------------------------- */
.tree {
  position: absolute;
  bottom: 3%;
  z-index: 4;
  pointer-events: none;
  filter: brightness(0);
}

.tree-left {
  left: -2.5%;
  height: min(40vh, 460px);
  opacity: 0.85;
}

.tree-right {
  right: -1.5%;
  height: min(38vh, 430px);
  opacity: 0.82;
}

/* 平台数据带（戏台风格：半透明深色底 / 泥金数字 / 楷体标签） */
.stats-band {
  position: absolute;
  left: 18px;
  bottom: 14px;
  z-index: 6;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 16px;
  border-radius: 8px;
  background: rgba(20, 14, 8, 0.52);
  border: 1px solid rgba(201, 162, 79, 0.35);
}

.stat-item {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.stat-item b {
  font-size: 17px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #e3c88c;
  font-family: var(--sp-font-serif);
  font-variant-numeric: tabular-nums;
}

.stat-item i {
  font-style: normal;
  font-size: 11px;
  letter-spacing: 1px;
  color: rgba(240, 232, 212, 0.75);
  font-family: var(--sp-font-serif);
}

.stat-divider {
  width: 1px;
  height: 18px;
  background: rgba(201, 162, 79, 0.4);
}

.stat-badge {
  font-size: 10px;
  letter-spacing: 2px;
  color: rgba(240, 232, 212, 0.6);
  border: 1px solid rgba(201, 162, 79, 0.35);
  border-radius: 3px;
  padding: 1px 6px;
  white-space: nowrap;
}

.scene-credit {
  position: absolute;
  right: 18px;
  bottom: 12px;
  z-index: 5;
  font-size: 11px;
  letter-spacing: 1px;
  color: rgba(60, 42, 16, 0.55);
}

/* ---------------------------------------------------------------------------
 * 幕布层：暖白幕布 + 幕后黑影 + 底沿木杆，升起时整体 translateY(-105%)
 * ------------------------------------------------------------------------- */
.curtain {
  position: fixed;
  inset: 0;
  z-index: 40;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: transform 2s cubic-bezier(0.65, 0, 0.35, 1);
  will-change: transform;
}

.curtain.lifting {
  transform: translateY(-105%);
}

/* 顶部戏台木框 */
.curtain::before {
  content: "";
  height: 14px;
  flex-shrink: 0;
  background: linear-gradient(180deg, #5a3f24, #33220f);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35);
}

.curtain-paper {
  position: relative;
  flex: 1;
  overflow: hidden;
  background-color: #f0e6cd;
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='280' height='280'%3E%3Cfilter id='p'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23p)' opacity='0.05'/%3E%3C/svg%3E"),
    radial-gradient(ellipse 60% 56% at 50% 46%, rgba(255, 248, 226, 0.95), rgba(240, 222, 180, 0.55) 55%, rgba(214, 186, 132, 0.38) 100%);
}

/* 幕后影子：黑化 + 微模糊 + 摇曳游走 */
.shadow {
  position: absolute;
  bottom: 15%;
  transform-origin: 50% 100%;
  filter: brightness(0) blur(1.5px);
  opacity: 0.8;
  pointer-events: none;
}

.shadow-a {
  left: 20%;
  height: 46vh;
  animation: shadow-play-a 6.5s ease-in-out infinite;
}

.shadow-b {
  left: 45%;
  height: 54vh;
  animation: shadow-play-b 7.8s ease-in-out -2s infinite;
}

.shadow-c {
  left: 68%;
  height: 42vh;
  animation: shadow-play-a 5.8s ease-in-out -3.5s infinite;
}

@keyframes shadow-play-a {
  0%, 100% { transform: translateX(0) rotate(-3deg); }
  50% { transform: translateX(26px) rotate(3deg); }
}

@keyframes shadow-play-b {
  0%, 100% { transform: translateX(0) rotate(2.5deg) translateY(0); }
  50% { transform: translateX(-30px) rotate(-2.5deg) translateY(-8px); }
}

.curtain-caption {
  position: absolute;
  left: 50%;
  bottom: 5%;
  transform: translateX(-50%);
  font-size: 15px;
  letter-spacing: 5px;
  color: rgba(87, 73, 59, 0.6);
}

/* 底沿木杆（比幕布略宽，两端如探出戏台） */
.curtain-rod {
  height: 12px;
  flex-shrink: 0;
  margin: 0 -1.5%;
  background: linear-gradient(180deg, #6b4a28, #3a2812);
  border-radius: 6px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.4);
}

/* ---------------------------------------------------------------------------
 * 加载页（黛蓝深夜底，与场景无缝衔接）
 * ------------------------------------------------------------------------- */
.preloader {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background-color: #1b4066;
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='280' height='280'%3E%3Cfilter id='p'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23p)' opacity='0.04'/%3E%3C/svg%3E"),
    linear-gradient(180deg, #2c689e 0%, #3f83bd 34%, #57a0cf 62%, #4b92c4 100%);
}

.pre-seal {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  background:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='90' height='90'%3E%3Cfilter id='s'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23s)' opacity='0.14'/%3E%3C/svg%3E"),
    linear-gradient(145deg, var(--sp-vermilion), var(--sp-vermilion-deep));
  color: #f8efdd;
  font-size: 22px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 0 0 2px rgba(248, 239, 221, 0.55), 0 4px 14px rgba(10, 20, 35, 0.45);
  transform: rotate(-3deg);
}

.pre-title {
  margin-top: 16px;
  font-size: 19px;
  letter-spacing: 8px;
  color: rgba(244, 238, 222, 0.9);
  text-shadow: 0 1px 2px rgba(10, 20, 35, 0.5);
}

.pre-num {
  margin-top: 10px;
  font-size: clamp(56px, 7vw, 88px);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: 2px;
  color: #e3c88c;
  text-shadow: 0 2px 2px rgba(10, 20, 35, 0.5), 0 0 30px rgba(227, 200, 140, 0.25);
  font-variant-numeric: tabular-nums;
}

.pre-pct {
  font-size: 0.42em;
  letter-spacing: 4px;
  margin-left: 4px;
}

.pre-bar {
  margin-top: 18px;
  display: flex;
  align-items: center;
  gap: 8px;
  width: min(46vw, 340px);
}

.pre-bar-cap {
  width: 5px;
  height: 5px;
  flex-shrink: 0;
  background: #e3c88c;
  opacity: 0.85;
  transform: rotate(45deg);
}

.pre-bar-track {
  flex: 1;
  height: 4px;
  border-radius: 2px;
  background: rgba(240, 220, 170, 0.22);
  overflow: hidden;
}

.pre-bar-fill {
  height: 100%;
  border-radius: 2px;
  background: linear-gradient(90deg, #c9a24f, #e3c88c);
  transition: width 0.25s ease;
}

.pre-hint {
  margin-top: 20px;
  font-size: 12px;
  letter-spacing: 3px;
  color: rgba(244, 238, 222, 0.55);
}

.loader-fade-leave-active {
  transition: opacity 0.5s ease;
}

.loader-fade-leave-to {
  opacity: 0;
}

/* ---------------------------------------------------------------------------
 * 动画（循环微动挂 .scene.ready 门控；场景层一次性就位，无分块入场）
 * 时间线：加载页淡出 → 幕后影子 1.6s → 幕布升起 2s（同步亮灯）→ 标题书写 → 按钮
 * ------------------------------------------------------------------------- */
@keyframes moon-breathe {
  0%, 100% { opacity: 0.55; transform: scale(1); }
  50% { opacity: 0.9; transform: scale(1.07); }
}

@keyframes actor-sway {
  0% { transform: rotate(0deg) translateY(0); }
  25% { transform: rotate(-4.5deg) translateY(-9px); }
  50% { transform: rotate(0deg) translateY(0); }
  75% { transform: rotate(4.5deg) translateY(-9px); }
  100% { transform: rotate(0deg) translateY(0); }
}

@keyframes motif-drift {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  50% { transform: translate(-36px, 14px) rotate(-2deg); }
}

/* 水墨字逐字书写：clip-path 自左向右擦出 */
@keyframes ink-write {
  from { clip-path: inset(-12% 106% -12% -6%); }
  to { clip-path: inset(-12% -6% -12% -6%); }
}

/* 副标题/按钮淡入上浮 */
@keyframes sub-in {
  from { opacity: 0; transform: translateY(14px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 背光极慢呼吸（与月晕错开） */
@keyframes glow-slow-breathe {
  0%, 100% { opacity: 0.85; transform: translateX(-50%) scale(1); }
  50% { opacity: 1; transform: translateX(-50%) scale(1.03); }
}

/* 云纹缓慢平移（元素宽 200%，位移一半无缝循环） */
@keyframes cloud-slide {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}

.scene.ready .moon-halo {
  animation: moon-breathe 7.2s ease-in-out infinite;
}

.scene.ready .dragon {
  animation: motif-drift 54s ease-in-out infinite;
}

.scene.ready .cloud-band {
  animation: cloud-slide 80s linear infinite;
}

.scene.ready .troupe-glow {
  animation: glow-slow-breathe 9s ease-in-out infinite;
}

.scene.ready .actor-left {
  animation: actor-sway 5.2s ease-in-out infinite;
}

.scene.ready .actor-lead {
  animation: actor-sway 6.1s ease-in-out -1.2s infinite;
}

.scene.ready .actor-far {
  animation: actor-sway 4.6s ease-in-out -2.3s infinite;
}

.scene.ready .ink-char {
  animation: ink-write 0.65s cubic-bezier(0.6, 0, 0.3, 1) forwards;
}

.scene.ready .ink-char:nth-child(1) { animation-delay: 0s; }
.scene.ready .ink-char:nth-child(2) { animation-delay: 0.55s; }
.scene.ready .ink-char:nth-child(3) { animation-delay: 1.1s; }
.scene.ready .ink-char:nth-child(4) { animation-delay: 1.65s; }

.scene.ready .st-sub {
  animation: sub-in 0.8s ease-out 2.2s both;
}

.scene.ready .st-desc {
  animation: sub-in 0.8s ease-out 2.35s both;
}

.scene.ready .st-actions {
  animation: sub-in 0.4s ease-out 2.7s both;
}

.scene.ready .screen-face {
  animation: face-breathe 5.3s ease-in-out infinite;
}

.scene.ready .screen-glow {
  animation: glow-breathe 5.3s ease-in-out infinite;
}

@keyframes face-breathe {
  0%, 100% { opacity: 0.82; }
  50% { opacity: 1; }
}

@keyframes glow-breathe {
  0%, 100% { opacity: 0.22; }
  50% { opacity: 0.45; }
}

/* 减少动态偏好：全部动画关闭，静态终态（书写遮罩同时解除） */
@media (prefers-reduced-motion: reduce) {
  .moon-halo,
  .dragon,
  .cloud-band,
  .troupe-glow,
  .actor-left,
  .actor-lead,
  .actor-far,
  .st-sub,
  .st-desc,
  .st-actions,
  .screen-face,
  .screen-glow,
  .shadow {
    animation: none !important;
  }

  .curtain {
    transition: none !important;
  }

  .scene-body {
    transition: none !important;
  }

  .ink-char {
    clip-path: none !important;
  }
}

/* 中窄屏：人物收小，影子减一件 */
@media (max-width: 1400px) {
  .actor-left {
    height: min(46vh, 590px);
  }
  .actor-lead {
    height: min(52vh, 670px);
  }
  .actor-far {
    height: min(40vh, 480px);
  }
  .table-scene {
    width: min(23vw, 520px);
  }
  .shadow-c {
    display: none;
  }
}

/* 小屏保护 */
@media (max-width: 700px) {
  .dragon {
    width: 64%;
    top: 16%;
  }
  .house,
  .tree-right,
  .actor-far {
    display: none;
  }
  .actor-left {
    height: 32vh;
  }
  .actor-lead {
    height: 38vh;
    margin-left: -90px;
  }
  .table-scene {
    width: 42vw;
  }
  .ink-title {
    width: 86vw;
  }
  .shadow-c {
    display: none;
  }
  .shadow-a {
    left: 14%;
  }
  .shadow-b {
    left: 52%;
  }
}
</style>
