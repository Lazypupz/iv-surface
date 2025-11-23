import streamlit as st
import streamlit_init as sf
import fetch_data as fd
import plot as pl

def main():
    sf.init_streamlit()
    
    if "ticker" not in st.session_state:
        st.session_state["ticker"] = None
    if "expiry" not in st.session_state:
        st.session_state["expiry"] = None

    #create and persist a single Sidebar instance per session (inorderto prevent duplication)
    if "sidebar" not in st.session_state:
        st.session_state["sidebar"] = sf.Sidebar()
    sidebar = st.session_state["sidebar"]

    new_ticker = sidebar.find_ticker()
    if new_ticker is not None:
        st.session_state["ticker"] = new_ticker

    if st.session_state["ticker"]:
        isValidTicker, yf_ticker = fd.check_ticker_input(st.session_state["ticker"])
        if isValidTicker:
            # keeps expiry selection constant unless selected otherwise
            new_expiry = sidebar.select_expiry(yf_ticker)
            if new_expiry is not None:
                st.session_state["expiry"] = new_expiry
            elif new_expiry is None:
                # "All Expiries" was selected (None means all expiries)
                st.session_state["expiry"] = None
            new_option_type = sidebar.select_option_type()
            if new_option_type is not None:
                st.session_state["option_type"] = new_option_type

    if st.session_state["ticker"]:

        selected_expiry = st.session_state.get("expiry")
        option_data = fd.fetch_data(st.session_state["ticker"], selected_expiry)
        option_type = st.session_state.get("option_type")

        if option_data is not None and option_type == "call":
            spotprice, call_strikeprice, put_strikeprice, time_until_expiry, risk_free_rate, puts, calls = option_data

            pl.plot_graph(calls, option_type, selected_expiry)
        elif option_data is not None and option_type == "put":
            spotprice, call_strikeprice, put_strikeprice, time_until_expiry, risk_free_rate, puts, calls = option_data

            pl.plot_graph(puts, option_type, selected_expiry)

if __name__ == "__main__":
    main()
