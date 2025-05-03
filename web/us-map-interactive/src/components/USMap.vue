<template>
  <div>
    <!-- SVG 地图容器 -->
    <div
      ref="svgContainer"
      class="svg-map"
      @mousemove="updateTooltipPosition"
    ></div>

    <!-- Tooltip 显示当前州与失业率 -->
    <div
      v-if="tooltip.visible"
      class="tooltip"
      :style="{ top: tooltip.y + 'px', left: tooltip.x + 'px' }"
    >
      <strong>{{ tooltip.state }}</strong
      ><br />
      unemployment_rate:{{ tooltip.rate }}%
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from "vue";
import { unemploymentData } from "../data/unemployment.js";
import usMapRaw from "../assets/us-map.svg?raw";

const year = inject("currentYear"); // 从上层组件注入当前年份
const month = inject("currentMonth");
const result = ref(null);
const svgContainer = ref(null);
const stateNameMap = {
  al: "Alabama",
  ca: "California",
  tx: "Texas",
};

// Tooltip 数据
const tooltip = ref({
  visible: false,
  x: 0,
  y: 0,
  state: "",
  rate: "",
});

// 更新 tooltip 位置
const updateTooltipPosition = (e) => {
  tooltip.value.x = e.pageX + 10;
  tooltip.value.y = e.pageY + 10;
};

const getUnemploymentRate = (stateName) => {
  const record = data.find(item => item.state === stateName)
  return record ? record.value : null
};

// 显示 tooltip（当鼠标进入某州时触发）
const showTooltip = async (code) => {
  // console.log(code);
  // const rate = unemploymentData[year.value]?.[code];
  if ((year.value == 2025 && month.value >= 3) || year.value == 2026) {
    const state = stateNameMap[code];
    if (!state) return;
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/unemployment/predict?state=${state}&year=${year.value}&month=${month.value}`
      );
      const data = await response.json();
      console.log("data", data);
      tooltip.value = {
        visible: true,
        x: tooltip.value.x,
        y: tooltip.value.y,
        state: code,
        rate: data?.unemployment_rate ?? "Unknown",
      };
    } catch (error) {
      console.error("Error fetching unemployment data:", error);
      tooltip.value = {
        visible: true,
        x: tooltip.value.x,
        y: tooltip.value.y,
        state: code,
        rate: "False",
      };
    }
  } else {
    const state = stateNameMap[code];
    if (!state) return;
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/unemployment/past?year=${year.value}&month=${month.value}`
      );
      const data = await response.json();
      console.log(data);
      const record = data.find(item => item.state === state)
      tooltip.value = {
        visible: true,
        x: tooltip.value.x,
        y: tooltip.value.y,
        state: code,
        rate: record.value ?? "Unknown",
      };
    } catch (error) {
      console.error("Error fetching unemployment data:", error);
      tooltip.value = {
        visible: true,
        x: tooltip.value.x,
        y: tooltip.value.y,
        state: code,
        rate: "False",
      };
    }
  }

  // tooltip.value = {
  //   visible: true,
  //   x: tooltip.value.x,
  //   y: tooltip.value.y,
  //   state: code,
  //   rate: rate ?? 'Unknown',
  // };
};

// 隐藏 tooltip
const hideTooltip = () => {
  tooltip.value.visible = false;
};

// 加载 SVG 并绑定事件
onMounted(() => {
  if (svgContainer.value) {
    svgContainer.value.innerHTML = usMapRaw;

    const paths = svgContainer.value.querySelectorAll("path");
    paths.forEach((path) => {
      // console.log(path);
      const code = path.classList[0];
      path.addEventListener("mouseenter", () => {
        showTooltip(code);
      });
      path.addEventListener("mouseleave", hideTooltip);
    });
  }
});
</script>

<!-- <script setup>
import { ref, onMounted } from 'vue';
import usMapRaw from '../assets/us-map.svg?raw';
import { unemploymentData } from '../data/unemployment.js';

const selectedYear = ref(2020)
const years = [2020, 2021, 2022]
const svgContainer = ref(null)

const tooltip = ref({
  visible: false,
  content: '',
  x: 0,
  y: 0
})

function getColor(code) {
  const rate = unemploymentData[code]?.[selectedYear.value]
  if (rate === undefined) return '#ccc'
  if (rate < 4) return '#90ee90'
  if (rate < 6) return '#f0e68c'
  return '#f08080'
}

function showTooltip(code, event) {
  const rate = unemploymentData[code]?.[selectedYear.value] ?? '无数据'
  tooltip.value = {
    visible: true,
    content: `${code}: ${rate}%`,
    x: event.clientX,
    y: event.clientY
  }
}

function hideTooltip() {
  tooltip.value.visible = false
}

onMounted(() => {
  svgContainer.value.innerHTML = usMapRaw
  const paths = svgContainer.value.querySelectorAll('path')

  paths.forEach(path => {
    const code = path.classList[0];
    if (!code) return

    // 设置基本样式
    path.setAttribute('fill', getColor(code))
    path.style.cursor = 'pointer'
    path.style.transition = 'transform 0.2s ease, fill 0.2s ease'
    path.style.stroke = '#fff'
    path.style.strokeWidth = '1'

    const bbox = path.getBBox()
    const originX = bbox.x + bbox.width / 2
    const originY = bbox.y + bbox.height / 2
    path.style.transformOrigin = `${originX}px ${originY}px`

    // 悬浮效果
    path.addEventListener('mouseenter', (e) => {
      path.style.fill = '#ff0000'
      path.style.transform = 'scale(1.1)'

      // 使当前州置顶
      path.parentNode.appendChild(path)

      showTooltip(code, e)
    })

    path.addEventListener('mousemove', (e) => {
      tooltip.value.x = e.clientX
      tooltip.value.y = e.clientY
    })

    path.addEventListener('mouseleave', () => {
      path.style.fill = getColor(code)
      path.style.transform = 'scale(1)'
      hideTooltip()
    })
  })
})
</script> -->


<style>
.svg-map {
  width: 100%;
  /* width: 650px; */
  height: auto;
  margin: 20px auto;
  display: flex;
  justify-content: center;
}

.svg-map svg {
  width: 100%;
  height: auto;
}

.svg-map path {
  transition: transform 0.3s ease, fill 0.3s ease;
  cursor: pointer;
  /* transform-box: fill-box;        使 transform-origin 相对于图形本身 */
  transform-origin: center; /* 设置变换原点为图形中心 */
}

.svg-map path:hover {
  transform: scale(1.02);
  z-index: 10;
}

.tooltip {
  position: absolute;
  background: white;
  border: 1px solid #ddd;
  padding: 8px;
  font-size: 14px;
  border-radius: 4px;
  pointer-events: none;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}
</style>
