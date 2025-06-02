import yfinance as yf
import pandas as pd
import numpy as np

# Step 1: Download S&P 500 data
sp500 = yf.download("^GSPC", start="1950-01-01", period="max", interval="1d")
sp500.columns = sp500.columns.to_flat_index()
sp500.columns = [col if isinstance(col, str) else col[0] for col in sp500.columns]
sp500 = sp500[['Close']].dropna()

# Step 2: Identify all-time highs
sp500['AllTimeHigh'] = sp500['Close'].cummax()
all_time_highs = sp500[sp500['Close'] == sp500['AllTimeHigh']]

# Step 3: For each pair of all-time highs, check for drawdowns between them
corrections = []
high_dates = all_time_highs.index

for i in range(len(high_dates) - 1):
    start_date = high_dates[i]
    end_date = high_dates[i + 1]
    period = sp500.loc[start_date:end_date]

    # Find the minimum close price and when it occurred
    min_close = period['Close'].min()
    min_date = period['Close'].idxmin()

    # Calculate drawdown relative to the starting all-time high
    high_price = period.loc[start_date, 'Close']
    drawdown_pct = (high_price - min_close) / high_price * 100

    if drawdown_pct >= 5:
        duration = (min_date.to_pydatetime().date() - start_date.to_pydatetime().date()).days
        corrections.append({'start_date': start_date, 'min_date': min_date, 'duration_days': duration})       

# Step 4: Get durations and calculate percentiles
durations = pd.Series([c['duration_days'] for c in corrections])
percentiles = durations.quantile([0.25, 0.5, 0.75])

# Step 5: Output results
print("Correction durations (in days):")
print(durations.describe())
print("\n25th / 50th (median) / 75th percentiles:")
print(percentiles)

# Optional: Print top corrections
print("\nSample corrections:")
for c in corrections[:100]:
    print(c)