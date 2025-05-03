<template>
  <div id="app">
    <h1>Unemployment Rates Across U.S. (2000–2026)</h1>

    <div class="selectors-row">
    <!-- 年份选择器 -->
    <div class="year-selector">
      <label for="year">Select Year: </label>
      <select v-model="currentYear" id="year">
        <option v-for="y in availableYears" :key="y" :value="y">{{ y }}</option>
      </select>
    </div>

    <!-- 年份选择器 -->
    <div class="month-selector">
      <label for="month">Select Month: </label>
      <select v-model="currentMonth" id="month">
        <option v-for="y in availableMonths" :key="y" :value="y">{{ y }}</option>
      </select>
    </div>
    </div>

    <!-- 地图组件 -->
    <USMap />
  </div>
</template>

<script setup>
import { ref, provide } from 'vue';
import USMap from './components/USMap.vue';
import { unemploymentData } from './data/unemployment.js';

// 当前选择的年份
const currentYear = ref(2022);
const currentMonth = ref(1);

// 提供给子组件使用
provide('currentYear', currentYear);
provide('currentMonth', currentMonth);

// 提供所有可选年份
const availableYears = Array.from({ length: 2027 - 2000 }, (_, i) => 2000 + i);
const availableMonths = [1,2,3,4,5,6,7,8,9,10,11,12];
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin: 20px;
}

/* .year-selector {
  margin-bottom: 20px;
  font-size: 18px;
}

.month-selector {
  margin-bottom: 20px;
  font-size: 18px;
} */

.selectors-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}
</style>
