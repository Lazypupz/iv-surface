import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime

    
def check_ticker_input(ticker):
    try :
        st_ticker = yf.Ticker(ticker)

        _ = st_ticker.history(period="5d")
        return True, st_ticker
    except Exception as e:
        st.sidebar.error(f'Invalid ticker symbol: {e}') 
        return False, None

def option_chains(st_ticker, expiry):

    try:
        calls = st_ticker.option_chain(expiry).calls
        calls["optionType"] = "call"

        puts = st_ticker.option_chain(expiry).puts
        puts["optionType"] = "put"

        chain = pd.concat([calls, puts], ignore_index=True)
    except Exception:
        return pd.DataFrame()

    chain["expiry"] = pd.to_datetime(expiry)
    now = pd.Timestamp.utcnow().replace(tzinfo=None)
    chain["T"] = (chain["expiry"] - now).dt.total_seconds() / (365 * 24 * 3600)

    chain["mid"] = (chain["bid"] + chain["ask"]) / 2.0
    chain["spread"] = (chain["ask"] - chain["bid"])

    return chain

def clean_chain(df):
    """Remove illiquid/Useless Strikes."""

    if df.empty:
        return df

    df = df.copy()

    # Remove bad prices
    df = df.dropna(subset=["bid", "ask", "mid"])

    df = df[df["mid"] > 0]                         # mid must be positive
    df = df[df["spread"] / df["mid"] < 0.25]       # 25% max spread
    df = df[df["T"] > 0]                           # no expired contracts

    if df["strike"].nunique() < 10:
        return pd.DataFrame()

    return df


def fetch_data(ticker, expiry=None):

    if not ticker:
        st.sidebar.error("Ticker not provided.")
        return None

    valid, st_ticker = check_ticker_input(ticker)
    if not valid:
        return None

    hist = st_ticker.history(period="5d")
    if hist.empty:
        st.sidebar.error("No historical data found for ticker")
        return None
    spot = hist["Close"].iloc[-1]

    risk_free_rate = 0.01

    if expiry:
        chain = option_chains(st_ticker, expiry)
        chain = clean_chain(chain)

        if chain.empty:
            st.sidebar.error("No usable options for this expiry")
            return None

        return {
            "spot": spot,
            "r": risk_free_rate,
            "chain": chain
        }

    all_expiries = st_ticker.options
    if not all_expiries:
        st.sidebar.error("No expiries available")
        return None

    frames = []
    for exp in all_expiries:
        df = option_chains(st_ticker, exp)
        df = clean_chain(df)
        if not df.empty:
            frames.append(df)

    if not frames:
        st.sidebar.error("No usable expiries found")
        return None

    all_chains = pd.concat(frames, ignore_index=True)

    return {
        "spot": spot,
        "r": risk_free_rate,
        "chain": all_chains
    }





##call = qfn.BlackScholesCall(spotprice, 0.20, strikeprice, 5/252, riskfreerate)
##print(call.price)

## implied vol 0.20 = 157 market price_vol = 90
## lim vol -> 0 