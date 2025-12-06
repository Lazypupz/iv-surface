import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import data_clean as dc
from scipy.interpolate import griddata


def _normalize_df(df):
    df = df.copy()
    df["impliedVolatility"] = pd.to_numeric(df["impliedVolatility"], errors='coerce')
    df = df.dropna(subset=["impliedVolatility", "strike", "T"])
    df = df[(df["impliedVolatility"] > 0.01) & (df["impliedVolatility"] < 3.0)]
    return df

def create_3d_surface(df, option_type):
    df, X, Y, Z, points, values = dc.cleanAndProcess_option_data(df=None)
    if df.empty and df.shape[0] < 4:
        st.info("Not enuf data bruv")
        return df


    nan_mask = np.isnan(Z)
    if nan_mask.any():
        Z[nan_mask] = griddata(points, values, (X[nan_mask], Y[nan_mask]), method="nearest")

    surface = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale="Earth")]) #Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot, # for colorscale options see https://plotly.com/python/colorscales/
    surface.update_layout(title=f"({option_type}) Implied Volatility Surface",  #Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd.
                          autosize=True,
                          width = 800,
                          height = 800,
                          scene=dict(
                                xaxis_title="Strike Price",
                                yaxis_title="Time to Expiry (in years)",
                                zaxis_title="Implied Volatility",
    ))

    st.plotly_chart(surface, use_container_width=True)
    print(df.groupby("T")["impliedVolatility"].describe())


def make_skew_plot(df, option_type, selected_expiry):
    skew_df = df[["strike", "impliedVolatility"]].dropna()
    if skew_df.empty:
        st.info("No data for selected expiry")
        return

    skew_df = skew_df.sort_values('strike')

    skew_fig = go.Figure()
    skew_fig.add_trace(go.Scatter(x=skew_df['strike'], y=skew_df["impliedVolatility"],
                            mode='lines+markers', name='IV'))
    title = f'({option_type}) IV Skew for {selected_expiry}' if selected_expiry is not None else 'Call IV Skew'
    skew_fig.update_layout(title=title, xaxis_title='Strike', yaxis_title="impliedVolatility")

    return skew_fig


def plot_graph(df, option_type, selected_expiry):
    df = _normalize_df(df)

    if df.empty:
        st.info(f"No {option_type} option data available to plot.")
        return
    
    if selected_expiry is None:
        create_3d_surface(df, option_type)
    else:
        skew_fig = make_skew_plot(df, option_type, selected_expiry)
        if skew_fig:
            st.plotly_chart(skew_fig, use_container_width=True)
        
    return

'''
def _filter_options_at_expiry(df, selected_expiry):
    df = df.copy()

    if selected_expiry is None:
        return
    options_at_expiry = df[df["expiry"] == pd.to_datetime(selected_expiry).date()]
    filtered_options_at_expiry = options_at_expiry[options_at_expiry["daystoexpiry"] == 0]
    filtered_options_at_expiry = filtered_options_at_expiry[filtered_options_at_expiry["impliedVolatility"] > 0.001]

def _filter_options_at_strike(df, strike_price):
    df = df.copy()

    options_at_strike = df[df["strike"] == strike_price]
    filtered_options_at_strike = options_at_strike[options_at_strike["impliedVolatility"] > 0.001]
    return filtered_options_at_strike
'''

    
    
    