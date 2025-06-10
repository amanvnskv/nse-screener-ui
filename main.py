from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "NSE Screener API is running. Use /screener to access data."}

@app.get("/screener")
def run_screener():
    symbols = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]
    results = []

    for symbol in symbols:
        try:
            data = yf.download(symbol, interval="30m", period="1d", progress=False)
            if len(data) >= 2:
                latest = data.iloc[-1]
                prev = data.iloc[-2]
                if latest["Close"] > prev["High"]:
                    results.append({
                        "symbol": symbol,
                        "price": round(latest["Close"], 2),
                        "breakout_above": round(prev["High"], 2)
                    })
        except Exception as e:
            print(f"Error for {symbol}: {e}")

    return {"screener_results": results}
