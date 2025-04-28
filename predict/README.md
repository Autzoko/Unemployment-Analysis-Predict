# Predict

使用ARIMA方法进行预测，预测范围是12个月，预测好的数据存放在 [文件夹](../dataset/predict)

## 技术栈
- 导入数据：pyspark, pandas
- 预测：statmodels
  
## 使用
```bash
python main.py
python predict.py
```

## tips
- main.py: 预处理数据 -> 大文件aggregate到若干个小文件中
- predict.py: 快速预测代码，因为文件较小，故直接in-memory处理更快，且不需要使用pyspark
- predict.ipynb：使用pyspark，较慢，因为每次查询都需要激活sparksession
