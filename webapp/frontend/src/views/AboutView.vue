<template>
  <div>
    <div class="sp-page-head about-head" style="text-align: center">
      <img class="sp-silhouette sp-silhouette-deco about-head-deco" :src="puppetSilhouette" alt="" aria-hidden="true" />
      <h1 class="sp-serif">关于本系统</h1>
      <p>非遗皮影艺术的数字创作实践 —— 产品、流程与文化背景</p>
    </div>

    <div class="about-layout">
      <section class="sp-card sp-card-pad about-prose">
        <h2 class="sp-section-title">河湟皮影 · 非遗简介</h2>
        <p>
          河湟皮影戏流传于青海河湟谷地，是国家级非物质文化遗产的重要组成。影人以牛皮雕镂，
          刀法洗练、色彩浓烈，人物轮廓与镂空纹饰承载着鲜明的地域审美特征。
        </p>
        <p>
          本平台以数字工具辅助皮影头像创作，让用户从一张线稿出发，快速获得可继续设计、展示和归档的
          皮影头像方案，为非遗传播、美育体验和文创设计提供更直观的创作入口。
        </p>
      </section>

      <div class="sp-divider">◆</div>

      <section class="sp-card sp-card-pad">
        <h2 class="sp-section-title">平台流程</h2>
        <p class="about-prose flow-intro">
          平台将输入、生成、预览与归档组织成一条完整工作流。生成能力通过受保护的服务接口接入，
          Web 层只负责产品交互、任务调度和结果管理。
        </p>
        <div class="flow-grid" aria-label="平台流程">
          <div class="flow-node"><b>1</b><strong>线稿输入</strong><span>上传图片或在线绘制</span></div>
          <span class="flow-arrow">→</span>
          <div class="flow-node"><b>2</b><strong>描述编辑</strong><span>组合角色与视觉偏好</span></div>
          <span class="flow-arrow">→</span>
          <div class="flow-node"><b>3</b><strong>任务生成</strong><span>异步排队并跟踪状态</span></div>
          <span class="flow-arrow">→</span>
          <div class="flow-node"><b>4</b><strong>预览归档</strong><span>比较候选并下载成品</span></div>
        </div>
      </section>

      <div class="sp-divider">◆</div>

      <section class="sp-card sp-card-pad">
        <h2 class="sp-section-title">工程要点</h2>
        <ul class="tech-list">
          <li><strong>创作输入</strong>：拖拽上传与在线画板共用统一校验、预览和提交逻辑。</li>
          <li><strong>交互设计</strong>：提示词助手、任务状态反馈、候选浏览、下载与分享卡形成闭环。</li>
          <li><strong>任务管理</strong>：FastAPI 串行队列处理耗时请求，前端轮询状态并展示排队位置。</li>
          <li><strong>数据归档</strong>：SQLite 保存任务参数、状态、耗时和结果索引，支持历史回看。</li>
          <li><strong>服务解耦</strong>：统一 Provider 接口连接私有生成服务，模型资产与平台代码分离。</li>
        </ul>
      </section>

      <div class="sp-divider">◆</div>
      <ShowcaseStrip />
    </div>
  </div>
</template>

<script setup>
import puppetSilhouette from '../assets/puppet-silhouette.png'
import ShowcaseStrip from '../components/ShowcaseStrip.vue'
</script>

<style scoped>
.about-head { position: relative; }
.about-head-deco { top: -16px; right: 7%; }
.flow-intro { margin-bottom: 20px; color: var(--sp-ink-soft); font-size: 14px; line-height: 1.9; }
.flow-grid { display: grid; grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr; align-items: center; gap: 12px; }
.flow-node { min-height: 112px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 7px; padding: 14px; text-align: center; border: 1px solid var(--sp-line-strong); border-radius: 8px; background: var(--sp-paper-card); }
.flow-node b { width: 24px; height: 24px; display: grid; place-items: center; border-radius: 4px; color: #f8efdd; background: var(--sp-vermilion); }
.flow-node strong { color: var(--sp-ink); font-family: var(--sp-font-serif); letter-spacing: 1px; }
.flow-node span { color: var(--sp-ink-faint); font-size: 12px; }
.flow-arrow { color: var(--sp-gold); font-size: 22px; }
.tech-list { margin: 0; padding-left: 22px; color: var(--sp-ink-soft); font-size: 14px; line-height: 2.1; }
.tech-list strong { color: var(--sp-vermilion); font-family: var(--sp-font-serif); }
@media (max-width: 900px) {
  .flow-grid { grid-template-columns: 1fr; }
  .flow-arrow { transform: rotate(90deg); justify-self: center; }
}
</style>
