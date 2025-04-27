# US-unemployment-Analysis-Predict

## Executive summary


## Code Execution Instructions

### Database

### Backend

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

# This is a Heading h1
## This is a Heading h2
###### This is a Heading h6

## Emphasis

*This text will be italic*  
_This will also be italic_

**This text will be bold**  
__This will also be bold__

_You **can** combine them_

## Lists

### Unordered

* Item 1
* Item 2
* Item 2a
* Item 2b
    * Item 3a
    * Item 3b

### Ordered

1. Item 1
2. Item 2
3. Item 3
    1. Item 3a
    2. Item 3b

## Images

![This is an alt text.](/image/sample.webp "This is a sample image.")

## Links

You may be using [Markdown Live Preview](https://markdownlivepreview.com/).

## Blockquotes

> Markdown is a lightweight markup language with plain-text-formatting syntax, created in 2004 by John Gruber with Aaron Swartz.
>
>> Markdown is often used to format readme files, for writing messages in online discussion forums, and to create rich text using a plain text editor.

## Tables

| Left columns  | Right columns |
| ------------- |:-------------:|
| left foo      | right foo     |
| left bar      | right bar     |
| left baz      | right baz     |

## Blocks of code

```
let message = 'Hello world';
alert(message);
```

## Inline code

This web site is using `markedjs/marked`.
