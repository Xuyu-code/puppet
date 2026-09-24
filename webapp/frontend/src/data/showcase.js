// 皮影元素示例素材清单
// 素材来源：五天晴·皮影资料库（https://piying.design/），详见 src/assets/showcase/CREDITS.md
// tone 用于卡片右下角传统色小 tag，按素材主色调归类（极小面积点缀）
import p01Thumb from '../assets/showcase/p01_thumb.webp'
import p01Full from '../assets/showcase/p01.webp'
import p02Thumb from '../assets/showcase/p02_thumb.webp'
import p02Full from '../assets/showcase/p02.webp'
import p03Thumb from '../assets/showcase/p03_thumb.webp'
import p03Full from '../assets/showcase/p03.webp'
import p04Thumb from '../assets/showcase/p04_thumb.webp'
import p04Full from '../assets/showcase/p04.webp'
import p05Thumb from '../assets/showcase/p05_thumb.webp'
import p05Full from '../assets/showcase/p05.webp'
import p06Thumb from '../assets/showcase/p06_thumb.webp'
import p06Full from '../assets/showcase/p06.webp'
import p07Thumb from '../assets/showcase/p07_thumb.webp'
import p07Full from '../assets/showcase/p07.webp'
import p08Thumb from '../assets/showcase/p08_thumb.webp'
import p08Full from '../assets/showcase/p08.webp'
import p09Thumb from '../assets/showcase/p09_thumb.webp'
import p09Full from '../assets/showcase/p09.webp'
import p10Thumb from '../assets/showcase/p10_thumb.webp'
import p10Full from '../assets/showcase/p10.webp'
import p11Thumb from '../assets/showcase/p11_thumb.webp'
import p11Full from '../assets/showcase/p11.webp'
import p12Thumb from '../assets/showcase/p12_thumb.webp'
import p12Full from '../assets/showcase/p12.webp'
import p13Thumb from '../assets/showcase/p13_thumb.webp'
import p13Full from '../assets/showcase/p13.webp'
import p14Thumb from '../assets/showcase/p14_thumb.webp'
import p14Full from '../assets/showcase/p14.webp'

export const showcaseItems = [
  { name: '武旦 · 穆桂英', category: '人物', tone: 'vermilion', thumb: p01Thumb, full: p01Full },
  { name: '蓝皮尧旦', category: '人物', tone: 'indigo', thumb: p02Thumb, full: p02Full },
  { name: '正旦 · 杨贵妃', category: '人物', tone: 'yellow', thumb: p03Thumb, full: p03Full },
  { name: '鸡盔净', category: '人物', tone: 'jade', thumb: p04Thumb, full: p04Full },
  { name: '神怪变化', category: '神怪', tone: 'vermilion', thumb: p05Thumb, full: p05Full },
  { name: '龙袍王帽生', category: '人物', tone: 'yellow', thumb: p06Thumb, full: p06Full },
  { name: '雷震子', category: '神怪', tone: 'jade', thumb: p07Thumb, full: p07Full },
  { name: '道姑旦', category: '人物', tone: 'indigo', thumb: p08Thumb, full: p08Full },
  { name: '青蛇蛇身', category: '神怪', tone: 'ink', thumb: p09Thumb, full: p09Full },
  { name: '丫鬟旦', category: '人物', tone: 'vermilion', thumb: p10Thumb, full: p10Full },
  { name: '观音菩萨', category: '人物', tone: 'gold', thumb: p11Thumb, full: p11Full },
  { name: '白无常', category: '神怪', tone: 'ink', thumb: p12Thumb, full: p12Full },
  { name: '假山花树 · 牡丹', category: '植物', tone: 'vermilion', thumb: p13Thumb, full: p13Full },
  { name: '假山花树 · 菊花', category: '植物', tone: 'yellow', thumb: p14Thumb, full: p14Full },
]

// 工作台空状态画廊取前 6 张（色调岔开）
export const galleryItems = showcaseItems.slice(0, 6)
