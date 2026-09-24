<template>
  <div>
    <div class="sp-page-head">
      <h1 class="sp-serif">生成工作台</h1>
      <p>上传或绘制线稿，补充角色与视觉描述，生成多组河湟皮影头像候选并保存成品。</p>
    </div>

    <div class="workbench">
      <!-- 左栏：输入区 -->
      <div class="workbench-left">
        <!-- 线稿上传 -->
        <section class="sp-card sp-card-pad sp-card-mount">
          <h2 class="sp-section-title">一 · 上传线稿</h2>
          <button type="button" class="guide-btn" title="什么样的线稿效果好？" @click="guideVisible = true">?</button>
          <div class="src-tabs">
            <button type="button" class="src-tab" :class="{ on: srcTab === 'upload' }" @click="srcTab = 'upload'">
              上传文件
            </button>
            <button type="button" class="src-tab" :class="{ on: srcTab === 'draw' }" @click="srcTab = 'draw'">
              在线画稿
            </button>
          </div>
          <el-upload
            v-show="srcTab === 'upload'"
            class="upload-drop"
            drag
            :auto-upload="false"
            :show-file-list="false"
            accept=".png,.jpg,.jpeg,.webp,.bmp"
            :on-change="onFileChange"
          >
            <el-icon class="upload-hint-icon"><UploadFilled /></el-icon>
            <div class="upload-main-text">拖拽线稿到此处，或 <em>点击选择文件</em></div>
            <div class="upload-sub-text">支持 PNG / JPEG / WEBP / BMP，不超过 5MB</div>
          </el-upload>

          <!-- 在线画板：白底黑笔，鼠标与触屏均可 -->
          <div v-show="srcTab === 'draw'" class="draw-panel">
            <div class="draw-toolbar">
              <span class="draw-label">笔刷</span>
              <button
                v-for="s in BRUSH_SIZES"
                :key="s"
                type="button"
                class="tool-btn"
                :class="{ on: !erasing && brushSize === s }"
                @click="pickBrush(s)"
              >{{ s === 3 ? '细' : s === 6 ? '中' : '粗' }}</button>
              <button type="button" class="tool-btn" :class="{ on: erasing }" @click="erasing = !erasing">橡皮</button>
              <span class="draw-sep"></span>
              <button type="button" class="tool-btn" :disabled="!undoCount" @click="undoStroke">撤销</button>
              <button type="button" class="tool-btn" :disabled="!hasDrawn" @click="clearCanvas">清空</button>
            </div>
            <div class="draw-frame sp-frame-corners">
              <canvas
                ref="canvasRef"
                class="draw-canvas"
                @pointerdown="onDrawStart"
                @pointermove="onDrawMove"
                @pointerup="onDrawEnd"
                @pointercancel="onDrawEnd"
                @pointerleave="onDrawEnd"
              ></canvas>
            </div>
            <div class="draw-hint">
              用鼠标或手指画出头像轮廓与纹样 ·
              <a href="javascript:;" class="guide-link" @click.prevent="guideVisible = true">什么样的线稿效果好？</a>
            </div>
            <el-button class="use-draw-btn" size="small" type="primary" :disabled="!hasDrawn" @click="applyDrawing">
              用作线稿生成
            </el-button>
          </div>

          <div v-if="lineart" class="lineart-preview">
            <img :src="lineart.previewUrl" alt="线稿预览" />
            <div class="lineart-meta">
              <span class="lineart-name">{{ lineart.file.name }}</span>
              <span>{{ (lineart.file.size / 1024).toFixed(1) }} KB</span>
              <span class="param-default-tag">{{ lineartSource === 'draw' ? '当前生效：画板稿' : '当前生效：上传文件' }}</span>
              <el-button size="small" text type="danger" :icon="Delete" @click="clearLineart">
                移除重选
              </el-button>
            </div>
          </div>
        </section>

        <!-- 提示词 -->
        <section class="sp-card sp-card-pad sp-card-mount">
          <h2 class="sp-section-title">二 · 描述提示词</h2>

          <!-- 中文描述助手：选项自动翻译为英文提示词 -->
          <div class="helper">
            <div class="helper-row">
              <el-select v-model="helper.facing" size="small" class="helper-sel" aria-label="朝向">
                <el-option label="向左" value="left" />
                <el-option label="向右" value="right" />
              </el-select>
              <el-select v-model="helper.role" size="small" class="helper-sel" aria-label="角色">
                <el-option label="女角（旦）" value="female" />
                <el-option label="男角（生）" value="male" />
                <el-option label="花脸（净）" value="painted-face" />
                <el-option label="神怪" value="shenguai" />
              </el-select>
              <el-select v-model="helper.crown" size="small" class="helper-sel" aria-label="冠饰">
                <el-option label="凤冠" value="phoenix" />
                <el-option label="王帽" value="wang" />
                <el-option label="宽冠" value="broad" />
                <el-option label="仪冠" value="ceremonial" />
                <el-option label="无冠" value="none" />
              </el-select>
              <el-select v-model="helper.color" size="small" class="helper-sel" aria-label="主色">
                <el-option label="玄黑" value="black" />
                <el-option label="朱红" value="crimson" />
                <el-option label="琥珀黄" value="amber" />
                <el-option label="翠绿" value="green" />
                <el-option label="靛蓝" value="indigo" />
              </el-select>
              <el-select v-model="helper.pattern" size="small" class="helper-sel" aria-label="纹样">
                <el-option label="繁密" value="dense" />
                <el-option label="适中" value="balanced" />
                <el-option label="疏朗" value="light" />
              </el-select>
              <el-button size="small" type="primary" plain @click="applyHelper">生成提示词</el-button>
            </div>
            <div class="helper-note">中文选项会自动转换为适合生成服务的描述</div>
          </div>

          <el-select
            v-model="presetName"
            placeholder="选择示例提示词（选填）"
            style="width: 100%; margin-bottom: 12px"
            :loading="presetsLoading"
            clearable
            @change="onPresetChange"
          >
            <el-option v-for="p in presets" :key="p.name" :label="p.name" :value="p.name" />
          </el-select>
          <el-input
            v-model="prompt"
            type="textarea"
            :rows="6"
            maxlength="2000"
            show-word-limit
            placeholder="描述皮影头像的朝向、冠饰、色彩与纹样，例如：一个向左的皮影头像剪影，整体以玄黑色为主调……"
          />
          <div class="prompt-tools">
            <el-button size="small" :loading="translating" @click="onTranslate">译为英文</el-button>
            <span class="translate-note">将识别角色、朝向、配色和纹样关键词</span>
          </div>
          <div v-if="translateSummary || unrecognized.length" class="translate-result">
            <span v-if="translateSummary" class="translate-summary">{{ translateSummary }}</span>
            <span v-if="unrecognized.length" class="translate-unrec">
              以下词未识别，建议用中文助手或换说法：{{ unrecognized.join('、') }}
            </span>
          </div>
        </section>

        <!-- 高级参数 -->
        <section class="sp-card sp-card-pad sp-card-mount">
          <el-collapse v-model="collapseActive">
            <el-collapse-item name="advanced">
              <template #title>
                <span class="sp-section-title" style="margin: 0">三 · 高级参数（可选）</span>
              </template>
              <div class="param-row" style="align-items: flex-start">
                <span class="param-label">
                  轮廓参考图<span class="param-default-tag">可选</span>
                </span>
                <div class="simple-upload">
                  <div class="simple-upload-hint">
                    不上传时由生成服务自动处理；上传后使用你指定的轮廓参考图。
                  </div>
                  <el-upload
                    :auto-upload="false"
                    :show-file-list="false"
                    accept=".png,.jpg,.jpeg,.webp,.bmp"
                    :on-change="onSimpleFileChange"
                  >
                    <el-button size="small" :icon="UploadFilled">选择条件图</el-button>
                  </el-upload>
                  <div v-if="simpleLineart" class="lineart-preview simple-preview">
                    <img :src="simpleLineart.previewUrl" alt="轮廓参考图预览" />
                    <div class="lineart-meta">
                      <span class="lineart-name">{{ simpleLineart.file.name }}</span>
                      <span>{{ (simpleLineart.file.size / 1024).toFixed(1) }} KB</span>
                      <el-button size="small" text type="danger" :icon="Delete" @click="clearSimpleLineart">移除</el-button>
                    </div>
                  </div>
                </div>
              </div>
              <div class="param-row">
                <span class="param-label">候选数量<span class="param-default-tag">默认 3</span></span>
                <el-input-number v-model="params.candidate_count" :min="1" :max="8" size="small" />
              </div>
              <div class="param-row">
                <span class="param-label">采样步数 steps<span class="param-default-tag">默认 40</span></span>
                <el-input-number v-model="params.steps" :min="1" :max="150" size="small" />
              </div>
              <div class="param-row">
                <span class="param-label">提示词引导强度<span class="param-default-tag">默认 8.0</span></span>
                <el-input-number v-model="params.guidance_scale" :min="1" :max="20" :step="0.5" size="small" />
              </div>
              <div class="param-row">
                <span class="param-label">条件强度<span class="param-default-tag">默认 0.5</span></span>
                <el-input-number v-model="params.conditioning_scale" :min="0" :max="2" :step="0.1" size="small" />
              </div>
              <div class="param-row">
                <span class="param-label">轮廓偏好<span class="param-default-tag">默认 0.4</span></span>
                <el-input-number v-model="params.simple_weight" :min="0" :max="1" :step="0.1" size="small" />
              </div>
              <div class="param-row">
                <span class="param-label">细节偏好<span class="param-default-tag">默认 0.6</span></span>
                <el-input-number v-model="params.complex_weight" :min="0" :max="1" :step="0.1" size="small" />
              </div>
              <div class="param-row">
                <span class="param-label">随机种子<span class="param-default-tag">可复现</span></span>
                <el-input-number v-model="params.seed" :min="0" :max="2147483647" size="small" />
              </div>
              <div class="param-row">
                <span class="param-label">成品后处理<span class="param-default-tag">默认开启</span></span>
                <el-switch v-model="params.postprocess" />
              </div>
            </el-collapse-item>
          </el-collapse>
        </section>

        <el-button
          class="generate-btn"
          type="primary"
          size="large"
          :loading="generating"
          :disabled="!canGenerate"
          @click="onGenerate"
        >
          {{ generating ? '生成中…' : '开 始 生 成' }}
        </el-button>
      </div>

      <!-- 右栏：状态与结果 -->
      <div class="workbench-right">
        <!-- 生成状态 -->
        <section v-if="generating || taskError" class="sp-card sp-card-pad status-card">
          <div class="status-lantern">
            <el-icon :class="{ 'spin-slow': generating }"><Loading v-if="generating" /><WarningFilled v-else /></el-icon>
          </div>
          <div>
            <div class="status-text-main">{{ statusTitle }}</div>
            <div class="status-text-sub">{{ statusSub }}</div>
          </div>
        </section>

        <!-- 空状态：皮影元素示例展示 -->
        <section v-if="!result && !generating" class="sp-card sp-card-pad example-gallery">
          <div class="example-head">
            <div class="empty-glyph sp-serif">影</div>
            <div class="example-head-text">
              <p class="example-title">尚未生成作品</p>
              <p class="empty-sub">
                上传线稿，生成属于你的皮影头像；也可以先到
                <router-link to="/history">历史图库</router-link> 查看既有生成记录
              </p>
            </div>
          </div>
          <div class="example-grid">
            <figure v-for="(item, i) in galleryItems" :key="item.name" class="puppet-card">
              <el-image
                :src="item.thumb"
                :preview-src-list="galleryPreviews"
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

        <!-- 结果 -->
        <ResultView
          v-if="result"
          :result="result"
          :prompt="prompt"
          :download-name="`shadow-puppet-${taskId || 'final'}.png`"
        />
      </div>
    </div>

    <!-- 皮影长廊：彩色皮影元素横向图录 -->
    <ShowcaseStrip class="workbench-strip" />

    <!-- 线稿指南弹窗 -->
    <el-dialog v-model="guideVisible" width="660px" top="7vh" destroy-on-close>
      <template #header>
        <span class="sp-serif" style="font-size: 18px; letter-spacing: 2px">线稿指南 · 什么样的线稿效果好</span>
      </template>
      <div class="guide-compare">
        <figure class="guide-card">
          <img :src="guideGood" alt="好线稿示例" />
          <figcaption>好线稿：闭合轮廓、白底黑线、主体居中、纹样疏密有致</figcaption>
        </figure>
        <figure class="guide-card">
          <img :src="guideBad" alt="不推荐示例" />
          <figcaption>不推荐：照片 / 彩色图——请提供清晰、干净的线稿</figcaption>
        </figure>
      </div>
      <ul class="guide-rules">
        <li><span class="rule-no">一</span>白底黑线，轮廓闭合不断笔</li>
        <li><span class="rule-no">二</span>主体占画面一半以上，居中构图</li>
        <li><span class="rule-no">三</span>纹样疏密适度——太密会糊、太空会素</li>
        <li><span class="rule-no">四</span>在线画稿时，笔画稍粗一点效果更好</li>
      </ul>
      <p class="guide-foot">画好后选预设模板，点击开始生成，约 15 秒出图。</p>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Delete, Loading, UploadFilled, WarningFilled } from '@element-plus/icons-vue'
import ResultView from '../components/ResultView.vue'
import ShowcaseStrip from '../components/ShowcaseStrip.vue'
import { galleryItems } from '../data/showcase'
import guideGood from '../assets/guide/good.png'
import guideBad from '../assets/guide/bad.png'
import {
  fetchPresets,
  fetchTask,
  submitGenerate,
  toChineseError,
  translateText,
} from '../api/client'

const MAX_UPLOAD_BYTES = 5 * 1024 * 1024
const ALLOWED_EXT = ['png', 'jpg', 'jpeg', 'webp', 'bmp']

// ---------------------------------------------------------------------------
// 输入状态
// ---------------------------------------------------------------------------
const lineart = ref(null) // { file, previewUrl }
const simpleLineart = ref(null) // 可选轮廓参考图
const prompt = ref('')
const presets = ref([])
const presetsLoading = ref(false)
const presetName = ref('')
const collapseActive = ref([])
const guideVisible = ref(false) // 线稿指南弹窗

// 与后端公开 API 默认参数保持一致
const params = reactive({
  candidate_count: 3,
  steps: 40,
  guidance_scale: 8.0,
  conditioning_scale: 0.5,
  simple_weight: 0.4,
  complex_weight: 0.6,
  seed: 42,
  postprocess: true,
})

const canGenerate = computed(() => !!lineart.value && prompt.value.trim().length > 0 && !generating.value)

// 空状态示例画廊的大图预览列表
const galleryPreviews = computed(() => galleryItems.map((it) => it.full))

// ---------------------------------------------------------------------------
// 在线画板（与上传文件共用 lineart 槽位，最近操作生效）
// ---------------------------------------------------------------------------
const BRUSH_SIZES = [3, 6, 10]
const CANVAS_SIZE = 512
const srcTab = ref('upload') // upload | draw
const lineartSource = ref('upload') // 当前生效线稿来源：upload | draw
const canvasRef = ref(null)
const brushSize = ref(6)
const erasing = ref(false)
const hasDrawn = ref(false)
const undoCount = ref(0)
let drawCtx = null
let drawing = false
let lastPt = null
const undoStack = []

function initCanvas() {
  const cv = canvasRef.value
  if (!cv) return
  cv.width = CANVAS_SIZE
  cv.height = CANVAS_SIZE
  drawCtx = cv.getContext('2d')
  drawCtx.fillStyle = '#ffffff'
  drawCtx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE)
  drawCtx.lineCap = 'round'
  drawCtx.lineJoin = 'round'
}

function canvasPos(e) {
  const r = canvasRef.value.getBoundingClientRect()
  return {
    x: ((e.clientX - r.left) * CANVAS_SIZE) / r.width,
    y: ((e.clientY - r.top) * CANVAS_SIZE) / r.height,
  }
}

function pushUndo() {
  undoStack.push(drawCtx.getImageData(0, 0, CANVAS_SIZE, CANVAS_SIZE))
  if (undoStack.length > 30) undoStack.shift()
  undoCount.value = undoStack.length
}

function strokeTo(pt) {
  drawCtx.strokeStyle = erasing.value ? '#ffffff' : '#1a1a1a'
  drawCtx.lineWidth = erasing.value ? 18 : brushSize.value
  drawCtx.beginPath()
  drawCtx.moveTo(lastPt.x, lastPt.y)
  drawCtx.lineTo(pt.x, pt.y)
  drawCtx.stroke()
}

function onDrawStart(e) {
  if (!drawCtx) return
  canvasRef.value.setPointerCapture(e.pointerId)
  pushUndo()
  drawing = true
  lastPt = canvasPos(e)
  strokeTo(lastPt) // 单点也落墨
  hasDrawn.value = true
}

function onDrawMove(e) {
  if (!drawing || !drawCtx) return
  const pt = canvasPos(e)
  strokeTo(pt)
  lastPt = pt
}

function onDrawEnd() {
  drawing = false
}

function pickBrush(s) {
  brushSize.value = s
  erasing.value = false
}

function undoStroke() {
  const prev = undoStack.pop()
  undoCount.value = undoStack.length
  if (prev) {
    drawCtx.putImageData(prev, 0, 0)
    // 撤销后保守保留 hasDrawn（可用「清空」重置状态）
  }
}

function clearCanvas() {
  pushUndo()
  drawCtx.fillStyle = '#ffffff'
  drawCtx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE)
  hasDrawn.value = false
}

function applyDrawing() {
  const cv = canvasRef.value
  if (!cv || !hasDrawn.value) return
  cv.toBlob((blob) => {
    if (!blob) return
    const file = new File([blob], 'canvas-lineart.png', { type: 'image/png' })
    lineart.value = { file, previewUrl: cv.toDataURL('image/png') }
    lineartSource.value = 'draw'
    ElMessage.success('画稿已作为线稿，可直接开始生成。')
  }, 'image/png')
}

function onFileChange(uploadFile) {
  const file = uploadFile.raw
  if (!file) return
  const ext = (file.name.split('.').pop() || '').toLowerCase()
  if (!ALLOWED_EXT.includes(ext)) {
    ElMessage.error('图片格式不支持，请使用 PNG / JPEG / WEBP / BMP。')
    return
  }
  if (file.size > MAX_UPLOAD_BYTES) {
    ElMessage.error('线稿文件超过 5MB 限制，请压缩后再上传。')
    return
  }
  const reader = new FileReader()
  reader.onload = (e) => {
    lineart.value = { file, previewUrl: e.target.result }
    lineartSource.value = 'upload'
  }
  reader.readAsDataURL(file)
}

function clearLineart() {
  lineart.value = null
}

function onSimpleFileChange(uploadFile) {
  const file = uploadFile.raw
  if (!file) return
  const ext = (file.name.split('.').pop() || '').toLowerCase()
  if (!ALLOWED_EXT.includes(ext)) {
    ElMessage.error('图片格式不支持，请使用 PNG / JPEG / WEBP / BMP。')
    return
  }
  if (file.size > MAX_UPLOAD_BYTES) {
    ElMessage.error('轮廓条件图超过 5MB 限制，请压缩后再上传。')
    return
  }
  const reader = new FileReader()
  reader.onload = (event) => {
    simpleLineart.value = { file, previewUrl: event.target.result }
  }
  reader.readAsDataURL(file)
}

function clearSimpleLineart() {
  simpleLineart.value = null
}

function onPresetChange(name) {
  const hit = presets.value.find((p) => p.name === name)
  if (hit) prompt.value = hit.prompt
}

// ---------------------------------------------------------------------------
// 中文描述助手：中文选项组合为可编辑的英文提示词
// ---------------------------------------------------------------------------
const HELPER_MAP = {
  facing: {
    left: 'left-facing side-profile',
    right: 'right-facing side-profile',
  },
  role: {
    female: 'female puppet head',
    male: 'male puppet head',
    'painted-face': 'painted-face male puppet head',
    shenguai: 'shenguai mythical puppet head',
  },
  crown: {
    phoenix: 'phoenix crown with winged side ornaments, refined ceremonial phoenix headwear',
    wang: 'royal wang hat with layered forehead band, carved brow plate',
    broad: 'broad horizontal crown silhouette, wide ceremonial crown spread, branched segmented crown top',
    ceremonial:
      'ceremonial crown with layered forehead band, hanging side decoration, prominent rear hanging side ornament',
    none: 'simple hair bun without crown, clean forehead line',
  },
  color: {
    black: 'deep black palette, strong black-white traditional color contrast',
    crimson: 'crimson red palette with black contour lines',
    amber: 'amber yellow palette with warm golden ornaments',
    green: 'jade green palette with black contour lines',
    indigo: 'indigo blue palette with black contour lines',
  },
  pattern: {
    dense: 'intricate hollow-carved leather ornament, pierced floral windows, dense facial carving density, rich layered motifs',
    balanced: 'balanced filled ornament structure, restrained carved window detail, moderate carving density',
    light: 'minimal ornament structure, sparse carved detail, light facial carving density, clean open surfaces',
  },
}

const helper = reactive({
  facing: 'left',
  role: 'female',
  crown: 'ceremonial',
  color: 'black',
  pattern: 'balanced',
})

function applyHelper() {
  prompt.value = [
    'Qinghai Hehuang shadow puppet head portrait, authentic Hehuang style Chinese folk shadow puppetry artifact, single isolated character head for shadow puppet generation',
    `${HELPER_MAP.facing[helper.facing]} ${HELPER_MAP.role[helper.role]}`,
    HELPER_MAP.crown[helper.crown],
    HELPER_MAP.pattern[helper.pattern],
    HELPER_MAP.color[helper.color],
    'pure white background, centered composition, isolated subject, high visual clarity, strong traditional shadow puppet identity',
  ].join(', ')
  unrecognized.value = []
  ElMessage.success('已按选项生成英文提示词，可继续编辑。')
}

// ---------------------------------------------------------------------------
// 译为英文：离线规则翻译（后端 /api/translate），透明填回可编辑
// ---------------------------------------------------------------------------
const CJK_RE = /[一-鿿]/
const translating = ref(false)
const unrecognized = ref([])
const translateSummary = ref('')

async function onTranslate() {
  const text = prompt.value.trim()
  if (!text) {
    ElMessage.warning('请先输入描述。')
    return
  }
  if (!CJK_RE.test(text)) {
    ElMessage.info('当前已是英文，无需翻译。')
    return
  }
  translating.value = true
  try {
    const r = await translateText(text)
    unrecognized.value = r.unrecognized || []
    translateSummary.value = r.summary_zh || ''
    if (!r.text_en) {
      ElMessage.warning('没有识别到可用的皮影关键词，请换种说法，或改用上方中文助手。')
      return
    }
    prompt.value = r.text_en
    ElMessage.success(`已译为英文（识别 ${r.recognized.length} 个关键词），可继续编辑。`)
  } catch (err) {
    ElMessage.error(toChineseError(err))
  } finally {
    translating.value = false
  }
}

// ---------------------------------------------------------------------------
// 生成与轮询
// ---------------------------------------------------------------------------
const generating = ref(false)
const taskId = ref('')
const taskStatus = ref('') // queued | running | done | failed
const queuePosition = ref(null)
const result = ref(null)
const taskError = ref('')

let pollTimer = null
let consecutivePollErrors = 0

const statusTitle = computed(() => {
  if (taskError.value) return '生成失败'
  if (taskStatus.value === 'queued') return '排队等待中'
  if (taskStatus.value === 'running') return '生成服务处理中'
  return '任务提交中'
})

const statusSub = computed(() => {
  if (taskError.value) return taskError.value
  if (taskStatus.value === 'queued') {
    const pos = queuePosition.value
    return pos != null
      ? `排队位置：第 ${pos} 位（第 1 位为下一个执行），每 1.5 秒自动刷新`
      : '已入队，等待调度…'
  }
  if (taskStatus.value === 'running') return '生成服务正在处理候选方案，请稍候…'
  return '正在将任务提交到队列…'
})

async function onGenerate() {
  if (!lineart.value) {
    ElMessage.warning('请先上传线稿。')
    return
  }
  if (!prompt.value.trim()) {
    ElMessage.warning('提示词不能为空，请输入或选择预设模板。')
    return
  }
  if (CJK_RE.test(prompt.value)) {
    ElMessage.warning('提示词仍为中文：请先点击「译为英文」或使用中文助手。')
    return
  }
  generating.value = true
  taskError.value = ''
  result.value = null
  taskStatus.value = ''
  queuePosition.value = null
  try {
    const resp = await submitGenerate({
      lineartFile: lineart.value.file,
      simpleLineartFile: simpleLineart.value ? simpleLineart.value.file : null,
      prompt: prompt.value.trim(),
      params,
    })
    taskId.value = resp.task_id
    taskStatus.value = 'queued'
    queuePosition.value = resp.position
    startPolling(resp.task_id)
  } catch (err) {
    taskError.value = toChineseError(err)
    ElMessage.error(taskError.value)
    generating.value = false
  }
}

function startPolling(id) {
  stopPolling()
  consecutivePollErrors = 0
  pollTimer = setInterval(() => pollOnce(id), 1500)
  pollOnce(id)
}

function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

async function pollOnce(id) {
  try {
    const t = await fetchTask(id)
    consecutivePollErrors = 0
    taskStatus.value = t.status
    queuePosition.value = t.position
    if (t.status === 'done') {
      result.value = t.result
      generating.value = false
      stopPolling()
      ElMessage.success('生成完成，已为您推荐综合得分最高的候选。')
    } else if (t.status === 'failed') {
      taskError.value = t.error ? `生成失败：${t.error}` : '生成失败，请调整参数后重试。'
      ElMessage.error(taskError.value)
      generating.value = false
      stopPolling()
    }
  } catch (err) {
    consecutivePollErrors += 1
    if (consecutivePollErrors >= 5) {
      taskError.value = toChineseError(err)
      ElMessage.error(taskError.value)
      generating.value = false
      stopPolling()
    }
  }
}

onMounted(async () => {
  initCanvas()
  presetsLoading.value = true
  try {
    presets.value = await fetchPresets()
  } catch (err) {
    ElMessage.warning(`预设模板加载失败：${toChineseError(err)}`)
  } finally {
    presetsLoading.value = false
  }
})

onBeforeUnmount(stopPolling)
</script>

<style scoped>
.simple-upload {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.simple-upload-hint {
  margin: 0;
  font-size: 12px;
  line-height: 1.5;
  color: var(--sp-ink-faint);
  text-align: right;
  max-width: 260px;
}

.simple-preview {
  width: 120px;
}

.empty-glyph {
  width: 56px;
  height: 56px;
  border-radius: 8px;
  flex-shrink: 0;
  background: linear-gradient(145deg, var(--sp-vermilion), var(--sp-vermilion-deep));
  color: #f8efdd;
  font-size: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 0 0 2.5px rgba(248, 239, 221, 0.5), 0 4px 12px rgba(142, 42, 30, 0.28);
}

.empty-sub {
  margin: 0;
  font-size: 13px;
  letter-spacing: 1px;
  color: var(--sp-ink-faint);
}

.empty-sub a {
  color: var(--sp-vermilion);
}

.workbench-strip {
  margin-top: 22px;
}

/* 线稿来源切换 */
.src-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.src-tab {
  flex: 1;
  padding: 7px 0;
  font-size: 13px;
  letter-spacing: 2px;
  color: var(--sp-ink-soft);
  background: var(--sp-paper);
  border: 1px solid var(--sp-line-strong);
  border-radius: 7px;
  cursor: pointer;
  transition: color 0.2s ease, border-color 0.2s ease, background-color 0.2s ease;
}

.src-tab.on {
  color: #f8efdd;
  background: linear-gradient(135deg, var(--sp-vermilion), var(--sp-vermilion-deep));
  border-color: rgba(142, 42, 30, 0.55);
}

/* 在线画板 */
.draw-panel {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.draw-toolbar {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.draw-label {
  font-size: 12px;
  letter-spacing: 1px;
  color: var(--sp-ink-faint);
  margin-right: 2px;
}

.tool-btn {
  padding: 4px 10px;
  font-size: 12px;
  letter-spacing: 1px;
  color: var(--sp-ink-soft);
  background: var(--sp-paper);
  border: 1px solid var(--sp-line-strong);
  border-radius: 6px;
  cursor: pointer;
  transition: color 0.18s ease, border-color 0.18s ease, background-color 0.18s ease;
}

.tool-btn.on {
  color: var(--sp-vermilion);
  border-color: var(--sp-vermilion);
  background: rgba(179, 55, 39, 0.06);
}

.tool-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.draw-sep {
  width: 1px;
  height: 16px;
  margin: 0 4px;
  background: var(--sp-line-strong);
}

.draw-frame {
  position: relative;
  padding: 16px;
  background: var(--sp-paper);
  border: 1px solid var(--sp-line-strong);
  border-radius: 8px;
  box-shadow:
    inset 0 0 0 4px var(--sp-paper),
    inset 0 0 0 5px rgba(185, 143, 62, 0.42);
}

.draw-canvas {
  display: block;
  width: 100%;
  aspect-ratio: 1;
  background: #fff;
  border-radius: 4px;
  cursor: crosshair;
  touch-action: none;
}

.draw-hint {
  font-size: 12px;
  letter-spacing: 1px;
  color: var(--sp-ink-faint);
  text-align: center;
}

.use-draw-btn {
  align-self: center;
  letter-spacing: 2px;
}

/* 线稿指南入口与弹窗 */
.guide-btn {
  position: absolute;
  top: 14px;
  right: 16px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid var(--sp-gold-soft);
  background: transparent;
  color: var(--sp-gold);
  font-size: 13px;
  line-height: 1;
  cursor: pointer;
  transition: color 0.18s ease, background-color 0.18s ease, border-color 0.18s ease;
}

.guide-btn:hover {
  color: #f8efdd;
  background: var(--sp-vermilion);
  border-color: var(--sp-vermilion);
}

.guide-link {
  color: var(--sp-vermilion);
  text-decoration: none;
  border-bottom: 1px dashed var(--sp-gold);
  padding-bottom: 1px;
}

.guide-compare {
  display: flex;
  gap: 16px;
}

.guide-card {
  flex: 1;
  margin: 0;
  border: 1px solid var(--sp-line-strong);
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
}

.guide-card img {
  display: block;
  width: 100%;
}

.guide-card figcaption {
  padding: 8px 10px;
  font-size: 12px;
  line-height: 1.7;
  color: var(--sp-ink-soft);
  background: var(--sp-paper-card);
  border-top: 1px solid var(--sp-line);
}

.guide-rules {
  margin: 16px 0 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.guide-rules li {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  letter-spacing: 1px;
  color: var(--sp-ink-soft);
}

.rule-no {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  flex-shrink: 0;
  background: linear-gradient(145deg, var(--sp-vermilion), var(--sp-vermilion-deep));
  color: #f8efdd;
  font-size: 11px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 0 0 1px rgba(248, 239, 221, 0.4);
}

.guide-foot {
  margin: 14px 0 0;
  padding-top: 12px;
  border-top: 1px dashed var(--sp-line-strong);
  font-size: 13px;
  letter-spacing: 1px;
  color: var(--sp-ink-faint);
  text-align: center;
}

/* 中文描述助手 */
.helper {
  margin-bottom: 12px;
  padding: 10px 12px;
  background: var(--sp-paper);
  border: 1px solid var(--sp-line);
  border-radius: 8px;
}

.helper-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.helper-sel {
  width: 96px;
  flex-shrink: 0;
}

.helper-note {
  margin-top: 7px;
  font-size: 11px;
  letter-spacing: 1px;
  color: var(--sp-ink-faint);
}

/* 译为英文工具行 */
.prompt-tools {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.translate-note {
  font-size: 11px;
  letter-spacing: 1px;
  color: var(--sp-ink-faint);
}

.translate-result {
  margin-top: 6px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.translate-summary {
  font-size: 12px;
  letter-spacing: 1px;
  line-height: 1.7;
  color: var(--sp-ink-soft);
}

.translate-unrec {
  font-size: 12px;
  letter-spacing: 1px;
  line-height: 1.7;
  color: var(--sp-vermilion);
}
</style>
