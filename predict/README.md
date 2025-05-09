# Predict

This project uses the ARIMA method to forecast unemployment data for the next 12 months. The forecast results are saved in the [folder](../dataset/predict).

## Tech Stack
- Data Loading: PySpark, Pandas
- Forecasting: statsmodels

## Usage
```bash
python main.py
python predict.py
```

## tips
- main.py: Preprocesses raw data and aggregates a large file into multiple smaller files.
- predict.py: Fast forecasting script. Since the files are small, in-memory processing is more efficient and PySpark is not required.
- predict.ipynb: Uses PySpark for forecasting. Slower due to SparkSession initialization for each query.
- check_auto.py: Uses auto_arima for modeling. First splits data into training and validation sets to calculate evaluation metrics, then fits the model on the full dataset to forecast future values.