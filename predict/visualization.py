import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os

# Step 1: Read large file using pandas
data_path = "D:/NYU_research/big_data/raw/raw/states_filtered/all_filtered_data.txt"
df = pd.read_csv(data_path, sep='\t')

# Step 2: Select the state of interest, for example 'California'
series_id = 'LASBS060000000000003          '  # Change this to the state you are interested in

# Step 3: Filter data by state_name (via series_id)
state_df = df[df['series_id'] == series_id]

# Check if the data is empty
if state_df.empty:
    print(f"{series_id} data is empty, cannot visualize.")
else:
    try:
        # Data preprocessing
        state_df['period'] = state_df['period'].str.replace('M', '')
        state_df['month'] = state_df['period'].astype(int)
        state_df = state_df[state_df['month'] != 13]
        
        state_df['timestamp'] = pd.to_datetime(
            state_df['year'].astype(str) + '-' + state_df['month'].astype(str) + '-01',
            format='%Y-%m-%d'
        )
        state_df = state_df.sort_values('timestamp')
        print(state_df)

        state_df['value'] = pd.to_numeric(state_df['value'], errors='coerce')
        state_df = state_df.dropna(subset=['value'])

        # Filter data to include only records from 2000 onwards
        start_date = pd.to_datetime('2000-01-01')
        filtered_df = state_df[state_df['timestamp'] >= start_date]

        # Step 4: ARIMA Forecast (parameters can be adjusted)
        model = sm.tsa.ARIMA(
            filtered_df['value'],
            order=(1, 1, 1),
            seasonal_order=(1, 1, 1, 12)
        ).fit()

        # Forecast the next 12 months
        n_periods = 12
        forecast = model.forecast(steps=n_periods)

        last_timestamp = filtered_df['timestamp'].max()
        future_dates = pd.date_range(last_timestamp + pd.offsets.MonthBegin(1), periods=n_periods, freq='MS')

        forecast_df = pd.DataFrame({
            'timestamp': future_dates,
            'value': forecast,
        })

        # Step 5: Plot Historical and Forecasted Data
        plt.figure(figsize=(10, 6))

        # Plot historical data
        plt.plot(filtered_df['timestamp'], filtered_df['value'], color='blue', label='Historical Data')

        # Plot forecasted data
        plt.plot(forecast_df['timestamp'], forecast_df['value'], color='red', linestyle='--', label='Forecasted Data')

        # Titles and labels
        plt.title('Prediction result')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

        # Add a legend
        plt.legend()

        # Display the plot
        plt.show()

    except Exception as e:
        print(f"Error occurred while processing {series_id}: {e}")
