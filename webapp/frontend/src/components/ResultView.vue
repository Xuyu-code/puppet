<template>
  <div class="result-view">
    <section class="sp-card sp-card-pad sp-card-mount">
      <h2 class="sp-section-title">最终成品</h2>
      <p v-if="prompt" class="prompt-quote">{{ prompt }}</p>
      <div class="final-panel">
        <div class="final-image-wrap">
          <img :src="result.final_url" alt="皮影头像成品" />
        </div>
        <div class="final-side">
          <h3 class="sp-serif">皮影头像 · 推荐方案</h3>
          <p class="elapsed">
            生成耗时 {{ formatElapsed(result.elapsed_seconds) }} · 共 {{ result.candidate_urls.length }} 张候选
          </p>
          <p class="result-note">系统将服务端返回的推荐方案置于首屏，你也可以在下方查看全部候选和评分。</p>
          <h4 class="condition-title">本次使用的条件图</h4>
          <div class="condition-strip">
            <div class="condition-item">
              <el-image
                :src="result.condition_simple_url"
                :preview-src-list="[result.condition_simple_url]"
                fit="contain"
                preview-teleported
              />
              <div class="condition-cap">
                轮廓条件
                <el-tag v-if="result.simple_mode === 'expert'" type="warning" size="small" effect="plain">手动指定</el-tag>
              </div>
            </div>
            <div class="condition-item">
              <el-image
                :src="result.condition_complex_url"
                :preview-src-list="[result.condition_complex_url]"
                fit="contain"
                preview-teleported
              />
              <div class="condition-cap">细节条件</div>
            </div>
          </div>
          <div class="final-actions">
            <el-button type="primary" :icon="Download" @click="onDownload">下载成品图</el-button>
            <el-button :icon="Share" :loading="sharing" @click="onShareCard">生成分享卡</el-button>
            <el-button :icon="Picture" @click="previewVisible = true">查看大图</el-button>
          </div>
        </div>
      </div>
    </section>

    <section class="sp-card sp-card-pad">
      <h2 class="sp-section-title">候选方案与评分</h2>
      <div class="candidate-grid">
        <div
          v-for="(url, index) in result.candidate_urls"
          :key="url"
          class="candidate-card"
          :class="{ selected: index === result.selected_index }"
        >
          <span class="candidate-index">{{ index + 1 }}</span>
          <span v-if="index === result.selected_index" class="candidate-badge sp-serif">推荐</span>
          <el-image :src="url" :preview-src-list="result.candidate_urls" fit="contain" preview-teleported />
          <div class="candidate-scores">
            <div><span>轮廓相似度</span><b>{{ fmtScore(result.candidate_scores[index]?.outline_similarity) }}</b></div>
            <div><span>细节相似度</span><b>{{ fmtScore(result.candidate_scores[index]?.detail_similarity) }}</b></div>
            <div class="score-total"><span>综合得分</span><b>{{ fmtScore(result.candidate_scores[index]?.overall_score) }}</b></div>
          </div>
        </div>
      </div>
    </section>

    <el-image-viewer v-if="previewVisible" :url-list="[result.final_url]" @close="previewVisible = false" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Download, Picture, Share } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import QRCode from 'qrcode'
import { downloadImage } from '../api/client'

const props = defineProps({
  result: { type: Object, required: true },
  prompt: { type: String, default: '' },
  downloadName: { type: String, default: 'shadow-puppet-final.png' },
})

const previewVisible = ref(false)
const sharing = ref(false)

function formatElapsed(seconds) {
  return typeof seconds === 'number' ? `${seconds.toFixed(1)} 秒` : '—'
}

function fmtScore(value) {
  return typeof value === 'number' ? value.toFixed(4) : '—'
}

function onDownload() {
  downloadImage(props.result.final_url, props.downloadName)
}

function loadImage(src) {
  return new Promise((resolve, reject) => {
    const image = new Image()
    image.onload = () => resolve(image)
    image.onerror = reject
    image.src = src
  })
}

async function buildShareCard() {
  const width = 1080
  const height = 1350
  const canvas = document.createElement('canvas')
  canvas.width = width
  canvas.height = height
  const context = canvas.getContext('2d')

  context.fillStyle = '#f6f0e2'
  context.fillRect(0, 0, width, height)
  context.strokeStyle = '#b98f3e'
  context.lineWidth = 3
  context.strokeRect(28, 28, width - 56, height - 56)

  context.fillStyle = '#b33727'
  context.beginPath()
  context.roundRect(70, 72, 64, 64, 9)
  context.fill()
  context.fillStyle = '#f8efdd'
  context.font = '700 34px STKaiti, KaiTi, serif'
  context.textAlign = 'center'
  context.fillText('影', 102, 116)

  context.fillStyle = '#262019'
  context.font = '700 46px STKaiti, KaiTi, serif'
  context.fillText('影脉相承 · 河湟皮影', width / 2 + 45, 116)
  context.fillStyle = '#8a7a66'
  context.font = '22px "Microsoft YaHei", sans-serif'
  context.fillText('让传统纹样在数字光影中重生', width / 2, 182)

  const artwork = await loadImage(props.result.final_url)
  const box = 880
  const x = (width - box) / 2
  const y = 245
  context.fillStyle = '#fff'
  context.fillRect(x, y, box, box)
  context.strokeStyle = 'rgba(62, 48, 32, 0.35)'
  context.strokeRect(x, y, box, box)
  const padding = 28
  const scale = Math.min((box - padding * 2) / artwork.width, (box - padding * 2) / artwork.height)
  const drawWidth = artwork.width * scale
  const drawHeight = artwork.height * scale
  context.drawImage(artwork, x + (box - drawWidth) / 2, y + (box - drawHeight) / 2, drawWidth, drawHeight)

  context.textAlign = 'left'
  context.fillStyle = '#57493b'
  context.font = '22px "Microsoft YaHei", sans-serif'
  context.fillText('AI 皮影头像生成平台', 70, 1202)
  context.fillStyle = '#8a7a66'
  context.fillText(new Date().toISOString().slice(0, 10), 70, 1240)

  const qrData = await QRCode.toDataURL(location.origin, { width: 260, margin: 1 })
  const qr = await loadImage(qrData)
  context.drawImage(qr, width - 210, 1160, 140, 140)
  return new Promise((resolve) => canvas.toBlob(resolve, 'image/png'))
}

async function onShareCard() {
  if (sharing.value) return
  sharing.value = true
  try {
    const blob = await buildShareCard()
    if (!blob) throw new Error('empty blob')
    const url = URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = `hehuang-share-card-${Date.now()}.png`
    anchor.click()
    URL.revokeObjectURL(url)
    ElMessage.success('分享卡已生成并下载。')
  } catch {
    ElMessage.error('分享卡生成失败，请稍后重试。')
  } finally {
    sharing.value = false
  }
}
</script>

<style scoped>
.result-view { display: flex; flex-direction: column; gap: 18px; }
.prompt-quote { margin: 0 0 16px; padding: 10px 14px; color: var(--sp-ink-soft); background: var(--sp-paper); border-left: 3px solid var(--sp-gold); }
.final-panel { display: grid; grid-template-columns: minmax(280px, 520px) 1fr; gap: 28px; align-items: center; }
.final-image-wrap { aspect-ratio: 1; display: grid; place-items: center; overflow: hidden; border: 1px solid var(--sp-line-strong); border-radius: 8px; background: #fff; }
.final-image-wrap img { width: 100%; height: 100%; object-fit: contain; }
.final-side h3 { margin: 0 0 10px; font-size: 22px; letter-spacing: 2px; }
.elapsed, .result-note { color: var(--sp-ink-faint); font-size: 13px; line-height: 1.8; }
.condition-title { margin: 18px 0 8px; color: var(--sp-ink); font-size: 14px; letter-spacing: 1px; }
.condition-strip { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
.condition-item { overflow: hidden; border: 1px solid var(--sp-line-strong); border-radius: 7px; background: #fff; }
.condition-item :deep(.el-image) { display: block; width: 100%; aspect-ratio: 1; }
.condition-cap { display: flex; align-items: center; justify-content: space-between; gap: 6px; padding: 7px 9px; color: var(--sp-ink-soft); background: var(--sp-paper); font-size: 12px; }
.final-actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 20px; }
.candidate-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 14px; }
.candidate-card { position: relative; overflow: hidden; border: 1px solid var(--sp-line-strong); border-radius: 8px; background: #fff; }
.candidate-card.selected { border: 2px solid var(--sp-vermilion); box-shadow: 0 6px 18px rgba(142, 42, 30, 0.14); }
.candidate-card :deep(.el-image) { display: block; width: 100%; aspect-ratio: 1; }
.candidate-scores { padding: 8px 10px 10px; border-top: 1px solid var(--sp-line); background: var(--sp-paper-card); }
.candidate-scores div { display: flex; justify-content: space-between; gap: 8px; padding: 3px 0; color: var(--sp-ink-faint); font-size: 12px; }
.candidate-scores b { color: var(--sp-ink-soft); font-variant-numeric: tabular-nums; }
.candidate-scores .score-total { margin-top: 3px; padding-top: 6px; border-top: 1px dashed var(--sp-line-strong); color: var(--sp-vermilion); }
.candidate-scores .score-total b { color: var(--sp-vermilion); }
.candidate-index, .candidate-badge { position: absolute; z-index: 2; top: 8px; padding: 3px 8px; border-radius: 4px; color: #fff; background: rgba(38, 32, 25, 0.78); font-size: 12px; }
.candidate-index { left: 8px; }
.candidate-badge { right: 8px; background: var(--sp-vermilion); letter-spacing: 1px; }
@media (max-width: 800px) { .final-panel { grid-template-columns: 1fr; } }
</style>
