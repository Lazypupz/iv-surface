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
    chains = pd.DataFrame()

    calls = st_ticker.option_chain(expiry).calls
    calls["optionType"] = "call"

    puts = st_ticker.option_chain(expiry).puts
    puts["optionType"] = "put"

    chain = pd.concat([calls, puts])
    chain["expiry"] = pd.to_datetime(expiry)

    chains = pd.concat([chains, chain])
    chains["daystoexpiry"] = (chains["expiry"] - pd.Timestamp.now()).dt.days
    return chains


def gather_recent_option_call(st_ticker, expiry):
    
    try:

        chains = option_chains(st_ticker, expiry)

        if expiry is None:
            st.sidebar.error("No expiry date selected.")
            return None

        hist = st_ticker.history(period="5d")
        if hist.empty:
            raise ValueError("No historical data found for this ticker.")
            return None 
        spotprice = hist['Close'].iloc[-1]

        calls = chains[chains["optionType"] == 'call']
        if calls.empty:
            st.sidebar.error('This ticker does not have call options data.') 
            return None
        call_strikeprice = calls['strike'].iloc[0]

        puts = chains[chains["optionType"] == 'put']
        if puts.empty:
            st.sidebar.error('This ticker does not have put options data.') 
            return None
        put_strikeprice = puts["strike"].iloc[0]

        expiry_date = datetime.strptime(expiry, '%Y-%m-%d').date()
        today = datetime.now().date()
        time_until_expiry = (expiry_date - today).days / 252

        risk_free_rate = 0.01 ##static 1% for now

        return spotprice, call_strikeprice, put_strikeprice, time_until_expiry, risk_free_rate, puts, calls
    except (IndexError, KeyError, ValueError, AttributeError) as e:
        st.sidebar.error(f"Error fetching options data: {e}") 
        return None

def fetch_data(ticker, expiry=None):


    if not ticker:
        st.sidebar.error("Ticker not provided.")
        return None

    valid, st_ticker = check_ticker_input(ticker)
    if not valid:
        return None

    if expiry is None: ## all expiries is selected
        available_expiries = st_ticker.options
        if not available_expiries:
            st.sidebar.error("No expirations available for this ticker.")
            return None
        
        all_calls = pd.DataFrame()
        all_puts = pd.DataFrame()
        
        for exp in available_expiries:
            try:
                chain = option_chains(st_ticker, exp)
                calls = chain[chain["optionType"] == 'call']
                puts = chain[chain["optionType"] == 'put']
                all_calls = pd.concat([all_calls, calls], ignore_index=True)
                all_puts = pd.concat([all_puts, puts], ignore_index=True)
            except Exception as e:
                continue
        
        if all_calls.empty or all_puts.empty:
            st.sidebar.error("No options data found across available expirations.")
            return None
        
        hist = st_ticker.history(period="20d")
        if hist.empty:
            st.sidebar.error("No historical data found for this ticker.")
            return None
        spotprice = hist['Close'].iloc[-1]
        
        return spotprice, None, None, None, 0.01, all_puts, all_calls
    else:
        # Fetch data for a specific expiry
        option_data = gather_recent_option_call(st_ticker, expiry)
        if option_data is None:
            return None
        return option_data






##call = qfn.BlackScholesCall(spotprice, 0.20, strikeprice, 5/252, riskfreerate)
##print(call.price)

## implied vol 0.20 = 157 market price_vol = 90
## lim vol -> 0 