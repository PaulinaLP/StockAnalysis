import yfinance as yf
import pandas as pd

# Diccionario de índices
indices = {
    "China - Shanghai Composite": "000001.SS",
    "Hong Kong - Hang Seng": "^HSI",
    "Australia - ASX 200": "^AXJO",
    "India - Nifty 50": "^NSEI",
    "Canada - TSX": "^GSPTSE",
    "Germany - DAX": "^GDAXI",
    "UK - FTSE 100": "^FTSE",
    "Japan - Nikkei 225": "^N225",
    "Mexico - IPC": "^MXX",
    "Brazil - Ibovespa": "^BVSP"
}

# Rango de fechas para el YTD
start_date = "2025-01-01"
end_date = "2025-05-01"
s_p=yf.download(start=start_date, end=end_date, tickers = "^GSPC",
                     period = "max",
                     interval = "1d")    
start=s_p['Close'].iloc[0]
close=s_p['Close'].iloc[-1]
s_p_returns=float((close-start)/start)
print(s_p_returns)
sup_s_p=0
for index in list(indices.values()):
    data = yf.download(start=start_date, end=end_date, tickers = index,
                     period = "max",
                     interval = "1d")
    start=data['Close'].iloc[0]
    close=data['Close'].iloc[-1]
    returns=float((close-start)/start)
    print(returns)
    if returns > s_p_returns:
        sup_s_p=sup_s_p+1
print(sup_s_p)
