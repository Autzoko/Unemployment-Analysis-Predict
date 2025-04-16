# Big Data Final Project

**U.S. State Unemployment Rate Analysis and Prediction Platform**

## Abstract

## Objectives

## TODO List

- 数据清洗（本周完成）
  - 数据入库
    - 数据筛选（每个州只保留百分比/实际失业人数）✅（貌似没有有问题的数据，但是需要弄清楚seriesid的具体意义）
    - 转化成NoSQL（csv-MongoDB document）✅（考虑是否使用远端repo）
- 前后端
  - 前端（Vue.js）
    - 设计：
      - 年份选择器+地图形式展示各州历史数据和预测数据
  - 后端（Flask/Django）
    - API
      - 获取州+月份特定数据（历史数据）（Spark）
      - 获取预测数据（周+月份）
  - 预测数据
    - 直接写死，预测完数据写入数据库
- 预测模型
## Demo
Demo illustrations.

### For Dev Uses

- To process raw data, run: ```python to_csv.py```, processed data will be generated under `./processed`. For each different *series_id* in state data, they are generated separatedly for different purposes.
- To upload processed data to local (or remote) repository, run ```python repository/upload_mongodb.py```, data will be uploaded to **MongoDB**. All auxiliary data will be stored in *basic_data* collection, data of different states will be stored in *state* collections accordingly.

## Data

[U.S. Unemployment Raw Data Google Drive](https://drive.google.com/file/d/1Fr_achKvi9N5baA5Rz4N1Z3B5xbNQc6L/view?usp=share_link)
*Decompress this data under `dataset/`.*