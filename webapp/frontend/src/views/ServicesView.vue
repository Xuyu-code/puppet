<template>
  <div>
    <div class="sp-page-head">
      <h1 class="sp-serif">文创服务</h1>
      <p>从数字生成到实物载体 —— 平台的服务方案与合作模式（规划展示，非在售商品）</p>
    </div>

    <div class="services-layout">
      <!-- 应用场景 -->
      <section class="sp-card sp-card-pad sp-card-mount">
        <h2 class="sp-section-title">应用场景</h2>
        <p class="svc-lead">
          平台生成的皮影头像可落地为多种文创实物载体。以下为效果示意图，展示「AI 皮影头像 × 传统器物」的变现路径。
        </p>
        <div class="mockup-grid">
          <figure v-for="m in mockups" :key="m.name" class="puppet-card">
            <el-image :src="m.img" :preview-src-list="[m.img]" fit="contain" preview-teleported :alt="m.name" />
            <figcaption>
              <span class="cap-name">{{ m.name }}</span>
            </figcaption>
            <p class="mockup-note">{{ m.note }}</p>
          </figure>
        </div>
      </section>

      <div class="sp-divider">◆</div>

      <!-- 定制服务流程 -->
      <section class="sp-card sp-card-pad sp-card-mount">
        <h2 class="sp-section-title">定制服务流程</h2>
        <svg class="flow-svg" viewBox="0 0 960 130" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="定制服务流程图">
          <defs>
            <marker id="svcArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
              <path d="M 0 1 L 9 5 L 0 9 z" fill="#b98f3e" />
            </marker>
            <linearGradient id="svcNode" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stop-color="#fbf7ec" />
              <stop offset="1" stop-color="#f3ecd8" />
            </linearGradient>
          </defs>
          <g font-family="'STKaiti','KaiTi','Noto Serif SC','SimSun',serif">
            <rect x="10" y="30" width="200" height="70" rx="10" fill="url(#svcNode)" stroke="#b33727" stroke-width="2" />
            <text x="110" y="62" text-anchor="middle" font-size="17" font-weight="700" fill="#262019">提交需求</text>
            <text x="110" y="84" text-anchor="middle" font-size="12" fill="#8a7a66">题材 / 用途 / 数量</text>

            <rect x="256" y="30" width="200" height="70" rx="10" fill="url(#svcNode)" stroke="#b33727" stroke-width="2" />
            <text x="356" y="62" text-anchor="middle" font-size="17" font-weight="700" fill="#262019">AI 生成候选</text>
            <text x="356" y="84" text-anchor="middle" font-size="12" fill="#8a7a66">多方案快速预览</text>

            <rect x="502" y="30" width="200" height="70" rx="10" fill="url(#svcNode)" stroke="#b33727" stroke-width="2" />
            <text x="602" y="62" text-anchor="middle" font-size="17" font-weight="700" fill="#262019">人工精选优化</text>
            <text x="602" y="84" text-anchor="middle" font-size="12" fill="#8a7a66">纹样 / 配色 / 细节</text>

            <rect x="748" y="30" width="200" height="70" rx="10" fill="#b33727" stroke="#b98f3e" stroke-width="2" />
            <text x="848" y="62" text-anchor="middle" font-size="17" font-weight="700" fill="#f8efdd">授权交付</text>
            <text x="848" y="84" text-anchor="middle" font-size="12" fill="#ecd9b8">高清素材包 + 授权说明</text>

            <line x1="212" y1="65" x2="252" y2="65" stroke="#b98f3e" stroke-width="2" marker-end="url(#svcArrow)" />
            <line x1="458" y1="65" x2="498" y2="65" stroke="#b98f3e" stroke-width="2" marker-end="url(#svcArrow)" />
            <line x1="704" y1="65" x2="744" y2="65" stroke="#b98f3e" stroke-width="2" marker-end="url(#svcArrow)" />
          </g>
        </svg>
      </section>

      <div class="sp-divider">◆</div>

      <!-- 合作方案 -->
      <section class="sp-card sp-card-pad sp-card-mount">
        <h2 class="sp-section-title">合作方案</h2>
        <p class="svc-lead">公益为本、造血可持续 —— 三类合作模式并行，均为服务方案规划。</p>
        <div class="plan-grid">
          <div class="plan-card">
            <h3 class="sp-serif"><span class="plan-seal">益</span>公益版</h3>
            <ul>
              <li>面向非遗传承人、学校、公益机构</li>
              <li>平台生成能力长期免费开放</li>
              <li>支持教学、展演、非商业传播用途</li>
              <li>以技术反哺非遗传承与普及</li>
            </ul>
          </div>
          <div class="plan-card">
            <h3 class="sp-serif"><span class="plan-seal">创</span>文创定制</h3>
            <ul>
              <li>面向文创作坊、品牌与活动方</li>
              <li>按素材包计费的设计服务</li>
              <li>AI 生成候选 + 人工精选优化</li>
              <li>高清素材包与授权说明交付</li>
            </ul>
          </div>
          <div class="plan-card">
            <h3 class="sp-serif"><span class="plan-seal">建</span>机构共建</h3>
            <ul>
              <li>面向文化馆、博物馆、教育机构</li>
              <li>皮影数字化馆藏与档案共建</li>
              <li>美育课程包与工作坊输出</li>
              <li>项目制合作，按共建内容议定</li>
            </ul>
          </div>
        </div>
      </section>

      <div class="sp-divider">◆</div>

      <!-- 合作意向 -->
      <section class="sp-card sp-card-pad sp-card-mount">
        <h2 class="sp-section-title">合作意向</h2>
        <p class="svc-lead">
          我们期待与非遗传承人、文化馆与博物馆、文创作坊、中小学及高校美育机构交流合作。
          无论是一件器物的定制尝试，还是一个长期的数字化共建项目，都欢迎来聊。
        </p>
        <p class="svc-contact">
          联系邮箱：<span class="svc-mail">19897077861@163.com</span>
        </p>
        <p class="svc-note">
          小提示：平台目前处于创意计划阶段，本页所示服务方案与合作模式均为规划内容，暂不作为正式商业要约。
        </p>
      </section>
    </div>
  </div>
</template>

<script setup>
import mockBookmark from '../assets/mockups/bookmark.png'
import mockFan from '../assets/mockups/fan.png'
import mockLantern from '../assets/mockups/lantern.png'
import mockPoster from '../assets/mockups/poster.png'

const mockups = [
  { name: '皮影书签', note: '轻薄载体，展演伴手礼与美育教具首选。', img: mockBookmark },
  { name: '皮影团扇', note: '扇面即幕布，适配线下体验与节礼场景。', img: mockFan },
  { name: '皮影灯笼', note: '光影同源，空间装置与节庆氛围营造。', img: mockLantern },
  { name: '主题海报', note: '展览视觉与传播物料的快速产出。', img: mockPoster },
]
</script>

<style scoped>
.services-layout {
  display: flex;
  flex-direction: column;
  gap: 22px;
  max-width: 1080px;
  margin: 0 auto;
}

.svc-lead {
  margin: 0 0 16px;
  font-size: 14px;
  line-height: 1.9;
  color: var(--sp-ink-soft);
}

/* 应用场景 */
.mockup-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.mockup-note {
  margin: 0;
  padding: 8px 10px 10px;
  font-size: 12px;
  line-height: 1.7;
  color: var(--sp-ink-faint);
  background: var(--sp-paper-card);
}

/* 合作方案 */
.plan-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.plan-card {
  border: 1px solid var(--sp-line-strong);
  border-radius: 10px;
  padding: 16px 18px;
  background: var(--sp-paper-card);
  box-shadow: inset 0 0 0 3px var(--sp-paper-card), inset 0 0 0 4px rgba(185, 143, 62, 0.3);
}

.plan-card h3 {
  margin: 0 0 10px;
  font-size: 17px;
  letter-spacing: 2px;
  color: var(--sp-ink);
  display: flex;
  align-items: center;
  gap: 9px;
}

.plan-seal {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  background: linear-gradient(145deg, var(--sp-vermilion), var(--sp-vermilion-deep));
  color: #f8efdd;
  font-size: 13px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 0 0 1.5px rgba(248, 239, 221, 0.5);
  transform: rotate(-3deg);
}

.plan-card ul {
  margin: 0;
  padding-left: 18px;
  font-size: 13px;
  line-height: 2;
  color: var(--sp-ink-soft);
}

/* 合作意向 */
.svc-contact {
  margin: 0 0 14px;
  font-size: 14px;
  letter-spacing: 1px;
  color: var(--sp-ink);
}

.svc-mail {
  color: var(--sp-gold);
  font-weight: 600;
}

.svc-note {
  margin: 0;
  padding: 10px 14px;
  font-size: 13px;
  line-height: 1.8;
  color: var(--sp-ink-soft);
  background: var(--sp-gold-faint);
  border-left: 3px solid var(--sp-gold);
  border-radius: 0 8px 8px 0;
}

@media (max-width: 980px) {
  .mockup-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .plan-grid {
    grid-template-columns: 1fr;
  }
}
</style>
