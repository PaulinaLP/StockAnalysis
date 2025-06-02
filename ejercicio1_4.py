import pandas as pd
import yfinance as yf
import numpy as np

# 1. Cargar datos de resultados trimestrales desde CSV
earnings_df = pd.read_csv("ha1_Amazon.csv", delimiter=';')
print(earnings_df.head(2))
earnings_df['Earnings Date'] = earnings_df['Earnings Date'].str.replace(r'\s+at\s+\d+\s+(AM|PM)\s+[A-Z]+', '', regex=True)
earnings_df['Earnings Date'] = pd.to_datetime(earnings_df['Earnings Date'])

# 2. Descargar precios históricos
amzn = yf.download('AMZN', start='2005-01-01')
amzn = amzn[['Close']]
amzn = amzn.reset_index()

# 3. Calcular variaciones porcentuales en 2 días (Day1→Day3)
amzn['Close_Day1'] = amzn['Close'].shift(1)
amzn['Close_Day3'] = amzn['Close'].shift(-1)
amzn['2day_return'] = (amzn['Close_Day3'] / amzn['Close_Day1']) - 1

# 4. Unir 
amzn.columns = amzn.columns.to_flat_index()
amzn.columns = [col if isinstance(col, str) else col[0] for col in amzn.columns]
joined = pd.merge(earnings_df, amzn, left_on='Earnings Date', right_on='Date')
joined ['EPS Estimate'] = pd.to_numeric(joined ['EPS Estimate'], errors='coerce')
joined ['Reported EPS'] = pd.to_numeric(joined ['Reported EPS'], errors='coerce')
joined ['Surprise (%)'] = pd.to_numeric(joined ['Surprise (%)'], errors='coerce')
changes = joined[(joined['Reported EPS'] > joined['EPS Estimate']) | (joined["Surprise (%)"] > 0)]
print(changes.head(50))
mediana = changes['2day_return'].median()
print(mediana)


amzn['SMA50'] = amzn['Close'].rolling(50).mean()

# Join this info with earnings data
merged_with_sma = pd.merge(changes, amzn[['Date', 'SMA50']], on='Date', how='left')

# Bull market = Close above 50-day moving average
merged_with_sma['Bull'] = merged_with_sma['Close'] > merged_with_sma['SMA50']

# Split returns by market condition
bull_returns = merged_with_sma[merged_with_sma['Bull'] == True]['2day_return']
bear_returns = merged_with_sma[merged_with_sma['Bull'] == False]['2day_return']

print(f"🐂 Bull market median return: {bull_returns.median() * 100:.2f}%")
print(f"🐻 Bear market median return: {bear_returns.median() * 100:.2f}%")