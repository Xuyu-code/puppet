<template>
  <div>
    <div class="sp-page-head">
      <h1 class="sp-serif">实践风采</h1>
      <p>平台落地实践的记录与回声 —— 走访、课堂与影像，将于 2026 年 9 月实践活动后据实更新。</p>
    </div>

    <div class="voices-layout">
      <!-- 传承人评价 -->
      <section class="sp-card sp-card-pad sp-card-mount">
        <h2 class="sp-section-title">传承人评价</h2>
        <div class="quote-grid">
          <figure v-for="i in 3" :key="i" class="quote-card">
            <div class="quote-seal sp-serif">言</div>
            <blockquote class="quote-text">走访活动后填入艺人评价</blockquote>
            <figcaption class="quote-meta">河湟皮影传承人 · 待走访</figcaption>
          </figure>
        </div>
      </section>

      <div class="sp-divider">◆</div>

      <!-- 学生作品墙 -->
      <section class="sp-card sp-card-pad sp-card-mount">
        <h2 class="sp-section-title">
          学生作品墙
          <span class="update-tag">美育课堂作品 · 2026 年 9 月更新</span>
        </h2>
        <div class="wall-grid">
          <div v-for="i in 6" :key="i" class="wall-slot">
            <span class="wall-seal sp-serif">影</span>
            <span class="wall-text">课堂作品占位</span>
          </div>
        </div>
      </section>

      <div class="sp-divider">◆</div>

      <!-- 活动影像 -->
      <section class="sp-card sp-card-pad sp-card-mount">
        <h2 class="sp-section-title">
          活动影像
          <span class="update-tag">实践影像记录 · 2026 年 9 月更新</span>
        </h2>
        <div class="wall-grid wall-grid-media">
          <div v-for="i in 4" :key="i" class="wall-slot wall-slot-media">
            <span class="wall-seal sp-serif">影</span>
            <span class="wall-text">活动照片占位</span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.voices-layout {
  display: flex;
  flex-direction: column;
  gap: 22px;
  max-width: 1080px;
  margin: 0 auto;
}

.update-tag {
  margin-left: auto;
  font-size: 12px;
  font-weight: 400;
  letter-spacing: 1px;
  color: var(--sp-ink-faint);
}

/* 传承人评价：引语占位卡 */
.quote-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.quote-card {
  margin: 0;
  padding: 24px 18px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-align: center;
  background: var(--sp-paper);
  border: 1.5px dashed var(--sp-line-strong);
  border-radius: 10px;
}

.quote-seal {
  width: 36px;
  height: 36px;
  border-radius: 7px;
  background: linear-gradient(145deg, var(--sp-vermilion), var(--sp-vermilion-deep));
  color: #f8efdd;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 0 0 2px rgba(248, 239, 221, 0.5);
  transform: rotate(-3deg);
}

.quote-text {
  margin: 0;
  font-size: 13px;
  letter-spacing: 2px;
  line-height: 1.9;
  color: var(--sp-ink-faint);
}

.quote-meta {
  font-size: 11px;
  letter-spacing: 1px;
  color: var(--sp-gold);
}

/* 作品墙 / 活动影像占位格 */
.wall-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.wall-grid-media {
  grid-template-columns: repeat(4, 1fr);
}

.wall-slot {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: var(--sp-paper);
  border: 1.5px dashed var(--sp-line-strong);
  border-radius: 10px;
}

.wall-slot-media {
  aspect-ratio: 4 / 3;
}

.wall-seal {
  width: 30px;
  height: 30px;
  border-radius: 6px;
  background: linear-gradient(145deg, var(--sp-vermilion), var(--sp-vermilion-deep));
  color: #f8efdd;
  font-size: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 0 0 1.5px rgba(248, 239, 221, 0.5);
  opacity: 0.75;
  transform: rotate(-3deg);
}

.wall-text {
  font-size: 12px;
  letter-spacing: 2px;
  color: var(--sp-ink-faint);
}

@media (max-width: 980px) {
  .quote-grid {
    grid-template-columns: 1fr;
  }
  .wall-grid,
  .wall-grid-media {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
