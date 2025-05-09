import pandas as pd
import statsmodels.api as sm
import os
from tqdm import tqdm

# Step 1: Read large file using pandas
data_path = "D:/NYU_research/big_data/raw/raw/states_filtered/all_filtered_data.txt"
df = pd.read_csv(data_path, sep='\t')

# Create directory to save forecast results
os.makedirs("result", exist_ok=True)

# Step 2: Group data by state_name
grouped = df.groupby('state_name')

# Step 3: Iterate through each state's data
all_forecasts = []

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

        if len(pandas_df) < 24:
            print(f"{state} has too little data ({len(pandas_df)} rows), skipping.")
            continue

        # ARIMA modeling
        model = sm.tsa.ARIMA(
            pandas_df['value'],
            order=(1, 1, 1),
            seasonal_order=(1, 1, 1, 12)
        ).fit()

        # Step 4: Forecast the next 12 months
        n_periods = 12
        forecast = model.forecast(steps=n_periods)

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

        # Save results for each state
        save_path = f"./result/{state}_predict.csv"
        forecast_df.to_csv(save_path, index=False)
        all_forecasts.append(forecast_df)
        print("finish")

    except Exception as e:
        print(f"{state} ARIMA modeling failed, skipping. Error: {e}")
