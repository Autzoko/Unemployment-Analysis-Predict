import pandas as pd
import os
from tqdm import tqdm
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
from pmdarima import auto_arima
import warnings
warnings.filterwarnings("ignore")

# Step 1: Read data
data_path = "D:/NYU_research/big_data/raw/raw/states_filtered/all_filtered_data.txt"
df = pd.read_csv(data_path, sep='\t')

# Create directory to save forecast results
os.makedirs("result", exist_ok=True)

# Group by state
grouped = df.groupby('state_name')

# Store all forecast results
all_forecasts = []

# Process each state
for state, pandas_df in tqdm(grouped, desc="Processing States"):
    if pandas_df.empty:
        print(f"{state} data is empty, skipping.")
        continue

    try:
        # Data preprocessing
        pandas_df['period'] = pandas_df['period'].str.replace('M', '')
        pandas_df['month'] = pandas_df['period'].astype(int)
        pandas_df = pandas_df[pandas_df['month'] != 13]

        pandas_df['timestamp'] = pd.to_datetime(
            pandas_df['year'].astype(str) + '-' + pandas_df['month'].astype(str) + '-01',
            format='%Y-%m-%d'
        )
        pandas_df = pandas_df.sort_values('timestamp')

        pandas_df['value'] = pd.to_numeric(pandas_df['value'], errors='coerce')
        pandas_df = pandas_df.dropna(subset=['value'])

        if len(pandas_df) < 36:
            print(f"{state} has too little data ({len(pandas_df)} rows), skipping.")
            continue

        # Split into training and validation sets
        split_idx = int(len(pandas_df) * 0.8)
        train_series = pandas_df['value'].iloc[:split_idx]
        valid_series = pandas_df['value'].iloc[split_idx:]
        valid_len = len(valid_series)

        # Fit seasonal auto-ARIMA model
        auto_model = auto_arima(
            train_series,
            seasonal=True,
            m=12,
            trace=False,
            suppress_warnings=True,
            error_action="ignore",
            stepwise=True
        )

        # Forecast on validation set
        val_forecast = auto_model.predict(n_periods=valid_len)

        # Calculate error metrics
        mae = mean_absolute_error(valid_series, val_forecast)
        rmse = mean_squared_error(valid_series, val_forecast, squared=False)
        mape = np.mean(np.abs((valid_series - val_forecast) / valid_series)) * 100

        print(f"[{state}] MAE: {mae:.2f}, RMSE: {rmse:.2f}, MAPE: {mape:.2f}%")

        # Optional: Uncomment to fit final model and forecast next 12 months
        auto_model_final = auto_arima(
            pandas_df['value'],
            seasonal=True,
            m=12,
            trace=False,
            suppress_warnings=True,
            error_action="ignore",
            stepwise=True
        )
        
        n_periods = 12
        forecast = auto_model_final.predict(n_periods=n_periods)
        last_timestamp = pandas_df['timestamp'].max()
        future_dates = pd.date_range(last_timestamp + pd.offsets.MonthBegin(1), periods=n_periods, freq='MS')
        series_id = pandas_df['series_id'].iloc[0]
        
        forecast_df = pd.DataFrame({
            'series_id': [series_id] * n_periods,
            'year': future_dates.year,
            'period': ['M' + str(month).zfill(2) for month in future_dates.month],
            'value': forecast,
            'state_name': [state] * n_periods
        })
        
        save_path = f"./result/{state}_predict.csv"
        forecast_df.to_csv(save_path, index=False)
        all_forecasts.append(forecast_df)

    except Exception as e:
        print(f"{state} model failed, skipping. Error: {e}")
