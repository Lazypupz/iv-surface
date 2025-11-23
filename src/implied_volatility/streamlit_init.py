import streamlit as st

##python -m streamlit run src/implied_volatility/main.py

## add input for call/puts
class Sidebar: 
    def __init__(self):
        self.ticker = None
        self.expiry = None
    
    def find_ticker(self):
        st.sidebar.header("Select Ticker")
        ticker = st.sidebar.text_input("Ticker", "AAPL", key="sidebar_ticker_input")
        isSubmitPressed = st.sidebar.button("Submit", key="sidebar_ticker_submit")

        if isSubmitPressed:
            if (ticker == '') or (not ticker.isalpha()):
                st.sidebar.error("Please enter a valid ticker symbol.") 
                return None
            return ticker
        
        return None

    def select_expiry(self, yf_ticker):
        if yf_ticker is None:
            st.sidebar.error("Invalid ticker or no options data available.")
            return None
        expiries = yf_ticker.options

        if not expiries:
            st.sidebar.error("This ticker has no options data available.") 
            return None
        
        expiry_options = ["All Expiries"] + list(expiries)
        expiry = st.sidebar.selectbox("Select Expiry", expiry_options, key="sidebar_expiry_select", index=0)

        # Return None if "All Expiries" is selected, otherwise return the selected expiry
        return None if expiry == "All Expiries" else expiry
    
    def select_option_type(self):
        option_type = st.sidebar.selectbox("Select Option Type", ["call", "put"], key="sidebar_option_type_select")
        return option_type

def init_streamlit():
    st.title("Implied Volatility Surface")
    st.write("This app calculates the implied volatility of options using the Black-Scholes model. And visualizes the volatility surface.")

    st.sidebar.header("User Input Parameters")


