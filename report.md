# US-unemployment-Analysis-Predict

## Executive summary

# Project Name
**U.S. State Unemployment Rate Analysis and Prediction Platform**

# Brief Summary
The U.S. labor market is a dynamic ecosystem shaped by economic policies, global events, and regional disparities. Analyzing unemployment rates at the state level over time is crucial for policymakers, researchers, and businesses. However, traditional unemployment analysis methods often lack scalability, real-time insights, and predictive capabilities.  
This project aims to build a **Big Data Analytics and Prediction Platform** that leverages distributed computing frameworks and machine learning to process, visualize, and forecast unemployment trends across all 50 U.S. states from 2000 to 2024. The platform will integrate historical data, provide real-time updates, and offer interactive dashboards, empowering stakeholders to explore trends and predict future scenarios accurately.

# Objectives
1. **Data Integration:** Aggregate and clean unemployment data from federal, state, and economic sources into a unified dataset spanning 2000–2024.
2. **Distributed Processing:** Use Hadoop and PySpark to manage and query large-scale data (~315,000 records) efficiently.
3. **Predictive Modeling:** Develop time-series forecasting models (e.g., ARIMA, Prophet) to predict state-level unemployment rates, incorporating economic indicators such as GDP and inflation.
4. **Interactive Visualization:** Build a React.js frontend combined with Matplotlib and Dash to deliver dynamic, state-specific visualizations (e.g., heatmaps, trend lines, forecasts).
5. **Real-time Dashboard:** Implement a Flask backend to serve APIs for real-time data updates and model predictions.
6. **Scalability and Accuracy:** Ensure the system supports future data expansions and concurrent user access while minimizing prediction errors through iterative model training and validation.

# Technologies Used
- **Data Processing & Storage:** Hadoop, PySpark, Pandas, Numpy, BeautifulSoup
- **Machine Learning & Forecasting:** Scikit-learn, PyTorch
- **Models:** ARIMA, LSTM
- **Backend & APIs:** FastAPI (Python), MongoDB, pyMongo
- **Frontend & Visualization:** Vue.js, Matplotlib, Plotly
- **Programming Languages:** Python, SQL, JavaScript

## Code Execution Instructions

### Database

### Backend

#### API

GetUmemploymentRateByYear:

```
GET

Request Params:
year: integer
month: integer

Response Params:
[
    {
        state: 'CA',
        value: 0.05,
    },
    {
        state: 'NY',
        value: 0.06,
    },
    ...
]
```

### Frontend
```BASH
cd web/us-map-interactive
```

```BASH
npm run dev
```
---

#  logic of  `us-map-interactive`

## Overview
This is a **Vue 3 + Vite** frontend project for displaying an interactive map of U.S. unemployment rates, supporting year-by-year data viewing.

---

## 1. Project Structure

```plaintext
us-map-interactive/
├── public/                  # Static assets (icons, favicon, etc.)
│
├── src/
│   ├── assets/               # Static files (images, SVG map, etc.)
│   ├── components/           # Vue components (Map, Sidebar, Controls)
│   ├── router/               # Vue Router configuration
│   ├── views/                # Pages (main HomeView)
│   ├── App.vue               # Root component
│   ├── main.ts               # Project entry file
│
├── package.json              # Project dependencies and scripts
├── vite.config.ts            # Vite configuration
└── tsconfig.json             # TypeScript configuration
```

---

## 2. Core Logic

### main.ts
- Creates the `Vue App` instance.
- Loads the global `router`.
- Mounts the app to the `#app` element.

```ts
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

createApp(App).use(router).mount('#app')
```

---

### router/index.ts
- Basic route configuration: 
  - `/` points to `HomeView.vue`.
- Can be extended for more pages in the future.

```ts
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const routes = [
  { path: '/', component: HomeView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

---

### App.vue
- Root layout component.
- Contains only a `<router-view />` for rendering pages dynamically.

```vue
<template>
  <router-view />
</template>
```

---

### views/HomeView.vue
- Main page displaying the interactive U.S. map and controls.
- Composes several key components:
  - `<USMap />` — Map visualization
  - `<Sidebar />` — Sidebar with detailed info
  - `<YearSelector />` — Year selection control
- Uses reactive state management (via `ref`, `reactive`, or possibly `pinia`).

---

### components/

| Component           | Description |
|:-------------------|:-------------|
| **USMap.vue**       | Renders the U.S. SVG map, handles hover and click events, colors states dynamically. |
| **Sidebar.vue**     | Displays detailed unemployment information of the selected state. |
| **YearSelector.vue**| Allows switching between different years. |
| **ColorLegend.vue** | Shows the color-to-unemployment-rate mapping legend. |

**Note**:  
- The map is controlled via **SVG** manipulation and direct CSS interaction.
- Unemployment data is preloaded or fetched via **JSON**.

---

### assets/
- Stores:
  - U.S. **SVG map files**.
  - Possible images or icons for the UI.
  - Static resources like backgrounds, logos, etc.

---

## 3. Data Flow

1. On page load, unemployment data (e.g., a `unemployment.json`) is preloaded.
2. When the user selects a year:
   - The map colors are updated based on the unemployment rates of that year.
3. When the user hovers or clicks on a state:
   - The sidebar shows the detailed data for that state and selected year.

---

## 4. Overall Structure

```plaintext
main.ts -> App.vue -> router -> HomeView.vue
                          |
                          |-- USMap.vue
                          |-- Sidebar.vue
                          |-- YearSelector.vue
                          |-- ColorLegend.vue
```

**Data update flow:**

```plaintext
YearSelector -> Update selected year
     ↓
Re-render USMap state colors
     ↓
User clicks on a state -> Update Sidebar details
```

---


### Prediction

## Technological Challenges

## Changes in Technology

## Uncovered Aspects from Presentations

## Lessons Learned

## Future Improvements

## Data Sources, and Results
