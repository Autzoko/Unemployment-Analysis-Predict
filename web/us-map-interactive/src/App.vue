<template>
  <div id="app">
    <h1>美国州失业率地图</h1>

    <!-- 年份选择器 -->
    <div class="year-selector">
      <label for="year">选择年份：</label>
      <select v-model="currentYear" id="year">
        <option v-for="y in availableYears" :key="y" :value="y">{{ y }}</option>
      </select>
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

// 提供给子组件使用
provide('currentYear', currentYear);

// 提供所有可选年份
const availableYears = Object.keys(unemploymentData).map(Number);
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin: 20px;
}

.year-selector {
  margin-bottom: 20px;
  font-size: 18px;
}
</style>
