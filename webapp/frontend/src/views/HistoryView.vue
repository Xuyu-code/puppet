<template>
  <div>
    <div class="sp-page-head">
      <h1 class="sp-serif">历史图库</h1>
      <p>历次生成任务的存档，点击卡片可查看候选方案与成品详情。共 {{ total }} 条记录。</p>
    </div>

    <div v-if="loading" class="history-loading" v-loading="loading" element-loading-text="正在翻阅历史档案…" style="height: 240px" />

    <el-empty v-else-if="!items.length" description="暂无历史生成记录，先到生成工作台创作一幅皮影吧。" />

    <div v-else class="history-grid">
      <div v-for="item in items" :key="item.task_id" class="sp-card history-card" @click="openDetail(item)">
        <div class="history-thumb">
          <img v-if="item.thumbnail_url" :src="item.thumbnail_url" :alt="item.task_id" loading="lazy" />
          <span v-else class="failed">{{ item.status === 'failed' ? '生成失败' : '未完成' }}</span>
        </div>
        <div class="history-body">
          <div class="history-time">
            <span>{{ formatTime(item.created_at) }}</span>
            <el-tag v-if="item.status === 'done'" type="success" size="small" effect="plain">完成</el-tag>
            <el-tag v-else-if="item.status === 'failed'" type="danger" size="small" effect="plain">失败</el-tag>
            <el-tag v-else type="warning" size="small" effect="plain">{{ item.status }}</el-tag>
          </div>
          <div class="history-prompt">{{ item.prompt_preview }}</div>
          <div class="history-meta">
            <span v-if="item.elapsed_seconds != null">耗时 {{ item.elapsed_seconds.toFixed(1) }} 秒</span>
            <span v-else>—</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 详情弹窗 -->
    <el-dialog v-model="dialogVisible" width="86%" top="4vh" destroy-on-close>
      <template #header>
        <span class="sp-serif" style="font-size: 18px; letter-spacing: 2px">生成档案 · {{ detail?.task_id }}</span>
      </template>
      <div v-if="detailLoading" v-loading="true" element-loading-text="正在调取档案…" style="height: 200px" />
      <template v-else-if="detail">
        <div class="detail-meta">
          <span>时间：{{ formatTime(detail.created_at) }}</span>
          <template v-if="detail.params">
            <span>候选数量：{{ detail.params.candidate_count }}</span>
            <span>生成步数：{{ detail.params.steps }}</span>
            <span>引导强度：{{ detail.params.guidance_scale }}</span>
            <span>条件强度：{{ detail.params.conditioning_scale }}</span>
            <span>轮廓/细节偏好：{{ detail.params.simple_weight }} / {{ detail.params.complex_weight }}</span>
            <span>随机种子：{{ detail.params.seed }}</span>
            <span>后处理：{{ detail.params.postprocess ? '开' : '关' }}</span>
            <span>轮廓条件：{{ detail.params.simple_mode === 'expert' ? '手动指定' : '自动处理' }}</span>
          </template>
        </div>
        <el-alert
          v-if="detail.status === 'failed'"
          type="error"
          :title="detail.error ? `任务失败：${detail.error}` : '任务失败'"
          :closable="false"
          show-icon
        />
        <ResultView
          v-else-if="detail.result"
          :result="detail.result"
          :prompt="detail.prompt"
          :download-name="`shadow-puppet-${detail.task_id}.png`"
        />
        <el-empty v-else description="该任务没有可展示的结果。" />
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import ResultView from '../components/ResultView.vue'
import { fetchHistory, fetchHistoryDetail, toChineseError } from '../api/client'

const items = ref([])
const total = ref(0)
const loading = ref(false)

const dialogVisible = ref(false)
const detail = ref(null)
const detailLoading = ref(false)

function formatTime(ts) {
  if (typeof ts !== 'number') return '—'
  return new Date(ts * 1000).toLocaleString('zh-CN', { hour12: false })
}

async function openDetail(item) {
  dialogVisible.value = true
  detail.value = null
  detailLoading.value = true
  try {
    detail.value = await fetchHistoryDetail(item.task_id)
  } catch (err) {
    ElMessage.error(toChineseError(err))
    dialogVisible.value = false
  } finally {
    detailLoading.value = false
  }
}

onMounted(async () => {
  loading.value = true
  try {
    const data = await fetchHistory(60, 0)
    items.value = data.items
    total.value = data.total
  } catch (err) {
    ElMessage.error(toChineseError(err))
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 18px;
  margin-bottom: 16px;
  font-size: 13px;
  color: var(--sp-ink-faint);
}
</style>
