<template>
  <div>
    <div
      ref="svgContainer"
      class="svg-map"
      @mousemove="updateTooltipPosition"
    ></div>

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
import usMapRaw from "../assets/us-map.svg?raw";

const year = inject("currentYear"); 
const month = inject("currentMonth");
const result = ref(null);
const svgContainer = ref(null);
const stateNameMap = {
  al: "Alabama",
  ak: "Alaska",
  az: "Arizona",
  ar: "Arkansas",
  ca: "California",
  co: "Colorado",
  ct: "Connecticut",
  de: "Delaware",
  fl: "Florida",
  ga: "Georgia",
  hi: "Hawaii",
  id: "Idaho",
  il: "Illinois",
  in: "Indiana",
  ia: "Iowa",
  ks: "Kansas",
  ky: "Kentucky",
  la: "Louisiana",
  me: "Maine",
  md: "Maryland",
  ma: "Massachusetts",
  mi: "Michigan",
  mn: "Minnesota",
  ms: "Mississippi",
  mo: "Missouri",
  mt: "Montana",
  ne: "Nebraska",
  nv: "Nevada",
  nh: "New Hampshire",
  nj: "New Jersey",
  nm: "New Mexico",
  ny: "New York",
  nc: "North Carolina",
  nd: "North Dakota",
  oh: "Ohio",
  ok: "Oklahoma",
  or: "Oregon",
  pa: "Pennsylvania",
  ri: "Rhode Island",
  sc: "South Carolina",
  sd: "South Dakota",
  tn: "Tennessee",
  tx: "Texas",
  ut: "Utah",
  vt: "Vermont",
  va: "Virginia",
  wa: "Washington",
  wv: "West Virginia",
  wi: "Wisconsin",
  wy: "Wyoming"
};

const tooltip = ref({
  visible: false,
  x: 0,
  y: 0,
  state: "",
  rate: "",
});

const updateTooltipPosition = (e) => {
  tooltip.value.x = e.pageX + 10;
  tooltip.value.y = e.pageY + 10;
};

const showTooltip = async (code) => {
  // console.log(code);
  // const rate = unemploymentData[year.value]?.[code];
  if ((year.value == 2025 && month.value >= 3) || year.value == 2026) {
    const state = stateNameMap[code];
    if (!state) return;
    try {
      const response = await fetch(
        `/api/unemployment/predict?state=${state}&year=${year.value}&month=${month.value}`
      );
      const data = await response.json();
      console.log("data", data);
      tooltip.value = {
        visible: true,
        x: tooltip.value.x,
        y: tooltip.value.y,
        state: state,
        rate: data?.unemployment_rate.toFixed(2) ?? "Unknown",
      };
    } catch (error) {
      console.error("Error fetching unemployment data:", error);
      tooltip.value = {
        visible: true,
        x: tooltip.value.x,
        y: tooltip.value.y,
        state: state,
        rate: "False",
      };
    }
  } else {
    const state = stateNameMap[code];
    if (!state) return;
    try {
      const response = await fetch(
        `/api/unemployment/past?year=${year.value}&month=${month.value}`
      );
      const data = await response.json();
      console.log(data);
      const record = data.find(item => item.state === state)
      tooltip.value = {
        visible: true,
        x: tooltip.value.x,
        y: tooltip.value.y,
        state: state,
        rate: record.value ?? "Unknown",
      };
    } catch (error) {
      console.error("Error fetching unemployment data:", error);
      tooltip.value = {
        visible: true,
        x: tooltip.value.x,
        y: tooltip.value.y,
        state: state,
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

const hideTooltip = () => {
  tooltip.value.visible = false;
};

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

    // 
    path.addEventListener('mouseenter', (e) => {
      path.style.fill = '#ff0000'
      path.style.transform = 'scale(1.1)'

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
  /* transform-box: fill-box;      
  transform-origin: center;  */
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
  color: black;
}
</style>
