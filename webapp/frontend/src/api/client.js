import axios from 'axios'

const client = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

export function toChineseError(err) {
  if (err.response) {
    const { status, data } = err.response
    const detail = data && typeof data.detail === 'string' ? data.detail : ''
    if (status === 429) return '请求过于频繁，请稍候再试。'
    if (status === 503) return '生成服务尚未配置或暂不可用。'
    if (status === 404) return '未找到对应的任务或资源。'
    if (status === 400) {
      if (/prompt must not be empty/i.test(detail)) return '提示词不能为空。'
      if (/exceeds the 5MB limit/i.test(detail)) return '线稿超过 5MB 限制，请压缩后重试。'
      if (/not a valid image/i.test(detail)) return '所选文件不是有效图片。'
      if (/Unsupported image format/i.test(detail)) return '图片格式不受支持。'
      return detail ? `请求参数有误：${detail}` : '请求参数有误，请检查输入。'
    }
    return `服务异常（HTTP ${status}），请稍后重试。`
  }
  if (err.code === 'ECONNABORTED') return '请求超时，请稍后重试。'
  return '无法连接后端服务，请确认服务已启动。'
}

export async function fetchPresets() {
  const { data } = await client.get('/presets')
  return data.presets
}

export async function fetchHealth() {
  const { data } = await client.get('/health')
  return data
}

export async function submitGenerate({ lineartFile, simpleLineartFile, prompt, negativePrompt, params }) {
  const form = new FormData()
  form.append('lineart', lineartFile)
  if (simpleLineartFile) form.append('simple_lineart', simpleLineartFile)
  form.append('prompt', prompt)
  if (negativePrompt && negativePrompt.trim()) form.append('negative_prompt', negativePrompt.trim())
  form.append('candidate_count', params.candidate_count)
  form.append('steps', params.steps)
  form.append('guidance_scale', params.guidance_scale)
  form.append('conditioning_scale', params.conditioning_scale)
  form.append('simple_weight', params.simple_weight)
  form.append('complex_weight', params.complex_weight)
  form.append('seed', params.seed)
  form.append('postprocess', params.postprocess)
  const { data } = await client.post('/generate', form)
  return data
}

export async function fetchTask(taskId) {
  const { data } = await client.get(`/tasks/${taskId}`)
  return data
}

export async function fetchStats() {
  const { data } = await client.get('/stats')
  return data
}

export async function translateText(text) {
  const { data } = await client.post('/translate', { text })
  return data
}

export async function fetchHistory(limit = 60, offset = 0) {
  const { data } = await client.get('/history', { params: { limit, offset } })
  return data
}

export async function fetchHistoryDetail(taskId) {
  const { data } = await client.get(`/history/${taskId}`)
  return data
}

export function downloadImage(url, filename = 'shadow-puppet.png') {
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  document.body.appendChild(anchor)
  anchor.click()
  document.body.removeChild(anchor)
}

export default client
